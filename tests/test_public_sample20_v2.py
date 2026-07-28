from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "spaces" / "huggingface_harness"))

from public_sample20_v2 import validate_records
from app import semantic_bim_preview
from public_forbidden_scan import normalize_text, scan_decoded_json
from verify_qlora_public_metrics import main as run_qlora_verifier

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


class TestPublicSample20V2(unittest.TestCase):
    def setUp(self):
        # Load canonical records
        self.records = []
        with JSONL_PATHS[0].open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    self.records.append(json.loads(line))
        with SCHEMA_PATHS[0].open("r", encoding="utf-8") as sf:
            self.schema = json.load(sf)

    def test_1_exactly_20_records(self):
        self.assertEqual(len(self.records), 20)

    def test_2_twenty_unique_ids(self):
        sample_ids = [r.get("sample_id") for r in self.records]
        self.assertEqual(len(set(sample_ids)), 20)

    def test_3_draft202012_valid(self):
        ok, errors, _ = validate_records(self.records, self.schema)
        self.assertTrue(ok, f"Validation failed with: {errors}")

    def test_4_null_value_mode_rejected(self):
        bad_records = [json.loads(json.dumps(r)) for r in self.records]
        # set value_mode to None in model_output
        bad_records[0]["model_output"]["value_mode"] = None
        ok, errors, _ = validate_records(bad_records, self.schema)
        self.assertFalse(ok)
        self.assertTrue(any("value_mode" in err or "schema" in err.lower() for err in errors))

    def test_5_unknown_value_mode_rejected(self):
        bad_records = [json.loads(json.dumps(r)) for r in self.records]
        bad_records[0]["model_output"]["value_mode"] = "INVALID_MODE"
        ok, errors, _ = validate_records(bad_records, self.schema)
        self.assertFalse(ok)
        self.assertTrue(any("value_mode" in err or "schema" in err.lower() for err in errors))

    def test_6_hard_block_rejected(self):
        bad_records = [json.loads(json.dumps(r)) for r in self.records]
        bad_records[0]["model_output"]["safe_next_action"] = "We are in HARD_BLOCK state"
        ok, errors, _ = validate_records(bad_records, self.schema)
        self.assertFalse(ok)
        self.assertTrue(any("hard_block" in err.lower() for err in errors))

    def test_7_safe_block_rejected(self):
        bad_records = [json.loads(json.dumps(r)) for r in self.records]
        bad_records[0]["model_output"]["safe_next_action"] = "We are in safe_block state"
        ok, errors, _ = validate_records(bad_records, self.schema)
        self.assertFalse(ok)
        self.assertTrue(any("safe_block" in err.lower() for err in errors))

    def test_8_internal_key_rejected(self):
        bad_records = [json.loads(json.dumps(r)) for r in self.records]
        bad_records[0]["prompt_payload"] = "some prompt"
        ok, errors, _ = validate_records(bad_records, self.schema)
        self.assertFalse(ok)
        self.assertTrue(any("forbidden key" in err.lower() or "unexpected" in err.lower() or "not allowed" in err.lower() or "schema error" in err.lower() for err in errors))

    def test_9_valid_incoherent_rejected(self):
        bad_records = [json.loads(json.dumps(r)) for r in self.records]
        # Case expectation is VALID, but set canonical_check.ok to False
        for r in bad_records:
            if r.get("case_expectation") == "VALID":
                r["canonical_check"]["ok"] = False
                break
        ok, errors, _ = validate_records(bad_records, self.schema)
        self.assertFalse(ok)
        self.assertTrue(any("canonical_check.ok" in err or "schema" in err.lower() for err in errors))

    def test_10_rejection_without_error_rejected(self):
        bad_records = [json.loads(json.dumps(r)) for r in self.records]
        # Case expectation is EXPECTED_CANONICAL_REJECTION, but set errors to empty
        for r in bad_records:
            if r.get("case_expectation") == "EXPECTED_CANONICAL_REJECTION":
                r["canonical_check"]["errors"] = []
                r["canonical_check"]["ok"] = False
                break
        ok, errors, _ = validate_records(bad_records, self.schema)
        self.assertFalse(ok)
        self.assertTrue(any("errors" in err or "schema" in err.lower() for err in errors))

    def test_11_two_expected_negatives_accepted(self):
        rejections = [r for r in self.records if r.get("case_expectation") == "EXPECTED_CANONICAL_REJECTION"]
        self.assertEqual(len(rejections), 2)
        for r in rejections:
            self.assertEqual(r.get("record_status"), "EXPECTED_REJECTION_PASS")
            self.assertFalse(r.get("canonical_check", {}).get("ok"))
            self.assertTrue(len(r.get("canonical_check", {}).get("errors", [])) >= 1)

    def test_12_recalculated_metrics_exact(self):
        ok, errors, metrics = validate_records(self.records, self.schema)
        self.assertTrue(ok)
        self.assertEqual(metrics["record_count"], 20)
        self.assertEqual(metrics["valid_case_count"], 18)
        self.assertEqual(metrics["expected_canonical_rejection_count"], 2)
        self.assertEqual(metrics["expectation_met_rate"], 1.0)
        self.assertEqual(
            metrics["canonical_acceptance_rate"],
            0.9,
        )
        obsolete_metric_key = "canonical_" + "validation_rate"
        self.assertNotIn(obsolete_metric_key, metrics)
        self.assertEqual(metrics["PREVIEW"], 6)
        self.assertEqual(metrics["PROPOSAL"], 5)
        self.assertEqual(metrics["GUIDED_RECOVERY"], 9)
        self.assertEqual(metrics["EXECUTE"], 0)
        self.assertEqual(metrics["package_status"], "PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES")

    def test_13_three_jsonl_identical(self):
        shas = [hashlib.sha256(p.read_bytes()).hexdigest() for p in JSONL_PATHS]
        self.assertEqual(len(set(shas)), 1, f"JSONL SHAs: {shas}")

    def test_14_three_schemas_identical(self):
        shas = [hashlib.sha256(p.read_bytes()).hexdigest() for p in SCHEMA_PATHS]
        self.assertEqual(len(set(shas)), 1, f"Schema SHAs: {shas}")

    def test_15_unknown_prompt_no_ifccolumn(self):
        json_str, loi, lod, evidence, lims, path = semantic_bim_preview("I want a random object")
        parsed = json.loads(json_str)
        self.assertIsNone(parsed.get("suggested_ifc_class"))
        self.assertEqual(parsed.get("value_mode"), "GUIDED_RECOVERY")
        self.assertTrue(parsed.get("recovery_needed"))
        self.assertIn("clarify", parsed.get("safe_next_action", "").lower())
        self.assertEqual(path, "")

    def test_16_scanner_detects_unicode_invisible(self):
        text = "Hello\u200bWorld"
        norm = normalize_text(text)
        self.assertEqual(norm, "HelloWorld")

    def test_17_scanner_detects_html_entity(self):
        text = "Hello&amp;World"
        norm = normalize_text(text)
        self.assertEqual(norm, "Hello&World")

    def test_18_scanner_detects_json_escaped_string(self):
        bad_json = {"status": "PASS", "metadata": "Some info", "custom_field": "hard_block"}
        errors = []
        scan_decoded_json(bad_json, "test.json", 1, errors)
        self.assertTrue(any("forbidden" in err.lower() or "legacy" in err.lower() for err in errors))

    def test_19_qlora_verifier_passes(self):
        rc = run_qlora_verifier()
        self.assertEqual(rc, 0)

    def test_20_documentation_no_legacy_states(self):
        for p in [ROOT / "README.md", ROOT / "PUBLIC_EVIDENCE.md", ROOT / "QUICKSTART.md"]:
            if p.exists():
                text = p.read_text(encoding="utf-8").lower()
                self.assertNotIn("hard_block", text)
                self.assertNotIn("safe_block", text)
                self.assertNotIn("research_pass", text)

    def test_21_html_entity_hiding_token_triggers_scanner(self):
        # h&#97;rd_block -> hard_block
        text = "This is a h&#97;rd_block state"
        norm = normalize_text(text)
        self.assertIn("hard_block", norm)

    def test_22_unicode_invisible_char_triggers_scanner(self):
        # hard_\u200bblock -> hard_block
        text = "This is a hard_\u200bblock state"
        norm = normalize_text(text)
        self.assertIn("hard_block", norm)

    def test_23_json_escaped_unicode_triggers_scanner(self):
        # \u0068\u0061\u0072\u0064\u005f\u0062\u006c\u006f\u0063\u006b -> hard_block
        json_raw = '{"key": "\\u0068\\u0061\\u0072\\u0064\\u005f\\u0062\\u006c\\u006f\\u0063\\u006b"}'
        parsed = json.loads(json_raw)
        errors = []
        scan_decoded_json(parsed, "dummy.json", 1, errors)
        self.assertTrue(len(errors) > 0)

    def test_24_both_app_py_scanned(self):
        import public_forbidden_scan
        skip_relpaths = public_forbidden_scan._SKIP_RELPATHS
        self.assertNotIn("spaces/huggingface/app.py", skip_relpaths)
        self.assertNotIn("spaces/huggingface_harness/app.py", skip_relpaths)

    def test_25_no_fourth_copy_in_examples(self):
        bad_predictions_path = ROOT / "examples" / "sample20_public_predictions.jsonl"
        self.assertFalse(bad_predictions_path.exists())

    def test_26_no_references_to_schema_minimal(self):
        for p in ROOT.glob("**/*.md"):
            if "node_modules" in p.parts or ".venv" in p.parts or ".git" in p.parts:
                continue
            if "RELEASE_NOTES" in p.name:
                continue
            text = p.read_text(encoding="utf-8")
            self.assertNotIn("schema_minimal.json", text)

    def test_27_docs_point_to_schema_v2(self):
        for path in [
            ROOT / "README.md",
            ROOT / "sample20" / "MANIFEST.md",
            ROOT / "sample20" / "VALIDATION_SUMMARY.md"
        ]:
            text = path.read_text(encoding="utf-8")
            self.assertIn("schema_public_sample20_v2.json", text)

    def test_28_legacy_blocking_state_count_increases(self):
        bad_records = [json.loads(json.dumps(r)) for r in self.records]
        bad_records[0]["model_output"]["safe_next_action"] = "hard_block"
        ok, errors, metrics = validate_records(bad_records, self.schema)
        self.assertFalse(ok)
        self.assertTrue(metrics["legacy_blocking_state_count"] > 0)

    def test_29_package_status_invalid_if_counts_incorrect(self):
        bad_records = [json.loads(json.dumps(r)) for r in self.records][:19]
        ok, errors, metrics = validate_records(bad_records, self.schema)
        self.assertFalse(ok)
        self.assertEqual(metrics["package_status"], "PUBLIC_SAMPLE_INVALID")

    def test_30_unknown_prompt_no_evaluated_metadata(self):
        json_str, loi_fields, _, _, _, _ = semantic_bim_preview("unknown request")
        parsed = json.loads(json_str)
        forbidden_metadata_keys = [
            "case_expectation",
            "expectation_met",
            "record_status",
            "reference_output",
            "agreement",
            "reference_scope"
        ]
        for key in forbidden_metadata_keys:
            self.assertNotIn(key, parsed)

    def test_31_steel_column_no_reinforced_concrete(self):
        json_str, loi_fields, _, _, _, _ = semantic_bim_preview("steel column")
        # Ensure 'reinforced concrete' is not in loi_fields values
        for row in loi_fields:
            val = str(row[1]).lower()
            self.assertNotIn("reinforced concrete", val)

    def test_32_window_no_double_glazing_or_aluminum(self):
        json_str, loi_fields, _, _, _, _ = semantic_bim_preview("window")
        # Ensure double glazing / aluminum frame are not assigned
        for row in loi_fields:
            val = str(row[1]).lower()
            self.assertNotIn("double glazing", val)
            self.assertNotIn("aluminum frame", val)


if __name__ == "__main__":
    unittest.main()
