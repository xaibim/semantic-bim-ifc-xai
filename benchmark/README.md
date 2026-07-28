# Benchmark

The benchmark folder contains reduced public sample validation artefacts.

Current contents:

- `results_sample20.md`
- `metrics/smoke20_metrics_table.md`
- `metrics/smoke20_research_summary.json`
- `schema/semantic_bim_output_schema.json`

`smoke20` is the validation run over `sample20` under the strict public sample20 v2 contract using JSON Schema Draft 2020-12 (defined in `sample20/schema_public_sample20_v2.json`). It is not a separate dataset.

The public validation expects:
- **Record Count**: 20 records;
- **Valid Cases**: 18 valid cases;
- **Expected Rejections**: 2 expected canonical rejections;
- **Canonical Acceptance Rate**: `canonical_acceptance_rate = 0.9` (18/20 records have `canonical_check.ok = true`; acceptance share, not accuracy);
- **Expectation Met Rate**: `expectation_met_rate = 1.0`;
- **Status**: `status = PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`.

All 1.0 metrics indicate internal agreement with the stored synthetic reference, not a final benchmark, production deployment, or certification. This is an academic research artifact, not a final benchmark, not a product, and does not claim production readiness or certification.
