#!/usr/bin/env python3
"""Daily Cyberlog / AI Sync helper for a personal daily workspace.

This script intentionally uses only the Python standard library. It never
modifies non-generated markdown notes during feed generation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


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
    # Default is "end" to match the example: 2026-05-01..2026-05-07 -> 2026-W19.
    # Set to "start" in cyberlog.config.json if you want strict start-date labeling.
    "weekly_week_basis": "end",
}

CONFIG_FILE_NAME = "cyberlog.config.json"

AI_SYNC_PROMPT = """# Daily Cyberlog / 工作画布 AI Sync Prompt

你是我的 cyberlog 整理 agent 和工作流分析 agent。

下面是我今天 Obsidian Daily 文件夹里的所有 markdown 内容。
这些内容是原始草稿，可能混乱、重复、不完整。

你的任务不是做普通总结，而是从中提取我的工作状态、任务流、决策、阻塞、产出和自我迭代信号。

请严格区分：
- 明确事实
- 合理推断
- 建议
- 不确定信息

不要编造。找不到就写“未发现”。

在正式输出前，请先在内部完成一次信息清洗，但不要展开这部分过程：
1. 按项目聚类：例如 A38 / A57 / cyberlog-workflow / workspace-skills / wiki-sync / 其他。
2. 给每条信息标记类型：fact / draft / sent-message / ai-suggestion / decision / todo / blocked / closed。
3. `chatroom`、`未命名`、历史 AI 回答、方案建议类内容，默认只能作为 `ai-suggestion` 或 `合理推断`，不能直接当作事实；只有原文明确出现“已完成 / 已发送 / 已确认 / 等待反馈 / 实测 / 核实”等状态词时，才可升级为事实。
4. 同一文件里如果同时出现“未发送版本”和“最终发送版本”，必须分别标记，不能合并成一个已发送事实。
5. 如果一个任务跨多个项目出现，请优先归入最具体项目，不要重复计算推进。

请输出以下结构：

# FILE: _cyberlog.md

# Cyberlog — {{date}}

## 1. 今日真实推进

列出今天真正产生推进的事项，而不是所有活动。

## 2. 当前工作画布

### Active

当前正在推进的任务。

### Queue

排队但未真正开始的任务。

### Blocked

被阻塞的任务。每个阻塞需要说明：
- 阻塞原因
- 解除方式
- owner
- 下一步

### Closed

今天已经关闭或完成的事项。

## 3. 关键决策

用表格输出：

| 决策 | 背景 | 理由 | 风险 | 后续动作 | 来源文件 |
|---|---|---|---|---|---|

## 4. 重要信息

提取今天记录中值得保留的信息、链接、材料、观点或上下文。
不要把所有信息都搬运过来，只保留未来仍有用的信息。

## 5. 今日产出

列出今天产生的可复用产出，例如：
- 文档
- 代码
- prompt
- 模板
- 设计
- 判断
- 结论
- 决策资产

每个产出需要说明：
- 产出是什么
- 属于哪个项目
- 位置或来源
- 可复用价值

## 6. 未完成任务

只列出仍然需要行动的事项。
每个任务给出：
- 任务
- 所属项目
- 下一步动作
- 优先级：P0 / P1 / P2
- 是否适合交给 AI / agent
- 为什么

## 7. 明日启动包

输出明天早上可以直接使用的启动信息：

# FILE: _tomorrow-boot.md

# Tomorrow Boot Packet — {{next_date}}

## 明日主线
-

## 背景
-

## 当前状态
-

## 第一动作
-

## 注意事项
-

## 不要重复踩的坑
-

## 可以交给 AI / agent 的部分
-

## 必须由我亲自判断的部分
-

## 8. 工作流摩擦

分析今天工作流中出现的摩擦，例如：
- 目标不清
- 上下文切换
- 工具链问题
- 决策拖延
- 范围膨胀
- 信息分散
- 执行中断
- 任务入口不清
- 缺少完成标准

每个摩擦请说明：
- 现象
- 可能原因
- 对推进的影响
- 明天的修正动作

## 9. 自我迭代建议

只给 1-3 条最有价值的建议。
每条建议必须能转化为明天或本周的具体行为。
不要给泛泛建议。

## 10. 规则候选

提取今天应该沉淀进 personal operating manual 的规则。
格式：

### 规则候选 N
- 触发条件：
- 规则：
- 原因：
- 例子：
- 是否建议写入 System/workflow-rules.md：yes / no

输出要求：
- 不要编造事实。
- 不确定就标记为“不确定”。
- 尽量引用来源文件名。
- 原始内容里没有的信息不要假装存在。
- 严格保留 `# FILE: _cyberlog.md` 和 `# FILE: _tomorrow-boot.md` 两个分隔标题，方便拆分保存。
- 输出要适合直接复制到 _cyberlog.md 和 _tomorrow-boot.md。
"""

WEEKLY_REVIEW_PROMPT = """# Weekly Workflow Review Prompt

你是我的 weekly workflow review agent。

下面是我这一周每天的 _cyberlog.md 和 _tomorrow-boot.md。
请分析我的工作流，而不是总结流水账。

请输出：

# Weekly Workflow Review — {{start_date}} to {{end_date}}

## 1. 本周真正推进的主线

不要按日期流水账总结，而是按项目和成果总结。

## 2. 本周主要产出

列出可复用产出，并说明它们的长期价值。

## 3. 重复出现的阻塞

找出重复出现的 blocker、friction、context switch、unclear goal、tool-chain issue。

## 4. 最大上下文切换来源

分析哪些项目、任务、工具或外部事件造成切换成本。

## 5. 高价值任务 vs 低价值消耗

把本周活动分成：
- high leverage
- maintenance
- distraction
- blocked
- learning
- reusable asset

## 6. 适合交给 AI / agent 的任务

列出任务类型，并说明为什么适合。

## 7. 必须由我亲自判断的任务

列出任务类型，并说明原因。

## 8. 工作流规则候选

输出应该写入 System/workflow-rules.md 的规则。

格式：
- 触发条件：
- 规则：
- 原因：
- 本周证据：
- 建议优先级：

## 9. 下周只做一个自我迭代实验

必须是一个最小实验，而不是大计划。
格式：
- 实验：
- 触发条件：
- 执行动作：
- 成功标准：
- 失败信号：
- 复查时间：

## 10. 下周默认工作画布

输出下周可以直接放进 Obsidian 的默认工作画布结构。
"""

PERSONAL_OPERATING_MANUAL = """# Personal Operating Manual

这个 manual 记录稳定有效的个人工作流规则。它不是日记，也不是任务清单；只沉淀能重复使用的操作方式。

## 我如何启动一天

1. 把今天的原始文件放入 `Daily/raw/YYYY-MM-DD/`。
2. 如需模板，可从 `Daily/templates/` 复制到当天 raw 目录后再写。
2. 写下今日主线：今天最希望推进的 1-3 件事。
3. 写下今日不做：明确排除会制造上下文切换的事项。
4. 从昨天的 `_tomorrow-boot.md` 拿第一动作，直接进入执行。

## 我如何关闭一天

1. 保留所有原始 notes，不重写、不清理事实轨迹。
2. 运行 `python tools/cyberlog.py daily --date YYYY-MM-DD` 生成 `_ai-request.md`。
3. 把 `_ai-request.md` 投喂给 AI。
4. 将 AI 输出拆分保存到当天目录的 `_cyberlog.md` 和 `_tomorrow-boot.md`。
5. 把明确值得复用的规则候选手动写入 `System/workflow-rules.md`。

## 我如何处理阻塞

阻塞必须写清楚四件事：原因、解除方式、owner、下一步。

如果同类阻塞重复出现，不再只写复盘结论，而是沉淀为规则、模板、checklist 或脚本。

## 我如何把任务交给 AI / agent

适合交给 AI / agent 的任务通常具备：
- 输入材料清楚。
- 完成标准可以描述。
- 判断风险低，或可以由我最后审核。
- 输出可以被复制、修改或丢弃。

不适合直接交给 AI / agent 的任务通常包括：
- 需要个人偏好或战略取舍的判断。
- 事实来源不足但后果较大的决策。
- 会影响真实资产、账号、生产系统或他人承诺的动作。

## 我如何判断任务是否完成

一个任务完成至少要满足：
- 产出已经落到明确位置。
- 下一步不存在，或已经写入后续任务。
- 风险、阻塞、未决问题已经显式记录。
- 未来恢复上下文不需要重新推理整段过程。

## 我如何做周复盘

1. 确保每天都有 `_cyberlog.md` 和 `_tomorrow-boot.md`，缺失可以接受但要知道缺口。
2. 运行 `python tools/cyberlog.py weekly --start YYYY-MM-DD --end YYYY-MM-DD`。
3. 把生成的 weekly request 投喂给 AI。
4. 只提取能改变下周行为的结论，不保存流水账总结。

## 我如何沉淀规则

规则必须包含触发条件、执行动作、原因和证据。

只有当规则能减少未来摩擦、降低上下文恢复成本、改善决策质量或减少重复劳动时，才写入 `System/workflow-rules.md`。
"""

WORKFLOW_RULES = """# Workflow Rules

## Rule 1: 原始 notes 永不覆盖

触发条件：任何 AI 整理、同步、压缩、改写动作。
规则：AI 只能生成下划线开头的新文件，不能覆盖原始 notes。
原因：保留真实工作轨迹，避免 AI 误写污染事实。

## Rule 2: 只记录影响系统状态的事件

触发条件：白天记录 event stream。
规则：优先记录决策、阻塞、产出、上下文切换、重要信息、下一步。
原因：cyberlog 的目标不是流水账，而是可分析的工作流遥测。

## Rule 3: 每天必须生成明日启动包

触发条件：当天结束前。
规则：生成 _tomorrow-boot.md 或至少在 _cyberlog.md 中保留 Tomorrow Boot Packet。
原因：降低第二天恢复上下文的成本。

## Rule 4: 重复 3 次的阻塞必须转成规则、模板或脚本

触发条件：同类 blocker/friction 在一周内重复出现。
规则：不要只复盘，要把它沉淀为 workflow rule、template、checklist 或 automation。
原因：自我迭代必须改变系统，而不是只改变意愿。
"""

README = """# Daily Cyberlog / 工作画布 AI Sync 系统

这个系统把 Obsidian Daily 文件夹里的原始 markdown 合并成 AI 投喂包，并生成固定 prompt。它的目标不是改变白天的记录习惯，而是在一天结束时把工作画布、事件流、决策、阻塞、任务和自我迭代信号整理成可复用资产。

## 文件结构

```text
my-daily/
  Daily/
    raw/
      2026-05-07/
        04-imported.md
    compiled/
      2026-05-07/
        _ai-feed.md
        _ai-request.md
        _cyberlog.md
        _tomorrow-boot.md
    templates/
        00-canvas.md
        01-notes.md
        02-research.md
        03-agent.md
  Reviews/
    weekly/
      2026-W19_ai-weekly-request.md
  System/
    ai-sync-prompt.md
    weekly-review-prompt.md
    personal-operating-manual.md
    workflow-rules.md
  tools/
    cyberlog.py
  cyberlog.config.json
  README-cyberlog.md
```

## 核心原则

- 原始 notes 永不覆盖。
- AI 生成内容和原始内容分开。
- 所有 AI 生成文件使用 `_` 开头。
- 生成 daily feed 时会排除 `_` 开头的 markdown，避免把 AI 输出再次喂回去。
- 当前系统只生成 feed、request、模板和命令，不直接调用 OpenAI API。

## 初始化

在 my-daily 根目录运行：

```bash
python tools/cyberlog.py init
```

该命令会创建必要目录和模板文件。已有模板默认不会覆盖。需要重置模板时运行：

```bash
python tools/cyberlog.py init --force
```

## 每天怎么用

早上或开始工作前创建今天的 Daily 工作画布：

```bash
python tools/cyberlog.py today
```

它会创建：

- `Daily/raw/YYYY-MM-DD/`
- `Daily/compiled/YYYY-MM-DD/`

`today` 不会往当天 raw 目录写入任何模板文件，避免污染原始输入区。

白天继续按原来的习惯自由写 markdown。建议分两类放：

- `Daily/raw/YYYY-MM-DD/`：当天原始输入文件，只放你写入或导入的原始 markdown。
- `Daily/templates/`：可复制模板，不参与 daily 合并。

你可以新增任意非 `_` 开头的 `.md` 文件，例如 `04-meeting.md`、`05-debug.md`、`06-idea.md`。

晚上生成 AI request：

```bash
python tools/cyberlog.py daily --date 2026-05-07
```

它会生成：

- `Daily/compiled/2026-05-07/_ai-feed.md`
- `Daily/compiled/2026-05-07/_ai-request.md`
- `Daily/compiled/2026-05-07/_ai-audit.md`

## 如何把 `_ai-request.md` 喂给 AI

打开当天的 `_ai-request.md`，复制全部内容，粘贴给 AI。AI 输出后建议保存为：

- `Daily/compiled/YYYY-MM-DD/_cyberlog.md`
- `Daily/compiled/YYYY-MM-DD/_tomorrow-boot.md`

如果 AI 把两个部分放在同一个回答里，你可以手动拆分。`_cyberlog.md` 保存完整日终整理，`_tomorrow-boot.md` 只保存明天启动包。

## 每周怎么用

周复盘只读取每天已经整理后的 `_cyberlog.md` 和 `_tomorrow-boot.md`，不会读取原始 daily notes。

```bash
python tools/cyberlog.py weekly --start 2026-05-01 --end 2026-05-07
```

它会生成类似：

```text
Reviews/weekly/2026-W19_ai-weekly-request.md
```

缺失的 `_cyberlog.md` 或 `_tomorrow-boot.md` 会作为 warning 写入 request，不会导致命令失败。

## 为什么不要覆盖原始 notes

原始 notes 是真实工作轨迹。它们保留了当时的混乱、上下文、误判、阻塞和决策过程。AI 输出是整理层，只能生成 `_` 开头的文件。如果让 AI 覆盖原始 notes，会污染事实来源，也会让后续分析无法判断哪些内容是真实记录、哪些是模型重写。

## 配置

默认配置在 `cyberlog.config.json`：

```json
{
  "daily_root": "Daily",
  "daily_raw_root": "Daily/raw",
  "daily_compiled_root": "Daily/compiled",
  "daily_templates_root": "Daily/templates",
  "system_root": "System",
  "reviews_root": "Reviews/weekly",
  "generated_prefix": "_",
  "daily_exclude_dirs": ["chatroom"],
  "timezone": "local",
  "weekly_week_basis": "end"
}
```

常见修改：

- Daily 文件夹不叫 `Daily`：修改 `daily_root`。
- 原始输入区不叫 `Daily/raw`：修改 `daily_raw_root`。
- 编译输出区不叫 `Daily/compiled`：修改 `daily_compiled_root`。
- 模板区不叫 `Daily/templates`：修改 `daily_templates_root`。
- System 文件夹不叫 `System`：修改 `system_root`。
- 周复盘输出目录不叫 `Reviews/weekly`：修改 `reviews_root`。
- 生成文件前缀不想用 `_`：修改 `generated_prefix`。
- 不想把讨论草稿目录喂给 AI：修改 `daily_exclude_dirs`，默认排除 `chatroom`。

`today` 当前使用本机本地日期。`timezone` 字段暂时只是配置记录，脚本不会强制切换时区。

`weekly_week_basis` 默认是 `end`，因此 `2026-05-01` 到 `2026-05-07` 会生成 `2026-W19_ai-weekly-request.md`。如果你希望严格按 start 日期计算周号，可以改成 `start`。

## 命令速查

```bash
python tools/cyberlog.py init
python tools/cyberlog.py today
python tools/cyberlog.py daily --date 2026-05-07
python tools/cyberlog.py weekly --start 2026-05-01 --end 2026-05-07
```

如果你不在 my-daily 根目录运行，可以指定 root：

```bash
python /path/to/my-daily/tools/cyberlog.py --root /path/to/my-daily daily --date 2026-05-07
```

## 手动测试步骤

1. 运行 `python tools/cyberlog.py init`，确认模板创建。
2. 修改一个模板文件，再运行 `python tools/cyberlog.py init`，确认不会覆盖。
3. 运行 `python tools/cyberlog.py today`，确认今天的 Daily 文件夹和默认文件存在。
4. 在 `Daily/raw/YYYY-MM-DD/` 目录写入一个原始文件，并在 `Daily/compiled/YYYY-MM-DD/` 写入 `_cyberlog.md`，运行 `daily`，确认 `_ai-feed.md` 只包含 raw 中非 `_` 开头文件，且默认排除 `chatroom/`。
5. 检查 `_ai-feed.md` 中是否有 `<file path=\"...\">` 文件边界。
6. 检查 `_ai-audit.md` 中的 included/excluded 文件清单和 prompt/request 检查。
7. 准备几天的 `_cyberlog.md` 和 `_tomorrow-boot.md`，运行 `weekly`，确认会收集存在的文件。
8. 删除某天的 `_tomorrow-boot.md` 后再运行 `weekly`，确认输出 warning 而不是失败。

也可以运行内置测试：

```bash
python tools/test_cyberlog.py
```

## 常见问题

### daily 提示 Daily 日期文件夹不存在

先运行 `python tools/cyberlog.py today` 创建今天目录，或手动创建 `Daily/raw/YYYY-MM-DD/`。

### daily 提示没有可合并的原始 md 文件

当天目录里只有 `_` 开头的生成文件，或没有 `.md` 文件。新增至少一个非 `_` 开头的 markdown。

### weekly 为什么不读取原始 notes

周复盘分析的是已经整理后的工作流状态，不应该重新吸入原始草稿。这样可以降低噪音，也避免把 AI 输出和原始内容混在同一层。

### AI 输出要不要自动写回文件

当前版本不自动调用 API，也不自动解析 AI 输出。建议先手动保存，保证你能审核内容质量。
"""

CONFIG_TEMPLATE = """{
  "daily_root": "Daily",
  "daily_raw_root": "Daily/raw",
  "daily_compiled_root": "Daily/compiled",
  "daily_templates_root": "Daily/templates",
  "system_root": "System",
  "reviews_root": "Reviews/weekly",
  "generated_prefix": "_",
  "daily_exclude_dirs": ["chatroom"],
  "timezone": "local",
  "weekly_week_basis": "end"
}
"""

CANVAS_TEMPLATE = """# Daily Canvas - {date}

## 今日主线

-

## 今日不做

-

## 当前任务

-

## Event Stream

-

## Decisions

-

## Blockers

-

## Outputs

-

## Next Actions

-
"""


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
    weekly_week_basis: str


def parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise CyberlogError(f"Invalid date '{value}'. Expected YYYY-MM-DD.") from exc


def default_workspace_root() -> Path:
    return Path(__file__).resolve().parents[1]


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
            "Run `python tools/cyberlog.py init` first."
        )
    return path.read_text(encoding="utf-8")


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


def markdown_files_for_daily(raw_dir: Path, config: Config) -> list[Path]:
    included, _ = daily_source_files(raw_dir, config)
    return included


def file_block(path: Path, config: Config) -> str:
    rel_path = html.escape(display_path(path, config.workspace_root), quote=True)
    content = path.read_text(encoding="utf-8")
    if not content.endswith("\n"):
        content += "\n"
    return f'<file path="{rel_path}">\n{content}</file>\n'


def join_blocks(paths: Iterable[Path], config: Config) -> str:
    return "\n".join(file_block(path, config).rstrip("\n") for path in paths) + "\n"


def build_daily_request(day: dt.date, prompt: str, feed: str) -> str:
    next_day = day + dt.timedelta(days=1)
    rendered_prompt = render_template(
        prompt,
        {
            "date": day.isoformat(),
            "next_date": next_day.isoformat(),
        },
    )
    return f"""# AI Sync Request - {day.isoformat()}

## 使用说明

复制本文件全部内容，粘贴给 AI。

AI 输出后建议保存为：
- `Daily/compiled/{day.isoformat()}/_cyberlog.md`
- `Daily/compiled/{day.isoformat()}/_tomorrow-boot.md`

请先审核 AI 输出，不要让 AI 覆盖任何非下划线开头的原始 notes。

## Prompt

{rendered_prompt.rstrip()}

## AI Feed

{feed.rstrip()}
"""


def status_line(label: str, ok: bool) -> str:
    return f"- [{'ok' if ok else 'warn'}] {label}"


def build_daily_audit(
    day: dt.date,
    source_files: list[Path],
    excluded_files: list[tuple[Path, str]],
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
    prompt_checks = "\n".join(
        (
            status_line("prompt contains project clustering guard", "按项目聚类" in prompt),
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
            status_line(
                "request excludes configured daily directories",
                not any(excluded_daily_dir(path, config.daily_raw_root / day.isoformat(), config.daily_exclude_dirs) for path in source_files),
            ),
        )
    )
    risk_section = "\n".join(risk_hits) if risk_hits else "- 未发现"

    return f"""# AI Request Audit - {day.isoformat()}

## Summary

- Included source files: {len(source_files)}
- Excluded markdown files: {len(excluded_files)}
- Configured excluded directories: {', '.join(config.daily_exclude_dirs) if config.daily_exclude_dirs else '未配置'}

## Included Source Files

{included_paths if included_paths else '- 未发现'}

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
            "Create it first or run `python tools/cyberlog.py today` for today's folder."
        )

    source_files, excluded_files = daily_source_files(raw_dir, config)
    if not source_files:
        raise CyberlogError(
            f"No raw markdown files found in {display_path(raw_dir, config.workspace_root)}. "
            f"Files starting with '{config.generated_prefix}' are intentionally excluded."
        )

    feed = join_blocks(source_files, config)
    prompt = read_required_prompt(config.system_root / "ai-sync-prompt.md", config)
    request = build_daily_request(day, prompt, feed)
    audit = build_daily_audit(day, source_files, excluded_files, prompt, request, config)

    feed_path = compiled_dir / f"{config.generated_prefix}ai-feed.md"
    request_path = compiled_dir / f"{config.generated_prefix}ai-request.md"
    audit_path = compiled_dir / f"{config.generated_prefix}ai-audit.md"
    write_text(feed_path, feed)
    write_text(request_path, request)
    write_text(audit_path, audit)

    print(f"Wrote {display_path(feed_path, config.workspace_root)}")
    print(f"Wrote {display_path(request_path, config.workspace_root)}")
    print(f"Wrote {display_path(audit_path, config.workspace_root)}")
    print(f"Merged {len(source_files)} raw markdown file(s).")
    if excluded_files:
        print(f"Excluded {len(excluded_files)} markdown file(s).")
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

周复盘只使用每天的 `_cyberlog.md` 和 `_tomorrow-boot.md`，不读取原始 daily notes。

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


def command_today(args: argparse.Namespace, config: Config) -> int:
    day = today_from_environment()
    raw_dir = config.daily_raw_root / day.isoformat()
    compiled_dir = config.daily_compiled_root / day.isoformat()
    raw_dir.mkdir(parents=True, exist_ok=True)
    compiled_dir.mkdir(parents=True, exist_ok=True)

    print(f"Raw folder: {display_path(raw_dir, config.workspace_root)}")
    print(f"Compiled folder: {display_path(compiled_dir, config.workspace_root)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Daily Cyberlog / AI Sync helper for Obsidian.")
    parser.add_argument(
        "--root",
        help="Workspace root. Defaults to the parent directory of this script.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    daily = subparsers.add_parser("daily", help="Build daily _ai-feed.md and _ai-request.md.")
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
    today.set_defaults(func=command_today)

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


if __name__ == "__main__":
    raise SystemExit(main())
