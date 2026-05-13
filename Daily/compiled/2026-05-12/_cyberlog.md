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
