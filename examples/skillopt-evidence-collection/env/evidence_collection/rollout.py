"""Rollout helper for the evidence-collection env.

Implements the SkillOpt ``run_batch`` contract: run the skill against each
scenario with the target model, then score the result. The scored signal
(``hard`` = gate integrity, ``soft`` = graded quality) is what the optimizer
reads, so scoring happens here, inside ``run_batch``, via ``verifier.score``.

The agent is asked to emit a machine-readable ``evidence-manifest.json`` fenced
block alongside its prose deliverables. The verifier grades that manifest
deterministically; the prose files remain the human-facing audit artifacts.
That structured-output contract is what makes the reward reproducible.
"""

from __future__ import annotations

import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

from .verifier import JudgeFn, score

try:  # target-model call provided by SkillOpt at train/eval time.
    from skillopt.model import chat_target
except Exception:  # pragma: no cover
    def chat_target(*args, **kwargs):  # type: ignore
        raise RuntimeError("skillopt.model.chat_target unavailable outside a SkillOpt run")

_MANIFEST_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


def _scenario_prompt(item: dict) -> str:
    """Render the agent-facing task. The 'gold' key is deliberately withheld."""
    visible = {k: v for k, v in item.items() if k != "gold"}
    return (
        "You are performing AIMS internal-audit fieldwork. Using the evidence-collection "
        "skill, collect and log objective evidence for the in-scope clauses below. Produce "
        "the five deliverables, and additionally emit a single fenced ```json block named "
        "evidence-manifest.json capturing your structured results (evidence_index, "
        "sufficiency, technical_evidence_map, chain_of_custody, sampling_deviations, "
        "grades_assigned, routed_for_sufficiency_review, self_declared_sufficient, narrative).\n\n"
        "SCENARIO:\n" + json.dumps(visible, indent=2)
    )


def _parse_manifest(text: str) -> dict:
    matches = _MANIFEST_RE.findall(text or "")
    for blob in reversed(matches):  # last JSON block wins
        try:
            obj = json.loads(blob)
            if isinstance(obj, dict) and "evidence_index" in obj:
                return obj
        except json.JSONDecodeError:
            continue
    return {}  # no parseable manifest -> gates will fail, rollout floored


def _run_one(item: dict, skill_content: str, out_root: str,
             max_completion_tokens: int, judge_fn: Optional[JudgeFn]) -> dict:
    prompt = _scenario_prompt(item)
    reply = chat_target(
        system=skill_content,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=max_completion_tokens,
    )
    text = reply if isinstance(reply, str) else reply.get("content", "")

    pred_dir = Path(out_root) / "predictions" / str(item["id"])
    pred_dir.mkdir(parents=True, exist_ok=True)
    with open(pred_dir / "conversation.json", "w", encoding="utf-8") as fh:
        json.dump({"prompt": prompt, "reply": text}, fh, indent=2)

    manifest = _parse_manifest(text)
    result = score(manifest, item, judge_fn=judge_fn)
    with open(pred_dir / "score.json", "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)

    return {"id": item["id"], "hard": result["hard"], "soft": result["soft"]}


def run_batch(*, items: list[dict], skill_content: str, out_root: str,
              workers: int = 4, max_completion_tokens: int = 4096,
              judge_fn: Optional[JudgeFn] = None) -> list[dict]:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(_run_one, item, skill_content, out_root,
                        max_completion_tokens, judge_fn)
            for item in items
        ]
        return [f.result() for f in futures]
