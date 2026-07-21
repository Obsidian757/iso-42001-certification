"""Data loader for the evidence-collection env.

Implements the one mandatory SkillOpt hook, ``load_split_items``. Each split is
a directory of scenario JSON files (see this package's README for the scenario
schema). The gold reference travels *inside* each item under ``"gold"``; the
rollout must never show that key to the agent - only the verifier reads it.
"""

from __future__ import annotations

import json
from pathlib import Path

try:  # SkillOpt provides the base class when installed.
    from skillopt.data import SplitDataLoader
except Exception:  # pragma: no cover - lets the file import standalone for review/tests.
    class SplitDataLoader:  # minimal shim mirroring the documented interface
        def load_split_items(self, split_path: str) -> "list[dict]":
            raise NotImplementedError


class EvidenceCollectionDataLoader(SplitDataLoader):
    def load_split_items(self, split_path: str) -> list[dict]:
        items: list[dict] = []
        for path in sorted(Path(split_path).glob("*.json")):
            with open(path, "r", encoding="utf-8") as fh:
                item = json.load(fh)
            if "id" not in item:
                raise ValueError(f"{path} is missing required 'id' field")
            items.append(item)
        return items
