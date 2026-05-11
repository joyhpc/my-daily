  1. SDM 是什么
  SDM = Secure Device Manager，是 Agilex 5 内部负责配置、启动、安全认证、加密、RSU、SmartVID/PMBus 等功能的配置管理子系统。

  SDM_IOx 就是被 SDM 管理的配置相关管脚。上电配置阶段这些 pin 先归 SDM 控制，部分 pin 后续可以按 Quartus 设置变成应用逻辑或可选配置功能。

  2. AS_DATA / AS_CLK 是什么
  AS = Active Serial，可以理解为 Intel/Altera 的“FPGA 主动从 QSPI flash 读取 bitstream 启动”。

  对应关系：

  | Agilex 5 AS 信号 | 含义 | QSPI flash 侧 |
  |---|---|---|
  | AS_CLK | SDM 输出给 flash 的配置时钟 | Flash CLK/SCK |
  | AS_DATA0 | QSPI 数据 0 | Flash IO0 / SI / DQ0 |
  | AS_DATA1 | QSPI 数据 1 | Flash IO1 / SO / DQ1 |
  | AS_DATA2 | QSPI 数据 2 | Flash IO2 / WP# / DQ2 |
  | AS_DATA3 | QSPI 数据 3 | Flash IO3 / HOLD# / DQ3 |
  | AS_nCSO0 | 第 0 片 flash 片选 | Flash CS# |
  | AS_nRST | SDM 控制的 flash reset | Flash RESET# |

  Agilex 5 的 AS 只支持 AS x4。官方指南里 AS x4 required signals 就是 AS_CLK、AS_DATA[3:0]、AS_nCSO[3:0]、AS_nRST、MSEL[2:0]、nCONFIG、nSTATUS。

  3. Xilinx 的 PROGRAM_B 对应 Agilex 哪个？
  最接近的是：

  | Xilinx XCKU | Agilex 5 |
  |---|---|
  | PROGRAM_B | nCONFIG |

  两者都是 低有效，触发重新配置/清空配置流程 的控制脚。
  所以你画原理图时，如果脑子里有 Xilinx PROGRAM_B，在 Agilex 5 这边看 nCONFIG。

  4. A5ED065B B32A SDM/QSPI 与 XCKU 配置区功能对比

  | 功能 | A5ED065B B32A / Agilex 5 | Ball | Xilinx XCKU 对应 | 是否一一对应 |
  |---|---|---:|---|---|
  | JTAG clock | TCK | CA109 | TCK | 是 |
  | JTAG mode | TMS | CA112 | TMS | 是 |
  | JTAG data in | TDI | BW112 | TDI | 是 |
  | JTAG data out | TDO | BW109 | TDO | 是 |
  | 重新配置控制 | nCONFIG | BU99 | PROGRAM_B | 功能等价 |
  | 配置状态/错误 | nSTATUS | BW99 | INIT_B | 近似等价 |
  | 配置完成 | CONF_DONE on SDM_IO16 | BP102 | DONE | 近似等价 |
  | 用户模式完成 | INIT_DONE on SDM_IO0 | CA99 | 无完全等价 dedicated pin | 不完全对应 |
  | 配置模式选择 | MSEL[2:0] | 复用在 SDM_IO5/7/9 | M[2:0] | 功能等价，但物理实现不同 |
  | SPI/QSPI 时钟 | AS_CLK on SDM_IO2 | BK99 | CCLK | 功能等价 |
  | QSPI IO0 | AS_DATA0 on SDM_IO4 | BH99 | D00_MOSI | 功能等价 |
  | QSPI IO1 | AS_DATA1 on SDM_IO1 | BK102 | D01_DIN | 功能等价 |
  | QSPI IO2 | AS_DATA2 on SDM_IO3 | CH99 | D02 | 功能等价 |
  | QSPI IO3 | AS_DATA3 on SDM_IO6 | CF102 | D03 | 功能等价 |
  | Flash CS0 | AS_nCSO0 / MSEL0 on SDM_IO5 | CF112 | FCS_B | 功能等价，但 Intel 复用 MSEL0 |
  | Flash CS1/2/3 | AS_nCSO1/2/3 | BM102/BM99/CC102 | Xilinx x8/多 flash 相关 CS | 不严格一一对应 |
  | Flash reset | AS_nRST on SDM_IO15 | CA102 | 无直接 dedicated 等价 | Intel 特有 |
  | 外部配置参考时钟 | OSC_CLK_1 | BR102 | EMCCLK | 近似，不完全等价 |
  | SDM 参考电阻 | RREF_SDM | CL103 | 无 | Intel 特有 |
  | SmartVID/PMBus | PWRMGT_SCL/SDA | CF109/CF99 | 无 XCKU dedicated 等价 | Intel 特有 |
  | 配置 bank 电压选择 | 无同类 pin | - | CFGBVS | Xilinx 特有 |
  | 配置期间上拉控制 | 无同类 pin | - | PUDC_B | Xilinx 特有 |
  | 电池密钥备份 | 无同类 pin | - | VBATT | Xilinx 特有 |

  5. 一个关键差异
  Intel 的 MSEL0/1/2 和 AS_nCSO0/2/1 是复用关系：上电时先作为 MSEL 采样，采样后变成 flash chip select。

  Xilinx XCKU 的 M[2:0] 和 SPI flash FCS_B 是分开的 pin。
  所以这里不能按名字逐脚照搬 Xilinx 原理图，只能按功能迁移。

  6. 可靠性结论
  这个对比在“功能层面”可靠，依据是：

  - Intel/Altera Agilex 5 Device Configuration User Guide
  - Intel/Altera A5ED065B B32A 官方 pinout
  - Intel/Altera 065B B32A 官方开发板 SOM 原理图
  - AMD/Xilinx UG570 UltraScale Configuration User Guide

  但 XCKU 侧我现在只能做通用 XCKU 系列功能对比，不能给 Xilinx ball number。要做 ball-to-ball 表，需要具体 XCKU 料号和封装，比如 XCKU040-FFVA1156 这种。
