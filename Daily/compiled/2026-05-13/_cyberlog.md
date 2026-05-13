# Cyberlog - 2026-05-13

## 0. 项目索引

- A57-eDP：今天主线是把 eDP AUX 问题从“主链路/眼图优先怀疑”收敛到 AUX/DPCD 代答、Manchester 解码、半双工 turnaround、DS90LV019 工程实现风险。
- A38-DF108-Agilex5：今天主线是确认 A5E 不能直接承接大量 1.2V/1.8V 可变 CMOS IO，并把 168 路 GPIO 问题改写成电压域边界与接口收敛问题。
- cyberlog-workflow：今天没有新的工具代码需求；本日处理使用 raw -> compiled -> validate/close 的现有闭环。

## 1. 今日真实推进

- A57-eDP 的 CR/EQ 失败定位口径被重新定义：当前结构不是标准 sink 根据真实 main-link 结果返回 CR/EQ 状态，而是由 FPGA/control logic 通过 AUX/DPCD 代答 training status；因此在没有 SerDes 状态参与代答的前提下，A57 的 CR/EQ fail 不应优先归因到 SerDes eye，而应先查 AUX/DPCD 模拟状态机、回包完整性、lane count/rate/status 一致性、training 时序和 HPD/AUX timeout/NACK/DEFER。来源：`EDP 问题定位到AUX.md`
- eDP AUX Manchester 解析规则完成整理：常规 AUX 按 Manchester-II、约 1 Mbps、半双工差分控制通道解析；以 AUX+ 单端视角看，0 是 L->H，1 是 H->L；应先用 SYNC 锁 half-UI，再按 bit cell 解码，不应直接用示波器测频当作 AUX bit rate。来源：`eDP v1.4b 的常规 AUX 曼切斯特编码.md`
- AUX UI 容差口径明确：UI_MAN 为 0.4~0.6 us，典型 0.5 us，对应有效数据率约 0.833~1.25 Mbps；若 885 kHz 是 SYNC 区 Manchester 翻转频率，则 UI 约 0.565 us，仍在容差内。来源：`UIMAN.md`, `aux周期 ±20%裕量允许.md`
- DS90LV019 作为 eDP AUX 半双工 PHY 替代的工程边界被写清：它可以作为工程折中，但不是标准 eDP AUX PHY；主要风险不是速度，而是 common-mode、幅度、方向切换、termination/bias、FPGA 侧 1.8V/1.2V 兼容和 turnaround guard time。来源：`DS90LV019 eDP AUX应用特性.md`, `DS90LV019 EN turnaround.md`
- A38-DF108-Agilex5 外部 IO 问题从“168 路怎么做 level shift”升级为“主 FPGA 是否应该直接暴露 168 个可变电平 CMOS pin”：A5E 的 bank 电压无法按外设自动在 1.2V/1.8V 间灵活切换，0R/DNP 装配选择也不符合自动化，优先方向应是固定连接器电平、适配板或 IO bridge/小 FPGA/CPLD，而不是主板上一对一堆 translator。来源：`A5E VDDIO范围.md`, `GPIO 1.2V 1.8V.md`

## 2. 当前工作画布

### Active

- A57-eDP AUX/DPCD training debug：先确认 AUX request/reply 是否按 Manchester-II 正确解析，再比对 DPCD training status 回包是否完整一致，尤其是 0x202/0x203/0x204 等状态与 link rate/lane count/training pattern 写入是否匹配。
- A57-eDP DS90LV019 AUX 实现评估：继续按半双工状态机梳理 DE、RE#、DIN、ROUT、AC coupling、bias、turnaround guard time 和 FPGA 侧 level translation。
- A38-DF108-Agilex5 1.2V/1.8V 外部 IO 架构：继续把 168 路 GPIO 拆成低速可寄存器化、必须低延迟同步、方向可控/不可控几类，决定是固定连接器电平、适配板、IO bridge，还是少量高位宽 translator。

### Queue

- 抓一组成功/失败 AUX transaction，对比 link rate、lane count、training pattern writes、DPCD status reads、AUX NACK/DEFER/timeout 和 HPD 行为。
- 在逻辑分析仪或差分转单端链路上确认 AUX 极性、SYNC、SYNC END/START、STOP 和 half-UI，不直接从随机边沿开始解码。
- 给 DS90LV019 AUX 方案画出 TX_PREPARE、TX_ACTIVE、TURNAROUND、RX_ACTIVE 状态机，并把 DE/RE# 分开控制作为优先方案。
- 对 A38 外部 168 路 IO 做分类表：方向、速率、实时性、是否可寄存器化、是否可协议化、外部 VDDIO 来源、是否需要热插拔/上电隔离。

### Blocked

- A57-eDP CR/EQ 根因冻结：阻塞原因是当前 raw 只说明应优先怀疑 AUX/DPCD 代答路径，还没有成功/失败 AUX transaction 级证据；解除方式是抓取并解码 request/reply，确认 training status 是否被正确返回；owner：硬件 / 逻辑 / 测试；下一步：先抓 0x202/0x203/0x204 相关读写和 AUX 错误类型。
- A57-eDP DS90LV019 AUX 方案冻结：阻塞原因是 common-mode、RX threshold margin、termination/bias、AC coupling、DE/RE# guard time 和 FPGA bank level translation 尚未实测；解除方式是保留 AC coupling/bias/极性/series/测试点选项并上板测 VAUX_DIFF_PP、VAUX_DC_CM、ROUT、DE/RE# 时序；owner：硬件；下一步：先画原理图可选网络和测点。
- A38-DF108-Agilex5 168 路 IO 架构冻结：阻塞原因是尚未确认这些 IO 中哪些必须透明、同步、低延迟，哪些可以寄存器化或协议化；解除方式是按速率/方向/实时性分类，并把主板接口电平固定策略与适配板/IO bridge 方案放到同一张 tradeoff 表；owner：硬件 / 架构；下一步：先完成 IO 分类，不急着选 translator。

### Closed

- “885 kHz 一定不符合 eDP AUX 1 Mbps”这个判断关闭：如果它对应 SYNC 区 Manchester 翻转频率，UI 约 0.565 us，落在 0.4~0.6 us 范围内。
- “A57 CR/EQ fail 优先等同于 SerDes eye fail”这个默认归因关闭：在当前代答 DPCD training status 架构下，必须先查 AUX/DPCD 代答逻辑和 transaction 证据。
- “A5E 主板直接面对 168 路 1.2V/1.8V 可变 CMOS IO”这个方案不作为首选：除非分类后证明必须透明低延迟，否则优先接口标准化、适配板或 IO bridge。

## 3. 关键决策

| 项目 | 决策 | 状态 | 背景 | 理由 | 风险 | 后续动作 | 来源文件 |
|---|---|---|---|---|---|---|---|
| A57-eDP | CR/EQ fail 先按 AUX/DPCD 代答链路排查，而不是直接冻结为 SerDes eye 问题 | proposed | 当前 training status 由 FPGA/control logic 经 AUX/DPCD 代答，不是标准 sink 基于真实 main-link 自动反馈 | 若 SerDes 状态未参与回包，source 读不到 pass status 更可能来自 AUX/DPCD 状态机、回包、时序或错误响应 | 仍可能存在真实 main-link 或电气问题，需要 transaction 证据后再判断 | 抓成功/失败 AUX request/reply，重点比对 0x202/0x203/0x204、lane count、link rate、NACK/DEFER/timeout | `EDP 问题定位到AUX.md` |
| A57-eDP | AUX 解析按 Manchester-II half-UI/SYNC 锁定，不能用示波器测频直接判断 bit rate | validated | eDP/DP AUX 是约 1 Mbps 半双工 Manchester-II transaction | 边沿频率取决于 bit pattern；SYNC 区频率和数据区边沿间隔都不能简单等同 bit rate | 若差分极性接反，0/1 和 STOP/SYNC END 形态会误判 | 先确认极性、SYNC 连续 0、非法 Manchester 边界，再解 command/address/data | `eDP v1.4b 的常规 AUX 曼切斯特编码.md`, `UIMAN.md`, `aux周期 ±20%裕量允许.md` |
| A57-eDP | DS90LV019 可作为 AUX 工程折中，但必须按非标准 AUX PHY 处理 | proposed | DS90LV019 不是标准 eDP AUX PHY，需外部处理半双工方向、common-mode、bias 和 FPGA level | 速度不是主风险；真正风险在电气窗口、turnaround、接收阈值、默认使能和上电状态 | RX margin、common-mode 和总线争用可能导致偶发失败 | 原理图保留 AC coupling/bias/series/极性选项，DE/RE# 分开控制，guard time 先按 0.5~2 us 设计并实测 | `DS90LV019 eDP AUX应用特性.md`, `DS90LV019 EN turnaround.md` |
| A38-DF108-Agilex5 | 168 路可变 1.2V/1.8V CMOS IO 不应默认一对一堆 translator | proposed | A5E bank 电压不能自动适配外部设备，0R/DNP 也不适合自动化选择 | 更稳的工程问题定义是固定接口电平、适配板或 IO bridge/小 FPGA 做电压域边界 | 如果 168 路全是高速同步透明信号，IO bridge/寄存器化可能不成立 | 先给 168 路 IO 做方向/速率/实时性/可寄存器化分类，再决定架构 | `A5E VDDIO范围.md`, `GPIO 1.2V 1.8V.md` |

## 4. 重要信息

- A57-eDP AUX transaction 解析时，应寻找 Idle/Precharge、SYNC、SYNC END/START、Command/Address/Length/Data、STOP、Turnaround、Reply SYNC、Reply Data、STOP 这条链路。
- 以 AUX+ 极性观察时，Manchester-II bit 0 是 L->H，bit 1 是 H->L；如果极性反了，SYNC END/STOP 形态会异常，应先尝试逻辑反相或检查差分输入接法。
- DS90LV019 输入侧 DIN/DE/RE# 和 ROUT 电平不适合直接连到 1.8V/1.2V FPGA bank，需要单向 level translator；不要用 I2C 自动双向 translator 处理这种方向明确的控制/数据线。
- DS90LV019 方向控制建议分离 DE 和 RE#，TX 时 DE=1、RE#=1，RX 时 DE=0、RE#=0，中间留 guard time 并清 RX FIFO/边沿检测，避免残余边沿误判。
- A38 外部 IO 最有价值的重构问题是：哪些 pin 可以被寄存器化、状态机化、串行化，而不是让主 FPGA 直接处理 168 路可变电平世界。

## 5. 今日产出

- A57-eDP AUX 根因定位口径：属于 A57-eDP；来源 `EDP 问题定位到AUX.md`；可复用价值是把后续测试优先级从 SerDes 眼图单点怀疑转到 AUX/DPCD transaction 证据。
- A57-eDP AUX Manchester 解码手册：属于 A57-eDP；来源 `eDP v1.4b 的常规 AUX 曼切斯特编码.md`, `UIMAN.md`, `aux周期 ±20%裕量允许.md`；可复用价值是现场抓波形时能先判断 UI、极性、SYNC 和 STOP。
- A57-eDP DS90LV019 AUX 方案边界：属于 A57-eDP；来源 `DS90LV019 eDP AUX应用特性.md`, `DS90LV019 EN turnaround.md`；可复用价值是原理图评审时能直接检查 DE/RE#、AC coupling、bias、level shift 和测试点。
- A38-DF108-Agilex5 外部 IO 架构判断：属于 A38-DF108-Agilex5；来源 `A5E VDDIO范围.md`, `GPIO 1.2V 1.8V.md`；可复用价值是避免直接进入 translator 堆料，把问题上移到接口标准化、适配板和 IO bridge tradeoff。

## 6. 未完成任务

| 任务 | 所属项目 | 下一步动作 | 优先级 | 是否适合交给 AI / agent | 为什么 |
|---|---|---|---|---|---|
| 抓取并解码 AUX training transaction | A57-eDP | 比对成功/失败下 link rate、lane count、training pattern writes、0x202/0x203/0x204 status reads、NACK/DEFER/timeout | P0 | 部分适合 | AI 可做解码/checklist，波形采集需现场执行 |
| 画 DS90LV019 AUX 半双工状态机 | A57-eDP | 明确 IDLE/TX_PREPARE/TX_ACTIVE/TURNAROUND/RX_ACTIVE 的 DE/RE#/DIN/ROUT 行为 | P0 | 适合 | raw 已给状态机雏形，AI 可整理成评审图和时序表 |
| 设计 DS90LV019 原理图可选网络 | A57-eDP | 预留 AC coupling、bias、polarity swap、series、测试点、DE 默认下拉和 ROUT 隔离策略 | P0 | 部分适合 | AI 可出检查表，最终需硬件评审 |
| 168 路外部 IO 分类 | A38-DF108-Agilex5 | 按方向、速率、实时性、是否可寄存器化、是否可协议化、VDDIO 来源建表 | P0 | 适合 | AI 可直接基于信号表生成分类模板 |
| A38 外部 IO 架构 tradeoff | A38-DF108-Agilex5 | 比较固定连接器电平、适配板、IO bridge/小 FPGA、高位宽 translator 四种方案 | P1 | 适合 | 今日 raw 已有方案边界，AI 可形成评审材料 |
| 确认 A5E bank/VDDIO 约束和正式器件型号 | A38-DF108-Agilex5 | 用官方 pinout/Quartus/FAE 复核 HSIO/HVIO/SDM VCCIO 和最终 ordering code | P0 | 部分适合 | AI 可整理证据，最终必须以官方工具/FAE 为准 |

## 7. 明日启动包

见 `Daily/compiled/2026-05-13/_tomorrow-boot.md`。

## 8. 工作流摩擦

- 现象：A57-eDP 问题很容易被“CR/EQ fail”这个表象带回 SerDes 眼图路径。可能原因：训练失败的最终显示在 CR/EQ，但当前架构中 source 看到的训练状态来自 AUX/DPCD 代答。影响：会漏掉状态机、回包、时序和 AUX 错误响应。明天修正动作：先抓 transaction 证据，再讨论是否回到 main-link 电气层。
- 现象：AUX 频率描述容易混淆 bit rate、half-UI 和边沿频率。可能原因：示波器测频不是协议解码。影响：可能误判 885 kHz 为不合规。明天修正动作：统一使用 UI_MAN、SYNC、STOP 和 Manchester cell 口径。
- 现象：DS90LV019 方案容易被当作“普通差分收发器够速率就行”。可能原因：速度指标直观，但 AUX 真正的风险在非标准 PHY 电气和半双工方向控制。影响：原理图可能漏掉 bias、AC coupling、level translation 和 guard time。明天修正动作：评审时按电气、方向、上电、测试点四类检查。
- 现象：A38 外部 168 路 IO 容易直接进入电平转换芯片选型。可能原因：raw 问题最初表达为 1.2V/1.8V level shift。影响：可能错过接口标准化和协议收敛这个更低人工维护成本的方案。明天修正动作：先做 IO 分类和架构 tradeoff，再选器件。

## 9. 自我迭代建议

1. 以后 raw 中出现 `#可信` 或 `#待验证` 时，daily 整理优先用它们区分事实层级；未标注且像推测的内容默认按 proposed/待验证处理。
2. A57-eDP 后续所有波形记录都要同时写 `采样点/极性/half-UI/SYNC/STOP/AUX错误类型`，减少整理时二次追问。
3. A38-DF108-Agilex5 后续所有大规模 IO 讨论，先填 `能否寄存器化/能否协议化/是否必须透明低延迟`，再进入 translator 或 bridge 器件选择。

## 10. 规则候选

### 规则候选 1
- 触发条件：debug 现象表现为协议训练失败，但系统中存在代答/模拟状态机。
- 规则：先追踪 source 实际读到的状态从哪里来，再决定是查电气层、协议层还是代答逻辑；不要只按最终错误名归因。
- 原因：最终错误名可能只是上层看到的失败结果，不代表真实故障层。
- 例子：今天 A57-eDP CR/EQ fail 更应先查 AUX/DPCD 代答路径。
- 是否建议写入 System/workflow-rules.md：yes

### 规则候选 2
- 触发条件：涉及大规模可变电压 GPIO 或高 pin 数 level shift。
- 规则：先判断接口能否标准化、适配板化、寄存器化或协议化；只有证明必须透明低延迟后，才进入一对一 translator 方案。
- 原因：堆 translator 会把方向、上电、SI、skew、维护成本全部留在主板。
- 例子：今天 A38-DF108-Agilex5 的 168 路 1.2V/1.8V CMOS IO 不应默认主板一对一转换。
- 是否建议写入 System/workflow-rules.md：yes
