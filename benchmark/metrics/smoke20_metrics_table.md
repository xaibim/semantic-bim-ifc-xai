# Public sample20 v2 validation metrics

These metrics measure the consistency within the public sample20 v2 dataset. They show the agreement between stored model output and stored synthetic reference within this reduced sample. They are not representative of general model performance or generalization to unseen data.

## Replay Metrics Summary (n=20)

| Metric | Value | Description |
|--------|-------|-------------|
| Record Count | 20 | Total records in public sample |
| Unique Sample ID Count | 20 | Unique hexadecimal identifiers |
| JSON Parse Rate | 1.0 | Compliance with JSON line parsing |
| Public Schema Valid Rate | 1.0 | Compliance with Draft 2020-12 strict schema |
| Canonical Acceptance Rate (`canonical_acceptance_rate`) | 0.9 | Acceptance share with `canonical_check.ok = true` (18/20); not accuracy or validation success |
| Valid Case Count | 18 | Number of positive test cases |
| Expected Canonical Rejection Count | 2 | Number of negative test cases |
| Expectation Met Rate | 1.0 | Rate at which model meets expectations (20/20) |
| Public Value Mode Conformance Rate | 1.0 | Conformance to public value modes |
| Legacy Blocking State Count | 0 | Count of legacy blocking state tokens |
| Safe Next Action Rate | 1.0 | Rate of presence of actionable next-step guidance |
| PREVIEW Mode Count | 6 | Records utilizing PREVIEW mode in model output |
| PROPOSAL Mode Count | 5 | Records utilizing PROPOSAL mode in model output |
| GUIDED_RECOVERY Mode Count | 9 | Records utilizing GUIDED_RECOVERY mode in model output |
| EXECUTE Mode Count | 0 | Records utilizing EXECUTE mode in model output |

## Agreement Metrics

The agreement metrics describe the agreement between stored model output and stored synthetic reference within this reduced sample:

- IFC Class Agreement: 100% agreement
- Semantic Type Agreement: 100% agreement
- Intent Class Agreement: 100% agreement
- Value Mode Agreement: 100% agreement
- Dimensions Agreement: 100% agreement
- Missing Inputs Agreement: 100% agreement

## Package Status: `PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`
