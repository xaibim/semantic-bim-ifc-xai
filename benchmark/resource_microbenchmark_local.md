# Local Resource Microbenchmark

This artifact is a local proxy measurement only.
It does not measure Deucalion or A100 performance.
The on-platform M1 measurement remains mandatory.

## Workload

- logical records: 20000
- repetitions: 1000
- warmup rounds: 5
- measured rounds: 10
- synthetic grouping key: `sample_id + "-iteration-" + index`
- no expanded dataset is written to disk

## CPU Results

| Operation | Mean s | Median s | P95 s | Records/s |
| --- | ---: | ---: | ---: | ---: |
| json_parsing | 0.238789 | 0.233862 | 0.278905 | 83755.95 |
| json_schema_validation | 16.935613 | 16.910517 | 18.796023 | 1180.94 |
| deterministic_serialization | 0.675038 | 0.674230 | 0.713304 | 29627.96 |
| sha256 | 0.729268 | 0.734760 | 0.795803 | 27424.76 |
| dedup_key_construction | 0.008135 | 0.008499 | 0.010873 | 2458560.96 |
| root_case_grouping | 0.009060 | 0.009209 | 0.010612 | 2207620.04 |
| cpu_pipeline_combined | 17.514210 | 17.406279 | 19.084700 | 1141.93 |

## GPU Status

- status: NOT_EXECUTED_MODEL_NOT_PROVIDED
- used_for_capacity_recalculation: false

## Boundary

This benchmark is a proxy for local CPU and optional local-model GPU behavior.
It does not change the planning envelopes and it does not replace the M1 on-platform measurement.
