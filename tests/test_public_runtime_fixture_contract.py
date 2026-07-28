from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "harness"))

from public_sample20_v2 import validate_records  # noqa: E402


JSONL_PATH = ROOT / "sample20" / "sample20_public_records.jsonl"
SCHEMA_PATH = ROOT / "sample20" / "schema_public_sample20_v2.json"


def load_records() -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in JSONL_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_schema() -> dict[str, object]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def deep_copy_record(record: dict[str, object]) -> dict[str, object]:
    return json.loads(json.dumps(record))


def first_record_with(predicate) -> tuple[int, dict[str, object]]:
    records = load_records()
    for index, record in enumerate(records):
        if predicate(record):
            return index, record
    raise AssertionError("No matching record found")


def all_ifc_classes(records: list[dict[str, object]]) -> list[str]:
    classes = []
    for record in records:
        for output_name in ("model_output", "reference_output"):
            output = record[output_name]
            if isinstance(output, dict):
                value = output.get("ifc_class")
                if isinstance(value, str):
                    classes.append(value)
    return sorted(set(classes))


def all_semantic_types(records: list[dict[str, object]]) -> list[str]:
    values = []
    for record in records:
        summary = record.get("input_summary")
        if isinstance(summary, dict):
            value = summary.get("semantic_type")
            if isinstance(value, str):
                values.append(value)
    return sorted(set(values))


def find_record_with_value_mode(records: list[dict[str, object]], value_mode: str) -> tuple[int, dict[str, object]]:
    for index, record in enumerate(records):
        model_output = record.get("model_output")
        if isinstance(model_output, dict) and model_output.get("value_mode") == value_mode:
            return index, record
    raise AssertionError(f"No record found with value_mode={value_mode}")


class TestPublicRuntimeFixtureContract(unittest.TestCase):
    def setUp(self) -> None:
        self.records = load_records()
        self.schema = load_schema()
        self.ifc_classes = all_ifc_classes(self.records)
        self.semantic_types = all_semantic_types(self.records)

    def _validate(self, records: list[dict[str, object]]):
        return validate_records(records, self.schema)

    def test_01_canonical_fixture(self):
        ok, errors, metrics = self._validate(self.records)
        self.assertTrue(ok, errors)
        self.assertEqual(errors, [])
        self.assertEqual(metrics["public_schema_valid_rate"], 1.0)
        self.assertEqual(metrics["package_status"], "PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES")

    def test_02_model_reference_mismatch(self):
        records = [deep_copy_record(record) for record in self.records]
        target = records[0]
        original = target["reference_output"]["ifc_class"]
        target["reference_output"]["ifc_class"] = next(
            cls for cls in self.ifc_classes if cls != original
        )
        ok, errors, metrics = self._validate(records)
        self.assertFalse(ok)
        self.assertEqual(metrics["public_schema_valid_rate"], 1.0)
        self.assertTrue(any("model_output and reference_output differ" in err for err in errors))

    def test_03_canonical_class_mismatch(self):
        records = [deep_copy_record(record) for record in self.records]
        records[1]["canonical_check"]["ifc_class"] = next(
            cls for cls in self.ifc_classes if cls != records[1]["model_output"]["ifc_class"]
        )
        ok, errors, metrics = self._validate(records)
        self.assertFalse(ok)
        self.assertEqual(metrics["public_schema_valid_rate"], 1.0)
        self.assertTrue(
            any("canonical_check.ifc_class does not match model_output.ifc_class" in err for err in errors)
        )

    def test_04_canonical_value_mode_mismatch(self):
        records = [deep_copy_record(record) for record in self.records]
        current = records[2]["model_output"]["value_mode"]
        records[2]["canonical_check"]["value_mode"] = next(
            mode for mode in ("EXECUTE", "PREVIEW", "PROPOSAL", "GUIDED_RECOVERY") if mode != current
        )
        ok, errors, metrics = self._validate(records)
        self.assertFalse(ok)
        self.assertEqual(metrics["public_schema_valid_rate"], 1.0)
        self.assertTrue(
            any("canonical_check.value_mode does not match model_output.value_mode" in err for err in errors)
        )

    def test_05_agreement_mismatch(self):
        records = [deep_copy_record(record) for record in self.records]
        records[3]["agreement"]["ifc_class"] = not records[3]["agreement"]["ifc_class"]
        ok, errors, metrics = self._validate(records)
        self.assertFalse(ok)
        self.assertEqual(metrics["public_schema_valid_rate"], 1.0)
        self.assertTrue(any("stored agreement does not match recomputed agreement" in err for err in errors))

    def test_06_input_summary_mismatch(self):
        records = [deep_copy_record(record) for record in self.records]
        current = records[4]["input_summary"]["semantic_type"]
        records[4]["input_summary"]["semantic_type"] = next(
            semantic_type for semantic_type in self.semantic_types if semantic_type != current
        )
        ok, errors, metrics = self._validate(records)
        self.assertFalse(ok)
        self.assertEqual(metrics["public_schema_valid_rate"], 1.0)
        self.assertTrue(
            any("input_summary.semantic_type does not match model_output.semantic_type" in err for err in errors)
        )

    def test_07_recovery_mismatch(self):
        index, record = find_record_with_value_mode(self.records, "GUIDED_RECOVERY")
        records = [deep_copy_record(item) for item in self.records]
        records[index]["model_output"]["recovery_needed"] = False
        records[index]["reference_output"]["recovery_needed"] = False
        ok, errors, metrics = self._validate(records)
        self.assertFalse(ok)
        self.assertEqual(metrics["public_schema_valid_rate"], 1.0)
        self.assertTrue(
            any("model_output recovery_needed is inconsistent with value_mode" in err for err in errors)
        )
        self.assertTrue(
            any("reference_output recovery_needed is inconsistent with value_mode" in err for err in errors)
        )

    def test_08_undeclared_evidence_relation(self):
        records = [deep_copy_record(record) for record in self.records]
        target = records[5]
        current_relationships = set(target["model_output"]["required_relationships"])
        replacement = next(
            relation
            for relation in self._all_relationships()
            if relation not in current_relationships
        )
        target["model_output"]["evidence_trace"]["relation_observed"] = replacement
        target["reference_output"]["evidence_trace"]["relation_observed"] = replacement
        ok, errors, metrics = self._validate(records)
        self.assertFalse(ok)
        self.assertEqual(metrics["public_schema_valid_rate"], 1.0)
        self.assertTrue(
            any("evidence relation is not declared in required_relationships" in err for err in errors)
        )

    def test_09_warnings_are_not_hardcoded(self):
        records = [deep_copy_record(record) for record in self.records]
        records[6]["canonical_check"]["warnings"] = []
        ok, errors, metrics = self._validate(records)
        self.assertTrue(ok, errors)
        self.assertEqual(metrics["public_schema_valid_rate"], 1.0)
        self.assertFalse(any("warnings" in err.lower() for err in errors))

    def test_10_duplicate_required_psets_rejected_by_schema(self):
        index = next(
            idx
            for idx, record in enumerate(self.records)
            if isinstance(record.get("model_output"), dict)
            and isinstance(record["model_output"].get("required_psets"), list)
            and len(record["model_output"]["required_psets"]) > 0
        )
        records = [deep_copy_record(record) for record in self.records]
        duplicate_pset = records[index]["model_output"]["required_psets"][0]
        records[index]["model_output"]["required_psets"].append(duplicate_pset)
        records[index]["reference_output"]["required_psets"].append(duplicate_pset)
        ok, errors, metrics = self._validate(records)
        self.assertFalse(ok)
        self.assertLess(metrics["public_schema_valid_rate"], 1.0)
        self.assertEqual(metrics["package_status"], "PUBLIC_SAMPLE_INVALID")
        self.assertTrue(
            any(
                "schema error" in error.lower()
                and "non-unique elements" in error.lower()
                for error in errors
            )
        )

    def test_11_unhashable_required_psets_are_failure_safe(self):
        records = [deep_copy_record(record) for record in self.records]
        target = records[0]
        target["model_output"]["required_psets"].append({"invalid": True})
        target["reference_output"]["required_psets"].append({"invalid": True})
        ok, errors, metrics = self._validate(records)
        self.assertFalse(ok)
        self.assertLess(metrics["public_schema_valid_rate"], 1.0)
        self.assertEqual(metrics["package_status"], "PUBLIC_SAMPLE_INVALID")
        self.assertTrue(any("schema error" in err.lower() for err in errors))

    def test_12_non_list_required_relationships_are_failure_safe(self):
        records = [deep_copy_record(record) for record in self.records]
        target = records[1]
        target["model_output"]["required_relationships"] = None
        target["reference_output"]["required_relationships"] = None
        ok, errors, metrics = self._validate(records)
        self.assertFalse(ok)
        self.assertLess(metrics["public_schema_valid_rate"], 1.0)
        self.assertEqual(metrics["package_status"], "PUBLIC_SAMPLE_INVALID")
        self.assertTrue(any("schema error" in err.lower() for err in errors))

    def _all_relationships(self) -> list[str]:
        relations: list[str] = []
        for record in self.records:
            for output_name in ("model_output", "reference_output"):
                output = record.get(output_name)
                if isinstance(output, dict):
                    rels = output.get("required_relationships")
                    if isinstance(rels, list):
                        for relation in rels:
                            if isinstance(relation, str):
                                relations.append(relation)
        return sorted(set(relations))


if __name__ == "__main__":
    unittest.main()
