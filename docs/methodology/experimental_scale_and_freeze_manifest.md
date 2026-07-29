# Experimental scale and freeze manifest

STATUS = PRE_EXECUTION_METHOD_FREEZE

This manifest fixes the planning scope used for dataset construction and resource calibration. Content hashes and exact model revisions remain `PENDING_DATA_FREEZE` until the corresponding artifacts exist. It does not prove IFC4 coverage or implementation readiness.

## Scale scenarios

| Dimension | Minimum | Planned | Ceiling |
| --- | ---: | ---: | ---: |
| Records | 10,000 | 20,000 | 50,000 |
| Root cases | 1,000 | 2,000 | 5,000 |
| Average controlled variants per root case | 10 | 10 | up to 10 |
| Frozen evaluation records | 1,000 | 2,000 | gate-dependent |

The ceiling is conditional and not an automatic target.

## Primary technical scope

- Primary IFC schema family: IFC4 / ISO 16739-1:2024 terminology.
- Compatibility subsets: IFC2X3 and IFC4X3 only when explicitly labelled and separately stratified.
- Planned disciplines: architecture, structural, mechanical, electrical, facility management and construction management.
- Primary language: English.
- Bounded robustness languages: Portuguese and Spanish; no full multilingual-coverage claim.
- Task families: entity/class mapping; property and Pset assignment; relationship identification; information-requirement completion; ambiguity/missing-input detection; expected-negative handling; safe recovery; evidence-trace construction.
- Complexity tiers: basic, intermediate, complex and adversarial/expected-negative.

## Split policy

- development/train: 70%
- validation: 10%
- test: 10%
- frozen evaluation: 10%
- grouping unit: `root_case_id`
- variants from one root case may not cross splits
- split seed and hashes: frozen when dataset v0.1 is created

## Benchmark cells

Required method families:

- A: deterministic IFC/schema/catalogue lookup;
- B: open-weight base model, prompt-only;
- C: the same output contract with retrieved IFC/bSDD/IDS context.

Planned compute cells use four model/configuration cells across B/C for capacity calculation. Exact model identifiers, revisions and licences are frozen in M1 before download. D/E grounding tools are conditional; F/G agent workflows are optional; H QLoRA is optional after all prerequisite gates.

## Repetition policy

- deterministic decoding: one frozen run plus technical dry run;
- stochastic robustness subset: three seeds;
- reruns: only after a documented infrastructure failure or predeclared sensitivity analysis;
- failed outputs remain in denominators.

## Metrics

- strict schema validity and output completeness;
- catalogue/reference resolution;
- entity/IFC grounding accuracy;
- expected-negative accuracy;
- missing-input recall and safe-recovery rate;
- invalid IFC claim rate;
- evidence supportedness only when references are resolvable;
- stratified metrics by task, complexity, discipline, language and IFC subset;
- wall time, CPU core.h, GPU.h, peak RAM/VRAM and storage footprint.

## Freeze outputs

Before final scoring, freeze and hash: dataset; schema; splits; root-case groups; prompt templates; model revisions; retrieval corpus; tools; generation settings; seeds; metric implementation; human-review protocol; container; Slurm scripts; and hardware description.
