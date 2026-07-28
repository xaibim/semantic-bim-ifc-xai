# Evidence-Trace Evaluation Position

## 1. Public executable meaning

The public artifact treats `evidence_trace` as a required structured field.
It contains `evidence_pattern`, `relation_observed` and `ambiguity_context`.
Public validation checks the field presence, schema type and stored coherence.
`relation_observed` must be declared in `required_relationships`.

## 2. What the public artefact verifies

The public artefact verifies only:

- structural presence;
- JSON Schema conformance;
- model/reference equality;
- internal fixture coherence;
- declared relationship-label coherence;
- stored expected-negative behavior.

## 3. What the public artefact does not verify

The public artefact does not verify:

- existence of an external evidence source;
- source identifiers or source locations;
- whether a source supports a technical claim;
- occurrence of a relationship in a real IFC model;
- professional sufficiency of the evidence;
- causal attribution;
- SHAP or LIME;
- chain-of-thought;
- certification.

## 4. Future dataset methodology

Future dataset methodology may include:

- resolvable source identifiers;
- source-to-claim supportedness review;
- professional reviewer scoring;
- real IFC instance checks;
- hallucination and evidence-sufficiency evaluation.

These items are planned and are not executed as current public checks.

## 5. Future benchmark criterion

Evidence-supportedness is planned as a future benchmark criterion, separate
from the current structural validation.

## 6. Adaptation and quantization

QLoRA, LoRA or quantization must preserve the contract if studied later, but
they are not explanation mechanisms.

## 7. Boundary

The current public evidence trace is a structured audit field, not proof that
a model used a cited source, not causal attribution, and not professional or
normative certification.
