# Release Notes: v0.1.1-public-validation

## Summary

> [!NOTE]
> This historical note is superseded by the public Evidence-Trace naming and does not by itself prove a Git tag or GitHub Release.
>
> The initial `schema_minimal.json` (minimal public contract) and validation rules referenced in this historical release have been replaced by the `strict public sample20 v2 contract using JSON Schema Draft 2020-12` (`sample20/schema_public_sample20_v2.json`).

This release updates the public reproducibility package after `v0.1-public-sample20`.

It strengthens the public validation layer and improves repository navigability. It does not introduce a new dataset, trained model, private adapter, production service or final benchmark.

## Public Artifacts Updated or Added

- `harness/replay.py`
- `harness/schema_validator.py`
- `scripts/public_forbidden_scan.py`
- `scripts/README.md`
- `.github/workflows/public-sample20.yml`
- `PUBLIC_EVIDENCE.md`
- `sample20/VALIDATION_SUMMARY.md`
- `benchmark/metrics/smoke20_metrics_table.md`
- `benchmark/metrics/smoke20_research_summary.json`
- `docs/methodology/schema_contract_map.md`
- README files for public folders
- `.gitignore`

## Validation Commands

```powershell
python harness/replay.py --sample sample20/
python harness/schema_validator.py sample20/sample20_public_records.jsonl
python scripts/public_forbidden_scan.py
python spaces/huggingface_harness/app.py --self-test
```

## Expected Outputs

* Historical output tokens retained for compatibility:
* `status=REPLAY_OK`
* `status=SCHEMA_VALIDATION_OK`
* `status=FORBIDDEN_SCAN_OK`
* `SELF_TEST_OK`

## What Changed Since v0.1-public-sample20

* The public schema validator now checks required keys, types, `ok`, `validation.ok`, `sample_id`, `parsed_output`, `expected_output` and `canonical_output.evidence_trace`.
* The replay harness now performs stricter public contract checks before reporting `REPLAY_OK`.
* A public forbidden-pattern scan was added for local paths, credentials, private artifacts and public-boundary violations.
* Public documentation was expanded with folder README files and a schema contract map.
* Public benchmark terminology was cleaned to avoid user-facing hard-block wording.
* The Hugging Face harness wording was aligned with the IFC-aware semantic contract and validation/replay framing.

## Scope and Limitations

* `sample20` remains a minimal public reproducibility sample of 20 records.
* This release does not include a complete corpus.
* This release does not include model training.
* This release does not publish private datasets, model weights, adapters, checkpoints, credentials or internal logs.
* This release does not claim certification, production readiness or final benchmark results.
* The public explainability claim remains evidence-trace auditability over stored records, not full mathematical attribution, external-source supportedness, or certification.

## Relation to v0.1-public-sample20

`v0.1-public-sample20` introduced the first public sample snapshot.

`v0.1.1-public-validation` tightens the public validation and documentation layer around that sample. A `PASS` under v0.1.1 is stricter than a `PASS` under v0.1 because the public validators now check more fields and the presence of evidence traces.
