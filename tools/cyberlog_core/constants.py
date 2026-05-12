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

MANAGEMENT_TAG_LIMIT = 2

TRUST_TAGS = {
    "可信": "high",
    "高可信": "high",
    "事实": "high",
    "已确认": "high",
    "实测": "high",
    "待确认": "medium",
    "中可信": "medium",
    "口头": "medium",
    "低可信": "low",
    "未核实": "low",
    "草稿": "low",
    "AI建议": "low",
    "ai建议": "low",
}

TYPE_TAGS = {
    "决策": "decision",
    "阻塞": "blocker",
    "待办": "todo",
    "todo": "todo",
    "已发送": "sent",
    "发送": "sent",
    "草稿": "draft",
}
