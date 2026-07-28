# Baseline Matrix (Planned Comparative Benchmark)

This document defines a planned comparative benchmark. It is an experimental
plan. No final comparative results exist yet. The public `sample20` fixture
does not establish comparative performance for any method.

## Baselines

| ID | Baseline | Status | Description |
| --- | --- | --- | --- |
| A | Deterministic IFC/schema/catalogue lookup | REQUIRED | Map the request to IFC classes, Psets and relationships using the public schema and canonical catalogue only. No learned model. |
| B | Base LLM, prompt-only | REQUIRED | A base LLM prompted to produce the structured semantic record with no retrieved context. |
| C | Base LLM with retrieved IFC/bSDD/IDS context | REQUIRED | Base LLM plus retrieved IFC/bSDD/IDS context with no graph grounding. |
| D | Graph or ontology-grounded retrieval | CONDITIONAL | Retrieval grounded in a graph or ontology, used only when the IFC model and tools are real and verifiable. |
| E | Tool-using adaptive IFC exploration | CONDITIONAL | Adaptive exploration over IFC data using verifiable tools and model-linked grounding. |
| F | Single-agent planner | OPTIONAL | One planning agent compares against simpler baselines. |
| G | Multi-agent workflow | OPTIONAL | Multiple agents cooperate in a workflow; it is not presumed superior to the single-agent planner. |
| H | QLoRA-adapted model | OPTIONAL_AFTER_GATES | Bounded adaptation studied only after dataset-quality and baseline gates. |

## Execution Prerequisites

The benchmark may only be executed after these gates are frozen:

- scope freeze;
- dataset version freeze;
- root-case grouping;
- deduplication audit;
- cross-split leakage audit;
- retrieval-corpus leakage audit;
- resolvable-reference gate;
- metric implementation freeze;
- statistical-analysis freeze;
- compute instrumentation;
- professional-review protocol where applicable.

## Canonical Planned Protocols

- [Planned Semantic BIM/IFC Benchmark Execution Protocol](benchmark_execution_protocol.md)
- [Planned Statistical Analysis Plan](statistical_analysis_plan.md)
- [Planned Dataset Governance, Split and Leakage Protocol](../docs/methodology/dataset_governance_split_and_leakage_protocol.md)

## Metrics

Planned metrics:

- strict schema validity;
- reference-resolution rate;
- entity-grounding accuracy;
- evidence-supportedness precision;
- evidence-supportedness recall;
- expected-negative accuracy;
- abstention precision;
- missing-input recall;
- safe-recovery rate;
- invalid IFC claim rate;
- task-family stratification;
- complexity-level stratification;
- repeated-run variability;
- wall-clock time;
- CPU core.hours;
- GPU.hours;
- peak RAM;
- peak VRAM;
- storage footprint.

Grounding and supportedness metrics require a future dataset with references
that are resolvable. They cannot be calculated from sample20.

## Status

- The matrix is the planned comparative benchmark.
- No final comparative results are reported here.
- `sample20` is a minimal reproducibility sample and does not establish
  comparative performance.
- QLoRA adaptation is optional and is not required for successful completion
  of the dataset and benchmark work.
- The matrix will be executed after scope freeze and prerequisite dataset-quality gates.
- Measured compute values may calibrate resource expectations, but they do
  not establish superiority.

## Links

- Canonical repository: <https://github.com/xaibim/semantic-bim-ifc-xai>
- Roadmap: see `README.md`
- Methodology: [`docs/methodology/validation_gates.md`](../docs/methodology/validation_gates.md)
- Dataset scope: [`docs/methodology/dataset_scope_and_compute_scaling.md`](../docs/methodology/dataset_scope_and_compute_scaling.md)
