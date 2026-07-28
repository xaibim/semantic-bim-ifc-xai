# Planned Statistical Analysis Plan

STATUS = PLANNED_NOT_EXECUTED
NO_COMPARATIVE_INFERENCE_HAS_BEEN_PERFORMED

## 1. Status and Purpose

This plan defines the future statistical analysis for the benchmark. It is not
an executed analysis and contains no results.

## 2. Units of Analysis

- The primary unit is the `root_case_id`.
- Variants derived from the same `root_case_id` are not independent cases.
- Comparisons are paired on the same cases whenever methods are compared.

## 3. Descriptive Reporting

- Publish counts, denominators, rates and absolute differences.
- Publish 95% bilateral confidence intervals.
- Report effect sizes alongside intervals.
- Do not rely only on p-values for conclusions.

## 4. Paired Comparative Analysis

- All method comparisons must be paired on the same cases.
- For binary paired outcomes, exact McNemar analysis may be used as a
  complementary analysis when applicable.
- For rates and rate differences, use clustered bootstrap resampling by
  `root_case_id`.

## 5. Clustered Uncertainty

- Clustered bootstrap resampling must respect `root_case_id` grouping.
- The bootstrap replicate count must be `TO_BE_FROZEN`.
- The analysis must not treat seed-level outputs as independent cases.

## 6. Repeated Runs and Seeds

- Seeds are repeated runs within a configuration, not new cases.
- Repeated seeds are used to estimate variability, not to create
  pseudoreplication.
- Do not average across seeds and cases in a way that creates pseudoreplication.

## 7. Multiple Comparisons

- Pre-specified comparison families must be adjusted with Holm.
- Any additional comparisons must be labeled exploratory.

## 8. Missing and Failed Runs

- A failed run remains in the denominator for the relevant metric.
- Exclusions must be defined before final analysis.
- Failed or missing runs are reported separately from successful runs.

## 9. Stratified and Sensitivity Analyses

- Stratified analyses may be reported by task family, complexity tier,
  language, discipline, expected-negative state and IFC version.
- These analyses are secondary to the primary paired analysis.
- Sensitivity analyses must be identified as secondary.

## 10. Professional Review

- If more than one professional reviewer is used, report reviewer agreement
  with a measure appropriate to the label type.
- The specific agreement measure must be frozen before evaluation.
- Professional review is separate from schema compatibility.

## 11. Computational Metrics

- Computational metrics are descriptive.
- They do not by themselves prove semantic quality.
- Report time and resource metrics with medians, interquartile ranges and
  paired estimates where appropriate.

## 12. Reporting Rules

- Report results with denominators and uncertainty.
- Preserve failed runs in the relevant denominator.
- Do not remove outliers after seeing which method they favor.
- Do not present post-hoc exclusions as pre-defined rules.

## 13. Prohibited Interpretations

- No statistical inference is executed on `sample20`.
- The pilot QLoRA run is not a substitute for the comparative benchmark.
- Do not claim general AECO superiority.
- Do not claim generalization.
- Do not claim certification.
- Do not claim production readiness.
