  1. Power Tree 必须重做
     Agilex 5 的 power rail、sequencing、monitor、SmartVID/PMBus 等不能沿用 KU040。Intel 官方 Power Management Guide 明确把 power tree、power estimation、
     power generation、I/O sequencing 作为设计阶段内容。
  2. Pin / bank / transceiver 必须先规划再画图
     Intel Pin Connection Guidelines 覆盖 FPGA core pins、GTS transceiver pins、HPS pins、power sharing 等。你应该先用官方 pinout + Quartus pin planning 固
     化 bank/VCCIO/refclk/GTS，再回到原理图，不要先凭封装页连线。
  3. Boot 模式是架构决策，不是原理图细节
     Agilex 5 SoC 有 FPGA Configuration First 和 HPS Boot First 这类路径。官方 HPS boot 文档说明 FPGA first 会先完成 FPGA/I/O 配置再释放 HPS；这更接近
     KU040 原 fabric-centric 产品的迁移节奏。
  4. 外设保持矩阵是主线
     8 路 FAKRA、POC、DPS、机壳、光口物理形态是硬约束。每个接口都要有一张表：


