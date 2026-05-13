#!/usr/bin/env python3
"""Daily Cyberlog / AI Sync helper for a personal daily workspace.

This script intentionally uses only the Python standard library. It never
modifies non-generated markdown notes during feed generation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys
from pathlib import Path
from typing import Iterable

from .templates import (
    AI_SYNC_PROMPT,
    CANVAS_TEMPLATE,
    CONFIG_TEMPLATE,
    ERROR_TAXONOMY_TEMPLATE,
    PERSONAL_OPERATING_MANUAL,
    PROJECTS_TEMPLATE,
    README,
    SCHEMAS_TEMPLATE,
    WEEKLY_REVIEW_PROMPT,
    WORKFLOW_RULES,
)
from .constants import (
    CAPTURE_TYPES,
    CONFIG_FILE_NAME,
    DEFAULT_CONFIG,
    ERROR_CODE_DEFINITIONS,
    FINDING_ERROR_CODES,
    MANAGEMENT_TAG_LIMIT,
    RUN_STATE_FILE_NAME,
    STRUCTURED_CAPTURE_TYPES,
    TRUST_TAGS,
    TYPE_TAGS,
)
from .models import (
    CommsRecord,
    Config,
    CyberlogError,
    DecisionRecord,
    GateFinding,
    ProjectEntry,
    RawFileEntry,
    TextHit,
)


def parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise CyberlogError(f"Invalid date '{value}'. Expected YYYY-MM-DD.") from exc


def default_workspace_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_path(root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return root / path


def load_config(root_arg: str | None = None) -> Config:
    workspace_root = Path(root_arg).expanduser().resolve() if root_arg else default_workspace_root()
    raw = dict(DEFAULT_CONFIG)
    config_path = workspace_root / CONFIG_FILE_NAME

    if config_path.exists():
        try:
            user_config = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CyberlogError(f"Invalid JSON in {display_path(config_path, workspace_root)}: {exc}") from exc
        if not isinstance(user_config, dict):
            raise CyberlogError(f"{CONFIG_FILE_NAME} must contain a JSON object.")
        for key in raw:
            if key in user_config:
                raw[key] = user_config[key]

    for key in (
        "daily_root",
        "daily_raw_root",
        "daily_compiled_root",
        "daily_templates_root",
        "system_root",
        "reviews_root",
        "generated_prefix",
        "timezone",
        "weekly_week_basis",
    ):
        if not isinstance(raw[key], str):
            raise CyberlogError(f"Config key '{key}' must be a string.")

    if not isinstance(raw["raw_retention_days"], int) or isinstance(raw["raw_retention_days"], bool):
        raise CyberlogError("Config key 'raw_retention_days' must be an integer.")
    if raw["raw_retention_days"] < 0:
        raise CyberlogError("Config key 'raw_retention_days' cannot be negative.")

    if not isinstance(raw["daily_exclude_dirs"], list) or not all(
        isinstance(item, str) for item in raw["daily_exclude_dirs"]
    ):
        raise CyberlogError("Config key 'daily_exclude_dirs' must be a list of strings.")

    generated_prefix = raw["generated_prefix"]
    if not generated_prefix:
        raise CyberlogError("Config key 'generated_prefix' cannot be empty.")
    if "/" in generated_prefix or "\\" in generated_prefix:
        raise CyberlogError("Config key 'generated_prefix' must be a filename prefix, not a path.")

    weekly_week_basis = raw["weekly_week_basis"].lower()
    if weekly_week_basis not in {"start", "end"}:
        raise CyberlogError("Config key 'weekly_week_basis' must be 'start' or 'end'.")

    daily_exclude_dirs = tuple(item.strip() for item in raw["daily_exclude_dirs"] if item.strip())
    if any("/" in item or "\\" in item for item in daily_exclude_dirs):
        raise CyberlogError("Config key 'daily_exclude_dirs' must contain directory names, not paths.")

    return Config(
        workspace_root=workspace_root,
        daily_root=resolve_path(workspace_root, raw["daily_root"]),
        daily_raw_root=resolve_path(workspace_root, raw["daily_raw_root"]),
        daily_compiled_root=resolve_path(workspace_root, raw["daily_compiled_root"]),
        daily_templates_root=resolve_path(workspace_root, raw["daily_templates_root"]),
        system_root=resolve_path(workspace_root, raw["system_root"]),
        reviews_root=resolve_path(workspace_root, raw["reviews_root"]),
        generated_prefix=generated_prefix,
        daily_exclude_dirs=daily_exclude_dirs,
        timezone=raw["timezone"],
        raw_retention_days=raw["raw_retention_days"],
        weekly_week_basis=weekly_week_basis,
    )


def display_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_template(content: str, values: dict[str, str]) -> str:
    rendered = content
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def read_required_prompt(path: Path, config: Config) -> str:
    if not path.exists():
        raise CyberlogError(
            f"Missing prompt file: {display_path(path, config.workspace_root)}. "
            "Run `python3 tools/cyberlog.py init` first."
        )
    return path.read_text(encoding="utf-8")


def read_optional_text(path: Path) -> str | None:
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    return None


def parse_front_matter(content: str) -> tuple[dict[str, str], str]:
    if not content.startswith("---\n"):
        return {}, content
    lines = content.splitlines()
    metadata: dict[str, str] = {}
    end_index: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = parse_yaml_scalar(value)
    if end_index is None:
        return {}, content
    body = "\n".join(lines[end_index + 1 :])
    if content.endswith("\n"):
        body += "\n"
    return metadata, body


def strip_inline_comment(value: str) -> str:
    in_single = False
    in_double = False
    for index, char in enumerate(value):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            if index == 0 or value[index - 1].isspace():
                return value[:index].rstrip()
    return value.strip()


def parse_yaml_scalar(value: str) -> str:
    cleaned = strip_inline_comment(value).strip()
    if cleaned.lower() in {"null", "none", "~"}:
        return ""
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {"'", '"'}:
        return cleaned[1:-1]
    return cleaned


def parse_yaml_list(value: str) -> tuple[str, ...]:
    parsed = parse_yaml_scalar(value)
    if not parsed:
        return ()
    if parsed.startswith("[") and parsed.endswith("]"):
        inner = parsed[1:-1].strip()
        if not inner:
            return ()
        return tuple(parse_yaml_scalar(item) for item in inner.split(",") if parse_yaml_scalar(item))
    return (parsed,)


HASHTAG_RE = re.compile(r"(?<![\w-])#([A-Za-z0-9_\-\u4e00-\u9fff]+)")


def extract_management_tags(content: str) -> tuple[str, ...]:
    tags: list[str] = []
    seen: set[str] = set()
    for match in HASHTAG_RE.finditer(content):
        tag = "#" + match.group(1)
        if tag not in seen:
            tags.append(tag)
            seen.add(tag)
        if len(tags) >= MANAGEMENT_TAG_LIMIT:
            break
    return tuple(tags)


def normalized_tag(tag: str) -> str:
    return tag.lstrip("#").strip()


def first_tag_value(tags: Iterable[str], mapping: dict[str, str]) -> str:
    for tag in tags:
        value = mapping.get(normalized_tag(tag))
        if value:
            return value
    return ""


def extract_date(value: str) -> dt.date | None:
    match = re.search(r"(20\d{2}-\d{2}-\d{2})", value)
    if not match:
        return None
    try:
        return parse_date(match.group(1))
    except CyberlogError:
        return None


def severity_sort_key(finding: GateFinding) -> tuple[int, str, str]:
    order = {"blocking": 0, "warning": 1, "info": 2}
    return (order.get(finding.severity, 3), finding.category, finding.message)


def count_findings(findings: Iterable[GateFinding], severity: str) -> int:
    return sum(1 for finding in findings if finding.severity == severity)


def gate_result(findings: Iterable[GateFinding]) -> str:
    finding_list = list(findings)
    if any(finding.severity == "blocking" for finding in finding_list):
        return "BLOCKED"
    if any(finding.severity == "warning" for finding in finding_list):
        return "PASS_WITH_WARNINGS"
    return "PASS"


def error_code_for_finding(finding: GateFinding) -> str:
    if finding.severity == "info":
        return ""
    return FINDING_ERROR_CODES.get(finding.category, "")


def finding_category_label(finding: GateFinding) -> str:
    error_code = error_code_for_finding(finding)
    if error_code:
        return f"{error_code}/{finding.category}"
    return finding.category


def observed_error_codes(findings: Iterable[GateFinding]) -> list[str]:
    codes = {error_code_for_finding(finding) for finding in findings}
    return sorted(code for code in codes if code)


def format_error_code_summary(findings: Iterable[GateFinding]) -> str:
    codes = observed_error_codes(findings)
    if not codes:
        return "none"
    return ", ".join(f"{code} {ERROR_CODE_DEFINITIONS.get(code, '')}".rstrip() for code in codes)


def format_gate_findings(findings: Iterable[GateFinding]) -> str:
    lines: list[str] = []
    for finding in sorted(findings, key=severity_sort_key):
        lines.append(f"- [{finding.severity}] {finding_category_label(finding)}: {finding.message}")
        for evidence in finding.evidence:
            lines.append(f"  - evidence: {evidence}")
    return "\n".join(lines) if lines else "- No gate findings."


def is_raw_markdown(path: Path, generated_prefix: str) -> bool:
    return path.is_file() and path.suffix.lower() == ".md" and not path.name.startswith(generated_prefix)


def excluded_daily_dir(path: Path, raw_dir: Path, exclude_dirs: Iterable[str]) -> str | None:
    exclude_lookup = {item.lower() for item in exclude_dirs}
    try:
        parts = path.relative_to(raw_dir).parts[:-1]
    except ValueError:
        parts = path.parts[:-1]
    for part in parts:
        if part.lower() in exclude_lookup:
            return part
    return None


def daily_markdown_candidates(raw_dir: Path) -> list[Path]:
    return sorted((path for path in raw_dir.rglob("*.md") if path.is_file()), key=lambda path: path.relative_to(raw_dir).as_posix())


def daily_source_files(raw_dir: Path, config: Config) -> tuple[list[Path], list[tuple[Path, str]]]:
    included: list[Path] = []
    excluded: list[tuple[Path, str]] = []
    for path in daily_markdown_candidates(raw_dir):
        if path.name.startswith(config.generated_prefix):
            excluded.append((path, f"generated prefix `{config.generated_prefix}`"))
            continue
        excluded_dir = excluded_daily_dir(path, raw_dir, config.daily_exclude_dirs)
        if excluded_dir:
            excluded.append((path, f"excluded directory `{excluded_dir}`"))
            continue
        included.append(path)
    return included, excluded


def projects_registry_path(config: Config) -> Path:
    return config.system_root / "projects.yml"


def load_project_registry(config: Config) -> tuple[list[ProjectEntry], str | None]:
    path = projects_registry_path(config)
    text = read_optional_text(path)
    if text is None:
        return [], None

    projects: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_list_key: str | None = None
    in_constraints = False

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        stripped = raw_line.strip()
        indent = len(raw_line) - len(raw_line.lstrip(" "))

        if indent == 2 and stripped.startswith("- id:"):
            if current is not None:
                projects.append(current)
            current = {"aliases": [], "forbidden_aliases": [], "constraints": []}
            current["id"] = parse_yaml_scalar(stripped.split(":", 1)[1])
            current_list_key = None
            in_constraints = False
            continue

        if current is None:
            continue

        if stripped.endswith(":"):
            key = stripped[:-1]
            current_list_key = key if key in {"aliases", "forbidden_aliases"} else None
            in_constraints = key == "constraints"
            continue

        if stripped.startswith("- ") and current_list_key:
            item = parse_yaml_scalar(stripped[2:])
            if item:
                current.setdefault(current_list_key, []).append(item)
            continue

        if not in_constraints and indent == 4 and ":" in stripped:
            key, value = stripped.split(":", 1)
            if key in {"aliases", "forbidden_aliases"}:
                current[key] = list(parse_yaml_list(value))
            elif key in {"status", "priority"}:
                current[key] = parse_yaml_scalar(value)
            continue

        if in_constraints and indent >= 6 and ":" in stripped:
            value = parse_yaml_scalar(stripped.split(":", 1)[1])
            if value:
                current.setdefault("constraints", []).append(value)
            continue

    if current is not None:
        projects.append(current)

    entries: list[ProjectEntry] = []
    for project in projects:
        project_id = str(project.get("id", "")).strip()
        if not project_id:
            continue
        aliases = tuple(str(item) for item in project.get("aliases", []) if str(item).strip())
        forbidden_aliases = tuple(str(item) for item in project.get("forbidden_aliases", []) if str(item).strip())
        constraints = tuple(str(item) for item in project.get("constraints", []) if str(item).strip())
        entries.append(
            ProjectEntry(
                project_id=project_id,
                status=str(project.get("status", "")).strip(),
                priority=str(project.get("priority", "")).strip(),
                aliases=aliases,
                forbidden_aliases=forbidden_aliases,
                constraints=constraints,
            )
        )
    return entries, text


def markdown_files_for_daily(raw_dir: Path, config: Config) -> list[Path]:
    included, _ = daily_source_files(raw_dir, config)
    return included


def file_block(path: Path, config: Config) -> str:
    content = path.read_text(encoding="utf-8")
    metadata, body = parse_front_matter(content)
    tags = extract_management_tags(body)
    attrs = {"path": display_path(path, config.workspace_root)}
    type_value = first_tag_value(tags, TYPE_TAGS) or metadata.get("type", "")
    if type_value:
        attrs["type"] = type_value
    project = metadata.get("project", "")
    if project:
        attrs["project"] = project
    trust = first_tag_value(tags, TRUST_TAGS) or metadata.get("trust", "")
    if trust:
        attrs["trust"] = trust
    if tags:
        attrs["tags"] = " ".join(tags)
    attr_text = " ".join(f'{key}="{html.escape(value, quote=True)}"' for key, value in attrs.items())
    if not content.endswith("\n"):
        content += "\n"
    return f"<file {attr_text}>\n{content}</file>\n"


def join_blocks(paths: Iterable[Path], config: Config) -> str:
    return "\n".join(file_block(path, config).rstrip("\n") for path in paths) + "\n"


def daily_context_sources(day: dt.date, config: Config) -> tuple[list[tuple[str, dt.date, Path]], list[str]]:
    sources: list[tuple[str, dt.date, Path]] = []
    warnings: list[str] = []
    previous_day = day - dt.timedelta(days=1)
    previous_cyberlog = (
        config.daily_compiled_root
        / previous_day.isoformat()
        / f"{config.generated_prefix}cyberlog.md"
    )
    if previous_cyberlog.exists() and previous_cyberlog.is_file():
        sources.append(("previous-day-cyberlog", previous_day, previous_cyberlog))
    else:
        warnings.append(f"Missing historical context: {display_path(previous_cyberlog, config.workspace_root)}")

    for offset in range(3, 0, -1):
        context_day = day - dt.timedelta(days=offset)
        boot_path = (
            config.daily_compiled_root
            / context_day.isoformat()
            / f"{config.generated_prefix}tomorrow-boot.md"
        )
        if boot_path.exists() and boot_path.is_file():
            sources.append(("recent-tomorrow-boot", context_day, boot_path))
        else:
            warnings.append(f"Missing historical context: {display_path(boot_path, config.workspace_root)}")
    return sources, warnings


def context_file_block(role: str, context_day: dt.date, path: Path, config: Config) -> str:
    block = file_block(path, config).rstrip("\n")
    return f'<context role="{role}" date="{context_day.isoformat()}">\n{block}\n</context>\n'


def build_daily_context(
    day: dt.date,
    context_sources: list[tuple[str, dt.date, Path]],
    warnings: list[str],
    config: Config,
) -> str:
    warning_text = "未发现缺失 historical context source。"
    if warnings:
        warning_text = "\n".join(f"- {warning}" for warning in warnings)

    source_text = "未收集到 historical context source 文件。\n"
    if context_sources:
        source_text = "\n".join(
            context_file_block(role, context_day, path, config).rstrip("\n")
            for role, context_day, path in context_sources
        ) + "\n"

    return f"""# AI Historical Context - {day.isoformat()}

This file is generated from previous compiled outputs. It is context only, not today's raw evidence.

## Boundary

- Use this context to detect continuity, repeated blockers, and yesterday's intended boot path.
- Do not treat historical context as proof that something happened today.
- Today's raw evidence remains `_ai-feed.md`.

## Warnings

{warning_text}

## Sources

{source_text.rstrip()}
"""


def build_daily_request(
    day: dt.date,
    prompt: str,
    feed: str,
    context: str,
    project_registry: str | None,
) -> str:
    next_day = day + dt.timedelta(days=1)
    day_dir = f"Daily/compiled/{day.isoformat()}"
    rendered_prompt = render_template(
        prompt,
        {
            "date": day.isoformat(),
            "next_date": next_day.isoformat(),
        },
    )
    if project_registry:
        project_registry_text = f"```yaml\n{project_registry.rstrip()}\n```"
    else:
        project_registry_text = "未发现 `System/projects.yml`。如果今天涉及多个项目，请按 raw 中最具体的项目名临时分组，并在输出中标记项目注册表缺失。"
    return f"""# AI Sync Request - {day.isoformat()}

## 使用说明

复制本文件全部内容，粘贴给 AI。

AI 输出后建议保存为：
- `{day_dir}/_cyberlog.md`
- `{day_dir}/_tomorrow-boot.md`
- `{day_dir}/_ai-output-audit.md`

请先审核 AI 输出，不要让 AI 覆盖任何非下划线开头的原始 notes。

## Codex / Agent 执行模式

如果你是 Codex、agent，或者任何可以读写此仓库文件的 AI，请默认完整处理，不要只返回文本答案：

1. 读取本 request、同目录 `_ai-audit.md` 和 `_ai-context.md`。
2. 生成并保存 `{day_dir}/_cyberlog.md`。
3. 生成并保存 `{day_dir}/_tomorrow-boot.md`。
4. 生成并保存 `{day_dir}/_ai-output-audit.md`，说明是否发现误读草稿状态、混入被排除目录、把推断升级成事实等问题。
5. 不覆盖任何非 `_` 开头的原始 notes。

只有在没有文件写入能力时，才把结果完整输出到聊天窗口。

## Prompt

{rendered_prompt.rstrip()}

## Project Registry

以下内容来自 `System/projects.yml`。它是项目 id、aliases、器件口径和约束的规范层；用于项目分页、别名归一化和冲突提示。

{project_registry_text}

## Historical Context

以下内容来自同目录 `_ai-context.md`。它只用于识别跨日连续性和重复 blocker，不是今天的 raw evidence。

{context.rstrip()}

## AI Feed

{feed.rstrip()}
"""


def status_line(label: str, ok: bool) -> str:
    return f"- [{'ok' if ok else 'warn'}] {label}"


def build_daily_audit(
    day: dt.date,
    source_files: list[Path],
    excluded_files: list[tuple[Path, str]],
    context_sources: list[tuple[str, dt.date, Path]],
    context_warnings: list[str],
    project_registry: str | None,
    prompt: str,
    request: str,
    config: Config,
) -> str:
    risk_patterns = (
        "可选方案",
        "我建议你选",
        "如果选错会怎样",
        "你现在只要决定的 1 件事",
        "未发送",
        "没有发送",
        "最终发送",
        "直接复制发送",
    )
    risk_hits: list[str] = []
    for path in source_files:
        content = path.read_text(encoding="utf-8")
        hits = [pattern for pattern in risk_patterns if pattern in content]
        if hits:
            risk_hits.append(
                f"- {display_path(path, config.workspace_root)}: {', '.join(hits)}"
            )

    included_paths = "\n".join(
        f"- {display_path(path, config.workspace_root)}" for path in source_files
    )
    excluded_paths = "\n".join(
        f"- {display_path(path, config.workspace_root)} — {reason}"
        for path, reason in excluded_files
    )
    context_paths = "\n".join(
        f"- {role} {context_day.isoformat()}: {display_path(path, config.workspace_root)}"
        for role, context_day, path in context_sources
    )
    context_warning_text = "\n".join(f"- {warning}" for warning in context_warnings)
    prompt_checks = "\n".join(
        (
            status_line("prompt references Project Registry", "Project Registry" in prompt),
            status_line("prompt contains project clustering guard", "按 project id 聚类" in prompt or "按项目聚类" in prompt),
            status_line("prompt requires project id grouping", "project id" in prompt),
            status_line("prompt contains information type labels", "fact / draft / sent-message" in prompt),
            status_line("prompt downgrades chatroom / historical AI suggestions", "`chatroom`" in prompt),
            status_line("prompt requires _cyberlog.md delimiter", "# FILE: _cyberlog.md" in prompt),
            status_line("prompt requires _tomorrow-boot.md delimiter", "# FILE: _tomorrow-boot.md" in prompt),
        )
    )
    request_checks = "\n".join(
        (
            status_line("request contains _cyberlog.md delimiter", "# FILE: _cyberlog.md" in request),
            status_line("request contains _tomorrow-boot.md delimiter", "# FILE: _tomorrow-boot.md" in request),
            status_line("request has at least one source file", bool(source_files)),
            status_line("request includes Project Registry section", "## Project Registry" in request),
            status_line("request includes System/projects.yml content", bool(project_registry)),
            status_line("request separates historical context from AI Feed", "## Historical Context" in request),
            status_line("request marks historical context as not raw evidence", "不是今天的 raw evidence" in request),
            status_line(
                "request omits files from configured excluded directories",
                not any(
                    reason.startswith("excluded directory")
                    and display_path(path, config.workspace_root) in request
                    for path, reason in excluded_files
                ),
            ),
        )
    )
    risk_section = "\n".join(risk_hits) if risk_hits else "- 未发现"
    provenance_rows = "\n".join(
        f"- `{path}` — sha256:{digest}" for path, digest in provenance_hashes(config).items()
    )

    return f"""# AI Request Audit - {day.isoformat()}

## Summary

- Included source files: {len(source_files)}
- Excluded markdown files: {len(excluded_files)}
- Included historical context files: {len(context_sources)}
- Missing historical context files: {len(context_warnings)}
- Project registry included: {'yes' if project_registry else 'no'}
- Configured excluded directories: {', '.join(config.daily_exclude_dirs) if config.daily_exclude_dirs else '未配置'}

## Provenance

{provenance_rows if provenance_rows else '- 未发现'}

## Included Source Files

{included_paths if included_paths else '- 未发现'}

## Included Historical Context Files

{context_paths if context_paths else '- 未发现'}

## Missing Historical Context Files

{context_warning_text if context_warning_text else '- 未发现'}

## Excluded Source Files

{excluded_paths if excluded_paths else '- 未发现'}

## Prompt Checks

{prompt_checks}

## Request Checks

{request_checks}

## Potential Mixed-State Or AI-Suggestion Cues In Included Sources

{risk_section}

## Notes

- This audit checks the generated request package, not the AI answer.
- Files under configured excluded directories should be manually distilled into normal raw notes if they contain decisions, sent messages, or action items.
"""


def command_daily(args: argparse.Namespace, config: Config) -> int:
    day = parse_date(args.date)
    raw_dir = config.daily_raw_root / day.isoformat()
    compiled_dir = config.daily_compiled_root / day.isoformat()
    if not raw_dir.exists() or not raw_dir.is_dir():
        raise CyberlogError(
            f"Daily raw folder not found: {display_path(raw_dir, config.workspace_root)}. "
            "Create it first or run `python3 tools/cyberlog.py today` for today's folder."
        )

    source_files, excluded_files = daily_source_files(raw_dir, config)
    if not source_files:
        raise CyberlogError(
            f"No raw markdown files found in {display_path(raw_dir, config.workspace_root)}. "
            f"Files starting with '{config.generated_prefix}' are intentionally excluded."
        )

    feed = join_blocks(source_files, config)
    context_sources, context_warnings = daily_context_sources(day, config)
    context = build_daily_context(day, context_sources, context_warnings, config)
    prompt = read_required_prompt(config.system_root / "ai-sync-prompt.md", config)
    project_registry = read_optional_text(config.system_root / "projects.yml")
    request = build_daily_request(day, prompt, feed, context, project_registry)
    audit = build_daily_audit(
        day,
        source_files,
        excluded_files,
        context_sources,
        context_warnings,
        project_registry,
        prompt,
        request,
        config,
    )

    feed_path = compiled_dir / f"{config.generated_prefix}ai-feed.md"
    context_path = compiled_dir / f"{config.generated_prefix}ai-context.md"
    request_path = compiled_dir / f"{config.generated_prefix}ai-request.md"
    audit_path = compiled_dir / f"{config.generated_prefix}ai-audit.md"
    write_text(feed_path, feed)
    write_text(context_path, context)
    write_text(request_path, request)
    write_text(audit_path, audit)
    record_run_state_transition(
        day,
        "packaged",
        "daily",
        config,
        updates={
            "provenance": provenance_hashes(config),
            "source_files_sha256": path_hashes(source_files, config),
            "outputs": output_status((feed_path, context_path, request_path, audit_path), config),
        },
        transition_details={
            "source_files": len(source_files),
            "excluded_files": len(excluded_files),
            "historical_context_files": len(context_sources),
            "missing_historical_context_files": len(context_warnings),
        },
    )
    state_path = run_state_path(day, config)

    print(f"Wrote {display_path(feed_path, config.workspace_root)}")
    print(f"Wrote {display_path(context_path, config.workspace_root)}")
    print(f"Wrote {display_path(request_path, config.workspace_root)}")
    print(f"Wrote {display_path(audit_path, config.workspace_root)}")
    print(f"Wrote {display_path(state_path, config.workspace_root)}")
    print(f"Merged {len(source_files)} raw markdown file(s).")
    print(f"Included {len(context_sources)} historical context file(s).")
    if project_registry:
        print("Included project registry.")
    else:
        print("Project registry not found.")
    if excluded_files:
        print(f"Excluded {len(excluded_files)} markdown file(s).")
    if context_warnings:
        print(f"Missing {len(context_warnings)} historical context file(s).")
    return 0


def find_text_hits(paths: Iterable[Path], term: str) -> list[TextHit]:
    needle = term.lower()
    hits: list[TextHit] = []
    for path in paths:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if needle in line.lower():
                hits.append(TextHit(path=path, line_number=line_number, line=line.strip()))
    return hits


def format_hit(hit: TextHit, config: Config) -> str:
    evidence = hit.line
    if len(evidence) > 240:
        evidence = evidence[:237].rstrip() + "..."
    return f"`{display_path(hit.path, config.workspace_root)}:{hit.line_number}` — {evidence}"


def conflict_scan_sources(day: dt.date, config: Config) -> tuple[list[Path], list[str]]:
    paths: list[Path] = []
    warnings: list[str] = []
    raw_dir = config.daily_raw_root / day.isoformat()
    if raw_dir.exists() and raw_dir.is_dir():
        source_files, excluded_files = daily_source_files(raw_dir, config)
        paths.extend(source_files)
        if excluded_files:
            warnings.append(f"Excluded {len(excluded_files)} raw markdown file(s) using daily exclude rules.")
    else:
        warnings.append(f"Raw folder not found: {display_path(raw_dir, config.workspace_root)}")

    feed_path = config.daily_compiled_root / day.isoformat() / f"{config.generated_prefix}ai-feed.md"
    if feed_path.exists() and feed_path.is_file():
        paths.append(feed_path)
    elif not paths:
        warnings.append(f"AI feed not found: {display_path(feed_path, config.workspace_root)}")

    deduped: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            deduped.append(path)
    return deduped, warnings


def lpddr_term_hits(source_files: list[Path]) -> tuple[list[TextHit], list[TextHit]]:
    lpddr5_hits: list[TextHit] = []
    lpddr5x_hits: list[TextHit] = []
    lpddr5_pattern = re.compile(r"\bLPDDR5\b(?!X)", re.IGNORECASE)
    lpddr5x_pattern = re.compile(r"\bLPDDR5X\b", re.IGNORECASE)
    for path in source_files:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if lpddr5_pattern.search(line):
                lpddr5_hits.append(TextHit(path=path, line_number=line_number, line=line.strip()))
            if lpddr5x_pattern.search(line):
                lpddr5x_hits.append(TextHit(path=path, line_number=line_number, line=line.strip()))
    return lpddr5_hits, lpddr5x_hits


def analyze_conflict_gate(
    day: dt.date,
    source_files: list[Path],
    source_warnings: list[str],
    projects: list[ProjectEntry],
    config: Config,
) -> list[GateFinding]:
    findings: list[GateFinding] = []
    for warning in source_warnings:
        findings.append(GateFinding("warning", "source", warning))

    for project in projects:
        for alias in project.forbidden_aliases:
            hits = find_text_hits(source_files, alias)
            if hits:
                findings.append(
                    GateFinding(
                        "blocking",
                        "forbidden_alias",
                        f"`{alias}` appeared for `{project.project_id}`.",
                        tuple(format_hit(hit, config) for hit in hits[:5]),
                    )
                )

    lpddr5_hits, lpddr5x_hits = lpddr_term_hits(source_files)
    has_not_lpddr5x_constraint = any(
        "not lpddr5x" in " ".join(project.constraints).lower()
        for project in projects
    )
    if lpddr5_hits and lpddr5x_hits:
        severity = "blocking" if has_not_lpddr5x_constraint else "warning"
        findings.append(
            GateFinding(
                severity,
                "memory_protocol",
                f"`LPDDR5` and `LPDDR5X` both appear in {day.isoformat()} sources.",
                tuple(format_hit(hit, config) for hit in lpddr5x_hits[:5]),
            )
        )
    elif lpddr5x_hits and has_not_lpddr5x_constraint:
        findings.append(
            GateFinding(
                "blocking",
                "memory_constraint",
                "`LPDDR5X` appears while a project constraint says NOT LPDDR5X.",
                tuple(format_hit(hit, config) for hit in lpddr5x_hits[:5]),
            )
        )

    return findings


def build_conflicts_report(
    day: dt.date,
    source_files: list[Path],
    source_warnings: list[str],
    projects: list[ProjectEntry],
    config: Config,
) -> str:
    source_list = "\n".join(f"- `{display_path(path, config.workspace_root)}`" for path in source_files)
    warning_list = "\n".join(f"- {warning}" for warning in source_warnings)
    gate_findings = analyze_conflict_gate(day, source_files, source_warnings, projects, config)
    result = gate_result(gate_findings)

    forbidden_lines: list[str] = []
    for project in projects:
        for alias in project.forbidden_aliases:
            hits = find_text_hits(source_files, alias)
            for hit in hits:
                forbidden_lines.append(
                    f"- `{alias}` matched forbidden_aliases for `{project.project_id}`: {format_hit(hit, config)}"
                )

    alias_lines: list[str] = []
    generic_aliases = {"cyberlog", "daily", "workflow", "ai sync", "workspace", "skills", "my wiki", "github wiki"}
    for project in projects:
        for alias in project.aliases:
            if alias == project.project_id:
                continue
            if alias.lower() in generic_aliases:
                continue
            hits = find_text_hits(source_files, alias)
            if hits:
                alias_lines.append(
                    f"- `{alias}` appeared {len(hits)} time(s); normalize to `{project.project_id}` in compiled output."
                )

    lpddr5_hits, lpddr5x_hits = lpddr_term_hits(source_files)

    memory_lines: list[str] = []
    if lpddr5_hits and lpddr5x_hits:
        memory_lines.append(
            f"- `LPDDR5` and `LPDDR5X` both appear in {day.isoformat()} sources; treat memory protocol wording as unresolved until a project decision closes it."
        )
    elif lpddr5x_hits:
        memory_lines.append("- `LPDDR5X` appears; check whether the project accepts it.")
    elif lpddr5_hits:
        memory_lines.append("- `LPDDR5` appears without `LPDDR5X`; no static LPDDR5/LPDDR5X coexistence conflict detected.")

    for hit in lpddr5x_hits[:10]:
        memory_lines.append(f"- LPDDR5X evidence: {format_hit(hit, config)}")
    if len(lpddr5x_hits) > 10:
        memory_lines.append(f"- Additional LPDDR5X hits omitted: {len(lpddr5x_hits) - 10}")

    constraint_lines: list[str] = []
    for project in projects:
        joined_constraints = " ".join(project.constraints).lower()
        if "not lpddr5x" in joined_constraints and lpddr5x_hits:
            constraint_lines.append(
                f"- `{project.project_id}` has a NOT LPDDR5X constraint, but LPDDR5X appears in the day sources. This needs an explicit accept/reject decision."
            )

    if not constraint_lines:
        constraint_lines.append("- No static project-constraint conflict detected from configured rules.")

    return f"""# Conflict Scan - {day.isoformat()}

Generated by `tools/cyberlog.py conflict-scan --date {day.isoformat()}`.

## Gate Summary

- Gate result: {result}
- Blocking findings: {count_findings(gate_findings, 'blocking')}
- Warning findings: {count_findings(gate_findings, 'warning')}
- Info findings: {count_findings(gate_findings, 'info')}

## Gate Findings

{format_gate_findings(gate_findings)}

## Sources

{source_list if source_list else '- No source files were available.'}

## Warnings

{warning_list if warning_list else '- None'}

## 1. Project / Device Vocabulary

### Forbidden Alias Hits

{chr(10).join(forbidden_lines) if forbidden_lines else '- No forbidden aliases found.'}

### Alias Normalization Hints

{chr(10).join(alias_lines) if alias_lines else '- No project aliases found.'}

## 2. LPDDR5 / LPDDR5X Candidate Conflict

{chr(10).join(memory_lines) if memory_lines else '- No LPDDR5 or LPDDR5X terms found.'}

## 3. Static Constraint Review

{chr(10).join(constraint_lines)}

## 4. Semantic Conflict Review

- Not run. This command currently performs deterministic static checks only. Use this section as the future LLM-backed slot, with input limited to today's raw sources plus `System/projects.yml` constraints.

## Closure Checklist

- Resolve or explicitly accept every forbidden-alias hit before using the affected device statement as design evidence.
- If LPDDR5 and LPDDR5X both appear, add or update a `_decisions.yml` entry that records the accepted protocol/capacity/lifecycle tradeoff.
- Keep unresolved items visible in `_cyberlog.md` Blocked or Unfinished Tasks.
"""


def command_conflict_scan(args: argparse.Namespace, config: Config) -> int:
    day = parse_date(args.date)
    projects, _ = load_project_registry(config)
    source_files, source_warnings = conflict_scan_sources(day, config)
    compiled_dir = config.daily_compiled_root / day.isoformat()
    output_path = compiled_dir / f"{config.generated_prefix}conflicts.md"
    report = build_conflicts_report(day, source_files, source_warnings, projects, config)
    write_text(output_path, report)

    print(f"Wrote {display_path(output_path, config.workspace_root)}")
    print(f"Scanned {len(source_files)} source file(s).")
    if source_warnings:
        print("Warnings:")
        for warning in source_warnings:
            print(f"- {warning}")
    return 0


def parse_decisions_file(path: Path) -> list[DecisionRecord]:
    records: list[DecisionRecord] = []
    current: dict[str, object] | None = None

    def flush() -> None:
        nonlocal current
        if current is None:
            return
        decision_id = str(current.get("id", "")).strip()
        if decision_id:
            records.append(
                DecisionRecord(
                    decision_id=decision_id,
                    project=str(current.get("project", "unknown")).strip() or "unknown",
                    topic=str(current.get("topic", "")).strip(),
                    status=str(current.get("status", "unknown")).strip() or "unknown",
                    owner=str(current.get("owner", "")).strip(),
                    next_action=str(current.get("next", "")).strip(),
                    blockers=tuple(str(item) for item in current.get("blockers", ()) if str(item).strip()),
                    supersedes=tuple(str(item) for item in current.get("supersedes", ()) if str(item).strip()),
                    evidence=tuple(str(item) for item in current.get("evidence", ()) if str(item).strip()),
                    source_path=path,
                    present_fields=tuple(str(item) for item in current.keys()),
                )
            )
        current = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        stripped = raw_line.strip()
        if stripped.startswith("- "):
            flush()
            current = {}
            item = stripped[2:]
            if ":" in item:
                key, value = item.split(":", 1)
                current[key.strip()] = parse_yaml_scalar(value)
            continue
        if current is None or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in {"blockers", "supersedes", "evidence"}:
            current[key] = parse_yaml_list(value)
        else:
            current[key] = parse_yaml_scalar(value)
    flush()
    return records


def parse_comms_file(path: Path) -> list[CommsRecord]:
    records: list[CommsRecord] = []
    current: dict[str, str] | None = None

    def flush() -> None:
        nonlocal current
        if current is None:
            return
        comms_id = str(current.get("id", "")).strip()
        if comms_id:
            records.append(
                CommsRecord(
                    comms_id=comms_id,
                    project=str(current.get("project", "unknown")).strip() or "unknown",
                    channel=str(current.get("channel", "")).strip(),
                    draft=str(current.get("draft", "")).strip(),
                    status=str(current.get("status", "unknown")).strip() or "unknown",
                    sent_to=str(current.get("sent_to", "")).strip(),
                    sent_at=str(current.get("sent_at", "")).strip(),
                    waiting_for=str(current.get("waiting_for", "")).strip(),
                    expected_reply_by=str(current.get("expected_reply_by", "")).strip(),
                    source_path=path,
                    present_fields=tuple(str(item) for item in current.keys()),
                )
            )
        current = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        stripped = raw_line.strip()
        if stripped.startswith("- "):
            flush()
            current = {}
            item = stripped[2:]
            if ":" in item:
                key, value = item.split(":", 1)
                current[key.strip()] = parse_yaml_scalar(value)
            continue
        if current is None or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        current[key.strip()] = parse_yaml_scalar(value)
    flush()
    return records


def comms_source_paths(through: dt.date, config: Config) -> list[Path]:
    paths: list[Path] = []
    if not config.daily_compiled_root.exists():
        return paths
    for path in sorted(config.daily_compiled_root.iterdir()):
        day = parsed_daily_dir(path)
        if day is None or day > through:
            continue
        comms_path = path / f"{config.generated_prefix}comms.yml"
        if comms_path.exists() and comms_path.is_file():
            paths.append(comms_path)
    return paths


def project_priority_map(projects: list[ProjectEntry]) -> dict[str, str]:
    return {project.project_id: project.priority.upper() for project in projects if project.priority}


def high_priority_project(project_id: str, priorities: dict[str, str]) -> bool:
    return priorities.get(project_id, "").upper() in {"P0", "P1"}


def analyze_comms_aging(
    records: list[CommsRecord],
    through: dt.date,
    project_priorities: dict[str, str] | None = None,
) -> list[GateFinding]:
    findings: list[GateFinding] = []
    project_priorities = project_priorities or {}
    required_fields = ("id", "project", "channel", "status")
    allowed_statuses = {"draft", "sent", "waiting_for_reply", "replied", "closed"}
    for record in records:
        missing_fields = [field for field in required_fields if field not in record.present_fields]
        if missing_fields:
            findings.append(
                GateFinding(
                    "warning",
                    "comms_schema",
                    f"`{record.comms_id}` is missing required field(s): {', '.join(missing_fields)}.",
                )
            )
        if record.status not in allowed_statuses:
            findings.append(
                GateFinding(
                    "warning",
                    "comms_status",
                    f"`{record.comms_id}` has non-standard status `{record.status}`.",
                )
            )

        created = extract_date(record.comms_id) or extract_date(record.sent_at) or extract_date(record.source_path.as_posix())
        age_days = (through - created).days if created else None
        if record.status == "draft":
            if age_days is None:
                severity = "warning"
                message = f"`{record.comms_id}` is draft and has no discoverable date for aging."
            elif age_days > 3:
                severity = "warning"
                message = f"`{record.comms_id}` has been draft for {age_days} day(s)."
            else:
                severity = "info"
                message = f"`{record.comms_id}` is draft for {age_days} day(s)."
            findings.append(GateFinding(severity, "comms_draft_aging", message))

        if record.status == "waiting_for_reply":
            expected = extract_date(record.expected_reply_by)
            if expected and expected < through:
                findings.append(
                    GateFinding(
                        "warning",
                        "comms_reply_overdue",
                        f"`{record.comms_id}` expected reply by {expected.isoformat()} and is still waiting.",
                    )
                )
            elif not expected and high_priority_project(record.project, project_priorities):
                findings.append(
                    GateFinding(
                        "warning",
                        "comms_missing_expected_reply_by",
                        f"`{record.comms_id}` is P0/P1 waiting_for_reply without expected_reply_by.",
                    )
                )
    return findings


def decision_source_paths(through: dt.date, config: Config) -> list[Path]:
    paths: list[Path] = []
    if not config.daily_compiled_root.exists():
        return paths
    for path in sorted(config.daily_compiled_root.iterdir()):
        day = parsed_daily_dir(path)
        if day is None or day > through:
            continue
        decision_path = path / f"{config.generated_prefix}decisions.yml"
        if decision_path.exists() and decision_path.is_file():
            paths.append(decision_path)
    return paths


def table_cell(value: str) -> str:
    return value.replace("\n", " ").replace("|", "\\|").strip()


def active_decision_records(records: list[DecisionRecord]) -> list[DecisionRecord]:
    superseded_ids = {item for record in records for item in record.supersedes}
    return [
        record
        for record in records
        if record.status.lower() not in {"frozen", "superseded"} and record.decision_id not in superseded_ids
    ]


def normalize_topic(value: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", value.lower())


def analyze_decision_integrity(records: list[DecisionRecord], config: Config) -> list[GateFinding]:
    findings: list[GateFinding] = []
    all_ids = {record.decision_id for record in records}
    active = active_decision_records(records)
    required_active_fields = ("owner", "next", "evidence", "blockers")

    for record in active:
        missing_fields = [field for field in required_active_fields if field not in record.present_fields]
        if missing_fields:
            findings.append(
                GateFinding(
                    "warning",
                    "decision_schema",
                    f"`{record.decision_id}` is missing required active field(s): {', '.join(missing_fields)}.",
                    (display_path(record.source_path, config.workspace_root),),
                )
            )
        if not record.owner:
            findings.append(GateFinding("warning", "decision_owner", f"`{record.decision_id}` has empty owner."))
        if not record.next_action:
            findings.append(GateFinding("warning", "decision_next", f"`{record.decision_id}` has empty next action."))
        if not record.evidence:
            findings.append(GateFinding("warning", "decision_evidence", f"`{record.decision_id}` has no evidence."))

    for record in records:
        missing_targets = [target for target in record.supersedes if target not in all_ids]
        if missing_targets:
            findings.append(
                GateFinding(
                    "blocking",
                    "decision_supersedes",
                    f"`{record.decision_id}` supersedes unknown decision id(s): {', '.join(missing_targets)}.",
                )
            )

    seen_topics: dict[tuple[str, str], DecisionRecord] = {}
    for record in active:
        normalized = normalize_topic(record.topic)
        if not normalized:
            continue
        key = (record.project, normalized)
        previous = seen_topics.get(key)
        if previous:
            findings.append(
                GateFinding(
                    "warning",
                    "decision_duplicate_topic",
                    f"`{previous.decision_id}` and `{record.decision_id}` have the same normalized topic in `{record.project}` without a supersedes chain.",
                )
            )
        else:
            seen_topics[key] = record
    return findings


def build_decisions_rollup(
    through: dt.date,
    records: list[DecisionRecord],
    source_paths: list[Path],
    config: Config,
) -> str:
    superseded_ids = {item for record in records for item in record.supersedes}
    active = active_decision_records(records)
    integrity_findings = analyze_decision_integrity(records, config)
    active.sort(key=lambda item: (item.project, item.status, item.decision_id))

    source_list = "\n".join(f"- `{display_path(path, config.workspace_root)}`" for path in source_paths)
    if not active:
        project_sections = "- No active decisions found."
    else:
        sections: list[str] = []
        for project in sorted({record.project for record in active}):
            project_records = [record for record in active if record.project == project]
            rows = "\n".join(
                "| "
                + " | ".join(
                    (
                        table_cell(record.decision_id),
                        table_cell(record.status),
                        table_cell(record.topic),
                        table_cell(record.owner),
                        table_cell(record.next_action),
                        table_cell(", ".join(record.blockers)),
                        table_cell(", ".join(record.evidence)),
                    )
                )
                + " |"
                for record in project_records
            )
            sections.append(
                f"""## {project}

| ID | Status | Topic | Owner | Next | Blockers | Evidence |
|---|---|---|---|---|---|---|
{rows}"""
            )
        project_sections = "\n\n".join(sections)

    return f"""# Active Decisions - through {through.isoformat()}

Generated by `tools/cyberlog.py decisions --rollup --through {through.isoformat()}`.

## Summary

- Active decisions: {len(active)}
- Parsed decisions: {len(records)}
- Source files: {len(source_paths)}
- Excluded statuses from active view: frozen, superseded
- Implicitly excluded by supersedes chain: {len(superseded_ids)}
- Integrity gate result: {gate_result(integrity_findings)}
- Integrity blocking findings: {count_findings(integrity_findings, 'blocking')}
- Integrity warning findings: {count_findings(integrity_findings, 'warning')}

## Sources

{source_list if source_list else '- No `_decisions.yml` files found.'}

## Integrity Checks

{format_gate_findings(integrity_findings)}

{project_sections}
"""


def command_decisions(args: argparse.Namespace, config: Config) -> int:
    if not args.rollup:
        raise CyberlogError("Only `decisions --rollup` is currently supported.")
    through = parse_date(args.through) if args.through else today_from_environment()
    source_paths = decision_source_paths(through, config)
    records: list[DecisionRecord] = []
    for path in source_paths:
        records.extend(parse_decisions_file(path))

    output_path = Path(args.output) if args.output else config.system_root / "decisions-active.md"
    if not output_path.is_absolute():
        output_path = config.workspace_root / output_path
    report = build_decisions_rollup(through, records, source_paths, config)
    write_text(output_path, report)

    print(f"Wrote {display_path(output_path, config.workspace_root)}")
    print(f"Parsed {len(records)} decision(s) from {len(source_paths)} file(s).")
    return 0


def validate_project_registry(projects: list[ProjectEntry], registry_text: str | None, config: Config) -> list[GateFinding]:
    findings: list[GateFinding] = []
    if registry_text is None:
        findings.append(
            GateFinding(
                "warning",
                "schema_projects",
                f"Project registry missing: `{display_path(projects_registry_path(config), config.workspace_root)}`.",
            )
        )
        return findings
    if not projects:
        findings.append(GateFinding("warning", "schema_projects", "`System/projects.yml` contains no parsed projects."))
    seen_ids: set[str] = set()
    for project in projects:
        if project.project_id in seen_ids:
            findings.append(GateFinding("warning", "schema_projects", f"Duplicate project id `{project.project_id}`."))
        seen_ids.add(project.project_id)
        if project.priority and project.priority.upper() not in {"P0", "P1", "P2", "P3"}:
            findings.append(
                GateFinding(
                    "warning",
                    "schema_projects",
                    f"`{project.project_id}` has non-standard priority `{project.priority}`.",
                )
            )
        if not project.aliases:
            findings.append(GateFinding("info", "schema_projects", f"`{project.project_id}` has no aliases."))
    return findings


def validate_schema_contract_files(config: Config) -> list[GateFinding]:
    path = config.system_root / "schemas.md"
    if path.exists() and path.is_file():
        return [GateFinding("info", "schema_contract", f"Schema contract present: `{display_path(path, config.workspace_root)}`.")]
    return [GateFinding("warning", "schema_contract", f"Schema contract missing: `{display_path(path, config.workspace_root)}`.")]


CYBERLOG_REQUIRED_HEADINGS = (
    "## 0. 项目索引",
    "## 1. 今日真实推进",
    "## 2. 当前工作画布",
    "## 3. 关键决策",
    "## 4. 重要信息",
    "## 5. 今日产出",
    "## 6. 未完成任务",
    "## 7. 明日启动包",
    "## 8. 工作流摩擦",
    "## 9. 自我迭代建议",
    "## 10. 规则候选",
)

TOMORROW_BOOT_REQUIRED_HEADINGS = (
    "## 明日主线",
    "## 背景",
    "## 当前状态",
    "## 第一动作",
    "## 注意事项",
    "## 不要重复踩的坑",
    "## 可以交给 AI / agent 的部分",
    "## 必须由我亲自判断的部分",
)


def markdown_headings(content: str) -> set[str]:
    return {line.strip() for line in content.splitlines() if line.lstrip().startswith("#")}


def markdown_section(content: str, heading: str) -> str:
    lines = content.splitlines()
    start: int | None = None
    heading_level = len(heading) - len(heading.lstrip("#"))
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index + 1
            break
    if start is None:
        return ""
    collected: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            if level <= heading_level:
                break
        collected.append(line)
    return "\n".join(collected)


def table_column_count(line: str) -> int:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return 0
    return len([cell for cell in stripped.strip("|").split("|")])


def feed_source_tokens(feed_path: Path) -> set[str]:
    if not feed_path.exists() or not feed_path.is_file():
        return set()
    content = feed_path.read_text(encoding="utf-8")
    tokens: set[str] = set()
    for match in re.finditer(r'<file\b[^>]*\bpath="([^"]+)"', content):
        path_text = html.unescape(match.group(1))
        tokens.add(path_text)
        tokens.add(Path(path_text).name)
    return tokens


def cited_markdown_tokens(content: str) -> set[str]:
    tokens: set[str] = set()
    for match in re.finditer(r"`([^`]+?\.md)`", content):
        token = match.group(1).strip()
        if token and not Path(token).name.startswith("_"):
            tokens.add(token)
    return tokens


def analyze_ai_output_contract(day: dt.date, config: Config) -> list[GateFinding]:
    findings: list[GateFinding] = []
    compiled_dir = config.daily_compiled_root / day.isoformat()
    cyberlog_path = compiled_dir / f"{config.generated_prefix}cyberlog.md"
    tomorrow_path = compiled_dir / f"{config.generated_prefix}tomorrow-boot.md"
    output_audit_path = compiled_dir / f"{config.generated_prefix}ai-output-audit.md"
    feed_path = compiled_dir / f"{config.generated_prefix}ai-feed.md"

    if not cyberlog_path.exists():
        findings.append(GateFinding("blocking", "ai_output_missing", f"Missing `{display_path(cyberlog_path, config.workspace_root)}`."))
    else:
        content = cyberlog_path.read_text(encoding="utf-8")
        headings = markdown_headings(content)
        missing = [heading for heading in CYBERLOG_REQUIRED_HEADINGS if heading not in headings]
        if missing:
            findings.append(
                GateFinding(
                    "blocking",
                    "cyberlog_structure",
                    f"`_cyberlog.md` is missing required section(s): {', '.join(missing)}.",
                    (display_path(cyberlog_path, config.workspace_root),),
                )
            )

        decision_section = markdown_section(content, "## 3. 关键决策")
        table_lines = [line for line in decision_section.splitlines() if line.strip().startswith("|")]
        if table_lines:
            column_count = table_column_count(table_lines[0])
            if column_count != 8:
                findings.append(
                    GateFinding(
                        "blocking",
                        "cyberlog_decision_table",
                        f"`_cyberlog.md` decision table has {column_count} column(s); expected 8.",
                        (table_lines[0].strip(),),
                    )
                )

        blocked_section = markdown_section(content, "### Blocked")
        if blocked_section and "未发现" not in blocked_section:
            required_terms = ("阻塞原因", "解除方式", "owner", "下一步")
            missing_terms = [term for term in required_terms if term not in blocked_section]
            if missing_terms:
                findings.append(
                    GateFinding(
                        "warning",
                        "cyberlog_blocked_detail",
                        f"`### Blocked` may be missing required detail(s): {', '.join(missing_terms)}.",
                    )
                )

        allowed_sources = feed_source_tokens(feed_path)
        if allowed_sources:
            unknown_citations = sorted(token for token in cited_markdown_tokens(content) if token not in allowed_sources and Path(token).name not in allowed_sources)
            if unknown_citations:
                findings.append(
                    GateFinding(
                        "warning",
                        "source_reference",
                        "`_cyberlog.md` cites markdown source(s) not found in today's `_ai-feed.md`.",
                        tuple(unknown_citations[:10]),
                    )
                )

    if not tomorrow_path.exists():
        findings.append(GateFinding("blocking", "ai_output_missing", f"Missing `{display_path(tomorrow_path, config.workspace_root)}`."))
    else:
        content = tomorrow_path.read_text(encoding="utf-8")
        headings = markdown_headings(content)
        missing = [heading for heading in TOMORROW_BOOT_REQUIRED_HEADINGS if heading not in headings]
        if missing:
            findings.append(
                GateFinding(
                    "blocking",
                    "tomorrow_boot_structure",
                    f"`_tomorrow-boot.md` is missing required section(s): {', '.join(missing)}.",
                    (display_path(tomorrow_path, config.workspace_root),),
                )
            )

    if not output_audit_path.exists() or not output_audit_path.read_text(encoding="utf-8").strip():
        findings.append(GateFinding("warning", "ai_output_audit", "`_ai-output-audit.md` is missing or empty."))

    return findings


def build_validation_report(day: dt.date, config: Config) -> tuple[str, list[GateFinding]]:
    projects, registry_text = load_project_registry(config)
    source_files, source_warnings = conflict_scan_sources(day, config)
    decision_paths = decision_source_paths(day, config)
    decision_records: list[DecisionRecord] = []
    for path in decision_paths:
        decision_records.extend(parse_decisions_file(path))
    comms_paths = comms_source_paths(day, config)
    comms_records: list[CommsRecord] = []
    for path in comms_paths:
        comms_records.extend(parse_comms_file(path))

    schema_findings = validate_schema_contract_files(config) + validate_project_registry(projects, registry_text, config)
    conflict_findings = analyze_conflict_gate(day, source_files, source_warnings, projects, config)
    ai_output_findings = analyze_ai_output_contract(day, config)
    decision_findings = analyze_decision_integrity(decision_records, config)
    comms_findings = analyze_comms_aging(comms_records, day, project_priority_map(projects))
    findings = schema_findings + conflict_findings + ai_output_findings + decision_findings + comms_findings

    source_list = "\n".join(f"- `{display_path(path, config.workspace_root)}`" for path in source_files)
    decision_source_list = "\n".join(f"- `{display_path(path, config.workspace_root)}`" for path in decision_paths)
    comms_source_list = "\n".join(f"- `{display_path(path, config.workspace_root)}`" for path in comms_paths)

    report = f"""# Cyberlog Validation - {day.isoformat()}

Generated by `tools/cyberlog.py validate --date {day.isoformat()}`.

## Gate Summary

- Gate result: {gate_result(findings)}
- Blocking findings: {count_findings(findings, 'blocking')}
- Warning findings: {count_findings(findings, 'warning')}
- Info findings: {count_findings(findings, 'info')}
- Error codes: {format_error_code_summary(findings)}

## Schema Contract

{format_gate_findings(schema_findings)}

## Conflict Gate

{format_gate_findings(conflict_findings)}

## AI Output Contract

{format_gate_findings(ai_output_findings)}

## Decision Integrity

{format_gate_findings(decision_findings)}

## Communication Aging

{format_gate_findings(comms_findings)}

## Sources Checked

### Daily Raw / Feed

{source_list if source_list else '- No raw/feed sources found.'}

### Decisions

{decision_source_list if decision_source_list else '- No `_decisions.yml` files found through this date.'}

### Communications

{comms_source_list if comms_source_list else '- No `_comms.yml` files found through this date.'}
"""
    return report, findings


def write_validation_report(day: dt.date, config: Config) -> tuple[Path, list[GateFinding]]:
    report, findings = build_validation_report(day, config)
    result = gate_result(findings)
    output_path = config.daily_compiled_root / day.isoformat() / f"{config.generated_prefix}validation.md"
    write_text(output_path, report)
    record_run_state_transition(
        day,
        "validated" if result != "BLOCKED" else "validation_blocked",
        "validate",
        config,
        updates={
            "validation": {
                "gate_result": result,
                "blocking": count_findings(findings, "blocking"),
                "warning": count_findings(findings, "warning"),
                "info": count_findings(findings, "info"),
                "report": display_path(output_path, config.workspace_root),
            },
            "outputs": output_status((output_path,), config),
        },
    )
    return output_path, findings


def command_validate(args: argparse.Namespace, config: Config) -> int:
    day = parse_date(args.date)
    report, findings = build_validation_report(day, config)
    if args.write:
        output_path, findings = write_validation_report(day, config)
        print(f"Wrote {display_path(output_path, config.workspace_root)}")
    else:
        sys.stdout.write(report)
        if not report.endswith("\n"):
            print()
    if args.strict and any(finding.severity == "blocking" for finding in findings):
        return 1
    return 0


def golden_days_root(config: Config) -> Path:
    return config.reviews_root.parent / "golden-days"


def golden_contract_path(day: dt.date, config: Config) -> Path:
    return golden_days_root(config) / f"{day.isoformat()}.json"


def resolve_golden_file(day: dt.date, filename: str, config: Config) -> Path:
    value = filename.strip()
    if value.startswith("_"):
        return config.daily_compiled_root / day.isoformat() / value
    path = Path(value)
    if path.is_absolute():
        return path
    return config.workspace_root / path


def load_golden_contract(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CyberlogError(f"Invalid JSON in {path.as_posix()}: {exc}") from exc
    if not isinstance(data, dict):
        raise CyberlogError(f"Golden contract must be a JSON object: {path.as_posix()}")
    return data


def build_golden_contract(day: dt.date, config: Config) -> dict[str, object]:
    _, findings = build_validation_report(day, config)
    return {
        "date": day.isoformat(),
        "description": "Edit only the assertions that matter; leave the rest empty.",
        "observed_error_codes": observed_error_codes(findings),
        "assertions": {
            "required_error_codes": [],
            "forbidden_error_codes": [],
            "must_contain": {},
            "must_not_contain": {},
        },
        "notes": [
            "Use `_cyberlog.md` or `_tomorrow-boot.md` as shorthand keys for compiled files.",
            "Use repo-relative paths for other files.",
            "This file is a regression contract, not another daily note.",
        ],
    }


def command_golden_add(args: argparse.Namespace, config: Config) -> int:
    day = parse_date(args.date)
    path = golden_contract_path(day, config)
    if path.exists() and not args.force:
        print(f"Golden contract already exists: {display_path(path, config.workspace_root)}")
        print("Use `--force` to regenerate the scaffold.")
        return 0
    write_text(path, json.dumps(build_golden_contract(day, config), ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {display_path(path, config.workspace_root)}")
    print("Next manual step: edit only the assertions you care about.")
    return 0


def string_list(value: object) -> list[str]:
    if isinstance(value, str):
        return [value] if value else []
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item)]


def string_map_of_lists(value: object) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        return {}
    result: dict[str, list[str]] = {}
    for key, items in value.items():
        result[str(key)] = string_list(items)
    return result


def check_golden_contract(path: Path, config: Config) -> tuple[dt.date, list[str], list[GateFinding]]:
    contract = load_golden_contract(path)
    day = parse_date(str(contract.get("date", path.stem)))
    _, validation_findings = build_validation_report(day, config)
    observed_codes = set(observed_error_codes(validation_findings))
    assertions = contract.get("assertions", {})
    if not isinstance(assertions, dict):
        assertions = {}

    findings: list[GateFinding] = []
    required_codes = string_list(assertions.get("required_error_codes"))
    forbidden_codes = string_list(assertions.get("forbidden_error_codes"))
    must_contain = string_map_of_lists(assertions.get("must_contain"))
    must_not_contain = string_map_of_lists(assertions.get("must_not_contain"))

    for code in required_codes:
        if code not in observed_codes:
            findings.append(
                GateFinding(
                    "blocking",
                    "golden_required_error_code",
                    f"`{code}` is required by `{display_path(path, config.workspace_root)}` but was not observed.",
                )
            )
    for code in forbidden_codes:
        if code in observed_codes:
            findings.append(
                GateFinding(
                    "blocking",
                    "golden_forbidden_error_code",
                    f"`{code}` is forbidden by `{display_path(path, config.workspace_root)}` but was observed.",
                )
            )

    for filename, needles in must_contain.items():
        target = resolve_golden_file(day, filename, config)
        if not target.exists():
            findings.append(
                GateFinding(
                    "blocking",
                    "golden_file_missing",
                    f"Expected file is missing: `{display_path(target, config.workspace_root)}`.",
                )
            )
            continue
        content = target.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in content:
                findings.append(
                    GateFinding(
                        "blocking",
                        "golden_must_contain",
                        f"`{display_path(target, config.workspace_root)}` does not contain expected text `{needle}`.",
                    )
                )

    for filename, needles in must_not_contain.items():
        target = resolve_golden_file(day, filename, config)
        if not target.exists():
            continue
        content = target.read_text(encoding="utf-8")
        for needle in needles:
            if needle in content:
                findings.append(
                    GateFinding(
                        "blocking",
                        "golden_must_not_contain",
                        f"`{display_path(target, config.workspace_root)}` contains forbidden text `{needle}`.",
                    )
                )
    return day, sorted(observed_codes), findings


def golden_contract_paths(config: Config, day: dt.date | None) -> list[Path]:
    root = golden_days_root(config)
    if day is not None:
        path = golden_contract_path(day, config)
        if not path.exists():
            raise CyberlogError(f"Golden contract not found: {display_path(path, config.workspace_root)}")
        return [path]
    if not root.exists():
        return []
    return sorted(path for path in root.glob("*.json") if path.is_file())


def build_golden_report(config: Config, day: dt.date | None) -> tuple[str, list[GateFinding]]:
    paths = golden_contract_paths(config, day)
    all_findings: list[GateFinding] = []
    sections: list[str] = []
    for path in paths:
        contract_day, codes, findings = check_golden_contract(path, config)
        all_findings.extend(findings)
        sections.append(
            f"""## {contract_day.isoformat()}

- Contract: `{display_path(path, config.workspace_root)}`
- Observed error codes: {', '.join(codes) if codes else 'none'}
- Result: {gate_result(findings)}

{format_gate_findings(findings)}
"""
        )
    report = f"""# Golden Days Report

Generated by `tools/cyberlog.py golden check`.

## Summary

- Contracts checked: {len(paths)}
- Gate result: {gate_result(all_findings)}
- Blocking findings: {count_findings(all_findings, 'blocking')}

{''.join(sections) if sections else 'No golden contracts found.'}
"""
    return report, all_findings


def command_golden_check(args: argparse.Namespace, config: Config) -> int:
    day = parse_date(args.date) if args.date else None
    report, findings = build_golden_report(config, day)
    if args.write:
        output_path = golden_days_root(config) / "_golden-report.md"
        write_text(output_path, report)
        print(f"Wrote {display_path(output_path, config.workspace_root)}")
    else:
        sys.stdout.write(report)
        if not report.endswith("\n"):
            print()
    if args.strict and any(finding.severity == "blocking" for finding in findings):
        return 1
    return 0


def command_golden(args: argparse.Namespace, config: Config) -> int:
    if args.golden_command == "add":
        return command_golden_add(args, config)
    if args.golden_command == "check":
        return command_golden_check(args, config)
    raise CyberlogError("Unknown golden command.")


def parsed_daily_dir(path: Path) -> dt.date | None:
    if not path.is_dir():
        return None
    try:
        return dt.date.fromisoformat(path.name)
    except ValueError:
        return None


def complete_daily_outputs(day: dt.date, config: Config) -> tuple[bool, list[Path]]:
    compiled_dir = config.daily_compiled_root / day.isoformat()
    required_names = (
        f"{config.generated_prefix}ai-audit.md",
        f"{config.generated_prefix}cyberlog.md",
        f"{config.generated_prefix}tomorrow-boot.md",
        f"{config.generated_prefix}ai-output-audit.md",
    )
    missing = [compiled_dir / name for name in required_names if not (compiled_dir / name).is_file()]
    return not missing, missing


def run_state_phase(day: dt.date, config: Config) -> str:
    return str(read_run_state(day, config).get("phase", "unknown"))


def close_day_outputs(day: dt.date, config: Config) -> tuple[Path, Path, Path]:
    compiled_dir = config.daily_compiled_root / day.isoformat()
    return (
        compiled_dir / f"{config.generated_prefix}conflicts.md",
        config.system_root / "decisions-active.md",
        compiled_dir / f"{config.generated_prefix}validation.md",
    )


def command_close_day(args: argparse.Namespace, config: Config) -> int:
    day = parse_date(args.date)
    complete, missing = complete_daily_outputs(day, config)
    if not complete:
        print(f"Cannot close {day.isoformat()}: missing core output(s).")
        for path in missing:
            print(f"- {display_path(path, config.workspace_root)}")
        return 1

    print(f"Closing {day.isoformat()}...")
    command_conflict_scan(argparse.Namespace(date=day.isoformat()), config)
    command_decisions(argparse.Namespace(rollup=True, through=day.isoformat(), output=None), config)
    validation_path, findings = write_validation_report(day, config)
    result = gate_result(findings)
    print(f"Wrote {display_path(validation_path, config.workspace_root)}")
    print(f"Validation gate: {result}")
    print(f"Blocking findings: {count_findings(findings, 'blocking')}")
    print(f"Warning findings: {count_findings(findings, 'warning')}")
    if result == "BLOCKED":
        print("Day remains open because validation has blocking findings.")
        return 1

    conflict_path, decisions_path, validation_path = close_day_outputs(day, config)
    record_run_state_transition(
        day,
        "closed",
        "close-day",
        config,
        updates={
            "outputs": output_status(
                (
                    conflict_path,
                    decisions_path,
                    validation_path,
                    config.daily_compiled_root / day.isoformat() / f"{config.generated_prefix}cyberlog.md",
                    config.daily_compiled_root / day.isoformat() / f"{config.generated_prefix}tomorrow-boot.md",
                    config.daily_compiled_root / day.isoformat() / f"{config.generated_prefix}ai-output-audit.md",
                ),
                config,
            )
        },
        transition_details={"validation_gate": result},
    )
    print(f"Closed {day.isoformat()}.")
    return 0


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def raw_file_entries(raw_dir: Path) -> list[RawFileEntry]:
    entries: list[RawFileEntry] = []
    for path in sorted((item for item in raw_dir.rglob("*") if item.is_file()), key=lambda item: item.relative_to(raw_dir).as_posix()):
        entries.append(RawFileEntry(path=path, size=path.stat().st_size, sha256=file_sha256(path)))
    return entries


def run_state_path(day: dt.date, config: Config) -> Path:
    return config.daily_compiled_root / day.isoformat() / f"{config.generated_prefix}{RUN_STATE_FILE_NAME}"


def now_iso_from_environment() -> str:
    current = now_from_environment()
    if current.tzinfo is None:
        current = current.astimezone()
    return current.isoformat(timespec="seconds")


def read_run_state(day: dt.date, config: Config) -> dict[str, object]:
    path = run_state_path(day, config)
    if not path.exists():
        return {"date": day.isoformat(), "phase": "unknown", "transitions": []}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CyberlogError(f"Invalid run state JSON: {display_path(path, config.workspace_root)}") from exc
    if not isinstance(loaded, dict):
        raise CyberlogError(f"Invalid run state shape: {display_path(path, config.workspace_root)}")
    loaded.setdefault("date", day.isoformat())
    loaded.setdefault("phase", "unknown")
    loaded.setdefault("transitions", [])
    if not isinstance(loaded["transitions"], list):
        loaded["transitions"] = []
    return loaded


def write_run_state(day: dt.date, state: dict[str, object], config: Config) -> None:
    path = run_state_path(day, config)
    write_text(path, json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def record_run_state_transition(
    day: dt.date,
    phase: str,
    actor: str,
    config: Config,
    updates: dict[str, object] | None = None,
    transition_details: dict[str, object] | None = None,
) -> None:
    state = read_run_state(day, config)
    timestamp = now_iso_from_environment()
    transition: dict[str, object] = {"phase": phase, "at": timestamp, "by": actor}
    if transition_details:
        transition.update(transition_details)
    transitions = state.get("transitions")
    if not isinstance(transitions, list):
        transitions = []
    transitions.append(transition)
    state["transitions"] = transitions
    state["date"] = day.isoformat()
    state["phase"] = phase
    state["updated_at"] = timestamp
    if updates:
        for key, value in updates.items():
            if isinstance(value, dict) and isinstance(state.get(key), dict):
                merged = dict(state[key])  # type: ignore[arg-type]
                merged.update(value)
                state[key] = merged
            else:
                state[key] = value
    write_run_state(day, state, config)


def path_hashes(paths: Iterable[Path], config: Config) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in paths:
        if path.exists() and path.is_file():
            hashes[display_path(path, config.workspace_root)] = file_sha256(path)
    return hashes


def provenance_paths(config: Config) -> list[Path]:
    return [
        config.system_root / "ai-sync-prompt.md",
        config.system_root / "workflow-rules.md",
        config.system_root / "personal-operating-manual.md",
        config.system_root / "projects.yml",
        config.system_root / "schemas.md",
        config.system_root / "error-taxonomy.md",
        config.workspace_root / CONFIG_FILE_NAME,
    ]


def provenance_hashes(config: Config) -> dict[str, str]:
    return path_hashes(provenance_paths(config), config)


def output_status(paths: Iterable[Path], config: Config) -> dict[str, bool]:
    return {display_path(path, config.workspace_root): path.exists() and path.is_file() for path in paths}


def build_raw_discard_log(
    day: dt.date,
    cutoff: dt.date,
    entries: list[RawFileEntry],
    config: Config,
) -> str:
    total_bytes = sum(entry.size for entry in entries)
    rows = "\n".join(
        f"- `{display_path(entry.path, config.workspace_root)}` — {entry.size} bytes — sha256:{entry.sha256}"
        for entry in entries
    )
    return f"""# Raw Discard Log - {day.isoformat()}

## Summary

- Raw folder: `Daily/raw/{day.isoformat()}`
- Prune cutoff: before {cutoff.isoformat()}
- Deleted files: {len(entries)}
- Deleted bytes: {total_bytes}

## Deleted Files

{rows if rows else '- No files were present.'}

## Retention Policy

Raw is a temporary fact input layer, not the permanent record. The permanent daily record is the reviewed compiled output.
"""


def delete_raw_tree(raw_dir: Path) -> None:
    for path in sorted((item for item in raw_dir.rglob("*") if item.is_file()), key=lambda item: len(item.parts), reverse=True):
        path.unlink()
    for path in sorted((item for item in raw_dir.rglob("*") if item.is_dir()), key=lambda item: len(item.parts), reverse=True):
        path.rmdir()
    raw_dir.rmdir()


def command_prune_raw(args: argparse.Namespace, config: Config) -> int:
    if args.before and args.older_than is not None:
        raise CyberlogError("Use either --before or --older-than, not both.")
    if args.before:
        cutoff = parse_date(args.before)
    else:
        retention_days = config.raw_retention_days if args.older_than is None else args.older_than
        if retention_days < 0:
            raise CyberlogError("--older-than cannot be negative.")
        cutoff = today_from_environment() - dt.timedelta(days=retention_days)

    mode = "apply" if args.apply else "dry-run"
    candidates: list[tuple[dt.date, Path]] = []
    for path in sorted(config.daily_raw_root.iterdir() if config.daily_raw_root.exists() else []):
        day = parsed_daily_dir(path)
        if day is not None and day < cutoff:
            candidates.append((day, path))

    print(f"Mode: {mode}")
    print(f"Prune raw folders before: {cutoff.isoformat()}")
    if not candidates:
        print("No raw folders eligible by date.")
        return 0

    deleted_count = 0
    skipped_count = 0
    for day, raw_dir in candidates:
        complete, missing = complete_daily_outputs(day, config)
        if not complete:
            skipped_count += 1
            print(f"Skip {display_path(raw_dir, config.workspace_root)}: incomplete compiled outputs")
            for path in missing:
                print(f"  missing: {display_path(path, config.workspace_root)}")
            continue
        phase = run_state_phase(day, config)
        if phase != "closed":
            skipped_count += 1
            print(f"Skip {display_path(raw_dir, config.workspace_root)}: run state phase is `{phase}`, expected `closed`")
            continue

        entries = raw_file_entries(raw_dir)
        total_bytes = sum(entry.size for entry in entries)
        log_path = config.daily_compiled_root / day.isoformat() / f"{config.generated_prefix}raw-discard-log.md"
        if args.apply:
            write_text(log_path, build_raw_discard_log(day, cutoff, entries, config))
            delete_raw_tree(raw_dir)
            print(
                f"Deleted {display_path(raw_dir, config.workspace_root)} "
                f"({len(entries)} file(s), {total_bytes} bytes); wrote {display_path(log_path, config.workspace_root)}"
            )
        else:
            print(
                f"Would delete {display_path(raw_dir, config.workspace_root)} "
                f"({len(entries)} file(s), {total_bytes} bytes); would write {display_path(log_path, config.workspace_root)}"
            )
        deleted_count += 1

    if not args.apply:
        print("Dry run only. Re-run with --apply to delete eligible raw folders.")
    print(f"Eligible complete folders: {deleted_count}")
    print(f"Skipped incomplete folders: {skipped_count}")
    return 0


def daterange(start: dt.date, end: dt.date) -> Iterable[dt.date]:
    current = start
    while current <= end:
        yield current
        current += dt.timedelta(days=1)


def week_label(start: dt.date, end: dt.date, basis: str) -> str:
    basis_date = start if basis == "start" else end
    iso_year, iso_week, _ = basis_date.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def build_weekly_request(
    start: dt.date,
    end: dt.date,
    prompt: str,
    collected_paths: list[Path],
    warnings: list[str],
    config: Config,
) -> str:
    rendered_prompt = render_template(
        prompt,
        {
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
        },
    )
    warning_text = "未发现缺失文件。"
    if warnings:
        warning_text = "\n".join(f"- {warning}" for warning in warnings)
    collected = join_blocks(collected_paths, config) if collected_paths else "未收集到任何 weekly source 文件。\n"

    return f"""# AI Weekly Review Request - {start.isoformat()} to {end.isoformat()}

## 使用说明

复制本文件全部内容，粘贴给 AI。

周复盘优先使用每天的 `_cyberlog.md` 和 `_tomorrow-boot.md`，并可读取同一 compiled 目录下的 `_decisions.yml`、`_comms.yml`、`_conflicts.md` 状态文件；不读取原始 daily notes。

## Warnings

{warning_text}

## Prompt

{rendered_prompt.rstrip()}

## Weekly Sources

{collected.rstrip()}
"""


def command_weekly(args: argparse.Namespace, config: Config) -> int:
    start = parse_date(args.start)
    end = parse_date(args.end)
    if end < start:
        raise CyberlogError("--end must be the same as or later than --start.")

    prompt = read_required_prompt(config.system_root / "weekly-review-prompt.md", config)
    collected_paths: list[Path] = []
    warnings: list[str] = []

    for day in daterange(start, end):
        compiled_dir = config.daily_compiled_root / day.isoformat()
        if not compiled_dir.exists() or not compiled_dir.is_dir():
            warnings.append(f"Missing daily compiled folder: {display_path(compiled_dir, config.workspace_root)}")
            continue
        for filename in (f"{config.generated_prefix}cyberlog.md", f"{config.generated_prefix}tomorrow-boot.md"):
            path = compiled_dir / filename
            if path.exists() and path.is_file():
                collected_paths.append(path)
            else:
                warnings.append(f"Missing weekly source: {display_path(path, config.workspace_root)}")
        for filename in (
            f"{config.generated_prefix}decisions.yml",
            f"{config.generated_prefix}comms.yml",
            f"{config.generated_prefix}conflicts.md",
        ):
            path = compiled_dir / filename
            if path.exists() and path.is_file():
                collected_paths.append(path)

    label = week_label(start, end, config.weekly_week_basis)
    output_path = config.reviews_root / f"{label}{config.generated_prefix}ai-weekly-request.md"
    request = build_weekly_request(start, end, prompt, collected_paths, warnings, config)
    write_text(output_path, request)

    print(f"Wrote {display_path(output_path, config.workspace_root)}")
    print(f"Collected {len(collected_paths)} weekly source file(s).")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


def command_init(args: argparse.Namespace, config: Config) -> int:
    config.workspace_root.mkdir(parents=True, exist_ok=True)
    for path in (
        config.daily_root,
        config.daily_raw_root,
        config.daily_compiled_root,
        config.daily_templates_root,
        config.reviews_root,
        golden_days_root(config),
        config.system_root,
        config.workspace_root / "tools",
    ):
        path.mkdir(parents=True, exist_ok=True)

    templates = {
        config.daily_templates_root / "00-canvas.md": CANVAS_TEMPLATE.format(date="{{date}}"),
        config.daily_templates_root / "01-notes.md": "# Notes - {{date}}\n\n",
        config.daily_templates_root / "02-research.md": "# Research - {{date}}\n\n",
        config.daily_templates_root / "03-agent.md": "# Agent - {{date}}\n\n",
        config.system_root / "ai-sync-prompt.md": AI_SYNC_PROMPT,
        config.system_root / "projects.yml": PROJECTS_TEMPLATE,
        config.system_root / "schemas.md": SCHEMAS_TEMPLATE,
        config.system_root / "error-taxonomy.md": ERROR_TAXONOMY_TEMPLATE,
        config.system_root / "weekly-review-prompt.md": WEEKLY_REVIEW_PROMPT,
        config.system_root / "personal-operating-manual.md": PERSONAL_OPERATING_MANUAL,
        config.system_root / "workflow-rules.md": WORKFLOW_RULES,
        config.workspace_root / "README-cyberlog.md": README,
        config.workspace_root / CONFIG_FILE_NAME: CONFIG_TEMPLATE,
    }

    for path, content in templates.items():
        existed = path.exists()
        if existed and not args.force:
            status = "skipped"
        else:
            write_text(path, content)
            status = "overwritten" if existed else "created"
        print(f"{status}: {display_path(path, config.workspace_root)}")
    return 0


def today_from_environment() -> dt.date:
    override = os.environ.get("CYBERLOG_TODAY")
    if override:
        return parse_date(override)
    return dt.date.today()


def now_from_environment() -> dt.datetime:
    override = os.environ.get("CYBERLOG_NOW")
    if override:
        normalized = override[:-1] + "+00:00" if override.endswith("Z") else override
        try:
            return dt.datetime.fromisoformat(normalized)
        except ValueError as exc:
            raise CyberlogError(f"Invalid CYBERLOG_NOW '{override}'. Expected ISO datetime.") from exc
    return dt.datetime.now()


def command_today(args: argparse.Namespace, config: Config) -> int:
    day = parse_date(args.date) if args.date else today_from_environment()
    raw_dir = config.daily_raw_root / day.isoformat()
    compiled_dir = config.daily_compiled_root / day.isoformat()
    raw_dir.mkdir(parents=True, exist_ok=True)
    compiled_dir.mkdir(parents=True, exist_ok=True)
    record_run_state_transition(
        day,
        "open",
        "today",
        config,
        updates={
            "raw_dir": display_path(raw_dir, config.workspace_root),
            "compiled_dir": display_path(compiled_dir, config.workspace_root),
        },
    )

    print(f"Raw folder: {display_path(raw_dir, config.workspace_root)}")
    print(f"Compiled folder: {display_path(compiled_dir, config.workspace_root)}")
    previous_day = day - dt.timedelta(days=1)
    previous_boot = (
        config.daily_compiled_root
        / previous_day.isoformat()
        / f"{config.generated_prefix}tomorrow-boot.md"
    )
    if previous_boot.exists() and previous_boot.is_file():
        print(f"Previous boot packet: {display_path(previous_boot, config.workspace_root)}")
        print("")
        content = previous_boot.read_text(encoding="utf-8")
        sys.stdout.write(content)
        if not content.endswith("\n"):
            print()
    else:
        print(f"Previous boot packet not found: {display_path(previous_boot, config.workspace_root)}")
    return 0


def command_capture(args: argparse.Namespace, config: Config) -> int:
    captured = " ".join(args.text)
    if not captured and not sys.stdin.isatty():
        captured = sys.stdin.read()
    if not captured.strip():
        raise CyberlogError("capture requires text arguments or stdin content.")
    if args.type in {"sent", "draft"} and not args.project:
        raise CyberlogError(f"capture --type {args.type} requires --project.")

    timestamp = now_from_environment()
    if args.date:
        day = parse_date(args.date)
    elif os.environ.get("CYBERLOG_TODAY"):
        day = today_from_environment()
    else:
        day = timestamp.date()
    raw_dir = config.daily_raw_root / day.isoformat()
    raw_dir.mkdir(parents=True, exist_ok=True)

    capture_type = args.type or "note"
    stem = f"{timestamp:%H%M}-{capture_type if capture_type != 'note' else 'capture'}"
    output_path = raw_dir / f"{stem}.md"
    suffix = 2
    while output_path.exists():
        output_path = raw_dir / f"{stem}-{suffix}.md"
        suffix += 1

    if not captured.endswith("\n"):
        captured += "\n"
    metadata: dict[str, str] = {}
    if capture_type in STRUCTURED_CAPTURE_TYPES or args.project or args.sent_to or args.subject or args.waiting_for:
        trust = "low" if capture_type == "draft" else "high" if capture_type == "sent" else "medium"
        metadata = {
            "type": capture_type,
            "captured_at": timestamp.isoformat(timespec="seconds"),
            "trust": trust,
        }
        optional = {
            "project": args.project,
            "sent_to": args.sent_to,
            "subject": args.subject,
            "waiting_for": args.waiting_for,
        }
        metadata.update({key: value for key, value in optional.items() if value})
    if metadata:
        front_matter = "\n".join(f"{key}: {value}" for key, value in metadata.items())
        captured = f"---\n{front_matter}\n---\n\n{captured}"
    write_text(output_path, captured)
    print(f"Wrote {display_path(output_path, config.workspace_root)}")
    return 0
