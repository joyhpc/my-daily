"""Built-in templates for the Daily Cyberlog runtime.

These are copied into workspace files by `cyberlog init`.
"""

from __future__ import annotations

AI_SYNC_PROMPT = """# Daily Cyberlog / 工作画布 AI Sync Prompt

你是我的 cyberlog 整理 agent 和工作流分析 agent。

下面的 request 通常包含两类输入：

- `AI Feed`：今天 `Daily/raw/YYYY-MM-DD/` 中进入合并的 markdown。它是今天的主要事实输入。
- `Historical Context`：昨天的 `_cyberlog.md` 和最近几天的 `_tomorrow-boot.md`。它只能用于识别连续性、重复 blocker 和昨天计划，不能当作今天发生过的事实。
- `Project Registry`：`System/projects.yml` 的内容。它是项目 id、aliases、器件口径和项目约束的规范层，用来归一化项目分页和发现口径漂移。

raw 是临时事实输入层，不是永久记录层。daily 完整生成并人工审核后，raw 可能在 7 天后清理；不要因为 raw 未来可清理，就降低今天的事实/推断边界要求。

raw 允许使用极少量 `#标签` 做管理信号，通常每个文件最多一两个。优先识别可信度标签：`#可信` / `#已确认` / `#实测` 表示 high，`#待确认` 表示 medium，`#草稿` / `#未核实` / `#AI建议` 表示 low。需要第二个标签时，可以用 `#已发送`、`#阻塞`、`#待办`、`#决策` 表示轻量类型。标签优先于脚本默认推断；如果标签和正文语义冲突，不要静默修正，要显式标出冲突。

如果 request 包含 `Project Registry`，必须优先使用其中的 `projects[].id` 作为项目名；raw 中出现 alias 时归一化到对应 project id；raw 中出现 `forbidden_aliases` 或与 `constraints` 明显冲突的内容时，不要静默修正，要在 `_cyberlog.md` 的工作流摩擦或未完成任务中显式 flag。

你的任务不是做普通总结，而是从中提取我的工作状态、任务流、决策、阻塞、产出和自我迭代信号。

请严格区分：
- 明确事实
- 合理推断
- 建议
- 不确定信息

不要编造。找不到就写“未发现”。

在正式输出前，请先在内部完成一次信息清洗，但不要展开这部分过程：
1. 先读取 `Project Registry`，建立 project id、aliases、devices、forbidden_aliases、constraints 的映射。
2. 按 project id 聚类；没有命中的内容才放入 `其他`，不要把多个项目混在同一段。
3. raw 中出现 alias 时统一写成 project id；出现 forbidden_aliases 时保留原文并标为口径风险。
4. 先读取 `<file ... tags="...">` 和正文中的 `#标签`，按标签优先判断可信度和轻量类型；没有标签时再按 front matter 和正文状态词推断。
5. 给每条信息标记类型：fact / draft / sent-message / ai-suggestion / decision / todo / blocked / closed。
6. `chatroom`、`未命名`、历史 AI 回答、方案建议类内容，默认只能作为 `ai-suggestion` 或 `合理推断`，不能直接当作事实；只有原文明确出现“已完成 / 已发送 / 已确认 / 等待反馈 / 实测 / 核实”等状态词时，才可升级为事实。
7. 同一文件里如果同时出现“未发送版本”和“最终发送版本”，必须分别标记，不能合并成一个已发送事实。
8. 如果一个任务跨多个项目出现，请优先归入最具体项目，不要重复计算推进。
9. 如果某条信息只出现在 `Historical Context`，只能写成延续背景或待确认，不要写成“今日真实推进”。
10. 引用来源时尽量保留文件名或路径；这些路径用于审核，不代表 raw 会永久存在。

请输出以下结构：

# FILE: _cyberlog.md

# Cyberlog — {{date}}

## 0. 项目索引

按 `Project Registry` 中的 project id 列出今天命中的项目。每个项目只写一行：
- project id
- 今日是否有真实推进：yes / no
- 主要状态：active / blocked / queued / closed / evidence-only
- 关键风险：如无则写“未发现”

## 1. 今日真实推进

列出今天真正产生推进的事项，而不是所有活动。
必须按 `### <project id>` 分组；每组只写该项目的推进，不要五项目混写。

## 2. 当前工作画布

本节必须按项目组织；同一个 Active / Queue / Blocked / Closed 条目必须写明 project id。

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

| 项目 | 决策 | 状态 | 背景 | 理由 | 风险 | 后续动作 | 来源文件 |
|---|---|---|---|---|---|---|---|

`状态` 只能使用：proposed / validated / frozen / superseded / unknown。不要把 draft 或建议写成 frozen。

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
- 属于哪个 project id
- 位置或来源
- 可复用价值

## 6. 未完成任务

只列出仍然需要行动的事项。
每个任务给出：
- 任务
- 所属 project id
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
如果输入中包含 `_decisions.yml`、`_comms.yml`、`_conflicts.md`，它们是结构化状态文件，应优先用于决策、沟通和冲突状态判断。
请分析我的工作流，而不是总结流水账。

边界规则：
- 周复盘只使用已经审核过的 compiled 输出，不回读 raw。
- raw 是临时事实输入层，可能已经按保留期清理；不要把 raw 缺失当成记录不完整。
- `_ai-feed.md` 和 `_ai-request.md` 是生成中间件，不是周复盘的长期事实来源。
- 如果某天缺少 `_cyberlog.md` 或 `_tomorrow-boot.md`，把它作为记录缺口，不要自行从其他来源补事实。
- `_comms.yml` 中状态卡在 `draft` 超过 3 天的沟通项必须列入追踪；`waiting_for_reply` 超过 `expected_reply_by` 的沟通项必须列入追踪；无 `expected_reply_by` 但影响 P0/P1 项目的等待项列为 warning。
- `_conflicts.md` 中未关闭的 forbidden alias、LPDDR5/LPDDR5X、constraint conflict 必须进入下周风险或阻塞。

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

## 9. 沟通状态追踪

基于 `_comms.yml` 输出：
- draft 超过 3 天的项
- waiting_for_reply 超过 expected_reply_by 的项
- 无 expected_reply_by 但影响 P0/P1 项目的 waiting 项
- 本周最该发送或追问的 1-3 项

## 10. 下周只做一个自我迭代实验

必须是一个最小实验，而不是大计划。
格式：
- 实验：
- 触发条件：
- 执行动作：
- 成功标准：
- 失败信号：
- 复查时间：

## 11. 下周默认工作画布

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
6. raw 只作为临时事实输入层。daily 完整生成、审核并通过 `close-day` 标记为 `closed` 后，7 天后可以运行 `python3 tools/cyberlog.py prune-raw --older-than 7 --apply` 清理，只保留 compiled 和 `_raw-discard-log.md`。

`close-day` 运行前的核心输出 gate：
- `_ai-audit.md`
- `_cyberlog.md`
- `_tomorrow-boot.md`
- `_ai-output-audit.md`

`_ai-feed.md`、`_ai-context.md`、`_ai-request.md` 是 `daily` 生成的投喂中间件，通常应存在，但不是直接 raw 清理 gate。`prune-raw` 只清理 `_run-state.json` 中 `phase == closed` 的日期。

当天有对应状态时还应生成或更新：
- `_conflicts.md`（运行 `python3 tools/cyberlog.py conflict-scan --date YYYY-MM-DD` 后生成）
- `_decisions.yml`（当天有关键决策、状态变化或 supersedes 时必须更新）
- `_comms.yml`（当天有 draft / sent / waiting_for_reply / replied / closed 沟通状态时必须更新）

## 我如何给 raw 打标签

raw 默认自由写，不需要填表。只有当可信度会影响后续整理时，才在正文开头加一两个 `#标签`：
- `#可信`：我确认过，可作为事实候选。
- `#待确认`：有价值但未完全核实，只能作为待确认或合理推断。
- `#草稿`：草稿、想法或 AI 建议，不得升级为事实。

需要第二个标签时才补类型，例如 `#已发送`、`#阻塞`、`#待办`、`#决策`。标签优先于脚本默认推断。

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

## 我如何关闭一天的冲突

1. 先运行 `python3 tools/cyberlog.py daily --date YYYY-MM-DD` 生成 request 和 audit。
2. 完成 `_cyberlog.md`、`_tomorrow-boot.md`、`_ai-output-audit.md` 后，运行 `python3 tools/cyberlog.py conflict-scan --date YYYY-MM-DD`。
3. 审核 `_conflicts.md` 中的 forbidden alias、LPDDR5/LPDDR5X、constraints 冲突；不能当天解决的，必须进入 `_cyberlog.md` 的 Blocked / 未完成任务。
4. 当天新增或改变的跨日决策写入 `_decisions.yml`；如果替代旧决策，必须写 `supersedes`。
5. 沟通稿、邮件、群内同步只要影响项目状态，就在 `_comms.yml` 写明 `draft / sent / waiting_for_reply / replied / closed`。
6. 最后运行 `python3 tools/cyberlog.py decisions --rollup --through YYYY-MM-DD`，更新 `System/decisions-active.md`，作为第二天早上的第一眼视图。
7. 运行 `python3 tools/cyberlog.py validate --date YYYY-MM-DD`；如需留档，使用 `--write` 生成 `_validation.md`。
8. 运行 `python3 tools/cyberlog.py close-day --date YYYY-MM-DD`；无 blocking finding 时会把 `_run-state.json` 标记为 `closed`。

## Daily flow 的定义/执行分离

流程定义固定为：

`daily -> AI output -> conflict-scan -> decisions rollup -> validate -> close-day -> prune/weekly`

每一步的职责边界：
- `_run-state.json`：由 `today`、`daily`、`validate --write`、`close-day` 维护，记录 phase、状态转换、输入 hash 和规则/provenance hash；`prune-raw` 只清理 `closed` 日期。
- `daily`：只组装输入和 audit，不替 AI 做判断。
- `AI output`：生成 `_cyberlog.md`、`_tomorrow-boot.md`、`_ai-output-audit.md`，必须人工审核。
- `conflict-scan`：生成 `_conflicts.md`，把口径冲突从叙述中抽成 gate finding。
- `decisions rollup`：生成 `System/decisions-active.md`，只展示未 frozen / superseded 的决策。
- `validate`：只读校验 schema、AI output contract、conflict gate、decision integrity、comms aging；默认打印，不写文件。
- `close-day`：串起 conflict scan、decision rollup 和 validation；只有无 blocking finding 才关闭当天。
- `weekly`：只读取 compiled 输出和结构化状态，不回读 raw。

如果 `validate --date YYYY-MM-DD` 出现 `blocking`，当天不能视作关闭；必须解决、显式接受，或把它记录为下一天的阻塞。
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

## Rule 8: 跨日决策只能通过 _decisions.yml 的 supersedes 链流转

触发条件：今天的结论与昨天或历史决策不一致。
规则：必须在 `Daily/compiled/YYYY-MM-DD/_decisions.yml` 中显式写 `supersedes: [<旧决策id>]`，并把旧决策标记为 `superseded`，或确保 `decisions --rollup` 能通过 supersedes 链把旧决策排除出 active view。
原因：避免 `_cyberlog.md` 决策表反复出现“昨天写过、今天又写一遍但措辞不同”的影子冲突。
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
        _ai-audit.md
        _run-state.json
        _cyberlog.md
        _tomorrow-boot.md
        _ai-output-audit.md
        _conflicts.md
        _validation.md
        _decisions.yml
        _comms.yml
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
    projects.yml
    schemas.md
    decisions-active.md
    weekly-review-prompt.md
    personal-operating-manual.md
    workflow-rules.md
  tools/
    cyberlog.py
    cyberlog_core/
      cli.py
      app.py
      constants.py
      models.py
      templates.py
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

## 代码结构

- `tools/cyberlog.py`：薄 CLI wrapper，只负责调用 runtime。
- `tools/cyberlog_core/cli.py`：参数解析和命令分发。
- `tools/cyberlog_core/app.py`：daily、validate、close-day、weekly、prune 等运行时命令实现。
- `tools/cyberlog_core/templates.py`：`init` 会落盘的内置 prompt / README / schema 模板。
- `tools/cyberlog_core/models.py`：共享 dataclass 模型。
- `tools/cyberlog_core/constants.py`：小型运行常量和默认配置。

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
python3 tools/cyberlog.py capture --type blocker --project A38-DF108-Agilex5 "等待 FAE 确认 SmartVID regulator"
python3 tools/cyberlog.py capture --type sent --project A38-DF108-Agilex5 --sent-to FAE --subject "SmartVID 问题清单" --waiting-for "regulator confirmation" "已发送 FAE 问题清单"
printf "会议结论..." | python3 tools/cyberlog.py capture
```

`capture` 会写入 `Daily/raw/YYYY-MM-DD/HHMM-capture.md`。结构化类型会写入 `HHMM-<type>.md`，并带 front matter：`type`、`project`、`trust`、`sent_to`、`subject`、`waiting_for` 等。`daily` 生成 `_ai-feed.md` 时会把这些字段暴露在 `<file ...>` 标签上，帮助 AI 区分事实、草稿、发送、阻塞和普通 note。如果同一分钟已经存在文件，会自动使用 `-2` 后缀，不会覆盖已有 raw note。

也可以不用 front matter，只在 raw 正文开头写一两个 `#标签`。推荐最小集合是 `#可信`、`#待确认`、`#草稿`；需要第二个标签时再补 `#已发送`、`#阻塞`、`#待办`、`#决策`。`daily` 会把前两个标签透传到 `<file tags="...">`，并优先用可信度标签生成 `trust="high|medium|low"`。

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
- `Daily/compiled/2026-05-07/_run-state.json`

`_ai-feed.md` 只包含当天 raw 目录中非 `_` 开头的 markdown。`_ai-context.md` 单独保存跨日上下文：昨天的 `_cyberlog.md` 和最近 3 天的 `_tomorrow-boot.md`。这些内容只用于识别连续任务和重复 blocker，不作为今天的 raw evidence。

如果存在 `System/projects.yml`，`daily` 会把它作为 `Project Registry` 注入 `_ai-request.md`。AI 输出应按 project id 分章节，并用 aliases / forbidden_aliases / constraints 做项目口径校验。

## 默认完整处理

`_ai-request.md` 是给 AI 的任务包，不是整理结果。`daily` 生成的 request package 包含：

- `_ai-feed.md`
- `_ai-context.md`
- `_ai-request.md`
- `_ai-audit.md`

这些是投喂与审计中间件，不是长期 daily record。`close-day` 运行前的核心输出 gate 是当天目录里同时存在：

- `_ai-audit.md`
- `_cyberlog.md`
- `_tomorrow-boot.md`
- `_ai-output-audit.md`

这 4 个文件表示：输入包已审计、AI 输出已落盘、明日启动包已生成、输出边界已自检。`_ai-feed.md`、`_ai-context.md`、`_ai-request.md` 通常也会存在，但不直接作为 raw 清理 gate。`prune-raw` 现在要求 `_run-state.json` 的 `phase` 为 `closed`，因此应先运行 `close-day`。

你可以用两种方式触发完整处理：

1. 在聊天窗口里打开当天的 `_ai-request.md`，复制全部内容，粘贴给 AI。
2. 在 Codex 工作区里直接说：`处理 Daily/compiled/YYYY-MM-DD/_ai-request.md，并保存 _cyberlog.md 和 _tomorrow-boot.md`。

如果 AI/Codex 有文件写入能力，它应该直接保存：

- `Daily/compiled/YYYY-MM-DD/_cyberlog.md`
- `Daily/compiled/YYYY-MM-DD/_tomorrow-boot.md`
- `Daily/compiled/YYYY-MM-DD/_ai-output-audit.md`

之后运行：

```bash
python3 tools/cyberlog.py conflict-scan --date YYYY-MM-DD
python3 tools/cyberlog.py decisions --rollup --through YYYY-MM-DD
python3 tools/cyberlog.py validate --date YYYY-MM-DD --write
python3 tools/cyberlog.py close-day --date YYYY-MM-DD
```

`conflict-scan` 会生成 `_conflicts.md`，先做静态口径检查：forbidden aliases、LPDDR5/LPDDR5X 共现、项目 constraints 冲突。`decisions --rollup` 会读取每天的 `_decisions.yml`，更新 `System/decisions-active.md`。`validate` 默认只读打印 gate 结果；需要落盘时加 `--write` 生成 `_validation.md`，需要 CI/脚本遇到 blocking 直接失败时加 `--strict`。`close-day` 会串起 conflict scan、decision rollup 和 validation；只有没有 blocking finding 时，才把 `_run-state.json` 标记为 `closed`。

`today`、`daily`、`validate --write` 和 `close-day` 会维护 `_run-state.json`。它记录当前 phase、状态转换、输入 raw 文件 hash，以及 prompt / workflow rules / projects / schemas / config 的 provenance hash。`prune-raw` 只清理 `phase == closed` 的日期。

如果当天有跨日决策或沟通状态变化，建议补：

- `Daily/compiled/YYYY-MM-DD/_decisions.yml`
- `Daily/compiled/YYYY-MM-DD/_comms.yml`

只有在 AI 没有文件写入能力时，才把结果完整输出到聊天窗口，由你手动保存。`_cyberlog.md` 保存完整日终整理，`_tomorrow-boot.md` 只保存明天启动包。

当前脚本不自动调用 AI API。这样可以避免 API key、费用、模型选择和自动覆盖结果的问题。`_ai-audit.md` 用来先审核任务包边界，真正的 AI 输出仍应在保存前过一遍人工检查。

`_ai-output-audit.md` 用于记录 AI 输出是否误读草稿状态、是否混入被排除目录、是否把推断升级成事实。

## 每周怎么用

周复盘只读取每天已经整理后的 compiled 输出，不会读取原始 daily notes。它会优先收集 `_cyberlog.md` 和 `_tomorrow-boot.md`，如果存在 `_decisions.yml`、`_comms.yml`、`_conflicts.md`，也会一起放入 weekly request。

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

`raw_retention_days` 默认是 `7`。raw 是临时事实输入层，不是永久记录层。当天完整生成、通过 `close-day` 标记为 `closed` 后，raw 可以在保留期之后用 `prune-raw` 清理；系统会在 compiled 目录保留 `_raw-discard-log.md`。

`weekly_week_basis` 默认是 `end`，因此 `2026-05-01` 到 `2026-05-07` 会生成 `2026-W19_ai-weekly-request.md`。如果你希望严格按 start 日期计算周号，可以改成 `start`。

## 命令速查

```bash
python3 tools/cyberlog.py init
python3 tools/cyberlog.py today
python3 tools/cyberlog.py capture "quick note"
python3 tools/cyberlog.py capture --type todo --project cyberlog-workflow "补 validate 引用追溯"
python3 tools/cyberlog.py daily --date 2026-05-07
python3 tools/cyberlog.py conflict-scan --date 2026-05-07
python3 tools/cyberlog.py decisions --rollup --through 2026-05-07
python3 tools/cyberlog.py validate --date 2026-05-07 --write
python3 tools/cyberlog.py close-day --date 2026-05-07
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
8. 运行 `conflict-scan --date YYYY-MM-DD`，确认会生成 `_conflicts.md` 并列出 forbidden alias / LPDDR5X 等静态冲突。
9. 准备 `_decisions.yml` 后运行 `decisions --rollup --through YYYY-MM-DD`，确认会生成 `System/decisions-active.md`。
10. 运行 `validate --date YYYY-MM-DD`，确认会打印 schema、AI output contract、conflict gate、decision integrity 和 comms aging 检查。
11. 运行 `close-day --date YYYY-MM-DD`，确认无 blocking 时 `_run-state.json` 进入 `closed`。
12. 运行 `prune-raw --older-than 7`，确认默认只预览；再用临时目录测试 `--apply` 只会删除 `phase == closed` 的 raw 并写 `_raw-discard-log.md`。
13. 准备几天的 `_cyberlog.md` 和 `_tomorrow-boot.md`，运行 `weekly`，确认会收集存在的文件。
14. 删除某天的 `_tomorrow-boot.md` 后再运行 `weekly`，确认输出 warning 而不是失败。

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

PROJECTS_TEMPLATE = """# Project Registry
#
# This file is the canonical project/alias/constraint layer for daily cyberlog
# generation. Daily raw notes may use aliases or draft names; compiled outputs
# should normalize to these project ids and flag forbidden aliases.

projects:
  - id: cyberlog-workflow
    aliases:
      - cyberlog
      - daily
      - daily cyberlog
      - workflow
      - AI sync
    status: maintenance
    priority: P2
    focus:
      - raw / compiled pipeline
      - AI request and audit prompts
      - workflow rules
      - context recovery
    constraints:
      generated_files: "AI may write generated underscore-prefixed files only; do not overwrite raw notes."
      daily_close_gate: "_ai-feed.md, _ai-context.md, _ai-request.md, _ai-audit.md, _cyberlog.md, _tomorrow-boot.md, and _ai-output-audit.md should exist before raw pruning."
"""

SCHEMAS_TEMPLATE = """# Cyberlog State Schemas

This document is the human-readable contract for the structured state files used by the cyberlog pipeline. The files are intentionally simple YAML so they can be edited by hand and read by lightweight tooling.

## System/projects.yml

Purpose: canonical project id, alias, device vocabulary, and constraints.

| Field | Required | Allowed / Format | Meaning | Example |
|---|---:|---|---|---|
| `id` | yes | stable string | Canonical project id used in compiled output | `A38-DF108-Agilex5` |
| `aliases` | no | list of strings | Raw names that normalize to `id` | `[A38, DF108]` |
| `status` | no | `active / queue / maintenance / closed` | Project activity state | `active` |
| `priority` | no | `P0 / P1 / P2 / P3` | Comms aging priority, used when waiting items lack `expected_reply_by` | `P1` |
| `focus` | no | list of strings | Current durable work themes | `LPDDR5 memory architecture` |
| `devices.primary` | no | string | Preferred device vocabulary | `A5ED052AB32AE2V` |
| `devices.candidates` | no | list of strings | Candidate or disputed device names | `A5ED065B B32A` |
| `devices.forbidden_aliases` | no | list of strings | Known wrong or historical names that must be flagged | `A5EC052A B32A` |
| `constraints` | no | map of string values | Project-level rules used by conflict scan | `memory: "LPDDR5 (NOT LPDDR5X)"` |

## Daily/compiled/YYYY-MM-DD/_decisions.yml

Purpose: machine-readable cross-day decisions. Active decisions feed `System/decisions-active.md`.

| Field | Required | Allowed / Format | Meaning | Example |
|---|---:|---|---|---|
| `id` | yes | `<project>/<YYYY-MM-DD-NNN>` | Stable decision id | `A38-DF108-Agilex5/2026-05-11-001` |
| `project` | yes | project id from `projects.yml` | Owning project | `A38-DF108-Agilex5` |
| `topic` | yes | string | Decision subject | `VCC/VCCP follow SmartVID` |
| `status` | yes | `proposed / validated / frozen / superseded / unknown` | Decision lifecycle | `proposed` |
| `blockers` | yes | list of strings, may be `[]` | What prevents closure | `[FAE confirmation]` |
| `owner` | yes | string | Responsible role or person | `HW` |
| `next` | yes | string | Next action required | `Send FAE questions` |
| `supersedes` | yes | list of decision ids, may be `[]` | Previous decisions replaced by this one | `[]` |
| `evidence` | yes | list of source names | Evidence trail | `[SmartVID PMBus.md]` |

## Daily/compiled/YYYY-MM-DD/_comms.yml

Purpose: communication state tracking so drafts, sent items, waits, and closures do not blur together.

| Field | Required | Allowed / Format | Meaning | Example |
|---|---:|---|---|---|
| `id` | yes | `<project>/<topic>-<YYYY-MM-DD>` | Stable communication id | `A38-DF108-Agilex5/smartvid-fae-2026-05-11` |
| `project` | yes | project id from `projects.yml` | Owning project | `A38-DF108-Agilex5` |
| `channel` | yes | string | Communication channel | `fae_message` |
| `draft` | no | file path or null | Draft source if any | `A5ED052AB32AE2V FAE 沟通.md` |
| `status` | yes | `draft / sent / waiting_for_reply / replied / closed` | Communication lifecycle | `draft` |
| `sent_to` | no | string or null | Recipient summary | `FAE` |
| `sent_at` | no | ISO date/datetime or null | Sent time | `2026-05-12` |
| `waiting_for` | no | string or null | Expected reply or decision | `regulator confirmation` |
| `expected_reply_by` | no | ISO date or null | Follow-up deadline | `2026-05-15` |

## Daily/compiled/YYYY-MM-DD/_run-state.json

Purpose: machine-readable execution telemetry for the daily pipeline. It is generated by `today`, `daily`, `validate --write`, and `close-day`; it is not manually edited.

| Field | Required | Allowed / Format | Meaning | Example |
|---|---:|---|---|---|
| `date` | yes | ISO date | Daily folder date | `2026-05-12` |
| `phase` | yes | `open / packaged / validated / validation_blocked / closed / unknown` | Current pipeline phase | `packaged` |
| `updated_at` | no | ISO datetime | Last state update | `2026-05-12T22:31:00+08:00` |
| `transitions` | yes | list of transition objects | Timeline of phase changes | `[{ "phase": "packaged", "by": "daily" }]` |
| `provenance` | no | map path -> sha256 | Rules/config files used when packaging | `System/ai-sync-prompt.md: ...` |
| `source_files_sha256` | no | map path -> sha256 | Raw files included in `_ai-feed.md` at packaging time | `Daily/raw/.../note.md: ...` |
| `outputs` | no | map path -> bool | Generated output presence when a phase changed | `_ai-request.md: true` |
| `validation` | no | object | Last `validate --write` result | `{ "gate_result": "BLOCKED" }` |

## Gate Severity

| Severity | Meaning |
|---|---|
| `info` | Useful visibility; does not block close |
| `warning` | Needs attention or follow-up; does not block close by default |
| `blocking` | Must be resolved or explicitly accepted before the day is considered closed |
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
