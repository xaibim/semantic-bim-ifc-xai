from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

# This public fixture check does not demonstrate IFC certification.
ROOT = Path(__file__).resolve().parents[1]
JSONL_PATHS = [
    ROOT / "sample20" / "sample20_public_records.jsonl",
    ROOT / "spaces" / "huggingface" / "sample20_public_predictions.jsonl",
    ROOT / "spaces" / "huggingface_harness" / "sample20_public_predictions.jsonl",
]

EXPECTED_PSETS_BY_SAMPLE_ID = {
    "4eeac340747306fd": ["Pset_ColumnCommon"],
    "495a677407a7f05a": ["Pset_WallCommon"],
    "1ae42de17ac977f7": ["Pset_BeamCommon"],
    "ae47e72e2af2b182": ["Pset_BeamCommon"],
    "8c0052ccd9bc96e4": ["Pset_PumpOccurrence"],
    "21129edbbd73ebef": ["Pset_SpaceCommon"],
    "d2ed814a93840a19": [],
    "fa3bca1c51085557": ["Pset_AirTerminalOccurrence"],
    "048b754023b7b6b4": ["Pset_ColumnCommon"],
    "5af537f550afd4aa": ["Pset_FanOccurrence"],
    "6ebb6c9ea431c6a7": ["Pset_ColumnCommon"],
    "ca455e91ed772fd8": ["Pset_ColumnCommon"],
    "f72f31f4c063475b": ["Pset_SpaceCommon"],
    "f84721ef28e281d1": ["Pset_SpaceCommon"],
    "23dad325e1a64458": [],
    "3dab4b257ae52bfc": [],
    "8f91faebc05dd115": [],
    "7f1ea524d9fdbdcb": ["Pset_ColumnCommon"],
}

EXPECTED_NEGATIVE_IDS = {
    "45f540e38ef9fe81",
    "ee5057a4b7f15e3c",
}


def load_records(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


class TestPublicSample20PsetRegression(unittest.TestCase):
    def test_jsonl_files_are_byte_identical(self) -> None:
        payloads = [path.read_bytes() for path in JSONL_PATHS]
        self.assertEqual(len(set(payloads)), 1)

    def test_records_match_expected_mapping(self) -> None:
        records = load_records(JSONL_PATHS[0])
        self.assertEqual(len(records), 20)

        positive_ids = [
            record["sample_id"]
            for record in records
            if record["case_expectation"] == "VALID"
        ]
        negative_ids = [
            record["sample_id"]
            for record in records
            if record["case_expectation"] == "EXPECTED_CANONICAL_REJECTION"
        ]

        self.assertEqual(len(positive_ids), 18)
        self.assertEqual(len(negative_ids), 2)
        self.assertEqual(set(positive_ids), set(EXPECTED_PSETS_BY_SAMPLE_ID))
        self.assertEqual(set(negative_ids), EXPECTED_NEGATIVE_IDS)

        for record in records:
            sample_id = record["sample_id"]
            model_output = record["model_output"]
            reference_output = record["reference_output"]

            self.assertTrue(record["expectation_met"])
            self.assertEqual(model_output, reference_output)

            if sample_id in EXPECTED_PSETS_BY_SAMPLE_ID:
                expected_psets = EXPECTED_PSETS_BY_SAMPLE_ID[sample_id]
                self.assertEqual(model_output["required_psets"], expected_psets)
                self.assertEqual(reference_output["required_psets"], expected_psets)

                for forbidden in [
                    "Pset_QuantityTakeOff",
                    "Pset_DistributionFlowElementCommon",
                    "Pset_MaterialCommon",
                ]:
                    self.assertNotIn(forbidden, model_output["required_psets"])
                    self.assertNotIn(forbidden, reference_output["required_psets"])

    def test_expected_negatives_are_unchanged(self) -> None:
        records = load_records(JSONL_PATHS[0])
        before = {record["sample_id"]: record for record in records}

        for sample_id in EXPECTED_NEGATIVE_IDS:
            record = before[sample_id]
            self.assertEqual(record["case_expectation"], "EXPECTED_CANONICAL_REJECTION")
            self.assertEqual(record["model_output"], record["reference_output"])
            self.assertEqual(record["model_output"]["required_psets"], record["reference_output"]["required_psets"])

    def test_required_psets_are_applicable_when_present(self) -> None:
        try:
            from ifcopenshell.util.pset import PsetQto
        except Exception as exc:  # pragma: no cover
            self.skipTest(f"IfcOpenShell unavailable: {exc}")

        templates = PsetQto("IFC4")
        records = load_records(JSONL_PATHS[0])

        for record in records:
            if record["case_expectation"] != "VALID":
                continue

            ifc_class = record["model_output"]["ifc_class"]
            applicable_psets = set(
                templates.get_applicable_names(ifc_class, pset_only=True)
            )
            for pset_name in record["model_output"]["required_psets"]:
                self.assertIn(pset_name, applicable_psets)

    def test_sha256_values_are_identical(self) -> None:
        shas = [
            hashlib.sha256(path.read_bytes()).hexdigest()
            for path in JSONL_PATHS
        ]
        self.assertEqual(len(set(shas)), 1)


if __name__ == "__main__":
    unittest.main()
