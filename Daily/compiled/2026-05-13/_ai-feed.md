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
