#!/usr/bin/env python3
"""Run the lightweight cyberlog quality gate.

Run from the my-daily root with:
    python3 tools/check.py --date 2026-05-13

If --date is omitted, the newest Daily/compiled/YYYY-MM-DD folder is used.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def display_command(command: list[str]) -> str:
    return " ".join(command)


def run_step(name: str, command: list[str], root: Path) -> int:
    print(f"\n== {name} ==", flush=True)
    print(f"$ {display_command(command)}", flush=True)
    completed = subprocess.run(command, cwd=root)
    if completed.returncode == 0:
        print(f"OK: {name}", flush=True)
    else:
        print(f"FAILED: {name} exited with {completed.returncode}", flush=True)
    return completed.returncode


def latest_compiled_date(root: Path) -> str:
    compiled_root = root / "Daily" / "compiled"
    if not compiled_root.exists():
        raise SystemExit("Daily/compiled does not exist; pass --date after creating a daily package.")
    dates = sorted(path.name for path in compiled_root.iterdir() if path.is_dir() and DATE_RE.match(path.name))
    if not dates:
        raise SystemExit("No Daily/compiled/YYYY-MM-DD folders found; pass --date after creating a daily package.")
    return dates[-1]


def run_state_phase(root: Path, day: str) -> str:
    path = root / "Daily" / "compiled" / day / "_run-state.json"
    if not path.exists():
        return "unknown"
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "invalid"
    return str(state.get("phase", "unknown"))


def diff_check_command(cached: bool) -> list[str]:
    command = ["git", "diff"]
    if cached:
        command.append("--cached")
    command.extend(
        [
            "--check",
            "--",
            ".",
            ":(exclude)Daily/raw/**",
            ":(exclude)Daily/compiled/**/_ai-feed.md",
            ":(exclude)Daily/compiled/**/_ai-request.md",
        ]
    )
    return command


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run compile, tests, cyberlog validation, and scoped git whitespace checks.")
    parser.add_argument("--date", help="Daily date to validate, in YYYY-MM-DD format. Defaults to latest compiled day.")
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--skip-tests", action="store_true", help="Skip tools/test_cyberlog.py.")
    parser.add_argument("--write-validation", action="store_true", help="Force validate --write even when the day is already closed.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    day = args.date or latest_compiled_date(root)
    if not DATE_RE.match(day):
        raise SystemExit(f"Invalid --date: {day}")

    steps: list[tuple[str, list[str]]] = [
        ("compile Python files", [sys.executable, "-m", "compileall", "-q", "tools"]),
    ]
    if not args.skip_tests:
        steps.append(("run cyberlog tests", [sys.executable, "tools/test_cyberlog.py"]))

    phase = run_state_phase(root, day)
    validate_command = [sys.executable, "tools/cyberlog.py", "validate", "--date", day]
    if args.write_validation or phase != "closed":
        validate_command.append("--write")
        validate_name = f"validate daily contract for {day} (write report)"
    else:
        validate_name = f"validate daily contract for {day} (read-only; phase is closed)"
    steps.append((validate_name, validate_command))

    steps.extend(
        [
            ("git whitespace check", diff_check_command(cached=False)),
            ("git staged whitespace check", diff_check_command(cached=True)),
        ]
    )

    failures = 0
    for name, command in steps:
        if run_step(name, command, root) != 0:
            failures += 1

    print("\n== Summary ==", flush=True)
    print(f"date: {day}", flush=True)
    print(f"run-state phase before validate: {phase}", flush=True)
    if failures:
        print(f"FAILED: {failures} step(s) failed.", flush=True)
        return 1
    print("OK: all checks passed.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
