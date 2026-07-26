# Validation Gates Specification

This document describes the validation layers used by the public
`semantic-bim-ifc-xai` artifact. It distinguishes **public executable checks**
(Layer A), which run today against the public sample, from **private / future
dataset methodology** (Layer B), which is described as methodology and is not
presented as an executable public check in this artifact.

The contract uses the `sample20` v2 schema
(`sample20/schema_public_sample20_v2.json`, JSON Schema Draft 2020-12). The
real record fields are:

- `schema_version`
- `sample_id`
- `case_expectation`
- `expectation_met`
- `record_status`
- `input_summary`
- `model_output`
- `reference_output`
- `canonical_check`
- `agreement`
- `reference_scope`

Within `model_output`:

- `intent_class`
- `semantic_type`
- `ifc_class`
- `value_mode`
- `required_psets`
- `required_relationships`
- `missing_inputs`
- `ambiguity_flags`
- `recovery_needed`
- `recovery_type`
- `safe_next_action`
- `reason_codes`
- `evidence_trace`

---

## Layer A — Public Executable Checks

These checks run against the public sample using the public harness and CI.

1. **JSON parsing** — every record parses as syntactically valid JSON.
2. **JSON Schema Draft 2020-12** — every record conforms to the strict
   `sample20` v2 contract.
3. **Strict schema validation** — required fields, enumerations and types are
   enforced (including `value_mode` conformance and forbidden states).
4. **Value-mode conformance** — `value_mode` is one of `PREVIEW`, `PROPOSAL`,
   `GUIDED_RECOVERY` (and `EXECUTE` only when separately authorized); legacy
   blocking terminology is rejected by the forbidden scan.
5. **Canonical coherence** — `canonical_check.ok` is consistent with
   `case_expectation` and `record_status`.
6. **Expected-negative coherence** — records with
   `case_expectation = EXPECTED_CANONICAL_REJECTION` carry `record_status =
   EXPECTED_REJECTION_PASS` and a non-empty `canonical_check.errors`.
7. **Safe-next-action presence** — `model_output.safe_next_action` is always
   present and never a blocking state.
8. **Evidence-trace structure** — the required evidence fields are present and
   schema-valid. This check does not prove that the evidence label resolves to
   an external source or that every claim is source-supported.
9. **Deterministic stored-record validation** — the harness reloads committed
   records and validates schema and stored conformance. It does not rerun
   model generation or the original prompt-to-output pipeline.
10. **Three-copy integrity** — the JSONL and schema copies in `sample20/`,
    `spaces/huggingface/` and `spaces/huggingface_harness/` are byte-identical.
11. **Forbidden scan** — file-level scan rejects real credentials, internal
    paths, and internal blocking terminology.
12. **QLoRA aggregate verifier** — the deterministic verifier checks the
    published aggregate QLoRA metrics file.
13. **Replay Space self-test** — the Replay Space `--self-test` passes.
14. **Harness Space self-test** — the Harness Space `--self-test` passes.

---

## Layer B — Private / Future Dataset Methodology

These are **methodology** steps for the larger curated dataset. They are not
executable public checks in this artifact and are documented only as planned
dataset-construction controls.

- **NER sanitization** — Named Entity Recognition redaction of private project
  names, locations, paths and persons.
- **Leakage analysis** — train/test contamination detection.
- **Near-duplicate analysis** — semantic and exact-duplicate filtering.
- **Split contamination analysis** — cross-split overlap checks.
- **Canonical catalogue validation** — mapping against buildingSMART IFC
  catalogues.
- **Real IFC file validation** — checks against actual IFC models (not present
  in `sample20`).
- **Domain expert review** — professional review of candidate records.

Layer B is described for transparency. It is **not** presented as a public,
currently executable check.

---

## Dataset candidate states (neutral)

When candidate records are evaluated for dataset inclusion, the artifact uses
neutral states only:

- `PASS`
- `REQUIRES_CORRECTION`
- `EXCLUDED_FROM_TRAINING`
- `EVAL_ONLY`

There is no blocking state and no user-facing blocking response.

---

## Professional interaction states

For professional interaction, the contract uses non-blocking states:

- `PREVIEW` — read-only preview, no mutation.
- `PROPOSAL` — proposed change requiring confirmation.
- `GUIDED_RECOVERY` — recovery path with `missing_inputs` and
  `safe_next_action`.
- `EXECUTE` — only when separately authorized and appropriate.

Every interaction always includes:

- `missing_inputs`;
- `safe_next_action`;
- a non-empty `safe_next_action` field.

A professional reviewer remains responsible for any engineering decision. The
artifact never certifies or auto-approves engineering actions.

---

## Public sample validation metrics

For the `sample20` dataset, the public validation expects:

- **Record count**: 20 records;
- **Valid cases**: 18 valid cases;
- **Expected rejections**: 2 expected canonical rejections;
- **Canonical validation rate**: `canonical_validation_rate = 0.9` (the 2
  expected negatives are rejected as intended);
- **Expectation met rate**: `expectation_met_rate = 1.0` (all 20 records match
  their case expectation);
- **Status**: `PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`.

All `1.0` metrics indicate internal agreement with the stored synthetic
reference, not a final benchmark, production deployment, or certification. This
is an academic research artifact, not a final benchmark, not a product, and does
not claim production readiness or certification.

---

## Relationship to XAI

Layer A checks 5 (canonical coherence) and 8 (evidence-trace structure)
expose and structurally validate the evidence-oriented XAI requirement at the
public sample level. Records are required to expose an explicit `evidence_trace`
and a `safe_next_action`. This structural validation is the foundation of the
XAI evaluation methodology documented in `xai_evaluation_position.md`.
