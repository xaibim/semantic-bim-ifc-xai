# Hugging Face Space Architecture

Purpose:

- Provide an interactive public stored-record validation of Semantic XAIBIM examples.
- Show reduced public predictions.
- Show aggregated metrics.
- Explain PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES.
- Avoid exposing raw training workspaces or model adapters.

The repository source packages use Gradio with committed public JSONL examples. The
canonical public entry points are the `XAIBIM` Spaces. Equivalence is not claimed
until the deployment manifest records matching commits, hashes and post-deployment
self-tests.
`Replay` is the historical Space name. The runtime displays and validates
stored records; inference is disabled.

## Canonical Replay Space

- https://huggingface.co/spaces/XAIBIM/semantic-xaibim-replay

## Canonical Harness Space

- https://huggingface.co/spaces/XAIBIM/semantic-xaibim-harness

## Operational mode

- canonical XAIBIM Spaces are static public entry points;
- inference is disabled in the repository source packages;
- remote artifact equivalence is pending;
- no availability guarantee.
