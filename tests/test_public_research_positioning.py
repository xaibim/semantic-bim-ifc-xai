from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VALIDATION_GATES = ROOT / "docs" / "methodology" / "validation_gates.md"

REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "PUBLIC_EVIDENCE.md",
    ROOT / "docs" / "literature" / "semantic_bim_ifc_bibliography_ieee.md",
    ROOT / "benchmark" / "baseline_matrix.md",
    ROOT / "benchmark" / "literature_capability_matrix.md",
    ROOT / "docs" / "methodology" / "research_positioning_and_originality.md",
    ROOT / "docs" / "methodology" / "dataset_construction_and_benchmark_readiness.md",
    ROOT / "tests" / "test_public_research_positioning.py",
]

RESEARCH_STATUS_PAIRS = [
    ("Structured contract", "CURRENT_PUBLIC_STRUCTURAL", "PLANNED"),
    ("Stored-record validation", "CURRENT_PUBLIC_EXECUTABLE", "PLANNED"),
    ("Dataset governance", "CURRENT_PUBLIC_DOCUMENTED", "PLANNED"),
    ("Root-case grouping", "NOT_CURRENTLY_EVALUATED", "PLANNED"),
    ("Duplicate control", "CURRENT_PUBLIC_DOCUMENTED", "PLANNED"),
    ("Leakage control", "CURRENT_PUBLIC_DOCUMENTED", "PLANNED"),
    ("Frozen splits", "NOT_CURRENTLY_EVALUATED", "PLANNED"),
    ("Resolvable IFC grounding", "NOT_CURRENTLY_EVALUATED", "PLANNED"),
    ("Evidence supportedness", "NOT_CURRENTLY_EVALUATED", "PLANNED"),
    ("Expected-negative handling", "CURRENT_PUBLIC_EXECUTABLE", "PLANNED"),
    ("Safe recovery", "CURRENT_PUBLIC_STRUCTURAL", "PLANNED"),
    ("Capability stratification", "NOT_CURRENTLY_EVALUATED", "PLANNED"),
    ("Complexity stratification", "NOT_CURRENTLY_EVALUATED", "PLANNED"),
    ("Professional review", "NOT_CURRENTLY_EVALUATED", "PLANNED"),
    ("Statistical evaluation", "NOT_CURRENTLY_EVALUATED", "PLANNED"),
    ("Computational measurement", "CURRENT_PUBLIC_DOCUMENTED", "PLANNED"),
    ("Comparative benchmark", "CURRENT_PUBLIC_DOCUMENTED", "PLANNED"),
    ("Optional model adaptation", "CURRENT_PUBLIC_DOCUMENTED", "CONDITIONAL"),
]

POSITIVES_CORE_DOCS = [
    ROOT / "README.md",
    ROOT / "PUBLIC_EVIDENCE.md",
    ROOT / "benchmark" / "baseline_matrix.md",
    ROOT / "docs" / "methodology" / "dataset_construction_and_benchmark_readiness.md",
    ROOT / "docs" / "methodology" / "dataset_scope_and_compute_scaling.md",
    ROOT / "docs" / "methodology" / "xai_evaluation_position.md",
    ROOT / "docs" / "methodology" / "xai_evidence_positioning.md",
]

CHANGED_MARKDOWN_DOCS = [
    ROOT / "README.md",
    ROOT / "PUBLIC_EVIDENCE.md",
    ROOT / "benchmark" / "baseline_matrix.md",
    ROOT / "benchmark" / "literature_capability_matrix.md",
    ROOT / "docs" / "methodology" / "research_positioning_and_originality.md",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(path: Path) -> str:
    return " ".join(read_text(path).split())


def lower_normalized(path: Path) -> str:
    return normalized(path).lower()


class TestPublicResearchPositioning(unittest.TestCase):
    def test_01_required_files_exist(self):
        old_path = (
            ROOT
            / "docs"
            / "methodology"
            / ("dataset_construction_and_" + "training_readiness.md")
        )
        self.assertFalse(old_path.exists())
        for path in REQUIRED_FILES:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), msg=str(path))

    def test_02_readme_links_exact_relative_paths(self):
        text = read_text(ROOT / "README.md")
        self.assertIn("docs/methodology/research_positioning_and_originality.md", text)
        self.assertIn("benchmark/literature_capability_matrix.md", text)
        self.assertIn("docs/literature/semantic_bim_ifc_bibliography_ieee.md", text)
        self.assertIn("benchmark/baseline_matrix.md", text)

    def test_03_research_positioning_headings(self):
        text = read_text(ROOT / "docs" / "methodology" / "research_positioning_and_originality.md")
        headings = [
            "## 1. Purpose",
            "## 2. Product Boundary",
            "## 3. What Is Already Established",
            "## 4. Claims Not Made",
            "## 5. Current Public Contribution",
            "## 6. Provisional Research Gap",
            "## 7. Planned Methodological Contribution",
            "## 8. Evidence Boundary",
            "## 9. Limitations",
        ]
        for heading in headings:
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

    def test_04_no_delimites_typo(self):
        text = read_text(ROOT / "docs" / "methodology" / "research_positioning_and_originality.md")
        self.assertNotIn("This document delimites", text)

    def test_05_product_boundary_rows(self):
        text = lower_normalized(ROOT / "docs" / "methodology" / "research_positioning_and_originality.md")
        self.assertIn("product | purpose | audience | public repository status", text)
        rows = [
            "public scientific repository | public scientific research artifact for reproducible semantic bim/ifc evidence. | scientific readers and reviewers. | public, neutral and reusable.",
            "external application or administrative package | submission material for a specific external call. | funding, procurement or administrative reviewers. | not part of this repository.",
            "future scientific publications | planned dissemination in future articles or proceedings. | academic and professional readership. | not yet published or peer reviewed.",
            "private or controlled research data | restricted datasets and controlled experimental inputs. | internal research team only. | not distributed publicly.",
        ]
        for row in rows:
            with self.subTest(row=row):
                self.assertIn(row, text)

    def test_06_current_public_contribution(self):
        text = lower_normalized(ROOT / "docs" / "methodology" / "research_positioning_and_originality.md")
        phrases = [
            "sample20 as a minimal sanitized reproducibility fixture",
            "20 stored records",
            "18 valid cases",
            "2 expected canonical rejections",
            "strict json schema draft 2020-12 contract",
            "deterministic stored-record validation",
            "separate parsing, schema, fixture-contract and integrity states",
            "canonical three-copy integrity checking",
            "ifc4 pset class-applicability audit",
            "ifc4 relationship schema-participation audit",
            "evidence-trace structural validation",
            "external-source supportedness not evaluated",
            "preliminary qlora aggregate compute-feasibility evidence",
            "comparative benchmark planned and not executed",
        ]
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertIn(
            "it does not include live generation, a final benchmark, or any claim of professional correctness from ifc schema participation.",
            text,
        )
        self.assertNotIn("- no live generation;", text)
        self.assertNotIn("- no final benchmark;", text)
        self.assertNotIn("- no claim of professional correctness from ifc schema participation.", text)

    def test_07_research_status_table(self):
        text = read_text(ROOT / "docs" / "methodology" / "research_positioning_and_originality.md")
        for dimension, current_status, planned_status in RESEARCH_STATUS_PAIRS:
            pattern = rf"(?m)^\| {re.escape(dimension)} \| {re.escape(current_status)} \| {re.escape(planned_status)} \|"
            with self.subTest(dimension=dimension):
                self.assertRegex(text, pattern)

    def test_08_evidence_levels(self):
        text = read_text(ROOT / "docs" / "methodology" / "research_positioning_and_originality.md")
        for phrase in [
            "E0",
            "TRACE_PRESENT",
            "E1",
            "REFERENCE_RESOLVABLE",
            "E2",
            "CLAIM_SUPPORTED",
            "E3",
            "PROFESSIONALLY_SUFFICIENT",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_09_current_artifact_demonstrates_e0_only(self):
        text = lower_normalized(ROOT / "docs" / "methodology" / "research_positioning_and_originality.md")
        self.assertIn("the current public artifact demonstrates e0 only", text)

    def test_10_seed_bibliography_identifiers(self):
        text = read_text(ROOT / "benchmark" / "literature_capability_matrix.md")
        identifiers = {int(match) for match in re.findall(r"\[(\d+)\]", text)}
        self.assertEqual(identifiers, set(range(1, 29)))

    def test_11_literature_matrix_families(self):
        text = lower_normalized(ROOT / "benchmark" / "literature_capability_matrix.md")
        families = [
            "iso 19650-1 and iso 19650-2",
            "iso 16739-1 and exchange-model research",
            "bim lifecycle information-management research",
            "bim semantic-enrichment reviews",
            "semantic nlp bim extension",
            "semantic nlp and logic reasoning for code checking",
            "bim-llm workflow reviews",
            "prompt-based bim information search",
            "ontology-aided multi-constraint querying",
            "query dsl and library-function alignment",
            "spatial bim query systems",
            "llm interpretation of building regulations",
            "llm-based bim compliance checking",
            "bim and knowledge-graph compliance checking",
            "ethics and ai governance in aeco",
            "retrieval-augmented generation research",
            "autonomous-agent and tool-use research",
            "multi-agent systems",
            "text2bim",
            "ifc-bench and recent ifc evaluation research",
        ]
        for family in families:
            with self.subTest(family=family):
                self.assertIn(family, text)

    def test_12_established_in_literature_count(self):
        text = read_text(ROOT / "benchmark" / "literature_capability_matrix.md")
        self.assertEqual(text.count("ESTABLISHED_IN_LITERATURE"), 20)

    def test_13_literature_foundations_and_notes(self):
        text = read_text(ROOT / "benchmark" / "literature_capability_matrix.md")
        phrases = [
            "Methodological and Explanatory Foundations",
            "[20], [21]",
            "[22]",
            "Bibliography Contract",
            "Canonical source metadata is defined in",
            "Seed identifiers `[1]` through `[28]`",
            "Supplementary entries `[S1]` and `[S2]`",
            "positioning resource",
            "not the result of a systematic or scoping review",
            "Query DSL and library-function alignment",
            "Text2BIM",
            "IFC-Bench and recent IFC evaluation research",
        ]
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_13b_validation_gates_bibliography_alignment(self):
        text = read_text(ROOT / "docs" / "methodology" / "validation_gates.md")
        normalized = " ".join(text.split())
        self.assertIn("experiment-specific values remain `TO_BE_FROZEN` before execution", normalized)
        self.assertIn("The protocol structure is public and versioned", normalized)
        self.assertNotIn("current public planned methodology is frozen for future use", text)
        self.assertNotIn("The current public planned methodology is public and versioned", normalized)

    def test_13c_bibliography_link_in_readme(self):
        text = read_text(ROOT / "README.md")
        self.assertIn("docs/literature/semantic_bim_ifc_bibliography_ieee.md", text)

    def test_14_baseline_matrix_rows_and_statuses(self):
        text = read_text(ROOT / "benchmark" / "baseline_matrix.md")
        expected_rows = {
            "A": r"(?m)^\| A \| Deterministic IFC/schema/catalogue lookup \| REQUIRED \|",
            "B": r"(?m)^\| B \| Base LLM, prompt-only \| REQUIRED \|",
            "C": r"(?m)^\| C \| Base LLM with retrieved IFC/bSDD/IDS context \| REQUIRED \|",
            "D": r"(?m)^\| D \| Graph or ontology-grounded retrieval \| CONDITIONAL \|",
            "E": r"(?m)^\| E \| Tool-using adaptive IFC exploration \| CONDITIONAL \|",
            "F": r"(?m)^\| F \| Single-agent planner \| OPTIONAL \|",
            "G": r"(?m)^\| G \| Multi-agent workflow \| OPTIONAL \|",
            "H": r"(?m)^\| H \| QLoRA-adapted model \| OPTIONAL_AFTER_GATES \|",
        }
        for ident, pattern in expected_rows.items():
            with self.subTest(ident=ident):
                self.assertRegex(text, pattern, msg=f"Missing or mismatched row for {ident}")

    def test_15_baseline_identifiers_unique(self):
        text = read_text(ROOT / "benchmark" / "baseline_matrix.md")
        for ident in "ABCDEFGH":
            with self.subTest(ident=ident):
                self.assertEqual(len(re.findall(rf"^\| {ident} \|", text, flags=re.MULTILINE)), 1)

    def test_16_baseline_h_q_lora_and_d_not_q_lora(self):
        text = read_text(ROOT / "benchmark" / "baseline_matrix.md")
        self.assertIn("| H | QLoRA-adapted model | OPTIONAL_AFTER_GATES |", text)
        d_line = re.search(r"^\| D \|.*$", text, flags=re.MULTILINE)
        self.assertIsNotNone(d_line)
        self.assertNotIn("QLoRA", d_line.group(0))

    def test_17_planned_metrics_present(self):
        text = lower_normalized(ROOT / "benchmark" / "baseline_matrix.md")
        metrics = [
            "strict schema validity",
            "reference-resolution rate",
            "entity-grounding accuracy",
            "evidence-supportedness precision",
            "evidence-supportedness recall",
            "expected-negative accuracy",
            "abstention precision",
            "missing-input recall",
            "safe-recovery rate",
            "invalid ifc claim rate",
            "task-family stratification",
            "complexity-level stratification",
            "repeated-run variability",
            "wall-clock time",
            "cpu core.hours",
            "gpu.hours",
            "peak ram",
            "peak vram",
            "storage footprint",
        ]
        for metric in metrics:
            with self.subTest(metric=metric):
                self.assertIn(metric, text)
        self.assertIn("cannot be calculated from sample20", text)

    def test_18_readme_updates(self):
        text = lower_normalized(ROOT / "README.md")
        phrases = [
            "eight-family baseline matrix",
            "deterministic lookup",
            "retrieved ifc/bsdd/ids context",
            "multi-agent workflows",
            "optional qlora adaptation",
            "planned",
            "not executed",
        ]
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        expected = (
            "this repository is a general public scientific research artifact. it is not "
            "the application package, technical resource request or administrative "
            "documentation of any specific funding or computing call."
        )
        self.assertIn(expected, text)
        self.assertEqual(
            text.count("this repository is a general public scientific research artifact"),
            1,
        )

    def test_19_no_positive_priority_claims(self):
        for path in POSITIVES_CORE_DOCS:
            text = lower_normalized(path)
            for phrase in [
                "first bim-llm system",
                "first semantic bim dataset",
                "first natural-language ifc benchmark",
                "first ifc benchmark",
                "first bim multi-agent framework",
                "first llm-based compliance checker",
                "first text-to-bim method",
                "state-of-the-art system",
                "proven superiority",
                "general aeco generalization",
                "iso compliant ai",
                "ai act compliant",
                "professionally certified",
            ]:
                with self.subTest(path=path, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_20_no_application_specific_tokens(self):
        forbidden_markdown = [
            "C" + "PCA",
            "My" + "FCT",
            "FCT/" + "C" + "PCA",
            "F" + "CCN",
            "R" + "NCA",
            "lote" + " E",
            "funding" + " application",
            "resource" + " application",
            "advanced" + " computing access work",
            "advanced" + "-computing access work",
            "planned" + " advanced computing work",
            "planned" + " advanced-computing work",
        ]
        word_boundary_tokens = ["A" + "0", "A" + "1", "A" + "2", "A" + "3"]
        for path in CHANGED_MARKDOWN_DOCS:
            text = read_text(path)
            low = text.lower()
            for phrase in forbidden_markdown:
                with self.subTest(path=path, phrase=phrase):
                    self.assertNotIn(phrase.lower(), low)
            for token in word_boundary_tokens:
                with self.subTest(path=path, token=token):
                    self.assertIsNone(re.search(rf"\b{re.escape(token)}\b", text, flags=re.IGNORECASE))

    def test_21_validation_gates_baseline_matrix_alignment(self):
        text = read_text(VALIDATION_GATES)
        text_norm = lower_normalized(VALIDATION_GATES)
        self.assertIn("../../benchmark/baseline_matrix.md", text)
        rows = {
            "A": r"(?m)^\| A \| Deterministic IFC/schema/catalogue lookup \| REQUIRED \|$",
            "B": r"(?m)^\| B \| Base LLM, prompt-only \| REQUIRED \|$",
            "C": r"(?m)^\| C \| Base LLM with retrieved IFC/bSDD/IDS context \| REQUIRED \|$",
            "D": r"(?m)^\| D \| Graph or ontology-grounded retrieval \| CONDITIONAL \|$",
            "E": r"(?m)^\| E \| Tool-using adaptive IFC exploration \| CONDITIONAL \|$",
            "F": r"(?m)^\| F \| Single-agent planner \| OPTIONAL \|$",
            "G": r"(?m)^\| G \| Multi-agent workflow \| OPTIONAL \|$",
            "H": r"(?m)^\| H \| QLoRA-adapted model \| OPTIONAL_AFTER_GATES \|$",
        }
        for ident, pattern in rows.items():
            with self.subTest(ident=ident):
                self.assertRegex(text, pattern)
                self.assertEqual(len(re.findall(pattern, text)), 1)
        self.assertIn("No comparative baseline results", text)
        self.assertIn("not presumed superior", text)
        self.assertIn("dataset-quality", text_norm)
        self.assertIn("required baseline gates", text_norm)

        d_line = re.search(r"(?m)^\| D \|.*$", text)
        h_line = re.search(r"(?m)^\| H \|.*$", text)
        self.assertIsNotNone(d_line)
        self.assertIsNotNone(h_line)
        self.assertNotIn("QLoRA", d_line.group(0))
        self.assertIn("QLoRA", h_line.group(0))
        self.assertNotIn("D = QLoRA", text)
        self.assertNotIn("E = graph/ontology", text)
        self.assertNotIn("D = QLoRA".lower(), text.lower())
        self.assertNotIn("E = graph/ontology".lower(), text.lower())

        table_rows = re.findall(r"(?m)^\| ([A-H]) \|", text)
        for ident in "ABCDEFGH":
            with self.subTest(unique_ident=ident):
                self.assertEqual(table_rows.count(ident), 1)


if __name__ == "__main__":
    unittest.main()
