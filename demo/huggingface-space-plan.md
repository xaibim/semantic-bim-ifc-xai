# Hugging Face Space Architecture

Purpose:

- Provide an interactive public stored-record validation of Semantic XAIBIM examples.
- Show reduced public predictions.
- Show aggregated metrics.
- Explain PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES.
- Avoid exposing raw training workspaces or model adapters.

The repository source packages use Gradio with committed public JSONL examples. The registered runtime endpoints are not treated as equivalent to those packages until the deployment manifest records matching commits, hashes and post-deployment self-tests.
`Replay` is the historical Space name. The runtime displays and validates
stored records; inference is disabled.

## Canonical Replay gateway

- https://huggingface.co/spaces/XAIBIM/semantic-xaibim-replay

## Registered Replay runtime endpoint

- https://huggingface.co/spaces/bimaiblend/semantic-xaibim-replay

## Canonical Harness gateway

- https://huggingface.co/spaces/XAIBIM/semantic-xaibim-harness

## Registered Harness runtime endpoint

- https://huggingface.co/spaces/bimaiblend/semantic-xaibim-harness

## Operational mode

- canonical gateways are static public entry points;
- bimaiblend URLs are registered interactive runtime endpoints;
- inference is disabled in the repository source packages;
- remote artifact equivalence is pending;
- no availability guarantee.
