# Space Notes

This folder contains the files intended for a future Hugging Face Space.

Current mode:

- Local preparation only.
- No online Space created yet.
- No credentials required.
- No model inference.
- No adapters.
- No checkpoints.
- No private BIM data.

Publication plan:

1. Review these files locally.
2. Commit in semantic repo.
3. Push branch.
4. Open PR.
5. After merge, copy or push this folder into a Hugging Face Space repository.

- README.md
- app.py
- requirements.txt
- sample20_public_predictions.jsonl
- schema_public_sample20_v2.json

## Published instance

- Space: https://huggingface.co/spaces/XAIBIM/semantic-xaibim-replay
- Direct app: https://XAIBIM-semantic-xaibim-replay.hf.space
- Status: published and running

---

## Public Sample and Demo Note

The interactive application in this folder conforms to the strict public sample20 v2 contract using JSON Schema Draft 2020-12 (defined in `schema_public_sample20_v2.json`).

Expected metrics are:
- **Record Count**: 20 records;
- **Valid Cases**: 18 valid cases;
- **Expected Rejections**: 2 expected canonical rejections;
- **Canonical Validation Rate**: `canonical_validation_rate = 0.9`;
- **Expectation Met Rate**: `expectation_met_rate = 1.0`;
- **Status**: `status = PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`.

All 1.0 metrics indicate internal agreement with the stored synthetic reference, not a final benchmark, production deployment, or certification. This is an academic research artifact, not a final benchmark, not a product, and does not claim production readiness or certification.

