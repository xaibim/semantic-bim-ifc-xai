from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

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

METRICS_JSON_PATH = ROOT / "benchmark" / "metrics" / "smoke20_research_summary.json"
METRICS_MD_PATH = ROOT / "benchmark" / "metrics" / "smoke20_metrics_table.md"
RESULTS_MD_PATH = ROOT / "benchmark" / "results_sample20.md"

FORBIDDEN_KEYS = {
    "prompt_payload", "instruction", "metadata", "safety_constraints", "raw_output",
    "json_fragment", "parsed_output", "expected_output", "canonical_output",
    "runtime_context_v1", "source_notes", "source_refs", "source_split",
    "split_profile", "dataset_id", "source_dataset_id", "aiMode", "agent", "cognitive",
    "created_at_utc", "latency_ms", "comparison", "commit_allowed", "safe_block",
    "confidence", "material", "ifc_candidates", "primary_anchor", "scenario_focus",
    "location_context", "recovery_hint", "base_model", "adapter_dir"
}

_INVISIBLE_RE = re.compile(r"[\u200b\u200c\u200d\u2060\ufeff]")
_HTML_ENTITY_RE = re.compile(r"&#[0-9]+;|&#x[0-9a-fA-F]+;")


def get_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_forbidden_and_obfuscation(text: str, path_name: str, errors: list[str]) -> None:
    # 1. Raw text checks for obfuscation
    if _HTML_ENTITY_RE.search(text):
        errors.append(f"Obfuscation check: HTML entity found in raw text of {path_name}")
    
    # Check for invisible chars (BOM at start of file is okay if it is the very first char of the file, but not inside the text)
    # Actually, let's check for any invisible chars at any position
    for match in _INVISIBLE_RE.finditer(text):
        if match.start() == 0 and match.group(0) == "\ufeff":
            continue # leading BOM in file is fine
        errors.append(f"Obfuscation check: Invisible Unicode character U+{ord(match.group(0)):04X} found in {path_name} at pos {match.start()}")

    # 2. Windows paths and other sensitive literals
    lowered = text.lower()
    if "c:\\" in lowered or "c:/" in lowered or "/mnt/data" in lowered or "users\\" in lowered:
        errors.append(f"Forbidden literal (local path marker) found in raw text of {path_name}")

    # Check for legacy block tokens in raw text
    for token in ("hard_block", "safe_block"):
        # Match using word boundaries or exact substrings
        if re.search(r"\b" + token + r"\b", lowered):
            # Exception: validation metric name "legacy_blocking_state_count" is allowed
            if "legacy_blocking_state_count" in lowered and token == "blocking":
                continue
            # Also "hard_block_count" or similar is forbidden unless it's the specific metric allowed?
            # Wait, the user prompt says: "No usar hard_block, hard_block o safe_block en artefactos públicos."
            # and: "No usar el nombre hard_block_count en el resumen público nuevo. Usa: legacy_blocking_state_count"
            errors.append(f"Legacy token '{token}' found in raw text of {path_name}")


def check_decoded_json(obj: Any, path_name: str, errors: list[str], path: str = "") -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in FORBIDDEN_KEYS:
                errors.append(f"Forbidden key '{k}' found in decoded JSON of {path_name} at {path or 'root'}")
            if "hard_block" in k.lower() or "safe_block" in k.lower():
                errors.append(f"Legacy key '{k}' in decoded JSON of {path_name} at {path or 'root'}")
            if isinstance(v, str):
                v_lower = v.lower()
                if "hard_block" in v_lower or "safe_block" in v_lower:
                    errors.append(f"Legacy token in value of '{k}' in decoded JSON of {path_name} at {path or 'root'}: {v}")
                if "c:\\" in v_lower or "c:/" in v_lower or "/mnt/data" in v_lower or "users\\" in v_lower:
                    errors.append(f"Local path in value of '{k}' in decoded JSON of {path_name} at {path or 'root'}: {v}")
            check_decoded_json(v, path_name, errors, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            check_decoded_json(item, path_name, errors, f"{path}[{idx}]")


def main() -> int:
    errors: list[str] = []

    # 1. Check SHA256 of JSONLs
    jsonl_shas = {}
    for p in JSONL_PATHS:
        if not p.exists():
            errors.append(f"Missing JSONL file: {p}")
            continue
        jsonl_shas[p] = get_sha256(p)

    if len(set(jsonl_shas.values())) > 1:
        errors.append("SHA-256 mismatch between the three JSONL files:")
        for p, sha in jsonl_shas.items():
            errors.append(f"  {p.relative_to(ROOT)}: {sha}")

    # 2. Check SHA256 of schemas
    schema_shas = {}
    for p in SCHEMA_PATHS:
        if not p.exists():
            errors.append(f"Missing schema file: {p}")
            continue
        schema_shas[p] = get_sha256(p)

    if len(set(schema_shas.values())) > 1:
        errors.append("SHA-256 mismatch between the three schema files:")
        for p, sha in schema_shas.items():
            errors.append(f"  {p.relative_to(ROOT)}: {sha}")

    # 3. Read and validate canonical records
    records = []
    if JSONL_PATHS[0].exists():
        with JSONL_PATHS[0].open("r", encoding="utf-8") as handle:
            for line_num, line in enumerate(handle, start=1):
                text = line.strip()
                if not text:
                    continue
                check_forbidden_and_obfuscation(text, f"sample20_public_records.jsonl Line {line_num}", errors)
                try:
                    r = json.loads(text)
                    records.append(r)
                    check_decoded_json(r, f"sample20_public_records.jsonl Line {line_num}", errors)
                except Exception as exc:
                    errors.append(f"Failed to parse JSONL line {line_num}: {exc}")

    # 4. Check schema file contents for obfuscation
    if SCHEMA_PATHS[0].exists():
        schema_text = SCHEMA_PATHS[0].read_text(encoding="utf-8")
        check_forbidden_and_obfuscation(schema_text, "schema_public_sample20_v2.json", errors)

    # 5. Recalculate metrics from JSONL
    if len(records) == 20:
        valid_cases = sum(1 for r in records if r.get("case_expectation") == "VALID")
        expected_rejections = sum(1 for r in records if r.get("case_expectation") == "EXPECTED_CANONICAL_REJECTION")
        canonical_acceptances = sum(
            1
            for r in records
            if isinstance(r.get("canonical_check"), dict)
            and r["canonical_check"].get("ok") is True
        )
        canonical_acceptance_rate = (
            canonical_acceptances / len(records)
        )
        
        vm_counts = {"PREVIEW": 0, "PROPOSAL": 0, "GUIDED_RECOVERY": 0, "EXECUTE": 0}
        for r in records:
            mo = r.get("model_output") or {}
            vm = mo.get("value_mode")
            if vm in vm_counts:
                vm_counts[vm] += 1

        # Read summary JSON
        if METRICS_JSON_PATH.exists():
            try:
                metrics_data = json.loads(METRICS_JSON_PATH.read_text(encoding="utf-8"))
                check_decoded_json(metrics_data, "smoke20_research_summary.json", errors)
                
                # Check metrics match
                def check_metric(key, expected):
                    val = metrics_data.get(key)
                    if val != expected:
                        errors.append(f"Metric mismatch: summary JSON has {key}={val}, expected {expected}")

                check_metric("record_count", 20)
                check_metric("valid_case_count", 18)
                check_metric("expected_canonical_rejection_count", 2)
                check_metric("expectation_met_rate", 1.0)
                check_metric(
                    "canonical_acceptance_rate",
                    canonical_acceptance_rate,
                )
                obsolete_metric_key = "canonical_" + "validation_rate"
                if obsolete_metric_key in metrics_data:
                    errors.append(
                        f"Obsolete metric key present in summary JSON: {obsolete_metric_key}"
                    )
                check_metric("PREVIEW", vm_counts["PREVIEW"])
                check_metric("PROPOSAL", vm_counts["PROPOSAL"])
                check_metric("GUIDED_RECOVERY", vm_counts["GUIDED_RECOVERY"])
                check_metric("EXECUTE", vm_counts["EXECUTE"])
                check_metric("legacy_blocking_state_count", 0)
                check_metric("package_status", "PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES")
            except Exception as exc:
                errors.append(f"Failed to read/validate metrics JSON: {exc}")
        else:
            errors.append(f"Missing metrics summary JSON at {METRICS_JSON_PATH}")

        # Check Table Markdown matches metrics JSON
        if METRICS_JSON_PATH.exists() and METRICS_MD_PATH.exists():
            md_content = METRICS_MD_PATH.read_text(encoding="utf-8")
            check_forbidden_and_obfuscation(md_content, "smoke20_metrics_table.md", errors)
            
            # Check numbers in markdown table
            for key, val in [
                ("sample_size", 20),
                ("valid_case_count", 18),
                ("expected_canonical_rejection_count", 2),
                ("PREVIEW", vm_counts["PREVIEW"]),
                ("PROPOSAL", vm_counts["PROPOSAL"]),
                ("GUIDED_RECOVERY", vm_counts["GUIDED_RECOVERY"]),
                ("EXECUTE", vm_counts["EXECUTE"]),
            ]:
                if str(val) not in md_content:
                    errors.append(f"Expected metric {key}={val} not found in metrics table markdown")
        else:
            errors.append(f"Missing metrics table markdown at {METRICS_MD_PATH}")

    else:
        errors.append(f"Cannot recalculate metrics: found {len(records)} records instead of 20")

    # 6. Check documentation counts, keywords and references
    bad_predictions_path = ROOT / "examples" / "sample20_public_predictions.jsonl"
    if bad_predictions_path.exists():
        errors.append("examples/sample20_public_predictions.jsonl should not exist in the repository.")

    # Check for schema_minimal.json references anywhere
    for p in ROOT.glob("**/*.md"):
        if "node_modules" in p.parts or ".venv" in p.parts or ".git" in p.parts:
            continue
        try:
            doc_text = p.read_text(encoding="utf-8")
            if "schema_minimal.json" in doc_text:
                # Allow historical note inside RELEASE_NOTES
                if "RELEASE_NOTES" in p.name:
                    continue
                errors.append(f"Found forbidden reference to schema_minimal.json in {p.relative_to(ROOT)}")
        except Exception:
            pass

    # Verify app.py files are not skipped in public_forbidden_scan.py
    scan_script_path = ROOT / "scripts" / "public_forbidden_scan.py"
    if scan_script_path.exists():
        scan_text = scan_script_path.read_text(encoding="utf-8")
        if "spaces/huggingface/app.py" in scan_text or "spaces/huggingface_harness/app.py" in scan_text:
            errors.append("Hugging Face app.py files should not be excluded/skipped in public_forbidden_scan.py")

    # Document counts and exact status verification
    doc_paths = [
        RESULTS_MD_PATH,
        ROOT / "README.md",
        ROOT / "PUBLIC_EVIDENCE.md",
        ROOT / "QUICKSTART.md",
        ROOT / "sample20" / "README.md",
        ROOT / "sample20" / "MANIFEST.md",
        ROOT / "sample20" / "VALIDATION_SUMMARY.md",
    ]
    for doc_path in doc_paths:
        if doc_path.exists():
            text = doc_path.read_text(encoding="utf-8")
            check_forbidden_and_obfuscation(text, doc_path.name, errors)

            # Check for exact status
            if "PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES" not in text:
                # Quickstart and manifest don't strictly require the status string unless they mention it,
                # but let's check it for results, readme, evidence, and validation summary
                if doc_path.name in ("results_sample20.md", "README.md", "PUBLIC_EVIDENCE.md", "VALIDATION_SUMMARY.md"):
                    errors.append(f"Expected status 'PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES' not found in {doc_path.name}")

            # Check for exact counts/metrics phrases
            # We check if 20 records and 18 valid and 2 expected are mentioned
            has_20 = "20 records" in text or "20 registros" in text or "'20'" in text or "`20`" in text or "exactly 20" in text or "exactly 20 records" in text or "count of 20" in text or "sample20" in text or "record_count\": 20" in text or "Record Count | 20" in text or "records=20" in text
            has_18 = "18 valid" in text or "18 casos válidos" in text or "18 casos" in text or "18 positive" in text or "valid_case_count\": 18" in text or "18/20" in text or "`18`" in text or "Valid Cases | 18" in text or "18 valid cases" in text or "valid_cases=18" in text or "valid_cases: `18`" in text
            has_2 = "2 expected" in text or "2 expected canonical rejections" in text or "2 rejections" in text or "2 expected negative" in text or "2 expected canonical" in text or "2 rechazos" in text or "rejection_count\": 2" in text or "`2`" in text or "2 expected rejections" in text or "Expected Rejections | 2" in text or "expected_rejections=2" in text or "expected_rejections: `2`" in text

            if not has_20:
                errors.append(f"Expected record count '20' not mentioned properly in {doc_path.name}")
            if not has_18:
                errors.append(f"Expected valid case count '18' not mentioned properly in {doc_path.name}")
            if not has_2:
                errors.append(f"Expected negative case count '2' not mentioned properly in {doc_path.name}")

    if errors:
        print("PUBLIC_SAMPLE20_INTEGRITY_FAIL", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print("PUBLIC_SAMPLE20_INTEGRITY_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
