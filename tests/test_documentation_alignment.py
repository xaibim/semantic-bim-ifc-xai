from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

README = ROOT / "README.md"
VALIDATION_GATES = ROOT / "docs" / "methodology" / "validation_gates.md"
LICENSES = ROOT / "LICENSES.md"
BASELINE_MATRIX = ROOT / "benchmark" / "baseline_matrix.md"
END_TO_END = ROOT / "docs" / "examples" / "end_to_end_public_example.md"
CITATION = ROOT / "CITATION.cff"
JSONL = ROOT / "sample20" / "sample20_public_records.jsonl"
SCHEMA_PATHS = [
    ROOT / "sample20" / "schema_public_sample20_v2.json",
    ROOT / "spaces" / "huggingface" / "schema_public_sample20_v2.json",
    ROOT / "spaces" / "huggingface_harness" / "schema_public_sample20_v2.json",
]

# Forbidden substrings are built by concatenation so this test file never
# contains the literal old/deprecated tokens (keeps the repository grep clean).
GH_OLD = "BIMAIBlend" + "gineer/semantic-bim-ifc-xai"
HF_OLD = "huggingface.co/spaces/XAIBIM" + "/legacy-"
MIN_CONTRACT = "minimal public schema " + "contract"
LEGACY_CLASS_FIELD = "suggested_ifc_" + "class"
LOI_FIELD = "loi_" + "table"
LEGACY_BLOCK = "hard_" + "block"
BLOCKED_PREREQ = "blocked-by-" + "prerequisite"
OLD_REPLAY_NOTE = "Deterministic public " + "replay completed successfully"
OLD_EXECUTED_REPLAY = "Executed " + "Replay"
OLD_RUN_PUBLIC_REPLAY = "Run the public replay"
SCHEMA_ONLY_VALIDATION_LOWER = "schema-only validation"
SCHEMA_ONLY_VALIDATION_TITLE = "Schema-only JSON parsing and JSON Schema validation"
NOT_EVALUATED_FIXTURE = "fixture_contract=NOT_EVALUATED"
NOT_CHECKED_INTEGRITY = "integrity=NOT_CHECKED"
LOWER_NOT_EVALUATED_FIXTURE = "fixture_contract=not_evaluated"
LOWER_NOT_CHECKED_INTEGRITY = "integrity=not_checked"


def tracked_text_files():
    files = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if ".git" in p.parts or "node_modules" in p.parts or ".venv" in p.parts:
            continue
        if p.suffix.lower() in {".png", ".pyc", ".jpg", ".jpeg", ".gif"}:
            continue
        files.append(p)
    return files


def normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


class TestDocumentationAlignment(unittest.TestCase):
    def test_01_github_canonical_xaibim(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("https://github.com/xaibim/semantic-bim-ifc-xai", text)

    def test_02_hf_canonical_xaibim(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("https://huggingface.co/spaces/XAIBIM/semantic-xaibim-replay", text)
        self.assertIn("https://huggingface.co/spaces/XAIBIM/semantic-xaibim-harness", text)
        self.assertIn("https://huggingface.co/XAIBIM/spaces", text)

    def test_03_kaggle_linked(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("https://www.kaggle.com/code/xaibim/semantic-bim-ifc-xai", text)

    def test_04_youtube_linked(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("https://www.youtube.com/@XAIBIM", text)

    def test_05_linkedin_linked(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("https://www.linkedin.com/company/xaibim", text)

    def test_06_three_schemas_byte_identical(self):
        shas = [p.read_bytes() for p in SCHEMA_PATHS]
        self.assertEqual(len(set(shas)), 1)

    def test_07_three_schemas_new_id(self):
        expected = (
            "https://github.com/xaibim/semantic-bim-ifc-xai/"
            "sample20/schema_public_sample20_v2.json"
        )
        for p in SCHEMA_PATHS:
            data = json.loads(p.read_text(encoding="utf-8"))
            self.assertEqual(data.get("$id"), expected)

    def test_08_readme_research_contributions(self):
        text = README.read_text(encoding="utf-8").lower()
        self.assertIn("research contributions", text)

    def test_09_readme_mermaid_architecture(self):
        text = README.read_text(encoding="utf-8").lower()
        self.assertIn("```mermaid", text)
        self.assertIn("natural-language aeco request", text)
        self.assertIn("professional review or safe next action", text)

    def test_10_readme_components_table(self):
        text = README.read_text(encoding="utf-8").lower()
        self.assertIn("components and responsibilities", text)
        for comp in [
            "semantic compiler",
            "ifc mapper",
            "schema validator",
            "canonical / fixture checker",
            "evidence-trace fields",
            "stored-record validator",
            "integrity verifier",
            "qlora aggregate verifier",
            "benchmark layer",
            "interactive space",
        ]:
            self.assertIn(comp, text)

    def test_11_readme_full_schema_command(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn(
            "python harness/schema_validator.py sample20/sample20_public_records.jsonl "
            "--schema sample20/schema_public_sample20_v2.json",
            text,
        )

    def test_12_readme_no_minimal_contract_phrase(self):
        text = README.read_text(encoding="utf-8").lower()
        self.assertNotIn(MIN_CONTRACT, text)

    def test_13_validation_gates_no_legacy_class_field(self):
        text = VALIDATION_GATES.read_text(encoding="utf-8").lower()
        self.assertNotIn(LEGACY_CLASS_FIELD, text)

    def test_14_validation_gates_no_loi_field(self):
        text = VALIDATION_GATES.read_text(encoding="utf-8").lower()
        self.assertNotIn(LOI_FIELD, text)

    def test_15_validation_gates_no_blocked_state(self):
        text = VALIDATION_GATES.read_text(encoding="utf-8").lower()
        self.assertNotIn(LEGACY_BLOCK, text)
        self.assertNotIn(BLOCKED_PREREQ, text)

    def test_16_validation_gates_two_layers(self):
        text = VALIDATION_GATES.read_text(encoding="utf-8")
        self.assertIn("Layer A", text)
        self.assertIn("Layer B", text)
        self.assertIn("Public Executable Checks", text)
        self.assertIn("Private / Future Dataset Methodology", text)

    def test_17_end_to_end_example_exists(self):
        self.assertTrue(END_TO_END.exists())
        text = END_TO_END.read_text(encoding="utf-8").lower()
        self.assertIn("stored public record", text)
        self.assertIn("stored-record walkthrough", text)
        self.assertIn("live model inference", text)
        self.assertIn("interactive conceptual demonstration", text)

    def test_18_baseline_matrix_exists(self):
        self.assertTrue(BASELINE_MATRIX.exists())
        text = BASELINE_MATRIX.read_text(encoding="utf-8")
        self.assertIn("Baseline Matrix (Planned Comparative Benchmark)", text)
        self.assertIn("| A | Deterministic IFC/schema/catalogue lookup | REQUIRED |", text)
        self.assertIn("| B | Base LLM, prompt-only | REQUIRED |", text)
        self.assertIn("| C | Base LLM with retrieved IFC/bSDD/IDS context | REQUIRED |", text)
        self.assertIn("| D | Graph or ontology-grounded retrieval | CONDITIONAL |", text)
        self.assertIn("| E | Tool-using adaptive IFC exploration | CONDITIONAL |", text)
        self.assertIn("| F | Single-agent planner | OPTIONAL |", text)
        self.assertIn("| G | Multi-agent workflow | OPTIONAL |", text)
        self.assertIn("| H | QLoRA-adapted model | OPTIONAL_AFTER_GATES |", text)
        self.assertIn("after scope freeze and prerequisite dataset-quality gates", text)
        self.assertNotIn("../../docs/", text)

    def test_19_licenses_mit_and_cc_by(self):
        text = LICENSES.read_text(encoding="utf-8")
        self.assertIn("SPDX-License-Identifier: MIT", text)
        self.assertIn("SPDX-License-Identifier: CC-BY-4.0", text)

    def test_20_sample20_exact_metrics(self):
        rows = [
            json.loads(l)
            for l in JSONL.read_text(encoding="utf-8").splitlines()
            if l.strip()
        ]
        self.assertEqual(len(rows), 20)
        valid = [r for r in rows if r["case_expectation"] == "VALID"]
        rej = [r for r in rows if r["case_expectation"] == "EXPECTED_CANONICAL_REJECTION"]
        self.assertEqual(len(valid), 18)
        self.assertEqual(len(rej), 2)
        for r in rej:
            self.assertEqual(r["record_status"], "EXPECTED_REJECTION_PASS")
        canonical_ok = sum(1 for r in rows if r["canonical_check"]["ok"])
        self.assertAlmostEqual(canonical_ok / len(rows), 0.9)
        expectation_met = sum(1 for r in rows if r["expectation_met"])
        self.assertAlmostEqual(expectation_met / len(rows), 1.0)

    def test_21_zero_old_canonical_links(self):
        for p in tracked_text_files():
            text = p.read_text(encoding="utf-8", errors="ignore")
            self.assertNotIn(GH_OLD, text)
            self.assertNotIn(HF_OLD, text)
            self.assertNotIn(MIN_CONTRACT, text)

    def test_22_youtube_linkedin_not_scientific_evidence(self):
        text = README.read_text(encoding="utf-8")
        yt_line = [ln for ln in text.splitlines() if "youtube" in ln.lower()]
        self.assertTrue(yt_line)
        self.assertIn("dissemination", text.lower())
        self.assertIn("not", text.lower())
        self.assertIn("Public demonstrations and dissemination", text)
        self.assertIn("Project updates and professional dissemination", text)

    def test_23_no_unqualified_ifc_version_claim(self):
        for p in tracked_text_files():
            text = p.read_text(encoding="utf-8", errors="ignore")
            low = text.lower()
            if "ifc2x3" in low or "ifc4" in low:
                self.assertTrue(
                    any(
                        k in low
                        for k in [
                            "does not demonstrate",
                            "does not prove",
                            "not demonstrate",
                            "no public evidence",
                            "no claim",
                            "does not",
                        ]
                    ),
                    msg=f"Unqualified IFC version claim in {p}",
                )

    def test_24_public_example_matches_jsonl(self):
        rows = [
            json.loads(line)
            for line in JSONL.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        row = next(r for r in rows if r["sample_id"] == "4eeac340747306fd")
        self.assertEqual(row["model_output"]["required_psets"], ["Pset_ColumnCommon"])
        example = END_TO_END.read_text(encoding="utf-8")
        self.assertIn('"required_psets": ["Pset_ColumnCommon"]', example)
        self.assertNotIn("Pset_QuantityTakeOff", example)
        self.assertNotIn("Pset_SlabCommon", example)

    def test_25_no_unqualified_multilingual_claim(self):
        for p in tracked_text_files():
            text = p.read_text(encoding="utf-8", errors="ignore")
            low = text.lower()
            if "multilingual" in low:
                self.assertTrue(
                    any(k in low for k in ["not", "no ", "does not", "without"]),
                    msg=f"Unqualified multilingual claim in {p}",
                )

    def test_26_no_prohibited_document_phrases(self):
        forbidden_phrases = [
            "re-" + "executes records",
            "re-" + "runs records",
            "resolvable " + "evidence_pattern",
            "Prompt payload " + "if available.",
            "Canonical " + "output.",
            "Expected " + "output.",
            "Parsed " + "output.",
            "doi: " + '""',
            "version: 0." + "2.0",
        ]
        for p in tracked_text_files():
            text = p.read_text(encoding="utf-8", errors="ignore")
            for phrase in forbidden_phrases:
                self.assertNotIn(phrase, text, msg=f"Forbidden phrase in {p}: {phrase}")

    def test_27_no_invented_comparative_benchmark(self):
        text = BASELINE_MATRIX.read_text(encoding="utf-8")
        self.assertIn("No final comparative results", text)
        self.assertIn("planned", text.lower())
        readme = README.read_text(encoding="utf-8").lower()
        self.assertIn("planned", readme)
        self.assertIn("not executed", readme)

    def test_28_stored_record_docs_updated(self):
        docs = [
            ROOT / "QUICKSTART.md",
            ROOT / "PUBLIC_EVIDENCE.md",
            ROOT / "sample20" / "VALIDATION_SUMMARY.md",
            ROOT / "benchmark" / "results_sample20.md",
        ]
        for path in docs:
            text = path.read_text(encoding="utf-8")
            lower = text.lower()
            self.assertIn("deterministic stored-record validation", lower)
            self.assertIn("json parsing", lower)
            self.assertIn("schema validation", lower)
            self.assertIn("fixture-contract validation", lower)
            self.assertIn("canonical three-copy integrity", lower)
            self.assertNotIn(OLD_REPLAY_NOTE, text)
            self.assertNotIn(OLD_EXECUTED_REPLAY, text)
            self.assertNotIn(OLD_RUN_PUBLIC_REPLAY, text)

    def test_29_schema_validator_docs_updated(self):
        quickstart = (ROOT / "QUICKSTART.md").read_text(encoding="utf-8")
        evidence = normalized_text(ROOT / "PUBLIC_EVIDENCE.md")
        summary = normalized_text(ROOT / "sample20" / "VALIDATION_SUMMARY.md")

        self.assertIn(SCHEMA_ONLY_VALIDATION_LOWER, quickstart.lower())
        self.assertIn(SCHEMA_ONLY_VALIDATION_TITLE, evidence)
        self.assertIn(SCHEMA_ONLY_VALIDATION_TITLE, summary)

        for text in (evidence, summary):
            self.assertIn(NOT_EVALUATED_FIXTURE, text)
            self.assertIn(NOT_CHECKED_INTEGRITY, text)
            self.assertNotIn(LOWER_NOT_EVALUATED_FIXTURE, text)
            self.assertNotIn(LOWER_NOT_CHECKED_INTEGRITY, text)

        self.assertIn("does not evaluate the fixture contract or canonical three-copy integrity", quickstart)
        self.assertIn("Counted from model and reference evidence_trace objects", evidence)
        self.assertIn("Counted from model and reference evidence_trace objects", summary)


if __name__ == "__main__":
    unittest.main()
