# Changelog

Historical repository chronology notice: headings below describe repository
development notes. They do not assert that corresponding Git tags or GitHub
Releases exist. Current commands, output states and evidentiary terminology are
defined by README.md, QUICKSTART.md, PUBLIC_EVIDENCE.md and the sample20 v2
contract.

## Unreleased

- Migrated public dataset to sample20 v2 format (schema_version = 2.0).
- Replaced permissive schema with strict schema_public_sample20_v2.json (Draft 2020-12) enforcing additionalProperties: false.
- Refactored harness replay and schema validator to utilize jsonschema and the new v2 schema.
- Added scripts/verify_public_sample20_integrity.py to deterministically verify SHA-256 consistency and metrics across the dataset and spaces.
- Updated public forbidden scan script with literal patterns and recursive JSON validation post-decoding.
- Updated Hugging Face Spaces app.py to comply with v2 schema format, removing legacy/internal keys.
- Removed invented values from Hugging Face Harness Space and improved recovery logic for unrecognized prompts.

## v0.1.1-public-validation - public validation cleanup

- Strengthened the public `sample20` schema validator.
- Strengthened replay checks for required fields, types and evidence traces.
- Added public forbidden-pattern scan for local paths, credentials, private artifacts and boundary violations.
- Added README coverage for public folders.
- Added schema contract mapping for public record envelope, semantic output contract and demo validation.
- Updated public benchmark terminology from hard-block wording to human-review / non-executable preview wording.
- Updated Hugging Face harness wording to align with IFC-aware semantic contract, evidence trace and validation/replay.
- Added `.gitignore` coverage for generated harness preview models.
- Confirmed that no private datasets, checkpoints, adapters or secrets are included.
- This release does not introduce a complete corpus, trained model, production system, certification tool or final benchmark.

## v0.1-public-sample20 - public sample snapshot

- Added the public sample20 entrypoint and quickstart.
- Added replay and schema validation for the public sample20 artifact.
- Added benchmark sample20 public results and evidence-trace wording.
- Clarified the public/private boundary for public review.
- Confirmed that no private datasets, checkpoints, or adapters are included.
