"""Environment adapter for the evidence-collection env.

Wires the data loader and the rollout helper together behind SkillOpt's
``EnvAdapter`` interface. Register it in ``scripts/train.py`` /
``scripts/eval_only.py`` per the README.
"""

from __future__ import annotations

from typing import Optional

from .dataloader import EvidenceCollectionDataLoader
from .rollout import run_batch
from .verifier import JudgeFn

try:
    from skillopt.envs.base import EnvAdapter
except Exception:  # pragma: no cover - standalone import for review/tests.
    class EnvAdapter:  # minimal shim mirroring the documented ABC
        pass


class EvidenceCollectionAdapter(EnvAdapter):
    """Task types double as the grouping SkillOpt uses to balance batches."""

    TASK_TYPES = ["document_review", "records_sampling", "interview", "technical_evidence"]

    def __init__(self, judge_fn: Optional[JudgeFn] = None):
        self.loader = EvidenceCollectionDataLoader()
        self.judge_fn = judge_fn

    def get_task_types(self) -> list[str]:
        return list(self.TASK_TYPES)

    def build_train_env(self, batch_size: int, seed: int, **kwargs):
        return {"role": "train", "batch_size": batch_size, "seed": seed, **kwargs}

    def build_eval_env(self, env_num: int, split: str, seed: int, **kwargs):
        return {"role": "eval", "env_num": env_num, "split": split, "seed": seed, **kwargs}

    def rollout(self, env_manager, skill_content: str, out_dir: str, **kwargs) -> list[dict]:
        split_path = kwargs.get("split_path") or env_manager.get("split_path")
        items = self.loader.load_split_items(split_path)
        return run_batch(
            items=items,
            skill_content=skill_content,
            out_root=out_dir,
            workers=kwargs.get("workers", 4),
            max_completion_tokens=kwargs.get("max_completion_tokens", 4096),
            judge_fn=self.judge_fn,
        )
