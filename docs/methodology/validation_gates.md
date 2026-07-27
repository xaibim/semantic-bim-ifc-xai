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

## Layer A - Public Executable Checks

These checks run against the public sample using the public harness and CI.

1. **JSON parsing** - every record parses as syntactically valid JSON.
2. **Schema-only JSON Schema validation** - every record conforms to the
   strict `sample20` v2 contract.
3. **Runtime fixture-contract coherence** - model/reference equality,
   canonical class/value-mode equality, stored agreement recomputation,
   input-summary equality, recovery/value-mode coherence, evidence relation
   declared in required relationships, and expected-negative state.
4. **Deterministic stored-record validation CLI** - the harness reloads
   committed records and validates schema and stored conformance. It does not
   rerun model generation or the original prompt-to-output pipeline.
5. **Canonical three-copy byte identity and LF-normalized hashes** - the JSONL
   and schema copies in `sample20/`, `spaces/huggingface/` and
   `spaces/huggingface_harness/` are byte-identical and match the published
   LF-normalized hashes.
6. **Forbidden scan** - file-level scan rejects real credentials, internal
   paths and internal blocking terminology.
7. **Published IFC4 Pset applicability audit** - class applicability only.
   Class applicability does not prove that a Pset is mandatory for every
   professional task.
8. **Published subtype-aware IFC4 relationship schema audit** - schema
   compatibility only. Schema compatibility does not prove semantic task
   suitability, occurrence in a real IFC model or correct instantiation.
9. **QLoRA aggregate verifier** - the public verifier checks aggregate
   structure, value bounds, distribution totals and derived compute
   arithmetic. It does not rerun training, access raw predictions or
   independently recompute empirical held-out scores. It does not prove
   superiority. It does not prove generalization.
10. **Replay Space self-test** - the Replay Space `--self-test` passes.
11. **Harness Space self-test** - the Harness Space `--self-test` passes.

The evidence-trace check in Layer A is structural and internal only; external
source supportedness is not evaluated.

---

## Layer B - Private / Future Dataset Methodology

These are methodology steps for the larger curated dataset. They are not
executable public checks in this artifact and are documented only as planned
dataset-construction controls.

- **NER sanitization** - Named Entity Recognition redaction of private project
  names, locations, paths and persons.
- **Leakage analysis** - train/test contamination detection.
- **Near-duplicate analysis** - semantic and exact-duplicate filtering.
- **Split contamination analysis** - cross-split overlap checks.
- **Canonical catalogue validation** - mapping against buildingSMART IFC
  catalogues.
- **Real IFC file validation** - checks against actual IFC models (not present
  in `sample20`).
- **Domain expert review** - professional review of candidate records.

Layer B is described for transparency. It is not presented as a public,
currently executable check.

---

## Layer C - Planned Comparative Benchmark Gates

The planned comparative benchmark gates are methodology controls and not public
currently executed checks. This current public planned methodology is frozen
for future use. Every gate below is `PLANNED_NOT_EXECUTED`.

| Gate | Meaning | Evidence required |
| --- | --- | --- |
| G0 | `SCOPE_AND_MANIFEST_FROZEN` | Frozen benchmark scope and manifest snapshot. |
| G1 | `DATASET_LINEAGE_AND_RIGHTS_REVIEWED` | Dataset lineage, permissions and rights review record. |
| G2 | `ROOT_CASE_DEDUP_AND_LEAKAGE_AUDITED` | Root-case grouping, deduplication and leakage audit log. |
| G3 | `RESOLVABLE_GROUNDING_AVAILABLE` | Verified resolvable references and grounding resources. |
| G4 | `REQUIRED_BASELINES_EXECUTABLE` | Executable baseline definitions for A, B and C. |
| G5 | `METRICS_AND_STATISTICAL_PLAN_FROZEN` | Frozen metric implementation and statistical-analysis plan. |
| G6 | `PROFESSIONAL_REVIEW_PROTOCOL_READY` | Frozen professional-review protocol where professional sufficiency is claimed. |
| G7 | `COMPUTE_MEASUREMENT_READY` | Frozen compute instrumentation and resource-measurement plan. |
| G8 | `FINAL_SCORING_LOCKED` | Locked scoring manifest and immutable final-scoring rules. |

The planned gates do not authorize certification or production. A, B and C
require G0, G1, G2, G3, G4, G5 and G7 before final scoring. D and E require
those gates plus real grounding tools and verified grounding resources. F and G
remain optional. H requires the dataset-quality gates and results from A, B and
C. G6 is mandatory only for metrics that claim professional sufficiency.

Links to the planned methodology documents:

- [Planned Semantic BIM/IFC Benchmark Execution Protocol](../../benchmark/benchmark_execution_protocol.md)
- [Planned Statistical Analysis Plan](../../benchmark/statistical_analysis_plan.md)
- [Planned Dataset Governance, Split and Leakage Protocol](dataset_governance_split_and_leakage_protocol.md)

---

## Planned Baselines

The canonical identifiers, names and statuses are maintained in [Baseline
Matrix](../../benchmark/baseline_matrix.md).

| ID | Baseline | Status |
| --- | --- | --- |
| A | Deterministic IFC/schema/catalogue lookup | REQUIRED |
| B | Base LLM, prompt-only | REQUIRED |
| C | Base LLM with retrieved IFC/bSDD/IDS context | REQUIRED |
| D | Graph or ontology-grounded retrieval | CONDITIONAL |
| E | Tool-using adaptive IFC exploration | CONDITIONAL |
| F | Single-agent planner | OPTIONAL |
| G | Multi-agent workflow | OPTIONAL |
| H | QLoRA-adapted model | OPTIONAL_AFTER_GATES |

- No comparative baseline results are reported by the current public artifact.
- Conditional and optional baselines must be compared against the required
  simpler baselines when executed.
- A multi-agent workflow is not presumed superior to a single-agent planner.
- QLoRA adaptation may be executed only after dataset-quality and required
  baseline gates have passed.

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

- `PREVIEW` - read-only preview, no mutation.
- `PROPOSAL` - proposed change requiring confirmation.
- `GUIDED_RECOVERY` - recovery path with `missing_inputs` and
  `safe_next_action`.
- `EXECUTE` - only when separately authorized and appropriate.

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
reference, not a final benchmark, production deployment or certification. This
is an academic research artifact, not a final benchmark, not a product, and
does not claim production readiness or certification.

---

## Relationship to XAI

The checks named above - JSON parsing, schema-only JSON Schema validation,
runtime fixture-contract coherence, deterministic stored-record validation CLI,
canonical three-copy byte identity and LF-normalized hashes, forbidden scan,
published IFC4 Pset applicability audit, published subtype-aware IFC4
relationship schema audit, QLoRA aggregate verifier, Replay Space self-test and
Harness Space self-test - together define the public XAI boundary. The
evidence-trace structure is verified structurally; external source supportedness
is not evaluated.
