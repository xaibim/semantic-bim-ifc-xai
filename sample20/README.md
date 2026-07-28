# sample20

`sample20` is the public sanitized frozen fixture. `smoke20` is a historical
label for deterministic stored-record validation over that fixture; it is not a
separate dataset.

## What It Is

- A small public fixture for academic review.
- A sanitized set of committed structured records.
- The canonical public stored input for `harness/replay.py`.

## What It Is Not

- It is not a private pilot dataset.
- It is not a training corpus for private adapters.
- It is not a certification dataset.
- It is not a separate `smoke20` dataset.

## How To Validate

1. Read `sample20/MANIFEST.md`.
2. Run `python harness/replay.py --sample sample20/`.
3. Review `PUBLIC_EVIDENCE.md` and `benchmark/results_sample20.md`.

## Limits

- The sample is intentionally small.
- It does not claim full XAI.
- It does not include private data or private weights.
- It is a public evidence surface, not a production BIM service.

See [../QUICKSTART.md](../QUICKSTART.md) for the minimal local run.

## Public Sample Validation Metrics

The `sample20` dataset is governed by the strict public sample20 v2 contract using JSON Schema Draft 2020-12 (defined in `schema_public_sample20_v2.json`). Set-like string arrays in the strict contract reject duplicate items through `uniqueItems: true`.

Expected metrics are:
- **Record Count**: 20 records;
- **Valid Cases**: 18 valid cases;
- **Expected Rejections**: 2 expected canonical rejections;
- **Canonical Acceptance Rate**: `canonical_acceptance_rate = 0.9` (18/20 records have `canonical_check.ok = true`; acceptance share, not accuracy);
- **Expectation Met Rate**: `expectation_met_rate = 1.0`;
- **Status**: `status = PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`.

All 1.0 metrics indicate internal agreement with the stored synthetic
reference, not a final benchmark, production deployment, or certification. This
is an academic research artifact, not a final benchmark, not a product, and
does not claim production readiness or certification.
