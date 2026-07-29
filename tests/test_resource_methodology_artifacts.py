from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PUBLIC_FILES = [
    ROOT / "docs/methodology/software_and_platform_compatibility.md",
    ROOT / "docs/methodology/resource_capacity_plan.md",
    ROOT / "docs/methodology/data_governance_and_release.md",
    ROOT / "docs/methodology/experimental_scale_and_freeze_manifest.md",
    ROOT / "docs/methodology/human_review_and_operational_risk.md",
    ROOT / "benchmark/resource_calibration.json",
    ROOT / "benchmark/resource_calibration.md",
    ROOT / "docs/evidence/kaggle_qlora_manifest.json",
]


class ResourceMethodologyArtifactsTest(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        missing = [str(path.relative_to(ROOT)) for path in PUBLIC_FILES if not path.is_file()]
        self.assertEqual([], missing)

    def test_public_documents_are_neutral(self) -> None:
        forbidden = ("CPCA", "MyFCT", "application allocation")
        for path in PUBLIC_FILES:
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, f"{token!r} found in {path.relative_to(ROOT)}")

    def test_resource_json_contract(self) -> None:
        data = json.loads((ROOT / "benchmark/resource_calibration.json").read_text(encoding="utf-8"))
        self.assertEqual("resource_capacity_calibration", data["artifact_type"])
        self.assertIn("minimum", data["scenarios"])
        self.assertIn("planned", data["scenarios"])
        self.assertIn("ceiling", data["scenarios"])
        planned = data["scenarios"]["planned"]
        self.assertEqual(20_000, planned["dataset_records"])
        self.assertEqual(20_000, planned["cpu"]["total_core_hours"])
        self.assertEqual(1_500, planned["gpu"]["rounded_planning_envelope_gpu_hours"])
        self.assertEqual(2.0, planned["storage"]["total_tb"])
        self.assertIn("UNMEASURED", planned["gpu"]["assumption_status"])

    def test_optional_adaptation_is_not_core(self) -> None:
        capacity = (ROOT / "docs/methodology/resource_capacity_plan.md").read_text(encoding="utf-8").lower()
        freeze = (ROOT / "docs/methodology/experimental_scale_and_freeze_manifest.md").read_text(encoding="utf-8").lower()
        self.assertIn("optional adaptation is cancelled", capacity)
        self.assertIn("qlora is optional", freeze)


if __name__ == "__main__":
    unittest.main()
