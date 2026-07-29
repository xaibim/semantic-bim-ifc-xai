# Resource calibration

This file is the readable companion to [`resource_calibration.json`](resource_calibration.json).

## Evidence classes

- **Measured prior evidence:** the bounded private 1,000-record QLoRA pilot, exposed only through aggregate measurements.
- **Planning assumptions:** workload dimensions and conservative per-case latency used to construct minimum, planned and ceiling envelopes.
- **Required future measurements:** M1 CPU and GPU microbenchmarks on the allocated platform.

The pilot measured 2.1107 effective GPU.h, 4.2214 allocated GPU.h and 6.6287 GB peak allocated VRAM. Those values establish that the earlier workflow executed; they do not establish performance on a different GPU, workload or dataset.

## Machine-readable calculations

The JSON records formulas, units, measured inputs, assumed inputs, scenario outputs, required measurements and stop rules. Any revised calibration must preserve the previous version and identify the hardware, software environment and run-manifest hashes.

## Interpretation rule

A scenario is scientifically usable only when every material assumed input is either replaced by a measured value or retained with an explicit sensitivity range. The maximum scenario is not an objective and is never activated solely to consume capacity.
