# XAI Evidence Positioning Compatibility Note

This note is retained for compatibility with older references. The canonical
public position is [Evidence-Trace Evaluation Position](xai_evaluation_position.md).

`Replay`, where retained as a historical CLI or Space name, means loading and
validating committed stored records. It does not mean rerunning model
generation or the original prompt-to-output pipeline.

The public evidence trace is a structured audit field over committed records.
It supports structural presence checks, JSON Schema conformance, model/reference
equality, fixture coherence, declared relationship-label coherence, and
expected-negative behavior. It does not establish external-source supportedness,
causal attribution, model-internal explanation, or certification.

Historical phrasing from the earlier note is superseded by the canonical
position document.
