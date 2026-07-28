# sample20 Validation Summary

Status: `PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`

## Public Executable Checks

| Check | Public executable? | Command/path | Status | Notes |
| --- | --- | --- | --- | --- |
| Schema-only JSON parsing and JSON Schema validation | yes | `python harness/schema_validator.py sample20/sample20_public_records.jsonl --schema sample20/schema_public_sample20_v2.json` | PASS | 20/20 records parsed and schema-valid. `fixture_contract=NOT_EVALUATED`; `integrity=NOT_CHECKED`. |
| JSON parsing | yes | `python harness/replay.py --sample sample20/` | PASS | 20/20 nonempty lines parsed |
| Strict schema validation | yes | `python harness/replay.py --sample sample20/` | PASS | 20/20 parsed records schema-valid |
| Fixture-contract validation | yes | `python harness/replay.py --sample sample20/` | PASS | Counts, expected negatives and stored coherence valid |
| Canonical three-copy integrity | yes | `python harness/replay.py --sample sample20/` | PASS | Three JSONL and three schema copies verified independently |
| Evidence-trace structure count | yes | `python harness/schema_validator.py sample20/sample20_public_records.jsonl` | PASS | Counted from model and reference evidence_trace objects. This does not verify external source supportedness. |
| Forbidden pattern scan | yes | `python scripts/public_forbidden_scan.py` | PASS | Scans tracked files for forbidden patterns and credentials |
| Leakage/dedupe | no | `not exposed as public executable check` | METHODOLOGICAL | Handled as a methodology-only process |
| NER sanitization | no | `not exposed as public executable check` | METHODOLOGICAL | Handled as a methodology-only process |

## Notes

- `sample20` is the public sanitized sample dataset.
- `smoke20` is the deterministic stored-record validation run executed on `sample20`.
- The public sample contains 20 records: 18 valid positive cases and 2 expected canonical rejections.
- Expected metrics are: `canonical_acceptance_rate = 0.9` (18/20 records have `canonical_check.ok = true`; acceptance share, not accuracy or validation success) and `expectation_met_rate = 1.0` (20/20 declared outcomes are met).
- This summary reports public evidence only.
