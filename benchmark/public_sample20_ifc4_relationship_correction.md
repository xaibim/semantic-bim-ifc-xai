# Public sample20 IFC4 relationship correction

## Scope

- frozen sample20 fixture;
- correction of six schema-incompatible pairs;
- no live inference;
- no real IFC instance validation;
- no IFC certification;
- no broad semantic-task suitability claim.

## Source

- parent commit: `24da422a7570813041ffcb1e75a1e6bce7aae1f7`
- source JSONL SHA-256: `016ebda71cf67ca1d09def86facdb6d9b4d2bdb2cd1728ac1229854a234accc0`
- fixture correction commit: `2b8b568b33e5a6852f6353499c9233771ac3c6c2`
- corrected JSONL SHA-256: `2c0f0c331e79924700e58e2579d35facc65d86ef76e971dbc9593641b98455aa`
- IFC schema: `IFC4`
- IfcOpenShell: `0.8.5`

## Decisions

| sample_id | ifc_class | previous_required_relationships | final_required_relationships | previous_relation_observed | final_relation_observed | decision |
| --- | --- | --- | --- | --- | --- | --- |
| `21129edbbd73ebef` | `IfcSpace` | `["IfcRelContainedInSpatialStructure","IfcRelConnectsElements"]` | `["IfcRelContainedInSpatialStructure","IfcRelSpaceBoundary"]` | `IfcRelContainedInSpatialStructure` | `IfcRelContainedInSpatialStructure` | Added `IfcRelSpaceBoundary` while preserving the observed containment relation. |
| `f72f31f4c063475b` | `IfcSpace` | `["IfcRelFillsElement"]` | `["IfcRelSpaceBoundary"]` | `IfcRelFillsElement` | `IfcRelSpaceBoundary` | Replaced unsupported fill relation with `IfcRelSpaceBoundary`. |
| `23dad325e1a64458` | `IfcAsset` | `["IfcRelFillsElement"]` | `["IfcRelAssignsToGroup"]` | `IfcRelFillsElement` | `IfcRelAssignsToGroup` | Replaced incompatible fill relation with `IfcRelAssignsToGroup`. |
| `ee5057a4b7f15e3c` | `IfcSystem` | `["IfcRelConnectsElements","IfcRelVoidsElement"]` | `["IfcRelAssignsToGroup"]` | `IfcRelConnectsElements` | `IfcRelAssignsToGroup` | Collapsed two incompatible relations into one schema-compatible group assignment. |
| `45f540e38ef9fe81` | `IfcZone` | `["IfcRelConnectsElements"]` | `["IfcRelAssignsToGroup"]` | `IfcRelConnectsElements` | `IfcRelAssignsToGroup` | Replaced incompatible connection relation with `IfcRelAssignsToGroup`. |

## Pair-count change

- previous record-relationship pairs: 37;
- corrected record-relationship pairs: 36;
- removed schema-incompatible pairs: 6;
- introduced schema-compatible pairs: 5;
- no unsupported second relationship was added to `IfcSystem`.

## Final schema state

- exact inverse endpoints: 31;
- inherited-supertype compatible: 5;
- schema-compatible total: 36;
- schema-incompatible: 0.

## Boundary

"The correction removes the six IFC4 schema-incompatible pairs identified by
the subtype-aware audit. It does not prove that every remaining relationship is
present in a real model, sufficient as evidence, or universally suitable for
the associated professional task."
