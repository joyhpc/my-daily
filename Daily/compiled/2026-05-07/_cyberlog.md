# Cyberlog - 2026-05-07

## 1. 今日真实推进

- A38 / DF108 Agilex 5 原理图第一版推进方向被收敛：MIPI 去掉 HS/LP switch 和 buffer，走解码板到连接器再直连 Agilex 5 MIPI-capable HSIO bank；DDR4 改 LPDDR5；24V 电源入口复用 LM5060 拓扑但参数需重算。来源：`框图修改.md`
- A38 第一版原理图推进计划被整理成可执行结构：包含当前状态、资源矩阵 CSV 字段、原理图绘制顺序、快速 gate 和关键假设。来源：`框图修改.md`
- LPDDR5 采购需求形成：单颗 x32、2GB/16Gb、主控端支持 3733 MT/s，建议寻源 5500 MT/s 或 6400 MT/s 规格并降频使用，商业级，要求 5-8 年无 EOL 风险。来源：`LPddr5需求 to 采购工程师 沟通.md`
- LPDDR5 / MIPI / QSFP pin planning 的协作诉求被明确，并形成最终发送的项目群简版：要求逻辑侧建最小 Quartus 工程，通过 Fitter 检查后输出可用于原理图设计的 pin list。来源：`lpddr5 pin assign 项目群沟通.md`
- A57 eDP 后两通道问题的排查方向收敛：AUX 通信和链路训练被记录为正常，焦点从链路训练转到 eDP 解码芯片是否正常输出有效数据。来源：`Issue4.md`
- A38 当前完成度被记录：原理图框架 60%，MIPI 90% 但缺 FPGA 仿真验证，QSFP 已完成，LPDDR5 / 电源树 / 时钟 / 复位未启动，GPIO 方案未定。来源：`今日完成项.md`

## 2. 当前工作画布

### Active

- A38 / DF108 Agilex 5 原理图第一版：当前在框架、MIPI、QSFP、LPDDR5、Power Tree、Clock/Reset/Config、GPIO 之间推进。
- A38 高速接口 pin planning：LPDDR5 / MIPI D-PHY / QSFP 需要逻辑侧通过 Quartus 最小工程和 Fitter 验证。
- A57 eDP 后两通道概率不出图排查：主攻方向转为 eDP 解码芯片配置、上电时序、IIC 参数下发和物理输出量测。
- cyberlog 工作流：当天计划包含同步当日事件和 cyberlog。

### Queue

- A57 项目进度、会议、方案、节点、落地、测试、配套设备、串行板梳理规划。
- workspace 加入 SOP、demo 等，并保持可拓展、容易修改。
- GitHub 上的 my wiki 同步到本地。
- 将项目做成 skills，并用当日内容作为测试用例。
- sch reviewer 增加中间解码层，让任意 LLM 能理解原理图数据结构。
- 将 Agilex 芯片资料也沉淀成 skills。

### Blocked

- A38 LPDDR5 原理图落 pin：阻塞原因是 LPDDR5 / MIPI / QSFP 组合会占用 bank、lane、PLL、RZQ、refclk、电压域资源，不能由硬件侧单独手工定 pin；解除方式是逻辑侧建立 A5ED052A B32A 最小 Quartus 工程并通过 Fitter 或至少 Pin Planner/Fitter 规则检查；owner：逻辑侧待明确，文案中点名询问吴志安是否主导；下一步：硬件侧提供 LPDDR5、MIPI、QSFP 参数，推动逻辑侧输出 pin assignment / QSF / pin report。
- A38 Power Tree：阻塞原因是 Agilex 5 power rail、sequencing、monitor、SmartVID/PMBus 等不能沿用 KU040；解除方式是依据 Intel 官方 Power Management Guide、power estimation 和 reference design 重做；owner：硬件侧；下一步：建立 rail list、最大电流估算、sequencing group、PG/reset 关系。
- A38 GPIO：阻塞原因是当前 GPIO 过多，扩展 FPGA 或简单 GPIO 扩展芯片方案未定；解除方式是先列 GPIO 数量、速率、方向、时序和控制语义，再比较扩展方案；owner：硬件侧/系统架构待定；下一步：输出 GPIO 保持矩阵。
- A57 eDP 后两通道：阻塞原因是 SerDes CDR 不能锁定、COMOM 不能对齐且复位无效，疑似 eDP 解码芯片未输出正常数据；解除方式是示波器抓上电时序、确认故障态下解码芯片物理输出、核查 MCU IIC 参数下发和双核控制变量；owner：硬件何鹏程/吴锋，MCU 或软件张纪琦/Candy|罗奇军；下一步：按 Issue4 Action Items 联合排查。

### Closed

- A38 MIPI 第一版连接方向已确认：去掉 HS/LP switch 和 buffer，直连 Agilex 5 HSIO bank。
- A38 QSFP 记录为已完成。
- A38 LPDDR5 采购需求已形成，状态为等待采购反馈。
- A38 高速接口前置验证项目群简版已形成，原文标记为“我最终发送的简版”。
- A57 最新排查同步文案已形成；是否已实际发送，原文未明确。

## 3. 关键决策

| 决策 | 背景 | 理由 | 风险 | 后续动作 | 来源文件 |
|---|---|---|---|---|---|
| A38 MIPI 去掉 HS/LP switch 和 buffer，连接器后直连 Agilex 5 HSIO bank | DF108 主控板改 Agilex 5 第一版原理图 | 原文明确记录“已确认”，MIPI 从解码板过来经过连接器后直连 | lane count、lane rate、clock lane、target bank/lane、RZQ/refclk 仍待确认 | 在原理图中只画直连框架，不能按普通 LVDS 差分 IO 处理 | `框图修改.md` |
| DDR4 改为 LPDDR5 | DF108/KU040 迁移到 Agilex 5 | 当前按 Agilex 5 E-Series Group A 口径，LPDDR5 上限按 3733 Mbps/pin | 实际颗粒、EMIF bank、byte lane、RZQ、refclk、reset、AC/data pin 未经 Quartus 验证 | 按 2 组 x32 颗粒规划，等待 Quartus EMIF + Pin Planner 回填 | `框图修改.md`, `LPddr5需求 to 采购工程师 沟通.md` |
| LPDDR5 / MIPI / QSFP pin assignment 由逻辑侧先建 Quartus 工程验证 | FAE 建议硬件不要盲分 pin | 多个高速接口共享 bank/lane/PLL/RZQ/refclk/电压域资源，组合后可能 Fitter 失败 | 逻辑侧 owner 和时间尚未明确，原理图 pin list 会被阻塞 | 在项目群推动逻辑侧输出最小工程、Fitter 检查结果和最终 pin list | `lpddr5 pin assign 项目群沟通.md` |
| Power Tree 必须重做 | Agilex 5 不能沿用 KU040 电源方案 | Intel 官方指南把 power tree、power estimation、power generation、I/O sequencing 作为设计阶段内容 | 若沿用旧值，可能导致 sequencing、monitor、SmartVID/PMBus、inrush 或 SOA 风险 | 建立 rail list、电流估算、PG chain、enable dependency、test point/sense/PMBus | `00设计项plan.md`, `框图修改.md` |
| A57 排查焦点转向 eDP 解码芯片输出/配置 | 后两通道 AUX 通信和链路训练记录为正常，但 SerDes 复位无效 | AUX 正常而 SerDes 仍无法锁定，合理推断源头没有输出正常有效图像数据 | 解码芯片异常原因仍不确定，可能是上电时序、IIC 指令或物理状态 | 抓上电时序、量测物理输出、核查 IIC 下发、验证双核控制变量 | `Issue4.md` |

## 4. 重要信息

- A38 器件命名存在 A5EC052A B32A / A5ED052AB32AE2V 差异，当前只能按占位处理，不能直接判为正式设计结论。
- A38 第一版不是 sign-off 图，目标是推进快速第一版原理图改版，同时保持假设和待补证状态清晰。
- A38 资源矩阵建议路径为 `revisions/rev-20260506-df108-ku040-to-a5ed052ab32ae2v/02_design_evidence/a5ec052a_b32a_resource_allocation_matrix_20260507.csv`。
- 资源矩阵字段要求：`domain,group,signal_group,source,connector_or_device_pin,target_bank,target_pin_or_lane,rate_or_voltage,dependency,status,evidence_required,schematic_page,notes`。
- 资源矩阵状态建议限定为：`confirmed`, `assumed_for_rev1`, `pending_quartus`, `pending_pin_planner`, `pending_datasheet`, `pending_reference_design`, `naming_cleanup`。
- LPDDR5 寻源建议为美光、三星、海力士等一线大厂，要求长期供应并确认未来 5-8 年无 EOL。
- A57 关键事实：后两通道 AUX 通信未卡死，握手指令读写能正常走完；SerDes CDR 不能锁定、COMOM 不能对齐，手动复位无改善。

## 5. 今日产出

- A38 第一版原理图推进计划：属于 A38 / DF108 Agilex 5 项目；来源 `框图修改.md`；可复用价值是给后续画图顺序、设计证据和 review gate 提供统一入口。
- A38 LPDDR5 采购需求：属于 A38 / DF108 Agilex 5 项目；来源 `LPddr5需求 to 采购工程师 沟通.md`；可复用价值是采购寻源和料号生命周期确认。
- A38 高速接口 Quartus 前置验证项目群文案：属于 A38 / DF108 Agilex 5 项目；来源 `lpddr5 pin assign 项目群沟通.md`；可复用价值是明确硬件侧输入、逻辑侧输出和 pin lock 前置条件。
- A57 eDP 后两通道排查同步文案：属于 A57 项目；来源 `Issue4.md`；可复用价值是统一最新事实、核心推断和多方 action items。
- A38 完成度快照：属于 A38 / DF108 Agilex 5 项目；来源 `今日完成项.md`；可复用价值是明天启动时直接判断主线和阻塞。

## 6. 未完成任务

| 任务 | 所属项目 | 下一步动作 | 优先级 | 适合交给 AI / agent | 为什么 |
|---|---|---|---|---|---|
| 推动逻辑侧建立 A5ED052A B32A 最小 Quartus 工程 | A38 | 明确 owner 和交付时间，提供 LPDDR5/MIPI/QSFP 参数 | P0 | 部分适合 | AI 可整理参数表和检查清单，但 Quartus 工程与 Fitter 需要逻辑同事实际执行 |
| 建立 A38 资源矩阵 CSV | A38 | 按指定字段创建 MIPI、LPDDR5、power、clock/reset/config、naming 五组矩阵 | P0 | 适合 | AI 可根据现有 notes 生成初版 CSV，但 pin/bank 必须标为待确认 |
| 重做 Agilex 5 Power Tree | A38 | 收集官方 power guide/reference design，列 rail、sequencing、PG/reset、PMBus/sense | P0 | 部分适合 | AI 可生成清单和模板，电流估算和器件选择需硬件判断 |
| 启动 LPDDR5 原理图设计 | A38 | 等 Quartus EMIF + Pin Planner 结果后回填两组 x32 颗粒连接 | P0 | 部分适合 | AI 可做结构页和待确认标注，不能替代 pin planning 证据 |
| 确定 GPIO 扩展方案 | A38 | 统计 GPIO 数量、方向、速率和控制语义，再比较扩展 FPGA vs GPIO 扩展芯片 | P1 | 适合 | AI 可生成比较矩阵，最终方案需结合成本、时序、PCB 和供应链 |
| A57 eDP 后两通道联合排查 | A57 | 抓上电时序、故障态输出、IIC 下发、双核控制变量 | P0 | 部分适合 | AI 可整理实验矩阵和记录模板，实测必须由硬件/软件团队执行 |
| 同步 GitHub my wiki 到本地 | workspace | 明确仓库来源和同步目标路径 | P2 | 适合 | AI/脚本可执行同步，但需要确认源仓库和目录策略 |
| 将项目和 Agilex 资料做成 skills | workspace-skills | 先定义 skill 边界和测试用例 | P2 | 适合 | AI 可草拟 skill 结构，但内容需要从项目资料中抽取 |
| sch reviewer 增加解码层 | sch-reviewer | 定义 LLM 可读的原理图中间数据结构 | P2 | 适合 | AI 可设计 schema 和样例，但需要对接实际工具输出 |

## 7. 明日启动包

见 `Daily/compiled/2026-05-07/_tomorrow-boot.md`。

## 8. 工作流摩擦

- 现象：A38 同时包含原理图绘制、器件命名、LPDDR5、MIPI、QSFP、电源树、GPIO 和 HPS/SoC 架构问题。可能原因：从 KU040 迁移到 Agilex 5 时把架构选择和原理图执行混在同一层。影响：容易先画图后补证，导致 pin/bank/power 返工。明天修正动作：先建立资源矩阵和待补证列表，再进入具体页面绘制。
- 现象：LPDDR5 pin assignment 卡在硬件和逻辑边界。可能原因：高速接口资源必须由 Quartus 工程验证，不能靠原理图经验决定。影响：LPDDR5 页和部分 MIPI/QSFP pin list 无法冻结。明天修正动作：把项目群文案转化为明确 owner、输入参数表和交付物清单。
- 现象：A57 记录里同时有事实、推断和待发送文案。可能原因：排查沟通节奏快，文案直接沉淀到 notes。影响：复盘时容易把“可复制发送”误当成“已发送”。明天修正动作：所有 issue 文案增加状态标记：draft / sent / confirmed。
- 现象：workspace、wiki、skills、sch reviewer 与 A38/A57 主线混在当日规划。可能原因：工作入口集中在单个日计划里。影响：主线优先级被稀释。明天修正动作：日计划先按 Active / Queue / Later 三层分区。

## 9. 自我迭代建议

1. 明天先做 A38 `resource_allocation_matrix_20260507.csv`，所有未被 Quartus/Pin Planner/官方资料证明的字段统一写 `pending_*`，不要在原理图里假装已确定。
2. 对外沟通文案必须在文件头标状态：`draft`、`sent`、`waiting-feedback`、`confirmed`。尤其是项目群和 issue 同步文案。
3. 每天结束前只保留 1 条明日主线。2026-05-08 的主线应优先是 A38 高速接口 pin planning owner 和资源矩阵，而不是同时推进所有页面。

## 10. 规则候选

### 规则候选 1
- 触发条件：涉及 FPGA 高速接口 pin assignment，尤其 LPDDR5、MIPI D-PHY、QSFP、transceiver。
- 规则：硬件原理图不能先手工定 pin；必须先由逻辑侧建最小工程，通过 Quartus Pin Planner/Fitter 规则检查后再锁定 pin list。
- 原因：bank、lane、PLL、RZQ、refclk、电压域资源存在组合冲突风险，后期返工成本高。
- 例子：A5ED052A B32A 的 LPDDR5 + MIPI + QSFP 需要逻辑侧输出 pin assignment / QSF / pin report。
- 是否建议写入 System/workflow-rules.md：yes

### 规则候选 2
- 触发条件：从旧 FPGA 平台迁移到新 FPGA/SoC 平台。
- 规则：Power Tree、pin planning、boot/config/reset、外设保持矩阵必须先成为设计证据，再进入 sign-off 级原理图。
- 原因：KU040 到 Agilex 5 不能沿用电源、配置、bank 和 IP 假设。
- 例子：Agilex 5 的 power rail、sequencing、SmartVID/PMBus、I/O sequencing 必须重做。
- 是否建议写入 System/workflow-rules.md：yes

### 规则候选 3
- 触发条件：daily notes 中出现沟通文案或 AI 生成文案。
- 规则：文件头必须标记状态：draft / sent / waiting-feedback / confirmed；未标记时不得在 cyberlog 中升级为已发送事实。
- 原因：避免把“可以直接复制发送”的文案误判成已经执行。
- 例子：A57 Issue4 是可复制发送文案，但原文未明确已发送；LPDDR5 pin assign 文件同时包含未发送详细版和最终发送简版。
- 是否建议写入 System/workflow-rules.md：yes
