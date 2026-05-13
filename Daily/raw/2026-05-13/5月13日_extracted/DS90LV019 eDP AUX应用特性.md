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