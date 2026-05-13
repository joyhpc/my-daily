# Tomorrow Boot Packet — 2026-05-14

## 明日主线

- A57-eDP：抓并解码 AUX training transaction，优先证明 source 实际读到的 DPCD training status 是否正确。
- A38-DF108-Agilex5：把 168 路外部 IO 从“选 translator”推进到“接口分类 + 架构 tradeoff”。

## 背景

- 5/13 的判断是：A57 当前 CR/EQ 失败不能直接等同 SerDes eye 失败，因为 training status 由 FPGA/control logic 通过 AUX/DPCD 代答；先查 AUX/DPCD transaction。
- eDP AUX 应按 Manchester-II、half-UI、SYNC、STOP、turnaround 解析；885 kHz 如果对应 SYNC 区翻转，仍可能在 UI_MAN 容差内。
- DS90LV019 可以作为工程折中，但不是标准 AUX PHY；评审重点是 common-mode、接收阈值、bias、AC coupling、DE/RE#、guard time、FPGA 侧 level translation。
- A38 外部 168 路 1.2V/1.8V CMOS IO 不应默认一对一堆 translator；先确认哪些信号能寄存器化、协议化或通过适配板解决。

## 当前状态

- A57-eDP 有清晰怀疑路径，但缺 transaction 级证据。
- DS90LV019 的方向状态机和原理图可选网络还没固化。
- A38-DF108-Agilex5 已确认 A5E bank 电压不能自动适配大量外部 1.2V/1.8V 设备，下一步要做 IO 分类。

## 第一动作

- 先做一张 AUX transaction 采集表：成功/失败、link rate、lane count、training pattern writes、0x202/0x203/0x204 reads、reply type、NACK/DEFER/timeout、HPD 状态、是否能看到 SYNC/STOP。
- 如果今天只能做一个 A38 动作，就先把 168 路 IO 按方向、速率、实时性、可寄存器化、可协议化、VDDIO 来源分类。

## 注意事项

- 不要直接用 CR/EQ fail 的名字反推 SerDes eye root cause。
- 不要用示波器测频替代 AUX Manchester 解码。
- DS90LV019 的速度不是首要风险；先看电气窗口、方向控制和上电默认状态。
- A38 的 translator 数量不是第一问题；接口边界和人工维护成本才是第一问题。

## 不要重复踩的坑

- 不要把 `885 kHz` 简化成“不满足 1 Mbps”。
- 不要把 raw 里的建议写成 frozen decision。
- 不要把 DS90LV019 当作标准 eDP AUX PHY。
- 不要在 168 路 IO 未分类前直接锁定高位宽 translator 方案。

## 可以交给 AI / agent 的部分

- 根据 AUX raw 生成 transaction decode checklist。
- 把 DS90LV019 半双工状态机整理成时序表和原理图评审 checklist。
- 生成 A38 168 路 IO 分类模板和四方案 tradeoff 表。

## 必须由我亲自判断的部分

- 是否接受 DS90LV019 作为非标准 AUX PHY 的工程风险。
- A57-eDP transaction 证据是否足以改变根因优先级。
- A38 外部 IO 是否允许改接口规范、增加适配板或引入 IO bridge。
