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
