# Internal preliminary semantic BIM experiments

Historical internal aggregate note. The underlying records, predictions and
reports are not public; the aggregate values are not an independently
reproducible public benchmark. Current public terminology and validation
contracts are defined by README.md, PUBLIC_EVIDENCE.md and
docs/methodology/xai_evaluation_position.md.

## Status

This document summarizes internal preliminary experiments used to test whether
the semantic BIM/IFC compilation protocol is technically measurable.

The underlying internal report files are not part of this public repository
snapshot. The
values below are aggregate internal feasibility indicators. They are included
to document motivation and scope, not to provide an independently reproducible
public benchmark.

These experiments are internal preliminary experiments. They are feasibility
evidence for the proposed benchmark workflow. They do not establish a final
benchmark result, claim production readiness, or certify BIM/IFC compliance.

This historical internal log is retained for methodology context only. It is
superseded by the public Evidence-Trace boundary language in the repository's
current public documentation.

## Research task

The experiments follow the same positioning: BIM 3D/IFC is the technical
object, semantic compilation is the computational task, traceability/evidence
is the XAI criterion, the chat interface is the user-facing surface, and the
benchmark is the evaluation method.

The experiments evaluate a structured task:

```text
natural-language BIM request
+ structured BIM/runtime context
+ safety and evidence constraints
        ->
IFC-aware semantic JSON record
        ->
schema validation
        ->
field-level comparison
        ->
evidence-trace structure and stored-record checks
```

The target is not a generic BIM chatbot. The target is a prompt-to-IFC contract
model that can produce structured records suitable for validation and benchmark
comparison.

## Smoke20 diagnostic run

The smoke20 run is a diagnostic smoke test. It demonstrates that the evaluation
pipeline can validate JSON, schema conformance, IFC class mapping and evidence
trace completeness, while also exposing weaknesses in intent classification,
missing-field handling and Pset recall.

| Metric | Preliminary value |
| --- | ---: |
| processed_count | 20 |
| json_parse_success | 1.0 |
| schema_valid_rate | 1.0 |
| ifc_class_accuracy | 1.0 |
| semantic_type_accuracy | 1.0 |
| evidence_trace_completeness | 1.0 |
| intent_class_accuracy | 0.55 |
| missing_fields_accuracy | 0.85 |
| required_psets_recall | 0.866667 |
| relationship_recall | 1.0 |
| latency_average_ms | 9265.93 |

Interpretation: this smoke test should not be read as a performance claim. Its
value is methodological: it confirms that the harness can both detect valid
structured outputs and expose measurable failure modes.

This historical metric counts stored evidence-trace field completeness. It does
not establish external evidence grounding or supportedness.

## V4 5k preliminary run

A larger internal preliminary run was used to test the same protocol at a
higher scale.

| Metric | Preliminary value |
| --- | ---: |
| processed_count | 5000 |
| json_parse_success | 1.0 |
| schema_valid_rate | 1.0 |
| ifc_class_accuracy | 1.0 |
| intent_class_accuracy | 1.0 |
| semantic_type_accuracy | 1.0 |
| evidence_trace_completeness | 1.0 |
| required_psets_recall | 0.90655 |
| relationship_recall | 0.9878 |
| missing_fields_accuracy | 0.9914 |
| latency_average_ms | 9126.94 |
| latency_median_ms | 8992.93 |
| latency_p95_ms | 11144.58 |

Interpretation: this run indicates that the protocol can be executed at larger
preliminary scale. It does not replace a controlled public benchmark.

## Preliminary QLoRA adaptation experiment

A private preliminary QLoRA adapter was trained in a bounded run on a private
controlled synthetic pilot dataset of 1,000 records.

- Adapter weights remain private and are not publicly released.
- Sanitized aggregate evidence (metrics, compute measurements, formulas) is
  published at [`benchmark/qlora/`](../../benchmark/qlora/).
- The result is preliminary: single run, single seed, one epoch, seven
  held-out semantic families.
- No broad AECO generalization is established.
- No production readiness is claimed.
- No final benchmark conclusion is drawn.

The adapter is not presented as a public artifact or product.

Public notebook: <https://www.kaggle.com/code/xaibim/semantic-bim-ifc-xai>

## What these experiments demonstrate

The preliminary runs show that the proposed protocol can measure:

* JSON parse validity;
* schema conformance;
* IFC class selection;
* semantic type assignment;
* intent classification;
* required Pset recall;
* IFC relationship recall;
* missing-field handling;
* evidence trace completeness;
* latency;
* GPU resource consumption and training feasibility.

## What these experiments do not claim

These runs do not claim that:

- a complete public corpus already exists;
- a final benchmark has been produced;
- the system is production ready;
- the repository is a certified BIM or regulatory checker;
- the adapter generalizes broadly to unseen AECO tasks;
- the results carry statistical significance.

## Relation to future work

The public repository provides a minimal reproducibility sample and stored-record
validation protocol. A systematic benchmark, a broader public dataset, and
further adaptation experiments remain future work. These preliminary
experiments are methodological support for a controlled research workflow.
