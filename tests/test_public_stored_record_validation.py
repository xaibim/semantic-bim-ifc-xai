from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness"))

from public_sample20_integrity import (  # noqa: E402
    EXPECTED_JSONL_LF_NORMALIZED_SHA256,
    EXPECTED_SCHEMA_LF_NORMALIZED_SHA256,
    is_canonical_public_pair,
    sha256_lf_normalized,
    verify_canonical_public_integrity,
    verify_copy_integrity,
)
from public_sample20_v2 import validate_records  # noqa: E402

JSONL_PATH = ROOT / "sample20" / "sample20_public_records.jsonl"
SCHEMA_PATH = ROOT / "sample20" / "schema_public_sample20_v2.json"
REPLAY_SCRIPT = ROOT / "harness" / "replay.py"


def parse_cli_output(stdout: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in stdout.splitlines():
        if "=" not in line or line.startswith(" "):
            continue
        key, _, value = line.partition("=")
        parsed[key.strip()] = value.strip()
    return parsed


def run_replay(sample_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPLAY_SCRIPT), "--sample", str(sample_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def load_canonical_records() -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in JSONL_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


class TestPublicStoredRecordValidation(unittest.TestCase):
    def test_01_canonical_cli_success(self):
        result = run_replay(ROOT / "sample20")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines()[0], "SEMANTIC_XAIBIM_PUBLIC_STORED_RECORD_VALIDATION_V3")
        parsed = parse_cli_output(result.stdout)
        self.assertEqual(parsed["records"], "20")
        self.assertEqual(parsed["nonempty_lines"], "20")
        self.assertEqual(parsed["parsed_records"], "20")
        self.assertEqual(parsed["json_parse_rate"], "1.000000")
        self.assertEqual(parsed["json_parse"], "PASS")
        self.assertEqual(parsed["valid_cases"], "18")
        self.assertEqual(parsed["expected_rejections"], "2")
        self.assertEqual(parsed["expectation_met_rate"], "1.000000")
        self.assertEqual(parsed["schema_valid_rate"], "1.000000")
        self.assertEqual(parsed["schema"], "PASS")
        self.assertEqual(parsed["fixture_contract"], "PASS")
        self.assertEqual(parsed["integrity_scope"], "CANONICAL_THREE_COPY")
        self.assertEqual(parsed["jsonl_copy_count"], "3")
        self.assertEqual(parsed["jsonl_copy_byte_identity"], "PASS")
        self.assertEqual(parsed["jsonl_lf_normalized_sha256"], EXPECTED_JSONL_LF_NORMALIZED_SHA256)
        self.assertEqual(parsed["schema_copy_count"], "3")
        self.assertEqual(parsed["schema_copy_byte_identity"], "PASS")
        self.assertEqual(parsed["schema_lf_normalized_sha256"], EXPECTED_SCHEMA_LF_NORMALIZED_SHA256)
        self.assertEqual(parsed["integrity"], "PASS")
        self.assertEqual(parsed["status"], "PUBLIC_SAMPLE20_V2_VALID")

    def test_02_validate_records_has_no_parse_rate(self):
        records = load_canonical_records()
        with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
            schema = json.load(handle)
        ok, errors, metrics = validate_records(records, schema)
        self.assertTrue(ok, errors)
        self.assertNotIn("json_parse_rate", metrics)

    def test_03_json_parse_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            shutil.copyfile(SCHEMA_PATH, schema_file)
            lines = JSONL_PATH.read_text(encoding="utf-8").splitlines()
            lines[5] = '{"broken":'
            sample_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

            result = run_replay(tmp_path)

        self.assertEqual(result.returncode, 1)
        parsed = parse_cli_output(result.stdout)
        self.assertEqual(parsed["nonempty_lines"], "20")
        self.assertEqual(parsed["parsed_records"], "19")
        self.assertEqual(parsed["json_parse_rate"], "0.950000")
        self.assertEqual(parsed["json_parse"], "FAIL")
        self.assertEqual(parsed["schema"], "NOT_EVALUATED")
        self.assertEqual(parsed["fixture_contract"], "NOT_EVALUATED")
        self.assertEqual(parsed["integrity_scope"], "NONCANONICAL_INPUT")
        self.assertEqual(parsed["integrity"], "NOT_CHECKED")
        self.assertEqual(parsed["status"], "STORED_RECORD_VALIDATION_INVALID")

    def test_04_schema_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            shutil.copyfile(JSONL_PATH, sample_file)
            schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
            schema["properties"]["sample_id"]["type"] = "integer"
            schema_file.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")

            result = run_replay(tmp_path)

        self.assertEqual(result.returncode, 1)
        parsed = parse_cli_output(result.stdout)
        self.assertEqual(parsed["json_parse"], "PASS")
        self.assertEqual(parsed["schema"], "FAIL")
        self.assertEqual(parsed["fixture_contract"], "FAIL")
        self.assertEqual(parsed["integrity_scope"], "NONCANONICAL_INPUT")
        self.assertEqual(parsed["integrity"], "NOT_CHECKED")

    def test_05_noncanonical_valid_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            shutil.copyfile(JSONL_PATH, sample_file)
            shutil.copyfile(SCHEMA_PATH, schema_file)

            result = run_replay(tmp_path)

        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = parse_cli_output(result.stdout)
        self.assertEqual(parsed["json_parse"], "PASS")
        self.assertEqual(parsed["schema"], "PASS")
        self.assertEqual(parsed["fixture_contract"], "PASS")
        self.assertEqual(parsed["integrity_scope"], "NONCANONICAL_INPUT")
        self.assertEqual(parsed["jsonl_copy_count"], "0")
        self.assertEqual(parsed["jsonl_copy_byte_identity"], "NOT_CHECKED")
        self.assertEqual(parsed["schema_copy_count"], "0")
        self.assertEqual(parsed["schema_copy_byte_identity"], "NOT_CHECKED")
        self.assertEqual(parsed["integrity"], "NOT_CHECKED")
        self.assertEqual(
            parsed["status"],
            "STORED_RECORD_VALIDATION_VALID_WITHOUT_CANONICAL_INTEGRITY",
        )

    def test_06_integrity_success(self):
        jsonl_hash = None
        schema_hash = None
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            jsonl_paths = []
            schema_paths = []
            for index, source in enumerate(
                (
                    JSONL_PATH,
                    ROOT / "spaces" / "huggingface" / "sample20_public_predictions.jsonl",
                    ROOT / "spaces" / "huggingface_harness" / "sample20_public_predictions.jsonl",
                ),
                start=1,
            ):
                target = tmp_path / f"sample{index}.jsonl"
                shutil.copyfile(source, target)
                jsonl_paths.append(target)
            for index, source in enumerate(
                (
                    SCHEMA_PATH,
                    ROOT / "spaces" / "huggingface" / "schema_public_sample20_v2.json",
                    ROOT / "spaces" / "huggingface_harness" / "schema_public_sample20_v2.json",
                ),
                start=1,
            ):
                target = tmp_path / f"schema{index}.json"
                shutil.copyfile(source, target)
                schema_paths.append(target)

            jsonl_hash = sha256_lf_normalized(jsonl_paths[0])
            schema_hash = sha256_lf_normalized(schema_paths[0])
            ok, errors, metrics = verify_copy_integrity(
                jsonl_paths,
                schema_paths,
                jsonl_hash,
                schema_hash,
            )

        self.assertTrue(ok, errors)
        self.assertTrue(metrics["jsonl_copy_byte_identity"])
        self.assertTrue(metrics["schema_copy_byte_identity"])
        self.assertEqual(metrics["jsonl_lf_normalized_sha256"], jsonl_hash)
        self.assertEqual(metrics["schema_lf_normalized_sha256"], schema_hash)

    def test_07_jsonl_integrity_failure(self):
        jsonl_hash = None
        schema_hash = None
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            jsonl_paths = []
            schema_paths = []
            for index, source in enumerate(
                (
                    JSONL_PATH,
                    ROOT / "spaces" / "huggingface" / "sample20_public_predictions.jsonl",
                    ROOT / "spaces" / "huggingface_harness" / "sample20_public_predictions.jsonl",
                ),
                start=1,
            ):
                target = tmp_path / f"sample{index}.jsonl"
                shutil.copyfile(source, target)
                jsonl_paths.append(target)
            for index, source in enumerate(
                (
                    SCHEMA_PATH,
                    ROOT / "spaces" / "huggingface" / "schema_public_sample20_v2.json",
                    ROOT / "spaces" / "huggingface_harness" / "schema_public_sample20_v2.json",
                ),
                start=1,
            ):
                target = tmp_path / f"schema{index}.json"
                shutil.copyfile(source, target)
                schema_paths.append(target)

            records = [
                json.loads(line)
                for line in jsonl_paths[1].read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            records[0]["sample_id"] = "mutated-sample-id"
            jsonl_paths[1].write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
                encoding="utf-8",
            )

            jsonl_hash = sha256_lf_normalized(jsonl_paths[0])
            schema_hash = sha256_lf_normalized(schema_paths[0])
            ok, errors, metrics = verify_copy_integrity(
                jsonl_paths,
                schema_paths,
                jsonl_hash,
                schema_hash,
            )

        self.assertFalse(ok)
        self.assertIn("JSONL copies are not byte-identical", errors)
        self.assertFalse(metrics["jsonl_copy_byte_identity"])

    def test_08_schema_integrity_failure(self):
        jsonl_hash = None
        schema_hash = None
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            jsonl_paths = []
            schema_paths = []
            for index, source in enumerate(
                (
                    JSONL_PATH,
                    ROOT / "spaces" / "huggingface" / "sample20_public_predictions.jsonl",
                    ROOT / "spaces" / "huggingface_harness" / "sample20_public_predictions.jsonl",
                ),
                start=1,
            ):
                target = tmp_path / f"sample{index}.jsonl"
                shutil.copyfile(source, target)
                jsonl_paths.append(target)
            for index, source in enumerate(
                (
                    SCHEMA_PATH,
                    ROOT / "spaces" / "huggingface" / "schema_public_sample20_v2.json",
                    ROOT / "spaces" / "huggingface_harness" / "schema_public_sample20_v2.json",
                ),
                start=1,
            ):
                target = tmp_path / f"schema{index}.json"
                shutil.copyfile(source, target)
                schema_paths.append(target)

            schema_data = json.loads(schema_paths[2].read_text(encoding="utf-8"))
            schema_data["title"] = "mutated schema"
            schema_paths[2].write_text(json.dumps(schema_data, indent=2) + "\n", encoding="utf-8")

            jsonl_hash = sha256_lf_normalized(jsonl_paths[0])
            schema_hash = sha256_lf_normalized(schema_paths[0])
            ok, errors, metrics = verify_copy_integrity(
                jsonl_paths,
                schema_paths,
                jsonl_hash,
                schema_hash,
            )

        self.assertFalse(ok)
        self.assertIn("Schema copies are not byte-identical", errors)
        self.assertFalse(metrics["schema_copy_byte_identity"])

    def test_09_hash_mismatch(self):
        jsonl_hash = None
        schema_hash = None
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            jsonl_paths = []
            schema_paths = []
            for index, source in enumerate(
                (
                    JSONL_PATH,
                    ROOT / "spaces" / "huggingface" / "sample20_public_predictions.jsonl",
                    ROOT / "spaces" / "huggingface_harness" / "sample20_public_predictions.jsonl",
                ),
                start=1,
            ):
                target = tmp_path / f"sample{index}.jsonl"
                shutil.copyfile(source, target)
                jsonl_paths.append(target)
            for index, source in enumerate(
                (
                    SCHEMA_PATH,
                    ROOT / "spaces" / "huggingface" / "schema_public_sample20_v2.json",
                    ROOT / "spaces" / "huggingface_harness" / "schema_public_sample20_v2.json",
                ),
                start=1,
            ):
                target = tmp_path / f"schema{index}.json"
                shutil.copyfile(source, target)
                schema_paths.append(target)

            jsonl_hash = sha256_lf_normalized(jsonl_paths[0])
            schema_hash = sha256_lf_normalized(schema_paths[0])
            ok, errors, metrics = verify_copy_integrity(
                jsonl_paths,
                schema_paths,
                "0000000000000000000000000000000000000000000000000000000000000000",
                "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            )

        self.assertFalse(ok)
        self.assertTrue(any("mismatch" in err.lower() for err in errors))
        self.assertEqual(metrics["jsonl_lf_normalized_sha256"], jsonl_hash)
        self.assertEqual(metrics["schema_lf_normalized_sha256"], schema_hash)

    def test_10_status_independence(self):
        records = load_canonical_records()
        with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
            schema = json.load(handle)
        ok, errors, metrics = validate_records(records, schema)
        self.assertTrue(ok, errors)
        self.assertNotIn("json_parse_rate", metrics)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            shutil.copyfile(JSONL_PATH, sample_file)
            shutil.copyfile(SCHEMA_PATH, schema_file)
            result = run_replay(tmp_path)
        parsed = parse_cli_output(result.stdout)
        self.assertEqual(parsed["schema"], "PASS")
        self.assertEqual(parsed["integrity"], "NOT_CHECKED")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            shutil.copyfile(JSONL_PATH, sample_file)
            schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
            schema["properties"]["sample_id"]["type"] = "integer"
            schema_file.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
            result = run_replay(tmp_path)
        parsed = parse_cli_output(result.stdout)
        self.assertEqual(parsed["schema"], "FAIL")
        self.assertEqual(parsed["integrity"], "NOT_CHECKED")

    def test_11_documentation(self):
        docs = [
            ROOT / "QUICKSTART.md",
            ROOT / "PUBLIC_EVIDENCE.md",
            ROOT / "sample20" / "VALIDATION_SUMMARY.md",
            ROOT / "benchmark" / "results_sample20.md",
        ]
        old_phrases = [
            "Deterministic public " + "replay completed successfully",
            "Executed " + "Replay",
            "Run the public replay",
        ]
        new_phrases = [
            "deterministic stored-record validation",
            "JSON parsing",
            "schema validation",
            "fixture-contract validation",
            "canonical three-copy integrity",
        ]
        for path in docs:
            text = path.read_text(encoding="utf-8")
            lower = text.lower()
            for phrase in old_phrases:
                self.assertNotIn(phrase, text)
            for phrase in new_phrases:
                self.assertIn(phrase.lower(), lower)
        self.assertTrue(is_canonical_public_pair(JSONL_PATH, SCHEMA_PATH))
        self.assertTrue(verify_canonical_public_integrity()[0])


if __name__ == "__main__":
    unittest.main()
