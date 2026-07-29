from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import math
import os
import platform
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_JSONL = ROOT / "sample20" / "sample20_public_records.jsonl"
SAMPLE_SCHEMA = ROOT / "sample20" / "schema_public_sample20_v2.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_jsonl_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                value = json.loads(text)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"Invalid JSONL at line {line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise RuntimeError(f"Expected object at line {line_number}, got {type(value).__name__}")
            records.append(value)
    return records


def load_schema(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def canonical_dumps(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return ordered[index]


def ns_to_seconds(value: int) -> float:
    return value / 1_000_000_000.0


def timing_loop(func: Callable[[], int], warmup_rounds: int, measured_rounds: int) -> tuple[list[float], list[float]]:
    warmups: list[float] = []
    measurements: list[float] = []

    for _ in range(warmup_rounds):
        start = time.perf_counter_ns()
        func()
        end = time.perf_counter_ns()
        warmups.append(ns_to_seconds(end - start))

    for _ in range(measured_rounds):
        start = time.perf_counter_ns()
        func()
        end = time.perf_counter_ns()
        measurements.append(ns_to_seconds(end - start))

    return warmups, measurements


def summarize_rounds(
    *,
    logical_records: int,
    repetitions: int,
    warmup_rounds: int,
    measured_rounds: int,
    warmup_seconds: list[float],
    measured_seconds: list[float],
    bytes_processed: int | None,
) -> dict[str, Any]:
    mean_seconds = statistics.mean(measured_seconds) if measured_seconds else 0.0
    median_seconds = statistics.median(measured_seconds) if measured_seconds else 0.0
    result = {
        "logical_records": logical_records,
        "repetitions": repetitions,
        "warmup_rounds": warmup_rounds,
        "measured_rounds": measured_rounds,
        "warmup_round_seconds": warmup_seconds,
        "measured_round_seconds": measured_seconds,
        "total_seconds": measured_seconds,
        "mean_seconds": mean_seconds,
        "median_seconds": median_seconds,
        "p95_seconds": p95(measured_seconds),
        "records_per_second": (logical_records / mean_seconds) if mean_seconds > 0 else 0.0,
    }
    if bytes_processed is not None:
        result["bytes_processed"] = bytes_processed
    return result


def build_environment() -> dict[str, Any]:
    try:
        import torch

        torch_version = getattr(torch, "__version__", None)
        cuda_available = bool(torch.cuda.is_available())
        cuda_runtime_version = getattr(torch.version, "cuda", None)
        if cuda_available:
            gpu_name = torch.cuda.get_device_name(0)
        else:
            gpu_name = "not_executed_model_not_provided"
    except Exception:
        torch_version = None
        cuda_available = False
        cuda_runtime_version = None
        gpu_name = "not_executed_model_not_provided"

    return {
        "operating_system_family": platform.system(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "processor_logical_count": os.cpu_count(),
        "cuda_available": cuda_available,
        "generic_gpu_name": gpu_name,
        "torch_version": torch_version,
        "cuda_runtime_version": cuda_runtime_version,
    }


def build_cpu_results(
    records: list[dict[str, Any]],
    schema: dict[str, Any],
    logical_records: int,
    warmup_rounds: int,
    measured_rounds: int,
) -> dict[str, Any]:
    validator = Draft202012Validator(schema)
    base_raw_records = [canonical_dumps(record) for record in records]
    base_serialized_records = [canonical_dumps(record) for record in records]
    repetitions = logical_records // len(records)
    if repetitions * len(records) != logical_records:
        raise ValueError("logical_records must be a multiple of the 20 public records")

    def iter_logical_records() -> list[tuple[int, int, dict[str, Any], str, str]]:
        items: list[tuple[int, int, dict[str, Any], str, str]] = []
        for repetition in range(repetitions):
            for index, record in enumerate(records):
                raw = base_raw_records[index]
                serialized = base_serialized_records[index]
                items.append((repetition, index, record, raw, serialized))
        return items

    logical_items = iter_logical_records()
    sample_bytes = sum(len(item[3].encode("utf-8")) for item in logical_items)
    serialized_bytes = sum(len(item[4].encode("utf-8")) for item in logical_items)

    def run_json_parsing() -> int:
        total = 0
        for _, _, _, raw, _ in logical_items:
            parsed = json.loads(raw)
            total += len(parsed)
        return total

    def run_schema_validation() -> int:
        total = 0
        for _, _, record, _, _ in logical_items:
            validator.validate(record)
            total += 1
        return total

    def run_serialization() -> int:
        total = 0
        for _, _, record, _, _ in logical_items:
            total += len(canonical_dumps(record))
        return total

    def run_sha256() -> int:
        total = 0
        for _, _, record, _, _ in logical_items:
            digest = hashlib.sha256(canonical_dumps(record).encode("utf-8")).hexdigest()
            total += len(digest)
        return total

    def run_dedup_keys() -> int:
        total = 0
        for repetition, index, record, _, _ in logical_items:
            sample_id = str(record.get("sample_id", f"sample-{index}"))
            proxy_root_case_id = f"{sample_id}-iteration-{repetition}"
            dedup_key = f"{proxy_root_case_id}|{sample_id}|{index}"
            total += len(dedup_key)
        return total

    def run_grouping() -> int:
        groups: dict[str, int] = {}
        for repetition, index, record, _, _ in logical_items:
            sample_id = str(record.get("sample_id", f"sample-{index}"))
            proxy_root_case_id = f"{sample_id}-iteration-{repetition}"
            groups[proxy_root_case_id] = groups.get(proxy_root_case_id, 0) + 1
        return len(groups)

    def run_combined_pipeline() -> int:
        total = 0
        groups: dict[str, int] = {}
        for repetition, index, record, raw, _ in logical_items:
            parsed = json.loads(raw)
            validator.validate(parsed)
            serialized = canonical_dumps(parsed)
            digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
            sample_id = str(parsed.get("sample_id", f"sample-{index}"))
            proxy_root_case_id = f"{sample_id}-iteration-{repetition}"
            dedup_key = f"{proxy_root_case_id}|{digest}"
            groups[proxy_root_case_id] = groups.get(proxy_root_case_id, 0) + 1
            total += len(dedup_key) + len(serialized)
        return total + len(groups)

    operations = {
        "json_parsing": (run_json_parsing, sample_bytes),
        "json_schema_validation": (run_schema_validation, sample_bytes),
        "deterministic_serialization": (run_serialization, serialized_bytes),
        "sha256": (run_sha256, serialized_bytes),
        "dedup_key_construction": (run_dedup_keys, sample_bytes),
        "root_case_grouping": (run_grouping, sample_bytes),
        "cpu_pipeline_combined": (run_combined_pipeline, sample_bytes),
    }

    payload: dict[str, Any] = {
        "logical_records": logical_records,
        "repetitions": repetitions,
        "warmup_rounds": warmup_rounds,
        "measured_rounds": measured_rounds,
        "operations": {},
    }

    for name, (runner, bytes_processed) in operations.items():
        warmups, measured = timing_loop(runner, warmup_rounds, measured_rounds)
        payload["operations"][name] = summarize_rounds(
            logical_records=logical_records,
            repetitions=repetitions,
            warmup_rounds=warmup_rounds,
            measured_rounds=measured_rounds,
            warmup_seconds=warmups,
            measured_seconds=measured,
            bytes_processed=bytes_processed if bytes_processed > 0 else None,
        )

    return payload


def build_gpu_results(args: argparse.Namespace) -> dict[str, Any]:
    if not args.model_path:
        return {
            "status": "NOT_EXECUTED_MODEL_NOT_PROVIDED",
            "used_for_capacity_recalculation": False,
        }

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except Exception as exc:
        raise RuntimeError("GPU execution requested but torch/transformers is unavailable") from exc

    if not torch.cuda.is_available():
        return {
            "status": "CUDA_NOT_AVAILABLE",
            "used_for_capacity_recalculation": False,
            "model_identifier": Path(args.model_path).name,
        }

    tokenizer_path = args.tokenizer_path or args.model_path
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_path,
        local_files_only=True,
        torch_dtype=torch.float16 if torch.cuda.is_available() else None,
    ).eval()

    sample_path = SAMPLE_JSONL
    records = read_jsonl_records(sample_path)
    cases = args.gpu_cases or 100
    if not 100 <= cases <= 200:
        raise ValueError("--gpu-cases must be between 100 and 200 when --model-path is provided")

    prompts = []
    for index in range(cases):
        record = records[index % len(records)]
        prompts.append(json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False))

    max_new_tokens = args.max_new_tokens or 32
    input_token_count = 0
    output_token_count = 0
    peak_allocated = 0
    peak_reserved = 0
    latencies: list[float] = []
    failures = 0
    retries = 0

    device = torch.device("cuda")
    model.to(device)

    for prompt in prompts:
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        input_token_count += int(inputs["input_ids"].numel())
        try:
            torch.cuda.reset_peak_memory_stats()
            start = time.perf_counter_ns()
            with torch.no_grad():
                output = model.generate(
                    **inputs,
                    do_sample=False,
                    max_new_tokens=max_new_tokens,
                    num_beams=1,
                    use_cache=True,
                )
            end = time.perf_counter_ns()
            latencies.append(ns_to_seconds(end - start))
            output_token_count += int(output.shape[-1] - inputs["input_ids"].shape[-1])
            peak_allocated = max(peak_allocated, int(torch.cuda.max_memory_allocated()))
            peak_reserved = max(peak_reserved, int(torch.cuda.max_memory_reserved()))
        except Exception:
            failures += 1
            retries += 1

    mean_latency = statistics.mean(latencies) if latencies else 0.0
    median_latency = statistics.median(latencies) if latencies else 0.0

    model_identifier = str(Path(args.model_path).name)
    model_hash = hashlib.sha256(
        canonical_dumps(
            {
                "model_identifier": model_identifier,
                "tokenizer_identifier": Path(tokenizer_path).name,
                "max_new_tokens": max_new_tokens,
                "gpu_cases": cases,
            }
        ).encode("utf-8")
    ).hexdigest()

    return {
        "status": "EXECUTED_LOCAL_MODEL",
        "used_for_capacity_recalculation": True,
        "model_identifier": model_identifier,
        "model_configuration_hash": model_hash,
        "cases": cases,
        "max_new_tokens": max_new_tokens,
        "mean_latency_seconds": mean_latency,
        "median_latency_seconds": median_latency,
        "p95_latency_seconds": p95(latencies),
        "input_tokens": input_token_count,
        "output_tokens": output_token_count,
        "tokens_per_second": (output_token_count / mean_latency) if mean_latency > 0 else 0.0,
        "peak_allocated_vram_bytes": peak_allocated,
        "peak_reserved_vram_bytes": peak_reserved,
        "failures": failures,
        "retries": retries,
    }


def build_interpretation(cpu_results: dict[str, Any], gpu_results: dict[str, Any]) -> dict[str, Any]:
    ops = cpu_results["operations"]
    fastest = min(ops.items(), key=lambda item: item[1]["mean_seconds"])
    slowest = max(ops.items(), key=lambda item: item[1]["mean_seconds"])
    return {
        "cpu_summary": {
            "local_proxy": True,
            "measured_operation_count": len(ops),
            "fastest_operation": fastest[0],
            "slowest_operation": slowest[0],
            "proxy_only": "This is a local proxy measurement only.",
        },
        "gpu_summary": {
            "status": gpu_results["status"],
            "used_for_capacity_recalculation": gpu_results["used_for_capacity_recalculation"],
            "boundary": "GPU execution is optional and requires an explicit local model path.",
        },
    }


def compute_artifact_sha256(payload: dict[str, Any]) -> str:
    without_hash = dict(payload)
    without_hash.pop("artifact_sha256", None)
    canonical = json.dumps(without_hash, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_markdown(payload: dict[str, Any]) -> str:
    cpu = payload["cpu_results"]["operations"]
    gpu = payload["gpu_results"]
    lines = [
        "# Local Resource Microbenchmark",
        "",
        "This artifact is a local proxy measurement only.",
        "It does not measure Deucalion or A100 performance.",
        "The on-platform M1 measurement remains mandatory.",
        "",
        "## Workload",
        "",
        f"- logical records: {payload['workload']['logical_records']}",
        f"- repetitions: {payload['workload']['repetitions']}",
        f"- warmup rounds: {payload['workload']['warmup_rounds']}",
        f"- measured rounds: {payload['workload']['measured_rounds']}",
        "- synthetic grouping key: `sample_id + \"-iteration-\" + index`",
        "- no expanded dataset is written to disk",
        "",
        "## CPU Results",
        "",
        "| Operation | Mean s | Median s | P95 s | Records/s |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name, stats in cpu.items():
        lines.append(
            f"| {name} | {stats['mean_seconds']:.6f} | {stats['median_seconds']:.6f} | "
            f"{stats['p95_seconds']:.6f} | {stats['records_per_second']:.2f} |"
        )
    lines.extend(
        [
            "",
            "## GPU Status",
            "",
            f"- status: {gpu['status']}",
            f"- used_for_capacity_recalculation: {str(gpu['used_for_capacity_recalculation']).lower()}",
            "",
            "## Boundary",
            "",
            "This benchmark is a proxy for local CPU and optional local-model GPU behavior.",
            "It does not change the planning envelopes and it does not replace the M1 on-platform measurement.",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local resource proxy microbenchmark.")
    parser.add_argument("--logical-records", type=int, required=True)
    parser.add_argument("--warmup-rounds", type=int, required=True)
    parser.add_argument("--measured-rounds", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-path")
    parser.add_argument("--tokenizer-path")
    parser.add_argument("--gpu-cases", type=int)
    parser.add_argument("--max-new-tokens", type=int)
    args = parser.parse_args(argv)

    if args.logical_records != 20000:
        raise SystemExit("--logical-records must be 20000 for this benchmark")
    if args.warmup_rounds != 5 or args.measured_rounds != 10:
        raise SystemExit("--warmup-rounds must be 5 and --measured-rounds must be 10")

    records = read_jsonl_records(SAMPLE_JSONL)
    schema = load_schema(SAMPLE_SCHEMA)
    validator = Draft202012Validator(schema)
    for record in records:
        validator.validate(record)

    environment = build_environment()
    cpu_results = build_cpu_results(
        records=records,
        schema=schema,
        logical_records=args.logical_records,
        warmup_rounds=args.warmup_rounds,
        measured_rounds=args.measured_rounds,
    )
    gpu_results = build_gpu_results(args)
    payload: dict[str, Any] = {
        "artifact_type": "local_proxy_resource_microbenchmark",
        "artifact_version": "1.0",
        "status": "LOCAL_PROXY_MEASUREMENT_NOT_DEUCALION",
        "scope_boundary": {
            "deucalion_measurement": False,
            "a100_measurement": False,
            "capacity_values_changed": False,
            "m1_on_platform_measurement_required": True,
        },
        "environment": environment,
        "workload": {
            "logical_records": args.logical_records,
            "repetitions": args.logical_records // len(records),
            "warmup_rounds": args.warmup_rounds,
            "measured_rounds": args.measured_rounds,
            "source_records": str(Path("sample20") / "sample20_public_records.jsonl"),
            "source_schema": str(Path("sample20") / "schema_public_sample20_v2.json"),
            "synthetic_grouping_key": 'sample_id + "-iteration-" + index',
            "gpu_requested": bool(args.model_path),
            "gpu_cases": args.gpu_cases if args.gpu_cases is not None else None,
            "max_new_tokens": args.max_new_tokens if args.max_new_tokens is not None else None,
        },
        "cpu_results": cpu_results,
        "gpu_results": gpu_results,
        "interpretation": {},
        "limitations": [
            "This artifact is a local proxy measurement and not a Deucalion run.",
            "This artifact does not measure A100 performance.",
            "The on-platform M1 measurement remains mandatory.",
            "The CPU workload uses in-memory repetition only and does not write an expanded dataset.",
            "GPU execution is skipped unless an explicit local model path is provided.",
        ],
        "generated_at_utc": utc_now(),
    }
    payload["interpretation"] = build_interpretation(cpu_results, gpu_results)
    payload["artifact_sha256"] = compute_artifact_sha256(payload)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md_path = args.output.with_suffix(".md")
    md_path.write_text(build_markdown(payload) + "\n", encoding="utf-8")
    print(f"WROTE_JSON={args.output}")
    print(f"WROTE_MD={md_path}")
    print(f"ARTIFACT_SHA256={payload['artifact_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
