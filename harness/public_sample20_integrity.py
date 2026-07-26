from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_JSONL_PATHS = [
    ROOT / "sample20" / "sample20_public_records.jsonl",
    ROOT / "spaces" / "huggingface" / "sample20_public_predictions.jsonl",
    ROOT / "spaces" / "huggingface_harness" / "sample20_public_predictions.jsonl",
]

CANONICAL_SCHEMA_PATHS = [
    ROOT / "sample20" / "schema_public_sample20_v2.json",
    ROOT / "spaces" / "huggingface" / "schema_public_sample20_v2.json",
    ROOT / "spaces" / "huggingface_harness" / "schema_public_sample20_v2.json",
]

_CANONICAL_PAIR_BINDINGS = {
    (ROOT / "sample20" / "sample20_public_records.jsonl").resolve(): {
        (ROOT / "sample20" / "schema_public_sample20_v2.json").resolve(),
    },
    (ROOT / "spaces" / "huggingface" / "sample20_public_predictions.jsonl").resolve(): {
        (ROOT / "spaces" / "huggingface" / "schema_public_sample20_v2.json").resolve(),
        (ROOT / "sample20" / "schema_public_sample20_v2.json").resolve(),
    },
    (ROOT / "spaces" / "huggingface_harness" / "sample20_public_predictions.jsonl").resolve(): {
        (ROOT / "spaces" / "huggingface_harness" / "schema_public_sample20_v2.json").resolve(),
        (ROOT / "sample20" / "schema_public_sample20_v2.json").resolve(),
    },
}

EXPECTED_JSONL_LF_NORMALIZED_SHA256 = "2c0f0c331e79924700e58e2579d35facc65d86ef76e971dbc9593641b98455aa"
EXPECTED_SCHEMA_LF_NORMALIZED_SHA256 = "de9c722f98085d7227906295531aa190755d105a0bf030d360fb26b1298ab216"

def sha256_lf_normalized(path: Path) -> str:
    data = path.read_bytes()
    normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def _paths_exist(paths: list[Path]) -> bool:
    return all(path.exists() for path in paths)


def _byte_identity(paths: list[Path]) -> bool:
    if not _paths_exist(paths):
        return False
    blobs = [path.read_bytes() for path in paths]
    return len(set(blobs)) == 1


def _group_hash(paths: list[Path]) -> str | None:
    if not _paths_exist(paths):
        return None
    if len({path.read_bytes() for path in paths}) != 1:
        return None
    return sha256_lf_normalized(paths[0])


def verify_copy_integrity(
    jsonl_paths: list[Path],
    schema_paths: list[Path],
    expected_jsonl_lf_sha256: str,
    expected_schema_lf_sha256: str,
) -> tuple[bool, list[str], dict[str, object]]:
    errors: list[str] = []
    metrics: dict[str, object] = {
        "jsonl_copy_count": len(jsonl_paths),
        "schema_copy_count": len(schema_paths),
        "jsonl_copy_byte_identity": False,
        "schema_copy_byte_identity": False,
        "jsonl_lf_normalized_sha256": None,
        "schema_lf_normalized_sha256": None,
    }

    if len(jsonl_paths) != 3:
        errors.append(f"Expected exactly 3 JSONL copies, found {len(jsonl_paths)}")
    if len(schema_paths) != 3:
        errors.append(f"Expected exactly 3 schema copies, found {len(schema_paths)}")

    if len(jsonl_paths) == 3:
        jsonl_identity = _byte_identity(jsonl_paths)
        metrics["jsonl_copy_byte_identity"] = jsonl_identity
        jsonl_hash = _group_hash(jsonl_paths)
        metrics["jsonl_lf_normalized_sha256"] = jsonl_hash
        if not _paths_exist(jsonl_paths):
            missing = [str(path) for path in jsonl_paths if not path.exists()]
            errors.extend(f"Missing JSONL copy: {path}" for path in missing)
        elif not jsonl_identity:
            errors.append("JSONL copies are not byte-identical")
        elif jsonl_hash != expected_jsonl_lf_sha256:
            errors.append(
                "JSONL LF-normalized SHA-256 mismatch: "
                f"expected {expected_jsonl_lf_sha256}, got {jsonl_hash}"
            )

    if len(schema_paths) == 3:
        schema_identity = _byte_identity(schema_paths)
        metrics["schema_copy_byte_identity"] = schema_identity
        schema_hash = _group_hash(schema_paths)
        metrics["schema_lf_normalized_sha256"] = schema_hash
        if not _paths_exist(schema_paths):
            missing = [str(path) for path in schema_paths if not path.exists()]
            errors.extend(f"Missing schema copy: {path}" for path in missing)
        elif not schema_identity:
            errors.append("Schema copies are not byte-identical")
        elif schema_hash != expected_schema_lf_sha256:
            errors.append(
                "Schema LF-normalized SHA-256 mismatch: "
                f"expected {expected_schema_lf_sha256}, got {schema_hash}"
            )

    return len(errors) == 0, errors, metrics


def verify_canonical_public_integrity() -> tuple[bool, list[str], dict[str, object]]:
    return verify_copy_integrity(
        CANONICAL_JSONL_PATHS,
        CANONICAL_SCHEMA_PATHS,
        EXPECTED_JSONL_LF_NORMALIZED_SHA256,
        EXPECTED_SCHEMA_LF_NORMALIZED_SHA256,
    )


def _within_root(path: Path) -> bool:
    try:
        path.relative_to(ROOT)
    except ValueError:
        return False
    return True


def is_canonical_public_pair(sample_file: Path, schema_file: Path) -> bool:
    if not sample_file.exists() or not schema_file.exists():
        return False

    sample_resolved = sample_file.resolve()
    schema_resolved = schema_file.resolve()

    if not _within_root(sample_resolved) or not _within_root(schema_resolved):
        return False

    allowed_schemas = _CANONICAL_PAIR_BINDINGS.get(sample_resolved)
    return allowed_schemas is not None and schema_resolved in allowed_schemas
