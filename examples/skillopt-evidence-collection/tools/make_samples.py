"""Generate internally-consistent sample scenarios and fixture manifests.

Run from the example root:  python tools/make_samples.py
It emits:
  data/train/scenario-0001.json, data/val/scenario-0002.json  (labeled scenarios)
  tests/fixtures/good_manifest.json      (gates pass, high rubric score)
  tests/fixtures/bad_hash_manifest.json  (G2 custody-integrity failure)
  tests/fixtures/grading_manifest.json   (G1 no-grading failure)

The chain-of-custody hashes are computed here so the committed fixtures are
valid; hand-authoring SHA-256 chains by eye is error-prone.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from env.evidence_collection.verifier import GENESIS, sha256_hex  # noqa: E402


def custody_chain(items: list[dict]) -> list[dict]:
    """Build a valid hash-chained custody log from evidence items.

    content_hash = sha256 of the item's canonical content; each entry's
    prior_entry_hash links to the previous entry's content_hash.
    """
    chain, prior = [], GENESIS
    for it in items:
        content_hash = sha256_hex(json.dumps(it, sort_keys=True))
        chain.append({
            "evidence_id": it["id"],
            "type": it["type"],
            "source": it["source"],
            "collector": "agent-run-42",
            "capture_timestamp": it["timestamp"] + "T09:00:00Z",
            "content_hash": content_hash,
            "prior_entry_hash": prior,
            "trusted_timestamp": "tst:" + content_hash[:16],
            "clauses": [it["clause"]],
            "sufficiency": "EVIDENCE-SUFFICIENT",
        })
        prior = content_hash
    return chain


# --- scenario 0001 (train) ---------------------------------------------------

SCENARIO_1 = {
    "id": "scenario-0001",
    "task_type": "technical_evidence",
    "audit_period": {"start": "2026-01-01", "end": "2026-06-30"},
    "scope_clauses": ["5.1", "6.1", "8.2", "8.9", "8.10", "8.13"],
    "corpus": {
        "AIMS-POL-01": {"title": "AI Policy", "version": "3.0", "approved": True, "date": "2026-02-10"},
        "RISK-REG": {"title": "AI Risk Register", "version": "live", "date": "2026-05-01"},
        "IA-8.2": {"title": "AI Impact Assessment - ChatAssist", "signed": True, "date": "2026-03-04"},
    },
    "red_swarm_reports": [
        {"file": "rs-2026-06.json", "findings": [
            {"id": "finding-001", "kind": "prompt_injection", "severity": "high"},
            {"id": "finding-002", "kind": "pii_leakage", "severity": "medium"},
        ]},
    ],
    "gold": {
        "scope_clauses": ["5.1", "6.1", "8.2", "8.9", "8.10", "8.13"],
        "audit_period": {"start": "2026-01-01", "end": "2026-06-30"},
        "expected_gaps": ["8.13"],  # no logging/monitoring evidence in corpus
        "expected_missing_records": ["8.13:monitoring-coverage"],
        "control_mappings": {
            "finding-001": {"annex_a": ["A.6.2.4"], "clause": "8.9"},
            "finding-002": {"annex_a": ["A.7.3"], "clause": "8.10"},
        },
    },
}

# Evidence the ideal rollout would collect for scenario 1. Every SUFFICIENT
# clause is corroborated by two independent evidence types (per the skill's
# sufficiency rule); 8.13 has none and is left as a gap.
EV_1 = [
    {"id": "E-001", "type": "document", "source": "AIMS-POL-01", "clause": "5.1", "timestamp": "2026-02-10"},
    {"id": "E-007", "type": "interview", "source": "Top management (role)", "clause": "5.1", "timestamp": "2026-06-01"},
    {"id": "E-002", "type": "record", "source": "RISK-REG#row-14", "clause": "6.1", "timestamp": "2026-05-01",
     "provenance": {"population": "2026 risk entries", "selection_method": "random n=5", "item_id": "row-14"}},
    {"id": "E-008", "type": "interview", "source": "Risk owner (role)", "clause": "6.1", "timestamp": "2026-06-01"},
    {"id": "E-003", "type": "document", "source": "IA-8.2", "clause": "8.2", "timestamp": "2026-03-04"},
    {"id": "E-004", "type": "interview", "source": "AI Lead (role)", "clause": "8.2", "timestamp": "2026-06-02"},
    {"id": "E-005", "type": "technical", "source": "rs-2026-06.json#finding-001", "clause": "8.9", "timestamp": "2026-06-15"},
    {"id": "E-009", "type": "document", "source": "SEC-PROC-09", "clause": "8.9", "timestamp": "2026-04-20"},
    {"id": "E-006", "type": "technical", "source": "rs-2026-06.json#finding-002", "clause": "8.10", "timestamp": "2026-06-15"},
    {"id": "E-010", "type": "document", "source": "PRIV-DPIA-03", "clause": "8.10", "timestamp": "2026-03-30"},
]

GOOD_MANIFEST = {
    "evidence_index": EV_1,
    "sufficiency": {"5.1": "SUFFICIENT", "6.1": "SUFFICIENT", "8.2": "SUFFICIENT",
                    "8.9": "SUFFICIENT", "8.10": "SUFFICIENT", "8.13": "GAP"},
    "technical_evidence_map": {
        "finding-001": {"annex_a": ["A.6.2.4"], "clause": "8.9"},
        "finding-002": {"annex_a": ["A.7.3"], "clause": "8.10"},
    },
    "chain_of_custody": custody_chain(EV_1),
    "sampling_deviations": [],
    "grades_assigned": [],
    "routed_for_sufficiency_review": True,
    "self_declared_sufficient": False,
    "narrative": "Collected documented, sampled, interview, and technical evidence; "
                 "8.13 monitoring coverage not evidenced - flagged as a gap for the human auditor.",
}

# scenario 0002 (val) reuses the shape with a smaller scope for variety.
SCENARIO_2 = {
    "id": "scenario-0002",
    "task_type": "records_sampling",
    "audit_period": {"start": "2026-01-01", "end": "2026-06-30"},
    "scope_clauses": ["8.2", "8.8"],
    "corpus": {"IA-8.2": {"title": "AI Impact Assessment", "signed": True, "date": "2026-03-04"}},
    "red_swarm_reports": [],
    "gold": {
        "scope_clauses": ["8.2", "8.8"],
        "audit_period": {"start": "2026-01-01", "end": "2026-06-30"},
        "expected_gaps": ["8.8"],
        "expected_missing_records": ["8.8:human-override-log"],
        "control_mappings": {},
    },
}


def _bad_hash(manifest: dict) -> dict:
    import copy
    m = copy.deepcopy(manifest)
    m["chain_of_custody"][2]["content_hash"] = "0" * 64  # breaks linkage for entry 3
    return m


def _grading(manifest: dict) -> dict:
    import copy
    m = copy.deepcopy(manifest)
    m["grades_assigned"] = [{"clause": "8.2", "grade": "C"}]  # forbidden: grading
    m["narrative"] += " Assigned NC-m to 8.13."
    return m


def write(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2)
    print("wrote", path.relative_to(ROOT))


def main() -> None:
    write(ROOT / "data/train/scenario-0001.json", SCENARIO_1)
    write(ROOT / "data/val/scenario-0002.json", SCENARIO_2)
    write(ROOT / "tests/fixtures/good_manifest.json", GOOD_MANIFEST)
    write(ROOT / "tests/fixtures/bad_hash_manifest.json", _bad_hash(GOOD_MANIFEST))
    write(ROOT / "tests/fixtures/grading_manifest.json", _grading(GOOD_MANIFEST))


if __name__ == "__main__":
    main()
