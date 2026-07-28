# Planned Semantic BIM/IFC Benchmark Execution Protocol

STATUS = PLANNED_NOT_EXECUTED
CURRENT_PUBLIC_FIXTURE = NOT_A_COMPARATIVE_BENCHMARK
COMPARATIVE_RESULTS = NONE

## 1. Scope and Status

This document defines a future benchmark protocol. It does not contain
comparative results. The public `sample20` fixture is a minimal
reproducibility fixture and is not a comparative benchmark.

The existing pilot QLoRA measurements remain separate preliminary evidence.
They may inform compute calibration, but compute calibration does not
demonstrate comparative performance. Administrative calculations of resource
capacity are outside this public protocol.

## 2. Experimental Units

The future benchmark will treat the following as explicit experimental units:

- `record_id`: individual evaluation unit;
- `root_case_id`: grouping unit that keeps variants from the same root case
  together;
- `variant_id`: linguistic, contextual or complexity variant derived from a
  root case;
- per-record results;
- aggregated root-case results.

These identifiers belong to the future dataset. `sample20` is not reinterpreted
as if it already implements them.

## 3. Pre-Execution Freeze Manifest

Before any execution, the following manifest items must be frozen. No values are
assigned here.

- dataset version: `TO_BE_FROZEN`;
- dataset content hash: `TO_BE_FROZEN`;
- schema version: `TO_BE_FROZEN`;
- IFC version or versions: `TO_BE_FROZEN`;
- task families: `TO_BE_FROZEN`;
- complexity tiers: `TO_BE_FROZEN`;
- included disciplines: `TO_BE_FROZEN`;
- included languages: `TO_BE_FROZEN`;
- included IFC classes: `TO_BE_FROZEN`;
- train/validation/test/evaluation split hashes: `TO_BE_FROZEN`;
- root-case grouping manifest: `TO_BE_FROZEN`;
- baseline identifiers: `TO_BE_FROZEN`;
- exact model identifiers and revisions: `TO_BE_FROZEN`;
- prompt-template hashes: `TO_BE_FROZEN`;
- retrieval-corpus version and hash: `TO_BE_FROZEN`;
- tool and library versions: `TO_BE_FROZEN`;
- generation settings: `TO_BE_FROZEN`;
- seed list: `TO_BE_FROZEN`;
- repetition count: `TO_BE_FROZEN`;
- hardware description: `TO_BE_FROZEN`;
- software environment: `TO_BE_FROZEN`;
- metric implementation version: `TO_BE_FROZEN`;
- professional-review protocol version: `TO_BE_FROZEN`.

## 4. Baselines

The minimum comparative set is A, B and C.

- A - Deterministic IFC/schema/catalogue lookup - REQUIRED
- B - Base LLM, prompt-only - REQUIRED
- C - Base LLM with retrieved IFC/bSDD/IDS context - REQUIRED
- D - Graph or ontology-grounded retrieval - CONDITIONAL
- E - Tool-using adaptive IFC exploration - CONDITIONAL
- F - Single-agent planner - OPTIONAL
- G - Multi-agent workflow - OPTIONAL
- H - QLoRA-adapted model - OPTIONAL_AFTER_GATES

Rules:

- A, B and C are the minimum comparative set.
- D and E may run only when real and verifiable grounding tools exist.
- F and G must be compared with simpler baselines.
- G is not presumed superior to F.
- H may run only after the dataset and baseline gates are satisfied.
- No concrete model names are listed here.
- No rankings are predicted.

## 5. Common Evaluation Conditions

The compared methods must share:

- the same evaluation set;
- no optimization on test or evaluation data;
- frozen prompts and configurations before final scoring;
- a frozen retrieval corpus;
- documented budgets and tool limits;
- common seeds where technically applicable;
- the same output schema;
- the same evaluator and metric version;
- preserved failed outputs;
- no silent post-hoc deletion of cases.

## 6. Execution Order

The planned order is:

1. freeze scope and manifest;
2. freeze dataset and grouped splits;
3. audit duplication and leakage;
4. validate resolvable references;
5. technical dry run without final scoring;
6. execute A, B and C;
7. conditionally execute D and E;
8. optionally execute F and G;
9. analyze errors;
10. make a documented decision on H;
11. lock scoring;
12. perform professional review and statistical analysis;
13. publish results and limitations.

## 7. Failure and Missing-Run Accounting

The future benchmark will distinguish:

- schema-invalid output;
- tool failure;
- timeout;
- missing output;
- non-resolvable reference;
- unsafe or unsupported mutation proposal;
- evaluator failure;
- infrastructure failure.

Rules:

- failures are not silently removed;
- every public metric reports numerator and denominator;
- technical failures and semantic failures are reported separately;
- any rerun must preserve reason, seed and linkage to the original run.

## 8. Metric Families

Planned metric families:

- Contract validity: schema validity rate, output completeness rate.
- IFC grounding: reference-resolution rate, entity-grounding accuracy,
  invalid IFC claim rate.
- Evidence: supportedness precision, supportedness recall, supportedness F1.
- Expected negatives and recovery: expected-negative accuracy, abstention
  precision, missing-input recall, safe-recovery rate.
- Stratification: task family, complexity tier, language, discipline, IFC
  version, expected-positive versus expected-negative.
- Variability: repeated-run variability, seed-level variability.
- Computational: wall-clock time, CPU core.hours, GPU.hours, peak RAM, peak
  VRAM, storage footprint.

Grounding and supportedness require future resolvable references and cannot be
calculated from `sample20`.

## 9. Computational Measurements

Measured pilot compute values may be used for calibration only. They do not
establish comparative performance.

The public protocol records computational measurements such as:

- wall-clock time;
- CPU core.hours;
- GPU.hours;
- peak RAM;
- peak VRAM;
- storage footprint.

Administrative resource-capacity calculations are outside the public protocol.

## 10. Required Research Outputs

Each future execution must produce:

- frozen manifest;
- run manifest;
- raw structured predictions;
- failure log;
- metric summary with denominators;
- stratified metrics;
- resource measurements;
- error taxonomy;
- statistical-analysis output;
- professional-review record where applicable;
- hashes of published artifacts.

These outputs are required for future execution. They are not claimed to exist
today.

## 11. Current Public Boundary

This document defines planned methodology. It does not report comparative
benchmark results, and it does not convert `sample20` into a benchmark.

The public boundary remains separated from future comparative execution and
from administrative resource-capacity calculations.
