from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness"))

from public_sample20_v2 import validate_records

RECORDS_PATH = (
    ROOT / "sample20" / "sample20_public_records.jsonl"
)
SCHEMA_PATH = (
    ROOT / "sample20" / "schema_public_sample20_v2.json"
)
SUMMARY_PATH = (
    ROOT
    / "benchmark"
    / "metrics"
    / "smoke20_research_summary.json"
)

PUBLIC_METRIC_DOCUMENTS = [
    ROOT / "PUBLIC_EVIDENCE.md",
    ROOT / "README.md",
    ROOT / "benchmark" / "README.md",
    ROOT / "benchmark" / "metrics" / "README.md",
    (
        ROOT
        / "benchmark"
        / "metrics"
        / "smoke20_metrics_table.md"
    ),
    ROOT / "benchmark" / "results_sample20.md",
    (
        ROOT
        / "docs"
        / "methodology"
        / "dataset_scope_and_compute_scaling.md"
    ),
    (
        ROOT
        / "docs"
        / "methodology"
        / "validation_gates.md"
    ),
    ROOT / "docs" / "public_boundary.md",
    ROOT / "sample20" / "README.md",
    ROOT / "sample20" / "VALIDATION_SUMMARY.md",
    ROOT / "spaces" / "README.md",
    ROOT / "spaces" / "huggingface" / "README.md",
    (
        ROOT
        / "spaces"
        / "huggingface_harness"
        / "README.md"
    ),
]


class TestPublicMetricSemantics(unittest.TestCase):
    def test_01_acceptance_rate_is_recomputed_from_canonical_check(
        self,
    ) -> None:
        records = [
            json.loads(line)
            for line in RECORDS_PATH.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        ]
        schema = json.loads(
            SCHEMA_PATH.read_text(encoding="utf-8")
        )

        ok, errors, metrics = validate_records(records, schema)
        self.assertTrue(ok, errors)

        acceptance_count = sum(
            1
            for record in records
            if isinstance(record.get("canonical_check"), dict)
            and record["canonical_check"].get("ok") is True
        )
        expected_rate = acceptance_count / len(records)

        self.assertEqual(acceptance_count, 18)
        self.assertEqual(expected_rate, 0.9)
        self.assertEqual(
            metrics["canonical_acceptance_rate"],
            expected_rate,
        )

        obsolete_key = "canonical_" + "validation_rate"
        self.assertNotIn(obsolete_key, metrics)

    def test_02_public_summary_and_documents_use_bounded_terminology(
        self,
    ) -> None:
        summary = json.loads(
            SUMMARY_PATH.read_text(encoding="utf-8")
        )
        obsolete_key = "canonical_" + "validation_rate"
        obsolete_label = "Canonical " + "Validation Rate"

        self.assertEqual(
            summary["canonical_acceptance_rate"],
            0.9,
        )
        self.assertNotIn(obsolete_key, summary)

        for path in PUBLIC_METRIC_DOCUMENTS:
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")
                lowered = text.lower()

                self.assertIn(
                    "canonical_acceptance_rate",
                    text,
                )
                self.assertNotIn(obsolete_key, text)
                self.assertNotIn(obsolete_label, text)
                self.assertIn("acceptance share", lowered)
                self.assertIn("not accuracy", lowered)


if __name__ == "__main__":
    unittest.main()
