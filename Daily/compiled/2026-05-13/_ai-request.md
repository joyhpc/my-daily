# AI Sync Request - 2026-05-13

## 使用说明

复制本文件全部内容，粘贴给 AI。

AI 输出后建议保存为：
- `Daily/compiled/2026-05-13/_cyberlog.md`
- `Daily/compiled/2026-05-13/_tomorrow-boot.md`
- `Daily/compiled/2026-05-13/_ai-output-audit.md`

请先审核 AI 输出，不要让 AI 覆盖任何非下划线开头的原始 notes。

## Codex / Agent 执行模式

如果你是 Codex、agent，或者任何可以读写此仓库文件的 AI，请默认完整处理，不要只返回文本答案：

1. 读取本 request、同目录 `_ai-audit.md` 和 `_ai-context.md`。
2. 生成并保存 `Daily/compiled/2026-05-13/_cyberlog.md`。
3. 生成并保存 `Daily/compiled/2026-05-13/_tomorrow-boot.md`。
4. 生成并保存 `Daily/compiled/2026-05-13/_ai-output-audit.md`，说明是否发现误读草稿状态、混入被排除目录、把推断升级成事实等问题。
5. 不覆盖任何非 `_` 开头的原始 notes。

只有在没有文件写入能力时，才把结果完整输出到聊天窗口。

## Prompt

# Daily Cyberlog / 工作画布 AI Sync Prompt

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

# Cyberlog — 2026-05-13

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

# Tomorrow Boot Packet — 2026-05-14

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

## Project Registry

以下内容来自 `System/projects.yml`。它是项目 id、aliases、器件口径和约束的规范层；用于项目分页、别名归一化和冲突提示。

```yaml
# Project Registry
#
# This file is the canonical project/alias/constraint layer for daily cyberlog
# generation. Daily raw notes may use aliases or draft names; compiled outputs
# should normalize to these project ids and flag forbidden aliases.

projects:
  - id: A38-DF108-Agilex5
    aliases:
      - A38
      - DF108
      - A38 / DF108
      - Agilex 5
      - Agilex5方案
      - A38 Agilex 5
      - A38 Intel Altera Agilex 5
    status: active
    priority: P1
    focus:
      - first schematic revision
      - LPDDR5 memory architecture and sourcing
      - SmartVID / PMBus power tree
      - SDM / QSPI / clock / reset / config
      - MIPI / QSFP / HSIO pin planning
    devices:
      primary: A5ED052AB32AE2V
      candidates:
        - A5ED052A B32A
        - A5ED065B B32A
      forbidden_aliases:
        - A5EC052AB32AE2V
        - A5EC052A B32A
      evidence_required:
        - final ordering code
        - official pinout / package file
        - Quartus device support
        - EMIF / Pin Planner / Fitter output
        - FAE-confirmed power / SmartVID guidance
    constraints:
      memory: "Outbound sourcing constraint is ordinary LPDDR5, not LPDDR5X, x32 package width, 16bit die / die organization, long lifecycle. If LPDDR5X appears as candidate, flag as a conflict until the project explicitly accepts it."
      pin_freeze: "LPDDR5 / MIPI / QSFP pins cannot be frozen before Quartus EMIF / Pin Planner / Fitter evidence."
      regulator_path: "Prefer FAE validated SmartVID / PMBus regulator path for VCC/VCCP, including TPS53676 / LTC3882-1 / ISL68223; treat LTC7883 as reference-only until FAE confirms support."
      sdm_boot: "External QSPI boot defaults to AS x4 Normal mode with MSEL[2:0]=011 unless new evidence overrides it."
    known_open_gates:
      - final FPGA ordering code
      - LPDDR5 versus LPDDR5X acceptance
      - two x32 memory device capacity acceptance
      - SmartVID regulator and PMBus mode confirmation
      - logic-side Quartus minimum project validation

  - id: A57-eDP
    aliases:
      - A57
      - A57 eDP
      - eDP HBR3
      - Issue4
      - 后两通道
    status: active
    priority: P1
    focus:
      - eDP HBR3 eye diagram criteria
      - back-channel no-image / SerDes lock investigation
      - test matrix and pass/fail evidence
    standards:
      edp_rx_primary: "eDP 1.4b TP3_EQ, 75mVpp differential / 0.5UI"
      edp_rx_target: "90mVpp differential / 0.5UI"
      not_primary: "Do not use ordinary DP RX 75mV / 0.35UI as the main eDP 1.4b conclusion."
    constraints:
      evidence_boundary: "Do not mark root cause closed without actual eye diagram, register, mode, multi-board, or timing evidence."

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

  - id: workspace-skills
    aliases:
      - workspace
      - skills
      - workspace-skills
      - sch-reviewer
      - Agilex skills
    status: queue
    priority: P3
    focus:
      - project skill extraction
      - schematic review intermediate representation
      - reusable SOP / demo assets
    constraints:
      priority: "Keep queued unless raw evidence shows active execution on the day."

  - id: wiki-sync
    aliases:
      - my wiki
      - my-wiki
      - wiki-sync
      - GitHub wiki
    status: queue
    priority: P3
    focus:
      - synchronize wiki repository locally
    constraints:
      priority: "Keep queued unless the day contains concrete sync action or a blocker."
```

## Historical Context

以下内容来自同目录 `_ai-context.md`。它只用于识别跨日连续性和重复 blocker，不是今天的 raw evidence。

# AI Historical Context - 2026-05-13

This file is generated from previous compiled outputs. It is context only, not today's raw evidence.

## Boundary

- Use this context to detect continuity, repeated blockers, and yesterday's intended boot path.
- Do not treat historical context as proof that something happened today.
- Today's raw evidence remains `_ai-feed.md`.

## Warnings

- Missing historical context: Daily/compiled/2026-05-10/_tomorrow-boot.md

## Sources

<context role="previous-day-cyberlog" date="2026-05-12">
<file path="Daily/compiled/2026-05-12/_cyberlog.md">
# Cyberlog - 2026-05-12

## 1. 今日真实推进

- A57 eDP AUX 不出图问题出现有效收敛：正常不测 AUX 时可稳定出图，示波器表笔直接点测 AUX 相关信号会干扰通信并触发不出图；TX/RX 未改动、仅给 AUX_EN 增加 4.7K 上拉后，探头测试不出图现象未复现，RX 原异常波形消失，循环 50 多次、约 1 小时运行和重启测试均稳定出图。来源：`A57 eDP DeBug最新状态.md`, `A57 eDP 群对话内容整理.md`
- A57 eDP 根因优先级被重新排序：当前不优先怀疑 AUX_RX / AUX_TX 本身，而是优先怀疑 AUX_EN 在 FPGA 上电、配置或初始化阶段存在不确定状态/高阻风险；后续应先固定 EN 默认状态，再比对固件版本，最后再深入 AUX_RX/TX 波形和解析层。来源：`A57 eDP DeBug最新状态.md`, `A57 eDP 群对话内容整理.md`
- A57 eDP 测试方法风险被明确：直接用示波器表笔点测 AUX_RX、AUX_TX、AUX_EN 可能扰动 AUX 通信，后续应优先确认可用测试点或从 AU15P / 主 FPGA 侧找更合适的测点。来源：`A57 eDP 群对话内容整理.md`
- A38 + A5EC052A_B32 低速 GPIO 资源口径完成整理：当前总需求为 205 个 GPIO，A5E 可统计 GPIO 资源约 256 个，理论余量约 51 个；原“168 个确认可用，剩余 88 个 OK”的口径只对应 256 - 168，不等于总需求口径。来源：`GPIO统计.md`
- A38 GPIO 分配原则形成：37 个 3.3V 低速控制 GPIO 优先放 HVIO；168 个解码板主体 GPIO 如能接受 1.2V / 1.8V，可由 HSIO 与部分 HVIO 组合承接；关键风险从“数量是否够”转为“VDDIO 分配是否合理”。来源：`GPIO统计.md`
- DDR4 / DDR5 / LPDDR4 / LPDDR5 器件侧评估请求形成：本次只评估成本、供货、生命周期和资料完整性，主控兼容性由内部确认；DDR4/DDR5 优先 64bit 总位宽 x16/x8 方案，LPDDR4/LPDDR5 优先 64bit 总位宽 x32 package width 方案，并要求明确 package width、die organization、温度等级、NRND/EOL/LTB 替代料和资料冲突。来源：`lpddr5沟通.md`

## 2. 当前工作画布

### Active

- A57 eDP AUX 稳定性排查：当前最强证据指向 AUX_EN 默认状态/高阻风险，4.7K 上拉是有效实验变量，但尚未完成位置、电阻值、固件版本、固件默认电平和 AP 工具行为确认。
- A38 / DF108 Agilex 5 GPIO 资源评估：数量层面暂时满足 205 个低速 GPIO 需求，下一步要进入 bank/VDDIO 约束分配和 pin allocation 细化。
- A38/A57 memory 方案评估：DDR4 / DDR5 / LPDDR4 / LPDDR5 进入器件侧寻样/比较请求阶段，仍不能写成架构冻结或 BOM 冻结。
- A38 / DF108 Agilex 5 外部设计证据：raw 中记录了生成物 URL `https://github.com/joyhpc/DF108-revision-workspace/blob/main/revisions/rev-20260506-df108-ku040-to-a5ed052ab32ae2v/02_design_evidence/a38_agilex5_high_speed_gpio_allocation_20260512.md`，但今日 daily 未读取该外部文件内容。

### Queue

- 把 A57 AUX_EN 4.7K 上拉验证整理成可复现测试表：板号、固件版本、烧录方式、是否探测、循环次数、运行时长、是否重启、是否出图、AP 工具是否报错。
- 确认 A57 AUX_RX / AUX_TX / AUX_EN 三个信号是否有可用测试点，避免继续用会扰动通信的直接点测方式。
- 基于 205 GPIO 需求，把 37 个 3.3V GPIO、168 个 1.2V/1.8V GPIO 分配到具体 HVIO/HSIO bank，并标出 VDDIO/复用限制。
- 等待或整理 DDR4 / DDR5 / LPDDR4 / LPDDR5 供应商/代理回复表。
- 若 memory 沟通文本已经发送，补一条独立 raw note 标明 `sent` / `waiting-feedback` 状态。

### Blocked

- A57 eDP AUX 根因冻结：阻塞原因是 AUX_EN 上拉验证很强，但仍缺上拉位置、电阻实测、双方 bit/bin/JTAG 版本一致性、固件 EN 默认状态和 AP 错误行为确认；解除方式是按同一测试矩阵复测并记录；owner：硬件 / 固件 / 测试；下一步：先确认 4.7K 实装位置和固件版本。
- A57 eDP 非侵入式测量：阻塞原因是直接探测会改变现象，当前测试手段本身是变量；解除方式是确认 AUX_RX/AUX_TX/AUX_EN 测试点或改用更低扰动测量方式；owner：硬件 / 测试；下一步：确认 3 个测试点是否存在。
- A38 GPIO bank 分配冻结：阻塞原因是目前只有资源数量和原则，仍需确认 HSIO Bank 3B 右 half 的 VDDIO/复用限制，以及哪些解码板 GPIO 可接受 1.2V/1.8V；解除方式是建立逐信号 bank 分配表；owner：硬件；下一步：从 37 个 3.3V 控制类 GPIO 开始先占 HVIO。
- Memory 方案冻结：阻塞原因是今日文本只是器件侧评估请求，主控兼容性、EMIF/Fitter、容量接受、生命周期和供应链回复均未闭环；解除方式是收集四类存储的候选料号表并与内部兼容性验证分开评审；owner：硬件 / 采购 / 逻辑 / FAE；下一步：把供应商回复格式固定成比较表。

### Closed

- A57 eDP 排查中“同时改 AUX_RX/AUX_TX/AUX_EN”的方向暂时关闭：当前应避免多变量同时修改。
- A38 GPIO “只看 168 个解码板 GPIO、余量 88 个”的旧口径被修正：总需求口径应按 205 个计算，理论余量约 51 个。
- A38 GPIO 数量是否足够的一级判断暂时关闭：数量上满足，剩余问题是 VDDIO、bank、复用和具体 pin 分配。

## 3. 关键决策

| 决策 | 背景 | 理由 | 风险 | 后续动作 | 来源文件 |
|---|---|---|---|---|---|
| A57 eDP 先按 AUX_EN 默认状态/高阻风险方向继续验证 | 探头点测 AUX 会触发不出图；仅 AUX_EN 加 4.7K 上拉后问题未复现 | TX/RX 未改动，AUX_EN 上拉是当前最有效实验变量，且 RX 原异常波形消失 | 还不能直接定为最终根因，因版本、焊接位置、固件默认状态未确认 | 确认上拉位置、实测 4.7K、bit/bin/JTAG 版本、EN 初始化电平 | `A57 eDP DeBug最新状态.md`, `A57 eDP 群对话内容整理.md` |
| A57 eDP 暂不同时改 AUX_RX / AUX_TX / AUX_EN | 多个上下拉方向都讨论过，AUX_RX 下拉没有明显效果 | 多变量修改会破坏归因，当前应围绕 AUX_EN 单变量复核 | 如果只盯 EN，可能延后发现 RX/TX 波形或解析层问题 | EN 固定后再按受控变量观察 RX/TX 波形和解析 | `A57 eDP DeBug最新状态.md`, `A57 eDP 群对话内容整理.md` |
| A38 GPIO 余量按 205 总需求计算为约 51 个 | 需求包括 168 个解码板 GPIO 和 37 个 3.3V 低速控制 GPIO | 256 - 168 = 88 只反映解码板主体口径，容易误导 | 256 是可统计资源，仍需确认 VDDIO/复用/实际 pin 可用性 | 建 bank/VDDIO 分配表，先锁定 37 个 3.3V 控制 GPIO | `GPIO统计.md` |
| 37 个 3.3V 低速控制 GPIO 优先放 HVIO | HSIO 多数固定 1.2V 或跟随 LPDDR5 VDDIO | HVIO 可调 1.2V-3.3V，更适合 3.3V 控制信号 | HVIO 若被其它接口占用，需重新平衡 | 按 PMU/QSFP/I2C/DEV ID/扩展 IO 分类分配 HVIO | `GPIO统计.md` |
| DDR/LPDDR 评估先限定为器件侧，不把主控兼容性外发 | 目标 FPGA/SoC 平台暂不披露 | 能让供应商先给成本、供货、生命周期和资料完整性，不泄露平台细节 | 外部推荐可能与内部控制器/EMIF 不兼容 | 内部另行做主控兼容性、EMIF/Fitter 和架构验证 | `lpddr5沟通.md` |

## 4. 重要信息

- A57 eDP 当前现象：不测 AUX 时系统可正常出图；直接点测 AUX_RX、AUX_TX、AUX_EN 可能扰动 AUX 通信，导致 CR / EQ 未完成并不出图。
- A57 有效实验结果：TX/RX 未改动，仅 AUX_EN 增加 4.7K 上拉后，探头测试不出图未复现，RX 原异常波形消失，50 多次循环、约 1 小时运行和重启测试均正常。
- AUX 解析讨论：按曼彻斯特编码理解，同步阶段可重新校正采样点，数据阶段不易继续校正；若目标频率接近 800K，应关注频率/采样点稳定性。
- A57 待确认清单：AUX_EN 4.7K 上拉位置、实测阻值、双方 bit/bin/JTAG 内容、是否存在 bin1 升级差异、板卡固件是否一致、AP 循环工具在不出图时是否报采集错误、AUX_EN 上电/配置/初始化默认电平、固件是否需要初始化 AUX_EN。
- A38 GPIO 需求：168 个解码板 GPIO，4 个解码板电源 EN，14 个 PMU 板 GPIO，7 个 QSFP，4 个加密/注册芯片 I2C，4 个 DEV ID，4 个客户扩展 IO，总计 205。
- A38 GPIO 资源：120 个 HVIO，26 个 HSIO Bank 2A 固定 1.2V，24 个 HSIO Bank 2B/3A 跟随 LPDDR5 VDDIO，48 个 HSIO Bank 3B 右 half 待确认，38 个 HSIO Bank 3B 左 half 固定 1.2V，GTS 不可用；可统计合计约 256。
- Memory 评估请求要求：DDR4/DDR5 优先 x16 或 x8 组成 64bit；LPDDR4/LPDDR5 优先 x32 package width 组成 64bit，并要求明确 package width 和 die organization。
- raw 中的 GitHub URL 只作为外部生成物位置记录，今日整理未把该 URL 内容当作已读取证据。

## 5. 今日产出

- A57 eDP AUX debug 最新状态整理：属于 A57 eDP；位置 `Daily/raw/2026-05-12/5月12日_extracted/A57 eDP DeBug最新状态.md`；可复用价值是把有效实验变量收敛到 AUX_EN 4.7K 上拉。
- A57 eDP 群对话内容整理：属于 A57 eDP；位置 `Daily/raw/2026-05-12/5月12日_extracted/A57 eDP 群对话内容整理.md`；可复用价值是把现象、测量扰动、AUX 解析、上下拉尝试和后续验证项放到一张排查路径里。
- A38 + A5EC052A_B32 低速 GPIO 需求与资源评估：属于 A38/DF108 Agilex 5；位置 `Daily/raw/2026-05-12/5月12日_extracted/GPIO统计.md`；可复用价值是统一 205 总需求、256 可统计资源、51 理论余量和 VDDIO 分配原则。
- DDR4 / DDR5 / LPDDR4 / LPDDR5 器件侧评估请求文本：属于 A38/A57 memory 方案；位置 `Daily/raw/2026-05-12/5月12日_extracted/lpddr5沟通.md`；可复用价值是给供应商/代理提供明确比较维度。
- A38 Agilex 5 high-speed GPIO allocation 外部生成物链接：属于 A38/DF108 设计证据；来源 `lpddr5沟通.md` 中 URL；可复用价值是作为后续回到正式工作空间核验的入口。

## 6. 未完成任务

| 任务 | 所属项目 | 下一步动作 | 优先级 | 是否适合交给 AI / agent | 为什么 |
|---|---|---|---|---|---|
| 复核 AUX_EN 4.7K 上拉实验 | A57 eDP | 确认焊接位置、实测阻值、板号、循环次数、运行时长、重启条件和是否复现 | P0 | 部分适合 | AI 可生成测试表，实测需硬件/测试执行 |
| 对齐双方固件和烧录版本 | A57 eDP | 核对 bit / bin / JTAG 烧录内容、bin1 是否升级、板卡固件是否一致 | P0 | 部分适合 | AI 可生成核对 checklist，版本事实需工程侧确认 |
| 确认固件中 AUX_EN 默认电平 | A57 eDP | 检查上电、配置、初始化、未使能阶段 AUX_EN 是否高阻或不确定 | P0 | 部分适合 | 需要读固件/约束/寄存器实现 |
| 设计非侵入式 AUX 测量方式 | A57 eDP | 确认 AUX_RX / AUX_TX / AUX_EN 测试点，避免直接探头点测原始管脚 | P1 | 适合起草 | AI 可出测试点检查表和测量注意项 |
| 建 A38 GPIO bank 分配表 | A38 GPIO | 把 37 个 3.3V GPIO 优先放 HVIO，168 个主体 GPIO按 1.2V/1.8V 能力分配 | P0 | 适合 | 今日已有数量和原则，可由 AI 生成表格模板 |
| 确认 HSIO Bank 3B 右 half 限制 | A38 GPIO | 查官方 pinout / bank VDDIO / 复用限制，确认 48 个统计资源是否可用于目标 GPIO | P0 | 部分适合 | AI 可整理资料，最终以官方文档/FAE为准 |
| 收集四类 memory 候选料号回复 | A38/A57 memory | 按 DDR4/DDR5/LPDDR4/LPDDR5、位宽、容量、温度、生命周期、替代料和资料完整性建表 | P0 | 适合 | AI 可生成供应商回复模板和比较表 |
| 标记 memory 沟通文本发送状态 | A38/A57 memory | 若已发送，新增 raw note 写 `sent_to`、`sent_time`、`waiting_for`、`expected_output` | P1 | 适合提醒 | 当前 raw 没有明确发送状态，不能当成已发送事实 |
| 回到外部正式工作空间核验 high-speed GPIO allocation 文档 | A38 / DF108 | 打开并核验 URL 对应文档内容是否与今日 GPIO/LPDDR5 口径一致 | P1 | 部分适合 | AI 可审阅，正式证据应留在受控工作空间 |

## 7. 明日启动包

见 `Daily/compiled/2026-05-12/_tomorrow-boot.md`。

## 8. 工作流摩擦

- 现象：A57 eDP 的测量动作会改变问题表现。可能原因：AUX 信号对探头寄生参数敏感，直接点测把测试手段变成了实验变量。影响：容易把测量扰动误判为真实电路状态。明天修正动作：先建立非侵入式测量方案和测试点确认表。
- 现象：A57 eDP 已有强实验结果，但还缺版本、焊接和固件默认状态元数据。可能原因：现场 debug 先追复现和现象收敛，记录表还没补齐。影响：结果难以签核为根因。明天修正动作：把每次测试都绑定板号、固件版本、bit/bin/JTAG、上拉位置和运行条件。
- 现象：A38 GPIO 曾出现 168/88 与 205/51 两套口径。可能原因：部分需求和总需求混用。影响：评审时可能误判资源余量。明天修正动作：所有资源表必须同时写需求范围、公式和适用口径。
- 现象：memory 沟通文本有清晰评估要求，但没有明确发送状态。可能原因：daily raw 记录了请求正文，没有追加 sent/waiting-feedback 状态。影响：整理时只能按草稿/请求文本处理，不能确认外部协作进度。明天修正动作：外发后补一条独立状态 note。
- 现象：raw 中出现外部 GitHub 生成物 URL，但 daily 未包含该文件内容。可能原因：正式工作空间和 daily 记录分层。影响：daily 只能保存入口，不能替代正式证据审核。明天修正动作：需要审核该文档时回到正式工作空间读取原文。

## 9. 自我迭代建议

1. A57 eDP 明天先补一张 `AUX_EN pull-up evidence table`，只要缺上拉位置、电阻实测、固件版本或复测次数，就不要把 4.7K 上拉写成最终根因。
2. A38 GPIO 后续每张资源表必须同时列 `需求口径`、`资源口径`、`计算公式`、`不可用/待确认资源`，防止 88 和 51 这类余量口径混用。
3. 对外沟通正文进入 daily raw 时，首行加 `status: draft/sent/waiting-feedback/confirmed`；未标注状态的内容默认按 draft 处理。

## 10. 规则候选

### 规则候选 1
- 触发条件：测量动作会改变被测现象，例如探头接入后问题出现或消失。
- 规则：先把测量方式标为实验变量，建立非侵入式测量方案或测试点计划；在测量扰动未排除前，不把波形现象直接升级为根因事实。
- 原因：否则 debug 会被测量手段污染，导致错误归因。
- 例子：今天 A57 eDP 直接点测 AUX 信号会干扰 AUX 通信并导致不出图。
- 是否建议写入 System/workflow-rules.md：yes

### 规则候选 2
- 触发条件：做资源余量、GPIO 数量、lane 数、带宽或容量统计。
- 规则：必须写清需求口径、资源口径和计算公式；如果存在历史口径，必须说明新旧口径差异。
- 原因：部分需求口径和总需求口径混用会造成余量误判。
- 例子：今天 A38 GPIO 的 `256 - 168 = 88` 和 `256 - 205 = 51` 分别对应不同口径。
- 是否建议写入 System/workflow-rules.md：yes

### 规则候选 3
- 触发条件：把供应商/FAE/群沟通正文放入 daily raw。
- 规则：首行必须标注 `status: draft`、`status: sent`、`status: waiting-feedback` 或 `status: confirmed`；未标注状态的正文默认只能作为草稿或请求文本。
- 原因：daily 整理不能凭正文存在推断消息已经发送或对方已经确认。
- 例子：今天 `lpddr5沟通.md` 有完整请求内容，但没有明确发送状态。
- 是否建议写入 System/workflow-rules.md：yes
</file>
</context>
<context role="recent-tomorrow-boot" date="2026-05-11">
<file path="Daily/compiled/2026-05-11/_tomorrow-boot.md">
# Tomorrow Boot Packet - 2026-05-12

## 明日主线

- A38 / DF108 Agilex 5：先冻结目标器件和 SmartVID 电源证据，不要在 `A5ED052A/A5ED065B/A5EC052A` 口径未清时继续扩大原理图。
- A38/A57 memory：把 LPDDR5/DDR5 决策拆成容量、协议、封装、生命周期、MIPI/HSIO、EMIF/Fitter 六个 gate，不要写成“LPDDR5 已定”。
- A57 eDP：把今天确认的 eDP 1.4b HBR3 眼图判据落到实际测量表。

## 背景

- 2026-05-11 的 raw 主要围绕 A5ED052AB32AE2V / B32A 最小系统设计、SmartVID 电源、SDM/QSPI 启动、LPDDR5 寻样和 eDP 眼图标准。
- SmartVID 当前建议：VCC/VCCP 使用 `A5E_VCC_VID`，初始 0.80V，PMBus Master Mode，`CF109/PWRMGT_SCL`、`CF99/PWRMGT_SDA`，`AV72/VCCLSENSE`、`AU72/GNDSENSE` remote sense。
- Regulator 不能冻结：候选方向是 `TPS53676 / LTC3882-1 / ISL68223` 等 fully validated 器件，`LTC7883` 只能作为参考设计路线，需 FAE 确认。
- SDM/QSPI 当前建议：AS x4 Normal，`MSEL[2:0]=011`，`OSC_CLK_1/BR102` 使用 125MHz / 1.8V，`RREF_SDM/CL103` 用 2.00k 1% 到 GND。
- LPDDR5 当前主线候选美光 `MT62F1G32D2DS-020 WT:D` 是 4GB / 32Gb x32 LPDDR5X，仍未冻结。
- 今天材料明确提示：`A5ED065B B32A` 的证据缺口未关闭，不能直接迁移 `A5EC052A/A5ED052A` 的 pin/bank/EMIF 结论。
- eDP HBR3 判据：eDP 1.4b TP3_EQ 最低 75mVpp differential / 0.5UI，更稳妥目标 90mVpp / 0.5UI；普通 DP RX 75mV / 0.35UI 不作为主结论。

## 当前状态

- A38 原理图计划已有 4 天拆解，但首要风险是证据 gate 未冻结。
- SmartVID 方向已清楚，但 FAE、Quartus、EPE/Power Analyzer、PDN 分析未闭环。
- 参考原理图已整理，但不同参考板对应不同器件和 PMBus 架构，不能照抄。
- LPDDR5 寻样存在约束冲突：项目想要普通 LPDDR5 / 非 LPDDR5X / 16bit die，但当前可推进候选偏 LPDDR5X 4GB x32。
- 群内沟通和供应商邮件目前只能按 draft 处理，未发现明确“已发送”证据。
- A57 eDP 只有判据，不等于故障根因闭环。

## 第一动作

- 建一张 `A5ED052A/A5ED065B Evidence Gate` 表，先填这几列：
  - 最终 ordering code
  - 官方 pinout / package 文件
  - SmartVID power option
  - VCC/VCCP regulator 推荐
  - PMBus mode / address / PAGE / format
  - OSC_CLK_1 / RREF / AS x4 / MSEL
  - LPDDR5 EMIF / Pin Planner / Fitter
  - FAE review 状态

先把每项标成 `confirmed` / `pending` / `blocked`，再决定今天能不能继续画原理图扩面。

## 注意事项

- 不要把 `A5ED065B B32A` 当成已经确认的最终目标器件，除非有正式 ordering code 和官方资料。
- 不要把 065B SOM、065A Premium Devkit、KEIm SOM 的电流能力直接照抄到 A5ED052A。
- 不要用普通 fixed 0.8V regulator 直接冻结 VCC/VCCP。
- 不要把所有 0.8V rail 都接到 `A5E_VCC_VID`，其它 rail-sharing 要单独确认。
- `PWRMGT_ALERT` 在 PMBus Master 下不一定必需，但建议保留兼容位。
- LPDDR5X 与“只选普通 LPDDR5”是一个显式冲突，明天必须先定优先级。
- 群沟通文案未标 `sent` 前，只能当 draft。
- eDP 眼图判断必须确认测量点是 TP3_EQ / RX_EQ，以及均衡条件是否符合标准。

## 不要重复踩的坑

- 同封装参考设计被误用成同芯片签核证据。
- AI/报告草稿被写成 FAE 已确认。
- 供应链候选被写成 BOM 冻结。
- LPDDR5 pin list 没有 Quartus/Fitter/FAE 证据就继续扩面。
- 把普通 DP RX 眼图数值直接套到 eDP 1.4b HBR3。
- 沟通稿发出后没有留下 sent/waiting-feedback 记录。

## 可以交给 AI / agent 的部分

- 生成 A5ED052A/A5ED065B evidence gate 表。
- 把 SmartVID FAE 问题清单压缩成正式邮件/微信版本。
- 把 LPDDR5 约束拆成 hard constraint / preference / open question。
- 生成供应商回复表格模板。
- 生成 eDP 眼图测量结果 pass/fail 表。
- 审核当天 raw 中哪些是 draft、哪些是 confirmed fact。

## 必须由我亲自判断的部分

- 最终 FPGA ordering code 是否从 A5ED052A 变为 A5ED065B。
- 是否接受 LPDDR5X，还是硬性要求普通 LPDDR5。
- 是否接受两颗 4GB x32 导致整板 8GB。
- A57 是否必须保留 16 组 MIPI，还是接受 LPDDR5 方案下约 14 组 MIPI。
- SmartVID regulator 最终选型和供应链风险。
- 是否允许在 FAE/Quartus/PDN 未闭环前继续画原理图扩面。
</file>
</context>
<context role="recent-tomorrow-boot" date="2026-05-12">
<file path="Daily/compiled/2026-05-12/_tomorrow-boot.md">
# Tomorrow Boot Packet - 2026-05-13

## 明日主线

- A57 eDP：围绕 AUX_EN 4.7K 上拉做证据闭环，先补齐测试元数据，再决定是否进入原理图/固件修改。
- A38 GPIO：把 205 个低速 GPIO 从数量评估推进到 bank/VDDIO 分配表，优先锁定 37 个 3.3V 控制类 GPIO 的 HVIO 位置。
- A38/A57 memory：收集 DDR4 / DDR5 / LPDDR4 / LPDDR5 器件侧候选回复，并保持“器件侧评估”和“主控兼容性验证”分离。

## 背景

- A57 eDP 当前最强实验结果：TX/RX 未改动，仅 AUX_EN 加 4.7K 上拉后，探头测试不出图未复现，RX 异常波形消失，50 多次循环、约 1 小时运行和重启测试均稳定。
- 该结果还不是最终根因签核：仍需确认 AUX_EN 上拉位置、实测 4.7K、双方 bit/bin/JTAG 内容、固件版本、AUX_EN 上电/配置/初始化默认电平，以及 AP 工具在不出图时是否必然报错。
- 直接用示波器表笔点测 AUX_RX / AUX_TX / AUX_EN 可能扰动 AUX 通信，明天不要继续把直接探测结果当作无扰动事实。
- A38 GPIO 当前总需求是 205 个，可统计资源约 256 个，理论余量约 51 个；`256 - 168 = 88` 只是解码板主体 GPIO 口径。
- 37 个 3.3V 低速控制 GPIO 应优先放 HVIO；168 个解码板主体 GPIO 可根据 1.2V / 1.8V 要求分配到 HSIO 与 HVIO。
- Memory 外部评估请求已经形成，但 raw 未明确发送状态；如果已经发出，需要补状态记录。

## 当前状态

- A57 eDP：方向从 AUX_RX/TX 转向 AUX_EN 默认状态/高阻风险；4.7K 上拉是当前有效实验变量。
- A38 GPIO：数量层面满足，VDDIO/bank/复用限制仍未闭环。
- A38/A57 memory：DDR4/DDR5/LPDDR4/LPDDR5 只是进入器件侧评估请求阶段，尚未冻结。
- 外部正式工作空间有 high-speed GPIO allocation URL，但今日 daily 没有读取该文档内容。

## 第一动作

- 先建 `A57_AUX_EN_4K7_Verification` 表，列：
  - 板号
  - AUX_EN 上拉位置
  - 实测电阻
  - bit / bin / JTAG 版本
  - 是否存在 bin1 升级差异
  - 是否直接探测 AUX
  - 循环次数
  - 运行时长
  - 重启次数
  - 是否出图
  - RX 异常波形是否存在
  - AP 工具是否报采集错误
  - 结论

填完这张表后，再决定是否把 AUX_EN 外部上拉写入原理图修改项，或先要求固件把 EN 初始化为确定电平。

## 注意事项

- 不要把 4.7K 上拉直接写成最终根因；当前只能写成最有效实验变量。
- 不要同时改 AUX_RX、AUX_TX 和 AUX_EN。
- 不要继续用直接点测 AUX 原始管脚的结果做无扰动判断。
- A38 GPIO 余量统一按 205 总需求口径写 51，不要再混用 88。
- HSIO Bank 3B 右 half 的 48 个资源仍是待确认项，不能直接全量使用。
- LPDDR4/LPDDR5 供应商回复必须写清 package width 和 die organization，不要只写 x32。
- Memory 沟通如果已经发送，必须补 `sent_to`、`sent_time`、`waiting_for`、`expected_output`。

## 不要重复踩的坑

- 把测量扰动当成真实电路状态。
- 现场 debug 只记录结果，不记录板号、固件、烧录方式和测试条件。
- 把 AUX_EN 上拉有效误写成 AUX_RX/TX 已经无风险。
- 把 GPIO 数量满足误写成 pin/bank/VDDIO 已经签核。
- 把供应商评估请求误写成供应商已回复。
- 把 daily 中的外部链接当成 daily 已经审核过的正式证据。

## 可以交给 AI / agent 的部分

- 生成 A57 AUX_EN 4.7K 验证表模板。
- 生成 A57 AUX_RX / AUX_TX / AUX_EN 非侵入式测量 checklist。
- 生成 A38 205 GPIO bank/VDDIO 分配表模板。
- 生成 DDR4 / DDR5 / LPDDR4 / LPDDR5 供应商回复对比表。
- 审核 memory 沟通文本是否具备明确 `draft/sent/waiting-feedback` 状态。

## 必须由我亲自判断的部分

- AUX_EN 4.7K 上拉是否进入正式原理图修改。
- AUX_EN 默认状态是否通过硬件上拉解决，还是优先要求固件初始化。
- 37 个 3.3V GPIO 的 HVIO 资源是否足够并符合整板 pinout。
- 是否接受某些解码板 GPIO 使用 1.2V/1.8V。
- DDR4 / DDR5 / LPDDR4 / LPDDR5 哪条路线继续作为架构主线。
- 是否需要回到正式工作空间审核 high-speed GPIO allocation 文档并同步口径。
</file>
</context>

## AI Feed

<file path="Daily/raw/2026-05-13/5月13日_extracted/A5E VDDIO范围.md">
A5EC052A_B32 / Agilex 5 E-Series:

HSIO bank:
  VCCIO_PIO = 1.0 / 1.05 / 1.1 / 1.2 / 1.3 V

HVIO bank:
  VCCIO_HVIO = 1.8 / 2.5 / 3.3 V

SDM I/O:
  VCCIO_SDM = 1.8 V

HPS I/O:
  A5EC = No HPS，不适用



不是不确定，是需要支持CMOS1.2V和1.8V，这里由外部接入的设备决定。系统会根据接入设备信息进行VDDIO选择。重点是A5E的bank电压不支持这样调
外部io特别多，不能做HSIO和HVIO的切换，这样会远远不够用。
也不能用0Ω / DNP 做装配选择，不符合自动化。
那认为用电平转换芯片应该是最好的方案，但是方向性怎么办。收发控制这里。以及其它要考虑的问题有哪些


</file>
<file path="Daily/raw/2026-05-13/5月13日_extracted/DS90LV019 EN turnaround.md">
**turnaround 期间 = 半双工链路“从一方发送切换到另一方发送”的换向窗口。**

在 eDP AUX 里，AUX+/AUX- 是一对半双工差分线，同一时刻只能有一端驱动：

```text
Source 发 request  --->  释放 AUX 总线  --->  Sink 发 reply
        ↑                    ↑                    ↑
     本端驱动             turnaround            对端驱动
```

所以 **turnaround 期间** 不是某个固定数据字段，而是：

```text
当前发送端停止驱动
↓
AUX 差分线从“被当前端驱动”变成“无人驱动/park/idle”
↓
另一端准备接管并开始驱动
```

## 放到 DS90LV019 上就是这个过程

以 **FPGA/Source 发 AUX request，然后等面板/Sink 回包** 为例：

```text
阶段 1：Source 发送
DE  = 1    DS90LV019 Driver 打开
RE# = 1    可选：关闭接收，避免自发自收
DIN 输出 Manchester AUX 数据
AUX+/AUX- 被 Source 侧驱动

阶段 2：turnaround
DE  = 0    Source 侧 Driver 关闭，释放 AUX 总线
AUX+/AUX- 进入 idle / bus park / bias 状态
等待线上的毛刺、残余边沿、AC coupling 恢复
此时不能让 Source 和 Sink 同时驱动

阶段 3：Source 接收 Sink reply
RE# = 0    DS90LV019 Receiver 打开
ROUT 接收面板回来的 Manchester 数据
```

简单画就是：

```text
DIN / TXD :  request bits  ..............
DE       :  ───────────────┐
                            └────────────
AUX线    :  Source drive    |  idle/park  |  Sink drive
                            ↑ turnaround ↑
RE#      :  ────────────────┐        ┌────
                             └────────
ROUT/RXD :                  忽略毛刺  reply bits
```

## 注意：turnaround 不是“等待回包的整个时间”

这两个概念要分开：

```text
turnaround：
发送端释放总线，另一端准备接管的短暂换向窗口。

reply latency / response delay：
Sink 收到 request 后，内部处理并开始 reply 的等待时间。
```

也就是说：

```text
Source 发完最后一个 bit
↓
Source 关 DE，释放 AUX
↓
这是 turnaround
↓
Sink 可能过一段时间才真正开始 reply
↓
Source 在接收窗口里等 reply
```

## 为什么这里容易出问题？

因为半双工链路最怕三件事：

### 1. 两边同时驱动

Source 的 `DE` 还没关，Sink 已经开始回包：

```text
Source drive  +  Sink drive  =  总线争用
```

结果可能是 AUX 波形畸变、回包错误，严重时还有 IO 应力风险。

### 2. 本端关得太晚，误把残余边沿当成回包

比如 `DE` 刚关，AUX 线上还有反射、AC coupling 恢复、bias 回归过程。此时如果 `RE#` 已经打开，`ROUT` 可能跳几下，协议层可能误判为 Manchester 边沿。

### 3. 接收开得太晚，漏掉 Sink reply 的起始

如果 `RE#` 开太晚，可能错过面板回包的 precharge / sync / 起始序列，导致 AUX 解码失败。

## 对你这个设计，最实用的定义

你可以把 turnaround 期间定义为：

```text
从本端 AUX_TX 最后一个有效 bit / stop 结束后，
到允许本端 AUX_RX 正式采样对端回包之前的保护窗口。
```

对应控制动作：

```text
1. 发送结束
2. DE 拉低，关闭 DS90LV019 Driver
3. 等待 guard time
4. RE# 拉低，打开 DS90LV019 Receiver
5. RX 逻辑开始寻找 Sink reply 的 AUX 起始序列
```

## 更工程化的状态机

```text
IDLE
  DE=0
  RE#=0 或 1

TX_PREPARE
  RE#=1      关接收，避免自发自收
  DE=1       打开发送

TX_ACTIVE
  DIN 输出 AUX request

TX_END
  保证最后 stop / idle 发送完整

TURNAROUND
  DE=0       关闭发送，释放 AUX 总线
  等待 guard time
  清 RX FIFO / 清边沿检测 / 忽略毛刺

RX_ACTIVE
  RE#=0      打开接收
  等 Sink reply

RX_DONE
  解析 reply
  回到 IDLE
```

## 一句话

**turnaround 期间就是 eDP AUX 半双工链路的“换向期”：本端刚发完并释放 AUX 总线，对端还没正式接管或刚要接管的过渡窗口。**  
在 DS90LV019 方案里，它主要对应 **DE 关闭、AUX 线恢复、RE# 打开、RX 开始有效采样** 这一段。


CR/EQ 的真实判定
</file>
<file path="Daily/raw/2026-05-13/5月13日_extracted/DS90LV019 eDP AUX应用特性.md">
**先给判断：DS90LV019 可以作为 eDP AUX 半双工链路的工程折中方案，但不要把它当成“标准 eDP AUX PHY”。**  
它是通用 LVDS Driver/Receiver，而 eDP AUX 是 AC-coupled、双向半双工、Manchester 编码的低速控制链路。真正风险不在 1Mbps 速率，而在 **共模、电平幅度、方向切换、终端/偏置、以及 FPGA 侧 1.8V/1.2V 兼容性**。TI 资料也说明 AUX 是约 1Mbps 半双工双向通道，eDP/DP AUX 有自己的幅度、共模、AC 耦合和 bus park 要求。([德州仪器](https://www.ti.com/lit/pdf/SDAA295 "Debugging Methodology for DisplayPort/Embedded DisplayPort Link Training Utilizing the Auxiliary Channel"))

## 1. 最大风险：DS90LV019 的“LVDS 电气”不完全等于 eDP AUX 电气

DS90LV019 的 Receiver 阈值是 **±100mV**，而 TI 给出的 eDP AUX 电气表里，eDP AUX 在 TP3 的差分峰峰值最小可以到 **0.14Vpp**。如果按差分信号从正到负摆动理解，0.14Vpp 对应单边只有约 ±70mV，这会落在 DS90LV019 的最坏阈值以内。也就是说：**典型情况下可能能收，但从最坏值保证角度不够漂亮**。这是用 DS90LV019 接收 eDP AUX 回包时最需要验证的点。([德州仪器](https://www.ti.com/lit/ds/symlink/ds90lv019.pdf "DS90LV019 3.3V or 5V LVDS Driver/Receiver datasheet (Rev. B)"))

另一个高风险点是共模。DS90LV019 Driver 的 offset/common-mode 典型约 1.25V，范围可到 1.7V；而 TI 的 eDP AUX 表给出的 eDP AUX DC common-mode 范围是 **0~1.2V**。所以 **不要直接假设 DS90LV019 可以 DC 直连面板 AUX**。如果直连，典型值就已经接近/略超过 eDP 共模上限，最坏值更不行。更稳妥的做法是按 eDP AUX 的 AC coupling + bias 结构处理，并在连接器/面板侧实测共模。([德州仪器](https://www.ti.com/lit/ds/symlink/ds90lv019.pdf "DS90LV019 3.3V or 5V LVDS Driver/Receiver datasheet (Rev. B)"))

## 2. 推荐连接思路

比较合理的结构是：

```text
FPGA / MCU AUX_TXD  -> 电平转换 -> DS90LV019 DIN
FPGA / MCU AUX_DIR  -> 电平转换 -> DS90LV019 DE
FPGA / MCU AUX_DIR# 或独立 GPIO -> 电平转换 -> DS90LV019 RE#
DS90LV019 ROUT -> 3.3V 转 FPGA VCCIO -> FPGA / MCU AUX_RXD

DS90LV019 DO+/DO-  \
                    +--- eDP AUX+/AUX- 受控半双工差分节点 --- AC coupling / bias / panel
DS90LV019 RI+/RI-  /
```

如果 GPIO 够，**DE 和 RE# 建议分开控制**，这样可以做“全关断保护时间”。如果 GPIO 不够，`DE` 和 `RE#` 可以用同一个方向控制信号：发送时 `DE=1, RE#=1`；接收时 `DE=0, RE#=0`。但更推荐独立控制，因为 AUX 的问题很多时候就出在 turnaround 期间的毛刺、误采样或总线争用。

## 3. 方向切换时序建议

DS90LV019 本身的 enable/disable 是 ns 级，Driver disable/enable 最坏大约 8~9ns，Receiver enable/disable 最坏约 6~8ns；但 AUX 是 Manchester，UI 约 0.5µs，TI 给出的 AUX Manchester transaction UI 范围是 0.4~0.6µs。实际设计时不要按 10ns 去抠，建议按 **0.5~2µs 级别 guard time** 做半双工切换。([德州仪器](https://www.ti.com/lit/ds/symlink/ds90lv019.pdf "DS90LV019 3.3V or 5V LVDS Driver/Receiver datasheet (Rev. B)"))

推荐状态机：

```text
默认态：
DE = 0
RE# = 0 或 1，取决于你是否希望常开接收
更安全的是系统未 ready 前 RE# = 1，避免 ROUT 乱跳或反灌 FPGA

发送前：
RE# = 1        先关接收，避免自发自收干扰解码
delay >= 0.5us
DE = 1         打开发送

发送结束：
保持最后一个 bit / stop / bus park 完整结束
DE = 0         关闭发送
delay >= 0.5~2us，建议先从 1us 起测

接收窗口：
RE# = 0
等待 sink 回包
收到完整回包后再进入 idle
```

重点：**不要让本端 Driver 和对端 Driver 同时打开。** eDP AUX 是 source 主导，sink 只在 source request 后 reply，理论上不会主动乱发，但如果你的 DE 关晚、或者协议层等待窗口做错，就会出现 bus contention。

## 4. 终端和偏置不要乱加

DS90LV019 的典型应用图是两个 DS90LV019 做 full-duplex point-to-point，两对差分线，每对远端 100Ω 终端；但 eDP AUX 是一对线半双工，而且 DP/eDP AUX 还有 AC coupling、pull-up/pull-down、source/sink 侧 stuffing option。TI 的 eDP AUX guidance 里给了 eDP 场景下 source 侧 100kΩ、sink 侧 1MΩ、C_AUX=100nF 等 stuffing 选项，也给了 75~200nF 的 C_AUX 范围。([德州仪器](https://www.ti.com/lit/ds/symlink/ds90lv019.pdf "DS90LV019 3.3V or 5V LVDS Driver/Receiver datasheet (Rev. B)"))

所以设计上注意：

**不要简单在 DS90LV019 RI+/RI- 上再并一个 100Ω，然后面板侧也有 100Ω。**  
这样可能变成双端终端，等效负载接近 50Ω，幅度被压低，DS90LV019 Driver 负载也偏离 datasheet 条件。

**不要同时叠加 DS90LV019 fail-safe 网络和 eDP AUX bias 网络。**  
DS90LV019 datasheet 给了 terminated input fail-safe 示例，但那是 LVDS 场景。eDP AUX 已经有自己的 bias/AC coupling 设计逻辑，两个体系叠加可能导致 idle 差分偏置过大、共模不对、或者接收阈值被压偏。

**建议预留可调工位：**

```text
AUX+ / AUX- 串联 AC coupling cap：默认 100nF，预留 75~200nF范围可替换
AUX+ / AUX- 弱偏置电阻：100k / 1M 级别按 source/sink 位置选择
DS90 DO 到 AUX 节点：预留 0Ω 或小阻值串联电阻位
DS90 RI 到 AUX 节点：短 stub，必要时预留 0Ω 隔离
AUX P/N 极性：预留交叉修正手段或至少方便飞线验证
```

## 5. FPGA / MCU 侧电平是硬约束

DS90LV019 的 `DIN / DE / RE#` 是 TTL/CMOS 输入，但 VIH 最小是 **2.0V**；`ROUT` 输出高电平在 3.3V 供电时接近 3.3V。因此如果 FPGA bank 是 1.8V 或 1.2V，**不能直接接**。([德州仪器](https://www.ti.com/lit/ds/symlink/ds90lv019.pdf "DS90LV019 3.3V or 5V LVDS Driver/Receiver datasheet (Rev. B)"))

建议：

```text
FPGA 1.8V -> DS90 DIN/DE/RE#：用 1.8V 到 3.3V 单向电平转换
DS90 ROUT -> FPGA 1.8V：用 3.3V 到 1.8V 单向电平转换
```

这里方向很清楚，不需要双向自动电平转换器。`DIN/DE/RE#` 是 FPGA 到 DS90，`ROUT` 是 DS90 到 FPGA。不要用 I2C 那类自动双向 MOS 管电平转换，它不适合这种边沿/方向明确的逻辑信号。

## 6. 上电默认状态要保守

强烈建议：

```text
DE：外部下拉，默认关闭 Driver
RE#：根据 FPGA 上电状态决定
    如果 FPGA VCCIO 未上电，RE# 建议默认拉高，避免 ROUT 驱动未上电 FPGA
    如果 FPGA 已经稳定，RE# 可以拉低进入接收态
DIN：给确定默认态，不要悬空
```

如果 DS90LV019 先上电、FPGA bank 后上电，`ROUT` 可能通过 FPGA IO 保护结构反灌。这个在调试板上容易被忽略，量产或热插拔/面板掉电时容易出问题。

## 7. 发送幅度也要实测

DS90LV019 Driver 在 100Ω 负载下的 VOD 是 250~450mV。换成差分峰峰值理解，链路上会看到大约 0.5~0.9Vpp 量级，通常没有超过 TI 表里 eDP AUX 1.38Vpp 的上限，但明显高于 eDP AUX 0.20Vpp 的 nominal。([德州仪器](https://www.ti.com/lit/ds/symlink/ds90lv019.pdf "DS90LV019 3.3V or 5V LVDS Driver/Receiver datasheet (Rev. B)"))

这意味着：

**TX 方向大概率比 RX 方向容易成功，但不代表标准裕量一定好。**  
你需要在面板 AUX connector/TP3 处实测：

```text
VAUX_DIFF_PP
VAUX_DC_CM
AUX turnaround common-mode
Manchester UI
pre-charge pulse
SYNC / STOP 是否可正确解码
```

## 8. 不要支持 / 不要启用 Fast AUX

标准 AUX 是 1Mbps Manchester。VESA 的资料也说明默认 AUX 是 1Mbps Manchester，Fast AUX 是 720Mbps、8b/10b。DS90LV019 虽然标称 high signaling rate above 100Mbps，但它显然不是 720Mbps Fast AUX 的器件。([VESA 显示行业标准](https://www.vesa.org/wp-content/uploads/2011/01/ICCE-Presentation-on-VESA-DisplayPort.pdf "Microsoft PowerPoint - ICCE Presentation on VESA DisplayPort, Jan 10 2010, Craig Wiley, Parade (rev 2).pptx"))

所以系统策略要明确：

```text
只按 standard AUX / 1Mbps Manchester 使用
不要假设可以跑 Fast AUX
不要让 IP/软件配置进入 Fast AUX 相关模式
```

## 9. 调试时的高价值观测点

TI 的 AUX debug 文档建议用差分转单端后再给逻辑分析仪解析，并提示采样率至少 250MS/s；它还指出 AUX P/N 极性错时，会看不到正常的 SYNC END/START 或 STOP 序列。这个对你调试很有用。([德州仪器](https://www.ti.com/lit/pdf/SDAA295 "Debugging Methodology for DisplayPort/Embedded DisplayPort Link Training Utilizing the Auxiliary Channel"))

建议你板上预留：

```text
AUX+ / AUX- 差分测试点：靠近面板连接器
DS90 ROUT 测试点：给逻辑分析仪抓单端 Manchester
DE / RE# / DIN 测试点：确认方向切换时序
HPD 测试点：确认 AUX 事务发生前 sink 已 ready
```

调试顺序建议：

```text
1. 只测 DS90LV019 本地：
   DIN 输入 1Mbps Manchester 测试码
   看 DO+/DO- 幅度、共模、极性

2. 接上面板但不跑完整训练：
   只做 AUX native read，例如读 DPCD 基础能力
   看 source request 和 sink reply 是否都有

3. 如果只有 request 没有 reply：
   优先查 DE 是否关晚、RE# 是否开晚、面板电源/HPD、AUX 极性、AC cap/bias

4. 如果有 reply 但解码错：
   查 ROUT 阈值裕量、AUX_DIFF_PP 是否过低、P/N 是否反、采样点/Manchester 解码

5. 如果探头一接就不出图：
   说明 AUX 节点被测试手段扰动了
   改用高阻差分探头，或者用 DS90/专用 receiver 转单端后抓 ROUT
```

## 10. 我建议你按这个 checklist 冻结设计

```text
[ ] DS90LV019 使用 3.3V，不用 5V
[ ] DIN / DE / RE# 已做 FPGA VCCIO 到 3.3V 电平转换
[ ] ROUT 已做 3.3V 到 FPGA VCCIO 电平转换
[ ] DE 默认下拉，系统未 ready 时 Driver 不会误打开
[ ] RE# 默认状态不会导致 ROUT 反灌未上电 FPGA
[ ] AUX P/N 经过 AC coupling / bias 方案审查
[ ] DS90 common-mode 没有直接顶到 eDP AUX DC common-mode 限值
[ ] 没有重复终端导致 100Ω 变 50Ω
[ ] 半双工方向切换有 ≥0.5~1us guard time
[ ] 关闭 TX 后再打开 RX，不依赖 ns 级边界
[ ] ROUT 自发自收 echo 已在逻辑层屏蔽
[ ] AUX P/N 极性可验证、可修正
[ ] 面板连接器处预留 AUX 差分测试点
[ ] ROUT / DE / RE# / DIN 预留逻辑分析仪测试点
[ ] 不启用 Fast AUX
[ ] 至少验证：DPCD read、EDID over AUX、link training、掉电/上电/复位重试
```

**一句话建议：**  
如果这是量产路径，我会把 DS90LV019 定义为“可验证的工程折中”，而不是天然合规的 eDP AUX PHY。设计上重点守住四件事：**AC coupling + bias、RX 阈值裕量、DE/RE# turnaround、FPGA 侧电平转换**。其中最需要提前打样验证的是 **panel → DS90LV019 的回包幅度是否足够跨过 ±100mV 接收阈值**。
</file>
<file path="Daily/raw/2026-05-13/5月13日_extracted/EDP 问题定位到AUX.md">
这条补充把问题边界改清楚了：你们不是完整标准 Sink 根据高速接收结果回填 CR/EQ，而是 FPGA/控制逻辑在 AUX 上“代答”训练状态。这样 EQ/CR fail 的优先怀疑对象会
  前移到 AUX/DPCD 仿真和训练状态机。

• 对，这个补充后，链路要重新定义：

  标准 eDP：
  Main Link 实际训练结果 -> Sink 判断 CR/EQ -> AUX 返回 DPCD 状态 -> Source 决定是否出图

  你们当前实现：
  A57/eDP Source 发训练字
  AUX 上由 FPGA/逻辑代答 DPCD 状态
  CR/EQ OK 不是 SerDes 反馈来的，而是 FPGA 直接告诉 Source

  所以这里的结论应该是：

  如果 FPGA 没有用 SerDes 状态参与 CR/EQ 返回，那么 A57 侧看到 CR/EQ 失败，优先不是 SerDes 眼图问题，而是 AUX/DPCD 仿真/训练状态机问题。

  更准确地说，现在这个 EQ/CR fail 不是“真实高速链路均衡失败”的直接证据，而是：

  A57 的 eDP 训练状态机没有从 AUX/DPCD 读到它认可的 pass 状态

  可能原因集中在这些点：

  1. AUX 物理层不稳定
     AUX+ / AUX- / HPD 三根相关信号有毛刺、时序、共模、幅度、极性、终端、上拉、干扰问题，导致读写偶发失败。
  2. DPCD 返回内容不完整或不一致
     不是只回“训练 OK”一个概念就行。Source 通常会读这些状态：

     0x202: LANE0_1_STATUS
     0x203: LANE2_3_STATUS
     0x204: LANE_ALIGN_STATUS_UPDATED
     0x206/0x207: ADJUST_REQUEST

     例如 2 lane 全 OK，0x202 通常应体现 lane0/lane1 的 CR_DONE、EQ_DONE、SYMBOL_LOCK 都置位，0x204 还要有 lane align done。

  3. lane 数 / 速率 / 状态位不匹配
     比如 Source 配了 4 lane，但 FPGA 只返回了 2 lane OK；或者 link rate/lane count 写入成功了，但状态寄存器仍按另一个配置返回。
  4. 训练阶段时序不对
     Source 写 TRAINING_PATTERN_SET 后，会按阶段读 CR/EQ 状态。FPGA 如果状态更新太晚、太早、阶段切换时短暂返回 0，都会被 Source 判失败。
  5. HPD 或 AUX 异常被驱动归类成训练失败
     有些驱动日志里显示 CR/EQ fail，但根因可能是 AUX timeout、AUX NACK/DEFER、HPD 抖动、DPCD 读错。

  可以在群里这样回：

  明白。按我们现在这个架构，CR/EQ 状态不是 SerDes 实际训练结果反馈回来的，
  而是 FPGA 在 AUX/DPCD 上代答给 eDP Source 的。

  所以现在 A57 侧报 CR/EQ 概率失败，优先应该看 AUX 通信、DPCD 仿真内容和训练状态机，
  而不是先看 SerDes 眼图。SerDes 眼图好坏不会直接影响 AUX 上读到的 CR/EQ 状态，
  除非 SerDes 状态被接入了返回逻辑，或者二者有共同的电源/温度/时钟干扰源。

  下一步应该抓成功和失败两组 AUX transaction，对比：
  link rate、lane count、training pattern 写入是否一致；
  0x202/0x203/0x204 状态返回是否完整；
  AUX 是否有 timeout/NACK/DEFER/HPD 抖动。
  如果 FPGA 理论上固定返回 OK，但 A57 仍然判 CR/EQ fail，
  那就是 Source 没读到 OK、读到了不一致状态，或者 AUX/HPD/状态机时序有问题。

  一句话：在你们这个非标准闭环里，CR/EQ fail 的第一嫌疑人是 AUX/DPCD 代答链路，不是 SerDes 主链路。


</file>
<file path="Daily/raw/2026-05-13/5月13日_extracted/GPIO 1.2V 1.8V.md">
对，**168 个 pin 不适合按“一对一电平转换”去堆料**。这时更好的判断是：

```text
如果 168 路必须原样、实时、逐 pin、双向、任意方向透传，
那电平适配器件无论叫什么，本质都逃不掉 168 个电平边界。

真正更好的方法不是换一种 translator，
而是改变“电平边界的位置”或“接口形态”。
```

## 我建议的方案排序

### 方案 1：把连接器接口标准化为固定电平

这是最推荐的系统级方案。

```text
主板 A5E 侧：
  固定 1.2V 或固定 1.8V

外部接入设备侧：
  必须适配主板定义的接口电平
  如果外设内部是另一种 VDDIO，由外设板自己转换
```

也就是把规则改成：

```text
主板连接器不再支持“1.2V/1.8V 任意接入”
主板连接器只定义一种 CMOS 电平
外部模块负责适配
```

这对 168pin 是最干净的。否则主板会被 168 路 level shifting 拖死。

---

### 方案 2：做一块“接口适配子板 / 模块适配板”

如果外部设备已经存在，不能要求它改接口，那就不要把复杂度放主板上。

```text
A5E 主板
  固定 1.2V 或 1.8V 接口

适配小板
  识别外部设备
  选择 VDDIO_EXT
  完成 1.2V/1.8V 转换
  做 ESD / 热插拔 / 保护

外部设备
  保持原接口
```

结构是：

```text
A5E 主板 ── 固定电平接口 ── 适配板 ── 可变 1.2V/1.8V 外设
```

这样主板不背负所有兼容成本。不同外设用不同适配板，主板保持统一。

---

### 方案 3：用小 FPGA / CPLD / IO bridge 做“电平域边界”

这比堆 21 颗 8bit level shifter 更像工程方案。

结构：

```text
                固定电平/固定协议
A5E FPGA  ───────────────────────  IO Bridge / 小 FPGA / CPLD
                                               │
                                               │ 外部 bank 跟随 VDDIO_EXT
                                               ▼
                                      外部 168 路 CMOS IO
```

关键是：**不要让这个 IO bridge 只是 168 路透明转接**。如果只是透明转接，它本质还是一个大 translator。

它应该承担一部分协议/寄存器/采样/缓存功能，把 168 路外部 IO 收敛成主 FPGA 侧的固定接口，例如：

```text
外部 168 路 GPIO / 并口
  ↓
IO bridge 内部寄存器化 / 状态机化
  ↓
A5E 侧使用固定电平接口：
  SPI / QSPI / 并行 local bus / LVDS / Aurora-like / 自定义高速串行
```

适合场景：

```text
168 路不是每一根都高速实时
很多是控制、状态、strap、低速 GPIO
允许有寄存器访问延迟
方向可以由寄存器配置
```

Lattice MachXO5-NX 这类器件的一个价值就是 I/O bank 电压范围比 A5E 这种 HSIO/HVIO 分裂结构更适合做“接口胶水”。公开 sysI/O 文档里，MachXO5-NX 一些 wide-range bank 支持 1.2V/1.5V/1.8V/2.5V/3.3V，部分 high-performance bank 支持 1.0V/1.2V/1.35V/1.5V/1.8V。([Mouser Electronics](https://www.mouser.com/pdfDocs/FPGA-TN-02067-1-9-sysIO-User-Guide-Nexus-Platform.pdf?srsltid=AfmBOoprAxk7XwpayB050PPBdyKwzSJZT19Lt-1qTBeXawEgmRqJ-JTb&utm_source=chatgpt.com "sysI/O User Guide for Nexus Platform Technical Note"))

这类方案的本质是：

```text
A5E 不直接面对 1.2V/1.8V 可变世界；
让一个更适合做 IO glue 的器件面对外部世界。
```

---

### 方案 4：如果必须一对一，至少用高位宽 translator，而不是一堆小芯片

这是下策，但比 8bit/4bit 堆料好。

168 路如果用 32bit translator：

```text
168 / 32 = 5.25
实际需要 6 颗 32bit translator
```

比如 SN74AVC32T245 是 32-bit dual-supply bus transceiver，VCCA/VCCB 支持 1.2V 到 3.6V，支持 1.2V、1.8V 等低压节点之间转换。([德州仪器](https://www.ti.com/lit/gpn/SN74AVC32T245?utm_source=chatgpt.com "SN74AVC32T245 32-Bit Dual-Supply Bus Transceiver ..."))

如果用 16bit translator：

```text
168 / 16 = 10.5
实际需要 11 颗 16bit translator
```

SN74AVC16T245 这类 16bit 器件支持 1.2V 到 3.6V，并且通过 DIR/OE 控制方向和隔离。([德州仪器](https://www.ti.com/lit/gpn/SN74AVC16T245?utm_source=chatgpt.com "SN74AVC16T245 16-Bit Dual-Supply Bus Transceiver with ...")) Nexperia 74AVC16T245 也是 16-bit dual-supply translating transceiver，可拆成两个 8-bit transceiver，每组有 OE 和 DIR。([Nexperia](https://www.nexperia.com/group/74avc16t245?utm_source=chatgpt.com "74AVC16T245 - 16-bit dual supply translating transceiver ..."))

但我不推荐把它作为首选，因为 6 颗 32bit translator 仍然会带来：

```text
DIR/OE 分组复杂
布线扇出复杂
时序 skew
上电/掉电隔离
热插拔保护
串扰和 SI
维护成本
```

---

## 对你这个场景的核心判断

你现在的问题不应该定义成：

```text
怎么给 168 个 pin 做 1.2V/1.8V 电平转换？
```

而应该定义成：

```text
为什么需要让主 FPGA 直接暴露 168 个可变电平 CMOS pin？
这些 pin 能不能被接口标准化、模块化、寄存器化、串行化？
```

## 我会建议你这样选

### 如果 168 路里面大部分是低速 GPIO / 控制 / 状态

用 **IO bridge / 小 FPGA / CPLD**。

```text
外部 168pin → IO bridge
IO bridge → A5E 用固定电平、少 pin 数接口
```

这是最有工程价值的。

---

### 如果 168 路是高速并口，必须低延迟同步

优先不要做运行时 1.2V/1.8V 兼容。应该改接口规范：

```text
连接器侧固定 1.2V 或固定 1.8V
不支持两种 VDDIO 自动切换
```

高速并口再加大规模 translator，时序和一致性风险很高。

---

### 如果外部设备不可改，主板也必须兼容

做 **适配板**，不要污染主板。

```text
主板接口固定
不同外设用不同适配板
```

---

### 如果以上都不能改

再退而求其次：

```text
6 颗 32bit dual-supply bus transceiver
按方向分组
DIR/OE 由 FPGA 状态机统一管理
外设侧 VCCB 跟随 VDDIO_EXT
默认 OE 关闭
VDDIO 稳定后再开通
```

## 一句话结论

**168 路可变 1.2V/1.8V CMOS，不建议主板上一对一电平转换。最好的方案是：连接器电平标准化；其次是适配板；再次是 IO bridge/小 FPGA 收敛协议；最后才是 32bit translator 堆 6 颗。**
</file>
<file path="Daily/raw/2026-05-13/5月13日_extracted/UIMAN.md">
eDP / DP AUX 的规范不是直接写“1.000 MHz ± x%”，而是定义 **Manchester transaction unit interval (UI)**：

UI_{MAN}=0.4\sim0.6\ \mu s

TI 文档（基于 DP v1.4a / eDP v1.4b）表 3-1 明确给出：  
`UI_MAN = 0.4 ~ 0.6 us`，典型值 `0.5 us`。

对应关系：

```text
UI_typ = 0.5 us
→ Manchester 半周期 typ = 0.5 us
→ 完整 bit typ = 1 us
→ typ data rate = 1 Mbps
```

因此容差实际上是：

```text
UI 容差：±20%
0.5 us ±20%
```

换算成 bit rate：

Bit\ Rate=\frac{1}{2\times UI_{MAN}}

得到：

```text
UI = 0.4 us → bit time = 0.8 us → 1.25 Mbps
UI = 0.6 us → bit time = 1.2 us → 0.833 Mbps
```

也就是：

```text
AUX 有效数据率允许范围：

0.833 Mbps ~ 1.25 Mbps
（相对 1 Mbps 为 ±20%）
```

所以你图里的：

```text
885 kHz
```

如果这是 SYNC 区看到的 Manchester 翻转频率，本质对应 UI ≈ 0.565 us：

UI\approx\frac{1}{2\times885kHz}\approx0.565\ \mu s

这个仍然落在：

```text
0.4 ~ 0.6 us
```

规范范围内。
</file>
<file path="Daily/raw/2026-05-13/5月13日_extracted/aux周期 ±20%裕量允许.md" tags="#正确 #可入知识库">

#正确 #可入知识库
**UIMAN = Manchester Transaction Unit Interval**，就是 AUX Manchester 编码里的**最小时间单元**，可以理解成“半个 Manchester bit 的宽度”。

规范表述是：

```text
UIMAN = 0.4 ~ 0.6 us
典型值 = 0.5 us
```

这来自 TI 基于 DP v1.4a / eDP v1.4b 整理的 AUX 电气规格表。

所以关系是：

```text
1 个 Manchester bit = 2 个 UIMAN

UIMAN 典型 0.5 us
→ 1 bit = 1.0 us
→ 数据率 = 1 Mbps
```

因此 **1 MHz 只是典型值，不是必须死卡 1.000 MHz**。

真正要满足的是：

```text
UIMAN 在 0.4 ~ 0.6 us
```

换算成你在 SYNC 区看到的方波频率：

```text
UIMAN = 0.4 us → SYNC 方波频率约 1.25 MHz
UIMAN = 0.5 us → SYNC 方波频率约 1.00 MHz
UIMAN = 0.6 us → SYNC 方波频率约 0.833 MHz
```

所以你测到：

```text
885 kHz
```

对应：

```text
周期 ≈ 1 / 885 kHz ≈ 1.13 us
半周期 ≈ 0.565 us
```

这个半周期就是 UIMAN，**0.565 us 在 0.4~0.6 us 范围内，因此从频率角度看是合格的。**

但不能只看平均频率，还要看：

```text
1. 每个 UI 是否都在 0.4~0.6 us
2. 周期抖动是否过大
3. START / STOP 特殊符号能否识别
4. AUX+ / AUX- 极性是否正确
5. 幅度、共模、电容、终端是否满足 AUX 电气要求
```

一句话：**AUX 不要求严格 1 MHz；1 MHz 是典型值。判定时优先看 UIMAN 是否在 0.4~0.6 us。**
</file>
<file path="Daily/raw/2026-05-13/5月13日_extracted/eDP v1.4b 的常规 AUX 曼切斯特编码.md">
关键结论：**eDP v1.4b 的常规 AUX 解析，按 DP/eDP AUX 的 Manchester-II、1 Mbps、半双工差分控制通道来解析。不是 Main Link 的 8b/10b，也不要把它当普通 UART/SPI。** TI 的 DP/eDP 调试应用笔记明确说明其内容基于 **DP v1.4a / eDP v1.4b**，并说明 AUX 使用半双工、Manchester-II transaction format。([德州仪器](https://www.ti.com/lit/pdf/SDAA295 "Debugging Methodology for DisplayPort/Embedded DisplayPort Link Training Utilizing the Auxiliary Channel"))

## 1. 曼切斯特编码到底怎么判

按 **AUX+ 单端视角**看，Manchester-II 的 bit cell 是这样：

```text
bit 0：L -> H   中间跳变上升沿
bit 1：H -> L   中间跳变下降沿
```

强证据是 VESA DP 规范文本里对 SYNC 的定义：SYNC 以连续 0 开始，而连续 0 在 Manchester-II 中表现为“每个 bit period 中间 L 到 H 跳变”。这等价于确认 **0 = L→H**。([glenwing.github.io](https://glenwing.github.io/docs/DP-1.0.pdf "VESA DisplayPort Standard Version 1.0"))

所以解码时不要看“边沿个数”简单判断 0/1，而是先锁定 bit cell：

```text
半 UI 约 0.5 us
1 bit ≈ 1 us

LH = 0
HL = 1
HH / LL = 非法 Manchester；通常用于 SYNC END / STOP 这类特殊序列
```

AUX 的 UI 规范给的是 **0.4 / 0.5 / 0.6 us**，也就是半 bit nominal 0.5 us；规范说明这个 UI 对应约 1 Mbps，并包含 Manchester-II 编码开销。([glenwing.github.io](https://glenwing.github.io/docs/DP-1.0.pdf "VESA DisplayPort Standard Version 1.0"))

## 2. 为什么你看到的频率可能不是“标准 1 MHz”

AUX 是 **1 Mbps 数据率**，不是一个固定 1 MHz 方波。

连续相同 bit，例如 `0000`：

```text
0 = LH | 0 = LH | 0 = LH
```

边界处也会跳变，所以边沿间隔可能接近 **0.5 us**。

交替 bit，例如 `0101`：

```text
0 = LH | 1 = HL | 0 = LH
```

bit 边界处可能没有跳变，所以边沿间隔可能接近 **1 us**。

因此示波器/逻辑分析仪上看到的“频率”不是一个稳定值。正确做法是：**用 SYNC 前导锁 half-UI，再按 bit cell 解码**，而不是直接用测频功能判断 AUX 是否正常。

## 3. AUX 一帧怎么找

一个 AUX transaction 大致是：

```text
Idle / Precharge
SYNC 前导
SYNC END / START
Command / Address / Length / Data
STOP
Turnaround
Reply SYNC
Reply Command / Data
STOP
```

面向 DP/eDP 1.4a/1.4b 的 TI 文档说，AUX 是半双工，数据传输严格符合 Manchester-II transaction format；SYNC 用于帧起始识别，包含 **16 到 32 个连续逻辑 0** 的 Manchester-II 编码。([德州仪器](https://www.ti.com/lit/pdf/SDAA295 "Debugging Methodology for DisplayPort/Embedded DisplayPort Link Training Utilizing the Auxiliary Channel"))

VESA DP 基础规范里也有同样的底层规则：AUX 是一对差分线、半双工、约 1 Mbps，并使用 Manchester-II 自时钟传输。([glenwing.github.io](https://glenwing.github.io/docs/DP-1.0.pdf "VESA DisplayPort Standard Version 1.0"))

## 4. SYNC / STOP 的关键特征

正常数据区只应该出现 `LH` 或 `HL` 这种 Manchester bit cell。

而 SYNC END / STOP 是故意做成 **非法 Manchester**，方便接收端识别边界：

```text
AUX+：高电平保持 2 bit period
然后：低电平保持 2 bit period
AUX-：相反极性
```

VESA 规范对 STOP 的描述也是：AUX-CH+ 先 H 保持 2 bit period，再 L 保持 2 bit period，这是 Manchester-II 的非法序列；STOP 后立即释放 AUX CH。([glenwing.github.io](https://glenwing.github.io/docs/DP-1.0.pdf "VESA DisplayPort Standard Version 1.0"))

所以你在波形里要重点找：

```text
连续 0 的 SYNC：LH LH LH LH ...
然后突然出现：HHHH LLLL 这种长保持
后面才是真正的 Command / Address / Data
```

这里的 `HHHH / LLLL` 是按 half-UI 展开的近似表达。

## 5. Command / Address / Data 如何解析

Native AUX Request 的字段格式是：

```text
SYNC
COMM[3:0] | ADDR[19:16]
ADDR[15:8]
ADDR[7:0]
LEN[7:0]
DATA[0] ... DATA[N]
STOP
```

Reply 的基本格式是：

```text
SYNC
COMM[3:0] | 0000
DATA[0] ... DATA[N]
STOP
```

VESA 规范列出了这个 Native AUX Request / Reply transaction syntax，并说明 burst data 最大 16 bytes。([glenwing.github.io](https://glenwing.github.io/docs/DP-1.0.pdf "VESA DisplayPort Standard Version 1.0"))

Command 粗略判断：

```text
Native AUX：
bit3 = 1
bits[2:0] = request type
000 = Write
001 = Read

I2C-over-AUX：
bit3 = 0
bit2 = MOT
bits[1:0] = I2C command
00 = Write
01 = Read
10 = Write Status Request
```

TI 的 AUX transaction 说明也按这个方式区分 Native AUX 和 I2C-over-AUX。([德州仪器](https://www.ti.com/lit/pdf/slla680 "Using DS90LV047-48EVM for Capturing DisplayPort AUX Channel"))

## 6. 极重要：差分极性会影响你看到的 0/1

AUX 本身是差分对。你用 DS90LV019 / LVDS 接收器 / 差分转单端后，逻辑分析仪看到的是“某个极性的单端结果”。

如果 AUX+ / AUX- 接反，`LH` 和 `HL` 会互换，SYNC END / STOP 也会变得不像标准序列。TI 的调试文档明确提醒：极性正确时每个 AUX transaction 会包含 SYNC END/START 和 STOP；极性反了则看不到正确的 SYNC END/START 或 STOP 形态。([德州仪器](https://www.ti.com/lit/pdf/SDAA295 "Debugging Methodology for DisplayPort/Embedded DisplayPort Link Training Utilizing the Auxiliary Channel"))

现场判断方式很简单：

```text
能稳定看到连续 0 前导：
LH LH LH LH ...

并且后面有明显的非法 Manchester 长保持：
H 保持约 2us，L 保持约 2us

=> 极性大概率正确
```

如果看到的是相反形态，先尝试把逻辑分析仪通道反相，或者确认差分接收器 A/B 输入是否接反。

## 7. 实测抓波形建议

建议这样抓：

```text
采样率：≥ 20 MS/s，最好 50 MS/s 以上
先只看单端转换后的 AUX_RX
触发：AUX 活动边沿 / SYNC 连续跳变
先找 SYNC，不要直接从随机边沿开始解码
先确认 half-UI ≈ 0.5us，再解 bit
```

TI 的应用笔记也采用“差分转单端后给逻辑分析仪/协议分析”的思路，因为 DP/eDP AUX 是差分信号，普通单端工具直接抓不方便。([德州仪器](https://www.ti.com/lit/pdf/SDAA295 "Debugging Methodology for DisplayPort/Embedded DisplayPort Link Training Utilizing the Auxiliary Channel"))

## 8. 一句话给研发群

可以这样说：

> eDP AUX 常规通道按 Manchester-II 解析，约 1 Mbps、半双工差分。按 AUX+ 极性看，0 是 bit 中间 L→H，1 是 H→L；SYNC 是连续 0，随后有非法 Manchester 的 SYNC END/START，STOP 也是非法 Manchester 长保持序列。调试时先锁 0.5us half-UI 和 SYNC，不要直接把示波器测到的边沿频率当 AUX bit rate。
</file>
