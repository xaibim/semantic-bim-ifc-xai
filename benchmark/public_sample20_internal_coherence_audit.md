# Public sample20 internal coherence correction

## Scope

- frozen public sample20 fixture;
- stored-record internal consistency;
- no live model inference;
- no IFC certification;
- no relationship applicability validation;
- no geometry validation;
- no evidence-source verification.

## Source state

- source commit:
  f295ae1ada020a35b975141c75d2d40418624a71
- source JSONL SHA-256:
  59515dff04c4a32f33b8b65d9a97fcab2a64ead95507d4098cc800b7a8344d5d

## Findings

- five canonical value-mode mismatches;
- two misleading expected-negative error codes;
- two expected-negative records containing incompatible required_psets;
- zero model/reference mismatches before correction.

## Correction table

| sample_id | field | previous | final | rationale |
| --- | --- | --- | --- | --- |
| 048b754023b7b6b4 | canonical_check.value_mode | PREVIEW | PROPOSAL | Make the canonical check coherent with the stored model/reference fixture. |
| 6ebb6c9ea431c6a7 | canonical_check.value_mode | PREVIEW | PROPOSAL | Make the canonical check coherent with the stored model/reference fixture. |
| f84721ef28e281d1 | canonical_check.value_mode | PREVIEW | PROPOSAL | Make the canonical check coherent with the stored model/reference fixture. |
| 3dab4b257ae52bfc | canonical_check.value_mode | PREVIEW | PROPOSAL | Make the canonical check coherent with the stored model/reference fixture. |
| 8f91faebc05dd115 | canonical_check.value_mode | PREVIEW | PROPOSAL | Make the canonical check coherent with the stored model/reference fixture. |
| ee5057a4b7f15e3c | required_psets | ["Pset_WallCommon", "Pset_MaterialCommon", "Pset_QuantityTakeOff"] | [] | Remove incompatible property-set content from the operational-scope rejection. |
| 45f540e38ef9fe81 | required_psets | ["Pset_QuantityTakeOff", "Pset_MaterialCommon"] | [] | Remove incompatible property-set content from the operational-scope rejection. |
| ee5057a4b7f15e3c | canonical_check.errors | ["ifc_class_forbidden_abstract_or_domain"] | ["ifc_class_out_of_operation_scope"] | Replace the misleading canonical error with the operational-scope rejection code. |
| 45f540e38ef9fe81 | canonical_check.errors | ["ifc_class_forbidden_abstract_or_domain"] | ["ifc_class_out_of_operation_scope"] | Replace the misleading canonical error with the operational-scope rejection code. |

## Interpretation

"The correction improves stored-fixture internal coherence. It does not
establish broad IFC semantic validity, relationship applicability, source
grounding, model performance or AECO generalization."

## Final state

- model/reference equality preserved;
- canonical class equality verified;
- canonical value-mode equality verified;
- expected-negative operational-scope error verified;
- aggregate record counts and value-mode distribution unchanged;
- relationship applicability remains pending a separate audit.
