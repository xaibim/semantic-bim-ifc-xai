from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "docs" / "literature" / "semantic_bim_ifc_bibliography_ieee.md"
MATRIX = ROOT / "benchmark" / "literature_capability_matrix.md"
README = ROOT / "README.md"
OVERVIEW = ROOT / "docs" / "research_overview.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized_text(path: Path) -> str:
    return " ".join(read_text(path).split())


def extract_entries(text: str) -> dict[str, str]:
    lines = text.splitlines()
    entries: dict[str, list[str]] = {}
    current_key: str | None = None
    for line in lines:
        match = re.match(r"^\[(\d+)\]", line)
        if match:
            current_key = match.group(1)
            entries[current_key] = [line]
            continue
        supp = re.match(r"^\[(S\d+)\]", line)
        if supp:
            current_key = supp.group(1)
            entries[current_key] = [line]
            continue
        if current_key is not None:
            entries[current_key].append(line)
    return {key: "\n".join(value) for key, value in entries.items()}


class TestPublicBibliographyAlignment(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bibliography = read_text(BIB)
        cls.matrix = read_text(MATRIX)
        cls.readme = read_text(README)
        cls.overview = read_text(OVERVIEW)
        cls.entries = extract_entries(cls.bibliography)

    def test_01_bibliography_exists(self) -> None:
        self.assertTrue(BIB.exists())

    def test_02_exact_seed_entries(self) -> None:
        ids = [int(match) for match in re.findall(r"(?m)^\[(\d+)\]", self.bibliography)]
        self.assertEqual(len(ids), 28)
        self.assertEqual(ids, list(range(1, 29)))
        self.assertEqual(set(ids), set(range(1, 29)))

    def test_03_supplementary_entries(self) -> None:
        supplementary = re.findall(r"(?m)^\[(S\d+)\]", self.bibliography)
        self.assertEqual(supplementary, ["S1", "S2"])

    def test_04_matrix_uses_seed_range_only(self) -> None:
        seed_ids = {int(match) for match in re.findall(r"\[(\d+)\]", self.matrix)}
        self.assertTrue(set(range(1, 29)).issubset(seed_ids))
        self.assertTrue(seed_ids.issubset(set(range(1, 29))))

    def test_05_matrix_links_bibliography(self) -> None:
        self.assertIn("../docs/literature/semantic_bim_ifc_bibliography_ieee.md", self.matrix)
        self.assertIn("docs/literature/semantic_bim_ifc_bibliography_ieee.md", self.readme)
        self.assertIn("literature/semantic_bim_ifc_bibliography_ieee.md", self.overview)
        self.assertNotIn("Canonical bibliography file:", self.overview)

    def test_06_minimal_correspondences(self) -> None:
        required = {
            "1": "ISO 19650-1:2018",
            "2": "ISO 19650-2:2018",
            "3": "10.1016/j.autcon.2013.09.001",
            "4": "10.5772/58445",
            "5": "ISO 16739-1:2024",
            "6": "10.1061/(ASCE)0887-3801(2010)24:1(25)",
            "7": "10.1007/s11831-021-09595-6",
            "8": "10.1061/(ASCE)CP.1943-5487.0000536",
            "9": "10.1016/j.autcon.2016.08.027",
            "10": "106905",
            "11": "105067",
            "12": "107066",
            "13": "106374",
            "14": "103375",
            "15": "10.32738/JEPPM-2024-0035",
            "16": "106707",
            "17": "7065",
            "18": "105369",
            "19": "Regulation (EU) 2024/1689",
            "20": "10.7326/M18-0850",
            "21": "10.11124/JBIES-20-00167",
            "22": "10.1016/j.artint.2018.07.007",
            "23": "Retrieval-augmented generation",
            "24": "10.1007/s11704-024-40231-1",
            "25": "10.35490/EC3.2025.218",
            "26": "pp. 9760-9779",
            "27": "04025142",
            "28": "10.35490/EC3.2025.265",
        }
        for ident, needle in required.items():
            with self.subTest(ident=ident):
                entry = self.entries[ident]
                if ident == "19":
                    entry = " ".join(entry.split())
                self.assertIn(needle, entry)

    def test_06b_corrected_metadata_details(self) -> None:
        self.assertIn("J. Poças Martins", self.entries["7"])
        self.assertIn("A. S. Guimarães", self.entries["7"])
        self.assertNotIn("Pozas Martins", self.entries["7"])
        self.assertNotIn("Guimaraes", self.entries["7"])
        self.assertIn("Art. no. 0035", self.entries["15"])
        entry_19 = " ".join(self.entries["19"].split())
        self.assertIn("European Parliament and Council of the European Union", entry_19)
        self.assertIn("amending Regulations", entry_19)
        self.assertIn("Artificial Intelligence Act", entry_19)
        self.assertIn("OJ L, 2024/1689", entry_19)
        self.assertIn("12 Jul. 2024", entry_19)
        self.assertIn("data.europa.eu/eli/reg/2024/1689/oj", entry_19)

    def test_07_peters_author_record(self) -> None:
        entry = self.entries["21"]
        for author in [
            "C. Marnie",
            "A. C. Tricco",
            "D. Pollock",
            "Z. Munn",
            "L. Alexander",
            "P. McInerney",
            "C. M. Godfrey",
            "H. Khalil",
        ]:
            with self.subTest(author=author):
                self.assertIn(author, entry)

    def test_08_named_authorships(self) -> None:
        self.assertIn("Hellin, S. Nousias, and A. Borrmann", self.entries["28"])
        self.assertIn("C. Du, S. Esser, S. Nousias, and A. Borrmann", self.entries["27"])
        self.assertIn("S. Jin", self.entries["S1"])
        self.assertIn("Z. Alwashah", self.entries["S2"])

    def test_08b_doi_uniqueness(self) -> None:
        doi_matches = re.findall(r"doi:\s*([^\s]+)", self.bibliography, flags=re.IGNORECASE)
        normalized = [match.lower() for match in doi_matches]
        self.assertEqual(len(normalized), len(set(normalized)))

    def test_09_prohibited_phrases_absent(self) -> None:
        forbidden_phrases = [
            "State" + "-of-the-art references",
            "should be verified before formal publication",
            "ISO 16739-1:2018",
            "Borrmann and Beetz",
            "in press",
            "Art. no. 106369",
            "24 entries canonical",
        ]
        text = self.bibliography
        for phrase in forbidden_phrases:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)

    def test_10_structure_statuses(self) -> None:
        text = self.bibliography
        for phrase in [
            "CURATED_POSITIONING_BIBLIOGRAPHY",
            "NON_SYSTEMATIC_POSITIONING_RESOURCE",
            "SEED_REFERENCE_COUNT = 28",
            "not a systematic review",
            "not a scoping-review result",
            "not a meta-analysis",
        ]:
            self.assertIn(phrase, text)

    def test_11_matrix_and_overview_links(self) -> None:
        self.assertIn("curated positioning bibliography", self.readme.lower())
        self.assertIn("curated positioning bibliography", self.overview.lower())
        self.assertIn("not results of a systematic or scoping review", self.readme.lower())
        self.assertNotIn("they are not a systematic or scoping review.", self.readme.lower())
        self.assertIn("not a completed systematic or scoping review", self.overview.lower())
        self.assertIn("literature/semantic_bim_ifc_bibliography_ieee.md", self.overview)
        self.assertNotIn("Canonical bibliography file:", self.overview)
        self.assertEqual(
            self.readme.count(
                "They are not results of a systematic or scoping review."
            ),
            1,
        )
        self.assertNotIn(
            "They are not a systematic or scoping review.",
            self.readme,
        )


    def test_12_narrative_limits(self) -> None:
        text = normalized_text(OVERVIEW)
        for phrase in [
            "can be ingested by any BIM authoring plugin or CDE system",
            "peer-review tool",
            "text metadata classification",
            "regulated structures",
        ]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)
        for phrase in [
            "current public artifact",
            "stored-record validation",
            "No comparative benchmark is executed",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertIn("Future model comparisons", text)
        self.assertIn(
            "comparison of different methods over frozen inputs and metrics",
            text,
        )
        self.assertIn(
            "No comparative benchmark is executed by the current public artifact",
            text,
        )
        for corruption in ["Ã", "Â", "â€", "�"]:
            with self.subTest(corruption=corruption):
                self.assertNotIn(corruption, read_text(OVERVIEW))
        self.assertIn(
            "natural language \u2192 engineering meaning \u2192 IFC candidate "
            "\u2192 information requirement \u2192 validation \u2192 evidence trace",
            text,
        )
        self.assertNotIn(
            "Enables researchers to run different LLMs on identical inputs",
            text,
        )
        self.assertNotIn(
            "**No comparative benchmark is executed**:",
            text,
        )


if __name__ == "__main__":
    unittest.main()
