from __future__ import annotations

import copy
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
OLD_PHRASE = "evidence-" + "grounded"
REF_SHA = "91d2ac59ed29d5b2a1ddf528acd2df76cb77d104"
REF_JSON_TITLE = (
    "Preliminary QLoRA Computational Feasibility Run for Evidence-"
    "Grounded Semantic BIM/IFC Outputs"
)
REF_JSON_PURPOSE = (
    "Demonstrate that a bounded QLoRA workflow can be executed and measured on "
    "commodity GPU infrastructure."
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_reference_json() -> dict:
    ref_spec = f"{REF_SHA}:benchmark/qlora/xaibim_qwen25_7b_qlora_preliminary_public_results.json"
    try:
        raw = subprocess.check_output(["git", "show", ref_spec], cwd=ROOT, text=True)
        return json.loads(raw)
    except subprocess.CalledProcessError:
        current = json.loads(
            read_text(ROOT / "benchmark" / "qlora" / "xaibim_qwen25_7b_qlora_preliminary_public_results.json")
        )
        return reconstruct_reference_json(current)


def reconstruct_reference_json(current: dict) -> dict:
    reference = copy.deepcopy(current)
    reference["title"] = REF_JSON_TITLE
    reference["scope"]["purpose"] = REF_JSON_PURPOSE
    reference["corrected_held_out_results"].pop("evidence_trace_metric_boundary", None)
    reference.pop("verification_boundary", None)
    has_ref_commit = (
        subprocess.run(
            ["git", "rev-parse", "--verify", f"{REF_SHA}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        ).returncode
        == 0
    )
    if has_ref_commit and "verification_boundary" in current:
        reference["verification_boundary"] = current["verification_boundary"]
    return reference


def leaf_paths(value, prefix=""):
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            yield from leaf_paths(child, child_prefix)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_prefix = f"{prefix}[{index}]"
            yield from leaf_paths(child, child_prefix)
    else:
        yield prefix, value


def diff_paths(left, right, prefix=""):
    if type(left) is not type(right):
        return {prefix}
    if isinstance(left, dict):
        paths = set()
        keys = set(left) | set(right)
        for key in keys:
            child_prefix = f"{prefix}.{key}" if prefix else key
            if key not in left or key not in right:
                paths.add(child_prefix)
            else:
                paths.update(diff_paths(left[key], right[key], child_prefix))
        return paths
    if isinstance(left, list):
        paths = set()
        if len(left) != len(right):
            paths.add(prefix)
            return paths
        for index, (l_item, r_item) in enumerate(zip(left, right)):
            paths.update(diff_paths(l_item, r_item, f"{prefix}[{index}]"))
        return paths
    return set() if left == right else {prefix}


class TestPublicEvidenceTraceTerminology(unittest.TestCase):
    def test_01_public_artifact_renamed(self):
        readme = read_text(ROOT / "README.md")
        citation = read_text(ROOT / "CITATION.cff")
        self.assertIn("# Semantic BIM/IFC Evidence-Trace Public Research Artifact", readme)
        self.assertIn('title: "Semantic BIM/IFC Evidence-Trace Public Research Artifact"', citation)

    def test_02_no_evidence_grounded_phrase(self):
        paths = [
            ROOT / "CITATION.cff",
            ROOT / "CHANGELOG.md",
            ROOT / "RELEASE_NOTES_v0.1.1-public-validation.md",
            ROOT / "benchmark" / "qlora" / "XAIBIM_QWEN25_7B_QLORA_PRELIMINARY_RESULTS.md",
            ROOT / "benchmark" / "qlora" / "xaibim_qwen25_7b_qlora_preliminary_public_results.json",
            ROOT / "docs" / "methodology" / "dataset_construction_and_training_readiness.md",
            ROOT / "docs" / "methodology" / "xai_evidence_positioning.md",
            ROOT / "docs" / "experiments" / "internal_preliminary_semantic_bim_runs.md",
        ]
        for path in paths:
            self.assertNotIn(OLD_PHRASE, read_text(path).lower(), msg=str(path))

    def test_03_qlora_boundary_metadata(self):
        md = " ".join(
            read_text(ROOT / "benchmark" / "qlora" / "XAIBIM_QWEN25_7B_QLORA_PRELIMINARY_RESULTS.md").lower().split()
        )
        data = json.loads(read_text(ROOT / "benchmark" / "qlora" / "xaibim_qwen25_7b_qlora_preliminary_public_results.json"))

        self.assertIn("structured, evidence-trace semantic bim/ifc output task", md)
        self.assertIn("evidence-trace exact match and evidence-trace field f1 measure agreement against stored structured target fields", md)
        for phrase in [
            "external-source supportedness",
            "source-to-claim entailment",
            "causal attribution",
            "professional evidence sufficiency",
        ]:
            self.assertIn(phrase, md)
        self.assertEqual(data["title"], "Preliminary QLoRA Computational Feasibility Run for Structured Evidence-Trace Semantic BIM/IFC Outputs")
        self.assertEqual(
            data["scope"]["purpose"],
            "Demonstrate that a bounded QLoRA workflow for structured Semantic BIM/IFC target fields can be executed and measured on commodity GPU infrastructure.",
        )
        self.assertIn("evidence_trace_metric_boundary", data["corrected_held_out_results"])
        self.assertEqual(
            data["corrected_held_out_results"]["evaluator_correction_note"],
            load_reference_json()["corrected_held_out_results"]["evaluator_correction_note"],
        )
        self.assertEqual(
            data["corrected_held_out_results"]["interpretation"],
            load_reference_json()["corrected_held_out_results"]["interpretation"],
        )
        ref = load_reference_json()
        delta = diff_paths(ref, data)
        self.assertEqual(
            delta,
            {
                "title",
                "scope.purpose",
                "verification_boundary",
                "corrected_held_out_results.evidence_trace_metric_boundary",
            },
        )
        self.assertEqual(
            data["verification_boundary"],
            {
                "public_verifier_scope": "aggregate_structure_and_derived_calculation_self_consistency",
                "raw_predictions_available": False,
                "held_out_metrics_publicly_recomputable": False,
                "empirical_results_independently_validated_by_repository": False,
            },
        )
        ref_numeric = {path: value for path, value in leaf_paths(ref) if isinstance(value, (int, float)) and not isinstance(value, bool)}
        data_numeric = {path: value for path, value in leaf_paths(data) if isinstance(value, (int, float)) and not isinstance(value, bool)}
        self.assertEqual(ref_numeric, data_numeric)
        ref_hashes = {path: value for path, value in leaf_paths(ref) if path.endswith("sha256")}
        data_hashes = {path: value for path, value in leaf_paths(data) if path.endswith("sha256")}
        self.assertEqual(ref_hashes, data_hashes)

    def test_03b_forced_shallow_fallback_reference_reconstruction(self):
        with patch(
            "subprocess.check_output",
            side_effect=subprocess.CalledProcessError(128, ["git", "show"]),
        ):
            reference = load_reference_json()

        current = json.loads(
            read_text(ROOT / "benchmark" / "qlora" / "xaibim_qwen25_7b_qlora_preliminary_public_results.json")
        )
        delta = diff_paths(reference, current)
        self.assertEqual(
            delta,
            {
                "title",
                "scope.purpose",
                "corrected_held_out_results.evidence_trace_metric_boundary",
            },
        )
        self.assertNotIn("evidence_trace_metric_boundary", reference["corrected_held_out_results"])
        ref_numeric = {path: value for path, value in leaf_paths(reference) if isinstance(value, (int, float)) and not isinstance(value, bool)}
        current_numeric = {path: value for path, value in leaf_paths(current) if isinstance(value, (int, float)) and not isinstance(value, bool)}
        self.assertEqual(ref_numeric, current_numeric)
        ref_hashes = {path: value for path, value in leaf_paths(reference) if path.endswith("sha256")}
        current_hashes = {path: value for path, value in leaf_paths(current) if path.endswith("sha256")}
        self.assertEqual(ref_hashes, current_hashes)

    def test_04_xai_compatibility_note(self):
        text = " ".join(read_text(ROOT / "docs" / "methodology" / "xai_evidence_positioning.md").lower().split())
        self.assertIn("canonical public position", text)
        self.assertIn("structured audit field", text)
        self.assertIn("external-source supportedness", text)
        self.assertIn("replay", text)
        self.assertIn("loading and validating committed stored records", text)
        self.assertIn("does not mean rerunning model generation or the original prompt-to-output pipeline", text)
        self.assertNotIn("candidate classes", text)
        self.assertNotIn("confidence", text)
        self.assertNotIn("evidence relevance", text)
        self.assertNotIn("field-level faithfulness", text)
        self.assertNotIn("replay reproducibility", text)
        self.assertNotIn("source-to-claim entailment", text)
        self.assertIn("causal attribution", text)

    def test_05_historical_notes(self):
        changelog = " ".join(read_text(ROOT / "CHANGELOG.md").lower().split())
        notes = " ".join(read_text(ROOT / "RELEASE_NOTES_v0.1.1-public-validation.md").lower().replace(">", " ").split())
        self.assertIn("historical repository chronology notice", changelog)
        self.assertIn("[!important]", notes)
        self.assertIn("not proof of a git tag or github release", notes)
        self.assertIn("superseded", notes)
        self.assertIn("historical output tokens retained below for documentary context; they are not the current cli contract.", notes)
        self.assertIn("the historical evidence-trace check covered field presence and stored structure. it did not verify external-source supportedness.", notes)

    def test_06_dataset_methodology_statuses(self):
        text = " ".join(read_text(ROOT / "docs" / "methodology" / "dataset_construction_and_training_readiness.md").lower().split())
        self.assertIn("do not by themselves guarantee alignment with canonical catalogues or structured contracts", text)
        self.assertIn("broader / private or planned", text)
        self.assertIn("current public executable", text)
        self.assertIn("stored-record validation", text)


if __name__ == "__main__":
    unittest.main()
