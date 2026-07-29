from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PUBLIC_FILES = [
    ROOT / "docs/methodology/software_and_platform_compatibility.md",
    ROOT / "docs/methodology/resource_capacity_plan.md",
    ROOT / "docs/methodology/data_governance_and_release.md",
    ROOT / "docs/methodology/experimental_scale_and_freeze_manifest.md",
    ROOT / "docs/methodology/human_review_and_operational_risk.md",
    ROOT / "benchmark/resource_calibration.json",
    ROOT / "benchmark/resource_calibration.md",
    ROOT / "docs/evidence/kaggle_qlora_manifest.json",
]


class ResourceMethodologyArtifactsTest(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        missing = [str(path.relative_to(ROOT)) for path in PUBLIC_FILES if not path.is_file()]
        self.assertEqual([], missing)

    def test_public_documents_are_neutral(self) -> None:
        forbidden = (
            "C" + "PCA",
            "My" + "FCT",
            "application " + "allocation",
        )
        for path in PUBLIC_FILES:
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, f"{token!r} found in {path.relative_to(ROOT)}")

    def test_resource_json_contract(self) -> None:
        data = json.loads((ROOT / "benchmark/resource_calibration.json").read_text(encoding="utf-8"))
        self.assertEqual("resource_capacity_calibration", data["artifact_type"])
        self.assertIn("minimum", data["scenarios"])
        self.assertIn("planned", data["scenarios"])
        self.assertIn("ceiling", data["scenarios"])
        planned = data["scenarios"]["planned"]
        self.assertEqual(20_000, planned["dataset_records"])
        self.assertEqual(20_000, planned["cpu"]["total_core_hours"])
        self.assertEqual(1_500, planned["gpu"]["rounded_planning_envelope_gpu_hours"])
        self.assertEqual(2.0, planned["storage"]["total_tb"])
        self.assertIn("UNMEASURED", planned["gpu"]["assumption_status"])

    def test_optional_adaptation_is_not_core(self) -> None:
        capacity = (ROOT / "docs/methodology/resource_capacity_plan.md").read_text(encoding="utf-8").lower()
        freeze = (ROOT / "docs/methodology/experimental_scale_and_freeze_manifest.md").read_text(encoding="utf-8").lower()
        self.assertIn("optional adaptation is cancelled", capacity)
        self.assertIn("qlora is optional", freeze)

    def test_parallelization_contract_and_platform_mapping(self) -> None:
        text = (ROOT / "docs/methodology/software_and_platform_compatibility.md").read_text(encoding="utf-8")
        self.assertIn("MPI = NO", text)
        self.assertIn("OPENMP = NO_EXPLICIT_USE", text)
        self.assertIn("CUDA = YES", text)
        self.assertIn("Deucalion GPU/x86", text)
        self.assertIn("Cirrus", text)
        self.assertIn("Navigator", text)
        self.assertIn("Oblivion", text)
        self.assertIn("ARM64 remains disabled", text)
        self.assertNotIn("Slurm 23.11.4", text)
        self.assertNotIn("load the platform CUDA, compiler and MPI modules", text)
        self.assertNotIn("32 CPUs per task", text)
        self.assertNotIn("full x86 node", text)

    def test_requested_job_profiles_and_capacity_narrative(self) -> None:
        text = (ROOT / "docs/methodology/resource_capacity_plan.md").read_text(encoding="utf-8")
        lower = text.lower()
        self.assertIn("requested cores per job", lower)
        self.assertIn("proposed_job_profile", lower)
        self.assertIn("15,360 core.h", text)
        self.assertIn("4,096 core.h", text)
        self.assertIn("20,000 core.h", text)
        self.assertIn("bounded benchmark/test corpus", lower)
        self.assertIn("development, portability, benchmarking, scalability and pipeline optimization", lower)

    def test_resource_json_planning_assumptions_and_sensitivity(self) -> None:
        data = json.loads((ROOT / "benchmark/resource_calibration.json").read_text(encoding="utf-8"))
        planned = data["scenarios"]["planned"]
        cpu_runs = planned["cpu"]["full_x86_pipeline_runs"]
        cpu_jobs = planned["cpu"]["calibration_qa_jobs"]
        gpu = planned["gpu"]

        self.assertNotIn("cores", cpu_runs)
        self.assertNotIn("cores", cpu_jobs)
        self.assertEqual("PLANNING_ASSUMPTION", cpu_runs["evidence_class"])
        self.assertEqual("PROPOSED_JOB_PROFILE_PENDING_PLATFORM_CONFIRMATION", cpu_runs["source"])
        self.assertEqual("TO_BE_REPLACED_BY_M1_ALLOCATED_CORES_MEASUREMENT", cpu_runs["verification_status"])
        self.assertEqual("PLANNING_ASSUMPTION", cpu_jobs["evidence_class"])
        self.assertEqual("PROPOSED_JOB_PROFILE_PENDING_PLATFORM_CONFIRMATION", cpu_jobs["source"])
        self.assertEqual("TO_BE_REPLACED_BY_M1_ALLOCATED_CORES_MEASUREMENT", cpu_jobs["verification_status"])
        self.assertEqual(30, gpu["assumed_seconds_per_case"])
        self.assertEqual("PLANNING_ASSUMPTION", gpu["evidence_class"])
        self.assertEqual("PROPOSED_JOB_PROFILE_PENDING_PLATFORM_CONFIRMATION", gpu["source"])
        self.assertEqual("TO_BE_REPLACED_BY_M1_LATENCY_MEASUREMENT", gpu["verification_status"])
        self.assertEqual([15, 30, 60], gpu["sensitivity_seconds_per_case"])
        self.assertEqual(916.6666666666666, gpu["sensitivity_gpu_hours"]["15"])
        self.assertEqual(1483.3333333333333, gpu["sensitivity_gpu_hours"]["30"])
        self.assertEqual(2616.6666666666665, gpu["sensitivity_gpu_hours"]["60"])
        self.assertEqual(1500, gpu["rounded_planning_envelope_gpu_hours"])
        self.assertEqual(20000, planned["cpu"]["total_core_hours"])
        self.assertEqual(20000, planned["dataset_records"])
        self.assertEqual(
            "Bounded benchmark/test corpus, pipeline QA, portability, scalability and required A/B/C performance tests.",
            planned["purpose"],
        )
        self.assertIn(
            "Do not execute optional adaptation before dataset and required baseline gates pass.",
            data["stop_rules"],
        )
        self.assertIn(
            "If p95 exceeds 30 seconds per case, remove optional adaptation first, then optional variants and non-essential repeats.",
            data["stop_rules"],
        )
        self.assertIn(
            "If p95 approaches or exceeds 60 seconds per case, reduce optional cells or models before proposing any envelope change.",
            data["stop_rules"],
        )

    def test_experimental_scale_manifest_scope(self) -> None:
        text = (ROOT / "docs/methodology/experimental_scale_and_freeze_manifest.md").read_text(encoding="utf-8").lower()
        self.assertIn("bounded benchmark/test-corpus records", text)
        self.assertIn("development, benchmarking, scalability, portability and optimization", text)
        self.assertIn("not mass scientific production", text)
        self.assertIn("ceiling of 50,000 records is not part of the initial request", text)
        self.assertIn("activates only after qa, review capacity and efficiency gates pass", text)
        self.assertIn("not activated to consume residual resources", text)
        self.assertIn("pending_data_freeze", text)

    def test_no_public_call_or_form_terms(self) -> None:
        scope_text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8").lower()
            for path in (
                "docs/methodology/software_and_platform_compatibility.md",
                "docs/methodology/resource_capacity_plan.md",
                "benchmark/resource_calibration.json",
                "docs/methodology/experimental_scale_and_freeze_manifest.md",
            )
        )
        self.assertNotIn("convocatoria", scope_text)
        self.assertNotIn("formulario", scope_text)
        self.assertNotIn("application form", scope_text)


if __name__ == "__main__":
    unittest.main()
