# Dataset Construction and Training-Readiness Methodology

## 1. Scientific Motivation

### A. Broader research target

The broader research target is a semantic BIM task where a professional
request can mention IFC context, information requirements, source-grounding
concepts and recoverable ambiguity. In that broader setting, a model would need
to produce structured outputs that support validation and review.

### B. Current public v2 fixture

The current public `sample20` fixture is narrower. The public schema does not
contain:

- original prompt;
- raw runtime payload;
- LOIN object;
- external source identifier;
- source location;
- audit metadata.

The public `evidence_trace` contains only structured labels.

![Semantic BIM/IFC record concept](../assets/figures/figure_02_semantic_bim_prompt.png)

*Figure 1. Structured semantic BIM/IFC record concept used to connect natural-language engineering requests with structured public record fields, validation metadata, and evidence-trace labels.*

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
   be audited. Engineering decisions require a clear evidence trace back to the
   source model.
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
- **sample20**: A public sanitized frozen fixture of 20 illustrative records.
- **Stored-record validation**: Code that loads stored public record payloads
  and validates schema, case-expectation and fixture-conformance fields. It
  does not rerun model generation.

> Historical internal development stages existed before the public artifact.
> They are historical internal development stages, not public releases or public
> validation claims, and are not presented here as public milestones.

![Dataset construction and benchmark cycle](../assets/figures/figure_03_experimental_cycle.png)

*Figure 2. Dataset and benchmark lifecycle linking record construction, stored-record validation, baseline evaluation, future adaptation, and XAI-oriented assessment.*

---

## 4. Verifiable Current State

| Item | Current state |
| --- | --- |
| 1. Public fixture | 20 committed records, 18 VALID, 2 expected rejections. |
| 2. Strict schema | JSON Schema Draft 2020-12. |
| 3. Stored-record validation | Parsing, schema, fixture contract and integrity. |
| 4. IFC4 Pset audit | Class applicability only. |
| 5. IFC4 relationship audit | Schema compatibility only; no task-suitability conclusion. |
| 6. Preliminary QLoRA evidence | One private controlled feasibility pilot; aggregate evidence only. |
| 7. Public gateways | Canonical XAIBIM gateways and verified bimaiblend Gradio runtimes. |
| 8. Planned work | Larger dataset and comparative benchmark. |

No tag or release state is claimed by this methodology document.

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
  building models, proprietary databases, or private corporate structures are
  exposed.
- **No Private Models**: The public Replay Space loads stored fixture records,
  and the public Harness Space provides a constrained conceptual demonstration.
  No private weights or custom adapters are published.
- **Research Orientation**: This repository demonstrates feasibility of the
  semantic contract and stored-record validation protocol. It does not provide
  certified commercial deliverables or professional engineering signatures.
