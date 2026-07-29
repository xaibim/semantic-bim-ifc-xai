# Human review and operational risk matrix

## Human-review protocol

### Eligibility and roles

A BIM/IFC reviewer must have documented BIM/IFC research or professional experience appropriate to the reviewed task family. Reviewers do not validate outside their competence. The technical executor may curate data but may not unilaterally adjudicate a disagreement in which they produced the disputed record.

### Coverage

- Stratified double review: 10% of the planned dataset, sampled by task family, complexity, discipline, language subset and expected-positive/negative state.
- Mandatory double review: all high-risk mutation-related cases, all professional-sufficiency claims, all unresolved catalogue mappings and all reviewer disagreements.
- Single review plus automated gates: remaining low-risk synthetic records.

### Agreement and adjudication

For two reviewers, categorical agreement is reported with Cohen's kappa and raw percentage agreement, including confidence intervals where feasible. A kappa below 0.80 in any material stratum triggers guideline revision, reviewer calibration and recoding of the affected stratum. Disagreements are resolved by a third eligible adjudicator or by consensus with a documented rationale. No record enters the frozen evaluation set with an unresolved material disagreement.

### Release gates

- automated contract gates pass;
- rights/privacy state permits the intended use;
- review requirement is satisfied;
- disagreement state is resolved;
- root-case leakage checks pass;
- content and review manifests are hashed.

## Operational risk matrix

| Risk | Trigger/threshold | Mitigation | Protected priority |
| --- | --- | --- | --- |
| Platform/library incompatibility | import or smoke-test failure | use versioned x86 SIF; fallback GPU platform; remove unsupported optional dependency | dataset and A/B/C baselines |
| ARM incompatibility | compiled wheel/container fails | do not use ARM; request/retain x86/GPU allocation | reproducibility |
| VRAM exhaustion | repeated OOM at frozen batch/context | batch 1; supported quantization; smaller predeclared model; shorter bounded subset | common output contract |
| Excessive latency | p95 exceeds frozen envelope | shard jobs; reduce optional variants; remove slow optional model cell | required baselines |
| High job failure rate | >5% infrastructure failures | checkpoint; bounded jobs; requeue; platform support ticket; preserve failure ledger | denominators and audit |
| Dataset production delay | <70% planned records by end M3 | freeze minimum scenario; prioritise task/discipline balance over volume | quality over scale |
| Reviewer capacity shortfall | mandatory double review cannot be completed | reduce ceiling/planned scale; retain minimum scenario; postpone professional-sufficiency claims | review quality |
| Low inter-reviewer agreement | kappa <0.80 | revise manual; calibration round; recode affected stratum | semantic validity |
| Duplicate or leakage failure | material cross-split similarity | regroup root cases; rebuild splits; invalidate contaminated runs | frozen evaluation |
| Rights/privacy uncertainty | missing licence or sensitive content | controlled use only; exclude from public release/training as required | legal/ethical compliance |
| Storage growth above envelope | projected use >90% quota | prune caches; compress immutable outputs; cancel optional checkpoints | raw evidence and manifests |
| Resource shortfall | remaining allocation cannot complete plan | cancel QLoRA and optional D-G cells; complete dataset and A/B/C | core deliverables |
| Remote CI unavailable | no checks for final SHA | preserve local test logs, bundle/hash and explicit limitation | honest evidence |
| Public endpoint unavailable | anonymous runtime cannot be verified | static manifest, screenshots/logs where lawful, canonical repository evidence | reproducibility |

## Invariants

- No AI output is certified or professionally approved by the artifact.
- No optional model experiment may consume capacity needed for dataset quality, review or required baselines.
- No failed run is silently removed.
- No public release occurs without rights, privacy, licence, hash and limitation metadata.
