# Public sample20 IFC4 Pset applicability correction

## Scope

- This report covers only the public `sample20` fixture.
- It uses IFC4.
- It uses `IfcOpenShell 0.8.5` with `PsetQto("IFC4")`.
- It does not freeze the future A1 dataset schema.
- It is not IFC certification.
- It does not validate relationships, geometry, materials, or evidence traces.

## Source

source SHA-256:
29f10ff0bd5bb25be0cb5bdb975bda93c783f65622e0c3c86e179a49665b313b

## Probe summary

- declared required_pset entries: 52
- applicable Psets: 9
- known templates not applicable to the declared class: 27
- unknown template names: 16

## Correction policy

1. applicable original Psets were preserved;
2. incompatible and unknown names were removed;
3. `Pset_QuantityTakeOff` was not converted into a Qto inside `required_psets`;
4. reviewed class-specific occurrence Psets were introduced only where semantically appropriate;
5. an empty `required_psets` array is intentional where no Pset is required or where the missing context prevents safe Pset selection;
6. `model_output` and `reference_output` remain identical;
7. the stored agreement remains fixture consistency, not model performance.

## Correction table

| sample_id | ifc_class | previous_required_psets | final_required_psets | decision |
| --- | --- | --- | --- | --- |
| `4eeac340747306fd` | `IfcColumn` | `["Pset_QuantityTakeOff", "Pset_ColumnCommon", "Pset_SlabCommon"]` | `["Pset_ColumnCommon"]` | preserve the class-applicable Pset only |
| `495a677407a7f05a` | `IfcWall` | `["Pset_WindowCommon", "Pset_WallCommon", "Pset_SpaceCommon", "Pset_DoorCommon"]` | `["Pset_WallCommon"]` | preserve the class-applicable Pset only |
| `1ae42de17ac977f7` | `IfcBeam` | `["Pset_BeamCommon", "Pset_ColumnCommon"]` | `["Pset_BeamCommon"]` | preserve the class-applicable Pset only |
| `ae47e72e2af2b182` | `IfcBeam` | `["Pset_QuantityTakeOff", "Pset_SlabCommon"]` | `["Pset_BeamCommon"]` | replace the incompatible mix with the beam-occurrence Pset |
| `8c0052ccd9bc96e4` | `IfcPump` | `["Pset_DistributionFlowElementCommon", "Pset_MaterialCommon", "Pset_WallCommon"]` | `["Pset_PumpOccurrence"]` | replace incompatible names with the pump-occurrence Pset |
| `21129edbbd73ebef` | `IfcSpace` | `["Pset_SpaceCommon", "Pset_WindowCommon", "Pset_SlabCommon", "Pset_WallCommon"]` | `["Pset_SpaceCommon"]` | preserve the class-applicable Pset only |
| `d2ed814a93840a19` | `IfcFlowTerminal` | `["Pset_WallCommon", "Pset_DistributionFlowElementCommon"]` | `[]` | no safe Pset remains for this record |
| `fa3bca1c51085557` | `IfcAirTerminal` | `["Pset_DistributionFlowElementCommon", "Pset_WallCommon", "Pset_QuantityTakeOff"]` | `["Pset_AirTerminalOccurrence"]` | replace the incompatible mix with the air-terminal-occurrence Pset |
| `048b754023b7b6b4` | `IfcColumn` | `["Pset_QuantityTakeOff", "Pset_ColumnCommon"]` | `["Pset_ColumnCommon"]` | preserve the class-applicable Pset only |
| `5af537f550afd4aa` | `IfcFan` | `["Pset_MaterialCommon", "Pset_DistributionFlowElementCommon"]` | `["Pset_FanOccurrence"]` | replace the incompatible mix with the fan-occurrence Pset |
| `6ebb6c9ea431c6a7` | `IfcColumn` | `["Pset_QuantityTakeOff", "Pset_ColumnCommon", "Pset_BeamCommon"]` | `["Pset_ColumnCommon"]` | preserve the class-applicable Pset only |
| `ca455e91ed772fd8` | `IfcColumn` | `["Pset_QuantityTakeOff", "Pset_WallCommon", "Pset_BeamCommon"]` | `["Pset_ColumnCommon"]` | replace incompatible names with the column-occurrence Pset |
| `f72f31f4c063475b` | `IfcSpace` | `["Pset_SlabCommon", "Pset_SpaceCommon", "Pset_DoorCommon"]` | `["Pset_SpaceCommon"]` | preserve the class-applicable Pset only |
| `f84721ef28e281d1` | `IfcSpace` | `["Pset_SpaceCommon", "Pset_SlabCommon", "Pset_DoorCommon", "Pset_QuantityTakeOff"]` | `["Pset_SpaceCommon"]` | preserve the class-applicable Pset only |
| `23dad325e1a64458` | `IfcAsset` | `["Pset_QuantityTakeOff", "Pset_WallCommon", "Pset_MaterialCommon"]` | `[]` | no safe Pset remains for this record |
| `3dab4b257ae52bfc` | `IfcFlowTerminal` | `["Pset_DistributionFlowElementCommon", "Pset_QuantityTakeOff", "Pset_WallCommon"]` | `[]` | no safe Pset remains for this record |
| `8f91faebc05dd115` | `IfcAsset` | `["Pset_QuantityTakeOff", "Pset_MaterialCommon"]` | `[]` | no safe Pset remains for this record |
| `7f1ea524d9fdbdcb` | `IfcColumn` | `["Pset_QuantityTakeOff", "Pset_ColumnCommon", "Pset_BeamCommon", "Pset_SlabCommon"]` | `["Pset_ColumnCommon"]` | preserve the class-applicable Pset only |

The IFC4 Pset correction applies only to the frozen public sample20 fixture.
The future A1 dataset protocol will define Psets, quantity sets and material associations as separate semantic dimensions.
