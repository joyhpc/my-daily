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