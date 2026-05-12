"""Small runtime constants for the Daily Cyberlog CLI."""

from __future__ import annotations

DEFAULT_CONFIG = {
    "daily_root": "Daily",
    "daily_raw_root": "Daily/raw",
    "daily_compiled_root": "Daily/compiled",
    "daily_templates_root": "Daily/templates",
    "system_root": "System",
    "reviews_root": "Reviews/weekly",
    "generated_prefix": "_",
    "daily_exclude_dirs": ["chatroom"],
    "timezone": "local",
    "raw_retention_days": 7,
    # Default is "end" to match the example: 2026-05-01..2026-05-07 -> 2026-W19.
    # Set to "start" in cyberlog.config.json if you want strict start-date labeling.
    "weekly_week_basis": "end",
}

CONFIG_FILE_NAME = "cyberlog.config.json"

RUN_STATE_FILE_NAME = "run-state.json"

CAPTURE_TYPES = ("note", "decision", "blocker", "todo", "sent", "draft")

STRUCTURED_CAPTURE_TYPES = set(CAPTURE_TYPES) - {"note"}
