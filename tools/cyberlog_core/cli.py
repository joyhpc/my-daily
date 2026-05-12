"""Argument parsing and command dispatch for the Daily Cyberlog CLI."""

from __future__ import annotations

import argparse
import sys

from .app import (
    command_capture,
    command_close_day,
    command_conflict_scan,
    command_daily,
    command_decisions,
    command_init,
    command_prune_raw,
    command_today,
    command_validate,
    command_weekly,
    load_config,
)
from .constants import CAPTURE_TYPES
from .models import CyberlogError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Daily Cyberlog / AI Sync helper for Obsidian.")
    parser.add_argument(
        "--root",
        help="Workspace root. Defaults to the parent directory of this script.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    daily = subparsers.add_parser("daily", help="Build daily _ai-feed.md, _ai-context.md, and _ai-request.md.")
    daily.add_argument("--date", required=True, help="Date in YYYY-MM-DD format.")
    daily.set_defaults(func=command_daily)

    weekly = subparsers.add_parser("weekly", help="Build weekly AI review request.")
    weekly.add_argument("--start", required=True, help="Start date in YYYY-MM-DD format.")
    weekly.add_argument("--end", required=True, help="End date in YYYY-MM-DD format.")
    weekly.set_defaults(func=command_weekly)

    init = subparsers.add_parser("init", help="Create directories and template files.")
    init.add_argument("--force", action="store_true", help="Overwrite existing templates.")
    init.set_defaults(func=command_init)

    today = subparsers.add_parser("today", help="Create today's daily folder and raw note files.")
    today.add_argument("--date", help="Date in YYYY-MM-DD format. Defaults to today.")
    today.set_defaults(func=command_today)

    capture = subparsers.add_parser("capture", help="Capture a raw note into today's daily folder.")
    capture.add_argument("--date", help="Date in YYYY-MM-DD format. Defaults to today.")
    capture.add_argument("--type", choices=CAPTURE_TYPES, default="note", help="Capture type. Structured types write YAML front matter.")
    capture.add_argument("--project", help="Canonical project id for structured captures.")
    capture.add_argument("--sent-to", dest="sent_to", help="Recipient summary for sent/draft communication captures.")
    capture.add_argument("--subject", help="Subject summary for communication captures.")
    capture.add_argument("--waiting-for", dest="waiting_for", help="Expected reply or decision for communication captures.")
    capture.add_argument("text", nargs="*", help="Capture text. Reads stdin when omitted.")
    capture.set_defaults(func=command_capture)

    prune_raw = subparsers.add_parser("prune-raw", help="Prune completed raw daily folders after retention.")
    prune_raw.add_argument("--before", help="Prune raw daily folders before this YYYY-MM-DD date.")
    prune_raw.add_argument(
        "--older-than",
        type=int,
        help="Prune raw daily folders older than this many days. Defaults to raw_retention_days.",
    )
    prune_raw.add_argument("--apply", action="store_true", help="Actually delete eligible raw folders.")
    prune_raw.set_defaults(func=command_prune_raw)

    decisions = subparsers.add_parser("decisions", help="Roll up daily _decisions.yml files into System/decisions-active.md.")
    decisions.add_argument("--rollup", action="store_true", help="Generate the active decisions rollup.")
    decisions.add_argument("--through", help="Include decisions through this YYYY-MM-DD date. Defaults to today.")
    decisions.add_argument("--output", help="Output path. Defaults to System/decisions-active.md.")
    decisions.set_defaults(func=command_decisions)

    conflict_scan = subparsers.add_parser("conflict-scan", help="Run deterministic daily conflict checks.")
    conflict_scan.add_argument("--date", required=True, help="Date in YYYY-MM-DD format.")
    conflict_scan.set_defaults(func=command_conflict_scan)

    validate = subparsers.add_parser("validate", help="Run read-only governance validation for one date.")
    validate.add_argument("--date", required=True, help="Date in YYYY-MM-DD format.")
    validate.add_argument("--write", action="store_true", help="Write Daily/compiled/YYYY-MM-DD/_validation.md instead of printing.")
    validate.add_argument("--strict", action="store_true", help="Return non-zero when blocking findings exist.")
    validate.set_defaults(func=command_validate)

    close_day = subparsers.add_parser("close-day", help="Run daily closure gates and mark the day closed when validation passes.")
    close_day.add_argument("--date", required=True, help="Date in YYYY-MM-DD format.")
    close_day.set_defaults(func=command_close_day)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        config = load_config(args.root)
        return args.func(args, config)
    except CyberlogError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
