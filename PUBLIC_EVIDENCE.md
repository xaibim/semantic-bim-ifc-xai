# Public Evidence

This repository contains a public, reduced, and sanitized evidence layer for the sample20 public artifact.

## Current public status

`PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`

## Public Evidence Index

### Public executable evidence

- [Runtime-link registry](docs/evidence/public_runtime_links.json)
- [Endpoint verification snapshot](docs/evidence/public_endpoint_audit.json)

### Limited external verification

- [Kaggle QLoRA manifest](docs/evidence/kaggle_qlora_manifest.json)

### Preliminary aggregate evidence

- [Resource calibration](benchmark/resource_calibration.json)

### Local proxy evidence

- [Local resource microbenchmark](benchmark/resource_microbenchmark_local.json)

### Planning and governance

- [Resource capacity plan](docs/methodology/resource_capacity_plan.md)
- [Software and platform compatibility](docs/methodology/software_and_platform_compatibility.md)
- [Human review and operational risk](docs/methodology/human_review_and_operational_risk.md)
- [Data governance and release](docs/methodology/data_governance_and_release.md)
- [Dataset governance, split and leakage protocol](docs/methodology/dataset_governance_split_and_leakage_protocol.md)
- [Experimental scale and freeze manifest](docs/methodology/experimental_scale_and_freeze_manifest.md)

The public executable evidence files are the canonical public index for the runtime-link registry and the endpoint snapshot. The Kaggle manifest is a limited external verification note, not a recovered notebook export.
The resource calibration is preliminary aggregate evidence from the bounded QLoRA pilot. The local microbenchmark is a sanitized proxy measurement and does not replace the on-platform M1 measurement.
The planning and governance documents remain planning material only; they do not convert assumptions into measured capacity values.

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

## Scientific Positioning Boundary

This page records public executable evidence for the committed stored-record
fixture and its validation helpers.

It does not:

- evaluate universal originality;
- substitute for a systematic literature review;
- turn `sample20` into a final benchmark;
- replace the broader research-positioning boundary documents.

See [research positioning and originality boundary](docs/methodology/research_positioning_and_originality.md)
and [literature capability matrix](benchmark/literature_capability_matrix.md).

## Dataset Structure and Metrics Wording

The public `sample20` dataset contains 20 records: 18 valid cases and 2 expected canonical rejections.
- The `canonical_acceptance_rate` is 0.9 (18/20): 18 records have `canonical_check.ok = true`. This is an acceptance share, not accuracy or validation success.
- The `expectation_met_rate` is 1.0 (20/20) since the model's actual status matches the expected case expectation in all 20 records.
- All 1.0 metrics indicate consistency within this reduced sample, not general model performance or generalization.
- The `sample20` dataset is not a complete corpus and is not a final benchmark.
- No private datasets, checkpoints, adapters or secrets are included.
