# Resource capacity plan

## Boundary

This document provides neutral, reproducible capacity-planning methodology. It separates measured prior evidence, explicit planning assumptions and future on-platform measurements. It does not state an administrative resource request.

## Formulae

CPU core-hours are calculated from actual allocations:

`CPU core-hours = sum(job wall-time hours x allocated CPU cores)`

GPU-hours are calculated by experimental cell:

`GPU-hours = cases x model cells x configurations x seeds x variants x seconds per case x GPUs per job / 3600`

Storage is the sum of source, dataset-version, model/container-cache, output, log, temporary/checkpoint and backup components.

## Scenarios

| Scenario | Dataset records | Root cases | Evaluation cases | CPU envelope | GPU envelope | Storage envelope | Activation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Minimum | 10,000 | 1,000 | 1,000 | 10,000 core.h | 700 GPU.h | 1.0 TB | Required dataset and A/B/C baselines |
| Planned | 20,000 | 2,000 | 2,000 | 20,000 core.h | 1,500 GPU.h | 2.0 TB | Main controlled benchmark |
| Ceiling | up to 50,000 | up to 5,000 | gate-dependent | 50,000 core.h | 3,000 GPU.h | 4.0 TB | Only after planned-scenario QA and efficiency gates |

The ceiling is not a target. It must not be activated to consume unused capacity.

## Planned CPU envelope

The planning model assumes a platform where CPU-only x86 nodes are exclusive and charged as full nodes:

- 12 complete pipeline runs x 10 wall-time hours x 128 cores = 15,360 core.h;
- 16 calibration/QA jobs x 8 hours x 32 cores = 4,096 core.h;
- controlled reruns and reporting = 544 core.h;
- total planning envelope = 20,000 core.h.

All job counts are assumptions to be replaced by M1 measurements. The public artifact records both the original assumption and the revised measured value.

## Planned GPU envelope

At an explicit conservative planning latency of 30 seconds per case on one GPU:

- core benchmark: 2,000 cases x 4 model cells x 2 configurations = 133.3 GPU.h;
- robustness subset: 500 cases x 4 model cells x 2 configurations x 3 seeds x 4 variants = 800 GPU.h;
- repeated evaluation subset = 200 GPU.h;
- calibration, loading and documented reruns = 250 GPU.h;
- optional post-gate adaptation = 100 GPU.h;
- total before rounding = 1,483.3 GPU.h;
- planned envelope = 1,500 GPU.h.

The 30-second input is not a measured A100 value. It must be replaced by a 100-200 case on-platform microbenchmark. No theoretical T4-to-A100 conversion is permitted.

## Planned storage envelope

| Component | TB |
| --- | ---: |
| Controlled sources and normalized dataset versions | 0.30 |
| Model and container cache | 0.60 |
| Structured predictions and benchmark outputs | 0.35 |
| Logs, manifests and reports | 0.15 |
| Optional checkpoints and temporary artifacts | 0.30 |
| Backup and retry margin | 0.30 |
| Total | 2.00 |

## Monthly execution profile

- M1: environment and microbenchmarks; approximately 10% of planned capacity.
- M2: dataset production and QA; approximately 15% CPU, 5% GPU.
- M3: review, deduplication, leakage and split freeze; approximately 25% CPU, 5% GPU.
- M4: required baselines; approximately 25% CPU, 35% GPU.
- M5: robustness and error analysis; approximately 15% CPU, 45% GPU.
- M6: controlled reruns and release; approximately 10% CPU, 10% GPU.

Percentages are scheduling envelopes and are updated after M1 measurement.

The local proxy microbenchmark artifact in `benchmark/resource_microbenchmark_local.json`
is available for CPU-only proxy measurement. It is not an on-platform replacement,
the current planning envelopes remain unchanged, and the M1 measurement remains mandatory.

## Stop and reduction rules

1. Required dataset-quality gates have priority over all optional model work.
2. Optional adaptation is cancelled before dataset scale, A/B/C baselines or review quality are reduced.
3. The ceiling scenario is disabled when review capacity, leakage, storage growth or failure-rate thresholds are exceeded.
4. A model cell is reduced or removed when it repeatedly exceeds the frozen wall-time or VRAM envelope.
5. Failed runs remain in denominators and are rerun only with a recorded reason.
6. Every capacity update preserves the original assumption, measured replacement, date, hardware and software hash.
