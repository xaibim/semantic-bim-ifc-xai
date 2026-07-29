from __future__ import annotations

import getpass
import hashlib
import json
import platform
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_JSON = ROOT / "benchmark" / "resource_microbenchmark_local.json"
ARTIFACT_MD = ROOT / "benchmark" / "resource_microbenchmark_local.md"
RESOURCE_CALIBRATION_JSON = ROOT / "benchmark" / "resource_calibration.json"
RESOURCE_CAPACITY_PLAN = ROOT / "docs" / "methodology" / "resource_capacity_plan.md"


def canonical_hash(payload: dict) -> str:
    without_hash = dict(payload)
    without_hash.pop("artifact_sha256", None)
    canonical = json.dumps(without_hash, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class ResourceMicrobenchmarkTest(unittest.TestCase):
    def test_01_artifacts_exist(self) -> None:
        self.assertTrue(ARTIFACT_JSON.is_file())
        self.assertTrue(ARTIFACT_MD.is_file())

    def test_02_json_contract(self) -> None:
        data = json.loads(ARTIFACT_JSON.read_text(encoding="utf-8"))
        self.assertEqual("local_proxy_resource_microbenchmark", data["artifact_type"])
        self.assertEqual("1.0", data["artifact_version"])
        self.assertEqual("LOCAL_PROXY_MEASUREMENT_NOT_DEUCALION", data["status"])
        self.assertEqual(
            {
                "deucalion_measurement": False,
                "a100_measurement": False,
                "capacity_values_changed": False,
                "m1_on_platform_measurement_required": True,
            },
            data["scope_boundary"],
        )

    def test_03_workload_dimensions(self) -> None:
        data = json.loads(ARTIFACT_JSON.read_text(encoding="utf-8"))
        self.assertEqual(20_000, data["workload"]["logical_records"])
        self.assertEqual(5, data["workload"]["warmup_rounds"])
        self.assertEqual(10, data["workload"]["measured_rounds"])
        self.assertEqual(1_000, data["workload"]["repetitions"])

    def test_04_cpu_metrics(self) -> None:
        data = json.loads(ARTIFACT_JSON.read_text(encoding="utf-8"))
        cpu_results = data["cpu_results"]
        self.assertEqual(20_000, cpu_results["logical_records"])
        self.assertEqual(5, cpu_results["warmup_rounds"])
        self.assertEqual(10, cpu_results["measured_rounds"])
        for op_name, stats in cpu_results["operations"].items():
            self.assertEqual(20_000, stats["logical_records"], op_name)
            self.assertEqual(5, stats["warmup_rounds"], op_name)
            self.assertEqual(10, stats["measured_rounds"], op_name)
            self.assertGreaterEqual(stats["mean_seconds"], 0.0, op_name)
            self.assertGreaterEqual(stats["median_seconds"], 0.0, op_name)
            self.assertGreaterEqual(stats["p95_seconds"], 0.0, op_name)
            self.assertGreater(stats["records_per_second"], 0.0, op_name)
            self.assertEqual(10, len(stats["measured_round_seconds"]), op_name)
            self.assertEqual(5, len(stats["warmup_round_seconds"]), op_name)
            self.assertGreaterEqual(stats["bytes_processed"], 0)

    def test_05_hash_and_sanitization(self) -> None:
        data = json.loads(ARTIFACT_JSON.read_text(encoding="utf-8"))
        text = ARTIFACT_JSON.read_text(encoding="utf-8") + "\n" + ARTIFACT_MD.read_text(encoding="utf-8")
        self.assertEqual(canonical_hash(data), data["artifact_sha256"])
        self.assertNotIn("C:\\", text)
        self.assertNotIn("/home/", text)
        self.assertNotIn(getpass.getuser().lower(), text.lower())
        self.assertNotIn(platform.node().lower(), text.lower())
        self.assertNotIn("username", text.lower())
        self.assertNotIn("hostname", text.lower())

    def test_06_gpu_boundary(self) -> None:
        data = json.loads(ARTIFACT_JSON.read_text(encoding="utf-8"))
        gpu = data["gpu_results"]
        self.assertEqual("NOT_EXECUTED_MODEL_NOT_PROVIDED", gpu["status"])
        self.assertFalse(gpu["used_for_capacity_recalculation"])
        self.assertFalse(data["scope_boundary"]["capacity_values_changed"])
        self.assertTrue(data["scope_boundary"]["m1_on_platform_measurement_required"])
        self.assertNotIn("Deucalion", data["interpretation"]["cpu_summary"]["proxy_only"])
        self.assertNotIn("A100", data["interpretation"]["cpu_summary"]["proxy_only"])

    def test_07_resource_calibration_unchanged(self) -> None:
        calibration = json.loads(RESOURCE_CALIBRATION_JSON.read_text(encoding="utf-8"))
        self.assertEqual("resource_capacity_calibration", calibration["artifact_type"])
        self.assertEqual(20_000, calibration["scenarios"]["planned"]["cpu"]["total_core_hours"])
        self.assertEqual(1_500, calibration["scenarios"]["planned"]["gpu"]["rounded_planning_envelope_gpu_hours"])
        self.assertEqual(2.0, calibration["scenarios"]["planned"]["storage"]["total_tb"])
        self.assertIn("UNMEASURED", calibration["scenarios"]["planned"]["gpu"]["assumption_status"])
        plan = RESOURCE_CAPACITY_PLAN.read_text(encoding="utf-8").lower()
        self.assertIn("local proxy microbenchmark artifact", plan)
        self.assertIn("m1 measurement remains mandatory", plan)


if __name__ == "__main__":
    unittest.main()
