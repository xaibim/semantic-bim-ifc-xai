"""
verify_qlora_public_metrics.py
==============================
Deterministic verifier for the public QLoRA preliminary results JSON.

The verifier checks aggregate document structure, value types, bounded ranges,
distribution totals, internal consistency and derived compute arithmetic.
It does not rerun training, access raw predictions, independently validate
superiority, or establish generalization.

Uses Python standard library only - no external dependencies.

Exit 0  -> all checks pass, prints QLORA_PUBLIC_AGGREGATE_SELF_CONSISTENCY_VALID
Exit 1  -> at least one check failed
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
JSON_PATH = REPO_ROOT / "benchmark" / "qlora" / "xaibim_qwen25_7b_qlora_preliminary_public_results.json"

EXPECTED_KAGGLE_URL = "https://www.kaggle.com/code/xaibim/semantic-bim-ifc-xai"
EXPECTED_TOKEN = "QLORA_PUBLIC_AGGREGATE_SELF_CONSISTENCY_VALID"
ABS_TOL = 1e-9
REL_TOL = 1e-9

VERIFICATION_BOUNDARY_EXPECTED = {
    "public_verifier_scope": "aggregate_structure_and_derived_calculation_self_consistency",
    "raw_predictions_available": False,
    "held_out_metrics_publicly_recomputable": False,
    "empirical_results_independently_validated_by_repository": False,
}


def close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=REL_TOL, abs_tol=ABS_TOL)


def is_numeric(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def check(failures: list[str], label: str, condition: bool, message: str | None = None) -> None:
    if not condition:
        if message:
            print(f"FAIL [{label}]: {message}")
        failures.append(label)


def require_key(container: object, key: str, label: str, failures: list[str]) -> object:
    if not isinstance(container, dict) or key not in container:
        check(failures, label, False, f"missing key {key!r}")
        return None
    return container[key]


def ensure_structure(data: dict[str, object], failures: list[str]) -> None:
    for key in [
        "artifact_type",
        "artifact_version",
        "title",
        "kaggle_notebook_url",
        "scope",
        "data",
        "model_and_training",
        "compute",
        "derived_calculations",
        "calculation_methodology",
        "corrected_held_out_results",
        "limitations",
        "public_boundary",
        "verification_boundary",
    ]:
        check(failures, f"top_level.{key}", key in data, f"missing top-level key {key!r}")

    scope = data.get("scope")
    check(failures, "scope.type", isinstance(scope, dict), "scope must be an object")
    if isinstance(scope, dict):
        check(failures, "scope.purpose", isinstance(scope.get("purpose"), str), "scope.purpose must be a string")
        check(
            failures,
            "scope.not_claimed",
            isinstance(scope.get("not_claimed"), list),
            "scope.not_claimed must be a list",
        )

    data_section = data.get("data")
    check(failures, "data.type", isinstance(data_section, dict), "data must be an object")
    if isinstance(data_section, dict):
        for key in [
            "dataset_visibility",
            "record_count",
            "dataset_sha256",
            "split_strategy",
            "train_records",
            "validation_records",
            "test_records",
            "train_families",
            "validation_families",
            "test_families",
            "legacy_normalized_records",
        ]:
            check(failures, f"data.{key}", key in data_section, f"missing data key {key!r}")

    model_training = data.get("model_and_training")
    check(failures, "model_and_training.type", isinstance(model_training, dict), "model_and_training must be an object")
    if isinstance(model_training, dict):
        for key in [
            "base_model",
            "method",
            "epochs",
            "seed",
            "lora_rank",
            "lora_alpha",
            "lora_dropout",
            "learning_rate",
            "effective_batch_size",
            "adapter_sha256",
            "adapter_size_bytes",
            "adapter_publicly_released",
        ]:
            check(failures, f"model_and_training.{key}", key in model_training, f"missing model_and_training key {key!r}")

    compute = data.get("compute")
    check(failures, "compute.type", isinstance(compute, dict), "compute must be an object")
    if isinstance(compute, dict):
        for key in [
            "allocated_gpu_count",
            "allocated_gpu_names",
            "effective_gpu_count",
            "training_runtime_seconds",
            "training_peak_allocated_vram_gb",
            "training_peak_reserved_vram_gb",
            "training_samples_per_second",
            "training_steps_per_second",
            "training_loss",
            "measured_end_to_end_runtime_seconds",
            "effective_gpu_hours",
            "allocated_gpu_hours",
            "validation_loss",
        ]:
            check(failures, f"compute.{key}", key in compute, f"missing compute key {key!r}")

    derived = data.get("derived_calculations")
    check(failures, "derived_calculations.type", isinstance(derived, dict), "derived_calculations must be an object")
    if isinstance(derived, dict):
        for key in [
            "training_runtime_hours",
            "end_to_end_runtime_hours",
            "non_training_overhead_seconds",
            "non_training_overhead_hours",
            "effective_gpu_hours_recomputed",
            "allocated_gpu_hours_recomputed",
            "expected_optimizer_steps",
            "adapter_size_mib",
            "training_runtime_share_percent",
            "non_training_runtime_share_percent",
        ]:
            check(failures, f"derived_calculations.{key}", key in derived, f"missing derived key {key!r}")

    corrected = data.get("corrected_held_out_results")
    check(failures, "corrected_held_out_results.type", isinstance(corrected, dict), "corrected_held_out_results must be an object")
    if isinstance(corrected, dict):
        for key in ["baseline", "adapter", "test_distribution", "evaluator_correction_note", "intent_class_note", "evidence_trace_metric_boundary", "interpretation"]:
            check(failures, f"corrected_held_out_results.{key}", key in corrected, f"missing corrected_held_out_results key {key!r}")

    verification_boundary = data.get("verification_boundary")
    check(failures, "verification_boundary.type", isinstance(verification_boundary, dict), "verification_boundary must be an object")
    if isinstance(verification_boundary, dict):
        for key, expected in VERIFICATION_BOUNDARY_EXPECTED.items():
            check(
                failures,
                f"verification_boundary.{key}",
                verification_boundary.get(key) == expected,
                f"expected {expected!r}, got {verification_boundary.get(key)!r}",
            )


def validate_numeric_ranges(data: dict[str, object], failures: list[str]) -> None:
    data_section = data["data"]
    model_training = data["model_and_training"]
    compute = data["compute"]
    corrected = data["corrected_held_out_results"]
    baseline = corrected["baseline"]
    adapter = corrected["adapter"]

    record_count = data_section["record_count"]
    train_records = data_section["train_records"]
    validation_records = data_section["validation_records"]
    test_records = data_section["test_records"]
    train_families = data_section["train_families"]
    validation_families = data_section["validation_families"]
    test_families = data_section["test_families"]

    check(failures, "data.record_count.int", isinstance(record_count, int) and not isinstance(record_count, bool), "record_count must be an int")
    check(failures, "data.record_count.positive", record_count > 0, "record_count must be positive")
    check(failures, "data.split_sum", train_records + validation_records + test_records == record_count, "train+validation+test must equal record_count")
    check(failures, "data.family_sum", train_families + validation_families + test_families == 100, "family counts must sum to 100")

    for label, value in [
        ("compute.training_runtime_seconds", compute["training_runtime_seconds"]),
        ("compute.measured_end_to_end_runtime_seconds", compute["measured_end_to_end_runtime_seconds"]),
        ("compute.training_peak_allocated_vram_gb", compute["training_peak_allocated_vram_gb"]),
        ("compute.training_peak_reserved_vram_gb", compute["training_peak_reserved_vram_gb"]),
        ("compute.effective_gpu_count", compute["effective_gpu_count"]),
        ("compute.allocated_gpu_count", compute["allocated_gpu_count"]),
        ("compute.effective_gpu_hours", compute["effective_gpu_hours"]),
        ("compute.allocated_gpu_hours", compute["allocated_gpu_hours"]),
    ]:
        check(failures, f"{label}.numeric", is_numeric(value), f"{label} must be numeric")
        if is_numeric(value):
            check(failures, f"{label}.positive", float(value) > 0, f"{label} must be positive")

    check(
        failures,
        "compute.effective_gpus_le_allocated",
        compute["effective_gpu_count"] <= compute["allocated_gpu_count"],
        "effective GPU count must be <= allocated GPU count",
    )

    for label, value in [
        ("derived.training_runtime_hours", data["derived_calculations"]["training_runtime_hours"]),
        ("derived.end_to_end_runtime_hours", data["derived_calculations"]["end_to_end_runtime_hours"]),
        ("derived.non_training_overhead_seconds", data["derived_calculations"]["non_training_overhead_seconds"]),
        ("derived.non_training_overhead_hours", data["derived_calculations"]["non_training_overhead_hours"]),
        ("derived.effective_gpu_hours_recomputed", data["derived_calculations"]["effective_gpu_hours_recomputed"]),
        ("derived.allocated_gpu_hours_recomputed", data["derived_calculations"]["allocated_gpu_hours_recomputed"]),
        ("derived.expected_optimizer_steps", data["derived_calculations"]["expected_optimizer_steps"]),
        ("derived.adapter_size_mib", data["derived_calculations"]["adapter_size_mib"]),
        ("derived.training_runtime_share_percent", data["derived_calculations"]["training_runtime_share_percent"]),
        ("derived.non_training_runtime_share_percent", data["derived_calculations"]["non_training_runtime_share_percent"]),
    ]:
        check(failures, f"{label}.numeric", is_numeric(value), f"{label} must be numeric")

    for container_name, container in [("baseline", baseline), ("adapter", adapter)]:
        check(failures, f"{container_name}.record_count", container["record_count"] == test_records, f"{container_name} record_count must equal test_records")
        for key, value in container.items():
            if key == "record_count":
                continue
            check(failures, f"{container_name}.{key}.numeric", is_numeric(value), f"{container_name}.{key} must be numeric")
            if is_numeric(value):
                check(
                    failures,
                    f"{container_name}.{key}.range",
                    0.0 <= float(value) <= 1.0,
                    f"{container_name}.{key} must be within [0.0, 1.0]",
                )

    for dim_name, expected_total in [
        ("intent_class", test_records),
        ("semantic_type", test_records),
        ("ifc_class", test_records),
        ("value_mode", test_records),
    ]:
        dist = corrected["test_distribution"][dim_name]
        check(
            failures,
            f"test_distribution.{dim_name}.sum",
            sum(dist.values()) == expected_total,
            f"{dim_name} distribution must sum to {expected_total}",
        )

    for name in ["training_runtime_hours", "end_to_end_runtime_hours", "non_training_overhead_hours"]:
        check(
            failures,
            f"derived.{name}.consistency",
            is_numeric(data["derived_calculations"][name]),
            f"{name} must be numeric",
        )


def validate_derived_arithmetic(data: dict[str, object], failures: list[str]) -> None:
    compute = data["compute"]
    derived = data["derived_calculations"]
    model_training = data["model_and_training"]
    data_section = data["data"]

    training_s = float(compute["training_runtime_seconds"])
    end_to_end_s = float(compute["measured_end_to_end_runtime_seconds"])
    effective_gpus = int(compute["effective_gpu_count"])
    allocated_gpus = int(compute["allocated_gpu_count"])
    adapter_bytes = int(model_training["adapter_size_bytes"])
    train_records = int(data_section["train_records"])
    effective_batch = int(model_training["effective_batch_size"])
    epochs = int(model_training["epochs"])

    expected_training_h = training_s / 3600.0
    expected_end_to_end_h = end_to_end_s / 3600.0
    expected_overhead_s = end_to_end_s - training_s
    expected_overhead_h = expected_overhead_s / 3600.0
    expected_effective_gpu_h = expected_end_to_end_h * effective_gpus
    expected_allocated_gpu_h = expected_end_to_end_h * allocated_gpus
    expected_adapter_mib = adapter_bytes / 1_048_576
    expected_training_share = training_s / end_to_end_s * 100.0
    expected_non_training_share = expected_overhead_s / end_to_end_s * 100.0
    expected_optimizer_steps = (train_records // effective_batch) * epochs

    checks = [
        ("derived.training_runtime_hours", derived["training_runtime_hours"], expected_training_h),
        ("derived.end_to_end_runtime_hours", derived["end_to_end_runtime_hours"], expected_end_to_end_h),
        ("derived.non_training_overhead_seconds", derived["non_training_overhead_seconds"], expected_overhead_s),
        ("derived.non_training_overhead_hours", derived["non_training_overhead_hours"], expected_overhead_h),
        ("derived.effective_gpu_hours_recomputed", derived["effective_gpu_hours_recomputed"], expected_effective_gpu_h),
        ("derived.allocated_gpu_hours_recomputed", derived["allocated_gpu_hours_recomputed"], expected_allocated_gpu_h),
        ("derived.expected_optimizer_steps", derived["expected_optimizer_steps"], expected_optimizer_steps),
        ("derived.adapter_size_mib", derived["adapter_size_mib"], expected_adapter_mib),
        ("derived.training_runtime_share_percent", derived["training_runtime_share_percent"], expected_training_share),
        ("derived.non_training_runtime_share_percent", derived["non_training_runtime_share_percent"], expected_non_training_share),
    ]
    for label, actual, expected in checks:
        if isinstance(expected, float):
            check(failures, label, close(float(actual), expected), f"expected {expected!r}, got {actual!r}")
        else:
            check(failures, label, actual == expected, f"expected {expected!r}, got {actual!r}")

    share_sum = float(derived["training_runtime_share_percent"]) + float(derived["non_training_runtime_share_percent"])
    check(failures, "derived.share_sum_to_100", close(share_sum, 100.0), f"share sum must equal 100, got {share_sum!r}")


def main() -> int:
    if not JSON_PATH.exists():
        print(f"FAIL: JSON not found at {JSON_PATH}")
        return 1

    with open(JSON_PATH, encoding="utf-8") as fh:
        data = json.load(fh)

    failures: list[str] = []

    check(failures, "kaggle_url", data.get("kaggle_notebook_url") == EXPECTED_KAGGLE_URL, "unexpected Kaggle notebook URL")
    check(
        failures,
        "adapter_publicly_released",
        data.get("model_and_training", {}).get("adapter_publicly_released") is False,
        "adapter_publicly_released must be false",
    )

    ensure_structure(data, failures)
    if failures:
        print(f"\nFAILED checks: {failures}")
        return 1

    validate_numeric_ranges(data, failures)
    validate_derived_arithmetic(data, failures)

    if failures:
        print(f"\nFAILED checks: {failures}")
        return 1

    print(EXPECTED_TOKEN)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
