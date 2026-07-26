from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSONL_PATHS = [
    ROOT / "sample20" / "sample20_public_records.jsonl",
    ROOT / "spaces" / "huggingface" / "sample20_public_predictions.jsonl",
    ROOT / "spaces" / "huggingface_harness" / "sample20_public_predictions.jsonl",
]
SCHEMA_PATHS = [
    ROOT / "sample20" / "schema_public_sample20_v2.json",
    ROOT / "spaces" / "huggingface" / "schema_public_sample20_v2.json",
    ROOT / "spaces" / "huggingface_harness" / "schema_public_sample20_v2.json",
]
JSON_OUTPUT = ROOT / "benchmark" / "public_sample20_ifc4_relationship_schema_participation.json"
MARKDOWN_OUTPUT = ROOT / "benchmark" / "public_sample20_ifc4_relationship_schema_participation.md"
SCRIPT_PATH = ROOT / "scripts" / "generate_public_sample20_ifc4_relationship_audit.py"
EXPECTED_JSONL_SHA256 = "016ebda71cf67ca1d09def86facdb6d9b4d2bdb2cd1728ac1229854a234accc0"
EXPECTED_SCHEMA_SHA256 = "de9c722f98085d7227906295531aa190755d105a0bf030d360fb26b1298ab216"
EXPECTED_SUMMARY = {
    "record_count": 20,
    "positive_count": 18,
    "expected_negative_count": 2,
    "unique_ifc_class_count": 11,
    "unique_relationship_count": 9,
    "record_relationship_pair_count": 37,
    "evidence_relation_declared_count": 20,
    "schema_inverse_participation_found_count": 26,
    "schema_inverse_participation_not_found_count": 11,
}

# This test module does not demonstrate IFC4 task suitability or real IFC instance validity.


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_normalized_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class TestPublicSample20IFC4RelationshipAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = read_jsonl(JSONL_PATHS[0])
        cls.audit = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
        cls.markdown = MARKDOWN_OUTPUT.read_text(encoding="utf-8")

    def test_01_jsonl_byte_identity_and_hashes(self) -> None:
        self.assertEqual(JSONL_PATHS[0].read_bytes(), JSONL_PATHS[1].read_bytes())
        self.assertEqual(JSONL_PATHS[0].read_bytes(), JSONL_PATHS[2].read_bytes())
        self.assertEqual(sha256_path(JSONL_PATHS[0]), EXPECTED_JSONL_SHA256)
        self.assertEqual(sha256_path(JSONL_PATHS[1]), EXPECTED_JSONL_SHA256)
        self.assertEqual(sha256_path(JSONL_PATHS[2]), EXPECTED_JSONL_SHA256)

    def test_02_schema_hashes(self) -> None:
        self.assertEqual(sha256_normalized_text(SCHEMA_PATHS[0]), EXPECTED_SCHEMA_SHA256)
        self.assertEqual(sha256_normalized_text(SCHEMA_PATHS[1]), EXPECTED_SCHEMA_SHA256)
        self.assertEqual(sha256_normalized_text(SCHEMA_PATHS[2]), EXPECTED_SCHEMA_SHA256)

    def test_03_audit_metadata_and_summary(self) -> None:
        self.assertEqual(self.audit["audit_id"], "XAIBIM_PUBLIC_SAMPLE20_IFC4_RELATIONSHIP_SCHEMA_PARTICIPATION_V1")
        self.assertIn("audit_metadata", self.audit)
        self.assertNotIn("metadata", self.audit)
        self.assertEqual(self.audit["audit_metadata"]["source_commit"], "b00dc9ce6a8a96309fb77472eabff9a90d0d50d7")
        self.assertEqual(self.audit["audit_metadata"]["source_file"], "sample20/sample20_public_records.jsonl")
        self.assertEqual(self.audit["audit_metadata"]["source_sha256"], EXPECTED_JSONL_SHA256)
        self.assertEqual(self.audit["audit_metadata"]["ifcopenshell_version"], "0.8.5")
        self.assertEqual(self.audit["audit_metadata"]["ifc_schema"], "IFC4")
        self.assertEqual(self.audit["summary"], EXPECTED_SUMMARY)
        self.assertTrue(self.audit["interpretation_boundary"]["schema_participation_only"])
        self.assertFalse(self.audit["interpretation_boundary"]["semantic_task_alignment_evaluated"])
        self.assertFalse(self.audit["interpretation_boundary"]["real_ifc_model_evaluated"])
        self.assertFalse(self.audit["interpretation_boundary"]["relationship_instances_created"])
        self.assertFalse(self.audit["interpretation_boundary"]["ifc_certification_claimed"])
        self.assertFalse(self.audit["interpretation_boundary"]["corrections_authorized"])

    def test_04_record_audit_counts(self) -> None:
        record_audits = self.audit["record_audits"]
        rows = [row for record in record_audits for row in record["relationship_audits"]]
        self.assertEqual(len(record_audits), 20)
        self.assertEqual(len(rows), 37)
        self.assertEqual(sum(1 for row in rows if row["class_inverse_participation_found"]), 26)
        self.assertEqual(sum(1 for row in rows if not row["class_inverse_participation_found"]), 11)
        self.assertEqual(sum(1 for record in record_audits if record["evidence_relation_declared"]), 20)

    def test_05_jsonl_to_audit_mapping(self) -> None:
        record_audits = self.audit["record_audits"]
        self.assertEqual(len(record_audits), len(self.records))
        for record, audit_record in zip(self.records, record_audits):
            self.assertEqual(audit_record["sample_id"], record["sample_id"])
            self.assertEqual(audit_record["case_expectation"], record["case_expectation"])
            self.assertEqual(audit_record["semantic_type"], record["model_output"]["semantic_type"])
            self.assertEqual(audit_record["ifc_class"], record["model_output"]["ifc_class"])
            self.assertEqual(audit_record["evidence_relation_observed"], record["model_output"]["evidence_trace"]["relation_observed"])
            self.assertEqual(audit_record["evidence_relation_declared"], record["model_output"]["evidence_trace"]["relation_observed"] in record["model_output"]["required_relationships"])
            self.assertEqual(len(audit_record["relationship_audits"]), len(record["model_output"]["required_relationships"]))
            self.assertEqual(record["model_output"], record["reference_output"])

            for relationship_audit in audit_record["relationship_audits"]:
                self.assertIn(relationship_audit["relationship"], record["model_output"]["required_relationships"])
                self.assertEqual(relationship_audit["interpretation_state"], "NOT_EVALUATED")
                self.assertEqual(
                    relationship_audit["class_inverse_participation_found"],
                    bool(relationship_audit["inverse_endpoints"]),
                )

    def test_06_markdown_contains_expected_content(self) -> None:
        self.assertIn("Public sample20 IFC4 relationship schema-participation audit", self.markdown)
        for record in self.records:
            self.assertIn(record["sample_id"], self.markdown)
            self.assertIn(record["model_output"]["ifc_class"], self.markdown)
        for relationship in sorted({rel for record in self.records for rel in record["model_output"]["required_relationships"]}):
            self.assertIn(relationship, self.markdown)
        matrix_section = self.markdown.split("## Record-relationship matrix", 1)[1].split("## No inverse participation found", 1)[0]
        matrix_rows = [
            line
            for line in matrix_section.splitlines()
            if line.startswith("|")
            and not line.startswith("| sample_id |")
            and not line.startswith("| ---")
            and line.strip()
        ]
        self.assertEqual(len(matrix_rows), 37)
        no_inverse_section = self.markdown.split("## No inverse participation found", 1)[1].split("## Interpretation", 1)[0]
        no_inverse_rows = [
            line
            for line in no_inverse_section.splitlines()
            if line.startswith("|")
            and not line.startswith("| sample_id |")
            and not line.startswith("| ---")
            and line.strip()
        ]
        self.assertEqual(len(no_inverse_rows), 11)

    def test_07_generator_check_mode(self) -> None:
        if importlib.util.find_spec("ifcopenshell") is None:
            self.skipTest("IfcOpenShell not available")
        proc = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--json-output",
                str(JSON_OUTPUT),
                "--markdown-output",
                str(MARKDOWN_OUTPUT),
                "--check",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("IFC4_RELATIONSHIP_AUDIT_CURRENT", proc.stdout)


if __name__ == "__main__":
    unittest.main()
