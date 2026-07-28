# spaces

## Purpose
This directory contains folders for Hugging Face Spaces mirrors and interactive web demos of the semantic compilation harness.

## Contents
- `huggingface/`: Source code for the simple interactive public sample replay application.
- `huggingface_harness/`: Source code for the detailed model-preview and JSON-validation public harness demo.

## What this folder does not contain
- It does not contain private datasets or model server weights.
- It does not contain production-ready web servers or official CAD integrations.

## Related files
- `harness/README.md`: The backend validation scripts documentation.

---

## Public Sample and Demo Note

The interactive applications in this folder conform to the strict public sample20 v2 contract using JSON Schema Draft 2020-12 (defined in `sample20/schema_public_sample20_v2.json`).

Expected metrics are:
- **Record Count**: 20 records;
- **Valid Cases**: 18 valid cases;
- **Expected Rejections**: 2 expected canonical rejections;
- **Canonical Acceptance Rate**: `canonical_acceptance_rate = 0.9` (18/20 records have `canonical_check.ok = true`; acceptance share, not accuracy);
- **Expectation Met Rate**: `expectation_met_rate = 1.0`;
- **Status**: `status = PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`.

All 1.0 metrics indicate internal agreement with the stored synthetic reference, not a final benchmark, production deployment, or certification. This is an academic research artifact, not a final benchmark, not a product, and does not claim production readiness or certification.
