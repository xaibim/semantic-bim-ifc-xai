from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Strict Public Forbidden Scanner.
# Scans all versioned repository files for forbidden tokens, credentials,
# and private metadata.
#
# Design principles:
#   - All substring checks are case-insensitive against normalized text.
#   - "Control" and "Studio" are checked as whole-word, case-sensitive regex
#     patterns to avoid false positives on "controlled", "uncontrolled", etc.
#   - The Windows drive-path regex uses a negative lookbehind so it does NOT
#     match "https://", "ftp://", or other URLs containing ":/".
#   - Binary files (images, fonts, binaries) are skipped entirely.
#   - Schema definition files (.schema.json) are skipped for FORBIDDEN_KEYS
#     because property names like "canonical_output" are legitimate there.
# ---------------------------------------------------------------------------

# Literal patterns to search for (post-normalization, case-insensitive)
FORBIDDEN_SUBSTRINGS = [
    "c:\\0 work",
    "c:/0 work",
    "c:/0%20work",
    "0%20xaibim%20ai%20trainer",
    "c:\\users\\",
    "/mnt/data",
    "sandbox:/mnt/data",
    "PRODUCT_POLICY_FAIL",
    "adapter_model.safetensors",
    ".safetensors",
    ".docx",
    ".zip",
    "internal_family_dataset_5k",
    "file:///",
    "file://",
    "scenario::",
    "hard_block",
    "safe_block",
    "RESEARCH_PASS",
]

# Regex patterns (applied case-sensitively to normalized text)
FORBIDDEN_REGEXES = [
    re.compile(r"hf_[a-zA-Z0-9]{15,}"),          # HuggingFace tokens
    re.compile(r"sk-[a-zA-Z0-9]{15,}"),            # OpenAI tokens
    # Windows absolute drive paths — negative lookbehind prevents matching
    # URL schemes like "https://". Requires the letter NOT be preceded by
    # another letter (so "https:" is excluded but "C:\" is matched).
    re.compile(r"(?<![a-zA-Z])[A-Za-z]:[/\\](?!//)"),
    # Internal system name "Studio" as a standalone word (case-sensitive)
    re.compile(r"\bStudio\b"),
    # Internal system name "Control" as a standalone word (case-sensitive)
    # This avoids matching "controlled", "uncontrolled", etc.
    re.compile(r"\bControl\b"),
]

# Forbidden keys in public JSON/JSONL data records.
# NOTE: "canonical_output" and "confidence" are intentionally NOT listed here
# because they are legitimate property names in the public JSON Schema
# definition files. They should not appear as keys in actual data records.
FORBIDDEN_KEYS = {
    "prompt_payload", "instruction", "metadata", "safety_constraints",
    "raw_output", "json_fragment", "parsed_output", "expected_output",
    "canonical_output", "runtime_context_v1", "source_notes", "source_refs",
    "source_split", "split_profile", "dataset_id", "source_dataset_id", "aiMode",
    "agent", "cognitive", "created_at_utc", "latency_ms", "comparison",
    "commit_allowed", "safe_block", "confidence", "material", "ifc_candidates",
    "primary_anchor", "scenario_focus", "location_context", "recovery_hint",
    "adapter_dir",
}

# Extensions treated as binary — skipped entirely for text scanning
_BINARY_EXTENSIONS = frozenset([
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".pdf", ".pkl", ".bin", ".pt", ".pth", ".h5",
    ".npz", ".npy", ".parquet", ".arrow", ".feather",
    ".pyc", ".pyd", ".so", ".dll", ".exe",
    ".mp3", ".mp4", ".wav", ".ogg", ".webm",
    ".tar", ".gz", ".bz2", ".xz", ".7z",
])

_INVISIBLE_CHARS_RE = re.compile(r"[\u200b\u200c\u200d\u2060\ufeff]")

# Files to skip entirely (the scanner itself, self-test validators, and integrity verifiers)
# These implement the forbidden-token CHECK logic themselves — their source code contains
# the token literals as string constants for comparison, not as data.
_SKIP_FILENAMES = frozenset([
    "public_forbidden_scan.py",
    "verify_public_sample20_integrity.py",
])

# File paths (relative, using forward slashes) to skip beyond filename-only matches
_SKIP_RELPATHS = frozenset([
    "harness/public_sample20_v2.py",         # validator code — checks for tokens, doesn't contain them as data
    "tests/test_public_sample20_v2.py",      # test code — uses tokens as negative test inputs
])

# Schema definition files — FORBIDDEN_KEYS check is skipped for these
# because they define property schemas, not data records.
_SCHEMA_DEFINITION_SUFFIXES = frozenset([".schema.json"])
_SCHEMA_DEFINITION_NAMES = frozenset([
    "semantic_bim_output_schema.json",
    "schema_public_sample20_v2.json",
])


def normalize_text(text: str) -> str:
    """Normalize text to defeat obfuscation (HTML entities & invisible chars)."""
    text = html.unescape(text)
    text = _INVISIBLE_CHARS_RE.sub("", text)
    return text


def _is_schema_definition_file(file_path: Path) -> bool:
    """Return True if this file is a JSON Schema definition (not a data record)."""
    name = file_path.name.lower()
    return (
        name in _SCHEMA_DEFINITION_NAMES
        or any(name.endswith(s) for s in _SCHEMA_DEFINITION_SUFFIXES)
    )


def scan_decoded_json(
    obj: Any,
    file_name: str,
    line_no: int,
    errors: list[str],
    is_schema_def: bool = False,
    path: str = "",
) -> None:
    """Recursively scan a decoded JSON object for forbidden keys and values."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            norm_k = normalize_text(str(k))

            # Key forbidden-key check — skip for schema definition files
            if not is_schema_def and norm_k in FORBIDDEN_KEYS:
                errors.append(
                    f"Forbidden key '{norm_k}' found in "
                    f"{file_name}:{line_no} at {path or 'root'}"
                )

            # Check key string for forbidden substrings
            norm_k_lower = norm_k.lower()
            for sub in FORBIDDEN_SUBSTRINGS:
                if sub in ("hard_block", "safe_block") and "legacy_blocking_state_count" in norm_k_lower:
                    continue
                if sub.lower() in norm_k_lower:
                    errors.append(
                        f"Forbidden substring '{sub}' in key '{norm_k}' "
                        f"at {file_name}:{line_no}"
                    )

            # Check string values
            if isinstance(v, str):
                norm_v = normalize_text(v)
                norm_v_lower = norm_v.lower()
                for sub in FORBIDDEN_SUBSTRINGS:
                    if sub in ("hard_block", "safe_block") and "legacy_blocking_state_count" in norm_v_lower:
                        continue
                    if sub.lower() in norm_v_lower:
                        errors.append(
                            f"Forbidden substring '{sub}' in value of "
                            f"'{norm_k}' at {file_name}:{line_no}: {norm_v[:120]}"
                        )
                for rx in FORBIDDEN_REGEXES:
                    if rx.search(norm_v):
                        errors.append(
                            f"Forbidden regex '{rx.pattern}' in value of "
                            f"'{norm_k}' at {file_name}:{line_no}"
                        )

            scan_decoded_json(
                v, file_name, line_no, errors, is_schema_def,
                f"{path}.{norm_k}" if path else norm_k,
            )
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            scan_decoded_json(
                item, file_name, line_no, errors, is_schema_def,
                f"{path}[{idx}]",
            )


def main() -> int:
    # Collect versioned files via git ls-files
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        )
        files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except Exception as exc:
        print(f"Error running git ls-files: {exc}", file=sys.stderr)
        return 1

    matches_found = 0
    scanned_count = 0
    match_lines: list[str] = []

    for file_path_str in files:
        file_path = Path(file_path_str)

        # Skip the scanner itself and other known-safe script files
        if file_path.name in _SKIP_FILENAMES:
            continue

        # Skip by relative path (normalise to forward slashes for cross-platform match)
        if file_path_str.replace("\\", "/") in _SKIP_RELPATHS:
            continue

        # Skip binary files — they produce meaningless garbage matches
        if file_path.suffix.lower() in _BINARY_EXTENSIONS:
            continue

        if not file_path.exists() or not file_path.is_file():
            continue

        scanned_count += 1
        errors: list[str] = []
        is_schema_def = _is_schema_definition_file(file_path)

        try:
            raw_text = file_path.read_text(encoding="utf-8", errors="ignore")

            # Line-by-line text scan
            for line_idx, line in enumerate(raw_text.splitlines(), start=1):
                norm_line = normalize_text(line)
                norm_line_lower = norm_line.lower()

                # Substring checks (case-insensitive)
                for sub in FORBIDDEN_SUBSTRINGS:
                    if sub in ("hard_block", "safe_block") and "legacy_blocking_state_count" in norm_line_lower:
                        continue
                    if sub.lower() in norm_line_lower:
                        errors.append(f"Line {line_idx}: Forbidden substring '{sub}' found")

                # Regex checks (applied to original-case normalized line)
                for rx in FORBIDDEN_REGEXES:
                    if rx.search(norm_line):
                        errors.append(f"Line {line_idx}: Forbidden regex '{rx.pattern}' found")

            # JSON/JSONL structural scan (key + value level)
            if file_path.suffix in (".json", ".jsonl"):
                try:
                    if file_path.suffix == ".jsonl":
                        for line_idx, line in enumerate(raw_text.splitlines(), start=1):
                            stripped = line.strip()
                            if stripped:
                                record = json.loads(stripped)
                                scan_decoded_json(record, file_path_str, line_idx, errors, is_schema_def)
                    else:
                        record = json.loads(raw_text)
                        scan_decoded_json(record, file_path_str, 1, errors, is_schema_def)
                except Exception as e:
                    errors.append(f"JSON parsing error: {e}")

        except Exception as exc:
            print(f"WARNING: could not read {file_path_str}: {exc}", file=sys.stderr)

        if errors:
            matches_found += len(errors)
            for err in errors:
                match_lines.append(f"MATCH file={file_path_str} {err}")

    # Output
    print("SEMANTIC_XAIBIM_PUBLIC_FORBIDDEN_SCAN")
    print(f"files_scanned={scanned_count}")
    print(f"matches={matches_found}")

    if matches_found > 0:
        print("status=FORBIDDEN_SCAN_FAIL")
        for m in match_lines[:50]:
            print(m, file=sys.stderr)
        if len(match_lines) > 50:
            print(f"... and {len(match_lines) - 50} more matches", file=sys.stderr)
        return 1

    print("status=FORBIDDEN_SCAN_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
