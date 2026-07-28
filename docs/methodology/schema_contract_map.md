# Schema Contract Mapping

This document maps the validation layers used in the `semantic-bim-ifc-xai` repository. It explains how public records, semantic outputs, and demo helpers interact.

## Layer Overview

There are three key layers of validation and schema contracts in this repository:

1. **Public Record Envelope**: The outer structure of the serialized records in the public sample.
2. **Semantic BIM Output Contract**: The inner fields of the semantic translation contained within `canonical_output`.
3. **Illustrative Demo Validation Contract**: The validation logic embedded in the interactive Hugging Face demo.

The current schema revision aligns the public executable checks with the **Public Record Envelope** to guarantee reproducible and clean public-sample validation.

## Layer Mapping Table

| Layer | File/script | Purpose |
|---|---|---|
| Public record envelope | `sample20/schema_public_sample20_v2.json`, `harness/schema_validator.py`, `harness/replay.py` | Validates public JSONL records under the strict public sample20 v2 contract using JSON Schema Draft 2020-12 |
| Semantic output contract | `canonical_output` inside each record | Stores IFC-aware semantic output fields |
| Demo JSON validation | `spaces/huggingface_harness/app.py` | UI helper for illustrative public demo; not the full sample20 validator |
