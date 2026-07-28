---
title: Semantic AI for BIM/IFC Public Harness
emoji: 🧪
colorFrom: blue
colorTo: gray
sdk: gradio
sdk_version: 5.33.0
app_file: app.py
pinned: false
license: mit
---

# Semantic AI for BIM/IFC: Guided Research Demo

**Subtitle**: Natural-language AECO/BIM request → IFC-aware semantic contract → evidence trace → validation/replay → AECO answer.

> [!WARNING]
> **Important Disclaimers**:
> - **This is not a full BIM authoring tool.**
> - **This is not a certified IFC generator.**
> - **This is a public research demo for semantic BIM/IFC interpretation.**
> - This public research demo does not generate certified IFC geometry or professional BIM deliverables. It provides a conceptual 3D preview, structured semantic metadata, LOI explanation, validation and replay over a reduced sanitized sample.

This Space is a public research validation harness loaded with 20 sanitized, hand-annotated records. It is intentionally separated from commercial XAIBIM ecosystem components. It is not an official product, certification system, university service or institutional endorsement.

---

## Tab Guide

### 1. Start here — Guided BIM/IFC preview
- **What this does**: Translates your plain text construction requests into structured BIM/IFC metadata and generates an illustrative 3D shape.
- **What to try**: Type a request like *'I need a reinforced concrete column'* or click one of the examples below.
- **What result means**: The JSON represents the auditable metadata contract (LOI), and the 3D canvas displays a conceptual geometry preview (LOD).

> The demo provides conceptual OBJ-based 3D previews for illustration, but it does not generate certified IFC geometry or full BIM authoring deliverables.

### 2. Search public cases
- **What this does**: Browse and inspect the 20 sanitized public records.
- **What to try**: Search keywords like 'column' or 'wall', select a filter in the dropdown, and select a record from the list to view.
- **What result means**: The table shows the parsed properties of matches, and selecting one loads its original full JSON record. If no results are found, suggestions are: `column, wall, beam, slab, window, IfcColumn, Pset_WindowCommon, PREVIEW`.

### 3. Find similar public sample
- **What this does**: This tab does not generate a new BIM/IFC semantic preview. It searches the reduced 20-record public sample and returns the closest existing public record.
- **What to try**: Enter a query or select an example to see what metadata would be mapped in this harness.
- **What result means**: Shows the closest matching record in JSON format for review.

### 4. Validate illustrative demo JSON
- **What this does**: Checks whether a JSON output meets the minimum research contract schema. This is a demo helper, not the full sample20 public record validator.
- **What to try**: Edit the pre-populated JSON payload and click 'Validate' to check for compliance.
- **What result means**: This validates the minimum research contract, not a BIM certification.

### 5. Run public harness
- **What this does**: Runs a reproducible validation across all 20 public records.
- **What to try**: Click the 'Run validation' button to verify all records.
- **What result means**: Outputs `SCHEMA_VALIDATION_OK` and `REPLAY_OK` for exactly 20 records if the dataset is intact.

---

## Usage Examples

To test the **Start here** and **Find similar public sample** tabs, you can use any of the following predefined prompts:

1. *"I need a reinforced concrete column with IFC classification and LOI information."*
2. *"Classify a partition wall and suggest IFC semantic information."*
3. *"Validate whether a window request can map to Pset_WindowCommon."*
4. *"Explain what information is missing to classify this BIM element."*
5. *"What is the difference between LOD and LOI for a BIM object?"*

---

## Scope Limitations

- **No certified IFC geometry generation**: The demo provides conceptual OBJ-based 3D previews for illustration, but it does not generate certified IFC geometry or full BIM authoring deliverables.
- **No live model inference**: matching is deterministic and resolved against the static 20-record database.
- **No certified BIM decisions**: all outputs are labelled `PREVIEW` and must be audited by qualified engineers before any model insertion.
- **No professional validation**: outputs are research previews only.
- **No final benchmark or production deployment**: this is a research prototype only, not a product.

---

## Public Sample and Demo Note

The interactive application in this folder conforms to the strict public sample20 v2 contract using JSON Schema Draft 2020-12 (defined in `schema_public_sample20_v2.json`).

Expected metrics are:
- **Record Count**: 20 records;
- **Valid Cases**: 18 valid cases;
- **Expected Rejections**: 2 expected canonical rejections;
- **Canonical Acceptance Rate**: `canonical_acceptance_rate = 0.9` (18/20 records have `canonical_check.ok = true`; acceptance share, not accuracy);
- **Expectation Met Rate**: `expectation_met_rate = 1.0`;
- **Status**: `status = PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`.

All 1.0 metrics indicate internal agreement with the stored synthetic reference, not a final benchmark, production deployment, or certification. This is an academic research artifact, not a final benchmark, not a product, and does not claim production readiness or certification.

---

The long-term goal is not to replace engineers, but to study how AI systems can make BIM/IFC interpretation more explicit, auditable and explainable.
