from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {".md", ".txt", ".yml", ".yaml", ".json", ".jsonl", ".cff", ".py", ".toml", ".ini", ".cfg"}
PROGRAM_TOKENS = [
    "C" + "PCA",
    "R" + "NCA",
    "F" + "CCN",
]
PHASE_TOKEN = "A" + "1"
EXCLUDED_NEUTRALITY_PATHS = {
    # These historical IFC4 artifacts do not demonstrate professional sufficiency.
    ROOT / "docs" / "methodology" / "schema_contract_map.md",
    ROOT / "tests" / "test_public_context_neutrality.py",
    ROOT / "tests" / "test_public_sample20_ifc4_relationship_corrections.py",
}


def tracked_files() -> list[str]:
    output = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    return [line for line in output.splitlines() if line.strip()]


def token_pattern(token: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![A-Za-z0-9]){re.escape(token)}(?![A-Za-z0-9])", re.IGNORECASE)


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS


class TestPublicContextNeutrality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tracked = tracked_files()

    def fail_matches(self, matches: list[str]) -> None:
        self.fail("\n".join(matches))

    def assert_no_token(self, token: str) -> None:
        pattern = token_pattern(token)
        matches: list[str] = []
        for rel in self.tracked:
            rel_path = Path(rel)
            if pattern.search(rel.lower()):
                matches.append(f"token={token} path={rel}")
                continue
            for part in rel_path.parts:
                if pattern.search(part.lower()):
                    matches.append(f"token={token} path={rel} component={part}")
                    break
            if not is_text_file(rel_path):
                continue
            try:
                text = (ROOT / rel_path).read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                if pattern.search(line):
                    matches.append(f"token={token} path={rel} line={lineno}")
                    break
        if matches:
            self.fail_matches(matches)

    def test_01_public_context_tokens_absent(self):
        for token in [*PROGRAM_TOKENS, PHASE_TOKEN]:
            with self.subTest(token=token):
                self.assert_no_token(token)

    def test_02_pset_audit_public_phrasing(self):
        text = (
            ROOT
            / "benchmark"
            / ("public_sample20_" + "if" + "c4" + "_pset_audit.md")
        ).read_text(encoding="utf-8").lower()
        self.assertIn("future expanded research dataset", text)
        self.assertIn("broader future research dataset", text)

    def test_03_dataset_methodology_public_boundary(self):
        text = " ".join((ROOT / "docs" / "methodology" / "dataset_construction_and_training_readiness.md").read_text(encoding="utf-8").lower().split())
        self.assertIn("plain text outputs do not by themselves guarantee alignment with canonical catalogues or structured contracts.", text)
        self.assertIn("broader / private or planned", text)
        self.assertIn("current public executable", text)
        self.assertIn("external-source supportedness is not evaluated", text)

    def test_04_readme_public_qlora_wording(self):
        text = " ".join((ROOT / "README.md").read_text(encoding="utf-8").split())
        lower = text.lower()
        self.assertIn("private pilot with public aggregate evidence only; not a comparative benchmark result", lower)
        self.assertIn("no private adapters or checkpoints are public.", lower)
        self.assertNotIn("not a public result", lower)
        self.assertNotIn("no public private adapters/checkpoints.", lower)

    def test_05_no_internal_process_tokens_in_tracked_text(self):
        pr_pattern = r"\b" + "PR" + r"\d+\b"
        micro_pattern = r"\b" + "MICRO" + r"[-_]\d+[A-Z]?\b"
        stop_pr_pattern = r"\b" + "STOP" + r"_PR"
        patterns = {
            "pr": re.compile(pr_pattern, re.IGNORECASE),
            "micro": re.compile(micro_pattern, re.IGNORECASE),
            "stop_pr": re.compile(stop_pr_pattern, re.IGNORECASE),
        }
        matches: list[str] = []
        tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
        for rel in tracked:
            rel_path = Path(rel)
            abs_path = (ROOT / rel_path).resolve()
            if abs_path in EXCLUDED_NEUTRALITY_PATHS:
                continue
            if not is_text_file(rel_path):
                continue
            try:
                text = abs_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for name, pattern in patterns.items():
                if pattern.search(text):
                    matches.append(f"token_group={name} path={rel}")
                    break
        if matches:
            self.fail_matches(matches)


if __name__ == "__main__":
    unittest.main()
