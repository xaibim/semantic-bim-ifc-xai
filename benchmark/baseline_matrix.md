# Baseline Matrix (Planned Comparative Benchmark)

This document defines a planned comparative benchmark. It is an experimental
plan. No final comparative results exist yet. The public sample20 fixture does
not demonstrate general superiority of any model or method.

## Baselines

| ID | Baseline | Status | Description |
| --- | --- | --- | --- |
| A | Deterministic rule / schema lookup | REQUIRED | Map the request to IFC classes, Psets and relationships using the public schema and canonical catalogue only. No learned model. |
| B | Base LLM, prompt-only | REQUIRED | A base LLM prompted to produce the structured semantic record with no retrieved context. |
| C | Base LLM with retrieved BIM/IFC context | REQUIRED | Base LLM plus retrieved BIM/IFC context (catalogues, Psets, relationships). |
| D | QLoRA-adapted model | OPTIONAL | Bounded adaptation only after dataset-quality and baseline gates. It is not required for successful completion of the project. |
| E | Graph / ontology-grounded retrieval | OPTIONAL | Optional only if implemented: retrieval grounded in an IFC graph or ontology. |

## Metrics

- JSON parse rate;
- strict schema validity (JSON Schema Draft 2020-12);
- IFC class agreement;
- semantic type agreement;
- intent agreement;
- `value_mode` conformance;
- missing-input recall;
- required-Pset recall;
- required-relationship recall;
- expected-negative handling;
- unsupported IFC claim rate;
- evidence supportedness;
- safe-next-action rate;
- latency;
- GPU-hours;
- peak VRAM.

## Status

- The matrix is the planned comparative benchmark.
- No final comparative results are reported here.
- `sample20` is a minimal reproducibility sample and does not demonstrate
  general superiority.
- QLoRA adaptation is optional and is not required for successful completion
  of the dataset and benchmark work.
- The matrix will be executed within the planned advanced-computing work after
  the scope freeze described in
  [`docs/methodology/dataset_scope_and_compute_scaling.md`](../docs/methodology/dataset_scope_and_compute_scaling.md).

## Links

- Canonical repository: <https://github.com/xaibim/semantic-bim-ifc-xai>
- Roadmap: see `README.md`
- Methodology: [`docs/methodology/validation_gates.md`](../docs/methodology/validation_gates.md)
- Dataset scope: [`docs/methodology/dataset_scope_and_compute_scaling.md`](../docs/methodology/dataset_scope_and_compute_scaling.md)
