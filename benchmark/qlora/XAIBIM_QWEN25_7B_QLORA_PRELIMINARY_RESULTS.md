# Preliminary QLoRA Computational Feasibility Run

## Scope

This document describes a **preliminary computational feasibility and resource
calibration experiment** for QLoRA fine-tuning of Qwen2.5-7B-Instruct on the
structured, evidence-trace Semantic BIM/IFC output task.

It is:

- a preliminary computational feasibility experiment;
- a resource calibration measurement on commodity GPU infrastructure;
- a controlled held-out target agreement measurement;
- a demonstration that the training workflow can be executed end-to-end.

It is **not**:

- a final benchmark;
- a claim of broad AECO generalization;
- a production-readiness assessment;
- a certification of BIM/IFC compliance.

---

## Public Kaggle Notebook

The training experiment was executed on Kaggle.

**Kaggle:** <https://www.kaggle.com/code/xaibim/semantic-bim-ifc-xai>

---

## Experimental Configuration

| Item | Value |
|---|---|
| Base model | `unsloth/Qwen2.5-7B-Instruct-bnb-4bit` |
| Method | QLoRA |
| Dataset | Private controlled synthetic pilot dataset |
| Total records | 1,000 |
| Train records | 800 |
| Validation records | 100 |
| Test records | 100 |
| Train semantic families | 84 |
| Validation semantic families | 9 |
| Test semantic families | 7 |
| Epochs | 1 |
| Seed | 3407 |
| LoRA rank | 16 |
| LoRA alpha | 16 |
| LoRA dropout | 0 |
| Learning rate | 2e-4 |
| Effective batch size | 4 |
| Allocated GPUs | 2 × Tesla T4 |
| Effective GPUs (training) | 1 × Tesla T4 |
| Legacy-normalized records | 113 |
| Dataset SHA-256 | `16c9b8b03a6dc897557183ac1457dfb00c9c4b36183a813d26f21b477de3fd12` |
| Adapter SHA-256 | `682a9dc9fc1719f8cff9bcc113eecac7f2b6aba9336f79838f0d0e6168c52392` |
| Adapter size | 161,533,192 bytes |
| Adapter publicly released | No |

---

## Compute Measurements

| Measurement | Value |
|---|---:|
| Training runtime | 3890.2480099201202 s |
| End-to-end runtime | 7598.515273094177 s |
| Peak allocated VRAM | 6.628742218017578 GB |
| Peak reserved VRAM | 7.490234375 GB |
| Training samples/s | 0.206 |
| Training steps/s | 0.051 |
| Training loss | 0.07460793347796425 |
| Validation loss | not recorded |
| Effective GPU-hours | 2.1106986869706046 |
| Allocated GPU-hours | 4.221397373941209 |

---

## Derived Calculations

All values below are deterministically derived from the raw measurements above.
The [verify_qlora_public_metrics.py](../../scripts/verify_qlora_public_metrics.py)
script recomputes and checks them without external dependencies.

| Calculation | Formula | Substitution | Result |
|---|---|---|---:|
| Training runtime (hours) | `training_s / 3600` | `3890.2480099201202 / 3600` | 1.0806244472000335 h |
| End-to-end runtime (hours) | `e2e_s / 3600` | `7598.515273094177 / 3600` | 2.1106986869706046 h |
| Non-training overhead (s) | `e2e_s − training_s` | `7598.515273094177 − 3890.2480099201202` | 3708.267263174057 s |
| Non-training overhead (hours) | `overhead_s / 3600` | `3708.267263174057 / 3600` | 1.0300742397705713 h |
| Effective GPU-hours (recomputed) | `e2e_h × 1 GPU` | `2.1106986869706046 × 1` | 2.1106986869706046 GPU-h |
| Allocated GPU-hours (recomputed) | `e2e_h × 2 GPUs` | `2.1106986869706046 × 2` | 4.221397373941209 GPU-h |
| Expected optimizer steps | `800 / 4 × 1 epoch` | `800 / 4 × 1` | 200 (derived expected count) |
| Adapter size (MiB) | `bytes / 1,048,576` | `161,533,192 / 1,048,576` | 154.05005645751953 MiB |
| Training runtime share | `training_s / e2e_s × 100` | `3890.248… / 7598.515… × 100` | 51.20% |
| Non-training runtime share | `overhead_s / e2e_s × 100` | `3708.267… / 7598.515… × 100` | 48.80% |

> Monetary costs are not estimated. GPU-hour costs vary by provider and are
> not universally applicable.

---

## Corrected Held-Out Target Agreement

The original evaluator treated `evidence_trace` as a list. The dataset
contract uses an object. The reevaluation corrected the evaluator using the
stored predictions. No retraining was required.

These `evidence_trace` metrics measure agreement against stored structured
targets in the public evaluator. They do not measure external-source
supportedness, citation truth, or source-based certification.

| Metric | Base model | QLoRA adapter |
|---|---:|---:|
| JSON parse rate | 100.0% | 100.0% |
| Strict schema-valid rate | 0.0% | 100.0% |
| Intent-class agreement † | 0.0% | 100.0% |
| Semantic-type agreement | 8.0% | 100.0% |
| IFC-class agreement | 40.0% | 100.0% |
| Value-mode agreement | 67.0% | 100.0% |
| Recovery-needed agreement | 2.0% | 100.0% |
| Missing-information F1 | 0.000 | 1.000 |
| Required-Pset F1 | 0.7467 | 0.7868 |
| Required-relationship F1 | 0.000 | 0.760 |
| Ambiguity-flags F1 | 0.760 | 1.000 |
| Reason-codes F1 | 0.000 | 1.000 |
| Evidence-trace exact match | 0.0% | 86.0% |
| Evidence-trace field F1 | 0.000 | 0.980 |

**† Intent-class agreement is not representative.** All 100 test records use
the same intent label (`unknown_edge`), so this metric does not reflect
discriminative classification ability.

---

## Test Distribution

### Intent class

| Label | Count |
|---|---:|
| unknown_edge | 100 |

### Semantic type

| Label | Count |
|---|---:|
| element_creation | 1 |
| element_deletion | 2 |
| normative_inspection | 38 |
| property_completion | 8 |
| pset_assignment | 8 |
| safe_preview | 25 |
| semantic_enrichment | 18 |

### IFC class

| Label | Count |
|---|---:|
| IfcAirTerminal | 38 |
| IfcAsset | 17 |
| IfcDuctSegment | 25 |
| IfcSpace | 20 |

### Value mode

| Label | Count |
|---|---:|
| GUIDED_RECOVERY | 2 |
| PREVIEW | 81 |
| PROPOSAL | 17 |

---

## Interpretation

The adapter demonstrated:

- **strong controlled held-out target agreement** across the 100-record test
  split;
- **computational feasibility** on Kaggle GPU infrastructure;
- **evidence-trace evaluator correction** against stored targets without
  retraining.

This result does **not** establish:

- broad AECO generalization;
- statistical significance;
- production readiness.

---

## Limitations

- Single run, single random seed.
- One model size (7B parameters), one training epoch.
- Seven held-out semantic families in the test split.
- Four IFC classes in the test split.
- One intent label (`unknown_edge`) across all 100 test records.
- Validation loss was not recorded during training.
- Private predictions are not publicly available.
- Adapter weights are not publicly released.
- Target agreement on this controlled split is not equivalent to broad AECO
  generalization.
- No statistical significance claim is made.

---

## Public/Private Boundary

### Public (this document and its JSON)

- Aggregate metrics
- Compute measurements
- Formulas and derived calculations
- Model and hyperparameter identifiers
- Dataset and adapter hashes
- Test distribution counts
- Methodological limitations
- Kaggle notebook link

### Private (not in this repository)

- Dataset rows
- Raw prompts
- Expected outputs
- Raw model predictions
- Adapter weights
- Checkpoint files
- Private ZIP archives
- Private project data

---

## Reuse

These measurements may be used as a **preliminary calibration point** for:

- research infrastructure planning;
- GPU platform scoping;
- grant applications;
- compute resource estimation;
- follow-up experiments.

They should not be used as a universal efficiency estimate or as evidence of
production readiness.
