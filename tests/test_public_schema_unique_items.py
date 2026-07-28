from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATHS = [
    ROOT / "sample20" / "schema_public_sample20_v2.json",
    ROOT / "spaces" / "huggingface" / "schema_public_sample20_v2.json",
    ROOT / "spaces" / "huggingface_harness" / "schema_public_sample20_v2.json",
]

RECORDS_PATH = (
    ROOT / "sample20" / "sample20_public_records.jsonl"
)

REVIEWED_SCHEMA_PATHS = [
    ("input_summary", "ambiguity_flags"),
    ("input_summary", "missing_inputs"),
    ("output_block", "required_psets"),
    ("output_block", "required_relationships"),
    ("output_block", "missing_inputs"),
    ("output_block", "ambiguity_flags"),
    ("output_block", "reason_codes"),
    ("canonical_check", "errors"),
    ("canonical_check", "warnings"),
]

INSTANCE_PATHS = [
    ("input_summary", "ambiguity_flags"),
    ("input_summary", "missing_inputs"),
    ("model_output", "required_psets"),
    ("model_output", "required_relationships"),
    ("model_output", "missing_inputs"),
    ("model_output", "ambiguity_flags"),
    ("model_output", "reason_codes"),
    ("reference_output", "required_psets"),
    ("reference_output", "required_relationships"),
    ("reference_output", "missing_inputs"),
    ("reference_output", "ambiguity_flags"),
    ("reference_output", "reason_codes"),
    ("canonical_check", "errors"),
    ("canonical_check", "warnings"),
]


def load_records() -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in RECORDS_PATH.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]


def count_unique_items_keywords(value: object) -> int:
    if isinstance(value, dict):
        return int("uniqueItems" in value) + sum(
            count_unique_items_keywords(item)
            for item in value.values()
        )

    if isinstance(value, list):
        return sum(
            count_unique_items_keywords(item)
            for item in value
        )

    return 0


class TestPublicSchemaUniqueItems(unittest.TestCase):
    def test_01_schema_copies_and_reviewed_keywords(
        self,
    ) -> None:
        blobs = [
            path.read_bytes()
            for path in SCHEMA_PATHS
        ]

        self.assertEqual(blobs[0], blobs[1])
        self.assertEqual(blobs[0], blobs[2])

        schema = json.loads(
            blobs[0].decode("utf-8")
        )

        self.assertEqual(
            count_unique_items_keywords(schema),
            9,
        )

        for definition, property_name in REVIEWED_SCHEMA_PATHS:
            with self.subTest(
                definition=definition,
                property=property_name,
            ):
                node = (
                    schema["$defs"][definition]
                    ["properties"][property_name]
                )
                self.assertEqual(node["type"], "array")
                self.assertEqual(
                    node["items"],
                    {"type": "string"},
                )
                self.assertIs(
                    node.get("uniqueItems"),
                    True,
                )

    def test_02_duplicate_items_are_rejected(
        self,
    ) -> None:
        schema = json.loads(
            SCHEMA_PATHS[0].read_text(
                encoding="utf-8"
            )
        )
        validator = jsonschema.Draft202012Validator(
            schema
        )
        records = load_records()

        valid_record = next(
            record
            for record in records
            if record["case_expectation"] == "VALID"
        )

        rejection_record = next(
            record
            for record in records
            if record["case_expectation"]
            == "EXPECTED_CANONICAL_REJECTION"
        )

        instance_paths = {
            ("input_summary", "ambiguity_flags"):
                ("input_summary", "ambiguity_flags"),
            ("input_summary", "missing_inputs"):
                ("input_summary", "missing_inputs"),
            ("output_block", "required_psets"):
                ("model_output", "required_psets"),
            ("output_block", "required_relationships"):
                ("model_output", "required_relationships"),
            ("output_block", "missing_inputs"):
                ("model_output", "missing_inputs"),
            ("output_block", "ambiguity_flags"):
                ("model_output", "ambiguity_flags"),
            ("output_block", "reason_codes"):
                ("model_output", "reason_codes"),
            ("canonical_check", "errors"):
                ("canonical_check", "errors"),
            ("canonical_check", "warnings"):
                ("canonical_check", "warnings"),
        }

        for schema_path in REVIEWED_SCHEMA_PATHS:
            source = (
                rejection_record
                if schema_path
                == ("canonical_check", "errors")
                else valid_record
            )

            record = copy.deepcopy(source)
            parent, field = instance_paths[schema_path]
            record[parent][field] = [
                "duplicate",
                "duplicate",
            ]

            errors = list(
                validator.iter_errors(record)
            )

            with self.subTest(
                schema_path=schema_path
            ):
                self.assertTrue(
                    any(
                        error.validator == "uniqueItems"
                        for error in errors
                    ),
                    [error.message for error in errors],
                )

    def test_03_committed_fixture_arrays_are_unique(
        self,
    ) -> None:
        for record in load_records():
            for parent, field in INSTANCE_PATHS:
                with self.subTest(
                    sample_id=record["sample_id"],
                    path=f"{parent}.{field}",
                ):
                    values = record[parent][field]
                    self.assertIsInstance(values, list)
                    self.assertEqual(
                        len(values),
                        len(set(values)),
                    )


if __name__ == "__main__":
    unittest.main()
