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
