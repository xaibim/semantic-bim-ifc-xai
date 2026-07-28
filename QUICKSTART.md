# Quickstart

Minimal local validation steps for the public sample and public validation layer.

## 1. Create a virtual environment

```powershell
python -m venv .venv
```

## 2. Activate it on Windows

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install root dependencies

```powershell
pip install -r requirements.txt
```

The public validation commands require the root dependencies in `requirements.txt`. The canonical copy-integrity helper itself uses only the Python standard library.

## 4. Run deterministic stored-record validation

```powershell
python harness/replay.py --sample sample20/
```

The historical CLI filename is `replay.py`, but the command loads and validates committed records. It does not rerun model generation.

Expected output includes:

* `records=20`
* `nonempty_lines=20`
* `parsed_records=20`
* `json_parse_rate=1.000000`
* `json_parse=PASS`
* `valid_cases=18`
* `expected_rejections=2`
* `expectation_met_rate=1.000000`
* `schema_valid_rate=1.000000`
* `schema=PASS`
* `fixture_contract=PASS`
* `integrity_scope=CANONICAL_THREE_COPY`
* `jsonl_copy_count=3`
* `jsonl_copy_byte_identity=PASS`
* `jsonl_lf_normalized_sha256=2c0f0c331e79924700e58e2579d35facc65d86ef76e971dbc9593641b98455aa`
* `schema_copy_count=3`
* `schema_copy_byte_identity=PASS`
* `schema_lf_normalized_sha256=8e4de7f560ef24dac0404c45b8d62661dd52c538876e17b7ad975a254306f7f9`
* `integrity=PASS`
* `status=PUBLIC_SAMPLE20_V2_VALID`

`integrity=PASS` means that the command independently verified the three public JSONL copies and the three public schema copies. It is not derived from schema validation.

The command reports JSON parsing, schema validation, fixture-contract validation, and canonical three-copy integrity as separate checks.

## 5. Run the public schema validator

```powershell
python harness/schema_validator.py sample20/sample20_public_records.jsonl --schema sample20/schema_public_sample20_v2.json
```

Expected output includes:

* `records=20`
* `nonempty_lines=20`
* `parsed_records=20`
* `json_parse_rate=1.000000`
* `json_parse=PASS`
* `schema_valid_records=20`
* `schema_valid_rate=1.000000`
* `schema=PASS`
* `records_with_required_keys=20`
* `records_with_evidence_trace=20`
* `fixture_contract=NOT_EVALUATED`
* `integrity=NOT_CHECKED`
* `status=SCHEMA_VALIDATION_OK`

The schema validator does not evaluate the fixture contract or canonical three-copy integrity. Use `harness/replay.py` for those checks.

This is schema-only validation: it checks JSON parsing and JSON Schema compliance, then reports the fixture and integrity fields as `NOT_EVALUATED` and `NOT_CHECKED`.

## 6. Run the public forbidden-pattern scan

```powershell
python scripts/public_forbidden_scan.py
```

Expected output includes:

* `matches=0`
* `status=FORBIDDEN_SCAN_OK`

## 7. Optional: run the Hugging Face harness self-test

Install optional demo dependencies:

```powershell
pip install -r spaces/huggingface_harness/requirements.txt
```

Run:

```powershell
python spaces/huggingface_harness/app.py --self-test
```

Expected output:

* `SELF_TEST_OK`

If `pandas` or `gradio` are not installed locally, the script may print warnings. These warnings do not block the public self-test if the command ends with `SELF_TEST_OK`.

## Scope

These commands validate the public sample and public reproducibility layer. They do not run private models, private datasets, adapters, checkpoints, production BIM services or certification workflows.
