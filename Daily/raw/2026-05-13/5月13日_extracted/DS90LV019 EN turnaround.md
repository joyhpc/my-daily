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