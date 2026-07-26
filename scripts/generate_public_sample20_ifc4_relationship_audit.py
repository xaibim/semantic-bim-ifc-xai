from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import ifcopenshell
from ifcopenshell.util.schema import is_a

ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "2b8b568b33e5a6852f6353499c9233771ac3c6c2"
SOURCE_JSONL = ROOT / "sample20" / "sample20_public_records.jsonl"
EXPECTED_JSONL_SHA256 = "4f670146a4860e96fa820805e0f6d3db19fd3490e9db74a595bf33589aee9de1"
EXPECTED_SCHEMA_SHA256 = "769a6dad5517cb97860b00a2c4fc33ab3c0e6362b30059172bc55735834cdb25"
EXPECTED_RECORD_COUNT = 20
EXPECTED_POSITIVE_COUNT = 18
EXPECTED_EXPECTED_NEGATIVE_COUNT = 2
EXPECTED_UNIQUE_IFC_CLASS_COUNT = 11
EXPECTED_UNIQUE_RELATIONSHIP_COUNT = 10
EXPECTED_RECORD_RELATIONSHIP_PAIR_COUNT = 36
EXPECTED_EVIDENCE_RELATION_DECLARED_COUNT = 20
EXPECTED_EXACT_INVERSE_ENDPOINT_COUNT = 31
EXPECTED_INHERITED_SUPERTYPE_COMPATIBLE_COUNT = 5
EXPECTED_SCHEMA_COMPATIBLE_COUNT = 36
EXPECTED_SCHEMA_INCOMPATIBLE_COUNT = 0
AUDIT_ID = "XAIBIM_PUBLIC_SAMPLE20_IFC4_RELATIONSHIP_SCHEMA_PARTICIPATION_V3"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"STOP_PR15_MICRO_06B_JSONL_PARSE_ERROR:{path}:{line_number}:{exc}") from exc
    return records


def get_member(obj: Any, name: str) -> Any:
    member = getattr(obj, name, None)
    if callable(member):
        try:
            return member()
        except Exception:
            return None
    return member


def object_name(obj: Any) -> str | None:
    if obj is None:
        return None
    name = get_member(obj, "name")
    if isinstance(name, str):
        return name
    if name is not None:
        return str(name)
    return None


def sorted_unique_strings(values: list[Any]) -> list[str]:
    return sorted({str(value) for value in values if value is not None})


def supertype_chain(declaration: Any) -> list[str]:
    chain: list[str] = []
    seen: set[str] = set()
    current = declaration
    while current is not None:
        current_name = object_name(current)
        if current_name is None or current_name in seen:
            break
        chain.append(current_name)
        seen.add(current_name)
        current = get_member(current, "supertype")
    return chain


def relationship_forward_attributes(declaration: Any) -> list[dict[str, Any]]:
    attributes = list(get_member(declaration, "all_attributes") or [])
    argument_types = list(get_member(declaration, "argument_types") or [])
    forward_attributes: list[dict[str, Any]] = []
    for index, attribute in enumerate(attributes):
        argument_type = argument_types[index] if index < len(argument_types) else None
        forward_attributes.append(
            {
                "index": index,
                "name": object_name(attribute),
                "argument_type": None if argument_type is None else str(argument_type),
            }
        )
    return forward_attributes


def class_inverse_endpoints(declaration: Any) -> list[dict[str, Any]]:
    inverses = list(get_member(declaration, "all_inverse_attributes") or [])
    endpoints: list[dict[str, Any]] = []
    for inverse in inverses:
        relationship_entity = get_member(inverse, "entity_reference")
        forward_attribute = get_member(inverse, "attribute_reference")
        endpoints.append(
            {
                "inverse_attribute_name": get_member(inverse, "name"),
                "relationship_entity": object_name(relationship_entity),
                "forward_attribute_name": object_name(forward_attribute),
            }
        )
    return sorted(
        endpoints,
        key=lambda row: (
            str(row["relationship_entity"]),
            str(row["inverse_attribute_name"]),
            str(row["forward_attribute_name"]),
        ),
    )


def build_catalogs(
    schema: Any, records: list[dict[str, Any]]
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    ifc_classes = sorted_unique_strings(record["model_output"]["ifc_class"] for record in records)
    relationship_names = sorted_unique_strings(
        relationship
        for record in records
        for relationship in record["model_output"]["required_relationships"]
    )

    class_catalog: dict[str, Any] = {}
    for class_name in ifc_classes:
        try:
            declaration = schema.declaration_by_name(class_name)
        except Exception as exc:
            class_catalog[class_name] = {
                "declaration_exists": False,
                "is_abstract": None,
                "supertype_chain": [],
                "all_inverse_attributes": [],
                "error": f"{type(exc).__name__}: {exc}",
            }
            continue

        class_catalog[class_name] = {
            "declaration_exists": True,
            "is_abstract": bool(get_member(declaration, "is_abstract")),
            "supertype_chain": supertype_chain(declaration),
            "all_inverse_attributes": class_inverse_endpoints(declaration),
        }

    relationship_catalog: dict[str, Any] = {}
    relationship_declarations: dict[str, Any] = {}
    for relationship_name in relationship_names:
        try:
            declaration = schema.declaration_by_name(relationship_name)
        except Exception as exc:
            relationship_catalog[relationship_name] = {
                "declaration_exists": False,
                "is_ifc_relationship": False,
                "is_abstract": None,
                "supertype_chain": [],
                "all_attributes": [],
                "argument_types": [],
                "forward_attributes": [],
                "error": f"{type(exc).__name__}: {exc}",
            }
            relationship_declarations[relationship_name] = None
            continue

        relationship_declarations[relationship_name] = declaration
        relationship_catalog[relationship_name] = {
            "declaration_exists": True,
            "is_ifc_relationship": bool(is_a(declaration, "IfcRelationship")),
            "is_abstract": bool(get_member(declaration, "is_abstract")),
            "supertype_chain": supertype_chain(declaration),
            "all_attributes": sorted_unique_strings(
                object_name(attribute) for attribute in (get_member(declaration, "all_attributes") or [])
            ),
            "argument_types": [
                None if argument_type is None else str(argument_type)
                for argument_type in (list(get_member(declaration, "argument_types") or []))
            ],
            "forward_attributes": relationship_forward_attributes(declaration),
        }

    return class_catalog, relationship_catalog, relationship_declarations


def build_record_audits(
    records: list[dict[str, Any]],
    class_catalog: dict[str, Any],
    relationship_catalog: dict[str, Any],
    relationship_declarations: dict[str, Any],
) -> list[dict[str, Any]]:
    audits: list[dict[str, Any]] = []
    for record in records:
        model_output = record["model_output"]
        ifc_class = model_output["ifc_class"]
        relation_observed = model_output["evidence_trace"]["relation_observed"]
        evidence_relation_declared = relation_observed in model_output["required_relationships"]
        class_endpoints = class_catalog.get(ifc_class, {}).get("all_inverse_attributes", [])

        relationship_audits: list[dict[str, Any]] = []
        for relationship in model_output["required_relationships"]:
            relation_info = relationship_catalog.get(relationship, {})
            declaration = relationship_declarations.get(relationship)
            exact_inverse_endpoints = [
                endpoint
                for endpoint in class_endpoints
                if endpoint.get("relationship_entity") == relationship
            ]
            inherited_supertype_endpoints: list[dict[str, Any]] = []
            if not exact_inverse_endpoints and declaration is not None:
                for endpoint in class_endpoints:
                    endpoint_relationship_name = endpoint.get("relationship_entity")
                    if endpoint_relationship_name is None:
                        continue
                    if not is_a(declaration, endpoint_relationship_name):
                        continue
                    inherited_supertype_endpoints.append(
                        {
                            "inverse_attribute_name": endpoint.get("inverse_attribute_name"),
                            "forward_attribute_name": endpoint.get("forward_attribute_name"),
                            "declared_relationship_supertype": endpoint_relationship_name,
                        }
                    )

            if exact_inverse_endpoints:
                compatibility_state = "EXACT_INVERSE_ENDPOINT"
            elif inherited_supertype_endpoints:
                compatibility_state = "INHERITED_SUPERTYPE_COMPATIBLE"
            else:
                compatibility_state = "SCHEMA_INCOMPATIBLE"
            relationship_audits.append(
                {
                    "relationship": relationship,
                    "required_relationship_supertype_chain": relation_info.get("supertype_chain", []),
                    "evidence_relation_observed": relation_observed,
                    "evidence_relation_declared": evidence_relation_declared,
                    "declaration_exists": bool(relation_info.get("declaration_exists")),
                    "is_ifc_relationship": bool(relation_info.get("is_ifc_relationship")),
                    "relationship_is_abstract": bool(relation_info.get("is_abstract")),
                    "compatibility_state": compatibility_state,
                    "schema_compatible": compatibility_state
                    in {"EXACT_INVERSE_ENDPOINT", "INHERITED_SUPERTYPE_COMPATIBLE"},
                    "exact_inverse_endpoints": exact_inverse_endpoints,
                    "inherited_supertype_endpoints": inherited_supertype_endpoints,
                    "interpretation_state": "NOT_EVALUATED",
                }
            )

        audits.append(
            {
                "sample_id": record["sample_id"],
                "case_expectation": record["case_expectation"],
                "semantic_type": model_output["semantic_type"],
                "ifc_class": ifc_class,
                "evidence_relation_observed": relation_observed,
                "evidence_relation_declared": evidence_relation_declared,
                "relationship_audits": relationship_audits,
            }
        )
    return audits


def build_audit() -> dict[str, Any]:
    schema = ifcopenshell.schema_by_name("IFC4")
    records = load_jsonl(SOURCE_JSONL)
    source_sha256 = sha256_path(SOURCE_JSONL)
    if source_sha256.lower() != EXPECTED_JSONL_SHA256:
        raise SystemExit("STOP_PR15_MICRO_06B_SOURCE_HASH_MISMATCH")
    if len(records) != EXPECTED_RECORD_COUNT:
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")
    sample_ids = [record.get("sample_id") for record in records]
    if len(set(sample_ids)) != EXPECTED_RECORD_COUNT:
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")
    if sum(record.get("case_expectation") == "VALID" for record in records) != EXPECTED_POSITIVE_COUNT:
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")
    if sum(record.get("case_expectation") == "EXPECTED_CANONICAL_REJECTION" for record in records) != EXPECTED_EXPECTED_NEGATIVE_COUNT:
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")
    if any(record.get("model_output") != record.get("reference_output") for record in records):
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")

    class_catalog, relationship_catalog, relationship_declarations = build_catalogs(schema, records)
    record_audits = build_record_audits(records, class_catalog, relationship_catalog, relationship_declarations)

    relationship_rows = [
        row
        for record in record_audits
        for row in record["relationship_audits"]
    ]
    evidence_relation_declared_count = sum(record["evidence_relation_declared"] for record in record_audits)
    exact_inverse_endpoint_count = sum(row["compatibility_state"] == "EXACT_INVERSE_ENDPOINT" for row in relationship_rows)
    inherited_supertype_compatible_count = sum(
        row["compatibility_state"] == "INHERITED_SUPERTYPE_COMPATIBLE" for row in relationship_rows
    )
    schema_compatible_count = sum(row["schema_compatible"] for row in relationship_rows)
    schema_incompatible_count = sum(row["compatibility_state"] == "SCHEMA_INCOMPATIBLE" for row in relationship_rows)

    if len(class_catalog) != EXPECTED_UNIQUE_IFC_CLASS_COUNT:
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")
    if len(relationship_catalog) != EXPECTED_UNIQUE_RELATIONSHIP_COUNT:
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")
    if len(relationship_rows) != EXPECTED_RECORD_RELATIONSHIP_PAIR_COUNT:
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")
    if evidence_relation_declared_count != EXPECTED_EVIDENCE_RELATION_DECLARED_COUNT:
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")
    if exact_inverse_endpoint_count != EXPECTED_EXACT_INVERSE_ENDPOINT_COUNT:
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")
    if inherited_supertype_compatible_count != EXPECTED_INHERITED_SUPERTYPE_COMPATIBLE_COUNT:
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")
    if schema_compatible_count != EXPECTED_SCHEMA_COMPATIBLE_COUNT:
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")
    if schema_incompatible_count != EXPECTED_SCHEMA_INCOMPATIBLE_COUNT:
        raise SystemExit("STOP_PR15_MICRO_06B_AUDIT_COUNT_MISMATCH")

    summary = {
        "record_count": EXPECTED_RECORD_COUNT,
        "positive_count": EXPECTED_POSITIVE_COUNT,
        "expected_negative_count": EXPECTED_EXPECTED_NEGATIVE_COUNT,
        "unique_ifc_class_count": EXPECTED_UNIQUE_IFC_CLASS_COUNT,
        "unique_relationship_count": EXPECTED_UNIQUE_RELATIONSHIP_COUNT,
        "record_relationship_pair_count": EXPECTED_RECORD_RELATIONSHIP_PAIR_COUNT,
        "evidence_relation_declared_count": EXPECTED_EVIDENCE_RELATION_DECLARED_COUNT,
        "exact_inverse_endpoint_count": EXPECTED_EXACT_INVERSE_ENDPOINT_COUNT,
        "inherited_supertype_compatible_count": EXPECTED_INHERITED_SUPERTYPE_COMPATIBLE_COUNT,
        "schema_compatible_count": EXPECTED_SCHEMA_COMPATIBLE_COUNT,
        "schema_incompatible_count": EXPECTED_SCHEMA_INCOMPATIBLE_COUNT,
    }

    result = {
        "audit_id": AUDIT_ID,
        "audit_metadata": {
            "source_commit": SOURCE_COMMIT,
            "source_file": "sample20/sample20_public_records.jsonl",
            "source_sha256": EXPECTED_JSONL_SHA256,
            "ifcopenshell_version": ifcopenshell.version,
            "ifc_schema": "IFC4",
            "scope_note": "This audit does not demonstrate professional task suitability or real IFC instance validity.",
        },
        "summary": summary,
        "interpretation_boundary": {
            "schema_participation_only": True,
            "semantic_task_alignment_evaluated": False,
            "real_ifc_model_evaluated": False,
            "relationship_instances_created": False,
            "ifc_certification_claimed": False,
            "corrections_authorized": False,
        },
        "class_catalog": class_catalog,
        "relationship_catalog": relationship_catalog,
        "record_audits": record_audits,
    }
    return result


def canonical_json_text(result: dict[str, Any]) -> str:
    return json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def markdown_cell(value: Any) -> str:
    if isinstance(value, bool):
        text = "true" if value else "false"
    elif value is None:
        text = ""
    elif isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    else:
        text = str(value)
    return text.replace("|", r"\|").replace("\n", " ")


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    metadata = result["audit_metadata"]
    relationship_catalog = result["relationship_catalog"]
    record_audits = result["record_audits"]

    lines: list[str] = []
    lines.append("# Public sample20 IFC4 subtype-aware relationship schema-participation audit")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.extend(
        [
            "- frozen public sample20;",
            "- IFC4 schema participation only;",
            "- subtype-aware classification of relationship endpoints;",
            "- no semantic task-alignment conclusion;",
            "- no real IFC instance validation;",
            "- no certification;",
            "- no correction authorized by this report.",
        ]
    )
    lines.append("")
    lines.append("## Source")
    lines.append("")
    lines.extend(
        [
            f"- commit: `{metadata['source_commit']}`",
            f"- source JSONL: `{metadata['source_file']}`",
            f"- SHA-256: `{metadata['source_sha256']}`",
            f"- IfcOpenShell version: `{metadata['ifcopenshell_version']}`",
            f"- IFC schema: `{metadata['ifc_schema']}`",
        ]
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| field | value |")
    lines.append("| --- | --- |")
    for key in [
        "record_count",
        "positive_count",
        "expected_negative_count",
        "unique_ifc_class_count",
        "unique_relationship_count",
        "record_relationship_pair_count",
        "evidence_relation_declared_count",
        "exact_inverse_endpoint_count",
        "inherited_supertype_compatible_count",
        "schema_compatible_count",
        "schema_incompatible_count",
    ]:
        lines.append(f"| `{key}` | `{summary[key]}` |")

    lines.append("")
    lines.append("## Relationship catalogue")
    lines.append("")
    lines.append("| relationship | declaration_exists | is_ifc_relationship | is_abstract | supertype_chain | forward_attributes |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for relationship_name in sorted(relationship_catalog):
        entry = relationship_catalog[relationship_name]
        lines.append(
            "| {relationship} | {declaration_exists} | {is_ifc_relationship} | {is_abstract} | {supertype_chain} | {forward_attributes} |".format(
                relationship=markdown_cell(relationship_name),
                declaration_exists=markdown_cell(entry["declaration_exists"]),
                is_ifc_relationship=markdown_cell(entry["is_ifc_relationship"]),
                is_abstract=markdown_cell("ABSTRACT_RELATIONSHIP" if entry["is_abstract"] else "CONCRETE_RELATIONSHIP"),
                supertype_chain=markdown_cell(entry["supertype_chain"]),
                forward_attributes=markdown_cell(
                    [row["name"] for row in entry["forward_attributes"]]
                ),
            )
        )

    lines.append("")
    lines.append("## Record-relationship matrix")
    lines.append("")
    lines.append("| sample_id | case_expectation | semantic_type | ifc_class | relationship | evidence_relation | declaration | abstract | compatibility_state | schema_compatible | exact_inverse_endpoints | inherited_supertype_endpoints | semantic_alignment |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    exact_rows: list[dict[str, Any]] = []
    inherited_rows: list[dict[str, Any]] = []
    incompatible_rows: list[dict[str, Any]] = []
    for record in record_audits:
        for row in record["relationship_audits"]:
            if row["compatibility_state"] == "EXACT_INVERSE_ENDPOINT":
                exact_rows.append(
                    {
                        "sample_id": record["sample_id"],
                        "ifc_class": record["ifc_class"],
                        "relationship": row["relationship"],
                        "exact_inverse_endpoints": row["exact_inverse_endpoints"],
                    }
                )
            elif row["compatibility_state"] == "INHERITED_SUPERTYPE_COMPATIBLE":
                inherited_rows.append(
                    {
                        "sample_id": record["sample_id"],
                        "ifc_class": record["ifc_class"],
                        "relationship": row["relationship"],
                        "inherited_supertype_endpoints": row["inherited_supertype_endpoints"],
                    }
                )
            else:
                incompatible_rows.append(
                    {
                        "sample_id": record["sample_id"],
                        "ifc_class": record["ifc_class"],
                        "relationship": row["relationship"],
                        "exact_inverse_endpoints": row["exact_inverse_endpoints"],
                        "inherited_supertype_endpoints": row["inherited_supertype_endpoints"],
                    }
                )
            lines.append(
                "| {sample_id} | {case_expectation} | {semantic_type} | {ifc_class} | {relationship} | {evidence_relation} | {declaration} | {abstract} | {compatibility_state} | {schema_compatible} | {exact_inverse_endpoints} | {inherited_supertype_endpoints} | {semantic_alignment} |".format(
                    sample_id=markdown_cell(record["sample_id"]),
                    case_expectation=markdown_cell(record["case_expectation"]),
                    semantic_type=markdown_cell(record["semantic_type"]),
                    ifc_class=markdown_cell(record["ifc_class"]),
                    relationship=markdown_cell(row["relationship"]),
                    evidence_relation=markdown_cell(row["evidence_relation_observed"]),
                    declaration=markdown_cell("DECLARATION_FOUND" if row["declaration_exists"] else "DECLARATION_MISSING"),
                    abstract=markdown_cell("ABSTRACT_RELATIONSHIP" if row["relationship_is_abstract"] else "CONCRETE_RELATIONSHIP"),
                    compatibility_state=markdown_cell(row["compatibility_state"]),
                    schema_compatible=markdown_cell(row["schema_compatible"]),
                    exact_inverse_endpoints=markdown_cell(row["exact_inverse_endpoints"]),
                    inherited_supertype_endpoints=markdown_cell(row["inherited_supertype_endpoints"]),
                    semantic_alignment=markdown_cell(row["interpretation_state"]),
                )
            )

    lines.append("")
    lines.append("## Exact inverse endpoints")
    lines.append("")
    lines.append("| sample_id | ifc_class | relationship | exact_inverse_endpoints |")
    lines.append("| --- | --- | --- | --- |")
    for row in exact_rows:
        lines.append(
            "| {sample_id} | {ifc_class} | {relationship} | {exact_inverse_endpoints} |".format(
                sample_id=markdown_cell(row["sample_id"]),
                ifc_class=markdown_cell(row["ifc_class"]),
                relationship=markdown_cell(row["relationship"]),
                exact_inverse_endpoints=markdown_cell(row["exact_inverse_endpoints"]),
            )
        )

    lines.append("")
    lines.append("## Inherited supertype-compatible rows")
    lines.append("")
    lines.append("| sample_id | ifc_class | relationship | inherited_supertype_endpoints |")
    lines.append("| --- | --- | --- | --- |")
    for row in inherited_rows:
        lines.append(
            "| {sample_id} | {ifc_class} | {relationship} | {inherited_supertype_endpoints} |".format(
                sample_id=markdown_cell(row["sample_id"]),
                ifc_class=markdown_cell(row["ifc_class"]),
                relationship=markdown_cell(row["relationship"]),
                inherited_supertype_endpoints=markdown_cell(row["inherited_supertype_endpoints"]),
            )
        )

    lines.append("")
    lines.append("## Schema-incompatible rows")
    lines.append("")
    lines.append("| sample_id | ifc_class | relationship | exact_inverse_endpoints | inherited_supertype_endpoints |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in incompatible_rows:
        lines.append(
            "| {sample_id} | {ifc_class} | {relationship} | {exact_inverse_endpoints} | {inherited_supertype_endpoints} |".format(
                sample_id=markdown_cell(row["sample_id"]),
                ifc_class=markdown_cell(row["ifc_class"]),
                relationship=markdown_cell(row["relationship"]),
                exact_inverse_endpoints=markdown_cell(row["exact_inverse_endpoints"]),
                inherited_supertype_endpoints=markdown_cell(row["inherited_supertype_endpoints"]),
            )
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        '"This audit identifies IFC4 schema-level declarations and inverse participation endpoints. It does not establish that a relationship is suitable for the professional task, present in a real IFC model, correctly instantiated, or sufficient as semantic evidence."'
    )
    return "\n".join(lines)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_check(json_output: Path, markdown_output: Path) -> int:
    result = build_audit()
    json_text = canonical_json_text(result)
    markdown_text = render_markdown(result) + "\n"
    if not json_output.exists() or not markdown_output.exists():
        print("IFC4_RELATIONSHIP_AUDIT_OUT_OF_DATE")
        return 1
    current_json = json_output.read_text(encoding="utf-8")
    current_markdown = markdown_output.read_text(encoding="utf-8")
    if current_json != json_text or current_markdown != markdown_text:
        print("IFC4_RELATIONSHIP_AUDIT_OUT_OF_DATE")
        return 1
    print("IFC4_RELATIONSHIP_AUDIT_CURRENT")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        return run_check(args.json_output, args.markdown_output)

    result = build_audit()
    write_text(args.json_output, canonical_json_text(result))
    write_text(args.markdown_output, render_markdown(result) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
