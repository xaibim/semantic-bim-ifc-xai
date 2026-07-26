from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

# This test does not demonstrate IFC4 schema suitability; it only verifies the
# corrected public sample20 fixture and the regenerated audit outputs.
ROOT = Path(__file__).resolve().parents[1]
JSONL_PATHS = [
    ROOT / "sample20" / "sample20_public_records.jsonl",
    ROOT / "spaces" / "huggingface" / "sample20_public_predictions.jsonl",
    ROOT / "spaces" / "huggingface_harness" / "sample20_public_predictions.jsonl",
]
AUDIT_JSON_PATH = ROOT / "benchmark" / "public_sample20_ifc4_relationship_schema_participation.json"
CORRECTION_MD_PATH = ROOT / "benchmark" / "public_sample20_ifc4_relationship_correction.md"
EXPECTED_JSONL_LF_NORMALIZED_SHA256 = "2c0f0c331e79924700e58e2579d35facc65d86ef76e971dbc9593641b98455aa"
EXPECTED_AUDIT_SUMMARY = {
    "record_count": 20,
    "positive_count": 18,
    "expected_negative_count": 2,
    "unique_ifc_class_count": 11,
    "unique_relationship_count": 10,
    "record_relationship_pair_count": 36,
    "evidence_relation_declared_count": 20,
    "exact_inverse_endpoint_count": 31,
    "inherited_supertype_compatible_count": 5,
    "schema_compatible_count": 36,
    "schema_incompatible_count": 0,
}
EXPECTED_MAPPING = {
    "21129edbbd73ebef": {
        "required_relationships": ["IfcRelContainedInSpatialStructure", "IfcRelSpaceBoundary"],
        "relation_observed": "IfcRelContainedInSpatialStructure",
    },
    "f72f31f4c063475b": {
        "required_relationships": ["IfcRelSpaceBoundary"],
        "relation_observed": "IfcRelSpaceBoundary",
    },
    "23dad325e1a64458": {
        "required_relationships": ["IfcRelAssignsToGroup"],
        "relation_observed": "IfcRelAssignsToGroup",
    },
    "ee5057a4b7f15e3c": {
        "required_relationships": ["IfcRelAssignsToGroup"],
        "relation_observed": "IfcRelAssignsToGroup",
    },
    "45f540e38ef9fe81": {
        "required_relationships": ["IfcRelAssignsToGroup"],
        "relation_observed": "IfcRelAssignsToGroup",
    },
}
EXPECTED_VALUE_MODE_DISTRIBUTION = {
    "PREVIEW": 6,
    "PROPOSAL": 5,
    "GUIDED_RECOVERY": 9,
    "EXECUTE": 0,
}
OLD_INCOMPATIBLE_PAIRS = {
    ("21129edbbd73ebef", "IfcSpace", "IfcRelConnectsElements"),
    ("f72f31f4c063475b", "IfcSpace", "IfcRelFillsElement"),
    ("23dad325e1a64458", "IfcAsset", "IfcRelFillsElement"),
    ("ee5057a4b7f15e3c", "IfcSystem", "IfcRelConnectsElements"),
    ("ee5057a4b7f15e3c", "IfcSystem", "IfcRelVoidsElement"),
    ("45f540e38ef9fe81", "IfcZone", "IfcRelConnectsElements"),
}


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_lf_normalized(path: Path) -> str:
    data = path.read_bytes()
    normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalized).hexdigest()


class TestPublicSample20IFC4RelationshipCorrections(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = read_jsonl(JSONL_PATHS[0])
        cls.audit = json.loads(AUDIT_JSON_PATH.read_text(encoding="utf-8"))
        cls.correction_md = CORRECTION_MD_PATH.read_text(encoding="utf-8")

    def test_01_jsonl_identity_and_hashes(self) -> None:
        self.assertEqual(JSONL_PATHS[0].read_bytes(), JSONL_PATHS[1].read_bytes())
        self.assertEqual(JSONL_PATHS[0].read_bytes(), JSONL_PATHS[2].read_bytes())
        for path in JSONL_PATHS:
            self.assertEqual(sha256_lf_normalized(path), EXPECTED_JSONL_LF_NORMALIZED_SHA256)

    def test_02_fixture_counts_and_correspondence(self) -> None:
        self.assertEqual(len(self.records), 20)
        self.assertEqual(len({record["sample_id"] for record in self.records}), 20)
        self.assertEqual(sum(record["case_expectation"] == "VALID" for record in self.records), 18)
        self.assertEqual(sum(record["case_expectation"] == "EXPECTED_CANONICAL_REJECTION" for record in self.records), 2)
        for record in self.records:
            self.assertEqual(record["model_output"], record["reference_output"])
            self.assertIn(record["model_output"]["evidence_trace"]["relation_observed"], record["model_output"]["required_relationships"])

    def test_03_expected_mapping_and_scope(self) -> None:
        for sample_id, expected in EXPECTED_MAPPING.items():
            record = next(record for record in self.records if record["sample_id"] == sample_id)
            model_output = record["model_output"]
            reference_output = record["reference_output"]
            self.assertEqual(model_output["required_relationships"], expected["required_relationships"])
            self.assertEqual(reference_output["required_relationships"], expected["required_relationships"])
            self.assertEqual(model_output["evidence_trace"]["relation_observed"], expected["relation_observed"])
            self.assertEqual(reference_output["evidence_trace"]["relation_observed"], expected["relation_observed"])

        self.assertFalse(any("IfcRelServicesBuildings" in json.dumps(record, ensure_ascii=False) for record in self.records))
        for record in self.records:
            for relationship in record["model_output"]["required_relationships"]:
                self.assertNotIn((record["sample_id"], record["model_output"]["ifc_class"], relationship), OLD_INCOMPATIBLE_PAIRS)
                self.assertNotEqual(relationship, "IfcRelServicesBuildings")

    def test_04_expected_negative_cases(self) -> None:
        negatives = [record for record in self.records if record["case_expectation"] == "EXPECTED_CANONICAL_REJECTION"]
        self.assertEqual(len(negatives), 2)
        for record in negatives:
            self.assertFalse(record["canonical_check"]["ok"])
            self.assertEqual(record["canonical_check"]["errors"], ["ifc_class_out_of_operation_scope"])
            self.assertEqual(record["record_status"], "EXPECTED_REJECTION_PASS")

    def test_05_agreement_and_value_modes(self) -> None:
        agreement_required_relationships_recall = {record["agreement"]["required_relationships_recall"] for record in self.records}
        self.assertEqual(agreement_required_relationships_recall, {1.0})
        value_mode_counts = {mode: 0 for mode in EXPECTED_VALUE_MODE_DISTRIBUTION}
        for record in self.records:
            value_mode_counts[record["model_output"]["value_mode"]] += 1
        self.assertEqual(value_mode_counts, EXPECTED_VALUE_MODE_DISTRIBUTION)

    def test_06_audit_v3_summary(self) -> None:
        self.assertEqual(self.audit["audit_id"], "XAIBIM_PUBLIC_SAMPLE20_IFC4_RELATIONSHIP_SCHEMA_PARTICIPATION_V3")
        self.assertEqual(self.audit["summary"], EXPECTED_AUDIT_SUMMARY)
        self.assertEqual(self.audit["audit_metadata"]["source_lf_normalized_sha256"], EXPECTED_JSONL_LF_NORMALIZED_SHA256)
        self.assertNotIn("source_sha256", self.audit["audit_metadata"])
        self.assertEqual(self.audit["audit_metadata"]["source_commit"], "2b8b568b33e5a6852f6353499c9233771ac3c6c2")
        self.assertEqual(self.audit["record_audits"][0]["relationship_audits"][0]["interpretation_state"], "NOT_EVALUATED")
        rows = [row for record in self.audit["record_audits"] for row in record["relationship_audits"]]
        self.assertEqual(len(rows), 36)
        self.assertEqual(sum(row["compatibility_state"] == "EXACT_INVERSE_ENDPOINT" for row in rows), 31)
        self.assertEqual(sum(row["compatibility_state"] == "INHERITED_SUPERTYPE_COMPATIBLE" for row in rows), 5)
        self.assertEqual(sum(row["compatibility_state"] == "SCHEMA_INCOMPATIBLE" for row in rows), 0)
        self.assertEqual(sum(row["schema_compatible"] for row in rows), 36)
        self.assertEqual(sum(not row["schema_compatible"] for row in rows), 0)

    def test_07_correction_report_content(self) -> None:
        self.assertIn("# Public sample20 IFC4 relationship correction", self.correction_md)
        self.assertIn("six schema-incompatible pairs", self.correction_md)
        self.assertIn("previous record-relationship pairs: 37", self.correction_md)
        self.assertIn("corrected record-relationship pairs: 36", self.correction_md)
        self.assertIn("LF-normalized SHA-256", self.correction_md)
        self.assertIn("MICRO-06B used three commits", self.correction_md)
        self.assertRegex(
            self.correction_md,
            r"no\s+rebase, reset, squash or force push was performed",
        )
        self.assertIn("2b8b568b33e5a6852f6353499c9233771ac3c6c2", self.correction_md)
        self.assertIn("5f467935def3613c2b325fee6ccaec044ba67236", self.correction_md)
        self.assertIn("92dfddfa911120027f282895aa76bc7897400b08", self.correction_md)
        self.assertIn("exact inverse endpoints: 31", self.correction_md)
        self.assertIn("schema-incompatible: 0", self.correction_md)
        self.assertIn("IfcRelSpaceBoundary", self.correction_md)
        self.assertIn("IfcRelAssignsToGroup", self.correction_md)


if __name__ == "__main__":
    unittest.main()
