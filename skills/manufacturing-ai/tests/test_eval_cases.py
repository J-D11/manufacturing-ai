"""CLI contract tests only; these do not score assistant behavior."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/eval_cases.py"


class EvalCliTests(unittest.TestCase):
    def run_cli(self, command, value):
        return subprocess.run([sys.executable, str(SCRIPT), command, str(value)],
                              text=True, capture_output=True, timeout=10)

    def check(self, value):
        # Keep test artifacts outside the installed skill.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scores.json"
            path.write_text(json.dumps(value))
            return self.run_cli("check-scores", path)

    def valid(self):
        return {"run_id": "test", "skill_fingerprint": "fixture", "model": "fixture",
                "records": [{"case_id": "radial-fit", "repeat": 1,
                             "response_path": "fixture.txt", "rationale": "fixture",
                             "assessor": "fixture", "critical_failures": [],
                             "scores": {k: 2 for k in
                                        ("correctness", "evidence", "scope", "next_step", "clarity")}}]}

    def assert_rejected(self, value):
        result = self.check(value)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)

    def test_prompt_contains_only_blinded_fields(self):
        result = self.run_cli("prompt", "radial-fit")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(json.loads(result.stdout)), {"case_id", "prompt", "context"})
        self.assertNotIn("10.4", result.stdout)
        self.assertNotIn("critical_failures", result.stdout)

    def test_valid_partial_scores_report_missing_cases(self):
        result = self.check(self.valid())
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertTrue(parsed["schema_valid"])
        self.assertNotIn("radial-fit", parsed["unrecorded_cases"])
        expected_ids = {c["id"] for c in json.loads((SCRIPT.parents[1] / "tests/scenarios.json").read_text())["cases"]}
        self.assertEqual(set(parsed["unrecorded_cases"]), expected_ids - {"radial-fit"})

    def test_top_level_shapes(self):
        for value in (None, [], "bad", 7):
            with self.subTest(value=value):
                self.assert_rejected(value)

    def test_non_object_records(self):
        for row in (None, [], "bad", 7):
            with self.subTest(row=row):
                value = self.valid()
                value["records"] = [row]
                self.assert_rejected(value)

    def test_duplicate_records(self):
        value = self.valid()
        value["records"].append(value["records"][0].copy())
        self.assert_rejected(value)

    def test_bool_and_out_of_range_scores(self):
        for score in (True, -1, 3, "2"):
            with self.subTest(score=score):
                value = self.valid()
                value["records"][0]["scores"]["clarity"] = score
                self.assert_rejected(value)

    def test_unknown_case(self):
        result = self.run_cli("prompt", "missing")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
