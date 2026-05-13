
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