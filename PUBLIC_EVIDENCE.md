# Public Evidence

This repository contains a public, reduced, and sanitized evidence layer for the sample20 public artifact.

## Current public status

`PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`

## Public Executable Checks

| Check | Public executable? | Command/path | Status | Notes |
| --- | --- | --- | --- | --- |
| JSON parse | yes | `python harness/schema_validator.py sample20/sample20_public_records.jsonl` | PASS | 20 records successfully parsed |
| Strict public sample20 v2 contract validation (JSON Schema Draft 2020-12) | yes | `python harness/schema_validator.py sample20/sample20_public_records.jsonl --schema sample20/schema_public_sample20_v2.json` | PASS | Schema-only validation; fixture coherence and canonical integrity are reported separately by the stored-record validation command. Reports `fixture_contract=NOT_EVALUATED` and `integrity=NOT_CHECKED` |
| JSON parsing | yes | `python harness/replay.py --sample sample20/` | PASS | 20/20 nonempty lines parsed |
| Strict schema validation | yes | `python harness/replay.py --sample sample20/` | PASS | 20/20 parsed records schema-valid |
| Fixture-contract validation | yes | `python harness/replay.py --sample sample20/` | PASS | Counts, expected negatives and stored coherence valid |
| Canonical three-copy integrity | yes | `python harness/replay.py --sample sample20/` | PASS | Three JSONL and three schema copies verified independently |
| Evidence trace presence | yes | `python harness/schema_validator.py sample20/sample20_public_records.jsonl` | PASS | Counted directly from both model and reference evidence_trace structures |
| Forbidden pattern scan | yes | `python scripts/public_forbidden_scan.py` | PASS | Scans tracked files for forbidden patterns and credentials |
| Leakage/dedupe | no | `not exposed as public executable check` | METHODOLOGICAL | Handled as a methodology-only process |
| NER sanitization | no | `not exposed as public executable check` | METHODOLOGICAL | Handled as a methodology-only process |

## Evidence Included

- Public sample20 records.
- Public deterministic stored-record validation.
- Public sample validation summary.
- Replay harness.
- Schema validator helper.
- Public forbidden scan utility script.

## Evidence Interpretation

The current evidence shows that a public sanitized sample can be loaded and validated from committed records with auditable outputs under a controlled research setting.

The evidence does not claim:

- Product readiness.
- Normative certification.
- Deployment approval.
- Exhaustive benchmark coverage.

## Dataset Structure and Metrics Wording

The public `sample20` dataset contains 20 records: 18 valid cases and 2 expected canonical rejections.
- The `canonical_validation_rate` is 0.9 (18/20) because the two expected negative cases are rejected as intended.
- The `expectation_met_rate` is 1.0 (20/20) since the model's actual status matches the expected case expectation in all 20 records.
- All 1.0 metrics indicate consistency within this reduced sample, not general model performance or generalization.
- The `sample20` dataset is not a complete corpus and is not a final benchmark.
- No private datasets, checkpoints, adapters or secrets are included.

