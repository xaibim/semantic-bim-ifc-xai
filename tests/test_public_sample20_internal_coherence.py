from __future__ import annotations

import hashlib
import json
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSONL_PATHS = [
    ROOT / "sample20" / "sample20_public_records.jsonl",
    ROOT / "spaces" / "huggingface" / "sample20_public_predictions.jsonl",
    ROOT / "spaces" / "huggingface_harness" / "sample20_public_predictions.jsonl",
]


EXPECTED_PROPOSAL_IDS = {
    "048b754023b7b6b4",
    "6ebb6c9ea431c6a7",
    "f84721ef28e281d1",
    "3dab4b257ae52bfc",
    "8f91faebc05dd115",
}

EXPECTED_NEGATIVE_IDS = {
    "ee5057a4b7f15e3c",
    "45f540e38ef9fe81",
}

EXPECTED_NEGATIVE_ERROR = ["ifc_class_out_of_operation_scope"]


def load_records(path: Path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def recall(expected, actual):
    if not expected:
        return 1.0 if not actual else 0.0
    expected_set = set(expected)
    actual_set = set(actual)
    return len(expected_set & actual_set) / len(expected_set)


def recompute_agreement(record):
    model = record["model_output"]
    reference = record["reference_output"]
    if model != reference:
        raise AssertionError(f"Model/reference mismatch for {record['sample_id']}")
    return {
        "ifc_class": model["ifc_class"] == reference["ifc_class"],
        "semantic_type": model["semantic_type"] == reference["semantic_type"],
        "intent_class": model["intent_class"] == reference["intent_class"],
        "value_mode": model["value_mode"] == reference["value_mode"],
        "dimensions": model["normalized_dimensions_m"] == reference["normalized_dimensions_m"],
        "missing_inputs": model["missing_inputs"] == reference["missing_inputs"],
        "required_psets_recall": recall(model.get("required_psets", []), reference.get("required_psets", [])),
        "required_relationships_recall": recall(
            model.get("required_relationships", []),
            reference.get("required_relationships", []),
        ),
    }


def check_input_summary_coherence(record):
    input_summary = record["input_summary"]
    model = record["model_output"]
    for field in ["semantic_type", "ambiguity_flags", "missing_inputs", "recovery_type"]:
        assert input_summary[field] == model[field], f"{record['sample_id']} {field}"


class TestPublicSample20InternalCoherence(unittest.TestCase):
    def setUp(self):
        self.records = [load_records(path) for path in JSONL_PATHS]

    def test_01_three_jsonl_byte_identical(self):
        hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in JSONL_PATHS]
        self.assertEqual(len(set(hashes)), 1, hashes)

    def test_02_record_counts_and_ids(self):
        records = self.records[0]
        self.assertEqual(len(records), 20)
        self.assertEqual(len({r["sample_id"] for r in records}), 20)
        self.assertEqual(sum(1 for r in records if r["case_expectation"] == "VALID"), 18)
        self.assertEqual(sum(1 for r in records if r["case_expectation"] == "EXPECTED_CANONICAL_REJECTION"), 2)

    def test_03_model_reference_equality(self):
        for record in self.records[0]:
            self.assertEqual(record["model_output"], record["reference_output"], record["sample_id"])

    def test_04_canonical_class_and_value_mode(self):
        for record in self.records[0]:
            model = record["model_output"]
            canonical = record["canonical_check"]
            self.assertEqual(canonical["ifc_class"], model["ifc_class"], record["sample_id"])
            self.assertEqual(canonical["value_mode"], model["value_mode"], record["sample_id"])

    def test_05_agreement_recomputation(self):
        for record in self.records[0]:
            self.assertEqual(record["agreement"], recompute_agreement(record), record["sample_id"])

    def test_06_input_summary_coherence(self):
        for record in self.records[0]:
            check_input_summary_coherence(record)

    def test_07_recovery_mode_coherence(self):
        for record in self.records[0]:
            model = record["model_output"]
            self.assertEqual(
                model["value_mode"] == "GUIDED_RECOVERY",
                bool(model["recovery_needed"]),
                record["sample_id"],
            )

    def test_08_evidence_relation_declared(self):
        for record in self.records[0]:
            model = record["model_output"]
            self.assertIn(
                model["evidence_trace"]["relation_observed"],
                model["required_relationships"],
                record["sample_id"],
            )

    def test_09_expected_proposal_ids(self):
        proposal_ids = {
            record["sample_id"]
            for record in self.records[0]
            if record["model_output"]["value_mode"] == "PROPOSAL"
        }
        self.assertEqual(proposal_ids, EXPECTED_PROPOSAL_IDS)

    def test_10_expected_negatives(self):
        for record in self.records[0]:
            if record["sample_id"] not in EXPECTED_NEGATIVE_IDS:
                continue
            model = record["model_output"]
            ref = record["reference_output"]
            canonical = record["canonical_check"]
            self.assertEqual(model["required_psets"], [])
            self.assertEqual(ref["required_psets"], [])
            self.assertEqual(canonical["errors"], EXPECTED_NEGATIVE_ERROR)
            self.assertFalse(canonical["ok"])

    def test_11_no_forbidden_error_code(self):
        for record in self.records[0]:
            self.assertNotIn(
                "ifc_class_forbidden_abstract_or_domain",
                json.dumps(record, ensure_ascii=False),
            )

    def test_12_valid_and_rejection_states(self):
        for record in self.records[0]:
            canonical = record["canonical_check"]
            if record["case_expectation"] == "VALID":
                self.assertEqual(record["record_status"], "PASS")
                self.assertTrue(canonical["ok"])
                self.assertEqual(canonical["errors"], [])
            else:
                self.assertEqual(record["record_status"], "EXPECTED_REJECTION_PASS")
                self.assertFalse(canonical["ok"])
                self.assertTrue(canonical["errors"])
