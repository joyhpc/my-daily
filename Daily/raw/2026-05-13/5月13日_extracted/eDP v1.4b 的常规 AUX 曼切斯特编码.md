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