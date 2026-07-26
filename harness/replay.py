from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from public_sample20_integrity import (
    is_canonical_public_pair,
    verify_canonical_public_integrity,
)
from public_sample20_v2 import validate_records


def resolve_sample_file(path: Path) -> Path:
    if path.is_dir():
        for candidate_name in (
            "sample20_public_records.jsonl",
            "sample20_public_predictions.jsonl",
        ):
            candidate = path / candidate_name
            if candidate.exists():
                return candidate
        candidates = sorted(p for p in path.glob("*.jsonl") if p.is_file())
        if len(candidates) == 1:
            return candidates[0]
        if candidates:
            return candidates[0]
        raise SystemExit(f"SAMPLE_FILE_NOT_FOUND: {path}")
    return path


def resolve_schema_file(sample_path: Path) -> Path | None:
    if sample_path.is_dir():
        candidate = sample_path / "schema_public_sample20_v2.json"
        if candidate.exists():
            return candidate
        candidates = sorted(p for p in sample_path.glob("*.json") if p.is_file())
        if len(candidates) == 1:
            return candidates[0]
    else:
        candidate = sample_path.with_name("schema_public_sample20_v2.json")
        if candidate.exists():
            return candidate
        candidates = sorted(p for p in sample_path.parent.glob("*.json") if p.is_file())
        if len(candidates) == 1:
            return candidates[0]
    return None


def load_jsonl_records(
    sample_file: Path,
) -> tuple[list[dict[str, Any]], int, int, list[str]]:
    records: list[dict[str, Any]] = []
    nonempty_line_count = 0
    parsed_record_count = 0
    parse_errors: list[str] = []

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
                parse_errors.append(
                    f"JSON_PARSE_ERROR line={line_number}: parsed JSON value is not an object"
                )
                continue
            records.append(record)
            parsed_record_count += 1

    return records, nonempty_line_count, parsed_record_count, parse_errors


def _status_token(value: bool | None) -> str:
    if value is None:
        return "NOT_CHECKED"
    return "PASS" if value else "FAIL"


def _emit_error_section(title: str, errors: list[str]) -> None:
    if not errors:
        return
    print(f"{title}:", file=sys.stderr)
    for err in errors[:20]:
        print(f"  {err}", file=sys.stderr)
    if len(errors) > 20:
        print(f"  ... (total {len(errors)} errors)", file=sys.stderr)


def _hash_token(value: str | None) -> str:
    return value if value is not None else "NOT_CHECKED"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate stored public sample20 v2 records."
    )
    parser.add_argument("--sample", required=True, help="Path to sample20/ or the JSONL file.")
    args = parser.parse_args(argv)

    sample_input = Path(args.sample)
    sample_file = resolve_sample_file(sample_input)
    schema_file = resolve_schema_file(sample_input if sample_input.is_dir() else sample_file)

    if not schema_file or not schema_file.exists():
        print(f"ERROR: schema file not found", file=sys.stderr)
        return 1

    try:
        with schema_file.open("r", encoding="utf-8") as sf:
            schema = json.load(sf)
    except Exception as exc:
        print(f"ERROR reading schema: {exc}", file=sys.stderr)
        return 1

    records, nonempty_line_count, parsed_record_count, parse_errors = load_jsonl_records(sample_file)
    json_parse_rate = (
        parsed_record_count / nonempty_line_count if nonempty_line_count else 0.0
    )
    json_parse_ok = (
        nonempty_line_count > 0
        and not parse_errors
        and parsed_record_count == nonempty_line_count
    )

    validation_errors: list[str] = []
    metrics: dict[str, Any] = {
        "valid_case_count": 0,
        "expected_canonical_rejection_count": 0,
        "expectation_met_rate": 0.0,
        "public_schema_valid_rate": 0.0,
    }

    if json_parse_ok:
        ok, validation_errors, metrics = validate_records(records, schema)
        schema_ok = metrics.get("public_schema_valid_rate") == 1.0
        fixture_contract_ok = ok is True
    else:
        schema_ok = False
        fixture_contract_ok = False

    canonical_pair = is_canonical_public_pair(sample_file, schema_file)
    integrity_errors: list[str] = []
    integrity_metrics: dict[str, object] = {
        "jsonl_copy_count": 0,
        "schema_copy_count": 0,
        "jsonl_copy_byte_identity": None,
        "schema_copy_byte_identity": None,
        "jsonl_lf_normalized_sha256": None,
        "schema_lf_normalized_sha256": None,
    }
    if canonical_pair:
        integrity_ok, integrity_errors, integrity_metrics = verify_canonical_public_integrity()
        integrity_scope = "CANONICAL_THREE_COPY"
        integrity_status = _status_token(integrity_ok)
    else:
        integrity_scope = "NONCANONICAL_INPUT"
        integrity_status = "NOT_CHECKED"

    if json_parse_ok:
        json_parse_status = "PASS"
    else:
        json_parse_status = "FAIL"

    if json_parse_ok:
        schema_status = "PASS" if schema_ok else "FAIL"
        fixture_contract_status = "PASS" if fixture_contract_ok else "FAIL"
    else:
        schema_status = "NOT_EVALUATED"
        fixture_contract_status = "NOT_EVALUATED"

    if canonical_pair:
        jsonl_copy_count = int(integrity_metrics.get("jsonl_copy_count", 0))
        schema_copy_count = int(integrity_metrics.get("schema_copy_count", 0))
        jsonl_copy_byte_identity = _status_token(
            integrity_metrics.get("jsonl_copy_byte_identity")
        )
        schema_copy_byte_identity = _status_token(
            integrity_metrics.get("schema_copy_byte_identity")
        )
        jsonl_lf_normalized_sha256 = integrity_metrics.get("jsonl_lf_normalized_sha256")
        schema_lf_normalized_sha256 = integrity_metrics.get("schema_lf_normalized_sha256")
    else:
        jsonl_copy_count = 0
        schema_copy_count = 0
        jsonl_copy_byte_identity = "NOT_CHECKED"
        schema_copy_byte_identity = "NOT_CHECKED"
        jsonl_lf_normalized_sha256 = "NOT_CHECKED"
        schema_lf_normalized_sha256 = "NOT_CHECKED"

    valid_cases = int(metrics.get("valid_case_count", 0)) if json_parse_ok else 0
    expected_rejections = int(metrics.get("expected_canonical_rejection_count", 0)) if json_parse_ok else 0
    expectation_met_rate = float(metrics.get("expectation_met_rate", 0.0)) if json_parse_ok else 0.0
    schema_valid_rate = float(metrics.get("public_schema_valid_rate", 0.0)) if json_parse_ok else 0.0

    if canonical_pair:
        final_status = (
            "PUBLIC_SAMPLE20_V2_VALID"
            if json_parse_status == "PASS"
            and schema_status == "PASS"
            and fixture_contract_status == "PASS"
            and integrity_status == "PASS"
            else "PUBLIC_SAMPLE20_V2_INVALID"
        )
    else:
        final_status = (
            "STORED_RECORD_VALIDATION_VALID_WITHOUT_CANONICAL_INTEGRITY"
            if json_parse_status == "PASS"
            and schema_status == "PASS"
            and fixture_contract_status == "PASS"
            and integrity_status == "NOT_CHECKED"
            else "STORED_RECORD_VALIDATION_INVALID"
        )

    print("SEMANTIC_XAIBIM_PUBLIC_STORED_RECORD_VALIDATION_V3")
    print(f"records={parsed_record_count}")
    print(f"nonempty_lines={nonempty_line_count}")
    print(f"parsed_records={parsed_record_count}")
    print(f"json_parse_rate={json_parse_rate:.6f}")
    print(f"json_parse={json_parse_status}")
    print(f"valid_cases={valid_cases}")
    print(f"expected_rejections={expected_rejections}")
    print(f"expectation_met_rate={expectation_met_rate:.6f}")
    print(f"schema_valid_rate={schema_valid_rate:.6f}")
    print(f"schema={schema_status}")
    print(f"fixture_contract={fixture_contract_status}")
    print(f"integrity_scope={integrity_scope}")
    print(f"jsonl_copy_count={jsonl_copy_count}")
    print(f"jsonl_copy_byte_identity={jsonl_copy_byte_identity}")
    print(f"jsonl_lf_normalized_sha256={_hash_token(jsonl_lf_normalized_sha256)}")
    print(f"schema_copy_count={schema_copy_count}")
    print(f"schema_copy_byte_identity={schema_copy_byte_identity}")
    print(f"schema_lf_normalized_sha256={_hash_token(schema_lf_normalized_sha256)}")
    print(f"integrity={integrity_status}")
    print(f"status={final_status}")

    _emit_error_section("Parsing errors", parse_errors)
    _emit_error_section("Validation errors", validation_errors if json_parse_ok else [])
    _emit_error_section("Integrity errors", integrity_errors if canonical_pair else [])

    return 0 if final_status in {
        "PUBLIC_SAMPLE20_V2_VALID",
        "STORED_RECORD_VALIDATION_VALID_WITHOUT_CANONICAL_INTEGRITY",
    } else 1


if __name__ == "__main__":
    raise SystemExit(main())
