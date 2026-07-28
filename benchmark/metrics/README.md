# benchmark/metrics

## Purpose
This folder holds metrics tables and summaries generated during public sample reproducibility runs.

## Contents
- `smoke20_metrics_table.md`: A markdown table representing consistent validation metrics over the public sample20.
- `smoke20_research_summary.json`: Machine-readable version of the public smoke validation summary.

## What this folder does not contain
- It does not contain final benchmark datasets or results.
- It does not contain general model performance metrics or leaderboard evaluations.
- It does not claim production readiness or final certification.

## Related files
- `benchmark/README.md`: Explains the benchmark purpose.
- `benchmark/results_sample20.md`: Summarizes results of public tests.

---

## Public Sample Validation Metrics Wording

The public reproducibility run on the `sample20` dataset conforms to the strict public sample20 v2 contract using JSON Schema Draft 2020-12 (defined in `sample20/schema_public_sample20_v2.json`).

Expected metrics are:
- **Record Count**: 20 records;
- **Valid Cases**: 18 valid cases;
- **Expected Rejections**: 2 expected canonical rejections;
- **Canonical Acceptance Rate**: `canonical_acceptance_rate = 0.9` (18/20 records have `canonical_check.ok = true`; acceptance share, not accuracy);
- **Expectation Met Rate**: `expectation_met_rate = 1.0`;
- **Status**: `status = PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`.

All 1.0 metrics indicate internal agreement with the stored synthetic reference, not a final benchmark, production deployment, or certification. This is an academic research artifact, not a final benchmark, not a product, and does not claim production readiness or certification.
