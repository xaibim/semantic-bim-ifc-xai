# Software and platform compatibility

## Status and boundary

This document defines a reproducible target environment and platform-validation procedure for future semantic BIM/IFC dataset and benchmark work. It is neutral research methodology. It does not assert that an allocation has been granted, and exact environment hashes are frozen only after the installation smoke test.

## Parallelization contract

MPI = NO
OPENMP = NO_EXPLICIT_USE
CUDA = YES

- The workflow does not require distributed MPI communication.
- OpenMP is not invoked explicitly by the workflow.
- CPU-side libraries may use internal threads, but those threads must be limited and recorded.
- GPU execution runs with CUDA through PyTorch.
- The primary platform mapping is Deucalion GPU/x86.
- Cirrus is the fallback development platform.
- Navigator and Oblivion are CPU alternatives only if they are assigned.
- ARM64 remains disabled until import, wheel, container, schema, IFC and test-suite checks all pass on the assigned ARM environment.

## Preferred execution environment

- Architecture: Linux `x86_64` on the assigned Deucalion GPU/x86 platform.
- Scheduler: assigned platform Slurm version, recorded at M1.
- GPU target: CUDA-capable NVIDIA GPU; one GPU per default inference job.
- CPU target: assigned x86 CPU allocation for CPU-only pipelines when a CPU phase is scheduled.
- Container: Singularity/Apptainer SIF built from a versioned definition file.
- Fallback: Cirrus or another compatible NVIDIA GPU platform with sufficient VRAM, after the same smoke tests.

ARM64 is not a default target. It may be enabled only after all compiled dependencies, wheels, containers, schemas, IFC fixtures and tests pass on the assigned ARM environment.

## Frozen target stack for the first compatibility gate

| Component | Target | Purpose |
| --- | --- | --- |
| Python | 3.11 | Runtime |
| PyTorch | 2.5.1 + CUDA 11.8 | GPU inference and optional bounded adaptation |
| Transformers | 4.56.2 | Model loading and generation |
| Datasets | 3.2.x | Dataset processing |
| PEFT | 0.14.x | Optional post-gate LoRA/QLoRA |
| Accelerate | 1.3.x | Device/runtime support |
| bitsandbytes | 0.45.x | Optional quantization |
| tokenizers | 0.21.x | Tokenization |
| IfcOpenShell | 0.8.5 | IFC2X3/IFC4/IFC4X3 parsing and schema access |
| jsonschema | 4.23.x | JSON Schema Draft 2020-12 validation |
| pandas | 2.2.x | Tabular analysis |
| scikit-learn | 1.6.x | Metrics and split utilities |
| pyarrow | 19.x | Columnar data exchange |
| Git | platform module/package | Versioning |
| Singularity/Apptainer | platform-supported | Reproducible SIF execution |

Versions are target pins, not claims of newest versions. A machine-readable lock file and container hash replace version ranges before final benchmark execution.

## Installation and smoke-test gate

1. Load the platform CUDA and compiler modules required by the partition.
2. Create or pull the versioned SIF container without embedding credentials.
3. Verify `python --version`, `torch.__version__`, `torch.version.cuda` and `torch.cuda.is_available()`.
4. Verify one tensor operation on the allocated GPU.
5. Import Transformers, Datasets, PEFT, bitsandbytes, IfcOpenShell, jsonschema, pandas and scikit-learn.
6. Parse representative IFC2X3, IFC4 and IFC4X3 fixtures where available.
7. Execute the public stored-record validation and unit tests.
8. Execute a 100-200 case inference microbenchmark and record latency, throughput and peak VRAM.
9. Freeze the container SHA-256, dependency lock hash, module list and Slurm script hash.

## Requested job profiles pending platform confirmation

### GPU inference/calibration

- nodes: 1
- GPUs: 1
- requested CPUs per task: 32, recorded as a requested and measured value rather than a platform guarantee
- requested RAM: initially 128 GB; reduce only after measurement
- requested wall time: 4 hours for development, up to 48 hours for planned batches
- checkpoint/output interval: at most 30 minutes or one completed shard

### CPU dataset pipeline

- nodes: 1 assigned x86 CPU allocation when CPU nodes are exclusive
- cores: requested cores per job, not a claim about physical node topology
- RAM: measured during M1; initial envelope 256 GB
- wall time: at most 24 hours per shard; prefer 8-10 hour bounded jobs
- outputs: immutable shard manifest, hashes, failure log and restart marker

## Reproducibility and fallback rules

- No unpinned source installation is permitted for final scoring.
- Model revisions and licences are recorded before download.
- Model caches are project-scoped and included in storage accounting.
- Jobs are requeue-safe and never overwrite a completed immutable run.
- Failure, timeout and out-of-memory states remain in the run ledger.
- If VRAM is insufficient, the response order is: reduce batch size; use supported quantization; reduce context/variant subset; select a smaller predeclared model cell. The benchmark contract is not changed silently.
- Optional adaptation is cancelled before required dataset or baseline work is reduced.
