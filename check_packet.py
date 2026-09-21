#!/usr/bin/env python3
"""Offline, fail-closed shape checks for the local contributor starter packet."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

TASK_REQUIRED = {"task_id", "title", "objective", "inputs", "deliverable", "estimated_minutes", "status"}
TASK_OPTIONAL = {"ai_optional"}
TASK_ALLOWED = TASK_REQUIRED | TASK_OPTIONAL
REPORT_REQUIRED = {"task_id", "title", "contributor", "work", "expected", "observed", "classification", "attribution", "withdrawal_requested"}
REPORT_OPTIONAL = {"operator", "evidence", "ai_provenance", "reuse_preference"}
REPORT_ALLOWED = REPORT_REQUIRED | REPORT_OPTIONAL
TASK_ID = re.compile(r"^CONTRIB-START-[0-9]{3}$")
STATUSES = {"local-review", "release-pending", "released"}
CLASSIFICATIONS = {"fact", "inference", "proposal", "unresolved", "mixed"}
ATTRIBUTIONS = {"named", "pseudonymous", "anonymous", "operator-credited"}
WATER_ALLOWED = {"case_id", "fictional", "facts", "questions", "submission_note"}
MAX_JSON_BYTES = 1_000_000


class PacketError(ValueError):
    """A packet is malformed or fails a bounded check."""


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise PacketError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    """Load bounded JSON while rejecting duplicate keys and non-finite numbers."""
    try:
        text = path.read_text(encoding="utf-8")
        if len(text.encode("utf-8")) > MAX_JSON_BYTES:
            raise PacketError(f"{path} exceeds {MAX_JSON_BYTES}-byte limit")
        return json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_constant=lambda value: (_ for _ in ()).throw(PacketError(f"non-finite number: {value}")),
            parse_float=lambda value: _finite_float(value),
        )
    except PacketError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PacketError(f"cannot load {path}: {exc}") from exc


def _finite_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise PacketError(f"non-finite number: {value}")
    raise PacketError("floating-point numbers are not allowed in packet JSON")


def _object(value: Any, label: str, allowed: set[str], required: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PacketError(f"{label} must be an object")
    unknown = set(value) - allowed
    missing = required - set(value)
    if unknown:
        raise PacketError(f"{label} unknown fields: {sorted(unknown)}")
    if missing:
        raise PacketError(f"{label} missing fields: {sorted(missing)}")
    return value


def _string(value: Any, label: str, *, nonempty: bool = False) -> None:
    if not isinstance(value, str) or (nonempty and not value):
        raise PacketError(f"{label} must be a{' non-empty' if nonempty else ''} string")


def _string_list(value: Any, label: str, *, nonempty: bool = True) -> None:
    if not isinstance(value, list) or (nonempty and not value) or any(not isinstance(item, str) or not item for item in value):
        qualifier = "non-empty " if nonempty else ""
        raise PacketError(f"{label} must be a {qualifier}list of non-empty strings")


def validate_task(value: Any, *, label: str = "task") -> dict[str, Any]:
    task = _object(value, label, TASK_ALLOWED, TASK_REQUIRED)
    _string(task["task_id"], f"{label}.task_id", nonempty=True)
    if not TASK_ID.fullmatch(task["task_id"]):
        raise PacketError(f"{label}.task_id has invalid format")
    for field in ("title", "objective"):
        _string(task[field], f"{label}.{field}", nonempty=True)
    _string_list(task["inputs"], f"{label}.inputs")
    _string_list(task["deliverable"], f"{label}.deliverable")
    # bool is an int subclass, so reject it explicitly.
    if isinstance(task["estimated_minutes"], bool) or not isinstance(task["estimated_minutes"], int) or not 1 <= task["estimated_minutes"] <= 1440:
        raise PacketError(f"{label}.estimated_minutes must be an integer from 1 to 1440")
    if not isinstance(task["status"], str) or task["status"] not in STATUSES:
        raise PacketError(f"{label}.status is invalid")
    if "ai_optional" in task and not isinstance(task["ai_optional"], bool):
        raise PacketError(f"{label}.ai_optional must be boolean")
    return task


def validate_report(value: Any, task_ids: set[str], *, label: str = "report") -> dict[str, Any]:
    report = _object(value, label, REPORT_ALLOWED, REPORT_REQUIRED)
    _string(report["task_id"], f"{label}.task_id", nonempty=True)
    if report["task_id"] not in task_ids:
        raise PacketError(f"{label}.task_id does not reference a known task")
    for field in ("title", "contributor", "work", "expected", "observed"):
        _string(report[field], f"{label}.{field}", nonempty=True)
    if not isinstance(report["classification"], str) or report["classification"] not in CLASSIFICATIONS:
        raise PacketError(f"{label}.classification is invalid")
    if not isinstance(report["attribution"], str) or report["attribution"] not in ATTRIBUTIONS:
        raise PacketError(f"{label}.attribution is invalid")
    if not isinstance(report["withdrawal_requested"], bool):
        raise PacketError(f"{label}.withdrawal_requested must be boolean")
    if "operator" in report and report["operator"] is not None:
        _string(report["operator"], f"{label}.operator")
    if "evidence" in report:
        _string_list(report["evidence"], f"{label}.evidence", nonempty=False)
    for field in ("ai_provenance", "reuse_preference"):
        if field in report:
            _string(report[field], f"{label}.{field}")
    return report


def validate_bundle(root: Path) -> list[str]:
    """Validate the packet's shipped examples and return checked paths."""
    task_paths = [root / "task.json", root / "ai-task.json"]
    tasks = [validate_task(load_json(path), label=str(path)) for path in task_paths]
    task_ids = {task["task_id"] for task in tasks}
    if len(task_ids) != len(tasks):
        raise PacketError("duplicate task_id across task files")
    report = validate_report(load_json(root / "report.template.json"), task_ids, label="report.template.json")
    if "EXAMPLE ONLY" not in report["title"] or "EXAMPLE ONLY" not in report["work"]:
        raise PacketError("report.template.json must remain visibly marked as an example")
    case = load_json(root / "examples" / "water-case.json")
    if not isinstance(case, dict) or case.get("fictional") is not True:
        raise PacketError("water case must be explicitly fictional")
    _object(case, "water case", WATER_ALLOWED, WATER_ALLOWED)
    for field in ("case_id", "facts", "questions", "submission_note"):
        if field not in case:
            raise PacketError(f"water case missing field: {field}")
    _string(case["case_id"], "water.case_id", nonempty=True)
    _string_list(case["facts"], "water.facts")
    _string_list(case["questions"], "water.questions")
    _string(case["submission_note"], "water.submission_note", nonempty=True)
    return [str(path.relative_to(root)) for path in (*task_paths, root / "report.template.json", root / "examples" / "water-case.json")]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="offline fail-closed starter packet check")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args(argv)
    try:
        checked = validate_bundle(args.root.resolve())
    except (PacketError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: checked " + ", ".join(checked))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
