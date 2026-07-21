# SkillOpt env: optimizing the `evidence-collection` skill

A drop-in [SkillOpt](https://github.com/microsoft/SkillOpt) environment for
training the `evidence-collection` AIMS audit skill. It implements SkillOpt's
env contract and ships a **runnable, offline-testable verifier** — the piece
that decides which skill edits get accepted, and therefore the piece worth
building and trusting first.

This is the buildable companion to the scoping brief at
[`framework/governance-operations/skillopt-evidence-collection-optimization.md`](../../framework/governance-operations/skillopt-evidence-collection-optimization.md).
Read that for the *why*, the dataset plan, and the governance controls; this
README covers the *how*.

> **Status:** working skeleton. The verifier, data loader, rollout, adapter,
> sample scenarios, and tests all run. The dataset is two illustrative
> scenarios, not the 40–60 the brief calls for. The LLM-judge seam (`judge_fn`)
> is optional and stubbed; the deterministic core stands in without it.

## Layout

```
env/evidence_collection/
  verifier.py      # ★ centerpiece: Layer-1 gates + Layer-2 rubric. Pure stdlib.
  dataloader.py    # SplitDataLoader.load_split_items
  rollout.py       # run_batch(...) -> [{id, hard, soft}]; calls chat_target, scores
  adapter.py       # EnvAdapter: build_train_env/build_eval_env/rollout/get_task_types
configs/evidence_collection/default.yaml
data/train, data/val   # labeled scenarios (gold reference travels inside each)
tests/test_verifier.py # validates the verifier against hand-graded rollouts
tools/make_samples.py  # regenerates scenarios + fixtures with valid hash chains
```

## Run it

```bash
cd examples/skillopt-evidence-collection
python tools/make_samples.py               # (re)generate sample data + fixtures
python -m unittest discover -s tests -v    # validate the verifier — no deps, no network
```

No SkillOpt install and no model call are needed for the tests: the verifier is
pure standard library, and the SkillOpt base classes / `chat_target` are guarded
with import shims so every module also imports standalone for review.

## Install into a SkillOpt checkout

1. Copy `env/evidence_collection/` → `skillopt/envs/evidence_collection/`.
2. Copy `configs/evidence_collection/` → `configs/evidence_collection/`.
3. Point `env.skill_init` at the deployed `evidence-collection/SKILL.md` (seed
   verbatim — never blank) and `env.split_dir` at your data root.
4. Register the adapter in `scripts/train.py` and `scripts/eval_only.py`:
   ```python
   try:
       from skillopt.envs.evidence_collection.adapter import EvidenceCollectionAdapter
       _ENV_REGISTRY["evidence_collection"] = EvidenceCollectionAdapter
   except ImportError:
       pass
   ```

## How scoring maps to the SkillOpt signal

`run_batch` returns `{id, hard, soft}` per rollout, which is what the optimizer
reads:

- **`hard` (0/1) — gate integrity.** `1.0` only if *every* Layer-1 gate passes.
  Configure the optimizer so any drop in mean `hard` on validation **rejects**
  the edit outright (`train.gate_regression: reject`). This is how the
  governance-critical invariants stay non-negotiable.
- **`soft` (0..1) — graded quality.** The weighted rubric total ÷ 100, or `0`
  when the rollout is gated. Edits are accepted only on strict `soft`
  improvement on the held-out split (SkillOpt's validation gating).

### Layer 1 — hard-constraint gates (`verifier.run_gates`)

| Gate | Enforces |
|---|---|
| `G1_no_grading` | Agent assigns no conformity grades (C/OFI/NC-m/NC-M/N-A) — grading is `conformity-assessment`'s job. |
| `G2_custody_integrity` | Every evidence item has a SHA-256 content hash; the chain-of-custody hashes link unbroken; trusted timestamps present. |
| `G3_sampling_discipline` | No silent sample changes; any deviation is flagged for the human auditor (GATE 1). |
| `G4_no_endorsement` | No opinion or vendor endorsement recorded as evidence. LLM judge if `judge_fn` supplied; lexical fallback otherwise. |
| `G5_human_gates` | Rollout routes for human sufficiency review and never self-declares sufficiency (GATE 2). |

### Layer 2 — weighted rubric (`verifier.run_rubric`, sums to 100)

`coverage` 20 · `sampling_fidelity` 15 · `corroboration` 15 · `currency` 15 ·
`technical_mapping` 15 · `gap_detection` 15 · `traceability` 5.

Most dimensions are deterministic given the manifest and gold (coverage counts,
tag matches, gap precision/recall, control-mapping overlap, hash-field
completeness). `corroboration` and `currency` also compute deterministically
from evidence types and timestamps. The `judge_fn` seam exists for the nuanced
calls (endorsement, relevance judgement) — but **the gold label, not the
judge's free opinion, is always the anchor.**

## Data contract

### Scenario (input + gold)

Each `data/<split>/*.json` is one unit of fieldwork. Everything except `gold`
is shown to the agent; `gold` is read only by the verifier.

```jsonc
{
  "id": "scenario-0001",
  "task_type": "technical_evidence",
  "audit_period": {"start": "2026-01-01", "end": "2026-06-30"},
  "scope_clauses": ["5.1", "6.1", "8.2", "8.9", "8.10", "8.13"],
  "corpus": { /* simulated auditee documents & records */ },
  "red_swarm_reports": [ /* technical findings to be mapped */ ],
  "gold": {
    "scope_clauses": ["..."],
    "audit_period": {"start": "...", "end": "..."},
    "expected_gaps": ["8.13"],
    "expected_missing_records": ["8.13:monitoring-coverage"],
    "control_mappings": { "finding-001": {"annex_a": ["A.6.2.4"], "clause": "8.9"} }
  }
}
```

### Manifest (agent output the verifier grades)

The rollout asks the agent to emit a fenced ` ```json ` `evidence-manifest.json`
block alongside its five prose deliverables. Grading that structured block is
what keeps the reward reproducible. Shape:

```jsonc
{
  "evidence_index": [
    {"id": "E-001", "type": "document|record|interview|technical",
     "source": "...", "clause": "8.2", "timestamp": "2026-03-04",
     "provenance": {"population": "...", "selection_method": "...", "item_id": "..."}}
  ],
  "sufficiency": {"8.2": "SUFFICIENT", "8.13": "GAP"},
  "technical_evidence_map": {"finding-001": {"annex_a": ["A.6.2.4"], "clause": "8.9"}},
  "chain_of_custody": [
    {"evidence_id": "E-001", "type": "document", "source": "...", "collector": "...",
     "capture_timestamp": "...", "content_hash": "<sha256>", "prior_entry_hash": "GENESIS|<sha256>",
     "trusted_timestamp": "...", "clauses": ["8.2"], "sufficiency": "EVIDENCE-SUFFICIENT"}
  ],
  "sampling_deviations": [],
  "grades_assigned": [],
  "routed_for_sufficiency_review": true,
  "self_declared_sufficient": false,
  "narrative": "..."
}
```

## Before trusting it to train (Phase 1 gate)

`tests/test_verifier.py` is the validate-the-verifier step from the brief: it
confirms a clean rollout passes all gates and scores high, and that each
governance breach (broken hash chain, grading, silent sampling, self-declared
sufficiency, missing manifest) is caught by the right gate and floors the
rollout. Expand this fixture set with real hand-graded rollouts until the
verifier's scores track a senior auditor's before pointing SkillOpt at it.
