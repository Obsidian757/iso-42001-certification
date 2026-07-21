"""Validate the verifier against hand-graded rollouts (SkillOpt Phase 1).

Before a verifier is trusted to drive training, its scores must track a human's
judgement on known-good and known-bad rollouts. These tests assert exactly that:
a clean rollout passes all gates and scores high; each governance breach is
caught by the right gate and floors the rollout.

Run from the example root:  python -m unittest discover -s tests
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "env"))

from env.evidence_collection.verifier import score  # noqa: E402

FIX = ROOT / "tests" / "fixtures"


def load(name: str) -> dict:
    with open(name, "r", encoding="utf-8") as fh:
        return json.load(fh)


class VerifierTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scenario = load(ROOT / "data/train/scenario-0001.json")
        cls.good = load(FIX / "good_manifest.json")

    def test_good_rollout_passes_all_gates(self):
        r = score(self.good, self.scenario)
        self.assertFalse(r["gated"], msg=r["gates"])
        self.assertEqual(r["hard"], 1.0)

    def test_good_rollout_scores_high(self):
        r = score(self.good, self.scenario)
        # Ideal rollout: full coverage, correct mappings, correct gap => strong soft score.
        self.assertGreater(r["soft"], 0.9)

    def test_gap_detection_matches_gold(self):
        r = score(self.good, self.scenario)
        self.assertEqual(r["rubric"]["gap_detection"], 1.0)

    def test_technical_mapping_correct(self):
        r = score(self.good, self.scenario)
        self.assertEqual(r["rubric"]["technical_mapping"], 1.0)

    def test_broken_hash_chain_is_gated(self):
        r = score(load(FIX / "bad_hash_manifest.json"), self.scenario)
        self.assertTrue(r["gated"])
        self.assertEqual(r["hard"], 0.0)
        self.assertEqual(r["soft"], 0.0)
        failed = [g["gate"] for g in r["gates"] if not g["passed"]]
        self.assertIn("G2_custody_integrity", failed)

    def test_grading_is_gated(self):
        r = score(load(FIX / "grading_manifest.json"), self.scenario)
        self.assertTrue(r["gated"])
        failed = [g["gate"] for g in r["gates"] if not g["passed"]]
        self.assertIn("G1_no_grading", failed)

    def test_missing_manifest_is_gated(self):
        # An empty manifest (agent produced no parseable JSON) must floor, not crash.
        r = score({}, self.scenario)
        self.assertTrue(r["gated"])
        self.assertEqual(r["hard"], 0.0)

    def test_self_declared_sufficiency_is_gated(self):
        m = dict(self.good, self_declared_sufficient=True)
        r = score(m, self.scenario)
        failed = [g["gate"] for g in r["gates"] if not g["passed"]]
        self.assertIn("G5_human_gates", failed)

    def test_silent_sampling_deviation_is_gated(self):
        m = dict(self.good, sampling_deviations=[{"clause": "6.1", "action": "applied_silently"}])
        r = score(m, self.scenario)
        failed = [g["gate"] for g in r["gates"] if not g["passed"]]
        self.assertIn("G3_sampling_discipline", failed)

    def test_weak_corroboration_lowers_score_without_gating(self):
        # Drop the second 8.2 evidence item -> 8.2 SUFFICIENT now single-source.
        m = json.loads(json.dumps(self.good))
        m["evidence_index"] = [e for e in m["evidence_index"] if e["id"] != "E-004"]
        # keep custody consistent by dropping the matching entry too
        m["chain_of_custody"] = [c for c in m["chain_of_custody"] if c["evidence_id"] != "E-004"]
        # re-link the chain after removal
        prior = "GENESIS"
        for entry in m["chain_of_custody"]:
            entry["prior_entry_hash"] = prior
            prior = entry["content_hash"]
        r = score(m, self.scenario)
        self.assertFalse(r["gated"], msg=r["gates"])
        self.assertLess(r["rubric"]["corroboration"], 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
