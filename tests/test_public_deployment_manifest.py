from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "evidence" / "public_deployment_manifest.json"

ALLOWED_AVAILABILITY = {
    "RUNNING",
    "SLEEPING",
    "PAUSED",
    "BUILDING",
    "ERROR",
    "UNKNOWN",
    "NOT_CHECKED",
    "PUBLIC_PAGE_ACCESSIBLE",
    "URL_RESOLVABLE",
}

REPLAY_PATHS = {
    "app": "spaces/huggingface/app.py",
    "records": "spaces/huggingface/sample20_public_predictions.jsonl",
    "schema": "spaces/huggingface/schema_public_sample20_v2.json",
    "requirements": "spaces/huggingface/requirements.txt",
}

HARNESS_PATHS = {
    "app": "spaces/huggingface_harness/app.py",
    "records": "spaces/huggingface_harness/sample20_public_predictions.jsonl",
    "schema": "spaces/huggingface_harness/schema_public_sample20_v2.json",
    "requirements": "spaces/huggingface_harness/requirements.txt",
}

EXPECTED_URLS = {
    "replay": {
        "canonical_space_url": "https://huggingface.co/spaces/XAIBIM/semantic-xaibim-replay",
    },
    "harness": {
        "canonical_space_url": "https://huggingface.co/spaces/XAIBIM/semantic-xaibim-harness",
    },
}

FORBIDDEN_PATTERNS = [
    "/home/",
    "hostname",
    "username",
    "api key",
    "token",
    "cookie",
    "@",
    "bimaiblend",
]


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(rel_path: str) -> str:
    """Calculate SHA-256 from the canonical Git index blob."""
    result = subprocess.run(
        ["git", "ls-tree", "HEAD", rel_path],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    blob_hash = result.stdout.strip().split()[2]
    blob = subprocess.run(
        ["git", "cat-file", "-p", blob_hash],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return hashlib.sha256(blob.stdout).hexdigest()


class TestPublicDeploymentManifest(unittest.TestCase):
    def test_01_manifest_exists_and_valid_json(self) -> None:
        self.assertTrue(MANIFEST_PATH.is_file())
        data = load_manifest()
        self.assertIsInstance(data, dict)

    def test_02_contract_fields_exact(self) -> None:
        data = load_manifest()
        self.assertEqual("public_runtime_deployment_manifest", data["artifact_type"])
        self.assertEqual("1.0", data["artifact_version"])
        self.assertEqual(
            "4970d7c99abcb1bfd244ea42c6d4295cccf812b5", data["source_commit"]
        )
        self.assertEqual("REMOTE_EQUIVALENCE_VERIFIED", data["status"])

    def test_03_scope_boundary(self) -> None:
        data = load_manifest()
        boundary = data["scope_boundary"]
        self.assertTrue(boundary["link_identity_recorded"])
        self.assertTrue(boundary["availability_is_dated_snapshot"])
        self.assertTrue(boundary["remote_artifact_equivalence_verified"])
        self.assertFalse(boundary["production_readiness"])

    def test_04_replay_paths_exist(self) -> None:
        for key, rel in REPLAY_PATHS.items():
            with self.subTest(key=key, path=rel):
                self.assertTrue(
                    (ROOT / rel).is_file(),
                    f"Replay {key} path missing: {rel}",
                )

    def test_05_harness_paths_exist(self) -> None:
        for key, rel in HARNESS_PATHS.items():
            with self.subTest(key=key, path=rel):
                self.assertTrue(
                    (ROOT / rel).is_file(),
                    f"Harness {key} path missing: {rel}",
                )

    def test_06_replay_hashes_match(self) -> None:
        data = load_manifest()
        replay = data["packages"]["replay"]["local_source"]
        for key, rel in REPLAY_PATHS.items():
            with self.subTest(key=key):
                expected = sha256_file(rel)
                actual = replay[key]["sha256"]
                self.assertEqual(expected, actual)

    def test_07_harness_hashes_match(self) -> None:
        data = load_manifest()
        harness = data["packages"]["harness"]["local_source"]
        for key, rel in HARNESS_PATHS.items():
            with self.subTest(key=key):
                expected = sha256_file(rel)
                actual = harness[key]["sha256"]
                self.assertEqual(expected, actual)

    def test_08_replay_urls_exact(self) -> None:
        data = load_manifest()
        replay = data["packages"]["replay"]
        self.assertEqual(EXPECTED_URLS["replay"]["canonical_space_url"], replay["canonical_space_url"])

    def test_09_harness_urls_exact(self) -> None:
        data = load_manifest()
        harness = data["packages"]["harness"]
        self.assertEqual(EXPECTED_URLS["harness"]["canonical_space_url"], harness["canonical_space_url"])

    def test_10_remote_fields_populated(self) -> None:
        data = load_manifest()
        for pkg_name in ("replay", "harness"):
            pkg = data["packages"][pkg_name]
            remote = pkg["remote_deployment"]
            self.assertIsNotNone(remote["commit"])
            self.assertIsNotNone(remote["app_sha256"])
            self.assertIsNotNone(remote["records_sha256"])
            self.assertIsNotNone(remote["schema_sha256"])
            self.assertIsNotNone(remote["requirements_sha256"])
            self.assertIsNotNone(remote["audited_at_utc"])

    def test_11_artifact_equivalence_verified(self) -> None:
        data = load_manifest()
        for pkg_name in ("replay", "harness"):
            pkg = data["packages"][pkg_name]
            remote = pkg["remote_deployment"]
            self.assertEqual(
                "VERIFIED",
                remote["artifact_equivalence_status"],
            )

    def test_12_remote_equivalence_verified(self) -> None:
        data = load_manifest()
        self.assertTrue(data["scope_boundary"]["remote_artifact_equivalence_verified"])

    def test_13_no_private_paths_or_credentials(self) -> None:
        text = read_text(MANIFEST_PATH)
        for pattern in FORBIDDEN_PATTERNS:
            self.assertNotIn(pattern, text)

    def test_14_no_network_calls_in_test_module(self) -> None:
        import ast

        module_source = Path(__file__).read_text(encoding="utf-8")
        module_ast = ast.parse(module_source)
        forbidden_modules = {"requests", "httpx", "aiohttp"}
        forbidden_calls = {"get", "post", "put", "patch", "delete", "head", "options", "urlopen"}
        for node in ast.walk(module_ast):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotIn(alias.name.split(".")[0], forbidden_modules)
            elif isinstance(node, ast.ImportFrom) and node.module:
                self.assertNotIn(node.module.split(".")[0], forbidden_modules)
                self.assertNotEqual("urllib.request", node.module)
            elif isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute):
                    self.assertNotIn(func.attr.lower(), forbidden_calls)

    def test_15_self_test_status_executed(self) -> None:
        data = load_manifest()
        for pkg_name in ("replay", "harness"):
            pkg = data["packages"][pkg_name]
            remote = pkg["remote_deployment"]
            self.assertEqual(
                "PASS",
                remote["self_test_status"],
            )

    def test_16_limitations_present(self) -> None:
        data = load_manifest()
        self.assertIsInstance(data["limitations"], list)
        self.assertGreater(len(data["limitations"]), 0)


if __name__ == "__main__":
    unittest.main()
