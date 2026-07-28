---
title: Semantic XAIBIM Replay
emoji: 🏗️
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: false
short_description: Public stored-record validation demo for Semantic BIM/IFC structured outputs
tags:
  - bim
  - ifc
  - semantic-bim
  - explainable-ai
  - gradio
---

# Semantic XAIBIM Replay

This Space is a lightweight public stored-record validation demo for Semantic XAIBIM, validating records against the strict public sample20 v2 contract using JSON Schema Draft 2020-12 (defined in `schema_public_sample20_v2.json`).

`Replay` is the historical product name. This Space loads and validates
committed records; it does not rerun the original model or prompt pipeline.

It does not run a model.

It loads a reduced public JSONL sample and displays:

- Public record index.
- `input_summary`.
- Stored `model_output` and `reference_output`.
- `canonical_check`.
- Stored field-level `agreement`.
- Validation information.
- Public validation status and aggregate fixture metrics.

PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES

Expected validation metrics:
- **Record Count**: 20 records;
- **Valid Cases**: 18 valid cases;
- **Expected Rejections**: 2 expected canonical rejections;
- **Canonical Acceptance Rate**: `canonical_acceptance_rate = 0.9` (18/20 records have `canonical_check.ok = true`; acceptance share, not accuracy);
- **Expectation Met Rate**: `expectation_met_rate = 1.0`;
- **Status**: `status = PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`.

All 1.0 metrics indicate internal agreement with the stored synthetic reference, not a final benchmark, production deployment, or certification. This is an academic research artifact, not a final benchmark, not a product, and does not claim production readiness or certification.

## Source repository

https://github.com/xaibim/semantic-bim-ifc-xai
