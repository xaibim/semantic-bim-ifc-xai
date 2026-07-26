# Public sample20 IFC4 relationship schema-participation audit

## Scope

- frozen public sample20;
- IFC4 schema participation only;
- no semantic task-alignment conclusion;
- no real IFC instance validation;
- no certification;
- no correction authorized by this report.

## Source

- commit: `b00dc9ce6a8a96309fb77472eabff9a90d0d50d7`
- source JSONL: `sample20/sample20_public_records.jsonl`
- SHA-256: `016ebda71cf67ca1d09def86facdb6d9b4d2bdb2cd1728ac1229854a234accc0`
- IfcOpenShell version: `0.8.5`
- IFC schema: `IFC4`

## Summary

| field | value |
| --- | --- |
| `record_count` | `20` |
| `positive_count` | `18` |
| `expected_negative_count` | `2` |
| `unique_ifc_class_count` | `11` |
| `unique_relationship_count` | `9` |
| `record_relationship_pair_count` | `37` |
| `evidence_relation_declared_count` | `20` |
| `schema_inverse_participation_found_count` | `26` |
| `schema_inverse_participation_not_found_count` | `11` |

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
| IfcRelVoidsElement | true | true | CONCRETE_RELATIONSHIP | ["IfcRelVoidsElement", "IfcRelDecomposes", "IfcRelationship", "IfcRoot"] | ["GlobalId", "OwnerHistory", "Name", "Description", "RelatingBuildingElement", "RelatedOpeningElement"] |

## Record-relationship matrix

| sample_id | case_expectation | semantic_type | ifc_class | relationship | evidence_relation | declaration | abstract | inverse_participation | inverse_endpoints | semantic_alignment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4eeac340747306fd | VALID | semantic_enrichment | IfcColumn | IfcRelConnectsElements | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedElement", "inverse_attribute_name": "ConnectedFrom", "relationship_entity": "IfcRelConnectsElements"}, {"forward_attribute_name": "RelatingElement", "inverse_attribute_name": "ConnectedTo", "relationship_entity": "IfcRelConnectsElements"}] | NOT_EVALUATED |
| 4eeac340747306fd | VALID | semantic_enrichment | IfcColumn | IfcRelDefinesByProperties | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "IsDefinedBy", "relationship_entity": "IfcRelDefinesByProperties"}] | NOT_EVALUATED |
| 495a677407a7f05a | VALID | ambiguity_resolution | IfcWall | IfcRelNests | IfcRelNests | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] | NOT_EVALUATED |
| 495a677407a7f05a | VALID | ambiguity_resolution | IfcWall | IfcRelAssignsToGroup | IfcRelNests | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_NOT_FOUND | [] | NOT_EVALUATED |
| 1ae42de17ac977f7 | VALID | evidence_generation | IfcBeam | IfcRelVoidsElement | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] | NOT_EVALUATED |
| 1ae42de17ac977f7 | VALID | evidence_generation | IfcBeam | IfcRelFillsElement | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedBuildingElement", "inverse_attribute_name": "FillsVoids", "relationship_entity": "IfcRelFillsElement"}] | NOT_EVALUATED |
| ae47e72e2af2b182 | VALID | evidence_generation | IfcBeam | IfcRelConnectsElements | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedElement", "inverse_attribute_name": "ConnectedFrom", "relationship_entity": "IfcRelConnectsElements"}, {"forward_attribute_name": "RelatingElement", "inverse_attribute_name": "ConnectedTo", "relationship_entity": "IfcRelConnectsElements"}] | NOT_EVALUATED |
| ae47e72e2af2b182 | VALID | evidence_generation | IfcBeam | IfcRelAggregates | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Decomposes", "relationship_entity": "IfcRelAggregates"}, {"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsDecomposedBy", "relationship_entity": "IfcRelAggregates"}] | NOT_EVALUATED |
| 8c0052ccd9bc96e4 | VALID | geometric_validation | IfcPump | IfcRelAssociatesMaterial | IfcRelAssociatesMaterial | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_NOT_FOUND | [] | NOT_EVALUATED |
| 8c0052ccd9bc96e4 | VALID | geometric_validation | IfcPump | IfcRelVoidsElement | IfcRelAssociatesMaterial | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] | NOT_EVALUATED |
| 21129edbbd73ebef | VALID | semantic_enrichment | IfcSpace | IfcRelContainedInSpatialStructure | IfcRelContainedInSpatialStructure | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatingStructure", "inverse_attribute_name": "ContainsElements", "relationship_entity": "IfcRelContainedInSpatialStructure"}] | NOT_EVALUATED |
| 21129edbbd73ebef | VALID | semantic_enrichment | IfcSpace | IfcRelConnectsElements | IfcRelContainedInSpatialStructure | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_NOT_FOUND | [] | NOT_EVALUATED |
| d2ed814a93840a19 | VALID | element_deletion | IfcFlowTerminal | IfcRelVoidsElement | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] | NOT_EVALUATED |
| d2ed814a93840a19 | VALID | element_deletion | IfcFlowTerminal | IfcRelFillsElement | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedBuildingElement", "inverse_attribute_name": "FillsVoids", "relationship_entity": "IfcRelFillsElement"}] | NOT_EVALUATED |
| fa3bca1c51085557 | VALID | evidence_generation | IfcAirTerminal | IfcRelNests | IfcRelNests | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] | NOT_EVALUATED |
| fa3bca1c51085557 | VALID | evidence_generation | IfcAirTerminal | IfcRelFillsElement | IfcRelNests | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedBuildingElement", "inverse_attribute_name": "FillsVoids", "relationship_entity": "IfcRelFillsElement"}] | NOT_EVALUATED |
| 048b754023b7b6b4 | VALID | element_modification | IfcColumn | IfcRelConnectsElements | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedElement", "inverse_attribute_name": "ConnectedFrom", "relationship_entity": "IfcRelConnectsElements"}, {"forward_attribute_name": "RelatingElement", "inverse_attribute_name": "ConnectedTo", "relationship_entity": "IfcRelConnectsElements"}] | NOT_EVALUATED |
| 048b754023b7b6b4 | VALID | element_modification | IfcColumn | IfcRelAggregates | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Decomposes", "relationship_entity": "IfcRelAggregates"}, {"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsDecomposedBy", "relationship_entity": "IfcRelAggregates"}] | NOT_EVALUATED |
| 5af537f550afd4aa | VALID | ambiguity_resolution | IfcFan | IfcRelContainedInSpatialStructure | IfcRelContainedInSpatialStructure | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedElements", "inverse_attribute_name": "ContainedInStructure", "relationship_entity": "IfcRelContainedInSpatialStructure"}] | NOT_EVALUATED |
| 5af537f550afd4aa | VALID | ambiguity_resolution | IfcFan | IfcRelNests | IfcRelContainedInSpatialStructure | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] | NOT_EVALUATED |
| 6ebb6c9ea431c6a7 | VALID | element_modification | IfcColumn | IfcRelVoidsElement | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] | NOT_EVALUATED |
| 6ebb6c9ea431c6a7 | VALID | element_modification | IfcColumn | IfcRelAssignsToGroup | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_NOT_FOUND | [] | NOT_EVALUATED |
| ca455e91ed772fd8 | VALID | recovery_request | IfcColumn | IfcRelVoidsElement | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatingBuildingElement", "inverse_attribute_name": "HasOpenings", "relationship_entity": "IfcRelVoidsElement"}] | NOT_EVALUATED |
| ca455e91ed772fd8 | VALID | recovery_request | IfcColumn | IfcRelAssignsToGroup | IfcRelVoidsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_NOT_FOUND | [] | NOT_EVALUATED |
| ee5057a4b7f15e3c | EXPECTED_CANONICAL_REJECTION | element_deletion | IfcSystem | IfcRelConnectsElements | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_NOT_FOUND | [] | NOT_EVALUATED |
| ee5057a4b7f15e3c | EXPECTED_CANONICAL_REJECTION | element_deletion | IfcSystem | IfcRelVoidsElement | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_NOT_FOUND | [] | NOT_EVALUATED |
| f72f31f4c063475b | VALID | recovery_request | IfcSpace | IfcRelFillsElement | IfcRelFillsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_NOT_FOUND | [] | NOT_EVALUATED |
| f84721ef28e281d1 | VALID | relationship_inference | IfcSpace | IfcRelAggregates | IfcRelAggregates | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Decomposes", "relationship_entity": "IfcRelAggregates"}, {"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsDecomposedBy", "relationship_entity": "IfcRelAggregates"}] | NOT_EVALUATED |
| f84721ef28e281d1 | VALID | relationship_inference | IfcSpace | IfcRelContainedInSpatialStructure | IfcRelAggregates | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatingStructure", "inverse_attribute_name": "ContainsElements", "relationship_entity": "IfcRelContainedInSpatialStructure"}] | NOT_EVALUATED |
| 23dad325e1a64458 | VALID | element_deletion | IfcAsset | IfcRelFillsElement | IfcRelFillsElement | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_NOT_FOUND | [] | NOT_EVALUATED |
| 3dab4b257ae52bfc | VALID | pset_assignment | IfcFlowTerminal | IfcRelNests | IfcRelNests | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] | NOT_EVALUATED |
| 3dab4b257ae52bfc | VALID | pset_assignment | IfcFlowTerminal | IfcRelFillsElement | IfcRelNests | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedBuildingElement", "inverse_attribute_name": "FillsVoids", "relationship_entity": "IfcRelFillsElement"}] | NOT_EVALUATED |
| 45f540e38ef9fe81 | EXPECTED_CANONICAL_REJECTION | element_deletion | IfcZone | IfcRelConnectsElements | IfcRelConnectsElements | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_NOT_FOUND | [] | NOT_EVALUATED |
| 8f91faebc05dd115 | VALID | material_assignment | IfcAsset | IfcRelDefinesByProperties | IfcRelDefinesByProperties | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "IsDefinedBy", "relationship_entity": "IfcRelDefinesByProperties"}] | NOT_EVALUATED |
| 8f91faebc05dd115 | VALID | material_assignment | IfcAsset | IfcRelNests | IfcRelDefinesByProperties | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsNestedBy", "relationship_entity": "IfcRelNests"}, {"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Nests", "relationship_entity": "IfcRelNests"}] | NOT_EVALUATED |
| 7f1ea524d9fdbdcb | VALID | ambiguity_resolution | IfcColumn | IfcRelAggregates | IfcRelAggregates | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_FOUND | [{"forward_attribute_name": "RelatedObjects", "inverse_attribute_name": "Decomposes", "relationship_entity": "IfcRelAggregates"}, {"forward_attribute_name": "RelatingObject", "inverse_attribute_name": "IsDecomposedBy", "relationship_entity": "IfcRelAggregates"}] | NOT_EVALUATED |
| 7f1ea524d9fdbdcb | VALID | ambiguity_resolution | IfcColumn | IfcRelAssociatesMaterial | IfcRelAggregates | DECLARATION_FOUND | CONCRETE_RELATIONSHIP | CLASS_INVERSE_PARTICIPATION_NOT_FOUND | [] | NOT_EVALUATED |

## No inverse participation found

| sample_id | ifc_class | relationship | inverse_endpoints |
| --- | --- | --- | --- |
| 495a677407a7f05a | IfcWall | IfcRelAssignsToGroup | [] |
| 8c0052ccd9bc96e4 | IfcPump | IfcRelAssociatesMaterial | [] |
| 21129edbbd73ebef | IfcSpace | IfcRelConnectsElements | [] |
| 6ebb6c9ea431c6a7 | IfcColumn | IfcRelAssignsToGroup | [] |
| ca455e91ed772fd8 | IfcColumn | IfcRelAssignsToGroup | [] |
| ee5057a4b7f15e3c | IfcSystem | IfcRelConnectsElements | [] |
| ee5057a4b7f15e3c | IfcSystem | IfcRelVoidsElement | [] |
| f72f31f4c063475b | IfcSpace | IfcRelFillsElement | [] |
| 23dad325e1a64458 | IfcAsset | IfcRelFillsElement | [] |
| 45f540e38ef9fe81 | IfcZone | IfcRelConnectsElements | [] |
| 7f1ea524d9fdbdcb | IfcColumn | IfcRelAssociatesMaterial | [] |

## Interpretation

"This audit identifies IFC4 schema-level declarations and inverse participation endpoints. It does not establish that a relationship is suitable for the professional task, present in a real IFC model, correctly instantiated, or sufficient as semantic evidence."
