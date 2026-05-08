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
    "raw_retention_days": 7,
    # Default is "end" to match the example: 2026-05-01..2026-05-07 -> 2026-W19.
    # Set to "start" in cyberlog.config.json if you want strict start-date labeling.
    "weekly_week_basis": "end",
}

CONFIG_FILE_NAME = "cyberlog.config.json"

AI_SYNC_PROMPT = """# Daily Cyberlog / 工作画布 AI Sync Prompt

你是我的 cyberlog 整理 agent 和工作流分析 agent。

下面的 request 通常包含两类输入：

- `AI Feed`：今天 `Daily/raw/YYYY-MM-DD/` 中进入合并的 markdown。它是今天的主要事实输入。
- `Historical Context`：昨天的 `_cyberlog.md` 和最近几天的 `_tomorrow-boot.md`。它只能用于识别连续性、重复 blocker 和昨天计划，不能当作今天发生过的事实。

raw 是临时事实输入层，不是永久记录层。daily 完整生成并人工审核后，raw 可能在 7 天后清理；不要因为 raw 未来可清理，就降低今天的事实/推断边界要求。

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
6. 如果某条信息只出现在 `Historical Context`，只能写成延续背景或待确认，不要写成“今日真实推进”。
7. 引用来源时尽量保留文件名或路径；这些路径用于审核，不代表 raw 会永久存在。

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
- 尽量引用来源文件名或路径；如果来源来自 Historical Context，要明确标注为历史上下文。
- 原始内容里没有的信息不要假装存在。
- 严格保留 `# FILE: _cyberlog.md` 和 `# FILE: _tomorrow-boot.md` 两个分隔标题，方便拆分保存。
- 输出要适合直接复制到 _cyberlog.md 和 _tomorrow-boot.md。
"""

WEEKLY_REVIEW_PROMPT = """# Weekly Workflow Review Prompt

你是我的 weekly workflow review agent。

下面是我这一周每天的 _cyberlog.md 和 _tomorrow-boot.md。
请分析我的工作流，而不是总结流水账。

边界规则：
- 周复盘只使用已经审核过的 compiled 输出，不回读 raw。
- raw 是临时事实输入层，可能已经按保留期清理；不要把 raw 缺失当成记录不完整。
- `_ai-feed.md` 和 `_ai-request.md` 是生成中间件，不是周复盘的长期事实来源。
- 如果某天缺少 `_cyberlog.md` 或 `_tomorrow-boot.md`，把它作为记录缺口，不要自行从其他来源补事实。

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
3. 写下今日主线：今天最希望推进的 1-3 件事。
4. 从昨天的 `_tomorrow-boot.md` 拿第一动作，直接进入执行。

## 我如何判断 daily 边界

这个 repo 只作为 daily 内容维护和 AI 整理的底层数据，不作为真实工作空间。

可以进入 daily 的内容：
- 工作状态、事实摘要、决策、阻塞、下一步。
- 已发送/待发送沟通的状态标记和脱敏摘要。
- 外部资料的位置或引用线索。

不进入 daily 的内容：
- 原厂邮件全文、报价、联系人、NDA 或商务条款。
- 正式设计源文件、项目交付物、采购证据、需要受控归档的原始材料。
- 会因为进入 `_ai-feed.md`、`_ai-request.md`、`_cyberlog.md` 或 weekly review 而产生扩散风险的内容。

## 我如何关闭一天

1. 保留当天 raw，不重写、不覆盖事实输入。
2. 运行 `python3 tools/cyberlog.py daily --date YYYY-MM-DD` 生成 `_ai-request.md` 和 `_ai-context.md`。
3. 默认让 Codex/agent 完整处理 `_ai-request.md`，并保存 `_cyberlog.md`、`_tomorrow-boot.md`、`_ai-output-audit.md`。
4. 审核 `_ai-audit.md` 和 `_ai-output-audit.md`，确认没有混入被排除目录、没有把草稿或推断升级成事实。
5. 把明确值得复用的规则候选手动写入 `System/workflow-rules.md`。
6. raw 只作为临时事实输入层。daily 完整生成并人工审核后，7 天后可以运行 `python3 tools/cyberlog.py prune-raw --older-than 7 --apply` 清理，只保留 compiled 和 `_raw-discard-log.md`。

当天关闭完成标准：
- `_ai-feed.md`
- `_ai-context.md`
- `_ai-request.md`
- `_ai-audit.md`
- `_cyberlog.md`
- `_tomorrow-boot.md`
- `_ai-output-audit.md`

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

对 daily cyberlog 来说，只生成 `_ai-request.md` 不算完成；必须生成并审核 `_cyberlog.md`、`_tomorrow-boot.md` 和 `_ai-output-audit.md`。

## 我如何做周复盘

1. 确保每天都有 `_cyberlog.md` 和 `_tomorrow-boot.md`，缺失可以接受但要知道缺口。
2. 运行 `python3 tools/cyberlog.py weekly --start YYYY-MM-DD --end YYYY-MM-DD`。
3. 把生成的 weekly request 投喂给 AI。
4. 只提取能改变下周行为的结论，不保存流水账总结。

## 我如何沉淀规则

规则必须包含触发条件、执行动作、原因和证据。

只有当规则能减少未来摩擦、降低上下文恢复成本、改善决策质量或减少重复劳动时，才写入 `System/workflow-rules.md`。
"""

WORKFLOW_RULES = """# Workflow Rules

## Rule 1: 原始 notes 在保留期内不可覆盖

触发条件：任何 AI 整理、同步、压缩、改写动作。
规则：AI 只能生成下划线开头的新文件，不能覆盖原始 notes。raw 是临时事实输入层，不是永久记录层；daily 完整生成并人工审核后，raw 可在 7 天后删除。
原因：保留短期纠错所需的真实工作轨迹，同时避免 repo 长期堆积低价值原始碎片。

## Rule 2: 只记录影响系统状态的事件

触发条件：白天记录 event stream。
规则：优先记录决策、阻塞、产出、上下文切换、重要信息、下一步。
原因：cyberlog 的目标不是流水账，而是可分析的工作流遥测。

## Rule 3: 每天必须生成明日启动包

触发条件：当天结束前。
规则：生成 _tomorrow-boot.md 或至少在 _cyberlog.md 中保留 Tomorrow Boot Packet。
原因：降低第二天恢复上下文的成本。

## Rule 4: Daily AI request 默认完整处理

触发条件：用户要求处理 daily、cyberlog、_ai-request.md，或当天结束流程。
规则：不要停在 _ai-request.md。默认生成 _cyberlog.md、_tomorrow-boot.md 和 _ai-output-audit.md；如果有写入权限，直接保存到 Daily/compiled/YYYY-MM-DD/。
原因：_ai-request.md 只是任务包，不是用户最终要看的整理结果。完整处理才能降低查看和恢复上下文成本。

## Rule 5: 重复 3 次的阻塞必须转成规则、模板或脚本

触发条件：同类 blocker/friction 在一周内重复出现。
规则：不要只复盘，要把它沉淀为 workflow rule、template、checklist 或 automation。
原因：自我迭代必须改变系统，而不是只改变意愿。

## Rule 6: Daily repo 只做底层记录，不做工作空间

触发条件：记录项目资料、采购反馈、设计证据、供应商邮件、外部协作材料时。
规则：本 repo 只维护 daily 内容和 AI 整理所需的底层数据；只记录状态、结论摘要、阻塞、下一步和外部资料位置，不保存原始工作资产。
原因：daily cyberlog 的价值是恢复上下文和分析工作流。如果把正式项目资料、采购证据、邮件全文、报价、设计源文件放进来，会污染 raw/compiled 管线，并让 AI feed、weekly review 和 Git 历史反复扩散不该扩散的信息。

## Rule 7: raw 清理必须留下 discard log

触发条件：清理 `Daily/raw/YYYY-MM-DD/`。
规则：只清理已经完整生成并人工审核的日期目录；删除前默认 dry-run，实际删除必须写入 `Daily/compiled/YYYY-MM-DD/_raw-discard-log.md`，记录文件名、大小和 hash。
原因：raw 不再永久保存，但清理行为本身要可解释，未来能知道当时丢弃了哪些输入。
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
        _ai-context.md
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

- raw 在保留期内不覆盖，完整整理并审核 7 天后可清理。
- AI 生成内容和原始内容分开。
- 所有 AI 生成文件使用 `_` 开头。
- 生成 daily feed 时会排除 `_` 开头的 markdown，避免把 AI 输出再次喂回去。
- 当前系统不直接调用 OpenAI API，但 Codex/agent 看到 `_ai-request.md` 时默认应完整处理并落盘结果。
- 本仓库只作为 daily 内容维护和 AI 整理的底层数据，不作为项目工作空间、采购资料库、设计证据库或正式交付资料库。

## 初始化

在 my-daily 根目录运行：

```bash
python3 tools/cyberlog.py init
```

该命令会创建必要目录和模板文件。已有模板默认不会覆盖。需要重置模板时运行：

```bash
python3 tools/cyberlog.py init --force
```

## 每天怎么用

早上或开始工作前创建今天的 Daily 工作画布：

```bash
python3 tools/cyberlog.py today
```

它会创建：

- `Daily/raw/YYYY-MM-DD/`
- `Daily/compiled/YYYY-MM-DD/`

`today` 不会往当天 raw 目录写入任何模板文件，避免污染原始输入区。

如果昨天存在 `Daily/compiled/<昨天>/_tomorrow-boot.md`，`today` 会直接打印这份启动包，但不会复制到当天 raw 目录。这样昨天的 AI 输出只作为晨间启动提示，不会混入今天的原始事实来源。

白天继续按原来的习惯自由写 markdown。建议分两类放：

- `Daily/raw/YYYY-MM-DD/`：当天原始输入文件，只放你写入或导入的原始 markdown。
- `Daily/templates/`：可复制模板，不参与 daily 合并。

你可以新增任意非 `_` 开头的 `.md` 文件，例如 `04-meeting.md`、`05-debug.md`、`06-idea.md`。

也可以用 `capture` 快速记录一条 raw note：

```bash
python3 tools/cyberlog.py capture "跟进 A38 LPDDR5 供应商正式回复"
printf "会议结论..." | python3 tools/cyberlog.py capture
```

`capture` 会写入 `Daily/raw/YYYY-MM-DD/HHMM-capture.md`。如果同一分钟已经存在文件，会自动使用 `HHMM-capture-2.md`，不会覆盖已有 raw note。

`Daily/raw/` 适合保存工作状态、事实摘要、决策、阻塞、下一步和外部资料位置。不适合保存原厂邮件全文、报价、联系人、NDA/商务条款、正式设计源文件、项目交付物或需要长期受控归档的证据材料。这些内容应放在对应的邮箱、采购系统、项目资料库或受控工作空间；daily 中只保留可用于恢复上下文的脱敏摘要。

晚上生成 AI request：

```bash
python3 tools/cyberlog.py daily --date 2026-05-07
```

它会生成：

- `Daily/compiled/2026-05-07/_ai-feed.md`
- `Daily/compiled/2026-05-07/_ai-context.md`
- `Daily/compiled/2026-05-07/_ai-request.md`
- `Daily/compiled/2026-05-07/_ai-audit.md`

`_ai-feed.md` 只包含当天 raw 目录中非 `_` 开头的 markdown。`_ai-context.md` 单独保存跨日上下文：昨天的 `_cyberlog.md` 和最近 3 天的 `_tomorrow-boot.md`。这些内容只用于识别连续任务和重复 blocker，不作为今天的 raw evidence。

## 默认完整处理

`_ai-request.md` 是给 AI 的任务包，不是整理结果。默认完成标准不是“生成 request”，而是当天目录里同时存在：

- `_ai-feed.md`
- `_ai-context.md`
- `_ai-request.md`
- `_ai-audit.md`
- `_cyberlog.md`
- `_tomorrow-boot.md`
- `_ai-output-audit.md`

你可以用两种方式触发完整处理：

1. 在聊天窗口里打开当天的 `_ai-request.md`，复制全部内容，粘贴给 AI。
2. 在 Codex 工作区里直接说：`处理 Daily/compiled/YYYY-MM-DD/_ai-request.md，并保存 _cyberlog.md 和 _tomorrow-boot.md`。

如果 AI/Codex 有文件写入能力，它应该直接保存：

- `Daily/compiled/YYYY-MM-DD/_cyberlog.md`
- `Daily/compiled/YYYY-MM-DD/_tomorrow-boot.md`
- `Daily/compiled/YYYY-MM-DD/_ai-output-audit.md`

只有在 AI 没有文件写入能力时，才把结果完整输出到聊天窗口，由你手动保存。`_cyberlog.md` 保存完整日终整理，`_tomorrow-boot.md` 只保存明天启动包。

当前脚本不自动调用 AI API。这样可以避免 API key、费用、模型选择和自动覆盖结果的问题。`_ai-audit.md` 用来先审核任务包边界，真正的 AI 输出仍应在保存前过一遍人工检查。

`_ai-output-audit.md` 用于记录 AI 输出是否误读草稿状态、是否混入被排除目录、是否把推断升级成事实。

## 每周怎么用

周复盘只读取每天已经整理后的 `_cyberlog.md` 和 `_tomorrow-boot.md`，不会读取原始 daily notes。

```bash
python3 tools/cyberlog.py weekly --start 2026-05-01 --end 2026-05-07
```

它会生成类似：

```text
Reviews/weekly/2026-W19_ai-weekly-request.md
```

缺失的 `_cyberlog.md` 或 `_tomorrow-boot.md` 会作为 warning 写入 request，不会导致命令失败。

## 为什么 raw 可清理但不能覆盖

raw 是真实工作轨迹的短期输入层。它保留当时的混乱、上下文、误判、阻塞和决策过程，方便当天整理和短期纠错。AI 输出是整理层，只能生成 `_` 开头的文件，不能覆盖 raw。daily 完整生成并人工审核后，raw 不再作为永久记录；7 天后可以清理，只保留 compiled 和 `_raw-discard-log.md`。

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
  "raw_retention_days": 7,
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
- raw 想保留更久或更短：修改 `raw_retention_days`。

`today` 和 `capture` 当前使用本机本地日期。需要指定日期时可以使用 `--date YYYY-MM-DD`。`timezone` 字段暂时只是配置记录，脚本不会强制切换时区。

`raw_retention_days` 默认是 `7`。raw 是临时事实输入层，不是永久记录层。当天完整生成并人工审核后，raw 可以在保留期之后用 `prune-raw` 清理；系统会在 compiled 目录保留 `_raw-discard-log.md`。

`weekly_week_basis` 默认是 `end`，因此 `2026-05-01` 到 `2026-05-07` 会生成 `2026-W19_ai-weekly-request.md`。如果你希望严格按 start 日期计算周号，可以改成 `start`。

## 命令速查

```bash
python3 tools/cyberlog.py init
python3 tools/cyberlog.py today
python3 tools/cyberlog.py capture "quick note"
python3 tools/cyberlog.py daily --date 2026-05-07
python3 tools/cyberlog.py prune-raw --older-than 7
python3 tools/cyberlog.py prune-raw --older-than 7 --apply
python3 tools/cyberlog.py weekly --start 2026-05-01 --end 2026-05-07
```

如果你不在 my-daily 根目录运行，可以指定 root：

```bash
python3 /path/to/my-daily/tools/cyberlog.py --root /path/to/my-daily daily --date 2026-05-07
```

## 手动测试步骤

1. 运行 `python3 tools/cyberlog.py init`，确认模板创建。
2. 修改一个模板文件，再运行 `python3 tools/cyberlog.py init`，确认不会覆盖。
3. 运行 `python3 tools/cyberlog.py today`，确认今天的 Daily 文件夹存在，并在昨天 `_tomorrow-boot.md` 存在时打印启动包。
4. 在 `Daily/raw/YYYY-MM-DD/` 目录写入一个原始文件，并在 `Daily/compiled/YYYY-MM-DD/` 写入 `_cyberlog.md`，运行 `daily`，确认 `_ai-feed.md` 只包含 raw 中非 `_` 开头文件，且默认排除 `chatroom/`。
5. 检查 `_ai-context.md` 只包含历史 compiled 输出，并和 `_ai-feed.md` 分开。
6. 检查 `_ai-feed.md` 中是否有 `<file path=\"...\">` 文件边界。
7. 检查 `_ai-audit.md` 中的 included/excluded 文件清单、historical context 清单和 prompt/request 检查。
8. 运行 `prune-raw --older-than 7`，确认默认只预览；再用临时目录测试 `--apply` 会删除完整 daily 的 raw 并写 `_raw-discard-log.md`。
9. 准备几天的 `_cyberlog.md` 和 `_tomorrow-boot.md`，运行 `weekly`，确认会收集存在的文件。
10. 删除某天的 `_tomorrow-boot.md` 后再运行 `weekly`，确认输出 warning 而不是失败。

也可以运行内置测试：

```bash
python3 tools/test_cyberlog.py
```

## 常见问题

### daily 提示 Daily 日期文件夹不存在

先运行 `python3 tools/cyberlog.py today` 创建今天目录，或手动创建 `Daily/raw/YYYY-MM-DD/`。

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
  "raw_retention_days": 7,
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
    raw_retention_days: int
    weekly_week_basis: str


@dataclass(frozen=True)
class RawFileEntry:
    path: Path
    size: int
    sha256: str


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


def build_daily_request(day: dt.date, prompt: str, feed: str, context: str) -> str:
    next_day = day + dt.timedelta(days=1)
    day_dir = f"Daily/compiled/{day.isoformat()}"
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
            status_line("request separates historical context from AI Feed", "## Historical Context" in request),
            status_line("request marks historical context as not raw evidence", "不是今天的 raw evidence" in request),
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
- Included historical context files: {len(context_sources)}
- Missing historical context files: {len(context_warnings)}
- Configured excluded directories: {', '.join(config.daily_exclude_dirs) if config.daily_exclude_dirs else '未配置'}

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
    request = build_daily_request(day, prompt, feed, context)
    audit = build_daily_audit(
        day,
        source_files,
        excluded_files,
        context_sources,
        context_warnings,
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

    print(f"Wrote {display_path(feed_path, config.workspace_root)}")
    print(f"Wrote {display_path(context_path, config.workspace_root)}")
    print(f"Wrote {display_path(request_path, config.workspace_root)}")
    print(f"Wrote {display_path(audit_path, config.workspace_root)}")
    print(f"Merged {len(source_files)} raw markdown file(s).")
    print(f"Included {len(context_sources)} historical context file(s).")
    if excluded_files:
        print(f"Excluded {len(excluded_files)} markdown file(s).")
    if context_warnings:
        print(f"Missing {len(context_warnings)} historical context file(s).")
    return 0


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

    timestamp = now_from_environment()
    day = parse_date(args.date) if args.date else timestamp.date()
    raw_dir = config.daily_raw_root / day.isoformat()
    raw_dir.mkdir(parents=True, exist_ok=True)

    stem = f"{timestamp:%H%M}-capture"
    output_path = raw_dir / f"{stem}.md"
    suffix = 2
    while output_path.exists():
        output_path = raw_dir / f"{stem}-{suffix}.md"
        suffix += 1

    if not captured.endswith("\n"):
        captured += "\n"
    write_text(output_path, captured)
    print(f"Wrote {display_path(output_path, config.workspace_root)}")
    return 0


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
