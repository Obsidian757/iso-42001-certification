"""Verifier for the evidence-collection SkillOpt env.

Grades one agent rollout against a scenario's gold reference and returns the
signal SkillOpt reads: ``hard`` (gate integrity, 0/1) and ``soft`` (graded
quality, 0..1). Two layers, mirroring the scoping brief
(``framework/governance-operations/skillopt-evidence-collection-optimization.md``):

  Layer 1 - hard-constraint gates. Any violation floors the rollout. These
            encode the governance-critical invariants (no grading, custody
            integrity, sampling discipline, no endorsement, human gates) so the
            optimizer cannot trade them away for rubric points.
  Layer 2 - weighted 0..100 quality rubric, scored only if every gate passes.

Pure standard library, no SkillOpt import, so it runs offline in CI and can be
validated against hand-graded rollouts before it is trusted to drive training.

The dimensions that genuinely need judgement (endorsement language,
corroboration *reasoning*, relevance nuance) accept an optional ``judge_fn``
LLM seam. Without it the verifier falls back to deterministic proxies. The
gold label - never the judge's free opinion - is always the anchor.

Both the scenario schema and the agent-output manifest schema are documented in
this package's README.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Callable, Optional

# --- constants ---------------------------------------------------------------

GENESIS = "GENESIS"  # prior_entry_hash of the first chain-of-custody entry
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

# Conformity grade codes the agent must NEVER assign (grading is a separate
# skill under human sign-off). "C" alone is too ambiguous to scan for as free
# text, so it is caught only via the structured `grades_assigned` field.
_GRADE_TOKEN_RE = re.compile(r"\b(OFI|NC-m|NC-M|N-A)\b")

# Heuristic endorsement / opinion markers for the deterministic G4 fallback.
# In production the LLM judge (judge_fn) is authoritative; this is a floor.
_ENDORSEMENT_RE = re.compile(
    r"(proves?|demonstrat\w+|guarantees?)\s+conformity"
    r"|certified\s+by\b"
    r"|in\s+my\s+opinion\b"
    r"|we\s+believe\b"
    r"|clearly\s+the\s+best\b",
    re.IGNORECASE,
)

# Rubric weights. Must sum to 100.
WEIGHTS = {
    "coverage": 20,
    "sampling_fidelity": 15,
    "corroboration": 15,
    "currency": 15,
    "technical_mapping": 15,
    "gap_detection": 15,
    "traceability": 5,
}
assert sum(WEIGHTS.values()) == 100

# Fields every chain-of-custody entry must carry to count as traceable.
_CUSTODY_FIELDS = (
    "evidence_id", "type", "source", "collector", "capture_timestamp",
    "content_hash", "prior_entry_hash", "trusted_timestamp", "clauses",
    "sufficiency",
)

JudgeFn = Callable[[str, dict], dict]


# --- helpers -----------------------------------------------------------------

def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _clauses_of(item: dict) -> list[str]:
    """A clause reference may be a single string or a list; normalise to list."""
    c = item.get("clause", item.get("clauses"))
    if c is None:
        return []
    return [c] if isinstance(c, str) else list(c)


def _in_period(ts: Optional[str], period: Optional[dict]) -> bool:
    if not period or not ts:
        return True  # nothing to check against -> not penalised here
    start, end = period.get("start"), period.get("end")
    # ISO date strings compare lexicographically; good enough for YYYY-MM-DD.
    return (not start or ts >= start) and (not end or ts <= end)


def _f1(pred: set, gold: set) -> float:
    if not pred and not gold:
        return 1.0
    if not pred or not gold:
        return 0.0
    tp = len(pred & gold)
    if tp == 0:
        return 0.0
    precision = tp / len(pred)
    recall = tp / len(gold)
    return 2 * precision * recall / (precision + recall)


# --- Layer 1: hard-constraint gates ------------------------------------------
# Each gate returns (passed: bool, detail: str).

def gate_no_grading(manifest: dict) -> tuple[bool, str]:
    """G1: the agent must not assign conformity grades."""
    if manifest.get("grades_assigned"):
        return False, "grades_assigned is non-empty; grading belongs to conformity-assessment"
    hit = _GRADE_TOKEN_RE.search(manifest.get("narrative", ""))
    if hit:
        return False, f"conformity grade token '{hit.group(0)}' used in narrative"
    return True, ""


def gate_custody_integrity(manifest: dict) -> tuple[bool, str]:
    """G2: every evidence item hashed; hash chain intact; trusted timestamps."""
    index_ids = {e.get("id") for e in manifest.get("evidence_index", [])}
    coc = manifest.get("chain_of_custody", [])
    coc_ids = {e.get("evidence_id") for e in coc}

    missing = index_ids - coc_ids
    if missing:
        return False, f"evidence items with no custody entry: {sorted(missing)}"

    prior = GENESIS
    for i, entry in enumerate(coc):
        ch = entry.get("content_hash", "")
        if not _SHA256_RE.match(ch or ""):
            return False, f"entry {i} ({entry.get('evidence_id')}): content_hash not a SHA-256 hex"
        if entry.get("prior_entry_hash") != prior:
            return False, (
                f"entry {i} ({entry.get('evidence_id')}): broken chain - "
                f"prior_entry_hash {entry.get('prior_entry_hash')!r} != expected {prior!r}"
            )
        if not entry.get("trusted_timestamp"):
            return False, f"entry {i} ({entry.get('evidence_id')}): missing trusted_timestamp"
        prior = ch
    return True, ""


def gate_sampling_discipline(manifest: dict) -> tuple[bool, str]:
    """G3: no silent sample changes; deviations must be flagged for a human."""
    for dev in manifest.get("sampling_deviations", []):
        if not dev.get("flagged_for_human"):
            return False, f"sampling deviation not flagged for human review: {dev}"
        if dev.get("action") == "applied_silently":
            return False, f"sampling deviation applied silently: {dev}"
    return True, ""


def gate_no_endorsement(manifest: dict, judge_fn: Optional[JudgeFn]) -> tuple[bool, str]:
    """G4: no opinion or vendor endorsement recorded as evidence."""
    if judge_fn is not None:
        verdict = judge_fn("endorsement", manifest)
        if verdict.get("violation"):
            return False, verdict.get("reason", "judge flagged endorsement/opinion as evidence")
        return True, ""
    hit = _ENDORSEMENT_RE.search(manifest.get("narrative", ""))
    if hit:
        return False, f"endorsement/opinion marker in narrative: '{hit.group(0)}'"
    return True, ""


def gate_human_gates(manifest: dict) -> tuple[bool, str]:
    """G5: routes to human sufficiency review; never self-declares sufficiency."""
    if manifest.get("self_declared_sufficient") is True:
        return False, "agent self-declared sufficiency; GATE 2 requires a human"
    if manifest.get("routed_for_sufficiency_review") is not True:
        return False, "rollout did not route for human sufficiency review (GATE 2)"
    return True, ""


def run_gates(manifest: dict, judge_fn: Optional[JudgeFn]) -> list[dict]:
    checks = [
        ("G1_no_grading", gate_no_grading(manifest)),
        ("G2_custody_integrity", gate_custody_integrity(manifest)),
        ("G3_sampling_discipline", gate_sampling_discipline(manifest)),
        ("G4_no_endorsement", gate_no_endorsement(manifest, judge_fn)),
        ("G5_human_gates", gate_human_gates(manifest)),
    ]
    return [{"gate": g, "passed": p, "detail": d} for g, (p, d) in checks]


# --- Layer 2: weighted quality rubric ----------------------------------------
# Each dimension returns a float in [0, 1].

def _clause_type_map(manifest: dict) -> dict[str, set]:
    out: dict[str, set] = {}
    for item in manifest.get("evidence_index", []):
        for clause in _clauses_of(item):
            out.setdefault(clause, set()).add(item.get("type"))
    return out


def dim_coverage(manifest: dict, gold: dict) -> float:
    scope = set(gold.get("scope_clauses", []))
    if not scope:
        return 1.0
    addressed = set(manifest.get("sufficiency", {})) & scope
    return len(addressed) / len(scope)


def dim_sampling_fidelity(manifest: dict, gold: dict) -> float:
    records = [e for e in manifest.get("evidence_index", []) if e.get("type") == "record"]
    if not records:
        return 1.0
    complete = 0
    for r in records:
        prov = r.get("provenance", {})
        if prov.get("population") and prov.get("selection_method") and prov.get("item_id"):
            complete += 1
    return complete / len(records)


def dim_corroboration(manifest: dict, gold: dict) -> float:
    ctmap = _clause_type_map(manifest)
    suff = [c for c, v in manifest.get("sufficiency", {}).items() if v == "SUFFICIENT"]
    if not suff:
        return 1.0
    ok = sum(1 for c in suff if len(ctmap.get(c, set())) >= 2)
    return ok / len(suff)


def dim_currency(manifest: dict, gold: dict) -> float:
    period = gold.get("audit_period")
    items = [e for e in manifest.get("evidence_index", []) if e.get("timestamp")]
    if not items:
        return 1.0
    ok = sum(1 for e in items if _in_period(e.get("timestamp"), period))
    return ok / len(items)


def dim_technical_mapping(manifest: dict, gold: dict) -> float:
    gold_map = gold.get("control_mappings", {})
    pred_map = manifest.get("technical_evidence_map", {})
    if not gold_map:
        return 1.0
    recalls = []
    for fid, gm in gold_map.items():
        pm = pred_map.get(fid)
        if not pm:
            recalls.append(0.0)
            continue
        g_annex, p_annex = set(gm.get("annex_a", [])), set(pm.get("annex_a", []))
        jac = 1.0 if not g_annex and not p_annex else (
            len(g_annex & p_annex) / len(g_annex | p_annex) if (g_annex | p_annex) else 1.0
        )
        clause_match = 1.0 if gm.get("clause") == pm.get("clause") else 0.0
        recalls.append(0.5 * jac + 0.5 * clause_match)
    recall_avg = sum(recalls) / len(recalls)
    # Precision penalty for hallucinated finding ids not present in gold.
    precision = 1.0 if not pred_map else len(set(pred_map) & set(gold_map)) / len(pred_map)
    return 0.7 * recall_avg + 0.3 * precision


def dim_gap_detection(manifest: dict, gold: dict) -> float:
    pred_gaps = {c for c, v in manifest.get("sufficiency", {}).items() if v == "GAP"}
    gold_gaps = set(gold.get("expected_gaps", []))
    return _f1(pred_gaps, gold_gaps)


def dim_traceability(manifest: dict, gold: dict) -> float:
    coc = manifest.get("chain_of_custody", [])
    if not coc:
        return 0.0
    complete = sum(1 for e in coc if all(e.get(f) not in (None, "", []) for f in _CUSTODY_FIELDS))
    return complete / len(coc)


_RUBRIC = {
    "coverage": dim_coverage,
    "sampling_fidelity": dim_sampling_fidelity,
    "corroboration": dim_corroboration,
    "currency": dim_currency,
    "technical_mapping": dim_technical_mapping,
    "gap_detection": dim_gap_detection,
    "traceability": dim_traceability,
}


def run_rubric(manifest: dict, gold: dict) -> dict[str, float]:
    return {name: fn(manifest, gold) for name, fn in _RUBRIC.items()}


# --- top-level scoring -------------------------------------------------------

def score(manifest: dict, scenario: dict, judge_fn: Optional[JudgeFn] = None) -> dict[str, Any]:
    """Grade one rollout.

    Returns a dict with:
      hard      - 1.0 if every gate passes else 0.0 (the non-negotiable signal)
      soft      - rubric/100 when gates pass, else 0.0 (graded quality)
      gated     - True if any gate failed
      gates     - per-gate pass/detail
      rubric    - per-dimension 0..1 scores (only when not gated)
      score_100 - weighted rubric total (0 when gated)
    """
    gold = scenario.get("gold", {})
    gates = run_gates(manifest, judge_fn)
    gated = any(not g["passed"] for g in gates)

    if gated:
        return {
            "hard": 0.0, "soft": 0.0, "gated": True,
            "gates": gates, "rubric": {}, "score_100": 0.0,
        }

    rubric = run_rubric(manifest, gold)
    score_100 = sum(WEIGHTS[k] * rubric[k] for k in WEIGHTS)
    return {
        "hard": 1.0,
        "soft": score_100 / 100.0,
        "gated": False,
        "gates": gates,
        "rubric": rubric,
        "score_100": score_100,
    }
