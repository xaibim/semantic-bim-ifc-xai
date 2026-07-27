from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def lower_text(path: Path) -> str:
    return read_text(path).lower()


def normalized_lower_text(path: Path) -> str:
    return " ".join(read_text(path).lower().split())


def normalized_text(path: Path) -> str:
    return " ".join(read_text(path).split())


class TestPublicNarrativeBoundaries(unittest.TestCase):
    def test_00_readme_title_uses_evidence_trace(self):
        text = read_text(ROOT / "README.md").splitlines()[0]
        self.assertEqual(text, "# Semantic BIM/IFC Evidence-Trace Public Research Artifact")

    def test_01_readme_boundary_language(self):
        text = normalized_lower_text(ROOT / "README.md")
        self.assertIn("executable public boundary begins with committed structured records", text)
        self.assertIn("conceptual / planned", text)
        self.assertIn("schema-only", text)
        self.assertIn("historical cli and space names", text)
        self.assertIn("not rerunning a model", text)
        self.assertNotIn("replayable", text)
        self.assertNotIn("ifc candidates", text)
        self.assertNotIn("material information", text)
        self.assertNotIn("evidence fragments or runtime context supported the output", text)
        self.assertNotIn("schema and replay validation", text)

    def test_02_sample20_readme_boundary_language(self):
        text = lower_text(ROOT / "sample20" / "README.md")
        self.assertNotIn("smoke/replay", text)
        self.assertNotIn("replayable public sample records", text)
        self.assertIn("public sanitized frozen fixture", text)

    def test_03_public_boundary_language(self):
        text = lower_text(ROOT / "docs" / "public_boundary.md")
        self.assertNotIn("executed sample20 replay results", text)
        self.assertIn("raw private or live model-generation outputs", text)

    def test_04_end_to_end_example_language(self):
        text = lower_text(ROOT / "docs" / "examples" / "end_to_end_public_example.md")
        self.assertIn("stored public record", text)
        self.assertIn("stored-record walkthrough", text)
        self.assertNotIn("stored replay record", text)
        self.assertNotIn("stored replay mode", text)

    def test_05_xai_position_limits(self):
        text = lower_text(ROOT / "docs" / "methodology" / "xai_evaluation_position.md")
        expected = [
            "existence of an external evidence source",
            "source identifiers or source locations",
            "whether a source supports a technical claim",
            "occurrence of a relationship in a real ifc model",
            "professional sufficiency of the evidence",
            "causal attribution",
            "shap or lime",
            "chain-of-thought",
            "certification",
        ]
        for phrase in expected:
            self.assertIn(phrase, text)
        for phrase in [
            "evidence corresponds to actual input context",
            "unsupported rationale currently fails a public supportedness check",
            "models trained on this dataset were exposed to verified evidence",
            "records are blocked from ingestion",
            "public harness demonstrates structured replay",
        ]:
            self.assertNotIn(phrase, text)

    def test_06_xai_position_boundary_sentence(self):
        text = normalized_text(ROOT / "docs" / "methodology" / "xai_evaluation_position.md")
        self.assertIn(
            "The current public evidence trace is a structured audit field, not proof that a model used a cited source, not causal attribution, and not professional or normative certification.",
            text,
        )

    def test_07_xai_compatibility_note(self):
        text = normalized_lower_text(ROOT / "docs" / "methodology" / "xai_evidence_positioning.md")
        self.assertIn("compatibility note", text)
        self.assertIn("canonical public position", text)
        self.assertIn("structured audit field", text)
        self.assertIn("external-source supportedness", text)
        self.assertIn("loading and validating committed stored records", text)
        self.assertIn("does not mean rerunning model generation or the original prompt-to-output pipeline", text)
        self.assertIn("causal attribution", text)
        self.assertIn("certification", text)
        for phrase in [
            "candidate classes",
            "confidence",
            "evidence relevance",
            "field-level faithfulness",
            "replay reproducibility",
            "source-to-claim entailment",
        ]:
            self.assertNotIn(phrase, text)

    def test_08_qlora_target_agreement_boundary(self):
        text = normalized_lower_text(
            ROOT / "benchmark" / "qlora" / "XAIBIM_QWEN25_7B_QLORA_PRELIMINARY_RESULTS.md"
        )
        self.assertIn("evidence-trace exact match and evidence-trace field f1 measure agreement against stored structured target fields", text)
        self.assertIn("external-source supportedness", text)
        self.assertIn("source-to-claim entailment", text)
        self.assertIn("causal attribution", text)
        self.assertIn("professional evidence sufficiency", text)

    def test_09_dataset_methodology_boundary(self):
        text = normalized_lower_text(ROOT / "docs" / "methodology" / "dataset_construction_and_training_readiness.md")
        self.assertNotIn("v0.1", text)
        self.assertNotIn("v0.1.1", text)
        self.assertNotIn("v0.2 final public research artifact", text)
        self.assertNotIn("release notes", text)
        self.assertNotIn("fully sanitized subset", text)
        self.assertIn("verifiable current state", text)
        self.assertIn("no tag or release state is claimed", text)
        self.assertIn("public sanitized frozen fixture", text)
        self.assertIn("do not by themselves guarantee alignment with canonical catalogues or structured contracts", text)
        self.assertIn("broader / private or planned", text)
        self.assertIn("current public executable", text)
        self.assertNotIn("fail to maintain alignments", text)
        self.assertIn("external-source supportedness is not evaluated", text)

    def test_10_pset_audit_boundary_language(self):
        text = normalized_lower_text(ROOT / "benchmark" / "public_sample20_ifc4_pset_audit.md")
        self.assertIn("future expanded research dataset", text)
        self.assertIn("broader future research dataset", text)
        self.assertNotIn("full future [external phase] dataset", text)
        self.assertNotIn("broader future [external phase] dataset", text)

    def test_11_readme_qlora_boundary_language(self):
        text = normalized_text(ROOT / "README.md")
        self.assertIn("private pilot with public aggregate evidence only; not a comparative benchmark result", text)
        self.assertIn("No private adapters or checkpoints are public.", text)
        self.assertNotIn("not a public result", text)
        self.assertNotIn("No public private adapters/checkpoints.", text)

    def test_12_validation_gates_boundary(self):
        text = normalized_lower_text(ROOT / "docs" / "methodology" / "validation_gates.md")
        self.assertIn("schema-only", text)
        self.assertIn("model/reference equality", text)
        self.assertIn("lf-normalized", text)
        self.assertIn("class applicability does not prove", text)
        self.assertIn("schema compatibility does not prove", text)
        self.assertIn("external source supportedness is not evaluated", text)

    def test_13_public_evidence_casing(self):
        evidence = read_text(ROOT / "PUBLIC_EVIDENCE.md")
        summary = read_text(ROOT / "sample20" / "VALIDATION_SUMMARY.md")
        for text in (evidence, summary):
            self.assertIn("fixture_contract=NOT_EVALUATED", text)
            self.assertIn("integrity=NOT_CHECKED", text)

    def test_14_huggingface_readme_boundary(self):
        text = normalized_lower_text(ROOT / "spaces" / "huggingface" / "README.md")
        self.assertIn("historical product name", text)
        self.assertIn("does not rerun", text)
        self.assertIn("loads and validates committed records", text)

    def test_15_qlora_verification_boundary(self):
        data = json.loads(read_text(ROOT / "benchmark" / "qlora" / "xaibim_qwen25_7b_qlora_preliminary_public_results.json"))
        boundary = data["verification_boundary"]
        self.assertEqual(
            boundary["public_verifier_scope"],
            "aggregate_structure_and_derived_calculation_self_consistency",
        )
        self.assertFalse(boundary["raw_predictions_available"])
        self.assertFalse(boundary["held_out_metrics_publicly_recomputable"])
        self.assertFalse(boundary["empirical_results_independently_validated_by_repository"])

    def test_16_qlora_verifier_token(self):
        script = read_text(ROOT / "scripts" / "verify_qlora_public_metrics.py")
        old_token = "QLORA" + "_PUBLIC" + "_METRICS_VALID"
        self.assertIn("QLORA_PUBLIC_AGGREGATE_SELF_CONSISTENCY_VALID", script)
        self.assertNotIn(old_token, script)

    def test_17_qlora_narrative_boundary(self):
        expectations = {
            ROOT / "README.md": [
                "derived compute arithmetic",
                "does not independently recompute empirical held-out scores",
                "does not prove superiority",
                "does not prove generalization",
            ],
            ROOT / "docs" / "methodology" / "validation_gates.md": [
                "derived compute arithmetic",
                "independently recompute empirical held-out scores",
                "does not prove superiority",
                "does not prove generalization",
            ],
            ROOT / "benchmark" / "qlora" / "README.md": [
                "derived compute arithmetic",
                "raw predictions",
                "does not independently recompute empirical held-out scores",
                "does not prove superiority",
                "does not prove generalization",
            ],
            ROOT / "benchmark" / "qlora" / "XAIBIM_QWEN25_7B_QLORA_PRELIMINARY_RESULTS.md": [
                "public verification boundary",
                "raw predictions and per-case outputs are not distributed",
                "cannot be independently recomputed",
                "does not reproduce training",
                "does not prove superiority",
                "does not prove generalization",
            ],
        }
        for path, phrases in expectations.items():
            text = normalized_lower_text(path)
            with self.subTest(path=path):
                for phrase in phrases:
                    self.assertIn(phrase, text)

    def test_18_historical_report_boundary(self):
        text = normalized_lower_text(ROOT / "docs" / "experiments" / "internal_preliminary_semantic_bim_runs.md")
        self.assertIn("evidence_status = historical_reported_aggregates_not_publicly_recomputable", text)
        self.assertIn("historical reported aggregates", text)
        self.assertIn("cannot be independently recomputed", text)
        self.assertNotIn("what these experiments demonstrate", text)
        self.assertNotIn("these results show", text)


if __name__ == "__main__":
    unittest.main()
