# Cyberlog - 2026-05-09

## 1. 今日真实推进

- A38 / Agilex 5 LPDDR5 的 FPGA 端网络连接有实际推进：记录中明确写到“lpddr5 fpga端网络连接好了”；相关工作基于 A5EC052A B32A、两颗独立 x32 LPDDR5、U_LPDDR5_0 -> IO96 bank 2A、U_LPDDR5_1 -> IO96 bank 2B 的假设展开。来源：`今日完成项.md`, `agilex5 lpddr5 pin assign.md`
- LPDDR5 pin assign 的规则边界被澄清：EMIF User Guide Table 22 的 Pin Index 是 FPGA IO96 bank 内部 0-95 号相对位置，不是 LPDDR5 颗粒 ball；当前“两颗 x32 LPDDR5，每颗作为独立 x32 interface”的场景应使用 x32 column，而不是 2 Channel x16 column。来源：`A5EC052A B32A lpddr5 pin assign.md`
- LP5 网络数量完成统计：U0 63 个、U1 63 个，总计 126 个网络；统计口径排除了空白单元格和占位 `0`。来源：`LP5 网络数量统计.md`
- A57 / 984 解码板 eDP 问题补充了新的架构和多板验证信息：eDP1/2 对应一颗 DS90UB984，eDP3/4 对应另一颗 DS90UB984；4 块解码板测试显示 eDP1/2/3/4 都有概率出问题，板间表现不同，目前没有一块可以稳定 4 通道出图。来源：`Issue4 A57 edp问题 今日新增.md`
- A57 排查项有进展：前后 2 通道 eDP SerDes 电路差异已确认无差异；前 2 通道与后 2 通道 984 IIC 指令、ini / 参数下发对比完成且未发现问题；解码芯片上电时序中电源、PWDN、I2C 看起来没问题，但 MODE 配置有问题，三个 MODE 都是 0V，提示软件侧未处理或配置未生效。来源：`Issue4 A57 edp问题 今日新增.md`, `今日完成项.md`
- A57 Redriver 行为边界被补充：eDP 高速链路 mainstream 中间的 Redriver 在设备上电后已经配置好，后续没有重新配置；当前重复测试方式是对解码芯片重新上下电和重新配置。来源：`Issue4 A57 edp问题 今日新增.md`
- AU15P 固化失败从单点现象扩展成对照矩阵：KU3P + W25Q256JWEIQ 可固化；AU15P + W25Q256JWEIQ 和 AU15P + W25Q128JWSIQ 都不可固化，Vivado/JTAG 报错均为 SPI flash sector at address `0x0000` locked for erase/program。来源：`issue5 AU15P + winbond flash 用jtag+vivado方式无法固化问题.md`

## 2. 当前工作画布

### Active

- A38 / Agilex 5 LPDDR5 原理图连接：FPGA 端网络已连接，但仍需要把当前 pin/net 表标记为工作输入，而不是签核证据。
- A38 LPDDR5 Quartus / Fitter 验证：仍需要用目标 EMIF IP、目标器件、目标 bank 组合跑 test-fit，确认 bank 2A / 2B、x32 topology、REFCLK、RZQ、CA/CK/WCK/DQ byte lane 等能收敛。
- A57 eDP 出图异常：当前从“前后通道差异”转向“多板、多通道、概率性异常 + MODE 配置异常 + 寄存器/厂家确认”的证据收敛。
- AU15P + Winbond SPI Flash 固化问题：当前关键事实是 AU15P 平台下两个容量 Flash 都在 `0x0000` sector lock 处失败，KU3P 对照正常。

### Queue

- 把 A38 LPDDR5 当前 CSV / pin-net 表纳入正式设计证据位置，并给每一类网络标注 `working`, `pending_quartus`, `pending_fae`, `pending_package_confirm`。
- 向 FPGA FAE 确认：A5EC052A B32A 是否支持 two independent LPDDR5 x32 interfaces、推荐 IO96 banks、是否有验证过的 memory vendor/package/part list、是否能提供 QSF / example design。
- 对 OrCAD 原理图执行一次 LPDDR5 网络核对：U0/U1 各 63 个网络、总 126 个网络，检查 DQ/DMI/RDQS/WCK/CK/CS/CA/RESET_N/RZQ/REFCLK 分类是否缺漏或重名。
- A57 继续补另外 2 块 984 解码板出图情况，并把 6 块板、4 个 eDP、2 颗 984、MODE 状态、寄存器读值放到同一张矩阵。
- A57 与厂家确认“模拟出图输出相关寄存器”和 984 关键管脚测量点。
- AU15P 读取 Flash status register / lock bit / protection bit，并记录 Vivado、JTAG、bitstream、配置存储器型号、命令和完整日志。

### Blocked

- A38 LPDDR5 pin assign 签核：阻塞原因是当前 pin/net 表是基于官方 pinout、EMIF 规则和 Micron 315-ball 参考封装合成的工作表，但未见 Quartus EMIF / Pin Planner / Fitter 证据；解除方式是逻辑侧或 FPGA FAE 输出 test-fit / report；owner：逻辑侧 / FPGA FAE / 硬件；下一步：拿当前 2A + 2B x32 假设跑最小工程。
- A38 memory-side ball mapping：阻塞原因是当前说明引用 Antmicro / Micron 315-ball 参考，若最终 LPDDR5 料号或封装不是该 ballout，内存颗粒侧 ball 会变化；解除方式是锁定最终料号和封装后重核 memory-side ball；owner：硬件 / 采购；下一步：把 memory package 状态标为 `pending_part_package_confirm`。
- A57 稳定 4 通道出图：阻塞原因是多板测试显示 4 个 eDP 都可能出问题，且没有一块板稳定 4 通道出图；解除方式是建立板卡/通道/解码芯片/MODE/寄存器矩阵，先确认 MODE 三个 0V 是否为直接配置缺口；owner：软件侧 / 陈斌 / 吴峰；下一步：确认 MODE 管脚期望状态和软件配置路径。
- A57 根因判断：阻塞原因是 SerDes 差异和 IIC/ini 参数已基本排除，但寄存器、MODE、厂家确认和剩余板卡测试仍未闭环；解除方式是补寄存器读值、关键管脚实测和厂家解释；owner：陈斌 / 吴峰 / 罗奇军；下一步：读 984 相关寄存器并对照出图状态。
- AU15P 固化：阻塞原因是 Vivado/JTAG 对 AU15P + Winbond Flash 报 `0x0000` sector locked，且两个 Flash 容量都复现；解除方式是读取并清除保护/锁定位，或确认 AU15P 配置链路/约束/工具流程差异；owner：未明确；下一步：读 status register 并尝试标准 unlock / erase 流程，保留日志。

### Closed

- LPDDR5 Table 22 Pin Index 的含义已澄清：它是 FPGA IO96 bank 内部相对位置，不是内存颗粒 ball。
- 当前两颗独立 x32 LPDDR5 的使用场景应按 x32 column 处理；除非真实拓扑改为两个独立 x16 channel，否则不应使用 2 Channel x16 column。
- LP5 网络数量统计完成：U0 63、U1 63、总 126。
- A57 前后 2 通道 eDP SerDes 电路差异确认无差异。
- A57 前 2 通道与后 2 通道 eDP 984 IIC 指令、ini / 参数下发对比完成，未发现问题。

## 3. 关键决策

| 决策 | 背景 | 理由 | 风险 | 后续动作 | 来源文件 |
|---|---|---|---|---|---|
| 当前两颗 x32 LPDDR5 应按 x32 column 做 pin placement，而不是 2 Channel x16 column | 目标是假设两颗独立 x32 LPDDR5，每颗作为 32-bit EMIF interface | Table 22 的 x32 对应单个 x32 interface；2 Channel x16 是两个独立 x16 channel，CA/CK/WCK 分配不同 | 如果真实拓扑不是两颗独立 x32，当前 CSV / 原理图连接需要重做 | 在 Quartus EMIF 中按 two independent x32 interfaces 建最小工程验证 | `A5EC052A B32A lpddr5 pin assign.md` |
| 当前 LPDDR5 pin/net 表只能作为工作输入，不能作为签核证据 | 记录中提到已生成 CSV 并完成 FPGA 端网络连接 | 生成表基于官方 pinout + EMIF 规则 + 参考 memory ballout，但还没有 Fitter/FAE 证据 | 若直接签核，可能出现 bank、PLL、RZQ、byte lane、package ball 或 PCB escape 问题 | 标注 `pending_quartus` / `pending_fae` / `pending_package_confirm`，并跑 test-fit | `agilex5 lpddr5 pin assign.md`, `A5EC052A B32A lpddr5 pin assign.md`, `今日完成项.md` |
| A57 eDP 问题不再按“后两通道异常”单一路径描述 | 新增 4 块板测试显示 eDP1/2/3/4 都可能异常，且板间表现不同 | 现象跨通道、跨解码芯片且概率性出现，单纯前后通道硬件差异解释力不足 | 如果继续沿用旧叙述，会误导排查方向 | 建立多板 x 多通道矩阵，并把 MODE、寄存器、上电、PWDN、I2C 和出图结果绑定记录 | `Issue4 A57 edp问题 今日新增.md` |
| A57 下一步优先检查 MODE 配置和寄存器证据 | 电源、PWDN、I2C 看起来没问题，但三个 MODE 都是 0V，且软件侧可能未处理 | SerDes 差异和 IIC/ini 参数对比已基本排除，MODE 是今天新增的明确疑点 | MODE 只是疑点，不能直接写成根因；仍需确认期望电平、采样时机和软件配置 | 先确认 MODE 期望状态、软件配置路径和 984 相关寄存器 | `今日完成项.md`, `Issue4 A57 edp问题 今日新增.md` |
| AU15P 固化失败应按 AU15P 平台/配置链路问题排查，而不是单一 Flash 容量问题 | AU15P + W25Q256 和 AU15P + W25Q128 都失败，KU3P + W25Q256 成功 | 同一 AU15P 平台不同容量 Flash 都报 `0x0000` locked，容量本身不是唯一变量 | 仍不能排除 flash protection 默认状态、工具识别、约束或板级连接差异 | 读取 status register / protection bit，执行 unlock / erase，并保留 Vivado 日志 | `issue5 AU15P + winbond flash 用jtag+vivado方式无法固化问题.md` |

## 4. 重要信息

- A38 当前 pin assign 假设：FPGA 为 A5EC052A B32A；U_LPDDR5_0 使用 IO96 bank 2A；U_LPDDR5_1 使用 IO96 bank 2B；两颗 LPDDR5 均按独立 x32 interface。
- EMIF Pin Index 映射链路是：EMIF User Guide Pin Index -> A5EC052A B32A pinout xlsx 中的 FPGA package ball -> LPDDR5 颗粒 pin name / ball。
- 示例映射：Table 22 中 Pin Index 0 = MEM_DQ[0]；若使用 A5EC052A B32A bank 2A，index 0 = FPGA ball CL91；再接到 LPDDR5 颗粒 DQ0_A / ball D1 这类 memory-side ball。
- `FPGA_RZQ` 是 FPGA OCT 电阻脚，不是 LPDDR5 颗粒 ZQ；`REFCLK_P/N` 接 EMIF PLL reference clock，不接内存颗粒。
- 记录中提到的 CSV：`lpddr5_x32_a5ec052a_b32a_2chips.csv` 和 `lpddr5_x32_a5ec052a_b32a_all_io96_banks.csv`。这些文件名出现在 raw note 中，但本次 daily raw 目录没有附带 CSV 本体。
- LP5 网络数量：DQ 64、DMI 8、RDQS C/T 16、WCK C/T 8、CK C/T 4、CS 4、CA 14、RESET_N 2、FPGA_RZQ 2、REFCLK_P/N 4，总计 126。
- A57 架构：eDP1/2 对应一颗 DS90UB984；eDP3/4 对应另一颗 DS90UB984。
- A57 多板现象：一块板 eDP3/4 出图异常概率较高，另外三块板 eDP1/2 出图异常概率较高；同一颗解码芯片对应的 eDP1/2 或 eDP3/4 不表现严格一致，存在一个好一个不好的情况。
- A57 当前测试方式：对解码芯片重新上下电和重新配置；Redriver 上电后配置完成，后续没有重新配置。
- A57 今日新增疑点：MODE 三个管脚都是 0V，记录中判断“软件那边没有进行处理”。
- AU15P 固化报错原文：`[Labtools 27-3347] Flash Programming Unsuccessful: SPI flash sector at address 0x0000 is locked for erase/program.`

## 5. 今日产出

- A38 LPDDR5 FPGA 端网络连接：属于 A38 / Agilex 5 原理图；来源 `今日完成项.md`；可复用价值是原理图 LPDDR5 页已经进入可核对状态，但仍需 Quartus / FAE 签核。
- A38 LPDDR5 pin assign 规则说明：属于 A38 / Agilex 5 pin planning；来源 `A5EC052A B32A lpddr5 pin assign.md`; 可复用价值是明确 x32 column、Pin Index、FPGA ball、memory ball 的层级关系，避免把 2 Channel x16 或 memory ball 误用于当前拓扑。
- A38 LP5 网络数量统计：属于 A38 / OrCAD 原理图核对；来源 `LP5 网络数量统计.md`；可复用价值是给 ERC / netlist / 原理图 review 提供数量基线。
- A57 Issue4 新输入：属于 A57 / 984 解码板 eDP 出图；来源 `Issue4 A57 edp问题 今日新增.md`；可复用价值是把昨天单板/后通道叙述修正为多板概率性问题，并补充架构、Redriver 配置时机和测试方法。
- A57 排查进展快照：属于 A57；来源 `今日完成项.md`；可复用价值是把 SerDes 差异、IIC/ini 参数、电源/PWDN/I2C 和 MODE 疑点分开，形成明天第一动作。
- AU15P 固化失败矩阵：属于 AU15P / Winbond Flash / Vivado JTAG 固化；来源 `issue5 AU15P + winbond flash 用jtag+vivado方式无法固化问题.md`；可复用价值是明确 KU3P 对照成功、AU15P 两个 Flash 型号失败和统一错误码。

## 6. 未完成任务

| 任务 | 所属项目 | 下一步动作 | 优先级 | 是否适合交给 AI / agent | 为什么 |
|---|---|---|---|---|---|
| 跑 A38 LPDDR5 Quartus EMIF / Pin Planner / Fitter test-fit | A38 | 用 A5EC052A B32A、bank 2A/2B、two independent x32 interfaces 建最小工程并导出报告 | P0 | 部分适合 | AI 可整理参数和验收清单，Quartus 工程需逻辑侧执行 |
| 核对 OrCAD LPDDR5 原理图网络 | A38 | 按 U0/U1 各 63 个网络对照 CSV / 原理图 netlist，检查缺漏、重名、方向和差分对 | P0 | 适合整理 | AI 可生成核对表或脚本思路，实际 OrCAD 文件需人工/工具执行 |
| 确认 LPDDR5 最终料号和封装 | A38 | 采购/硬件确认是否使用 Micron 315-ball 类封装，若改封装则重核 memory-side ball | P0 | 不完全适合 | AI 可列风险，最终料号和供应链选择需要人判断 |
| 向 FPGA FAE 确认 LPDDR5 topology 和推荐 pin assignment | A38 | 发送 topology、bank、料号、封装、test-fit 输入，请求 QSF / reference / review | P1 | 适合起草 | AI 可起草问题清单，正式确认来自 FAE |
| 建立 A57 6 板 x 4 通道测试矩阵 | A57 | 补另外 2 块板，记录每块板 eDP1/2/3/4、984 芯片、MODE、电源/PWDN/I2C、寄存器和出图状态 | P0 | 适合 | AI 可生成表格模板，测试由现场执行 |
| 确认 A57 MODE 三个 0V 的根因 | A57 | 查 MODE 期望电平、采样时机、软件配置路径、是否需要重新配置或硬件拉电阻 | P0 | 部分适合 | AI 可整理检查项，测量和软件修改需对应 owner 执行 |
| 读取并解释 A57 984 相关寄存器 | A57 | 和厂家确认模拟出图输出相关寄存器，建立好/坏通道读值对比 | P0 | 适合整理 | AI 可做对比模板，寄存器读值需软件/厂家提供 |
| 排查 AU15P + Winbond Flash `0x0000` locked | AU15P | 读取 status/protection register，执行 unlock / erase，保存 Vivado/JTAG 完整日志，对比 KU3P 流程 | P0 | 部分适合 | AI 可生成排查 checklist，实际工具和硬件操作需要现场执行 |
| 把今日生成的 LPDDR5 CSV / 表格放到正式项目证据目录 | A38 | 如果 CSV 存在于工作区，移动或复制到受控项目资料位置，并在 daily 只保留引用 | P1 | 适合提醒 | daily raw 不应成为正式设计资产仓库 |

## 7. 明日启动包

见 `Daily/compiled/2026-05-09/_tomorrow-boot.md`。

## 8. 工作流摩擦

- 现象：A38 LPDDR5 raw note 中同时包含 AI 问答、生成 CSV 的描述、原理图绘制诉求和封装选择建议。可能原因：为了快速推进 OrCAD 绘图，把知识澄清和工程执行混在一个文件里。影响：容易把“AI 生成的工作表”误判为“已经签核的 pin assignment”。明天修正动作：所有 pin/net 表都加 `status` 字段，至少区分 `working_table`、`quartus_verified`、`fae_reviewed`、`schematic_connected`。
- 现象：A38 已经开始按 pin/net 表画网络，但 Quartus / Fitter 证据仍未出现。可能原因：原理图进度压力要求先提高绘图效率。影响：如果 bank 或 topology 后续不通过，返工成本会集中爆发。明天修正动作：先做最小 test-fit 或至少发 FAE review，再扩大原理图连接范围。
- 现象：A57 从昨天“后两通道异常”变成今天“4 个通道都有概率异常，板间不同”。可能原因：样本量扩大后暴露了原叙述不稳定。影响：旧问题框架会误导责任划分和排查方向。明天修正动作：废弃“前/后通道”单线叙述，改用板卡 x 通道 x 解码芯片 x 配置状态矩阵。
- 现象：A57 记录里同时出现“4 块板已测”“计划 6 块”“另外 2 块确认”的信息。可能原因：计划和已完成进度混在同一表格。影响：复盘时容易误读样本量。明天修正动作：表格拆成 `tested_count`、`planned_count`、`pending_board` 三列。
- 现象：AU15P 固化问题有了错误码，但还没有 status register、unlock 命令、工具版本和完整日志。可能原因：记录仍偏结果快照。影响：明天可能继续重复烧录而不是定位 lock/protect 来源。明天修正动作：先采集最小故障证据，再试解锁。

## 9. 自我迭代建议

1. 明天 A38 不要只继续连线；先把 LPDDR5 每个网络组打上验证状态：`schematic_connected`、`pending_quartus`、`pending_fae`、`pending_memory_package`。这能防止“画完了”被误当成“可签核”。
2. A57 第一动作是建一张 6 板 x 4 eDP 的矩阵，把 MODE 三个 0V 放成显式字段。只要 MODE 状态没解释清楚，不要急着回到 Redriver 或 SerDes 差异方向。
3. AU15P 不要继续盲目 Program Configuration Memory Device；先读 Flash status/protection 位并记录 unlock/erase 过程，否则每次失败都只会重复同一个 `0x0000 locked` 结论。

## 10. 规则候选

### 规则候选 1
- 触发条件：用 AI 或脚本生成高速接口 pin/net 表并开始画原理图。
- 规则：生成表必须标注证据层级：`working_table`、`schematic_connected`、`quartus_verified`、`fae_reviewed`、`released`，未完成前不得写成 sign-off。
- 原因：高速接口 pin assign 的错误会直接造成原理图和 PCB 返工。
- 例子：A38 LPDDR5 FPGA 端网络已连接，但 bank 2A/2B x32 topology 仍缺 Quartus / Fitter 证据。
- 是否建议写入 System/workflow-rules.md：yes

### 规则候选 2
- 触发条件：多板、多通道硬件问题的表现从单一通道扩展为概率性、板间差异性现象。
- 规则：停止使用单一叙述，改用矩阵记录板号、通道、芯片、配置状态、寄存器、测量点和结果。
- 原因：样本量扩大后，旧叙述会保留错误假设。
- 例子：A57 eDP 从“后两通道异常”变成 eDP1/2/3/4 都有概率问题，且不同板表现不同。
- 是否建议写入 System/workflow-rules.md：yes

### 规则候选 3
- 触发条件：Vivado/JTAG 固化报 sector locked、erase/program locked 或类似保护错误。
- 规则：先记录 Flash 型号、平台、工具版本、完整错误、status/protection register、unlock/erase 命令和成功对照，再继续烧录尝试。
- 原因：没有保护位证据时，重复烧写无法区分工具流程、Flash 默认保护、配置链路或板级连接问题。
- 例子：AU15P + W25Q256JWEIQ / W25Q128JWSIQ 都报 `0x0000` sector locked，而 KU3P + W25Q256JWEIQ 可固化。
- 是否建议写入 System/workflow-rules.md：yes
