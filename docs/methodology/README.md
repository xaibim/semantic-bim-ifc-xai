# docs/methodology

## Purpose

This folder explains the methodologies behind validation gates, dataset construction, experimental scope, evaluation positioning, evidence traceability, platform compatibility, resource measurement, human review, operational risk, and controlled release.

## Contents

- `validation_gates.md`: criteria used to qualify records.
- `dataset_scope_and_compute_scaling.md`: public fixture, private pilot boundary, optional QLoRA and compute-scaling context.
- `dataset_construction_and_training_readiness.md`: structured dataset construction and readiness boundary.
- `dataset_governance_split_and_leakage_protocol.md`: grouped splits, leakage and governance rules.
- `semantic_bim_compilation_task.md`: overview of the prompt-to-IFC compilation task.
- `xai_evaluation_position.md` / `xai_evidence_positioning.md`: evidence-trace evaluation boundaries.
- `schema_contract_map.md`: validation schema layers.
- `software_and_platform_compatibility.md`: frozen target stack, Slurm profiles, smoke tests and fallbacks.
- `resource_capacity_plan.md`: minimum, planned and ceiling capacity scenarios with stop rules.
- `experimental_scale_and_freeze_manifest.md`: planned record/root-case scale, splits, IFC/language/task scope and freeze outputs.
- `human_review_and_operational_risk.md`: review coverage, agreement/adjudication and operational risk matrix.
- `data_governance_and_release.md`: source rights, privacy, provenance, retention, dataset-use states and release gate.

## Related benchmark artifacts

- `benchmark/baseline_matrix.md`: planned comparative methods.
- `benchmark/benchmark_execution_protocol.md`: planned benchmark execution rules.
- `benchmark/statistical_analysis_plan.md`: planned statistical analysis.
- `benchmark/resource_calibration.json`: machine-readable measurements, assumptions and scenario calculations.
- `benchmark/resource_calibration.md`: readable interpretation of the resource-calibration JSON.

## What this folder does not contain

- Private datasets, protected IFC files, model checkpoints or adapters.
- Production, certification or professional-approval tools.
- Administrative application values or funding-form language.
