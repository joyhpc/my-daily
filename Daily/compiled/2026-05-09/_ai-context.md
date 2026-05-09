# AI Historical Context - 2026-05-09

This file is generated from previous compiled outputs. It is context only, not today's raw evidence.

## Boundary

- Use this context to detect continuity, repeated blockers, and yesterday's intended boot path.
- Do not treat historical context as proof that something happened today.
- Today's raw evidence remains `_ai-feed.md`.

## Warnings

- Missing historical context: Daily/compiled/2026-05-06/_tomorrow-boot.md

## Sources

<context role="previous-day-cyberlog" date="2026-05-08">
<file path="Daily/compiled/2026-05-08/_cyberlog.md">
# Cyberlog - 2026-05-08

## 1. 今日真实推进

- A57 / 984 解码板 eDP 后两通道异常被重新整理成可执行排查计划：前 1、2 通道开关视频流测试 1000 次未出现问题；后两通道异常目前只基于 1 块板，不能判定为共性问题；上午讨论形成多板测试、IIC 指令对比、寄存器读取、上电时序测量、SerDes 电路差异确认 5 个排查项。来源：`Issue4.md`
- A57 Redriver 相关判断被收敛：控制波形前后通道一致，所以“控制波形差异”不是当前已知差异点；但 PWDN 实际电平仍未确认，不能排除 Redriver 相关问题。来源：`Issue4.md`
- 出现 AU15P 固件固化阻塞：固件烧录未完成，0x0000 地址被 lock，无法擦除和烧写；同样步骤在 KU3P 上没有问题。来源：`今日完成项.md`
- A38 / DF108 LPDDR5 采购寻样结论形成：未找到完全匹配 `2GB / 16Gb、x32、LPDDR5、商业级、未来 5-8 年无 EOL` 的料号；美光 `MT62F1G32D2DS-020 WT:D` 被整理为当前最明确的主候选，但它是 `4GB / 32Gb x32 LPDDR5X`。来源：`lpddr5_report_decision.md`, `lpddr5_report_procurement.md`
- A38 LPDDR5 供应商路线被分类：美光 4GB x32 LPDDR5X 作为主线推进；三星 Golden Supreme 反馈的 `K3KL8L80DM-TGCT` 245FBGA 消费类路线不作为主推；南亚路线关闭；Henry / HSRP 当前只见需求发出，未见回复。来源：`lpddr5_report_decision.md`, `lpddr5_report_engineering_evidence.md`
- A38 LPDDR5 对外/群内同步文案形成：建议采购继续跟进美光和三星 32Gb x32 料号，项目/罗奇军确认整板容量从 4GB 上浮到 8GB 是否可接受，吴志安协助做 Quartus EMIF / Pin Planner / Fitter 验证，硬件侧在验证完成前不冻结 LPDDR5 pin list。来源：`lpddr5 情况群内反馈 2.md`, `lpddr5 情况群内反馈.md`
- A38 LPDDR5 工程证据报告形成：整理了需求追踪、Gmail message evidence、PCN/EOL 风险、Quartus 验证建议和进入 pin list 冻结前的验收标准。来源：`lpddr5_report_engineering_evidence.md`
- A38 LPDDR5 pin placement 资料入口被定位：LPDDR5 pin assign / pin placement 规范在 Agilex 5 EMIF IP User Guide 的 Chapter 9.2.3 / 9.2.4；`altera-pbc-b32a-a5e.xlsx` 只是 package ball coordinate，不是 LPDDR5 pin assignment；开发板资料主要是 LPDDR4，不是当前需要的 LPDDR5 规范。来源：`LPDDR5 PIN ASSIGN.md`

## 2. 当前工作画布

### Active

- A38 / DF108 LPDDR5 选型与采购确认：当前主线是美光 `MT62F1G32D2DS-020 WT:D`，并保留三星 315FBGA x32 LPDDR5X 正式渠道作为并行确认方向。
- A38 LPDDR5 工程可行性验证：需要逻辑侧用候选料号做 Quartus EMIF / Pin Planner / Fitter 验证，硬件侧暂不冻结 pin list。
- A57 / 984 解码板 eDP 后两通道异常排查：需要先扩大样本量，再对比 IIC、寄存器、上电时序、SerDes 差异和 Redriver PWDN。
- AU15P 固件固化问题：当前卡在 0x0000 地址 locked，无法擦除和烧写。
- LPDDR5 采购/项目/逻辑/硬件群内同步：已有简版 action items，但原文未明确是否已经发送。

### Queue

- 给美光/WT 补充项目资料：终端客户、项目名称、应用、试产时间、量产时间、主芯片、年用量、每片用量。
- 催 Henry / HSRP 是否有 2GB x32 长生命周期 LPDDR5/LPDDR5X 或可替代 4GB x32 料号。
- 通过正式三星渠道确认 315FBGA、x32、32Gb LPDDR5X 料号的供货、价格、生命周期和样品情况。
- 把 A38 LPDDR5 候选料号转为逻辑侧 EMIF 验证输入表。
- 把 A57 Issue4 排查计划转为多板测试记录表和前后通道对比表。
- 同步远端 agent 更新到本地。来源：`Issue4.md` 中有该提醒，但缺少仓库、分支和目标路径信息。

### Blocked

- A38 LPDDR5 原始 2GB x32 方案：阻塞原因是当前供应商反馈没有长期稳定匹配料号，旧代 2GB x32 有 EOL / 停产风险；解除方式是接受 4GB x32 作为主评估方向，或让供应商提供非 EOL 的 2GB x32 正式替代；owner：采购 / 项目负责人；下一步：项目确认是否接受容量上浮。
- A38 LPDDR5 主候选生命周期和商务条件：阻塞原因是美光 `MT62F1G32D2DS-020 WT:D` 的生命周期、温度等级、价格、lead time、MOQ / MPQ 未正式确认；解除方式是采购向美光/WT/WPI 补充项目信息并获取正式回复；owner：采购；下一步：发送问题清单和项目信息。
- A38 LPDDR5 pin list 冻结：阻塞原因是 LPDDR5X 9600 降频到 3733 MT/s、x32 x2 组成 x64、bank/pin/byte lane/RZQ/refclk/PLL 与 MIPI/QSFP 共存都需要 Quartus 证据；解除方式是逻辑侧完成 EMIF / Pin Planner / Fitter 验证；owner：吴志安 / 逻辑侧待确认；下一步：选美光和三星各一个候选料号进入最小工程验证。
- A57 eDP 后两通道异常：阻塞原因是当前只有 1 块 984 解码板样本，IIC 指令、寄存器、上电时序、SerDes 差异、Redriver PWDN 实测都未反馈；解除方式是按 action items 输出实测结果；owner：软件侧 / 硬件侧 / 何鹏程 / 吴锋 / Candy 或罗奇军；下一步：先做多板复现确认和 PWDN 电平测量。
- AU15P 固件固化：阻塞原因是 0x0000 地址 locked，导致擦除和烧写失败；解除方式尚未记录；owner：未明确；下一步：记录烧录工具、器件型号、保护位/lock bit 状态、擦除命令和报错日志，并与 KU3P 成功流程逐项对比。

### Closed

- 南亚 LPDDR5 路线关闭：供应商反馈没有 LPDDR5。
- 三星 Golden Supreme 反馈的 245FBGA 消费类 `K3KL8L80DM-TGCT` 不作为 A38 主推料号：生命周期通常 2-3 年，不满足 5-8 年要求。
- 旧代美光 2GB x32 方向不应作为主线：已有 PCN/EOL 风险，不满足长期供货目标。
- `chatroom/未命名.md` 被排除在 daily feed 外，未用于本次整理。

## 3. 关键决策

| 决策 | 背景 | 理由 | 风险 | 后续动作 | 来源文件 |
|---|---|---|---|---|---|
| A57 后两通道异常暂不能判为共性问题 | 当前仅 1 块 984 解码板测试发现后两通道异常 | 样本量不足，吴锋也提醒需要先多测几块 | 如果直接按共性问题推进，可能误导软硬件排查方向 | 多测几块 984 解码板，记录是否复现、通道和条件 | `Issue4.md` |
| Redriver 控制波形差异暂不作为已知差异点，但 PWDN 仍要测 | Candy/罗奇军反馈 Redriver 控制波形前后一样 | 控制波形一致说明该项不是当前已知差异，但 PWDN 实际电平未确认 | 若跳过 PWDN，可能漏掉 Redriver 未使能或时序异常 | 何鹏程实测 Redriver PWDN 电平和测量时机 | `Issue4.md` |
| A38 LPDDR5 以美光 `MT62F1G32D2DS-020 WT:D` 作为主线评估 | 原 2GB x32 长生命周期料号未找到 | 美光给出明确 4GB x32 LPDDR5X 料号、datasheet/PCN 资料和项目资料需求 | 容量上浮、成本、降频、生命周期和封装仍未确认 | 采购获取正式回复，项目确认容量上浮，逻辑做 EMIF 验证 | `lpddr5_report_decision.md`, `lpddr5_report_procurement.md` |
| 不再把旧代 2GB x32 LPDDR5 作为唯一方案 | 美光旧代 2GB 相关料号存在 EOL/停产风险 | 与 5-8 年生命周期目标冲突 | 若项目坚持 2GB，供应链风险会成为设计风险 | 将 2GB x32 标为高风险或不可满足，除非供应商给出正式替代 | `lpddr5_report_decision.md`, `lpddr5_report_engineering_evidence.md` |
| 三星消费类 245FBGA 路线不作为主推，但三星正式 315FBGA x32 路线可继续并行确认 | 不同文件中分别记录了三星 245FBGA 反馈和公开 315FBGA 候选 | 245FBGA 消费类生命周期不匹配；315FBGA x32 料号仍需正式渠道核实 | 如果把“三星”整体关闭，可能漏掉可用正式渠道；如果不区分，可能误选消费类短生命周期料号 | 采购区分询问：关闭 `K3KL8L80DM-TGCT` 消费类路线，同时确认三星 315FBGA x32 32Gb 长生命周期路线 | `lpddr5_report_procurement.md`, `lpddr5 情况群内反馈.md` |
| LPDDR5 pin list 在 Quartus 验证前不冻结 | LPDDR5/LPDDR5X pin 分配影响 bank、byte lane、RZQ、refclk、MIPI/QSFP 共存和 PCB SI | 仅靠采购料号或 package ball coordinate 不能证明 FPGA 端可实现 | 先画死 pin 可能导致 Fitter 不过或 PCB 返工 | 逻辑侧输出 EMIF 配置、Pin Planner、Fitter、QSF / pin report | `LPDDR5 PIN ASSIGN.md`, `lpddr5_report_engineering_evidence.md`, `lpddr5 情况群内反馈 2.md` |

## 4. 重要信息

- 原 DF108 方案：最大线速 2.5Gbps/lane，摄像头端最大数据量约 80Gbps；4 颗 H5AN4G6NBJR DDR4，4Gb / x16 x4，总位宽 64bit，总容量 2GB，理论峰值带宽约 153.6Gbps。
- 当前 Agilex 方案：最大线速 4Gbps/lane，摄像头端最大数据量约 128Gbps；原计划 2 颗 LPDDR5，单颗 2GB / 16Gb x32，总位宽 64bit，总容量 4GB，按 3733MT/s 计算理论峰值带宽约 239Gbps。
- 若采用 32Gb / 4GB x32 颗粒，两颗组成 x64 后整板 LPDDR 容量会从 4GB 上浮到 8GB。
- 美光当前主候选：`MT62F1G32D2DS-020 WT:D`，LPDDR5X，4GB / 32Gb，x32，9600 Mb/s per pin，315-ball TFBGA DS。
- 三星公开候选方向在群内文案中被列出：`K3KL8L80QM-MFCT`、`K3KL8L80CM-MGCT`、`K3KL8L80DM-MFCU`、`K3KL8L80EM-MHCV`，但这些需要正式渠道确认生命周期、供货、价格和样品；不能直接当成已确认可用料号。
- 三星渠道已明确不匹配的具体料号是 `K3KL8L80DM-TGCT`，32Gb / x32 / 245FBGA / 7500 Mbps / Tc -25 to 85 C，消费类生命周期通常 2-3 年。
- 美光旧代 PCN/EOL 风险：`PCN 36290` 涉及 Y52P specific 315b packages，Published 2026-02-04，Last Order Date 2026-08-04，Last Ship Date 2027-02-04；邮件还引用 `PCN_36383`，涉及 Y52Q 315b x32 2GB SDP 等 EOL。
- LPDDR5 pin assign / pin placement 规范入口：`External Memory Interfaces (EMIF) IP User Guide Agilex 5 FPGAs and SoCs 817467_D842785.pdf`，重点是 Chapter 9.2.3 和 9.2.4。
- `altera-pbc-b32a-a5e.xlsx` 只是 package ball coordinate，不是 LPDDR5 pin assignment。
- A57 当前关键事实：前 1、2 通道开关视频流 1000 次未出问题；后两通道异常仅 1 块板样本；Redriver 控制波形已抓且前后一样；PWDN 为拉低使能但实际板上电平未确认。
- AU15P 固化问题的已知事实只有：0x0000 地址 locked，擦除和烧写失败；KU3P 同流程正常。项目归属、工具、具体芯片状态和报错日志未记录。

## 5. 今日产出

- A57 Issue4 排查计划：属于 A57 / 984 解码板；来源 `Issue4.md`；可复用价值是把后两通道异常拆成多板复现、IIC、寄存器、上电时序、SerDes、Redriver PWDN 六类证据。
- A38 LPDDR5 采购沟通报告：属于 A38 / DF108 Agilex 5；来源 `lpddr5_report_procurement.md`；可复用价值是给采购内部同步、美光邮件、三星回复和 Henry 催办提供文本基础。
- A38 LPDDR5 内部决策报告：属于 A38 / DF108 Agilex 5；来源 `lpddr5_report_decision.md`；可复用价值是明确主候选、美光/三星/南亚/Henry 路线判断和下一步 owner。
- A38 LPDDR5 工程证据报告：属于 A38 / DF108 Agilex 5；来源 `lpddr5_report_engineering_evidence.md`；可复用价值是支撑设计评审、风险登记和 Quartus / 原理图验证入口。
- A38 LPDDR5 群内同步文案：属于 A38 / DF108 Agilex 5；来源 `lpddr5 情况群内反馈.md`, `lpddr5 情况群内反馈 2.md`；可复用价值是把采购、项目、逻辑、硬件四方 action items 压缩成可同步版本。
- LPDDR5 pin placement 资料索引：属于 A38 / DF108 Agilex 5；来源 `LPDDR5 PIN ASSIGN.md`；可复用价值是避免把 package ball coordinate 或 LPDDR4 开发板资料误当 LPDDR5 pin placement 证据。
- AU15P 固化问题快照：来源 `今日完成项.md`；可复用价值是保留明天排查入口，但当前信息不足，需要补日志。

## 6. 未完成任务

| 任务 | 所属项目 | 下一步动作 | 优先级 | 是否适合交给 AI / agent | 为什么 |
|---|---|---|---|---|---|
| 确认是否接受 LPDDR5 容量从 4GB 整板上浮到 8GB 整板 | A38 | 项目/罗奇军评估成本、软件地址空间、启动初始化和功耗影响 | P0 | 不完全适合 | AI 可整理影响清单，最终取舍需要项目负责人判断 |
| 向美光/WT/WPI 补充项目信息并确认 `MT62F1G32D2DS-020 WT:D` | A38 | 发送生命周期、温度等级、lead time、价格、MOQ/MPQ、降频使用问题 | P0 | 适合起草 | AI 可生成邮件，采购需要实际发送和确认供应商回复 |
| 逻辑侧做 LPDDR5X 候选料号 Quartus EMIF 验证 | A38 | 选美光和三星各一个候选，输出 EMIF 参数、Pin Planner、Fitter、QSF / pin report | P0 | 部分适合 | AI 可整理输入参数和验收清单，Quartus 工程需逻辑侧执行 |
| 区分三星路线并继续正式渠道确认 315FBGA x32 料号 | A38 | 关闭 245FBGA 消费类主推，同时询问 315FBGA 32Gb x32 料号生命周期和样品 | P1 | 适合起草 | AI 可整理询问清单，正式渠道反馈需采购获取 |
| 催 Henry / HSRP 回复 | A38 | 询问是否有 2GB x32 长生命周期或 4GB x32 替代料号 | P1 | 适合起草 | AI 可生成催办邮件，采购执行 |
| 建立 A57 多板测试记录表 | A57 | 记录每块 984 解码板是否复现、复现通道、复现条件 | P0 | 适合 | AI 可生成表格模板，测试需软件/硬件执行 |
| 实测 Redriver PWDN 电平 | A57 | 确认 PWDN 是否按拉低使能要求工作，并记录测量时机 | P0 | 不适合执行 | AI 可提醒检查点，实测由硬件完成 |
| 对比前后通道 eDP IIC 指令和寄存器 | A57 | 输出差异表和异常位说明 | P0 | 适合整理 | AI 可整理对比模板，读取数据需软件侧提供 |
| 排查 AU15P 固化失败 | 未明确 / 固件烧录 | 补齐烧录工具、保护位、地址 lock、擦除命令、报错日志，并与 KU3P 成功流程逐项对比 | P0 | 部分适合 | AI 可生成排查 checklist，实际解除 lock 需要工具和硬件环境 |
| 同步远端 agent 更新到本地 | workspace / agent | 明确远端仓库、分支、目标路径和是否允许 pull/merge | P2 | 适合 | AI 可执行同步，但当前 daily note 未给出足够上下文 |

## 7. 明日启动包

见 `Daily/compiled/2026-05-08/_tomorrow-boot.md`。

## 8. 工作流摩擦

- 现象：A38 LPDDR5 资料中同时存在采购报告、工程证据报告、群内详细版和群内简版。可能原因：需要同时面向采购、项目、逻辑、硬件四类对象沟通。影响：容易把“内部判断”“可发送文案”“正式已发送结论”混在一起。明天修正动作：每个沟通文件头部加状态：draft / sent / waiting-feedback / confirmed，并标明受众。
- 现象：三星路线在不同文件里看似结论相反。可能原因：一个结论针对 Golden Supreme 的 245FBGA 消费类料号，另一个结论针对公开 315FBGA x32 料号和正式渠道确认。影响：如果不拆路线，会误判为冲突。明天修正动作：供应商矩阵按“厂商 + 具体料号 + 封装 + 渠道 + 生命周期状态”记录，不按厂商品牌粗粒度关闭。
- 现象：LPDDR5 采购选型、容量变更、EMIF 验证和原理图 pin list 冻结高度耦合。可能原因：存储器件从 2GB x32 转向 4GB x32 LPDDR5X 后，供应链选择直接影响工程实现。影响：任一环节未确认都会阻塞原理图冻结。明天修正动作：把 P0 分成三条并行线：采购正式回复、项目容量接受、逻辑 Quartus 验证。
- 现象：A57 Issue4 记录里包含同步文案和“用内部工具跑一遍”等指令。可能原因：排查资料和给 AI 的要求混在同一个原始文件。影响：整理时容易把工具指令或待发送文案误当成已经执行。明天修正动作：Issue 文件拆成 `facts`、`draft-message`、`agent-request` 三块。
- 现象：AU15P 固化问题只有一句事实快照。可能原因：当天主要精力在 Issue4 和 LPDDR5，固化问题未展开记录。影响：明天恢复现场需要重新追问工具、日志和保护状态。明天修正动作：补一张最小故障记录表：器件、工具、命令、地址、错误码、lock bit、对照板。

## 9. 自我迭代建议

1. 明天先把 A38 LPDDR5 决策拆成 3 个并行等待项：`供应商正式回复`、`项目接受 8GB 整板容量`、`逻辑 Quartus/Fitter 验证`。只要这三项没闭环，硬件侧不要冻结 LPDDR5 pin list。
2. 对所有对外或群内文案，在文件首行标 `status: draft/sent/waiting-feedback/confirmed` 和 `audience:`，避免明天复盘时把可发送文本误判为已发送事实。
3. AU15P 固化问题明天不要只继续试烧；先记录失败证据和保护状态，再判断是工具流程、flash lock/protect、器件差异还是板级连接问题。

## 10. 规则候选

### 规则候选 1
- 触发条件：供应商反馈按厂商、渠道、料号、封装、生命周期出现多个版本。
- 规则：不能按品牌粗粒度关闭或推进；必须按 `厂商 + 料号 + 封装 + 渠道 + 生命周期状态 + 证据来源` 建供应商矩阵。
- 原因：三星 245FBGA 消费类路线不满足要求，但三星 315FBGA x32 正式渠道仍可能需要确认；混在一起会导致错误决策。
- 例子：`K3KL8L80DM-TGCT` 不作为主推，不等于关闭所有 Samsung LPDDR5X x32 路线。
- 是否建议写入 System/workflow-rules.md：yes

### 规则候选 2
- 触发条件：LPDDR5/LPDDR5X 选型影响 FPGA EMIF、bank、pin、byte lane、RZQ、refclk 或其他高速接口共存。
- 规则：采购候选料号只能作为验证输入；原理图 pin list 必须等 Quartus EMIF / Pin Planner / Fitter 证据后冻结。
- 原因：package ball coordinate、datasheet 和开发板资料不能证明当前 FPGA 器件和接口组合可实现。
- 例子：`altera-pbc-b32a-a5e.xlsx` 只是 ball coordinate，不是 LPDDR5 pin assignment。
- 是否建议写入 System/workflow-rules.md：yes

### 规则候选 3
- 触发条件：硬件异常只在 1 块板上复现。
- 规则：不得把问题升级为共性设计问题；必须先做多板复现矩阵，再进入共性根因判断。
- 原因：样本量不足会误导软件、硬件和器件方向。
- 例子：A57 984 解码板后两通道异常当前只基于 1 块板测试结果。
- 是否建议写入 System/workflow-rules.md：yes

### 规则候选 4
- 触发条件：烧录/固化失败涉及地址 locked、擦除失败或写入失败。
- 规则：先记录工具、器件、命令、地址、lock/protect 状态、错误码和成功对照流程，再继续尝试修复。
- 原因：没有最小故障证据时，重复烧写会消耗时间且无法判断是流程、保护位、器件差异还是板级问题。
- 例子：AU15P 0x0000 地址 locked，KU3P 同步骤正常。
- 是否建议写入 System/workflow-rules.md：yes
</file>
</context>
<context role="recent-tomorrow-boot" date="2026-05-07">
<file path="Daily/compiled/2026-05-07/_tomorrow-boot.md">
# Tomorrow Boot Packet - 2026-05-08

## 明日主线

- A38 / DF108 Agilex 5 第一版原理图继续推进，但优先级不是继续画所有页，而是锁定高速接口 pin planning 前置条件和资源矩阵。

## 背景

- 当前 A38 主控板从 KU040 迁移到 Agilex 5，第一版目标是快速改版，不是最终 sign-off。
- MIPI 方向已确认：去掉 HS/LP switch 和 buffer，连接器后直连 Agilex 5 MIPI-capable HSIO bank。
- DDR4 改 LPDDR5，当前按两组 LPDDR5_CTRL0_X32 / LPDDR5_CTRL1_X32 规划，每组对应一个 LPDDR5 主控和一个 x32 颗粒。
- FAE 建议 LPDDR5、MIPI D-PHY、QSFP 不要由硬件侧单独手工定 pin，需要逻辑侧先建 Quartus 最小工程做组合验证。

## 当前状态

- A38 原理图框架：60%。
- MIPI：90%，缺 FPGA 仿真/验证。
- QSFP：已完成。
- LPDDR5：未启动，等待 Quartus EMIF + Pin Planner/Fitter 证据。
- GPIO：方案未定，当前 GPIO 过多，需要判断扩展 FPGA 还是简单 GPIO 扩展芯片。
- 电源树、时钟、复位：未启动。
- LPDDR5 采购需求已形成，状态是等待采购反馈。
- A57 后两通道 eDP 问题：记录显示 AUX 通信和链路训练正常，主攻方向转到 eDP 解码芯片配置、上电时序、IIC 参数下发和物理输出。

## 第一动作

- 建立 A38 资源矩阵初版 CSV，路径建议：
  `revisions/rev-20260506-df108-ku040-to-a5ed052ab32ae2v/02_design_evidence/a5ec052a_b32a_resource_allocation_matrix_20260507.csv`

字段使用：
`domain,group,signal_group,source,connector_or_device_pin,target_bank,target_pin_or_lane,rate_or_voltage,dependency,status,evidence_required,schematic_page,notes`

第一版只填已知事实和待确认项，未验证的 pin、bank、lane、refclk、RZQ、电压域统一标为 `pending_quartus`、`pending_pin_planner`、`pending_datasheet` 或 `pending_reference_design`。

## 注意事项

- 不要把 A5EC052A B32A / A5ED052AB32AE2V 命名差异当成已解决结论；先标 `naming_cleanup`。
- 不要把 MIPI 当普通 LVDS 差分 IO 处理。
- 不要沿用 KU040 Power Tree 的 rail、sequencing、monitor、SmartVID/PMBus、current limit、inrush、MOSFET SOA 等参数。
- 不要在 Quartus / Pin Planner / 官方 datasheet / reference design 未确认前冻结 LPDDR5 pin list。
- `Issue4.md` 是排查同步文案，是否实际发送原文未明确；记录时不要写成“已发送”。

## 不要重复踩的坑

- 先凭封装页或经验画 pin，再等逻辑侧发现 Fitter 不过。
- 把未发送详细版、最终发送简版、可复制发送文案混成同一种事实。
- 把第一版快速原理图当作 sign-off 图。
- 把 A38、A57、workspace skills、wiki sync 全部并行推进，导致明日主线发散。

## 可以交给 AI / agent 的部分

- 生成资源矩阵 CSV 初版，所有未证实字段保留 `pending_*`。
- 把 LPDDR5 / MIPI / QSFP 硬件侧输入参数整理成给逻辑侧的 checklist。
- 整理 Power Tree 页面 checklist：rail list、电流估算、sequencing group、PG/reset、test point/sense/PMBus。
- 把 A57 issue 排查计划整理成实验矩阵和记录模板。
- 把 daily notes 中的 draft / sent / confirmed 状态自动审核出来。

## 必须由我亲自判断的部分

- A38 高速接口 pin planning 的逻辑侧 owner 和交付时间。
- GPIO 过多时选扩展 FPGA 还是 GPIO 扩展芯片。
- LPDDR5 颗粒最终料号、供应风险和采购反馈。
- A57 实测结论是否足以关闭 FPGA 接收逻辑方向，转为解码芯片配置/物理输出方向。
- A5EC/A5ED 最终器件命名和正式设计证据。
</file>
</context>
<context role="recent-tomorrow-boot" date="2026-05-08">
<file path="Daily/compiled/2026-05-08/_tomorrow-boot.md">
# Tomorrow Boot Packet - 2026-05-09

## 明日主线

- A38 / DF108 LPDDR5 决策闭环：同时推进供应商正式回复、项目容量接受、逻辑 Quartus/Fitter 验证；在这三项完成前不冻结 LPDDR5 pin list。
- A57 / AU15P 两个 P0 阻塞只做证据收敛：A57 先做多板复现和 PWDN 实测，AU15P 先补烧录失败证据。

## 背景

- A38 原需求是 2 颗 2GB / 16Gb x32 LPDDR5，总容量 4GB，主控侧约 3733 MT/s。
- 当前未找到满足 5-8 年生命周期的 2GB x32 LPDDR5 料号；美光明确主候选是 `MT62F1G32D2DS-020 WT:D`，4GB / 32Gb x32 LPDDR5X，9600 Mb/s per pin，315-ball TFBGA。
- 如果使用 4GB x32 颗粒，两颗组成 x64 后整板容量会从 4GB 上浮到 8GB。
- 三星 245FBGA 消费类 `K3KL8L80DM-TGCT` 不作为主推；但三星 315FBGA x32 32Gb LPDDR5X 正式渠道仍可并行确认，不能把两条路线混为一个结论。
- LPDDR5 pin assignment 需要看 Agilex 5 EMIF IP User Guide Chapter 9.2.3 / 9.2.4；`altera-pbc-b32a-a5e.xlsx` 只是 package ball coordinate，不是 LPDDR5 pin assignment。
- A57 984 解码板 eDP 后两通道异常目前只基于 1 块板；前 1、2 通道开关视频流 1000 次正常。
- AU15P 固件固化失败：0x0000 地址 locked，擦除和烧写不了；KU3P 同样步骤正常。

## 当前状态

- A38 美光主候选：可推进，但生命周期、温度等级、lead time、价格、MOQ/MPQ、降频使用建议未正式确认。
- A38 项目容量决策：未确认是否接受整板容量从 4GB 上浮到 8GB。
- A38 逻辑验证：未看到 Quartus EMIF / Pin Planner / Fitter 输出，pin list 不能冻结。
- A38 采购路线：南亚关闭；Henry 未见回复；三星消费类 245FBGA 不适合作主推；三星 315FBGA 正式渠道待确认。
- A57 Issue4：待反馈多板测试、IIC 指令对比、寄存器读值、上电时序、SerDes 差异、Redriver PWDN 实测电平。
- AU15P：只有失败现象，缺少工具、命令、错误码、protect/lock 状态和日志。

## 第一动作

- 先建一个 A38 LPDDR5 P0 决策表，列三行：
  - 供应商正式回复：owner 采购，输入美光/WT/WPI 问题清单，输出生命周期/温度/价格/lead time/MOQ/MPQ/降频建议。
  - 项目容量接受：owner 项目/罗奇军，输入 4GB -> 8GB 整板容量变化，输出是否接受及成本/软件/初始化/功耗影响。
  - 逻辑 Quartus 验证：owner 吴志安/逻辑侧，输入美光和三星各一个候选料号，输出 EMIF 配置、Pin Planner、Fitter、QSF / pin report。

完成这张表后，再处理 A57 和 AU15P，不要先进入 LPDDR5 原理图 pin 绘制。

## 注意事项

- 不要把“美光 4GB x32 可评估”写成“料号已冻结”。
- 不要把“供应商没找到 2GB x32”写成“项目已经接受 8GB 整板容量”。
- 不要把“三星 245FBGA 消费类不推进”扩大成“三星所有 LPDDR5X 都不推进”。
- 不要在没有 Quartus / Fitter 证据前冻结 LPDDR5 pin list。
- 不要把 A57 Issue4 的群内同步文案当成已发送事实，原文未明确已发送。
- AU15P 不要继续盲试烧录；先把 lock/protect 状态和错误日志补齐。

## 不要重复踩的坑

- 用 package ball coordinate 代替 pin assignment 规范。
- 把采购料号选择、项目容量决策、逻辑 Fitter 验证混成同一个“已确定”结论。
- 单板复现就判断为共性硬件问题。
- 对外文案不标 draft/sent/confirmed 状态。
- 烧录失败没有记录命令和错误码，只留下“烧不进去”。

## 可以交给 AI / agent 的部分

- 生成 A38 LPDDR5 P0 决策表和 owner/action/output 模板。
- 起草给美光/WT/WPI 的补充问题邮件。
- 起草给三星正式渠道的 315FBGA x32 LPDDR5X 询问清单，同时明确 245FBGA 消费类不是主推。
- 生成 A57 多板测试记录表、IIC 指令对比表、寄存器读值对比表。
- 生成 AU15P 固化失败最小记录表。
- 审核当天文案是否标记 draft/sent/waiting-feedback/confirmed。

## 必须由我亲自判断的部分

- 是否接受 A38 LPDDR5 整板容量从 4GB 上浮到 8GB。
- 美光主候选在成本、生命周期和降频使用上是否足以进入设计主线。
- 三星 315FBGA 料号是否值得作为并行候选继续投入时间。
- A57 多板测试结果是否足以把问题定义为共性问题。
- AU15P locked 地址问题是否需要切换工具、改保护配置、返查板级连接或找供应商支持。
</file>
</context>
