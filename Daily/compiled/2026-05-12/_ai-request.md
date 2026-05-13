# AI Sync Request - 2026-05-12

## 使用说明

复制本文件全部内容，粘贴给 AI。

AI 输出后建议保存为：
- `Daily/compiled/2026-05-12/_cyberlog.md`
- `Daily/compiled/2026-05-12/_tomorrow-boot.md`
- `Daily/compiled/2026-05-12/_ai-output-audit.md`

请先审核 AI 输出，不要让 AI 覆盖任何非下划线开头的原始 notes。

## Codex / Agent 执行模式

如果你是 Codex、agent，或者任何可以读写此仓库文件的 AI，请默认完整处理，不要只返回文本答案：

1. 读取本 request、同目录 `_ai-audit.md` 和 `_ai-context.md`。
2. 生成并保存 `Daily/compiled/2026-05-12/_cyberlog.md`。
3. 生成并保存 `Daily/compiled/2026-05-12/_tomorrow-boot.md`。
4. 生成并保存 `Daily/compiled/2026-05-12/_ai-output-audit.md`，说明是否发现误读草稿状态、混入被排除目录、把推断升级成事实等问题。
5. 不覆盖任何非 `_` 开头的原始 notes。

只有在没有文件写入能力时，才把结果完整输出到聊天窗口。

## Prompt

# Daily Cyberlog / 工作画布 AI Sync Prompt

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

# Cyberlog — 2026-05-12

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

# Tomorrow Boot Packet — 2026-05-13

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

## Historical Context

以下内容来自同目录 `_ai-context.md`。它只用于识别跨日连续性和重复 blocker，不是今天的 raw evidence。

# AI Historical Context - 2026-05-12

This file is generated from previous compiled outputs. It is context only, not today's raw evidence.

## Boundary

- Use this context to detect continuity, repeated blockers, and yesterday's intended boot path.
- Do not treat historical context as proof that something happened today.
- Today's raw evidence remains `_ai-feed.md`.

## Warnings

- Missing historical context: Daily/compiled/2026-05-10/_tomorrow-boot.md

## Sources

<context role="previous-day-cyberlog" date="2026-05-11">
<file path="Daily/compiled/2026-05-11/_cyberlog.md">
# Cyberlog - 2026-05-11

## 1. 今日真实推进

- A38 / DF108 Agilex 5 原理图设计节奏被拆成 4 天计划：Day 1 做系统框图、电源树、FPGA 主芯片分页和 GPIO bank 分配；Day 2 做两组 LPDDR5 x32 颗粒选型、封装、LPDDR5 模块原理图和 EMIF pin assign；Day 3 做电源口、系统电源及时序、clock/reset/config、外设；Day 4 按 checklist 检查全图，重点看 Pin Plan / EMIF / power sequence。来源：`A38 + Agilex5方案原理图设计规划.md`
- A5ED052AB32AE2V 的 VCC/VCCP 供电方案有实质推进：形成 SmartVID / PMBus 设计方向，建议建立 `A5E_VCC_VID` 可调核心电源轨，VCC/VCCP 接同一 SmartVID rail，初始 0.80V，默认 PMBus Master Mode，`CF109/SDM_IO14` 接 `PWRMGT_SCL`，`CF99/SDM_IO11` 接 `PWRMGT_SDA`，`AV72/VCCLSENSE` 和 `AU72/GNDSENSE` 做 remote sense。来源：`SmartVID PMBus.md`, `a5ed052a_b32a_vcc_smartvid_power_design_report_zh.md`
- A5ED052A B32A 的参考原理图体系被整理：Altera 官方 065B SOM、KEIm A5E SOM、Sulfur Type-A carrier、065A Premium Devkit 各自适用边界被区分。结论是 pin/ball 以 A5ED052A B32A 官方 pinout 为准，065B/065A/KEIm 只能作为同封装或同系列设计参考，不能直接照抄电流能力、PMBus 主控关系或所有 rail 规划。来源：`a5ed052a_b32a_vcc_reference_schematic_summary_zh.md`, `draft/agilex b32a 参考图.md`, `draft/LTC7883 + LTC7050.md`, `draft/电源设计.md`
- SDM / 启动配置页推进：A5ED052A/A5ED065B B32A 外部 QSPI 启动建议使用 AS x4 Normal mode，`MSEL[2:0]=011`，并整理了 AS_CLK、AS_DATA[3:0]、AS_nCSO0、AS_nRST、nCONFIG、nSTATUS、CONF_DONE、INIT_DONE、OSC_CLK_1、RREF_SDM 的连接建议。来源：`A5ED065B B32A启动配置.md`, `A5ED065B B32A SDM  与 XCKU 配置区功能对比.md`, `Agilex5和XCKU的SDM对比.md`
- SDM 基础约束被澄清：`RREF_SDM/CL103` 应通过 2.00k 1% 接 GND，不可当 GPIO、不可悬空；`OSC_CLK_1/BR102` 建议用 125MHz / 1.8V LVCMOS free-running oscillator，不建议用 20MHz。来源：`RREF_SDM.md`, `SDM系统时钟选择.md`
- LPDDR5 寻样问题被重新整理成采购和项目决策 brief：当前 2GB / 16Gb x32 长生命周期料号未找到，美光 `MT62F1G32D2DS-020 WT:D` 可作为主线候选但属于 4GB / 32Gb x32 LPDDR5X，仍未冻结；三星 245FBGA 消费类不作为主推，三星 315FBGA x32 32Gb 路线仍可并行确认，南亚关闭，Henry/Hynix 等待补证。来源：`a5ed065b_b32a_lpddr5_sourcing_brief.md`
- 一个新的器件口径风险被明确写出：`A5ED065B B32A` 在当前工作区、本地资料和 daily 历史中未找到足够证据，不能把既有 `A5EC052A/A5ED052A B32A` 的 pin assign、bank 2A/2B、EMIF 结论直接迁移到 `A5ED065B B32A`。来源：`a5ed065b_b32a_lpddr5_sourcing_brief.md`
- LPDDR5 内部群沟通和供应商/原厂回复草稿形成：内部要确认 FPGA 最终型号、是否接受 4GB x32 两颗导致总容量 8GB、是否只选普通 LPDDR5、`16bit die` 是否硬性要求、短生命周期料号接受边界、逻辑侧是否能跑 Quartus EMIF / Pin Planner / Fitter；对外要求供应商推荐普通 LPDDR5、单颗 4GB / 32Gb、x32 package width、16bit die / die organization、生命周期、替代料和交期。来源：`a5ed065b_b32a_lpddr5_internal_supplier_drafts.md`
- A38/A57 + Agilex 5 DDR / LPDDR5 架构沟通稿形成：原 DF108 DDR4 方案约 153.6Gbps 理论带宽；当前 LPDDR5 两颗 x32、约 3733MT/s 时理论约 239Gbps、总容量 8GB；A57 场景下 LPDDR5 方案约 14 组 MIPI，DDR5 方案约 16 组 MIPI、约 173Gbps 理论带宽。来源：`lpddr5 群内沟通.md`, `群内沟通 lpddr.md`
- eDP HBR3 眼图标准形成知识结论：eDP 1.4b / HBR3 / 8.1Gbps 接收端建议以附件 eDP v1.4b 为主，TP3_EQ 最低判断为 75mVpp differential / 0.5UI，更稳妥目标为 90mVpp differential / 0.5UI；普通 DP RX 的 75mV / 0.35UI 不作为 eDP v1.4b 主结论。来源：`eDP眼图.md`, `eDP眼图标准.md`

## 2. 当前工作画布

### Active

- A38 / DF108 Agilex 5 原理图首版：当前工作重心从 LPDDR5 pin/net 单点推进扩展到最小系统页、电源树、SmartVID、电源时序、SDM/QSPI、clock/reset/config 的整体闭环。
- A5ED052AB32AE2V SmartVID 电源：已形成推荐架构，但 regulator 选型、PMBus address/PAGE/format、EPE/Power Analyzer 电流预算、PDN 和 FAE 确认仍未闭环。
- A5ED052A/A5ED065B B32A SDM/config 页：AS x4 Normal、MSEL、RREF、OSC_CLK_1、JTAG、nCONFIG/nSTATUS/CONF_DONE/INIT_DONE 已有工作表和连接建议。
- A38/A57 LPDDR5/DDR5 方案决策：当前不是单纯选颗粒，而是项目容量、MIPI 通道数量、HSIO bank、内存带宽、供应链和控制器复杂度的联合取舍。
- A57 eDP 眼图标准：今天主要推进的是测试判据和标准解释，不是现场根因闭环。

### Queue

- 把 A5ED052AB32AE2V SmartVID FAE 问题清单发出，并要求 FAE 给官方 regulator 推荐、Quartus 设置、PDN checklist 和参考设计依据。
- 建立 A5ED052A vs A5ED065B 的器件证据包：ordering code、官方 pinout、package、power option、EMIF 支持、reference schematic、Quartus device support。
- 用最终 FPGA 型号 + 候选 LPDDR5 料号跑 Quartus EMIF / Pin Planner / Fitter 最小验证。
- 把内部 LPDDR5 沟通稿和供应商邮件从 draft 变成明确的 `sent` / `waiting-feedback` / `confirmed` 状态记录。
- 用 eDP 1.4b HBR3 判据回填实际眼图数据，形成 pass/fail 表。

### Blocked

- SmartVID regulator 冻结：阻塞原因是当前只形成设计建议，尚无 FAE 对 regulator 优先级、PMBus mode、address/PAGE/voltage format、Quartus 支持和 NVM 初始电压的正式确认；解除方式是发出 FAE 问题并归档回复；owner：硬件 / FAE；下一步：发送 `A5ED052AB32AE2V SmartVID/PMBus 电源方案` 问题清单。
- A5ED065B B32A 口径迁移：阻塞原因是今天 brief 明确写到本地未找到 `A5ED065B B32A` 的既有证据；解除方式是确认最终 FPGA ordering code，并拉取对应官方 pinout / package / EMIF / power 文档；owner：项目 / 硬件 / FAE；下一步：先确认 A5ED065B 是否是最终目标型号或只是口误。
- LPDDR5 料号冻结：阻塞原因是 2GB / 16Gb x32 长生命周期候选缺失，主线美光为 4GB / 32Gb x32 LPDDR5X，而今天对外草稿又提出“普通 LPDDR5、不要 LPDDR5X、16bit die”的新约束，约束间存在冲突；解除方式是项目确认容量/协议/封装/生命周期优先级，供应商按表格正式回复；owner：项目 / 采购 / 硬件；下一步：把冲突项列成决策表。
- LPDDR5 FPGA 端可行性：阻塞原因是尚未看到最终 FPGA 型号 + 候选颗粒的 Quartus EMIF / Pin Planner / Fitter 输出；解除方式是逻辑侧跑最小工程并输出报告；owner：逻辑 / FAE；下一步：以最终型号为前提建立 test-fit。
- A57 eDP 根因：阻塞原因是今天只有标准判据整理，没有新的实测眼图、寄存器、MODE 或多板矩阵闭环；解除方式是把实际眼图数据套入 eDP 1.4b HBR3 判据，并与历史 MODE/多板数据合并；owner：硬件 / 软件 / 测试；下一步：收集 TP3_EQ / RX_EQ 测量数据。

### Closed

- AS x4 Normal mode 的启动配置建议已形成：`MSEL[2:0]=011`，单 flash 下 MSEL0/1 上拉、MSEL2 下拉。
- `RREF_SDM/CL103` 的处理已明确：2.00k 1% 到 GND，不可复用为 GPIO。
- `OSC_CLK_1/BR102` 的首选方向已明确：125MHz / 1.8V free-running oscillator；20MHz 不建议。
- A5ED052A B32A SmartVID 设计方向已从“是否需要 PMBus”推进到“需要 FAE 确认具体 regulator 和 Quartus 参数”的阶段。
- eDP 1.4b HBR3 接收端眼图主判据已明确为 75mVpp / 0.5UI，90mVpp / 0.5UI 可作为更稳妥目标。

## 3. 关键决策

| 决策 | 背景 | 理由 | 风险 | 后续动作 | 来源文件 |
|---|---|---|---|---|---|
| A5ED052AB32AE2V 的 VCC/VCCP 按 SmartVID / PMBus 可调 rail 设计，不按普通固定 0.8V buck 处理 | 目标器件为 `A5ED052AB32AE2V`，记录中判断其属于 -2V SmartVID 器件 | raw 中多份报告都指向 VCC/VCCP 需要 PMBus-compliant regulator，且不建议 fixed-output regulator | 该结论仍需 FAE 对具体 ordering code 和项目 Quartus 版本确认 | 发送 FAE 问题清单，归档正式回复 | `SmartVID PMBus.md`, `a5ed052a_b32a_vcc_smartvid_power_design_report_zh.md` |
| 本项目核心电源 rail 建议命名为 `A5E_VCC_VID`，VCC/VCCP 接同一 SmartVID rail | 需要避免把 SmartVID rail 误当普通 0.8V rail | 名称能表达 VID 可调和 PMBus 控制属性；参考设计也显示 VCC/VCCP 进入 VID rail | 其它 0.8V rail 是否可共轨未确认，不能无脑合并 | 单独确认 VCCL、VCCPLL、HSSI、PLL 等 rail-sharing 规则 | `a5ed052a_b32a_vcc_smartvid_power_design_report_zh.md` |
| 默认采用 PMBus Master Mode，`PWRMGT_ALERT/BR99` 先预留 | 当前没有明确外部电源管理 MCU 负责 VID 流程 | 最小系统中 SDM 做 PMBus master 更直接，Slave mode 需要外部 master、alert 和 firmware 时序 | 若后续系统管理架构改变，PMBus 拓扑要重评 | 让 FAE 确认 PMBus mode、ALERT 是否必需、level shift 和上拉策略 | `SmartVID PMBus.md`, `draft/smartvid方案.md` |
| Regulator 优先让 FAE 在 fully validated 器件中推荐；LTC7883 只作为参考设计路线，不直接冻结 | Altera 参考板和 KEIm 使用 LTC7883，但 raw 中也记录其为 API validated only | `TPS53676 / LTC3882-1 / ISL68223` 被整理为风险更低的 fully validated 路线 | 供应、成本、功率级和工程复用可能推动 LTC7883，但必须确认 Quartus/FAE 支持 | 要求 FAE 给推荐优先级和参数 | `a5ed052a_b32a_vcc_reference_schematic_summary_zh.md`, `draft/LTC7883 + LTC7050.md`, `draft/smartvid方案.md` |
| AS x4 Normal mode 采用 `MSEL[2:0]=011`，不默认选 AS Fast | 外部 QSPI flash 启动是当前配置方向 | AS Normal 风险低；AS Fast 对电源 10ms 稳定有更强约束 | 如果后续要求更快配置，需要重新评估电源稳定时间和 flash 能力 | 在原理图和 Quartus Device and Pin Options 中同步配置 | `A5ED065B B32A启动配置.md` |
| LPDDR5 不能写成已冻结，必须拆成供应商回复、容量接受、FPGA/逻辑验证三个 gate | 2GB x32 长生命周期候选缺失，美光 4GB x32 LPDDR5X 主线仍未冻结 | 这三个 gate 的 owner、输入和输出不同，合并会误导设计状态 | 若继续画图快于验证，可能造成封装、容量、协议和 pin list 级返工 | 做一张 gate 表并逐项标 `pending` / `accepted` / `rejected` | `a5ed065b_b32a_lpddr5_sourcing_brief.md` |
| eDP HBR3 判据优先使用 eDP 1.4b TP3_EQ 75mVpp / 0.5UI | 今天记录对多个来源进行了区分 | 普通 DP RX 75mV / 0.35UI 不应直接作为 eDP 1.4b 主结论 | 仍需将实际测试 setup、均衡条件和测量点对齐 | 用该判据复核实测眼图 | `eDP眼图.md`, `eDP眼图标准.md` |

## 4. 重要信息

- SmartVID 相关 pin：`CF109/SDM_IO14/PWRMGT_SCL`，`CF99/SDM_IO11/PWRMGT_SDA`，`BR99/SDM_IO12/PWRMGT_ALERT` 可选保留，`BP102/SDM_IO16/CONF_DONE`，`CA99/SDM_IO0/INIT_DONE`。
- Sense 相关 pin：`AV72/VCCLSENSE` 接 regulator remote sense positive，`AU72/GNDSENSE` 接 regulator remote sense negative / ground sense。
- A5ED052A B32A 报告列出的 VCC/VCCP 数量：`VCC` 41 个 ball，`VCCP` 14 个 ball；这些应接到 SmartVID 核心 rail，但其它低压 rail 需单独确认。
- AS x4 Normal QSPI 关键连接：`BK99/AS_CLK`、`BH99/AS_DATA0`、`BK102/AS_DATA1`、`CH99/AS_DATA2`、`CF102/AS_DATA3`、`CF112/AS_nCSO0/MSEL0`、`CA102/AS_nRST`。
- MSEL 建议：`CF112/MSEL0` 上拉，`BM99/MSEL1` 上拉，`BM102/MSEL2` 下拉，即 `MSEL[2:0]=011`。
- `OSC_CLK_1/BR102` 建议 125MHz / 1.8V LVCMOS free-running oscillator；`AS_CLK` 频率仍需按 flash 和 speed grade 设置，不等于一定 125MHz。
- `RREF_SDM/CL103` 使用 2.00k 1% 到 GND，电阻靠近 FPGA，走线短，不串测试点/跳线。
- A5ED052A / A5ED065B / A5EC052A 口径不能混用：今天材料明确要求最终以真实 ordering code 和官方 pinout 为准。
- LPDDR5 当前主线候选仍是美光 `MT62F1G32D2DS-020 WT:D`，但它是 4GB / 32Gb x32 LPDDR5X；今天对外草稿中“普通 LPDDR5、不要 LPDDR5X、16bit die”的要求会改变供应商搜索空间，需要项目确认。
- A38/A57 架构沟通中的关键数字：原 DDR4 理论约 153.6Gbps；两颗 x32 LPDDR5 约 239Gbps、总容量 8GB；DDR5 16bit+32bit 约 173Gbps；摄像头端从约 80Gbps 提升到约 128Gbps。
- eDP HBR3：8.1Gbps/lane，1UI 约 123ps；75mVpp / 0.5UI 对应约 61.5ps 眼宽。

## 5. 今日产出

- A38 / Agilex 5 4 天原理图推进计划：属于 A38/DF108 原理图管理；来源 `A38 + Agilex5方案原理图设计规划.md`；可复用价值是把首版原理图从单点 pin 绘制拉回到系统页、电源、配置和检查闭环。
- A5ED052A B32A VCC / SmartVID 供电设计报告：属于 A38/DF108 电源设计；来源 `a5ed052a_b32a_vcc_smartvid_power_design_report_zh.md`；可复用价值是能直接作为原理图评审和 FAE 问题包基础。
- A5ED052A B32A 可参考原理图 VCC / SmartVID 汇总：属于参考设计取证；来源 `a5ed052a_b32a_vcc_reference_schematic_summary_zh.md`；可复用价值是区分官方 065B SOM、KEIm、Sulfur carrier 的适用边界。
- SmartVID / PMBus FAE 沟通模板：属于外部确认；来源 `A5ED052AB32AE2V FAE 沟通.md`, `draft/smartvid方案.md`；可复用价值是能要求 FAE 明确 regulator、PMBus、sense、QSF/PDN checklist。
- SDM / QSPI / RREF / OSC_CLK 工作笔记：属于最小系统原理图；来源 `A5ED065B B32A启动配置.md`, `RREF_SDM.md`, `SDM系统时钟选择.md`；可复用价值是减少从 Xilinx 配置页迁移到 Agilex SDM 时的误接。
- LPDDR5 寻样 brief 和内部/外部沟通草稿：属于 A38/A57 memory 架构与采购；来源 `a5ed065b_b32a_lpddr5_sourcing_brief.md`, `a5ed065b_b32a_lpddr5_internal_supplier_drafts.md`；可复用价值是把供应链、容量、封装、die organization、逻辑验证拆成独立 gate。
- A38/A57 DDR/LPDDR5 方案群沟通稿：属于项目架构沟通；来源 `lpddr5 群内沟通.md`, `群内沟通 lpddr.md`；可复用价值是把 MIPI 数量、HSIO bank、带宽和容量取舍讲清楚。
- eDP 1.4b HBR3 眼图标准整理：属于 A57 eDP 测试判据；来源 `eDP眼图.md`, `eDP眼图标准.md`；可复用价值是后续实测眼图 pass/fail 的判断基线。

## 6. 未完成任务

| 任务 | 所属项目 | 下一步动作 | 优先级 | 是否适合交给 AI / agent | 为什么 |
|---|---|---|---|---|---|
| 确认最终 FPGA ordering code | A38 / DF108 | 明确到底是 `A5ED052AB32AE2V`、`A5ED065B B32A` 还是其它型号，并保存官方 pinout/package/power 文档 | P0 | 不完全适合 | AI 可整理差异表，最终型号必须由项目/FAE确认 |
| 发送 SmartVID / PMBus FAE 问题清单 | A38 电源 | 把 regulator、PMBus Master、VCC/VCCP 同 rail、sense、OSC、QSF/PDN checklist 问题发给 FAE | P0 | 适合起草 | 今日已有草稿，正式发送和确认需人工 |
| 选择 VCC/VCCP regulator | A38 电源 | 在 `TPS53676 / LTC3882-1 / ISL68223 / LTC7883` 中按 FAE、供应、电流和 Quartus 支持选型 | P0 | 部分适合 | AI 可做对比表，最终冻结要结合供应链和 FAE |
| 做 EPE / Quartus Power Analyzer 电流预算 | A38 电源 | 用实际资源、频率、温度和接口估算 `A5E_VCC_VID` 电流，不照抄参考板电流 | P0 | 部分适合 | AI 可生成输入清单，工具和参数由工程侧执行 |
| 建立 LPDDR5 决策 gate 表 | A38/A57 memory | 拆开供应商回复、容量接受、协议/封装约束、FPGA/逻辑验证、FAE review | P0 | 适合 | AI 可以直接生成表格模板 |
| 解决 LPDDR5 普通 LPDDR5 vs LPDDR5X 约束冲突 | A38/A57 memory | 明确是否真的排除 LPDDR5X；若排除，重新评估可采购性和生命周期 | P0 | 不完全适合 | 这是项目/供应链取舍，AI 可指出冲突 |
| 让逻辑侧跑最终 FPGA + 候选颗粒 EMIF / Fitter | A38/A57 memory | 生成最小工程、QSF、pin report、Fitter report，验证 two x32 / controller 方案 | P0 | 部分适合 | AI 可写 checklist，工具执行需逻辑侧 |
| 把群沟通稿标记成发送状态 | A38/A57 memory | 如果已发送，写入 `sent` note；如果未发送，保持 draft，不写成事实 | P1 | 适合提醒 | 这是 daily 边界问题，AI 可审计 |
| 用 eDP 判据复核实测数据 | A57 eDP | 收集 TP3_EQ / RX_EQ 眼图，按 75mVpp/0.5UI 和 90mVpp/0.5UI 两档判定 | P1 | 部分适合 | AI 可做判定表，测试数据需现场提供 |

## 7. 明日启动包

见 `Daily/compiled/2026-05-11/_tomorrow-boot.md`。

## 8. 工作流摩擦

- 现象：今天 raw 中包含正式报告、沟通草稿、AI 问答、参考设计分析和项目群文案，且 `draft/` 目录被合并进 feed。可能原因：为了快速整理方案，把工程证据和可复制草稿放在同一层。影响：容易把“可发送草稿”误读为“已发送/已确认事实”。明天修正动作：所有沟通稿在文件名或首行标 `draft` / `sent` / `waiting-feedback` / `confirmed`。
- 现象：`A5EC052A`、`A5ED052A`、`A5ED065B` 口径反复出现。可能原因：参考设计、历史工作表、供应链 brief 和目标器件升级混在一起。影响：pinout、EMIF bank、电源电流、参考图适用性都可能被错误迁移。明天修正动作：先冻结 ordering code evidence packet，再继续原理图扩面。
- 现象：LPDDR5 寻样约束存在冲突：当前主线候选是 LPDDR5X，而今天对外草稿要求普通 LPDDR5、不要 LPDDR5X、16bit die。可能原因：项目希望约束供应商回复，但未同步检查市场可得性。影响：供应商可能按不现实约束返回“无料”，或者与已评估候选断开。明天修正动作：把“必须条件”和“偏好条件”分开，不要把偏好写成硬门槛。
- 现象：参考原理图很多，但对应器件、开发板类型、PMBus 架构不同。可能原因：想快速复用官方/供应商设计。影响：可能照抄不适合本板的相数、电流能力、carrier PMBus 拓扑。明天修正动作：每张参考图只摘录可迁移项和不可迁移项。
- 现象：eDP 今天只推进了标准判据，没有连接到实际故障矩阵。可能原因：标准确认和问题排查被分开记录。影响：明天可能还是停留在“标准是什么”，没有转换为 pass/fail 证据。明天修正动作：建一个眼图测量结果表，列测试点、速率、均衡、眼宽、眼高、结论。

## 9. 自我迭代建议

1. 明天第一动作不是继续画图，而是先建 `A5ED052A/A5ED065B evidence gate`：最终 ordering code、官方 pinout、SmartVID regulator、PMBus mode、Quartus support、EMIF/Fitter，每一项只允许 `confirmed` / `pending` / `blocked` 三种状态。
2. 对所有供应商/FAE/项目群沟通稿，发送后必须补一条独立 raw note，写清 `sent_to`、`sent_time`、`waiting_for`、`expected_output`，否则 daily 只能把它们当草稿。
3. LPDDR5 决策表里新增一列 `hard constraint or preference`，把“普通 LPDDR5、非 LPDDR5X、16bit die、315-ball、4GB x32、5-8 年生命周期”逐项分级，避免把互相冲突的偏好同时发给供应商。

## 10. 规则候选

### 规则候选 1
- 触发条件：同一项目中出现多个相近 FPGA ordering code 或同封装不同 die 的参考设计。
- 规则：先建立器件证据包，明确 target device、reference device、哪些结论可迁移、哪些必须重验；未完成前不得冻结 pinout、power 或 EMIF 结论。
- 原因：同封装不代表同 die、同电源容量、同资源或同 Quartus 约束。
- 例子：今天材料同时出现 `A5EC052A`、`A5ED052A`、`A5ED065B`。
- 是否建议写入 System/workflow-rules.md：yes

### 规则候选 2
- 触发条件：把外部沟通文案、群内同步文案或邮件模板放入 daily raw。
- 规则：必须显式标注 `draft` / `sent` / `waiting-feedback` / `confirmed`；未标注的沟通内容默认只能作为草稿，不得写成已发送事实。
- 原因：daily feed 会把 raw 合并给 AI，不标状态会导致事实边界错误。
- 例子：今天的 FAE 沟通、LPDDR5 群内沟通和供应商回复内容都更像草稿/模板。
- 是否建议写入 System/workflow-rules.md：yes

### 规则候选 3
- 触发条件：供应链寻样条件同时包含容量、协议、封装、die organization、生命周期和替代料要求。
- 规则：先把条件拆成 `hard constraint`、`preference`、`open question`，再发给供应商；不能把互相冲突的偏好混成硬性要求。
- 原因：供应商会按硬性条件筛料，约束冲突会直接导致候选为空或回复不可用。
- 例子：当前主线候选是 LPDDR5X，但今天草稿又要求普通 LPDDR5、不要 LPDDR5X、16bit die。
- 是否建议写入 System/workflow-rules.md：yes
</file>
</context>
<context role="recent-tomorrow-boot" date="2026-05-09">
<file path="Daily/compiled/2026-05-09/_tomorrow-boot.md">
# Tomorrow Boot Packet - 2026-05-10

## 明日主线

- A38 / Agilex 5 LPDDR5：当前 two independent x32 + bank 2A/2B 继续作为主线，但 LPDDR5 原理图扩面暂停；先做 OrCAD 网络核对，再补 Quartus / Fitter / FAE 验证闭环。
- A57 / 984 eDP：围绕 MODE 三个 0V 和多板概率性异常收敛证据，优先做矩阵，不要继续沿用“后两通道问题”的旧框架。
- AU15P / Winbond Flash：先读取和解除 Flash lock/protection 状态，再继续 Vivado Program Configuration Memory Device。

## 背景

- A38 LPDDR5 当前工作假设是 A5EC052A B32A + 两颗独立 x32 LPDDR5，U_LPDDR5_0 -> IO96 bank 2A，U_LPDDR5_1 -> IO96 bank 2B。
- 今日记录显示 A38 LPDDR5 FPGA 端网络已经连接完成，并统计出 U0 63 个、U1 63 个、总计 126 个网络。
- 当前 pin/net 表来源是 Altera A5EC052A pinout、Agilex 5 EMIF LPDDR5 pin placement / data width mapping，以及 Micron / Antmicro 315-ball 参考。它是工作输入，不是最终签核。
- 架构评审后的执行决策：当前架构可作为主线，但状态必须标为 `schematic_connected`, `not_signoff`, `pending_quartus`, `pending_fae`, `pending_package_confirm`；“标准支持场景之一”不能当事实写入设计结论，必须等 Quartus / FAE 证据。
- A57 新增架构信息：eDP1/2 对应一颗 DS90UB984，eDP3/4 对应另一颗 DS90UB984。
- A57 多板测试显示 eDP1/2/3/4 都有概率异常，板间表现不同，目前没有一块板稳定 4 通道出图。
- A57 已完成或初步完成的排查：前后通道 SerDes 电路无差异；IIC 指令和 ini / 参数下发对比无问题；电源、PWDN、I2C 看起来没问题。
- A57 新疑点：三个 MODE 都是 0V，记录中判断软件侧没有处理。
- AU15P + W25Q256JWEIQ 和 AU15P + W25Q128JWSIQ 都固化失败；KU3P + W25Q256JWEIQ 可固化；失败报错指向 `0x0000` sector locked。

## 当前状态

- A38 原理图网络：FPGA 端 LPDDR5 网络已连接，但扩面暂停；需要 ERC / netlist / 数量核对。
- A38 pin assign：状态是 `schematic_connected` + `not_signoff`，缺 Quartus EMIF / Pin Planner / Fitter 和 FAE review。
- A38 memory-side ball：如果最终 LPDDR5 料号或封装不是当前参考的 Micron 315-ball 类封装，需要重核 memory-side ball mapping。
- A57 问题框架：已经不是单纯后两通道异常，而是多板、多通道、概率性异常。
- A57 当前最明确的新疑点：MODE 三个 0V。
- AU15P：失败现象清楚，但还缺 Flash status/protection register、unlock/erase 过程和完整工具日志。

## 第一动作

- 先做 A38 LPDDR5 原理图核对表：
  - U0 网络数应为 63。
  - U1 网络数应为 63。
  - 总网络数应为 126。
  - 每组分类核对 DQ、DMI、RDQS、WCK、CK、CS、CA、RESET_N、FPGA_RZQ、REFCLK_P/N。
  - 每组标注状态：`schematic_connected`、`not_signoff`、`pending_quartus`、`pending_fae`、`pending_package_confirm`。

完成这张表后，直接启动 Quartus 最小 EMIF/Fitter 验证并准备 FAE review 包；不要直接继续扩展 LPDDR5 原理图范围。

## 注意事项

- 不要把 Table 22 的 Pin Index 当成 LPDDR5 颗粒 ball。
- 当前两颗 x32 LPDDR5 场景使用 x32 column；不要误用 2 Channel x16 column。
- `FPGA_RZQ` 是 FPGA OCT 电阻脚，不是 LPDDR5 颗粒 ZQ。
- `REFCLK_P/N` 接 EMIF PLL reference clock，不接内存颗粒。
- 不要把“FPGA 端网络连接好了”写成“LPDDR5 pin assign 已签核”。
- 不要把“two independent x32 是标准支持场景之一”写成已确认事实；当前只能写成待 Quartus / FAE 验证的主线方案。
- 如果 8GB 容量不被接受，方向是找 2GB x32 / 16Gb x32 长生命周期料号或重评容量/位宽，不是换更大密度。
- A57 MODE 三个 0V 是强疑点，但还不能直接写成最终根因。
- AU15P 不要继续重复烧录；先读保护状态。

## 不要重复踩的坑

- 用 AI 生成的 CSV 代替 Quartus / Fitter / FAE 证据。
- 原理图扩面快于验证闭环，把小的 test-fit 风险放大成 126 网络级返工。
- 最终 LPDDR5 封装未定时，把参考 memory ballout 画成不可变事实。
- 用昨天的“后两通道异常”旧叙述覆盖今天的多板概率性事实。
- A57 测试表不区分已测 4 块、计划 6 块和待测 2 块。
- AU15P 只保存一句报错，不保存 status register 和 unlock 过程。

## 可以交给 AI / agent 的部分

- 生成 A38 LPDDR5 OrCAD 网络核对表。
- 生成发给 FPGA FAE 的 LPDDR5 topology / bank / package / QSF / Fitter review 问题清单。
- 把 A57 做成 6 板 x 4 eDP x 2 颗 984 x MODE / register / 出图状态矩阵。
- 生成 AU15P Flash lock 排查 checklist，包括 status register、BP/TB/CMP/SRP/WPS、unlock、erase、program 和日志字段。
- 审核 daily note 里哪些是 AI 生成建议、哪些是已完成事实。

## 必须由我亲自判断的部分

- A38 当前 bank 2A / 2B x32 方案是否继续作为原理图主线。
- 是否接受 LPDDR5 原理图扩面暂停，直到 Quartus / FAE 证据到位。
- A57 MODE 三个 0V 是否由软件配置、硬件拉电阻、采样时机或 DS90UB984 模式设置导致。
- AU15P 是否需要切换 Vivado 流程、改约束、换配置器件识别方式，或找芯片/板级支持。
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

## AI Feed

<file path="Daily/raw/2026-05-12/5月12日_extracted/A57 eDP DeBug最新状态.md">

目前现象是：正常不测时可以稳定出图，但用示波器表笔直接点 AUX 相关信号后，会干扰 AUX 通信，出现不出图。结合现象看，不出图大概率是 AUX 通信异常导致 EQ / CR 没完成。

前面讨论过 AUX_RX、AUX_TX、AUX_EN 的上下拉问题，也讨论过是否是 AUX_RX / AUX_TX 默认状态异常。但目前最有效的验证结果是：TX、RX 没有改动，只在 AUX_EN 上加了 4.7K 上拉后，再用探头测试，之前的不出图现象没有复现，RX 上原来的异常波形也消失了。当前已经循环测试 50 多次正常，后续跑了约 1 小时，重启测试也能稳定出图。

所以当前判断：问题重点不应先放在 AUX_RX / AUX_TX 本身，而是优先怀疑 AUX_EN 在 FPGA 初始化前后存在不确定状态或高阻风险。EN 外部 4.7K 上拉后，把默认状态固定下来，AUX 通信稳定性明显改善。

下一步建议先按 AUX_EN 外部 4.7K 上拉方向继续验证，TX/RX 暂时不要一起改，避免变量太多。同时需要确认几个点：第一，主板上 EN 上拉具体加在哪个位置；第二，实测电阻是否确实为 4.7K；第三，当前双方使用的 bit / bin / JTAG 烧录版本是否一致；第四，固件里 EN 在上电、配置、初始化阶段的默认电平是否确定；第五，AP 循环测试工具在不出图时是否一定会报采集错误。

目前建议的处理优先级是：先固定 EN 默认状态，再对比固件版本，最后再继续看 AUX_RX / AUX_TX 波形和解析层问题。
</file>
<file path="Daily/raw/2026-05-12/5月12日_extracted/A57 eDP 群对话内容整理.md">
AUX 不出图问题排查整理

一、问题现象

当前现象是：不测 AUX 信号时，系统可以正常出图；使用示波器表笔直接点测 AUX 相关信号时，会出现不出图。

不出图时，初步表现为 AUX 通信受到影响，导致 CR / EQ 没有正常完成，最终不出图。

涉及信号主要包括：

1. AUX_RX
2. AUX_TX
3. AUX_EN


二、测试方式问题

直接用示波器表笔点测 AUX_RX、AUX_TX、AUX_EN，可能会影响 AUX 正常通信。

因此后续测试不建议直接点原始管脚，优先考虑把相关信号引到测试点，或者在 AU15P / 主 FPGA 侧找合适的测试点再测。

当前需要确认是否有 3 个可用测试点，分别对应 AUX_RX、AUX_TX、AUX_EN。


三、AUX 编码与解析讨论

前期讨论中确认，AUX 通信按曼彻斯特编码理解。

AUX 解析过程中，会通过同步字判断频率，并根据曼彻斯特编码中的时钟信息确定采样点。

需要注意的是：

1. 同步阶段可以重新校正采样点；
2. 数据阶段不容易继续校正；
3. 如果频率或采样点漂移较大，数据阶段可能采偏；
4. 如果目标频率接近 800K，则应尽量保持稳定，避免解析偏移。

所以 AUX 不出图不只是“有没有频率配置项”的问题，也可能和波形稳定性、默认电平状态、采样点稳定性有关。


四、上下拉尝试过程

前面讨论过对 AUX_RX、AUX_TX、AUX_EN 做上下拉处理。

已知尝试包括：

1. AUX_RX 曾加过下拉；
2. 该下拉用于屏蔽两组 AUX_RX 上电为高的状态；
3. 但 AUX_RX 下拉没有明显效果；
4. 后续讨论过 AUX_RX、AUX_TX、AUX_EN 是否都需要加上拉。

中间也考虑过一种可能：示波器探头的寄生参数改变了信号默认状态，导致 AUX 通信异常。

同时，AUX_EN 在未使能阶段可能处于高阻态，因此 EN 默认状态是否确定，也成为一个需要重点确认的问题。


五、有效验证结果

后续实测中，TX 和 RX 没有改动，只对 AUX_EN 增加了 4.7K 上拉。

修改后观察到：

1. 再用探头测试时，之前的不出图现象没有复现；
2. RX 波形中原先的异常消失；
3. 循环测试 50 多次均能正常出图；
4. 继续跑约 1 小时，重启测试仍然稳定出图；
5. 之前约 10% 概率不出图的问题，在该测试条件下没有再出现。

当前最有效的实验变量是：AUX_EN 增加 4.7K 上拉。


六、当前记录结论

从当前测试结果看，问题重点暂时不应优先放在 AUX_RX / AUX_TX 本身，而应优先确认 AUX_EN 的默认状态。

AUX_EN 如果在 FPGA 上电、配置或初始化阶段没有确定电平，或者在未使能阶段处于高阻状态，就可能导致 AUX 通信状态不稳定。

增加 AUX_EN 4.7K 外部上拉后，EN 状态被固定，探头测试导致不出图的问题明显改善。


七、后续待确认事项

后续需要继续确认以下问题：

1. AUX_EN 4.7K 上拉在主板上的具体修改位置；
2. 实际焊接后，万用表测得的电阻是否确认为 4.7K；
3. 双方使用的 bit / bin / JTAG 烧录内容是否一致；
4. 中间是否存在 bin1 升级版本差异；
5. 当前板卡是否使用了相同固件版本；
6. AP 循环测试工具在不出图时是否一定会报采集错误；
7. AUX_EN 在 FPGA 上电、配置、初始化前后的默认电平状态；
8. 是否需要在固件中初始化 AUX_EN 为确定电平。


八、建议排查顺序

建议后续按以下顺序继续推进：

第一步，先固定 AUX_EN 默认状态，优先验证 4.7K 外部上拉方案。

第二步，确认双方固件版本、bit 文件、bin 文件、JTAG 烧录内容是否一致。

第三步，在变量受控的情况下，再继续观察 AUX_RX、AUX_TX、AUX_EN 的波形。

第四步，如果 EN 固定后问题仍复现，再继续深入 AUX 解析层，包括频率稳定性、采样点、同步阶段和数据阶段的解析偏移问题。

当前不建议 AUX_RX、AUX_TX、AUX_EN 同时大范围修改，避免引入过多变量，导致问题归因不清。
</file>
<file path="Daily/raw/2026-05-12/5月12日_extracted/GPIO统计.md">

整理版如下：

## A38 + A5EC052A_B32 低速 GPIO 需求与资源评估

### 1. GPIO 需求汇总

总需求：**205 个 GPIO**

|需求数量|来源/用途|VDDIO 要求|备注|
|--:|---|---|---|
|168|解码板|VDDIO 可配置 1.2V ~ 1.8V|主体 GPIO 需求|
|4|解码板相关电源 EN|3.3V|电源使能|
|14|PMU 板|3.3V|PMU 控制/状态|
|7|QSFP|3.3V|QSFP 相关控制信号|
|4|加密 / 注册芯片 I2C|3.3V|I2C 类低速接口|
|4|DEV ID|3.3V|板卡 ID 配置|
|4|外部扩展 IO，客户用|3.3V|预留扩展|

### 2. 需求分类

|类型|GPIO 数量|电平要求|
|---|--:|---|
|解码板主体 GPIO|168|1.2V ~ 1.8V|
|3.3V 低速控制 GPIO|37|3.3V|
|**合计**|**205**|—|

---

## A5E 剩余 GPIO 资源汇总

|GPIO 数量|来源|VDDIO 范围 / 特性|风险项|
|--:|---|---|---|
|120|HVIO Bank × 6|可调 1.2V ~ 3.3V|最适合承接 3.3V 低速 GPIO|
|26|HSIO Bank 2A|固定 1.2V|仅适合 1.2V 逻辑|
|24|HSIO Bank 2B、3A|同 LPDDR5 VDDIO 电压|独立 lane 的可用，共 2 lane|
|48|HSIO Bank 3B 右边 half|待确认|需确认 VDDIO / 复用限制|
|38|HSIO Bank 3B 左边 half|固定 1.2V|仅适合 1.2V 逻辑|
|0|GTS|—|不可用|

### 资源合计

|项目|数量|
|---|--:|
|A5E 可统计 GPIO 资源|256|
|低速 GPIO 总需求|205|
|理论余量|**51**|

---

## 初步结论

1. **总 GPIO 数量上是够的**：  
    A5E 可统计资源约 **256 个**，当前需求 **205 个**，理论余量 **51 个**。
    
2. **关键不是数量，而是电平分配**：  
    其中 **37 个 3.3V GPIO** 应优先放到 **HVIO Bank**，因为 HSIO 多数固定 1.2V 或跟随 LPDDR5 VDDIO，不适合直接接 3.3V。
    
3. **168 个解码板 GPIO** 如果能接受 **1.2V / 1.8V**，可以使用 HSIO + 部分 HVIO 组合承接。
    
4. 原表中“**168 个确认可用，剩余 88 个 OK**”对应的是：  
    **256 - 168 = 88**。  
    但如果按总需求 **205 个** 计算，实际余量应是：  
    **256 - 205 = 51**。  
    这个口径建议统一，避免后续沟通误解。
    

---

## 建议分配原则

|信号类型|优先使用资源|
|---|---|
|3.3V GPIO|优先 HVIO|
|1.2V GPIO|可使用 HSIO 固定 1.2V Bank|
|1.8V GPIO|优先确认 HVIO 或支持对应 VDDIO 的 Bank|
|LPDDR5 同电压 GPIO|仅用于能接受 LPDDR5 VDDIO 的低风险信号|
|客户扩展 IO|建议放 HVIO，兼容性最好|

最终建议把这句话作为结论：

> A5E GPIO 数量上满足当前 205 个低速 GPIO 需求，但需要重点确认 VDDIO 分配。37 个 3.3V 控制类 GPIO 建议优先放 HVIO；168 个解码板 GPIO 可根据 1.2V / 1.8V 电平要求分配到 HSIO 与 HVIO。当前理论余量约 51 个 GPIO。
</file>
<file path="Daily/raw/2026-05-12/5月12日_extracted/lpddr5沟通.md">
请协助同时评估 DDR4 / DDR5 / LPDDR4 / LPDDR5 四类存储方案。

主控为目标 FPGA / SoC 平台，具体厂商、平台系列和型号暂不披露。
本次只做存储器器件侧的成本、供货、生命周期和资料完整性评估。
最终主控兼容性由我方内部确认。

评估重点：
1. DDR4 / DDR5：优先推荐可组成 64bit 总位宽的 x16 或 x8 方案。
2. LPDDR4 / LPDDR5：优先推荐可组成 64bit 总位宽的 x32 package width 方案。
3. LPDDR 请明确 package width 和 die organization，不要只写 x32。
4. 商业级 / 工业级均可，但需要明确温度等级。
5. 如料号存在 NRND / EOL / LTB 风险，必须提供替代料号。
6. 如资料、官网、代理系统、原厂反馈存在冲突，请在备注中说明。


 生成物 URL：
  https://github.com/joyhpc/DF108-revision-workspace/blob/main/revisions/rev-20260506-df108-ku040-to-a5ed052ab32ae2v/02_design_evidence/a38_agilex5_high_speed_gpio_allocation_20260512.md

</file>
