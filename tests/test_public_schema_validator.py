from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VALIDATOR = ROOT / "harness" / "schema_validator.py"
JSONL_PATH = ROOT / "sample20" / "sample20_public_records.jsonl"
SCHEMA_PATH = ROOT / "sample20" / "schema_public_sample20_v2.json"


def run_schema_validator(sample_path: Path, schema_path: Path | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(SCHEMA_VALIDATOR), str(sample_path)]
    if schema_path is not None:
        cmd.extend(["--schema", str(schema_path)])
    return subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def parse_stdout(stdout: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in stdout.splitlines():
        if "=" not in line or line.startswith(" "):
            continue
        key, _, value = line.partition("=")
        parsed[key.strip()] = value.strip()
    return parsed


def load_records() -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in JSONL_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


class TestPublicSchemaValidator(unittest.TestCase):
    def test_00_canonical_directory_success(self):
        result = run_schema_validator(ROOT / "sample20")
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = parse_stdout(result.stdout)
        self.assertEqual(result.stdout.splitlines()[0], "SEMANTIC_XAIBIM_SCHEMA_VALIDATION_V2")
        self.assertTrue(parsed["file"].endswith("sample20_public_records.jsonl"))
        self.assertEqual(parsed["schema"], "PASS")
        self.assertEqual(parsed["status"], "SCHEMA_VALIDATION_OK")

    def test_01_known_prediction_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_dir = tmp_path / "sample"
            sample_dir.mkdir()
            shutil.copyfile(JSONL_PATH, sample_dir / "sample20_public_predictions.jsonl")
            shutil.copyfile(SCHEMA_PATH, sample_dir / "schema_public_sample20_v2.json")
            result = run_schema_validator(sample_dir)

        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = parse_stdout(result.stdout)
        self.assertTrue(parsed["file"].endswith("sample20_public_predictions.jsonl"))
        self.assertTrue(parsed["schema_file"].endswith("schema_public_sample20_v2.json"))
        self.assertEqual(parsed["schema"], "PASS")
        self.assertEqual(parsed["status"], "SCHEMA_VALIDATION_OK")

    def test_02_directory_without_known_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_dir = tmp_path / "sample"
            sample_dir.mkdir()
            (sample_dir / "random.jsonl").write_text("{}\n", encoding="utf-8")
            shutil.copyfile(SCHEMA_PATH, sample_dir / "schema_public_sample20_v2.json")
            result = run_schema_validator(sample_dir)

        self.assertEqual(result.returncode, 2)
        self.assertIn("SAMPLE_FILE_NOT_FOUND", result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_03_schema_root_is_array(self):
        records = load_records()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            sample_file.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
                encoding="utf-8",
            )
            schema_file.write_text("[]\n", encoding="utf-8")
            result = run_schema_validator(sample_file, schema_file)

        self.assertEqual(result.returncode, 1)
        output = result.stdout + result.stderr
        self.assertIn("SCHEMA_DEFINITION_ERROR", output)
        self.assertNotIn("Traceback", output)

    def test_04_invalid_json_schema(self):
        records = load_records()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            sample_file.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
                encoding="utf-8",
            )
            schema_file.write_text('{"type": "not-a-valid-json-schema-type"}\n', encoding="utf-8")
            result = run_schema_validator(sample_file, schema_file)

        self.assertEqual(result.returncode, 1)
        output = result.stdout + result.stderr
        self.assertIn("SCHEMA_DEFINITION_ERROR", output)
        self.assertNotIn("Traceback", output)

    def test_05_explicit_missing_schema(self):
        records = load_records()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            sample_file.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
                encoding="utf-8",
            )
            shutil.copyfile(SCHEMA_PATH, schema_file)
            missing_schema = tmp_path / "missing_schema.json"
            result = run_schema_validator(sample_file, missing_schema)

        self.assertEqual(result.returncode, 2)
        self.assertIn("SCHEMA_FILE_NOT_FOUND", result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_01_canonical_success(self):
        result = run_schema_validator(JSONL_PATH, SCHEMA_PATH)
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = parse_stdout(result.stdout)
        self.assertEqual(result.stdout.splitlines()[0], "SEMANTIC_XAIBIM_SCHEMA_VALIDATION_V2")
        self.assertEqual(parsed["schema_file"], str(SCHEMA_PATH))
        self.assertEqual(parsed["records"], "20")
        self.assertEqual(parsed["json_parse"], "PASS")
        self.assertEqual(parsed["schema"], "PASS")
        self.assertEqual(parsed["schema_valid_records"], "20")
        self.assertEqual(parsed["records_with_required_keys"], "20")
        self.assertEqual(parsed["records_with_evidence_trace"], "20")
        self.assertEqual(parsed["fixture_contract"], "NOT_EVALUATED")
        self.assertEqual(parsed["integrity"], "NOT_CHECKED")
        self.assertEqual(parsed["status"], "SCHEMA_VALIDATION_OK")

    def test_02_nineteen_valid_records(self):
        records = load_records()[:19]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            shutil.copyfile(SCHEMA_PATH, schema_file)
            sample_file.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
                encoding="utf-8",
            )
            result = run_schema_validator(sample_file, schema_file)

        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = parse_stdout(result.stdout)
        self.assertEqual(parsed["json_parse"], "PASS")
        self.assertEqual(parsed["schema"], "PASS")
        self.assertEqual(parsed["records"], "19")
        self.assertEqual(parsed["schema_valid_records"], "19")
        self.assertEqual(parsed["records_with_required_keys"], "19")
        self.assertEqual(parsed["records_with_evidence_trace"], "19")
        self.assertEqual(parsed["fixture_contract"], "NOT_EVALUATED")
        self.assertEqual(parsed["integrity"], "NOT_CHECKED")
        self.assertEqual(parsed["status"], "SCHEMA_VALIDATION_OK")

    def test_03_schema_valid_model_reference_mismatch(self):
        records = load_records()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            shutil.copyfile(SCHEMA_PATH, schema_file)
            records[0]["reference_output"]["ifc_class"] = "IfcBeam"
            sample_file.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
                encoding="utf-8",
            )
            result = run_schema_validator(sample_file, schema_file)

        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = parse_stdout(result.stdout)
        self.assertEqual(parsed["json_parse"], "PASS")
        self.assertEqual(parsed["schema"], "PASS")
        self.assertEqual(parsed["fixture_contract"], "NOT_EVALUATED")
        self.assertEqual(parsed["integrity"], "NOT_CHECKED")

    def test_04_missing_required_key(self):
        records = load_records()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            shutil.copyfile(SCHEMA_PATH, schema_file)
            del records[0]["sample_id"]
            sample_file.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
                encoding="utf-8",
            )
            result = run_schema_validator(sample_file, schema_file)

        self.assertEqual(result.returncode, 1)
        parsed = parse_stdout(result.stdout)
        self.assertEqual(parsed["json_parse"], "PASS")
        self.assertEqual(parsed["schema"], "FAIL")
        self.assertEqual(parsed["schema_valid_records"], "19")
        self.assertEqual(parsed["records_with_required_keys"], "19")

    def test_05_missing_evidence_trace(self):
        records = load_records()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            shutil.copyfile(SCHEMA_PATH, schema_file)
            del records[0]["model_output"]["evidence_trace"]
            sample_file.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
                encoding="utf-8",
            )
            result = run_schema_validator(sample_file, schema_file)

        self.assertEqual(result.returncode, 1)
        parsed = parse_stdout(result.stdout)
        self.assertEqual(parsed["json_parse"], "PASS")
        self.assertEqual(parsed["schema"], "FAIL")
        self.assertEqual(parsed["records_with_evidence_trace"], "19")

    def test_06_json_syntax_failure(self):
        records = load_records()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            shutil.copyfile(SCHEMA_PATH, schema_file)
            lines = [json.dumps(record, ensure_ascii=False) for record in records]
            lines[5] = '{"broken":'
            sample_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
            result = run_schema_validator(sample_file, schema_file)

        self.assertEqual(result.returncode, 1)
        parsed = parse_stdout(result.stdout)
        self.assertEqual(parsed["nonempty_lines"], "20")
        self.assertEqual(parsed["parsed_records"], "19")
        self.assertEqual(parsed["json_parse_rate"], "0.950000")
        self.assertEqual(parsed["json_parse"], "FAIL")
        self.assertEqual(parsed["schema"], "NOT_EVALUATED")
        self.assertEqual(parsed["fixture_contract"], "NOT_EVALUATED")
        self.assertEqual(parsed["integrity"], "NOT_CHECKED")
        self.assertEqual(parsed["status"], "SCHEMA_VALIDATION_FAIL")

    def test_07_non_object_json(self):
        records = load_records()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample_file = tmp_path / "sample.jsonl"
            schema_file = tmp_path / "schema_public_sample20_v2.json"
            shutil.copyfile(SCHEMA_PATH, schema_file)
            lines = [json.dumps(record, ensure_ascii=False) for record in records]
            lines[3] = "[]"
            sample_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
            result = run_schema_validator(sample_file, schema_file)

        self.assertEqual(result.returncode, 1)
        parsed = parse_stdout(result.stdout)
        self.assertEqual(parsed["json_parse"], "FAIL")
        self.assertEqual(parsed["schema"], "NOT_EVALUATED")
        self.assertIn("JSON_OBJECT_REQUIRED", result.stderr)

    def test_08_source_isolation(self):
        text = SCHEMA_VALIDATOR.read_text(encoding="utf-8")
        self.assertNotIn("validate_records", text)
        self.assertNotIn("public_sample20_v2", text)
        self.assertNotIn("verify_canonical_public_integrity", text)


if __name__ == "__main__":
    unittest.main()
