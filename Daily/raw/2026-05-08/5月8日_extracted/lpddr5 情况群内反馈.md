 各位同步一下 LPDDR5 / LPDDR5X 采购寻样与方案评估进展。

  一、原 DF108 DDR4 方案回顾

  之前 DF108 最大线速支持 2.5Gbps/lane，摄像头端最大数据量约 80Gbps。

  原方案使用 4 颗 16bit DDR4：H5AN4G6NBJR
  - 颗粒配置：4Gb / x16 × 4
  - 总位宽：64bit
  - 总容量：2GB
  - 理论峰值带宽：约 153.6Gbps

  二、当前 Altera / Agilex 方案需求

  当前方案最大线速提升到 4Gbps/lane，摄像头端最大数据量约 128Gbps。

  原计划使用：
  - 2 颗 LPDDR5
  - 单颗规格：2GB / 16Gb，x32
  - 总位宽：64bit
  - 总容量：4GB
  - 按主控侧约 3733MT/s 计算，理论峰值带宽约 239Gbps

  该带宽相对 128Gbps 摄像头端输入有一定余量。

  三、采购寻样反馈

  原始寻样需求是：
  - 单颗 2GB / 16Gb
  - x32 位宽
  - LPDDR5 或 LPDDR5X
  - 商业级即可
  - 希望未来 5–8 年无 EOL 风险

  目前供应商反馈来看，暂时还没有找到完全匹配 2GB x32 且长期供货稳定的料号。

  1. 美光
  - 旧款 2GB x32 相关料号存在 EOL / 停产风险，不适合作为长期项目方案。
  - 目前比较明确、可继续评估的候选料号是：
    MT62F1G32D2DS-020 WT:D
  - 规格大致为：
    LPDDR5X，单颗 4GB / 32Gb，x32，9600Mbps/pin，315-ball TFBGA。
  - 该料号容量高于原始需求，速率也高于当前主控侧计划使用速率，需要按降频使用评估。

  2. 三星
  - 之前代理反馈的 245-ball LP5X 更偏消费类，生命周期通常 2–3 年，不能直接满足 5–8 年长期供货要求。
  - 但三星路线不建议完全排除。LPDDR5/LPDDR5X 本身很多料号都是移动端/消费类供货模式，不管哪个品牌都需要单独确认生命周期和 PCN/EOL 机制，不能只因为“消费级”就
  排除三星。
  - 公开资料里能看到三星也有 32Gb / x32 / 315 FBGA 的 LPDDR5X 料号，例如：
    K3KL8L80QM-MFCT：32Gb，x32，315 FBGA，7500Mbps，-40~95°C，量产状态
    K3KL8L80CM-MGCT：32Gb，x32，315 FBGA，7500Mbps，-25~85°C，量产状态
  - 所以建议采购继续找三星正式渠道或其他代理确认 315FBGA、x32、32Gb 这类料号的供货、价格、生命周期和样品情况。三星可以作为并行优先候选，而不是直接关闭。

  3. 南亚
  - 反馈目前没有 LPDDR5 可供选择。

  4. 海力士
  - 当前代理未有效响应，暂时没有可用反馈。
  - 建议继续找其他海力士渠道确认是否有 32Gb / x32 / LPDDR5X / 315FBGA 或类似规格可供。

  四、市场替代料初筛

  目前可以并行询价/确认的方向如下：

  A. 三星优先候选
  - K3KL8L80QM-MFCT
    32Gb / x32 / LPDDR5X / 315 FBGA / 7500Mbps / -40~95°C / 量产
  - K3KL8L80CM-MGCT
    32Gb / x32 / LPDDR5X / 315 FBGA / 7500Mbps / -25~85°C / 量产
  - K3KL8L80DM-MFCU
    32Gb / x32 / LPDDR5X / 315 FBGA / 8533Mbps / -40~95°C / 样品
  - K3KL8L80EM-MHCV
    32Gb / x32 / LPDDR5X / 315 FBGA / 9600Mbps / -40~105°C / 样品

  B. 美光候选
  - MT62F1G32D2DS-020 WT:D
    32Gb / x32 / LPDDR5X / 315-ball TFBGA / 9600Mbps/pin
  - 美光这条资料最明确，但容量同样是 4GB 起步，需要确认成本和生命周期。

  五、当前主要风险点

  1. 容量高于实际需求，价格可能更贵
  原计划是 2 颗 2GB x32，总容量 4GB。
  如果改用 32Gb / 4GB x32 颗粒，则 2 颗组成 x64 后整板 LPDDR 容量变为 8GB。
  项目侧需要确认是否接受容量从 4GB 上浮到 8GB。

  2. 速率匹配风险
  美光候选是 9600Mbps/pin，三星候选有 7500 / 8533 / 9600Mbps 等不同档位。
  当前主控侧计划约 3733MT/s，需要确认这些高速料号是否可以稳定降频使用。

  3. 封装与布局风险
  优先考虑 315 FBGA / 315-ball TFBGA 这类更接近 FPGA 高速存储应用的封装。
  需要进一步确认：
  - Agilex 5 EMIF 是否支持该器件配置
  - Bank / pin / byte lane 分配是否可行
  - PCB 扇出、层数、阻抗、等长约束是否可接受

  4. 生命周期风险
  本项目希望 5–8 年供货稳定，所以无论美光、三星还是海力士，都必须让供应商明确提供：
  - 生命周期 / Longevity
  - EOL 风险
  - PCN/EOL 通知周期
  - 样品交期
  - 量产交期
  - MOQ / MPQ
  - 价格阶梯

  六、建议下一步动作

  1. 采购侧
  请继续并行确认美光和三星：
  - 美光：MT62F1G32D2DS-020 WT:D
  - 三星：优先问 K3KL8L80QM-MFCT / K3KL8L80CM-MGCT，以及是否有更适合长期供货的 32Gb x32 315FBGA LPDDR5X 料号

  重点确认：
  - 生命周期 / Longevity
  - 是否有明确 EOL 风险
  - 商业级或工业级温度等级
  - 单价
  - 样品交期
  - 量产交期
  - MOQ / MPQ
  - 是否有长期供货承诺或 PCN/EOL 通知周期

  2. 项目侧
  需要确认是否接受容量调整：
  - 原计划：2 颗 2GB x32，总容量 4GB
  - 当前主流候选：2 颗 4GB x32，总容量 8GB

  如果容量上浮对成本、软件地址空间、启动初始化、功耗没有明显负面影响，可以把 32Gb / x32 LPDDR5X 作为当前主方向继续评估。

  3. 逻辑 / FPGA 侧
  建议先选 1 个美光候选和 1 个三星候选，做 Quartus EMIF / Pin Planner / Fitter 验证：
  - 美光：MT62F1G32D2DS-020 WT:D
  - 三星：优先 K3KL8L80QM-MFCT 或 K3KL8L80CM-MGCT

  重点确认：
  - Agilex 5 是否支持该 LPDDR5X 器件配置
  - x32 × 2 组成 x64 是否可行
  - Bank 资源是否足够
  - Pin 分配是否能收敛
  - Fitter 是否能通过
  - 目标速率下时序是否有可实现性

  4. 硬件侧
  在 Quartus EMIF / Pin Planner / Fitter 验证完成前，建议暂时不要冻结 LPDDR5 pin list。
  LPDDR5/LPDDR5X 的 pin 分配会直接影响 Bank 选择、字节组、走线拓扑、扇出和 SI 约束，建议等 FPGA 侧初步验证通过后，再进入原理图与 PCB 约束冻结。

  公开资料我查到的三星备选主要来自三星半导体官网：K3KL8L80QM-MFCT 是 32Gb、x32、315 FBGA、7500Mbps、-40~95°C、量产；K3KL8L80CM-MGCT 是 32Gb、x32、315
  FBGA、7500Mbps、-25~85°C、量产；K3KL8L80EM-MHCV 是 32Gb、x32、315 FBGA、9600Mbps、-40~105°C、样品；K3KL8L80DM-MFCU 是 32Gb、x32、315 FBGA、
  8533Mbps、-40~95°C、样品。Micron 公共渠道也能看到同系列 32Gbit x32 315-TFBGA 料号，但库存/价格状态需要采购再确认。来源：三星官网 K3KL8L80QM-MFCT、
  K3KL8L80CM-MGCT、K3KL8L80EM-MHCV、K3KL8L80DM-MFCU 页面，以及 DigiKey 的 Micron MT62F1G32D2DS-020 AUT:F 页面。


