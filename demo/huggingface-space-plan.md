# Hugging Face Space Architecture

Purpose:

- Provide an interactive public stored-record validation of Semantic XAIBIM examples.
- Show reduced public predictions.
- Show aggregated metrics.
- Explain PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES.
- Avoid exposing raw training workspaces or model adapters.

Initial implementation can use Gradio with static JSONL examples.

## Canonical Replay gateway

- https://huggingface.co/spaces/XAIBIM/semantic-xaibim-replay

## Verified Replay runtime

- https://huggingface.co/spaces/bimaiblend/semantic-xaibim-replay

## Canonical Harness gateway

- https://huggingface.co/spaces/XAIBIM/semantic-xaibim-harness

## Verified Harness runtime

- https://huggingface.co/spaces/bimaiblend/semantic-xaibim-harness

## Operational mode

- canonical gateways are static public entry points;
- verified runtimes are Gradio implementations;
- inference disabled;
- no deletion or redeployment in this phase.
