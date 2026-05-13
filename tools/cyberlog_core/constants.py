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

ERROR_CODE_DEFINITIONS = {
    "E1": "factual_upgrade",
    "E2": "source_hallucination",
    "E3": "context_leak",
    "E4": "project_boundary",
    "E5": "state_drift",
    "E6": "decision_drift",
    "E7": "output_contract",
}

FINDING_ERROR_CODES = {
    "ai_output_audit": "E7",
    "ai_output_missing": "E7",
    "comms_draft_aging": "E5",
    "comms_missing_expected_reply_by": "E5",
    "comms_reply_overdue": "E5",
    "comms_schema": "E5",
    "comms_status": "E5",
    "cyberlog_blocked_detail": "E7",
    "cyberlog_decision_table": "E6",
    "cyberlog_structure": "E7",
    "decision_duplicate_topic": "E6",
    "decision_evidence": "E6",
    "decision_next": "E6",
    "decision_owner": "E6",
    "decision_schema": "E6",
    "decision_supersedes": "E6",
    "forbidden_alias": "E4",
    "memory_constraint": "E4",
    "memory_protocol": "E4",
    "schema_contract": "E7",
    "schema_projects": "E4",
    "source": "E2",
    "source_reference": "E2",
    "tomorrow_boot_structure": "E7",
}
