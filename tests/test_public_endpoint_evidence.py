from __future__ import annotations

import ast
import json
import re
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_PATH = ROOT / "docs" / "evidence" / "public_endpoint_audit.json"
PUBLIC_EVIDENCE_PATH = ROOT / "PUBLIC_EVIDENCE.md"
RUNTIME_LINKS_PATH = ROOT / "docs" / "evidence" / "public_runtime_links.json"
KAGGLE_MANIFEST_PATH = ROOT / "docs" / "evidence" / "kaggle_qlora_manifest.json"
RESOURCE_CALIBRATION_PATH = ROOT / "benchmark" / "resource_calibration.json"
LOCAL_PROXY_PATH = ROOT / "benchmark" / "resource_microbenchmark_local.json"
RESOURCE_CAPACITY_PLAN_PATH = ROOT / "docs" / "methodology" / "resource_capacity_plan.md"
SOFTWARE_COMPATIBILITY_PATH = ROOT / "docs" / "methodology" / "software_and_platform_compatibility.md"
HUMAN_REVIEW_PATH = ROOT / "docs" / "methodology" / "human_review_and_operational_risk.md"
DATA_RELEASE_PATH = ROOT / "docs" / "methodology" / "data_governance_and_release.md"
LEAKAGE_PROTOCOL_PATH = ROOT / "docs" / "methodology" / "dataset_governance_split_and_leakage_protocol.md"
FREEZE_MANIFEST_PATH = ROOT / "docs" / "methodology" / "experimental_scale_and_freeze_manifest.md"

EXPECTED_URLS = {
    "repository": "https://github.com/xaibim/semantic-bim-ifc-xai",
    "replay_gateway": "https://huggingface.co/spaces/XAIBIM/semantic-xaibim-replay",
    "replay_runtime": "https://huggingface.co/spaces/bimaiblend/semantic-xaibim-replay",
    "harness_gateway": "https://huggingface.co/spaces/XAIBIM/semantic-xaibim-harness",
    "harness_runtime": "https://huggingface.co/spaces/bimaiblend/semantic-xaibim-harness",
    "kaggle_notebook": "https://www.kaggle.com/code/xaibim/semantic-bim-ifc-xai",
}

REQUIRED_PUBLIC_EVIDENCE_LINKS = [
    "docs/evidence/public_runtime_links.json",
    "docs/evidence/public_endpoint_audit.json",
    "docs/evidence/kaggle_qlora_manifest.json",
    "benchmark/resource_calibration.json",
    "benchmark/resource_microbenchmark_local.json",
    "docs/methodology/resource_capacity_plan.md",
    "docs/methodology/software_and_platform_compatibility.md",
    "docs/methodology/human_review_and_operational_risk.md",
    "docs/methodology/data_governance_and_release.md",
    "docs/methodology/dataset_governance_split_and_leakage_protocol.md",
    "docs/methodology/experimental_scale_and_freeze_manifest.md",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_utc_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class TestPublicEndpointEvidence(unittest.TestCase):
    def test_01_artifacts_exist(self) -> None:
        self.assertTrue(ARTIFACT_PATH.is_file())
        self.assertTrue(PUBLIC_EVIDENCE_PATH.is_file())

    def test_02_json_contract_exact(self) -> None:
        data = load_json(ARTIFACT_PATH)
        self.assertEqual("public_endpoint_verification_snapshot", data["artifact_type"])
        self.assertEqual("1.0", data["artifact_version"])
        self.assertEqual("ANONYMOUS_PUBLIC_PAGE_INSPECTION", data["audit_mode"])
        self.assertEqual("public_runtime_links.json", data["canonical_link_registry"])
        self.assertEqual(
            {
                "identity_distinct_from_availability": True,
                "snapshot_not_availability_guarantee": True,
                "kaggle_content_independently_reproduced": False,
                "professional_or_normative_validation": False,
            },
            data["interpretation_boundary"],
        )

    def test_03_urls_and_timestamp(self) -> None:
        data = load_json(ARTIFACT_PATH)
        endpoints = data["endpoints"]
        self.assertEqual(EXPECTED_URLS["repository"], endpoints["repository"]["url"])
        self.assertEqual(EXPECTED_URLS["replay_gateway"], endpoints["replay_gateway"]["url"])
        self.assertEqual(EXPECTED_URLS["replay_runtime"], endpoints["replay_runtime"]["url"])
        self.assertEqual(EXPECTED_URLS["harness_gateway"], endpoints["harness_gateway"]["url"])
        self.assertEqual(EXPECTED_URLS["harness_runtime"], endpoints["harness_runtime"]["url"])
        self.assertEqual(EXPECTED_URLS["kaggle_notebook"], endpoints["kaggle_notebook"]["url"])
        self.assertEqual(set(EXPECTED_URLS.values()), {entry["url"] for entry in endpoints.values()})

        audited_at = parse_utc_timestamp(data["audited_at_utc"])
        self.assertIsNotNone(audited_at.tzinfo)
        self.assertEqual(timezone.utc, audited_at.tzinfo)

    def test_04_endpoint_states_are_conservative(self) -> None:
        data = load_json(ARTIFACT_PATH)
        endpoints = data["endpoints"]
        self.assertEqual("PUBLIC_PAGE_ACCESSIBLE", endpoints["repository"]["verification_status"])
        self.assertEqual("RUNNING", endpoints["replay_gateway"]["observed_state"])
        self.assertEqual("VALID", endpoints["replay_runtime"]["identity_status"])
        self.assertEqual("RUNNING", endpoints["replay_runtime"]["observed_state"])
        self.assertEqual("RUNNING", endpoints["harness_gateway"]["observed_state"])
        self.assertEqual("RUNNING", endpoints["harness_runtime"]["observed_state"])
        self.assertEqual(
            "URL_RESOLVABLE_CONTENT_NOT_RECOVERED_BY_ANONYMOUS_AUTOMATED_AUDIT",
            endpoints["kaggle_notebook"]["verification_status"],
        )
        self.assertTrue(endpoints["replay_runtime"]["checked_anonymously"])
        self.assertTrue(endpoints["harness_runtime"]["checked_anonymously"])
        self.assertFalse(endpoints["kaggle_notebook"]["content_recovered"])
        self.assertTrue(data["interpretation_boundary"]["snapshot_not_availability_guarantee"])

    def test_05_public_evidence_index_references_required_artifacts(self) -> None:
        text = read_text(PUBLIC_EVIDENCE_PATH)
        for token in REQUIRED_PUBLIC_EVIDENCE_LINKS:
            self.assertIn(token, text)
        self.assertIn("Public executable evidence", text)
        self.assertIn("Limited external verification", text)
        self.assertIn("Preliminary aggregate evidence", text)
        self.assertIn("Local proxy evidence", text)
        self.assertIn("Planning and governance", text)

    def test_06_no_private_paths_or_network_calls(self) -> None:
        data_text = read_text(ARTIFACT_PATH) + "\n" + read_text(PUBLIC_EVIDENCE_PATH)
        self.assertNotIn("C:" + "\\", data_text)
        self.assertNotIn("/home/", data_text)
        self.assertNotIn("hostname", data_text.lower())
        self.assertNotIn("username", data_text.lower())
        self.assertNotIn("api key", data_text.lower())
        self.assertNotIn("token", data_text.lower())
        self.assertNotIn("cookie", data_text.lower())

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

        for path in [
            RUNTIME_LINKS_PATH,
            KAGGLE_MANIFEST_PATH,
            RESOURCE_CALIBRATION_PATH,
            LOCAL_PROXY_PATH,
            RESOURCE_CAPACITY_PLAN_PATH,
            SOFTWARE_COMPATIBILITY_PATH,
            HUMAN_REVIEW_PATH,
            DATA_RELEASE_PATH,
            LEAKAGE_PROTOCOL_PATH,
            FREEZE_MANIFEST_PATH,
        ]:
            self.assertTrue(path.is_file(), str(path))


if __name__ == "__main__":
    unittest.main()
