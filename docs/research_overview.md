# Research Overview

## 1. Engineering Problem

BIM projects contain geometric, alphanumeric and documentary information. However, much engineering intent still appears as natural language: requirements, comments, design decisions, review notes, specifications and coordination instructions. The research question is how AI can interpret this natural language and map it to structured BIM/IFC concepts without losing traceability.

On active construction and engineering projects, communication is often unstructured. The translation from natural-language engineering intent (e.g. email threads or client requirements) to physical databases must be systematized to reduce structural errors, misalignment, and parameter corruption.

---

## 2. BIM as Information Management

ISO 19650-1 and ISO 19650-2 establish concepts, principles and delivery-phase
information-management processes for managing information using BIM. The Common
Data Environment (CDE) remains a management concept within that information
workflow.

The broader research investigates how natural-language requirements may be
mapped into structured BIM information-management and IFC exchange contexts.

---

## 3. IFC as Semantic Infrastructure

To ensure software interoperability, the industry relies on the **Industry Foundation Classes (IFC)** schema (ISO 16739). IFC is an open, object-oriented data specification that provides a logical framework to represent building components, properties, and relationships.

Key components of the IFC semantic infrastructure include:
- **Spatial Hierarchies**: e.g., `IfcProject` &rarr; `IfcSite` &rarr; `IfcBuilding` &rarr; `IfcBuildingStorey`.
- **Physical Entities**: e.g., `IfcColumn`, `IfcWall`, `IfcWindow`, `IfcBeam`.
- **Property Sets (Psets)**: Alphanumeric attribute sheets attached to entities (e.g., `Pset_WallCommon`, `Pset_WindowCommon`).
- **Relational Grounding**: Establishing clear object relationships (e.g., connecting a wall and a column via `IfcRelConnectsElements`).

---

## 4. Semantic AI

In this research context, "semantic" goes beyond simple word association or conversational AI. It refers to the systematic alignment of human natural language with standard technical schemas. 

The broader planned research target can be represented as:
`natural language → engineering meaning → IFC candidate → information requirement → validation → evidence trace`.

The current public executable boundary does not implement this complete
prompt-to-output pipeline. It begins with committed stored records.

Rather than acting as a creative text generator, a semantic parser behaves as a classifier and structurer, mapping unstructured prompts into explicit, typed entities governed by engineering schemas.

---

## 5. Why JSON Contracts

The research harness uses JSON (JavaScript Object Notation) and JSONL (JSON Lines) to structure predictions. This format is selected because it enables:
- **Machine-readable outputs**: Standardized payloads support structured downstream use.
- **Reproducible validation**: The structured format allows schema checkers to evaluate keys and data types programmatically.
- **Future model comparisons**: A common structured format can support future
  comparison of different methods over frozen inputs and metrics. No
  comparative benchmark is executed by the current public artifact.
- **Stored-Record Validation and Audit**: Simplifies tracing historical stored
  records and inspecting output flags.
- **Downstream CDE Integration**: Compatible downstream tools may ingest structured payloads when an explicit integration contract is implemented. No such CDE or BIM-authoring mutation is executed by the current public artifact.

---

## 6. Current Public Harness

The public harness hosted in this repository is a reduced demonstration designed to review the core architecture of the research.
- **Sanitized Dataset**: Uses 20 stored synthetic or sanitized records.
- **No Live Inference**: The web interface does not call live model servers or API keys.
- **No 3D Generation**: It validates stored structured metadata and does not generate geometry or physical IFC files.
- **Focus**: Serves as a public review aid for stored-record validation, JSON
contract inspection and deterministic local verification.

---

## 7. Limitations

- **No geometric generation**: The system does not output 3D geometry or model files (no physical IFC files are generated).
- **No live public model**: There is no live neural network running inference in the public web app.
- **No SHAP/LIME feature attribution**: Mathematical explanation metrics are not implemented in this public release.
- **No technical certification**: The system does not certify BIM models for compliance or regulatory review.
- **No replacement for human review**: The stored fixture uses PREVIEW,
  PROPOSAL and GUIDED_RECOVERY states. EXECUTE is absent from the current
  public sample.

## 8. Positioning Sources

- [Literature capability matrix](../benchmark/literature_capability_matrix.md)
- [Curated positioning bibliography](literature/semantic_bim_ifc_bibliography_ieee.md)
- [Research positioning and originality boundary](methodology/research_positioning_and_originality.md)

These sources support public positioning. They are not a completed systematic or scoping review.
