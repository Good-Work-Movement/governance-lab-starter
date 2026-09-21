import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).parents[1]))
import check_packet


ROOT = Path(__file__).parents[1]


class CheckPacketTests(unittest.TestCase):
    def test_valid_bundle_and_report(self):
        checked = check_packet.validate_bundle(ROOT)
        self.assertIn("report.template.json", checked)
        self.assertEqual(check_packet.main(["--root", str(ROOT)]), 0)

    def test_extra_field_rejected(self):
        task = json.loads((ROOT / "task.json").read_text())
        task["surprise"] = True
        with self.assertRaises(check_packet.PacketError):
            check_packet.validate_task(task)

    def test_unknown_task_rejected(self):
        report = json.loads((ROOT / "report.template.json").read_text())
        report["task_id"] = "CONTRIB-START-999"
        with self.assertRaises(check_packet.PacketError):
            check_packet.validate_report(report, {"CONTRIB-START-001"})

    def test_bool_as_integer_rejected(self):
        task = json.loads((ROOT / "task.json").read_text())
        task["estimated_minutes"] = True
        with self.assertRaises(check_packet.PacketError):
            check_packet.validate_task(task)

    def test_malformed_enum_rejected_by_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for source in ("task.json", "ai-task.json", "report.template.json"):
                value = json.loads((ROOT / source).read_text())
                if source == "task.json":
                    value["status"] = {"bad": True}
                (target / source).write_text(json.dumps(value))
            (target / "examples").mkdir()
            (target / "examples" / "water-case.json").write_text((ROOT / "examples" / "water-case.json").read_text())
            with patch("sys.stderr"):
                self.assertEqual(check_packet.main(["--root", str(target)]), 1)

    def test_duplicate_keys_and_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text('{"a": 1, "a": 2}')
            with self.assertRaises(check_packet.PacketError):
                check_packet.load_json(path)
            path.write_text('{"a": NaN}')
            with self.assertRaises(check_packet.PacketError):
                check_packet.load_json(path)
            path.write_text('{"a": 1e999}')
            with self.assertRaises(check_packet.PacketError):
                check_packet.load_json(path)

    def test_water_case_unknown_field_rejected(self):
        case = json.loads((ROOT / "examples" / "water-case.json").read_text())
        case["unexpected"] = "no"
        with self.assertRaises(check_packet.PacketError):
            check_packet._object(case, "water case", check_packet.WATER_ALLOWED, check_packet.WATER_ALLOWED)

    def test_cli_clean_site_disabled(self):
        environment = os.environ.copy()
        for name in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"):
            environment.pop(name, None)
        result = subprocess.run(
            [sys.executable, "-B", "-S", str(ROOT / "check_packet.py"), "--root", str(ROOT)],
            env=environment, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
