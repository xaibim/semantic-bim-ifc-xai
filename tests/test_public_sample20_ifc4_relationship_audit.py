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
EXPECTED_JSONL_LF_NORMALIZED_SHA256 = "2c0f0c331e79924700e58e2579d35facc65d86ef76e971dbc9593641b98455aa"
EXPECTED_SCHEMA_LF_NORMALIZED_SHA256 = "8e4de7f560ef24dac0404c45b8d62661dd52c538876e17b7ad975a254306f7f9"
EXPECTED_SUMMARY = {
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
EXPECTED_EXACT_ROWS = {
    ("4eeac340747306fd", "IfcColumn", "IfcRelConnectsElements"),
    ("4eeac340747306fd", "IfcColumn", "IfcRelDefinesByProperties"),
    ("495a677407a7f05a", "IfcWall", "IfcRelNests"),
    ("1ae42de17ac977f7", "IfcBeam", "IfcRelVoidsElement"),
    ("1ae42de17ac977f7", "IfcBeam", "IfcRelFillsElement"),
    ("ae47e72e2af2b182", "IfcBeam", "IfcRelConnectsElements"),
    ("ae47e72e2af2b182", "IfcBeam", "IfcRelAggregates"),
    ("8c0052ccd9bc96e4", "IfcPump", "IfcRelVoidsElement"),
    ("21129edbbd73ebef", "IfcSpace", "IfcRelContainedInSpatialStructure"),
    ("d2ed814a93840a19", "IfcFlowTerminal", "IfcRelVoidsElement"),
    ("d2ed814a93840a19", "IfcFlowTerminal", "IfcRelFillsElement"),
    ("fa3bca1c51085557", "IfcAirTerminal", "IfcRelNests"),
    ("fa3bca1c51085557", "IfcAirTerminal", "IfcRelFillsElement"),
    ("048b754023b7b6b4", "IfcColumn", "IfcRelConnectsElements"),
    ("048b754023b7b6b4", "IfcColumn", "IfcRelAggregates"),
    ("5af537f550afd4aa", "IfcFan", "IfcRelContainedInSpatialStructure"),
    ("5af537f550afd4aa", "IfcFan", "IfcRelNests"),
    ("6ebb6c9ea431c6a7", "IfcColumn", "IfcRelVoidsElement"),
    ("ca455e91ed772fd8", "IfcColumn", "IfcRelVoidsElement"),
    ("f84721ef28e281d1", "IfcSpace", "IfcRelAggregates"),
    ("f84721ef28e281d1", "IfcSpace", "IfcRelContainedInSpatialStructure"),
    ("3dab4b257ae52bfc", "IfcFlowTerminal", "IfcRelNests"),
    ("3dab4b257ae52bfc", "IfcFlowTerminal", "IfcRelFillsElement"),
    ("8f91faebc05dd115", "IfcAsset", "IfcRelDefinesByProperties"),
    ("8f91faebc05dd115", "IfcAsset", "IfcRelNests"),
    ("7f1ea524d9fdbdcb", "IfcColumn", "IfcRelAggregates"),
    ("21129edbbd73ebef", "IfcSpace", "IfcRelSpaceBoundary"),
    ("f72f31f4c063475b", "IfcSpace", "IfcRelSpaceBoundary"),
    ("23dad325e1a64458", "IfcAsset", "IfcRelAssignsToGroup"),
    ("ee5057a4b7f15e3c", "IfcSystem", "IfcRelAssignsToGroup"),
    ("45f540e38ef9fe81", "IfcZone", "IfcRelAssignsToGroup"),
}
EXPECTED_INHERITED_ROWS = {
    ("495a677407a7f05a", "IfcWall", "IfcRelAssignsToGroup", "IfcRelAssigns"),
    ("8c0052ccd9bc96e4", "IfcPump", "IfcRelAssociatesMaterial", "IfcRelAssociates"),
    ("6ebb6c9ea431c6a7", "IfcColumn", "IfcRelAssignsToGroup", "IfcRelAssigns"),
    ("ca455e91ed772fd8", "IfcColumn", "IfcRelAssignsToGroup", "IfcRelAssigns"),
    ("7f1ea524d9fdbdcb", "IfcColumn", "IfcRelAssociatesMaterial", "IfcRelAssociates"),
}
EXPECTED_INCOMPATIBLE_ROWS = set()

# This test module does not demonstrate IFC4 task suitability or real IFC instance validity.


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_lf_normalized(path: Path) -> str:
    data = path.read_bytes()
    normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalized).hexdigest()


class TestPublicSample20IFC4RelationshipAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = read_jsonl(JSONL_PATHS[0])
        cls.audit = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
        cls.markdown = MARKDOWN_OUTPUT.read_text(encoding="utf-8")

    def test_01_jsonl_byte_identity_and_hashes(self) -> None:
        self.assertEqual(JSONL_PATHS[0].read_bytes(), JSONL_PATHS[1].read_bytes())
        self.assertEqual(JSONL_PATHS[0].read_bytes(), JSONL_PATHS[2].read_bytes())
        self.assertEqual(sha256_lf_normalized(JSONL_PATHS[0]), EXPECTED_JSONL_LF_NORMALIZED_SHA256)
        self.assertEqual(sha256_lf_normalized(JSONL_PATHS[1]), EXPECTED_JSONL_LF_NORMALIZED_SHA256)
        self.assertEqual(sha256_lf_normalized(JSONL_PATHS[2]), EXPECTED_JSONL_LF_NORMALIZED_SHA256)

    def test_02_schema_hashes(self) -> None:
        self.assertEqual(sha256_lf_normalized(SCHEMA_PATHS[0]), EXPECTED_SCHEMA_LF_NORMALIZED_SHA256)
        self.assertEqual(sha256_lf_normalized(SCHEMA_PATHS[1]), EXPECTED_SCHEMA_LF_NORMALIZED_SHA256)
        self.assertEqual(sha256_lf_normalized(SCHEMA_PATHS[2]), EXPECTED_SCHEMA_LF_NORMALIZED_SHA256)

    def test_03_audit_metadata_and_summary(self) -> None:
        self.assertEqual(self.audit["audit_id"], "XAIBIM_PUBLIC_SAMPLE20_IFC4_RELATIONSHIP_SCHEMA_PARTICIPATION_V3")
        self.assertIn("audit_metadata", self.audit)
        self.assertNotIn("metadata", self.audit)
        self.assertEqual(self.audit["audit_metadata"]["source_commit"], "2b8b568b33e5a6852f6353499c9233771ac3c6c2")
        self.assertEqual(self.audit["audit_metadata"]["source_file"], "sample20/sample20_public_records.jsonl")
        self.assertEqual(self.audit["audit_metadata"]["source_lf_normalized_sha256"], EXPECTED_JSONL_LF_NORMALIZED_SHA256)
        self.assertNotIn("source_sha256", self.audit["audit_metadata"])
        self.assertEqual(self.audit["audit_metadata"]["source_copy_count"], 3)
        self.assertTrue(self.audit["audit_metadata"]["source_copy_byte_identity_verified"])
        self.assertIn("normalized to LF", self.audit["audit_metadata"]["hash_contract"])
        self.assertEqual(self.audit["audit_metadata"]["ifcopenshell_version"], "0.8.5")
        self.assertEqual(self.audit["audit_metadata"]["ifc_schema"], "IFC4")
        self.assertEqual(
            set(self.audit["audit_metadata"]),
            {
                "source_commit",
                "source_file",
                "source_lf_normalized_sha256",
                "hash_contract",
                "source_copy_count",
                "source_copy_byte_identity_verified",
                "ifcopenshell_version",
                "ifc_schema",
                "scope_note",
            },
        )
        self.assertEqual(self.audit["summary"], EXPECTED_SUMMARY)
        self.assertTrue(self.audit["interpretation_boundary"]["schema_participation_only"])
        self.assertFalse(self.audit["interpretation_boundary"]["semantic_task_alignment_evaluated"])
        self.assertFalse(self.audit["interpretation_boundary"]["real_ifc_model_evaluated"])
        self.assertFalse(self.audit["interpretation_boundary"]["relationship_instances_created"])
        self.assertFalse(self.audit["interpretation_boundary"]["ifc_certification_claimed"])
        self.assertFalse(self.audit["interpretation_boundary"]["corrections_authorized"])
        self.assertEqual(
            set(self.audit),
            {
                "audit_id",
                "audit_metadata",
                "class_catalog",
                "interpretation_boundary",
                "record_audits",
                "relationship_catalog",
                "summary",
            },
        )

    def test_04_record_audit_counts(self) -> None:
        record_audits = self.audit["record_audits"]
        rows = [row for record in record_audits for row in record["relationship_audits"]]
        self.assertEqual(len(record_audits), 20)
        self.assertEqual(len(rows), 36)
        self.assertEqual(sum(1 for row in rows if row["compatibility_state"] == "EXACT_INVERSE_ENDPOINT"), 31)
        self.assertEqual(sum(1 for row in rows if row["compatibility_state"] == "INHERITED_SUPERTYPE_COMPATIBLE"), 5)
        self.assertEqual(sum(1 for row in rows if row["compatibility_state"] == "SCHEMA_INCOMPATIBLE"), 0)
        self.assertEqual(sum(1 for row in rows if row["schema_compatible"]), 36)
        self.assertEqual(sum(1 for row in rows if not row["schema_compatible"]), 0)
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
                self.assertIn("required_relationship_supertype_chain", relationship_audit)
                self.assertNotIn("class_inverse_participation_found", relationship_audit)
                self.assertIn(relationship_audit["compatibility_state"], {
                    "EXACT_INVERSE_ENDPOINT",
                    "INHERITED_SUPERTYPE_COMPATIBLE",
                    "SCHEMA_INCOMPATIBLE",
                })
                if relationship_audit["compatibility_state"] == "EXACT_INVERSE_ENDPOINT":
                    self.assertTrue(relationship_audit["exact_inverse_endpoints"])
                    self.assertEqual(relationship_audit["inherited_supertype_endpoints"], [])
                elif relationship_audit["compatibility_state"] == "INHERITED_SUPERTYPE_COMPATIBLE":
                    self.assertEqual(relationship_audit["exact_inverse_endpoints"], [])
                    self.assertTrue(relationship_audit["inherited_supertype_endpoints"])
                else:
                    self.assertEqual(relationship_audit["exact_inverse_endpoints"], [])
                    self.assertEqual(relationship_audit["inherited_supertype_endpoints"], [])

    def test_06_markdown_contains_expected_content(self) -> None:
        self.assertIn("Public sample20 IFC4 subtype-aware relationship schema-participation audit", self.markdown)
        for record in self.records:
            self.assertIn(record["sample_id"], self.markdown)
            self.assertIn(record["model_output"]["ifc_class"], self.markdown)
        for relationship in sorted({rel for record in self.records for rel in record["model_output"]["required_relationships"]}):
            self.assertIn(relationship, self.markdown)
        matrix_section = self.markdown.split("## Record-relationship matrix", 1)[1].split("## Exact inverse endpoints", 1)[0]
        matrix_rows = [
            line
            for line in matrix_section.splitlines()
            if line.startswith("|")
            and not line.startswith("| sample_id |")
            and not line.startswith("| ---")
            and line.strip()
        ]
        self.assertEqual(len(matrix_rows), 36)
        exact_section = self.markdown.split("## Exact inverse endpoints", 1)[1].split("## Inherited supertype-compatible rows", 1)[0]
        exact_rows = [
            line
            for line in exact_section.splitlines()
            if line.startswith("|")
            and not line.startswith("| sample_id |")
            and not line.startswith("| ---")
            and line.strip()
        ]
        self.assertEqual(len(exact_rows), 31)
        inherited_section = self.markdown.split("## Inherited supertype-compatible rows", 1)[1].split("## Schema-incompatible rows", 1)[0]
        inherited_rows = [
            line
            for line in inherited_section.splitlines()
            if line.startswith("|")
            and not line.startswith("| sample_id |")
            and not line.startswith("| ---")
            and line.strip()
        ]
        self.assertEqual(len(inherited_rows), 5)
        incompatible_section = self.markdown.split("## Schema-incompatible rows", 1)[1].split("## Interpretation", 1)[0]
        incompatible_rows = [
            line
            for line in incompatible_section.splitlines()
            if line.startswith("|")
            and not line.startswith("| sample_id |")
            and not line.startswith("| ---")
            and line.strip()
        ]
        self.assertEqual(len(incompatible_rows), 0)

    def test_07_compatibility_classification_sets(self) -> None:
        rows = [row for record in self.audit["record_audits"] for row in record["relationship_audits"]]
        exact = {
            (record["sample_id"], record["ifc_class"], row["relationship"])
            for record in self.audit["record_audits"]
            for row in record["relationship_audits"]
            if row["compatibility_state"] == "EXACT_INVERSE_ENDPOINT"
        }
        inherited = {
            (record["sample_id"], record["ifc_class"], row["relationship"], row["inherited_supertype_endpoints"][0]["declared_relationship_supertype"])
            for record in self.audit["record_audits"]
            for row in record["relationship_audits"]
            if row["compatibility_state"] == "INHERITED_SUPERTYPE_COMPATIBLE"
        }
        incompatible = {
            (record["sample_id"], record["ifc_class"], row["relationship"])
            for record in self.audit["record_audits"]
            for row in record["relationship_audits"]
            if row["compatibility_state"] == "SCHEMA_INCOMPATIBLE"
        }
        self.assertEqual(exact, EXPECTED_EXACT_ROWS)
        self.assertEqual(inherited, EXPECTED_INHERITED_ROWS)
        self.assertEqual(incompatible, EXPECTED_INCOMPATIBLE_ROWS)

    def test_08_generator_check_mode(self) -> None:
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
