from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
KNOWN_SAMPLE_FILENAMES = ("sample20_public_records.jsonl", "sample20_public_predictions.jsonl")
SCHEMA_FILENAME = "schema_public_" + "sample20_v2.json"


def _resolve_sample_file(sample_path: Path) -> Path | None:
    if sample_path.is_file():
        return sample_path

    if sample_path.is_dir():
        for name in KNOWN_SAMPLE_FILENAMES:
            candidate = sample_path / name
            if candidate.exists():
                return candidate

    return None


def _resolve_schema_path(sample_file: Path, explicit_schema: Path | None) -> Path | None:
    if explicit_schema is not None:
        return explicit_schema

    candidate = sample_file.parent / SCHEMA_FILENAME
    return candidate if candidate.exists() else None


def _has_required_keys(record: dict[str, Any], required_keys: list[str]) -> bool:
    return all(key in record for key in required_keys)


def _has_evidence_trace(record: dict[str, Any]) -> bool:
    for output_name in ("model_output", "reference_output"):
        output = record.get(output_name)
        if not isinstance(output, dict):
            return False
        evidence_trace = output.get("evidence_trace")
        if not isinstance(evidence_trace, dict):
            return False
        if not {"evidence_pattern", "relation_observed", "ambiguity_context"}.issubset(evidence_trace):
            return False
    return True


def _emit_errors(title: str, errors: list[str]) -> None:
    if not errors:
        return
    print(f"{title}:", file=sys.stderr)
    for error in errors[:20]:
        print(f"  {error}", file=sys.stderr)
    if len(errors) > 20:
        print(f"  ... (total {len(errors)} errors)", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Parse JSONL records and validate them against a JSON Schema.",
    )
    parser.add_argument("sample", help="Path to sample20/ or the JSONL file.")
    parser.add_argument(
        "--schema",
        help="Optional explicit schema path. Falls back to schema_public_" + "sample20_v2.json.",
    )
    args = parser.parse_args(argv)

    sample_input = Path(args.sample)
    if not sample_input.exists():
        print("FILE_NOT_FOUND")
        return 2

    sample_file = _resolve_sample_file(sample_input)
    if sample_file is None:
        print("SAMPLE_FILE_NOT_FOUND")
        return 2

    schema_path = _resolve_schema_path(sample_file, Path(args.schema) if args.schema else None)
    if schema_path is None or not schema_path.exists():
        print("SCHEMA_FILE_NOT_FOUND")
        return 2

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: failed to read schema: {exc}")
        return 1

    if not isinstance(schema, dict):
        print("SCHEMA_DEFINITION_ERROR: schema root must be a JSON object")
        return 1

    try:
        jsonschema.Draft202012Validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError as exc:
        message = exc.message if hasattr(exc, "message") else str(exc)
        print(f"SCHEMA_DEFINITION_ERROR: {message}")
        return 1

    parse_errors: list[str] = []
    schema_errors: list[str] = []
    records: list[dict[str, Any]] = []
    nonempty_line_count = 0
    parsed_record_count = 0

    try:
        with sample_file.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                text = line.strip()
                if not text:
                    continue
                nonempty_line_count += 1
                try:
                    record = json.loads(text)
                except json.JSONDecodeError as exc:
                    parse_errors.append(f"JSON_PARSE_ERROR line={line_number}: {exc}")
                    continue
                if not isinstance(record, dict):
                    parse_errors.append(f"JSON_OBJECT_REQUIRED line={line_number}")
                    continue
                records.append(record)
                parsed_record_count += 1
    except Exception as exc:
        print(f"ERROR: failed to read input file: {exc}")
        return 1

    json_parse_rate = parsed_record_count / nonempty_line_count if nonempty_line_count else 0.0
    json_parse_ok = (
        nonempty_line_count > 0
        and not parse_errors
        and parsed_record_count == nonempty_line_count
    )

    root_required_keys = list(schema.get("required", []))
    records_with_required_keys = sum(
        1 for record in records if _has_required_keys(record, root_required_keys)
    )
    records_with_evidence_trace = sum(1 for record in records if _has_evidence_trace(record))

    schema_valid_records = 0
    if json_parse_ok:
        validator = jsonschema.Draft202012Validator(schema)
        for index, record in enumerate(records):
            record_errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
            if record_errors:
                for err in record_errors:
                    schema_errors.append(
                        f"Record {index} schema error at {list(err.path)}: {err.message}"
                    )
            else:
                schema_valid_records += 1

    schema_valid_rate = schema_valid_records / parsed_record_count if parsed_record_count else 0.0
    if not json_parse_ok:
        schema_status = "NOT_EVALUATED"
    elif parsed_record_count > 0 and schema_valid_records == parsed_record_count:
        schema_status = "PASS"
    else:
        schema_status = "FAIL"

    status = "SCHEMA_VALIDATION_OK" if json_parse_ok and schema_status == "PASS" else "SCHEMA_VALIDATION_FAIL"

    print("SEMANTIC_XAIBIM_SCHEMA_VALIDATION_V2")
    print(f"file={sample_file}")
    print(f"schema_file={schema_path}")
    print(f"records={parsed_record_count}")
    print(f"nonempty_lines={nonempty_line_count}")
    print(f"parsed_records={parsed_record_count}")
    print(f"json_parse_rate={json_parse_rate:.6f}")
    print(f"json_parse={'PASS' if json_parse_ok else 'FAIL'}")
    print(f"schema_valid_records={schema_valid_records}")
    print(f"schema_valid_rate={schema_valid_rate:.6f}")
    print(f"schema={schema_status}")
    print(f"records_with_required_keys={records_with_required_keys}")
    print(f"records_with_evidence_trace={records_with_evidence_trace}")
    print("fixture_contract=NOT_EVALUATED")
    print("integrity=NOT_CHECKED")
    print(f"status={status}")

    _emit_errors("Parsing errors", parse_errors)
    _emit_errors("Schema errors", schema_errors)

    if status == "SCHEMA_VALIDATION_OK":
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
