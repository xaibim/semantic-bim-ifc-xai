from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# Forbidden keys in the public sample records at any depth
FORBIDDEN_KEYS = {
    "prompt_payload", "instruction", "metadata", "safety_constraints", "raw_output",
    "json_fragment", "parsed_output", "expected_output", "canonical_output",
    "runtime_context_v1", "source_notes", "source_refs", "source_split",
    "split_profile", "dataset_id", "source_dataset_id", "aiMode", "agent", "cognitive",
    "created_at_utc", "latency_ms", "comparison", "commit_allowed", "safe_block",
    "confidence", "material", "ifc_candidates", "primary_anchor", "scenario_focus",
    "location_context", "recovery_hint", "base_model", "adapter_dir"
}

ALLOWED_VALUE_MODES = {"EXECUTE", "PREVIEW", "PROPOSAL", "GUIDED_RECOVERY"}


def _recall(expected: list[Any], actual: list[Any]) -> float:
    expected_list = list(expected)
    actual_list = list(actual)
    if not expected_list:
        return 1.0 if not actual_list else 0.0
    return len(set(expected_list) & set(actual_list)) / len(expected_list)


def _recompute_agreement(
    model: dict[str, Any],
    reference: dict[str, Any],
) -> dict[str, Any]:
    return {
        "ifc_class": model.get("ifc_class") == reference.get("ifc_class"),
        "semantic_type": model.get("semantic_type") == reference.get("semantic_type"),
        "intent_class": model.get("intent_class") == reference.get("intent_class"),
        "value_mode": model.get("value_mode") == reference.get("value_mode"),
        "dimensions": model.get("normalized_dimensions_m") == reference.get("normalized_dimensions_m"),
        "missing_inputs": model.get("missing_inputs") == reference.get("missing_inputs"),
        "required_psets_recall": _recall(
            reference.get("required_psets", []),
            model.get("required_psets", []),
        ),
        "required_relationships_recall": _recall(
            reference.get("required_relationships", []),
            model.get("required_relationships", []),
        ),
    }


def _dict_value(record: dict[str, Any], key: str) -> dict[str, Any] | None:
    value = record.get(key)
    return value if isinstance(value, dict) else None


def _validate_record_coherence(
    record: dict[str, Any],
    record_index: int,
) -> list[str]:
    errors: list[str] = []
    prefix = f"Record {record_index}:"

    model_output = _dict_value(record, "model_output")
    reference_output = _dict_value(record, "reference_output")
    canonical_check = _dict_value(record, "canonical_check")
    agreement = _dict_value(record, "agreement")
    input_summary = _dict_value(record, "input_summary")

    if model_output is None or reference_output is None:
        errors.append(f"{prefix} model_output and reference_output differ")
        return errors

    if model_output != reference_output:
        errors.append(f"{prefix} model_output and reference_output differ")

    if canonical_check is None or canonical_check.get("ifc_class") != model_output.get("ifc_class"):
        errors.append(f"{prefix} canonical_check.ifc_class does not match model_output.ifc_class")

    if canonical_check is None or canonical_check.get("value_mode") != model_output.get("value_mode"):
        errors.append(f"{prefix} canonical_check.value_mode does not match model_output.value_mode")

    canonical_warnings = canonical_check.get("warnings") if canonical_check is not None else None
    if canonical_warnings != ["reason_codes_at_maximum"]:
        errors.append(f"{prefix} canonical_check.warnings must equal ['reason_codes_at_maximum']")

    recomputed_agreement = _recompute_agreement(model_output, reference_output)
    if agreement != recomputed_agreement:
        errors.append(f"{prefix} stored agreement does not match recomputed agreement")

    for field in ("semantic_type", "ambiguity_flags", "missing_inputs", "recovery_type"):
        model_value = model_output.get(field)
        summary_value = None if input_summary is None else input_summary.get(field)
        if summary_value != model_value:
            errors.append(f"{prefix} input_summary.{field} does not match model_output.{field}")

    for output_name, output in (("model_output", model_output), ("reference_output", reference_output)):
        is_guided_recovery = output.get("value_mode") == "GUIDED_RECOVERY"
        recovery_needed = output.get("recovery_needed") is True
        if is_guided_recovery != recovery_needed:
            errors.append(
                f"{prefix} {output_name} recovery_needed is inconsistent with value_mode"
            )

        evidence_trace = _dict_value(output, "evidence_trace")
        relation_observed = None if evidence_trace is None else evidence_trace.get("relation_observed")
        required_relationships = output.get("required_relationships")
        if isinstance(required_relationships, list):
            relationship_set = set(required_relationships)
        else:
            relationship_set = set()
        if relation_observed not in relationship_set:
            errors.append(
                f"{prefix} {output_name} evidence relation is not declared in required_relationships"
            )

    case_exp = record.get("case_expectation")
    canonical_ok = canonical_check.get("ok") if canonical_check is not None else None
    canonical_errors = canonical_check.get("errors") if canonical_check is not None else None
    if case_exp == "VALID":
        if canonical_ok is not True:
            errors.append(f"{prefix} canonical_check.ok must be true for VALID records")
        if canonical_errors != []:
            errors.append(f"{prefix} canonical_check.errors must be empty for VALID records")
    elif case_exp == "EXPECTED_CANONICAL_REJECTION":
        if canonical_ok is not False:
            errors.append(
                f"{prefix} canonical_check.ok must be false for EXPECTED_CANONICAL_REJECTION records"
            )
        if not isinstance(canonical_errors, list) or len(canonical_errors) == 0:
            errors.append(
                f"{prefix} canonical_check.errors must be non-empty for EXPECTED_CANONICAL_REJECTION records"
            )

    return errors


def check_forbidden_and_legacy(obj: Any, errors: list[str], path: str = "") -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in FORBIDDEN_KEYS:
                errors.append(f"Forbidden key '{k}' found at {path or 'root'}")
            if "hard_block" in k.lower() or "safe_block" in k.lower():
                errors.append(f"Legacy key '{k}' found at {path or 'root'}")
            if isinstance(v, str):
                if "hard_block" in v.lower() or "safe_block" in v.lower():
                    errors.append(f"Legacy token in value of '{k}' at {path or 'root'}: {v}")
            check_forbidden_and_legacy(v, errors, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            check_forbidden_and_legacy(item, errors, f"{path}[{idx}]")


def validate_records(records: list[dict[str, Any]], schema: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    import jsonschema

    errors: list[str] = []
    validator = jsonschema.Draft202012Validator(schema)

    # 1. Check exact record count
    if len(records) != 20:
        errors.append(f"Expected exactly 20 records, found {len(records)}")

    # 2. Check unique sample_ids
    sample_ids = [r.get("sample_id") for r in records]
    unique_ids = set(sample_ids)
    if len(unique_ids) != len(records):
        errors.append(f"Duplicate sample_ids found: {len(records) - len(unique_ids)} duplicates")

    valid_cases = 0
    expected_rejections = 0
    expectation_met_count = 0
    value_mode_counts: dict[str, int] = {vm: 0 for vm in ALLOWED_VALUE_MODES}

    schema_valid_count = 0
    value_mode_conformance_count = 0
    safe_next_action_count = 0

    for idx, r in enumerate(records):
        # Validate schema
        schema_errors = sorted(validator.iter_errors(r), key=lambda e: e.path)
        if schema_errors:
            for err in schema_errors:
                errors.append(f"Record {idx} schema error at {list(err.path)}: {err.message}")
        else:
            schema_valid_count += 1

        # Check forbidden/legacy
        record_errors: list[str] = []
        check_forbidden_and_legacy(r, record_errors)
        if record_errors:
            errors.extend(f"Record {idx}: {err}" for err in record_errors)

        # Coherence check of case_expectation and record_status
        case_exp = r.get("case_expectation")
        rec_status = r.get("record_status")
        exp_met = r.get("expectation_met")
        canonical_check = r.get("canonical_check") or {}

        if case_exp == "VALID":
            valid_cases += 1
            if rec_status != "PASS":
                errors.append(f"Record {idx}: case_expectation VALID but record_status is {rec_status}")
            if canonical_check.get("ok") is not True:
                errors.append(f"Record {idx}: case_expectation VALID but canonical_check.ok is False")
        elif case_exp == "EXPECTED_CANONICAL_REJECTION":
            expected_rejections += 1
            if rec_status != "EXPECTED_REJECTION_PASS":
                errors.append(f"Record {idx}: case_expectation EXPECTED_CANONICAL_REJECTION but record_status is {rec_status}")
            if canonical_check.get("ok") is not False:
                errors.append(f"Record {idx}: EXPECTED_CANONICAL_REJECTION but canonical_check.ok is True")
        else:
            errors.append(f"Record {idx}: unknown case_expectation {case_exp}")

        if exp_met is True:
            expectation_met_count += 1
        else:
            errors.append(f"Record {idx}: expectation_met must be True, got {exp_met}")

        # Check value mode in model_output / reference_output / canonical_check
        val_mode_ok = True
        for path_name, path in (("model_output", "value_mode"), ("reference_output", "value_mode"), ("canonical_check", "value_mode")):
            val_mode = safe_get(r, path_name, path)
            if val_mode not in ALLOWED_VALUE_MODES:
                val_mode_ok = False
                errors.append(f"Record {idx}: value_mode '{val_mode}' at {path_name} not in {ALLOWED_VALUE_MODES}")
        if val_mode_ok:
            value_mode_conformance_count += 1

        # Recalculate value mode counts from model_output
        mo_vm = safe_get(r, "model_output", "value_mode")
        if mo_vm in value_mode_counts:
            value_mode_counts[mo_vm] += 1

        # Check safe_next_action is present and non-empty in model_output / reference_output
        sna_ok = True
        for mo in ("model_output", "reference_output"):
            sna = safe_get(r, mo, "safe_next_action")
            if not isinstance(sna, str) or not sna.strip():
                sna_ok = False
                errors.append(f"Record {idx}: safe_next_action in {mo} is missing or empty")
        if sna_ok:
            safe_next_action_count += 1

        record_coherence_errors = _validate_record_coherence(r, idx)
        if record_coherence_errors:
            errors.extend(record_coherence_errors)

    # Traverse all keys and values recursively to count legacy blocking states
    def count_legacy_tokens(obj: Any) -> int:
        count = 0
        if isinstance(obj, dict):
            for k, v in obj.items():
                if "hard_block" in k.lower() or "safe_block" in k.lower():
                    count += 1
                if isinstance(v, str):
                    if "hard_block" in v.lower() or "safe_block" in v.lower():
                        count += 1
                count += count_legacy_tokens(v)
        elif isinstance(obj, list):
            for item in obj:
                count += count_legacy_tokens(item)
        return count

    legacy_blocking_state_count = sum(count_legacy_tokens(r) for r in records)

    expectation_met_rate = expectation_met_count / len(records) if records else 0.0
    public_schema_valid_rate = schema_valid_count / len(records) if records else 0.0
    public_value_mode_conformance_rate = value_mode_conformance_count / len(records) if records else 0.0
    safe_next_action_rate = safe_next_action_count / len(records) if records else 0.0

    # Determine status
    is_package_valid = (
        len(records) == 20
        and len(unique_ids) == 20
        and valid_cases == 18
        and expected_rejections == 2
        and expectation_met_rate == 1.0
        and public_schema_valid_rate == 1.0
        and legacy_blocking_state_count == 0
        and len(errors) == 0
    )
    package_status = "PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES" if is_package_valid else "PUBLIC_SAMPLE_INVALID"

    metrics = {
        "record_count": len(records),
        "unique_sample_id_count": len(unique_ids),
        "public_schema_valid_rate": public_schema_valid_rate,
        "canonical_validation_rate": valid_cases / len(records) if records else 0.0,
        "valid_case_count": valid_cases,
        "expected_canonical_rejection_count": expected_rejections,
        "expectation_met_rate": expectation_met_rate,
        "public_value_mode_conformance_rate": public_value_mode_conformance_rate,
        "legacy_blocking_state_count": legacy_blocking_state_count,
        "safe_next_action_rate": safe_next_action_rate,
        "PREVIEW": value_mode_counts.get("PREVIEW", 0),
        "PROPOSAL": value_mode_counts.get("PROPOSAL", 0),
        "GUIDED_RECOVERY": value_mode_counts.get("GUIDED_RECOVERY", 0),
        "EXECUTE": value_mode_counts.get("EXECUTE", 0),
        "package_status": package_status
    }

    # Verify counts
    if not errors:
        if valid_cases != 18:
            errors.append(f"Expected exactly 18 valid cases, found {valid_cases}")
        if expected_rejections != 2:
            errors.append(f"Expected exactly 2 expected rejections, found {expected_rejections}")
        if expectation_met_rate != 1.0:
            errors.append(f"Expected expectation_met_rate 1.0, got {expectation_met_rate}")

    return len(errors) == 0, errors, metrics


def safe_get(record: dict[str, Any], parent: str, key: str) -> Any:
    p = record.get(parent)
    if isinstance(p, dict):
        return p.get(key)
    return None
