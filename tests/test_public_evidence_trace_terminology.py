from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_PHRASE = "evidence-" + "grounded"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestPublicEvidenceTraceTerminology(unittest.TestCase):
    def test_01_public_artifact_renamed(self):
        readme = read_text(ROOT / "README.md")
        citation = read_text(ROOT / "CITATION.cff")
        self.assertIn("# Semantic BIM/IFC Evidence-Trace Public Research Artifact", readme)
        self.assertIn('title: "Semantic BIM/IFC Evidence-Trace Public Research Artifact"', citation)

    def test_02_no_evidence_grounded_phrase(self):
        paths = [
            ROOT / "README.md",
            ROOT / "CITATION.cff",
            ROOT / "CHANGELOG.md",
            ROOT / "RELEASE_NOTES_v0.1.1-public-validation.md",
            ROOT / "benchmark" / "qlora" / "XAIBIM_QWEN25_7B_QLORA_PRELIMINARY_RESULTS.md",
            ROOT / "benchmark" / "qlora" / "xaibim_qwen25_7b_qlora_preliminary_public_results.json",
        ]
        for path in paths:
            self.assertNotIn(OLD_PHRASE, read_text(path).lower(), msg=str(path))

    def test_03_qlora_boundary_metadata(self):
        md = " ".join(
            read_text(ROOT / "benchmark" / "qlora" / "XAIBIM_QWEN25_7B_QLORA_PRELIMINARY_RESULTS.md").lower().split()
        )
        data = json.loads(read_text(ROOT / "benchmark" / "qlora" / "xaibim_qwen25_7b_qlora_preliminary_public_results.json"))

        self.assertIn("structured, evidence-trace semantic bim/ifc output task", md)
        self.assertIn("agreement against stored structured targets in the public evaluator", md)
        self.assertIn("external-source supportedness", md)
        self.assertEqual(data["title"], "Preliminary QLoRA Computational Feasibility Run for Evidence-Trace Semantic BIM/IFC Outputs")
        self.assertIn("evidence-trace semantic bim/ifc target agreement", data["scope"]["purpose"].lower())
        self.assertIn("not external-source supportedness", data["corrected_held_out_results"]["evaluator_correction_note"].lower())
        self.assertIn("not external-source supportedness", data["corrected_held_out_results"]["interpretation"].lower())

    def test_04_xai_compatibility_note(self):
        text = " ".join(read_text(ROOT / "docs" / "methodology" / "xai_evidence_positioning.md").lower().split())
        self.assertIn("canonical public position", text)
        self.assertIn("structured audit field", text)
        self.assertIn("external-source supportedness", text)
        self.assertNotIn("candidate classes", text)
        self.assertNotIn("confidence and reason codes", text)
        self.assertNotIn("field-level faithfulness", text)
        self.assertNotIn("replay reproducibility", text)

    def test_05_historical_notes(self):
        changelog = read_text(ROOT / "CHANGELOG.md").lower()
        notes = read_text(ROOT / "RELEASE_NOTES_v0.1.1-public-validation.md").lower()
        self.assertIn("historical chronology only", changelog)
        self.assertIn("superseded by the public evidence-trace naming", notes)
        self.assertIn("does not by itself prove a git tag or github release", notes)
        self.assertIn("historical output tokens retained for compatibility", notes)

    def test_06_dataset_methodology_statuses(self):
        text = read_text(ROOT / "docs" / "methodology" / "dataset_construction_and_training_readiness.md").lower()
        self.assertIn("does not resolve an external source", text)
        self.assertIn("broader / private or planned", text)
        self.assertIn("current public executable", text)
        self.assertIn("stored-record validation", text)


if __name__ == "__main__":
    unittest.main()
