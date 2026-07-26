# Dataset Construction and Training-Readiness Methodology

## 1. Scientific Motivation

The semantic interpretation of Building Information Modeling (BIM) data in the
context of the Industry Foundation Classes (IFC) schema is not a generic
prompt-response task. Standard natural language processing systems often treat
text inputs and structured outputs in isolation, disregarding the deep domain
constraints inherent in civil engineering. A valid semantic BIM record must
capture and formalize:

- **Engineering Intent**: The precise technical objective requested by the
  practitioner (e.g., classification, property enrichment, spatial query,
  compliance check).
- **BIM/IFC Context**: The structural topology, spatial relationships, and
  metadata of the element under consideration.
- **IFC Class Candidate**: The target entity within the IFC schema hierarchy
  (e.g., `IfcWall`, `IfcColumn`, `IfcSlab`).
- **Information Requirements**: The Level of Information Need (LOIN)
  specifying mandatory properties, quantities, and classifications.
- **Evidence Trace**: The explicit grounds (GlobalIds, property sets, rules, or
  geometric parameters) that justify a classification or property assignment.
- **Validation State and Traceability**: Audit metadata detailing origin,
  sanitization status, and schema validation results.

Without these components, models are prone to hallucinating invalid IFC classes,
incorrect property set mappings, and groundless technical claims — compromising
safety and quality in governed AECO workflows.

![Semantic BIM/IFC record concept](../assets/figures/figure_02_semantic_bim_prompt.png)

*Figure 1. Structured semantic BIM/IFC record concept used to connect natural-language engineering requests with IFC grounding, information requirements, validation metadata, and evidence traces.*

---

## 2. Rejection of Plain Instruction-Output Training

Conventional LLM fine-tuning on plain `instruction/context/output` text pairs
was rejected for several critical reasons:

1. **Lack of Schema Enforcement**: Standard token-generation models do not
   inherently respect the strict syntax and schema requirements of formats like
   IFC, ifcJSON, or structured engineering contracts.
2. **Hallucination of Catalogues**: In civil engineering, elements must map to
   canonical classification catalogues and standard property sets. Plain text
   outputs fail to maintain alignments with these Single Sources of Truth
   (SSOT).
3. **Absence of Grounding and Rationale**: A plain text response cannot easily
   be audited. Engineering decisions require a clear evidence trace back to
   the source model.
4. **Mutational Safety**: Plain instructions do not distinguish between safe
   queries (read-only preview) and destructive mutations (model alterations),
   presenting risks to the integrity of Common Data Environments (CDE).

Dataset design therefore centers on structured, schema-validated runtime
payloads mapped to canonical catalogues.

---

## 3. Runtime and Payload Architecture

The dataset and pipeline infrastructure is governed by several key concepts:

- **Runtime Payload and SSOT**: A structured payload encapsulates the input
  request, the active database schema, and the target catalogues, ensuring any
  generated output is evaluated against a Single Source of Truth.
- **Capabilities Catalog**: A registry of supported operations, classes, and
  properties, preventing the AI from generating arbitrary properties or
  violating schema rules.
- **Public record contract**: The strict `sample20` v2 schema
  (`sample20/schema_public_sample20_v2.json`, JSON Schema Draft 2020-12) encodes
  the public fields, value modes, and neutral dataset-candidate states.
- **private pilot dataset**: A private development pilot used for early
  LoRA/QLoRA adaptation experiments (not published).
- **private high-fidelity internal dataset**: A private high-fidelity seed
  dataset used for closed-loop testing (not published).
- **sample20**: A public, fully sanitized subset of 20 illustrative frozen fixture cases for
  scientific evidence and reproducible evaluation.
- **Stored-record validation and Guided Harness**: Codebases that load stored
  public record payloads and validate schema, case-expectation and
  fixture-conformance fields. They do not rerun model generation.

> Historical internal development stages existed before the public artifact.
> They are **historical internal development stages, not public releases or
> public validation claims**, and are not presented here as public milestones.

![Dataset construction and benchmark cycle](../assets/figures/figure_03_experimental_cycle.png)

*Figure 2. Dataset and benchmark lifecycle linking record construction, validation, replay, baseline evaluation, future adaptation, and XAI-oriented assessment.*

---

## 4. Verifiable Public Chronology

| Phase | Title | Description |
| --- | --- | --- |
| 1 | Semantic task definition | Defined the structured semantic BIM compilation task: NL request → IFC-aware semantic record with validation, evidence and replay. |
| 2 | `v0.1` public sample | First public sanitized sample and public repository foundation. |
| 3 | `v0.1.1` validation cleanup | Public validation cleanup: forbidden scan, CI and release notes. |
| 4 | Preliminary QLoRA feasibility evidence | Bounded Qwen2.5-7B QLoRA compute-feasibility experiment on a private pilot (synthetic/controlled). |
| 5 | `sample20` v2 strict validation | Strict `sample20` v2 JSON Schema Draft 2020-12 contract with expected negatives. |
| 6 | GitHub/Hugging Face integrity alignment | Three-copy schema/JSONL integrity and alignment of the public Replay and Harness Spaces. |
| 7 | `v0.2` final public research artifact | Canonical `xaibim` GitHub namespace, `XAIBIM` Hugging Face namespace, corrected documentation and planned comparative benchmark matrix. |

Internal development work that preceded these public steps is treated as
**historical internal development stages, not public releases or public
validation claims**.

---

## 5. Public Record Structure (`sample20` v2)

A single valid public semantic record contains:

| Field | Description |
| --- | --- |
| `schema_version` | Contract version (currently `2.0`). |
| `sample_id` | Unique record identifier. |
| `case_expectation` | `VALID` or `EXPECTED_CANONICAL_REJECTION`. |
| `expectation_met` | Whether actual status matches the case expectation. |
| `record_status` | `PASS` or `EXPECTED_REJECTION_PASS`. |
| `input_summary` | Discipline, IFC class group, semantic type, ambiguity flags, missing inputs, recovery type. |
| `model_output` | Structured output: intent, semantic type, IFC class, value mode, dimensions, Psets, relationships, missing inputs, ambiguity flags, recovery, safe next action, reason codes, evidence trace. |
| `reference_output` | Stored synthetic reference target for agreement checking. |
| `canonical_check` | Coherence check between output, reference and expectation. |
| `agreement` | Field-level agreement between model output and reference output. |
| `reference_scope` | Scope of the reference (synthetic target, not normative certification). |

---

## 6. Public Artifact Boundary

The public artifacts in this repository represent a strictly sanitized and
demonstrative research surface:

- **Sanitized Dataset**: `sample20` uses generic, synthetic cases. No real
  building models, proprietary databases, or private corporate structures
  are exposed.
- **No Private Models**: The public Replay Space loads stored fixture records,
  and the public Harness Space provides a constrained conceptual demonstration.
  No private weights or custom adapters are published.
- **Research Orientation**: This repository demonstrates feasibility of the
  semantic contract and benchmark protocol. It does not provide certified
  commercial deliverables or professional engineering signatures.
