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


