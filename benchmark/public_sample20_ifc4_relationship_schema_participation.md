# Public sample20 IFC4 subtype-aware relationship schema-participation audit

## Scope

- frozen public sample20;
- IFC4 schema participation only;
- subtype-aware classification of relationship endpoints;
- no semantic task-alignment conclusion;
- no real IFC instance validation;
- no certification;
- no correction authorized by this report.

## Source

- commit: `2b8b568b33e5a6852f6353499c9233771ac3c6c2`
- source JSONL: `sample20/sample20_public_records.jsonl`
- LF-normalized SHA-256: `2c0f0c331e79924700e58e2579d35facc65d86ef76e971dbc9593641b98455aa`
- hash contract: `SHA-256 over UTF-8 source bytes after CRLF and CR line endings are normalized to LF.`
- three public JSONL copies byte-identical: `true`
- IfcOpenShell version: `0.8.5`
- IFC schema: `IFC4`

## Summary

| field | value |
| --- | --- |
| `record_count` | `20` |
| `positive_count` | `18` |
| `expected_negative_count` | `2` |
| `unique_ifc_class_count` | `11` |
| `unique_relationship_count` | `10` |
| `record_relationship_pair_count` | `36` |
| `evidence_relation_declared_count` | `20` |
| `exact_inverse_endpoint_count` | `31` |
| `inherited_supertype_compatible_count` | `5` |
| `schema_compatible_count` | `36` |
| `schema_incompatible_count` | `0` |

## Relationship catalogue

| relationship | declaration_exists | is_ifc_relationship | is_abstract | supertype_chain | forward_attributes |
| --- | --- | --- | --- | --- | --- |
| IfcRelAggregates | true | true | CONCRETE_RELATIONSHIP | ["IfcRelAggregates", "IfcRelDecomposes", "IfcRelationship", "IfcRoot"] | ["GlobalId", "OwnerHistory", "Name", "Description", "RelatingObject", "RelatedObjects"] |
| IfcRelAssignsToGroup | true | true | CONCRETE_RELATIONSHIP | ["IfcRelAssignsToGroup", "IfcRelAssigns", "IfcRelationship", "IfcRoot"] | ["GlobalId", "OwnerHistory", "Name", "Description", "RelatedObjects", "RelatedObjectsType", "RelatingGroup"] |
| IfcRelAssociatesMaterial | true | true | CONCRETE_RELATIONSHIP | ["IfcRelAssociatesMaterial", "IfcRelAssociates", "IfcRelationship", "IfcRoot"] | ["GlobalId", "OwnerHistory", "Name", "Description", "RelatedObjects", "RelatingMaterial"] |
| IfcRelConnectsElements | true | true | CONCRETE_RELATIONSHIP | ["IfcRelConnectsElements", "IfcRelConnects", "IfcRelationship", "IfcRoot"] | ["GlobalId", "OwnerHistory", "Name", "Description", "ConnectionGeometry", "RelatingElement", "RelatedElement"] |
| IfcRelContainedInSpatialStructure | true | true | CONCRETE_RELATIONSHIP | ["IfcRelContainedInSpatialStructure", "IfcRelConnects", "IfcRelationship", "IfcRoot"] | ["GlobalId", "OwnerHistory", "Name", "Description", "RelatedElements", "RelatingStructure"] |
| IfcRelDefinesByProperties | true | true | CONCRETE_RELATIONSHIP | ["IfcRelDefinesByProperties", "IfcRelDefines", "IfcRelationship", "IfcRoot"] | ["GlobalId", "OwnerHistory", "Name", "Description", "RelatedObjects", "RelatingPropertyDefinition"] |
| IfcRelFillsElement | true | true | CONCRETE_RELATIONSHIP | ["IfcRelFillsElement", "IfcRelConnects", "IfcRelationship", "IfcRoot"] | ["GlobalId", "OwnerHistory", "Name", "Description", "RelatingOpeningElement", "RelatedBuildingElement"] |
| IfcRelNests | true | true | CONCRETE_RELATIONSHIP | ["IfcRelNests", "IfcRelDecomposes", "IfcRelationship", "IfcRoot"] | ["GlobalId", "OwnerHistory", "Name", "Description", "RelatingObject", "RelatedObjects"] |
| IfcRelSpaceBoundary | true | true | CONCRETE_RELATIONSHIP | ["IfcRelSpaceBoundary", "IfcRelConnects", "IfcRelationship", "IfcRoot"] | ["GlobalId", "OwnerHistory", "Name", "Description", "RelatingSpace", "RelatedBuildingElement", "ConnectionGeometry", "PhysicalOrVirtualBoundary", "InternalOrExternalBoundary"] |
| IfcRelVoidsElement | true | true | CONCRETE_RELATIONSHIP | ["IfcRelVoidsElement", "IfcRelDecomposes", "IfcRelationship", "IfcRoot"] | ["GlobalId", "OwnerHistory", "Name", "Description", "RelatingBuildingElement", "RelatedOpeningElement"] |

## Record-relationship matrix

| sample_id | case_expectation | semantic_type | ifc_class | relationship | evidence_relation | declaration | abstract | compatibility_state | schema_compatible | exact_inverse_endpoints | inherited_supertype_endpoints | semantic_alignment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4eeac340747306fd | VALID | semantic_enrichment | IfcColumn | IfcRelConnectsElements | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedElement", "inverse_attribute_name": "ConnectedFrom", "relationship_entity": "IfcRelConnectsElements"}, {"forward_attribute_name": "RelatingElement", "inverse_attribute_name": "ConnectedTo", "relationship_entity": "IfcRelConnectsElements"}] | [] | NOT_EVALUATED |
| 4eeac340747306fd | VALID | semantic_enrichment | IfcColumn | IfcRelDefinesByProperties | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "IsDefinedBy", "relationship_entity": "IfcRelDefinesByProperties"}] | [] | NOT_EVALUATED |
| 495a677407a7f05a | VALID | ambiguity_resolution | IfcWall | IfcRelNests | IfcRelNests | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] | [] | NOT_EVALUATED |
| 495a677407a7f05a | VALID | ambiguity_resolution | IfcWall | IfcRelAssignsToGroup | IfcRelNests | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | INHERITED_SUPERTYPE_COMPATIBLE | true | [] | [{"declared_relationship_supertype": "IfcRelAssigns", "forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "HasAssignments"}] | NOT_EVALUATED |
| 1ae42de17ac977f7 | VALID | evidence_generation | IfcBeam | IfcRelVoidsElement | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] | [] | NOT_EVALUATED |
| 1ae42de17ac977f7 | VALID | evidence_generation | IfcBeam | IfcRelFillsElement | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedBuildingElement", "inverse_attribute_name": "FillsVoids", "relationship_entity": "IfcRelFillsElement"}] | [] | NOT_EVALUATED |
| ae47e72e2af2b182 | VALID | evidence_generation | IfcBeam | IfcRelConnectsElements | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedElement", "inverse_attribute_name": "ConnectedFrom", "relationship_entity": "IfcRelConnectsElements"}, {"forward_attribute_name": "RelatingElement", "inverse_attribute_name": "ConnectedTo", "relationship_entity": "IfcRelConnectsElements"}] | [] | NOT_EVALUATED |
| ae47e72e2af2b182 | VALID | evidence_generation | IfcBeam | IfcRelAggregates | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Decomposes", "relationship_entity": "IfcRelAggregates"}, {"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsDecomposedBy", "relationship_entity": "IfcRelAggregates"}] | [] | NOT_EVALUATED |
| 8c0052ccd9bc96e4 | VALID | geometric_validation | IfcPump | IfcRelAssociatesMaterial | IfcRelAssociatesMaterial | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | INHERITED_SUPERTYPE_COMPATIBLE | true | [] | [{"declared_relationship_supertype": "IfcRelAssociates", "forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "HasAssociations"}] | NOT_EVALUATED |
| 8c0052ccd9bc96e4 | VALID | geometric_validation | IfcPump | IfcRelVoidsElement | IfcRelAssociatesMaterial | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] | [] | NOT_EVALUATED |
| 21129edbbd73ebef | VALID | semantic_enrichment | IfcSpace | IfcRelContainedInSpatialStructure | IfcRelContainedInSpatialStructure | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingStructure", "inverse_attribute_name": "ContainsElements", "relationship_entity": "IfcRelContainedInSpatialStructure"}] | [] | NOT_EVALUATED |
| 21129edbbd73ebef | VALID | semantic_enrichment | IfcSpace | IfcRelSpaceBoundary | IfcRelContainedInSpatialStructure | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingSpace", "inverse_attribute_name": "BoundedBy", "relationship_entity": "IfcRelSpaceBoundary"}] | [] | NOT_EVALUATED |
| d2ed814a93840a19 | VALID | element_deletion | IfcFlowTerminal | IfcRelVoidsElement | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] | [] | NOT_EVALUATED |
| d2ed814a93840a19 | VALID | element_deletion | IfcFlowTerminal | IfcRelFillsElement | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedBuildingElement", "inverse_attribute_name": "FillsVoids", "relationship_entity": "IfcRelFillsElement"}] | [] | NOT_EVALUATED |
| fa3bca1c51085557 | VALID | evidence_generation | IfcAirTerminal | IfcRelNests | IfcRelNests | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] | [] | NOT_EVALUATED |
| fa3bca1c51085557 | VALID | evidence_generation | IfcAirTerminal | IfcRelFillsElement | IfcRelNests | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedBuildingElement", "inverse_attribute_name": "FillsVoids", "relationship_entity": "IfcRelFillsElement"}] | [] | NOT_EVALUATED |
| 048b754023b7b6b4 | VALID | element_modification | IfcColumn | IfcRelConnectsElements | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedElement", "inverse_attribute_name": "ConnectedFrom", "relationship_entity": "IfcRelConnectsElements"}, {"forward_attribute_name": "RelatingElement", "inverse_attribute_name": "ConnectedTo", "relationship_entity": "IfcRelConnectsElements"}] | [] | NOT_EVALUATED |
| 048b754023b7b6b4 | VALID | element_modification | IfcColumn | IfcRelAggregates | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Decomposes", "relationship_entity": "IfcRelAggregates"}, {"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsDecomposedBy", "relationship_entity": "IfcRelAggregates"}] | [] | NOT_EVALUATED |
| 5af537f550afd4aa | VALID | ambiguity_resolution | IfcFan | IfcRelContainedInSpatialStructure | IfcRelContainedInSpatialStructure | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedElements", "inverse_attribute_name": "ContainedInStructure", "relationship_entity": "IfcRelContainedInSpatialStructure"}] | [] | NOT_EVALUATED |
| 5af537f550afd4aa | VALID | ambiguity_resolution | IfcFan | IfcRelNests | IfcRelContainedInSpatialStructure | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] | [] | NOT_EVALUATED |
| 6ebb6c9ea431c6a7 | VALID | element_modification | IfcColumn | IfcRelVoidsElement | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] | [] | NOT_EVALUATED |
| 6ebb6c9ea431c6a7 | VALID | element_modification | IfcColumn | IfcRelAssignsToGroup | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | INHERITED_SUPERTYPE_COMPATIBLE | true | [] | [{"declared_relationship_supertype": "IfcRelAssigns", "forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "HasAssignments"}] | NOT_EVALUATED |
| ca455e91ed772fd8 | VALID | recovery_request | IfcColumn | IfcRelVoidsElement | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] | [] | NOT_EVALUATED |
| ca455e91ed772fd8 | VALID | recovery_request | IfcColumn | IfcRelAssignsToGroup | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | INHERITED_SUPERTYPE_COMPATIBLE | true | [] | [{"declared_relationship_supertype": "IfcRelAssigns", "forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "HasAssignments"}] | NOT_EVALUATED |
| ee5057a4b7f15e3c | EXPECTED_CANONICAL_REJECTION | element_deletion | IfcSystem | IfcRelAssignsToGroup | IfcRelAssignsToGroup | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingGroup", "inverse_attribute_name": "IsGroupedBy", "relationship_entity": "IfcRelAssignsToGroup"}] | [] | NOT_EVALUATED |
| f72f31f4c063475b | VALID | recovery_request | IfcSpace | IfcRelSpaceBoundary | IfcRelSpaceBoundary | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingSpace", "inverse_attribute_name": "BoundedBy", "relationship_entity": "IfcRelSpaceBoundary"}] | [] | NOT_EVALUATED |
| f84721ef28e281d1 | VALID | relationship_inference | IfcSpace | IfcRelAggregates | IfcRelAggregates | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Decomposes", "relationship_entity": "IfcRelAggregates"}, {"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsDecomposedBy", "relationship_entity": "IfcRelAggregates"}] | [] | NOT_EVALUATED |
| f84721ef28e281d1 | VALID | relationship_inference | IfcSpace | IfcRelContainedInSpatialStructure | IfcRelAggregates | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingStructure", "inverse_attribute_name": "ContainsElements", "relationship_entity": "IfcRelContainedInSpatialStructure"}] | [] | NOT_EVALUATED |
| 23dad325e1a64458 | VALID | element_deletion | IfcAsset | IfcRelAssignsToGroup | IfcRelAssignsToGroup | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingGroup", "inverse_attribute_name": "IsGroupedBy", "relationship_entity": "IfcRelAssignsToGroup"}] | [] | NOT_EVALUATED |
| 3dab4b257ae52bfc | VALID | pset_assignment | IfcFlowTerminal | IfcRelNests | IfcRelNests | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] | [] | NOT_EVALUATED |
| 3dab4b257ae52bfc | VALID | pset_assignment | IfcFlowTerminal | IfcRelFillsElement | IfcRelNests | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedBuildingElement", "inverse_attribute_name": "FillsVoids", "relationship_entity": "IfcRelFillsElement"}] | [] | NOT_EVALUATED |
| 45f540e38ef9fe81 | EXPECTED_CANONICAL_REJECTION | element_deletion | IfcZone | IfcRelAssignsToGroup | IfcRelAssignsToGroup | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingGroup", "inverse_attribute_name": "IsGroupedBy", "relationship_entity": "IfcRelAssignsToGroup"}] | [] | NOT_EVALUATED |
| 8f91faebc05dd115 | VALID | material_assignment | IfcAsset | IfcRelDefinesByProperties | IfcRelDefinesByProperties | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "IsDefinedBy", "relationship_entity": "IfcRelDefinesByProperties"}] | [] | NOT_EVALUATED |
| 8f91faebc05dd115 | VALID | material_assignment | IfcAsset | IfcRelNests | IfcRelDefinesByProperties | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] | [] | NOT_EVALUATED |
| 7f1ea524d9fdbdcb | VALID | ambiguity_resolution | IfcColumn | IfcRelAggregates | IfcRelAggregates | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | EXACT_INVERSE_ENDPOINT | true | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Decomposes", "relationship_entity": "IfcRelAggregates"}, {"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsDecomposedBy", "relationship_entity": "IfcRelAggregates"}] | [] | NOT_EVALUATED |
| 7f1ea524d9fdbdcb | VALID | ambiguity_resolution | IfcColumn | IfcRelAssociatesMaterial | IfcRelAggregates | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | INHERITED_SUPERTYPE_COMPATIBLE | true | [] | [{"declared_relationship_supertype": "IfcRelAssociates", "forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "HasAssociations"}] | NOT_EVALUATED |

## Exact inverse endpoints

| sample_id | ifc_class | relationship | exact_inverse_endpoints |
| --- | --- | --- | --- |
| 4eeac340747306fd | IfcColumn | IfcRelConnectsElements | [{"forward_attribute_name": "RelatedElement", "inverse_attribute_name": "ConnectedFrom", "relationship_entity": "IfcRelConnectsElements"}, {"forward_attribute_name": "RelatingElement", "inverse_attribute_name": "ConnectedTo", "relationship_entity": "IfcRelConnectsElements"}] |
| 4eeac340747306fd | IfcColumn | IfcRelDefinesByProperties | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "IsDefinedBy", "relationship_entity": "IfcRelDefinesByProperties"}] |
| 495a677407a7f05a | IfcWall | IfcRelNests | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] |
| 1ae42de17ac977f7 | IfcBeam | IfcRelVoidsElement | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] |
| 1ae42de17ac977f7 | IfcBeam | IfcRelFillsElement | [{"forward_attribute_name": "RelatedBuildingElement", "inverse_attribute_name": "FillsVoids", "relationship_entity": "IfcRelFillsElement"}] |
| ae47e72e2af2b182 | IfcBeam | IfcRelConnectsElements | [{"forward_attribute_name": "RelatedElement", "inverse_attribute_name": "ConnectedFrom", "relationship_entity": "IfcRelConnectsElements"}, {"forward_attribute_name": "RelatingElement", "inverse_attribute_name": "ConnectedTo", "relationship_entity": "IfcRelConnectsElements"}] |
| ae47e72e2af2b182 | IfcBeam | IfcRelAggregates | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Decomposes", "relationship_entity": "IfcRelAggregates"}, {"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsDecomposedBy", "relationship_entity": "IfcRelAggregates"}] |
| 8c0052ccd9bc96e4 | IfcPump | IfcRelVoidsElement | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] |
| 21129edbbd73ebef | IfcSpace | IfcRelContainedInSpatialStructure | [{"forward_attribute_name": "RelatingStructure", "inverse_attribute_name": "ContainsElements", "relationship_entity": "IfcRelContainedInSpatialStructure"}] |
| 21129edbbd73ebef | IfcSpace | IfcRelSpaceBoundary | [{"forward_attribute_name": "RelatingSpace", "inverse_attribute_name": "BoundedBy", "relationship_entity": "IfcRelSpaceBoundary"}] |
| d2ed814a93840a19 | IfcFlowTerminal | IfcRelVoidsElement | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] |
| d2ed814a93840a19 | IfcFlowTerminal | IfcRelFillsElement | [{"forward_attribute_name": "RelatedBuildingElement", "inverse_attribute_name": "FillsVoids", "relationship_entity": "IfcRelFillsElement"}] |
| fa3bca1c51085557 | IfcAirTerminal | IfcRelNests | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] |
| fa3bca1c51085557 | IfcAirTerminal | IfcRelFillsElement | [{"forward_attribute_name": "RelatedBuildingElement", "inverse_attribute_name": "FillsVoids", "relationship_entity": "IfcRelFillsElement"}] |
| 048b754023b7b6b4 | IfcColumn | IfcRelConnectsElements | [{"forward_attribute_name": "RelatedElement", "inverse_attribute_name": "ConnectedFrom", "relationship_entity": "IfcRelConnectsElements"}, {"forward_attribute_name": "RelatingElement", "inverse_attribute_name": "ConnectedTo", "relationship_entity": "IfcRelConnectsElements"}] |
| 048b754023b7b6b4 | IfcColumn | IfcRelAggregates | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Decomposes", "relationship_entity": "IfcRelAggregates"}, {"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsDecomposedBy", "relationship_entity": "IfcRelAggregates"}] |
| 5af537f550afd4aa | IfcFan | IfcRelContainedInSpatialStructure | [{"forward_attribute_name": "RelatedElements", "inverse_attribute_name": "ContainedInStructure", "relationship_entity": "IfcRelContainedInSpatialStructure"}] |
| 5af537f550afd4aa | IfcFan | IfcRelNests | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] |
| 6ebb6c9ea431c6a7 | IfcColumn | IfcRelVoidsElement | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] |
| ca455e91ed772fd8 | IfcColumn | IfcRelVoidsElement | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] |
| ee5057a4b7f15e3c | IfcSystem | IfcRelAssignsToGroup | [{"forward_attribute_name": "RelatingGroup", "inverse_attribute_name": "IsGroupedBy", "relationship_entity": "IfcRelAssignsToGroup"}] |
| f72f31f4c063475b | IfcSpace | IfcRelSpaceBoundary | [{"forward_attribute_name": "RelatingSpace", "inverse_attribute_name": "BoundedBy", "relationship_entity": "IfcRelSpaceBoundary"}] |
| f84721ef28e281d1 | IfcSpace | IfcRelAggregates | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Decomposes", "relationship_entity": "IfcRelAggregates"}, {"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsDecomposedBy", "relationship_entity": "IfcRelAggregates"}] |
| f84721ef28e281d1 | IfcSpace | IfcRelContainedInSpatialStructure | [{"forward_attribute_name": "RelatingStructure", "inverse_attribute_name": "ContainsElements", "relationship_entity": "IfcRelContainedInSpatialStructure"}] |
| 23dad325e1a64458 | IfcAsset | IfcRelAssignsToGroup | [{"forward_attribute_name": "RelatingGroup", "inverse_attribute_name": "IsGroupedBy", "relationship_entity": "IfcRelAssignsToGroup"}] |
| 3dab4b257ae52bfc | IfcFlowTerminal | IfcRelNests | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] |
| 3dab4b257ae52bfc | IfcFlowTerminal | IfcRelFillsElement | [{"forward_attribute_name": "RelatedBuildingElement", "inverse_attribute_name": "FillsVoids", "relationship_entity": "IfcRelFillsElement"}] |
| 45f540e38ef9fe81 | IfcZone | IfcRelAssignsToGroup | [{"forward_attribute_name": "RelatingGroup", "inverse_attribute_name": "IsGroupedBy", "relationship_entity": "IfcRelAssignsToGroup"}] |
| 8f91faebc05dd115 | IfcAsset | IfcRelDefinesByProperties | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "IsDefinedBy", "relationship_entity": "IfcRelDefinesByProperties"}] |
| 8f91faebc05dd115 | IfcAsset | IfcRelNests | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] |
| 7f1ea524d9fdbdcb | IfcColumn | IfcRelAggregates | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Decomposes", "relationship_entity": "IfcRelAggregates"}, {"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsDecomposedBy", "relationship_entity": "IfcRelAggregates"}] |

## Inherited supertype-compatible rows

| sample_id | ifc_class | relationship | inherited_supertype_endpoints |
| --- | --- | --- | --- |
| 495a677407a7f05a | IfcWall | IfcRelAssignsToGroup | [{"declared_relationship_supertype": "IfcRelAssigns", "forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "HasAssignments"}] |
| 8c0052ccd9bc96e4 | IfcPump | IfcRelAssociatesMaterial | [{"declared_relationship_supertype": "IfcRelAssociates", "forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "HasAssociations"}] |
| 6ebb6c9ea431c6a7 | IfcColumn | IfcRelAssignsToGroup | [{"declared_relationship_supertype": "IfcRelAssigns", "forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "HasAssignments"}] |
| ca455e91ed772fd8 | IfcColumn | IfcRelAssignsToGroup | [{"declared_relationship_supertype": "IfcRelAssigns", "forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "HasAssignments"}] |
| 7f1ea524d9fdbdcb | IfcColumn | IfcRelAssociatesMaterial | [{"declared_relationship_supertype": "IfcRelAssociates", "forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "HasAssociations"}] |

## Schema-incompatible rows

| sample_id | ifc_class | relationship | exact_inverse_endpoints | inherited_supertype_endpoints |
| --- | --- | --- | --- | --- |

## Interpretation

"This audit identifies IFC4 schema-level declarations and inverse participation endpoints. It does not establish that a relationship is suitable for the professional task, present in a real IFC model, correctly instantiated, or sufficient as semantic evidence."
