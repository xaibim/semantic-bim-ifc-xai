from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "docs" / "evidence" / "public_runtime_links.json"
README_PATH = ROOT / "README.md"
SPACE_NOTES_PATH = ROOT / "spaces" / "huggingface" / "SPACE_NOTES.md"
DEMO_PLAN_PATH = ROOT / "demo" / "huggingface-space-plan.md"

EXPECTED_CONTRACT = {
    "artifact_type": "public_runtime_link_registry",
    "artifact_version": "1.0",
    "canonical_repository": "https://github.com/xaibim/semantic-bim-ifc-xai",
    "huggingface": {
        "replay": {
            "official_gateway": "https://huggingface.co/spaces/XAIBIM/semantic-xaibim-replay",
            "interactive_runtime": "https://huggingface.co/spaces/bimaiblend/semantic-xaibim-replay",
            "runtime_maintainer_namespace": "bimaiblend",
        },
        "harness": {
            "official_gateway": "https://huggingface.co/spaces/XAIBIM/semantic-xaibim-harness",
            "interactive_runtime": "https://huggingface.co/spaces/bimaiblend/semantic-xaibim-harness",
            "runtime_maintainer_namespace": "bimaiblend",
        },
    },
    "kaggle_notebook": "https://www.kaggle.com/code/xaibim/semantic-bim-ifc-xai",
    "availability_boundary": (
        "Endpoints may sleep or become temporarily unavailable; link identity is distinct "
        "from current runtime availability."
    ),
}

EXPECTED_URLS = {
    "https://github.com/xaibim/semantic-bim-ifc-xai",
    "https://huggingface.co/spaces/XAIBIM/semantic-xaibim-replay",
    "https://huggingface.co/spaces/bimaiblend/semantic-xaibim-replay",
    "https://huggingface.co/spaces/XAIBIM/semantic-xaibim-harness",
    "https://huggingface.co/spaces/bimaiblend/semantic-xaibim-harness",
    "https://www.kaggle.com/code/xaibim/semantic-bim-ifc-xai",
}

TARGET_FILES = {
    "docs/evidence/public_runtime_links.json",
    "docs/evidence/public_endpoint_audit.json",
    "docs/evidence/public_deployment_manifest.json",
    "README.md",
    "spaces/huggingface/SPACE_NOTES.md",
    "demo/huggingface-space-plan.md",
    "docs/methodology/dataset_construction_and_training_readiness.md",
    "docs/methodology/validation_gates.md",
    "PUBLIC_EVIDENCE.md",
    "tests/test_public_endpoint_evidence.py",
    "tests/test_public_deployment_manifest.py",
    "tests/test_public_narrative_boundaries.py",
    "tests/test_public_runtime_links.py",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_contract() -> dict:
    with CONTRACT_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def gather_urls(value) -> set[str]:
    urls: set[str] = set()
    if isinstance(value, dict):
        for child in value.values():
            urls.update(gather_urls(child))
    elif isinstance(value, list):
        for child in value:
            urls.update(gather_urls(child))
    elif isinstance(value, str) and value.startswith(("http://", "https://")):
        urls.add(value)
    return urls


class TestPublicRuntimeLinks(unittest.TestCase):
    def test_01_contract_json_is_valid_and_exact(self):
        contract = load_contract()
        self.assertEqual(contract, EXPECTED_CONTRACT)
        self.assertEqual(gather_urls(contract), EXPECTED_URLS)

    def test_02_public_documents_use_canonical_gateways(self):
        readme = read_text(README_PATH)
        notes = read_text(SPACE_NOTES_PATH)
        demo_plan = read_text(DEMO_PLAN_PATH)

        for text in (readme, notes, demo_plan):
            self.assertNotIn("BIMAIBlendgineer", text)
            self.assertNotIn("always running", text.lower())
            self.assertNotIn("availability guaranteed", text.lower())

        self.assertIn("https://huggingface.co/spaces/XAIBIM/semantic-xaibim-replay", readme)
        self.assertIn("https://huggingface.co/spaces/XAIBIM/semantic-xaibim-harness", readme)
        self.assertIn("bimaiblend", readme)

        self.assertIn("https://huggingface.co/spaces/XAIBIM/semantic-xaibim-replay", notes)
        self.assertIn("bimaiblend", notes)

        self.assertIn("https://huggingface.co/spaces/XAIBIM/semantic-xaibim-replay", demo_plan)
        self.assertIn("https://huggingface.co/spaces/XAIBIM/semantic-xaibim-harness", demo_plan)
        self.assertIn("bimaiblend", demo_plan)

    def test_03_contract_marks_xaibim_gateways_and_bimaiblend_runtimes(self):
        contract = load_contract()
        hf = contract["huggingface"]

        self.assertTrue(hf["replay"]["official_gateway"].startswith("https://huggingface.co/spaces/XAIBIM/"))
        self.assertTrue(hf["harness"]["official_gateway"].startswith("https://huggingface.co/spaces/XAIBIM/"))
        self.assertEqual(hf["replay"]["runtime_maintainer_namespace"], "bimaiblend")
        self.assertEqual(hf["harness"]["runtime_maintainer_namespace"], "bimaiblend")
        self.assertEqual(
            contract["availability_boundary"],
            EXPECTED_CONTRACT["availability_boundary"],
        )

    def test_04_only_allowed_files_are_modified(self):
        status = subprocess.check_output(
            ["git", "status", "--short", "--untracked-files=all"],
            cwd=ROOT,
            text=True,
        ).splitlines()
        changed_paths: set[str] = set()
        for line in status:
            if not line.strip():
                continue
            path = line[3:] if len(line) > 3 else ""
            changed_paths.add(path.replace("\\", "/"))

        self.assertTrue(changed_paths.issubset(TARGET_FILES), sorted(changed_paths - TARGET_FILES))
