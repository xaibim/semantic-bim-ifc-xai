# Dataset scope and compute scaling

## Public sample (`sample20`)

`sample20` is a minimal, sanitized, synthetic reproducibility sample. All
distributions below are computed directly from
[`sample20/sample20_public_records.jsonl`](../../sample20/sample20_public_records.jsonl)
using the public test suite. They are descriptive of this sample only.

### What `sample20` contains

- **20 records** in total.
- **18 valid cases** (`case_expectation = VALID`, `record_status = PASS`).
- **2 expected negatives** (`case_expectation = EXPECTED_CANONICAL_REJECTION`,
  `record_status = EXPECTED_REJECTION_PASS`).
- `canonical_validation_rate = 0.9` (18/20).
- `expectation_met_rate = 1.0` (20/20).

### Discipline distribution (20 records)

| Discipline | Count |
| --- | --- |
| structural_elements | 7 |
| mechanical | 5 |
| architecture | 3 |
| facility_management | 3 |
| construction_management | 2 |

### IFC class distribution (20 records)

| IFC class | Count |
| --- | --- |
| IfcColumn | 5 |
| IfcSpace | 3 |
| IfcBeam | 2 |
| IfcFlowTerminal | 2 |
| IfcAsset | 2 |
| IfcWall | 1 |
| IfcPump | 1 |
| IfcAirTerminal | 1 |
| IfcFan | 1 |
| IfcSystem | 1 |
| IfcZone | 1 |

These are IFC entity labels used by the contract. Their presence does **not**
demonstrate full IFC2x3 or IFC4 coverage.

### Semantic type distribution (20 records)

| Semantic type | Count |
| --- | --- |
| element_deletion | 4 |
| ambiguity_resolution | 3 |
| evidence_generation | 3 |
| semantic_enrichment | 2 |
| element_modification | 2 |
| recovery_request | 2 |
| geometric_validation | 1 |
| relationship_inference | 1 |
| pset_assignment | 1 |
| material_assignment | 1 |

### `value_mode` distribution (20 records)

| value_mode | Count |
| --- | --- |
| GUIDED_RECOVERY | 9 |
| PREVIEW | 6 |
| PROPOSAL | 5 |

### `recovery_needed` distribution (20 records)

| recovery_needed | Count |
| --- | --- |
| false | 11 |
| true | 9 |

### Ambiguity flag counts (across records)

| Ambiguity flag | Count |
| --- | --- |
| discipline_mismatch | 3 |
| ambiguous_ifc_class | 2 |
| surface_handoff_missing | 2 |
| lod_loi_conflict | 2 |
| pset_missing | 2 |
| insufficient_context | 2 |
| duplicate_identity_risk | 2 |
| missing_dimensions | 1 |
| relation_missing | 1 |
| unsafe_delete | 1 |
| runtime_context_partial | 1 |
| missing_material | 1 |

### Missing-input counts (across records)

| Missing input | Count |
| --- | --- |
| discipline | 3 |
| ifc_classes | 2 |
| surface_handoff_package | 2 |
| lod | 2 |
| loi | 2 |
| required_psets | 2 |
| context.phase | 2 |
| context.bimUse | 2 |
| identity_resolution_key | 2 |
| normalized_dimensions_m | 1 |
| required_relationships | 1 |
| safe_mutation_approval | 1 |
| runtime_context_v1 | 1 |
| material | 1 |

---

## What `sample20` does NOT contain or demonstrate

- `sample20` is **minimal**.
- `sample20` is **synthetic / sanitized**.
- `sample20` contains **no real IFC files**.
- The use of IFC entity names does **not** prove IFC2x3 or IFC4 coverage.
- There is **no public evidence** of building-typology generalization.
- The public sample does **not** demonstrate multilingual coverage.
- The original private prompts are **not published**.
- `sample20` is **not** a final benchmark.
- `sample20` does **not** demonstrate superiority of any model.
- The preliminary QLoRA pilot is **private, synthetic/controlled and limited**.

---

## Private controlled pilot dataset

A private controlled synthetic pilot dataset of 1,000 records was used in a
preliminary QLoRA feasibility experiment.

The dataset is **not publicly released**. Only aggregate metrics, hashes, and
compute measurements derived from it are published in
[`benchmark/qlora/`](../../benchmark/qlora/).

The pilot dataset was used to:

- validate the dataset preparation and split construction pipeline;
- calibrate GPU resource consumption;
- measure controlled held-out target agreement;
- confirm the training workflow is executable end-to-end.

---

## Preliminary QLoRA experiment

A preliminary QLoRA fine-tuning experiment was executed on Kaggle
GPU infrastructure using the private pilot dataset.

Public notebook: <https://www.kaggle.com/code/xaibim/semantic-bim-ifc-xai>

The experiment measured:

- training runtime and end-to-end runtime;
- peak VRAM consumption;
- effective and allocated GPU-hours;
- controlled held-out target agreement before and after fine-tuning.

The result is **preliminary and bounded**:

- single run, single seed, one epoch;
- seven held-out semantic families;
- four IFC classes in the test split;
- no broad AECO generalization established;
- no production readiness claimed.

---

## Compute scaling

The pilot used 1,000 records and one epoch on a single Tesla T4.

Effective GPU-hours measured: ≈ 2.11 h (1 effective GPU).
Allocated GPU-hours measured: ≈ 4.22 h (2 allocated GPUs).

These figures are calibration data points for future resource planning.
They are not universal efficiency guarantees.

---

## Experimental order

The work proceeds in this order:

1. define the semantic BIM/IFC contract;
2. generate and curate the synthetic/controlled dataset;
3. validate schema, leakage, deduplication and coverage;
4. execute baseline model evaluations;
5. analyse errors;
6. optionally execute a bounded LoRA/QLoRA adaptation only after dataset
   quality and baseline evaluation gates are satisfied;
7. compare adapted and non-adapted results only if step 6 is executed.

Successful completion of the planned dataset and benchmark work does not depend
on executing the optional adaptation step.

---

## Planned scope to be frozen before benchmark execution

The following dimensions are **to be confirmed in the experimental protocol**
and are **not** asserted by the current public artifact:

- IFC2x3 versus IFC4 coverage;
- disciplines included;
- languages included;
- semantic families included;
- IFC classes included;
- building typologies included;
- sizes per train/validation/test/eval split;
- number of random seeds;
- baseline model set.

---

## Boundary

A systematic benchmark at larger scale and a broader public dataset remain
future work. The public sample and preliminary internal experiments are
starting evidence for a controlled research workflow, not a replacement for
broader scientific validation.
