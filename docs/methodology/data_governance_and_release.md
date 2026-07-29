# Data governance and controlled release

## Purpose

This protocol governs origin, rights, privacy, storage, retention, access, dataset use and public release for semantic BIM/IFC research records and related artifacts.

## Data classes

| Class | Typical content | Access | Public release |
| --- | --- | --- | --- |
| S0 - synthetic public | Generated prompts, records and small fixtures with no real project data | Public after QA | Permitted under declared licence |
| S1 - sanitized controlled | Derived or transformed records that passed privacy and rights review | Project team; selected release | Only approved fields/aggregates |
| S2 - protected research | Real IFC files, contractual material, private prompts/predictions | Named project members | Not public by default |
| S3 - restricted/sensitive | Personal data, confidential or third-party restricted content | Minimum authorised group | Prohibited unless a new lawful basis and approval exist |

## Source and rights register

Every source or source family records: source identifier; owner/provider; acquisition date; licence or permission; permitted research use; permitted derivatives; permitted public fields; retention requirement; responsible person; and evidence of approval. A missing or ambiguous right defaults to controlled use and blocks public release, not internal audit.

## Provenance

Every dataset record has a stable record identifier, root-case identifier, variant identifier, source class, transformation history, reviewer state and content hash. Synthetic generation is labelled as synthetic. Sanitization does not erase the relationship to the controlled provenance record.

## Privacy and confidentiality gates

- Scan for personal identifiers, credentials, private paths, client/project identifiers and contractual text.
- Reject secrets and authentication material from datasets and logs.
- Store raw protected sources separately from derived records.
- Do not publish raw private prompts, private model outputs, adapters, checkpoints or record-level protected predictions.
- Record every sanitization action and reviewer decision.

## Dataset-use states

- `TRAIN_CANDIDATE`: eligible only after rights, privacy, QA, dedupe and leakage gates.
- `VALIDATION_CANDIDATE`: eligible for development validation; never used for final scoring after freeze.
- `TEST_FROZEN`: immutable test unit grouped by root case.
- `EVAL_FROZEN`: immutable final evaluation unit grouped by root case.
- `EVAL_ONLY`: usable for error analysis/evaluation but excluded from training.
- `REQUIRES_CORRECTION`: not used until corrected and re-reviewed.
- `EXCLUDED_FROM_TRAINING`: retained only for audit or negative analysis.

## Split and leakage controls

Variants from a root case remain in one split. Duplicate and near-duplicate checks run before and after splitting. Retrieval corpora are versioned and audited against test/evaluation targets. Prompt templates and generated variants are checked for target leakage. Any post-freeze correction produces a new dataset version and a documented impact analysis.

## Retention and backup

Retention follows the institutional data-management plan, source agreements and legal requirements. The working default is five years after project closure when no stricter or shorter obligation applies. Protected sources use access-controlled storage, periodic integrity checks and at least one independent backup. Public releases are preserved through versioned repositories or institutional archives where available.

## Release gate

A public release requires: rights/publicability decision; privacy scan; QA status; licence; provenance boundary; content hashes; version/date; known limitations; responsible approval; and link audit. Public releases contain the minimum necessary data. Controlled or restricted material remains outside the public repository.

## Roles

- Technical executor: maintains provenance, processing, hashes and release package.
- Data curator: applies record-level QA and source classification.
- BIM/IFC reviewer: reviews semantic and IFC mappings.
- Adjudicator: resolves documented disagreements.
- Principal Investigator or delegated institutional authority: approves controlled public release.
