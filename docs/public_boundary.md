# Public/Private Boundary

This document defines the public surface of the repository and the material
that remains private.

## Purpose

The boundary exists to keep the repository reproducible, sanitized, and narrow
enough for academic review.

## Publicly Available

| Category | Artifact | Location |
| --- | --- | --- |
| Sanitized dataset | `sample20` | `sample20/` |
| Stored-record validator | Public validation entrypoint | `harness/` |
| Benchmark sample results | Executed sample20 stored-record validation results | `benchmark/results_sample20.md` |
| Preliminary QLoRA evidence | Aggregate metrics, compute, distributions | `benchmark/qlora/` |
| Public evidence | Validation status and checks | `PUBLIC_EVIDENCE.md` |
| Methodology docs | Public validation and boundary notes | `docs/methodology/` |
| Hugging Face links | Public demo references | `README.md` |

## Not Published

| Category | Reason |
| --- | --- |
| Private pilot datasets | Not part of the public artifact |
| Private high-fidelity datasets | Not part of the public artifact |
| Fine-tuned adapter weights | Not included in the public repo |
| Raw private or live model-generation outputs | Not included in the public repo |
| Checkpoint files | Not included in the public repo |
| Private ZIP archives | Not included in the public repo |
| Production inference infrastructure | Not included in the public repo |
| Private commercial or project data | Not included in the public repo |
| Raw user feedback events | Not included in the public repo |
| Internal database schemas | Not included in the public repo |
| Local workspace paths | Not included in the public repo |

## Enforcement

The public boundary is enforced by:

1. Validation gates documented in `docs/methodology/validation_gates.md`.
2. Public pattern scans for forbidden private markers.
3. Repository hygiene rules that exclude private artifacts.

## Public Sample and Contract Note

`sample20` is the public sanitized sample dataset. Its schema is defined in
`sample20/schema_public_sample20_v2.json` as the strict public sample20 v2
contract using JSON Schema Draft 2020-12.

The public validation metrics are defined as:

- **Record Count**: 20 records;
- **Valid Cases**: 18 valid cases;
- **Expected Rejections**: 2 expected canonical rejections;
- **Canonical Validation Rate**: `canonical_validation_rate = 0.9` (since the
  2 expected negatives are successfully rejected);
- **Expectation Met Rate**: `expectation_met_rate = 1.0` (all 20 records
  match their case expectations);
- **Status**: `status = PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`.

All 1.0 metrics indicate internal agreement with the stored synthetic
reference, not a final benchmark, production deployment, or certification.

The committed `model_output` fields in sample20 are public stored fixture
fields. They are not raw private inference logs.

## Disclaimer

This is an academic research artifact.
It is not a certification tool, production BIM service, or institutional
endorsement.
It contains only public synthetic or sanitized examples.
It is not a final benchmark, not a product, and does not claim production
readiness.
