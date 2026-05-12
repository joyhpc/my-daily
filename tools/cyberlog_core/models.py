"""Shared data models for the Daily Cyberlog runtime."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

class CyberlogError(Exception):
    """User-facing command error."""


@dataclass(frozen=True)
class Config:
    workspace_root: Path
    daily_root: Path
    daily_raw_root: Path
    daily_compiled_root: Path
    daily_templates_root: Path
    system_root: Path
    reviews_root: Path
    generated_prefix: str
    daily_exclude_dirs: tuple[str, ...]
    timezone: str
    raw_retention_days: int
    weekly_week_basis: str


@dataclass(frozen=True)
class RawFileEntry:
    path: Path
    size: int
    sha256: str


@dataclass(frozen=True)
class ProjectEntry:
    project_id: str
    status: str
    priority: str
    aliases: tuple[str, ...]
    forbidden_aliases: tuple[str, ...]
    constraints: tuple[str, ...]


@dataclass(frozen=True)
class TextHit:
    path: Path
    line_number: int
    line: str


@dataclass(frozen=True)
class DecisionRecord:
    decision_id: str
    project: str
    topic: str
    status: str
    owner: str
    next_action: str
    blockers: tuple[str, ...]
    supersedes: tuple[str, ...]
    evidence: tuple[str, ...]
    source_path: Path
    present_fields: tuple[str, ...]


@dataclass(frozen=True)
class CommsRecord:
    comms_id: str
    project: str
    channel: str
    draft: str
    status: str
    sent_to: str
    sent_at: str
    waiting_for: str
    expected_reply_by: str
    source_path: Path
    present_fields: tuple[str, ...]


@dataclass(frozen=True)
class GateFinding:
    severity: str
    category: str
    message: str
    evidence: tuple[str, ...] = ()
