# benchmark/qlora

This folder contains the sanitized aggregate evidence from a preliminary
computational feasibility experiment for QLoRA fine-tuning of
Qwen2.5-7B-Instruct on the structured Semantic BIM/IFC output task.

## Contents

| File | Purpose |
|---|---|
| [XAIBIM_QWEN25_7B_QLORA_PRELIMINARY_RESULTS.md](XAIBIM_QWEN25_7B_QLORA_PRELIMINARY_RESULTS.md) | Full experiment report: configuration, compute, metrics, distributions, limitations |
| [xaibim_qwen25_7b_qlora_preliminary_public_results.json](xaibim_qwen25_7b_qlora_preliminary_public_results.json) | Machine-readable aggregate results with derived calculations |
| [verify_qlora_public_metrics.py](../../scripts/verify_qlora_public_metrics.py) | Deterministic CPU verifier - checks aggregate structure, bounded values, distribution totals and derived compute arithmetic |

## Public Kaggle Notebook

<https://www.kaggle.com/code/xaibim/semantic-bim-ifc-xai>

## Public/Private Boundary

**Public (here):**

- aggregate metrics and compute measurements;
- formulas and derived calculations;
- model and hyperparameter identifiers;
- dataset and adapter hashes;
- test distribution counts;
- methodological limitations;
- Kaggle notebook link.

**Private (not in this repository):**

- private dataset rows and raw prompts;
- expected outputs and raw predictions;
- adapter weights and checkpoint files;
- private ZIP archives.

See [docs/public_boundary.md](../../docs/public_boundary.md) for the full
public/private boundary map.

## Run Verifier

```bash
python scripts/verify_qlora_public_metrics.py
```

Expected output on success:

```
QLORA_PUBLIC_AGGREGATE_SELF_CONSISTENCY_VALID
```

The script checks aggregate structure, bounded values, distribution totals and
derived compute arithmetic. It does not reproduce the private experiment and
does not independently recompute empirical held-out scores. It does not prove
superiority. It does not prove generalization. The score aggregates come from
a private controlled execution and the raw predictions are not distributed.
Exit code 1 on any discrepancy.

## Scientific Scope

This is a **preliminary computational feasibility experiment**, not a final
benchmark or production-readiness assessment. Results reflect controlled
held-out target agreement on a bounded private dataset. No broad AECO
generalization is claimed. The verifier does not reproduce training and a
PASS does not demonstrate superiority or generalization.
