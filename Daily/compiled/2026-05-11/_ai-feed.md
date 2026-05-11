<file path="Daily/raw/2026-05-11/5月11日_extracted/A38 + Agilex5方案原理图设计规划.md">
天数 主要目标  
Day 1 系统框图、电源树图、FPGA 主芯片分页、GPIO bank 分配  
Day 2 LPDDR5 x32 两组颗粒选型、封装制作、LPDDR5 模块原理图、EMIF pin assign  
Day 3 电源口、系统电源及时序、clock/reset/config、外设  
Day 4 依据 checklist 进行全图检查，特别是 Pin Plan / EMIF / power sequence 这一块

</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/A5ED052AB32AE2V FAE 沟通.md">
你可以直接这样问 FAE，重点是让他给官方确认和推荐电源方案，不要只口头说“可以”。

  邮件/微信内容模板

  主题：请确认 A5ED052AB32AE2V SmartVID/PMBus 电源方案

  FAE 您好，

  我们当前项目计划使用：

  A5ED052AB32AE2V

  封装：B32A
  启动方式：外部 QSPI Flash，AS x4 Normal mode
  配置相关计划：

  - PWRMGT_SCL = SDM_IO14 / CF109
  - PWRMGT_SDA = SDM_IO11 / CF99
  - CONF_DONE = SDM_IO16 / BP102
  - INIT_DONE = SDM_IO0 / CA99
  - nCONFIG = BU99
  - nSTATUS = BW99
  - OSC_CLK_1 = BR102，计划 125 MHz / 1.8V
  - RREF_SDM = CL103，2.00k 1% to GND

  我们查到 Agilex 5 -2V 属于 SmartVID 器件，VCC/VCCP 需要使用 PMBus-compliant regulator 配合 SmartVID，不能用固定输出 regulator。请帮忙确认以下几点：

  1. A5ED052AB32AE2V 是否必须使用 SmartVID / PMBus regulator 给 VCC/VCCP 供电？
  2. VCC 和 VCCP 是否推荐合并为同一个 SmartVID rail？初始电压是否设为 0.80V？
  3. 对该器件，推荐的 PMBus regulator 型号是什么？
     我们优先考虑官方 fully validated 器件，例如 TPS53676 / LTC3882-1 / ISL68223，请给推荐优先级。
  4. 如果使用 TPS53676，请确认 Quartus/board 侧推荐配置：
      - VID_OPERATION_MODE = PMBus Master
      - PWRMGT_SCL = SDM_IO14
      - PWRMGT_SDA = SDM_IO11
      - PMBus speed 初版是否建议 100 kHz
      - voltage format、address、PAGE 设置是否有参考值
  5. PWRMGT_ALERT 在 PMBus Master mode 下是否可以不接？
     我们计划将 BR99 / SDM_IO12 预留为 TP/DNP 或 CAT_TRIP_N/PWRMGT_ALERT 兼容位。
  6. VCCLSENSE / GNDSENSE 是否必须接到 VCC/VCCP regulator 的 remote sense？
     推荐连接点是在 FPGA 负载点还是 regulator 输出端？
  7. 是否有针对 A5ED052AB32AE2V B32A 的官方参考设计、PDN checklist、power tree 示例或 Quartus .qsf 示例可以提供？
  8. 请确认 OSC_CLK_1 = 125 MHz / 1.8V 是否适合本方案，是否有推荐 XO 型号或 jitter/startup 要求。
  9. 请确认 AS x4 Normal mode 的 MSEL 配置是否为 MSEL[2:0]=011：
      - MSEL0 / CF112 上拉
      - MSEL1 / BM99 上拉
      - MSEL2 / BM102 下拉

  请尽量提供对应 Intel/Altera 官方文档章节或 design example，方便我们归档到原理图评审记录。

  谢谢。

  附件建议发给 FAE

  附上这三个文件：

  10. /home/ubuntu/misc-tasks/a5ed052a_min_system_pin_assign/deliverables/a5ed052a_b32a_min_system_pin_assign_draft_v2.xlsx
  11. 官方 pinout：a5ed052A.xlsx
  12. 你当前电源树草图，哪怕是手画 block diagram 也可以

  问法重点

  让 FAE 必须回答这几句：

  - A5ED052AB32AE2V 是否必须 SmartVID
  - 推荐哪个 PMBus regulator
  - VCC/VCCP 是否同 rail
  - PWRMGT_SCL/SDA/ALERT 怎么接
  - 是否给官方参考设计/QSF/PDN checklist

  这样问，FAE 的回答可以直接作为设计依据归档。
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/A5ED065B B32A SDM  与 XCKU 配置区功能对比.md">


| 功能               | A5ED065B B32A / Agilex 5    |                 Ball | Xilinx XCKU 对应            | 是否一一对应                |
| ---------------- | --------------------------- | -------------------: | ------------------------- | --------------------- |
| JTAG clock       | TCK                         |                CA109 | TCK                       | 是                     |
| JTAG mode        | TMS                         |                CA112 | TMS                       | 是                     |
| JTAG data in     | TDI                         |                BW112 | TDI                       | 是                     |
| JTAG data out    | TDO                         |                BW109 | TDO                       | 是                     |
| 重新配置控制           | nCONFIG                     |                 BU99 | PROGRAM_B                 | 功能等价                  |
| 配置状态/错误          | nSTATUS                     |                 BW99 | INIT_B                    | 近似等价                  |
| 配置完成             | CONF_DONE on SDM_IO16       |                BP102 | DONE                      | 近似等价                  |
| 用户模式完成           | INIT_DONE on SDM_IO0        |                 CA99 | 无完全等价 dedicated pin       | 不完全对应                 |
| 配置模式选择           | MSEL[2:0]                   |      复用在 SDM_IO5/7/9 | M[2:0]                    | 功能等价，但物理实现不同          |
| SPI/QSPI 时钟      | AS_CLK on SDM_IO2           |                 BK99 | CCLK                      | 功能等价                  |
| QSPI IO0         | AS_DATA0 on SDM_IO4         |                 BH99 | D00_MOSI                  | 功能等价                  |
| QSPI IO1         | AS_DATA1 on SDM_IO1         |                BK102 | D01_DIN                   | 功能等价                  |
| QSPI IO2         | AS_DATA2 on SDM_IO3         |                 CH99 | D02                       | 功能等价                  |
| QSPI IO3         | AS_DATA3 on SDM_IO6         |                CF102 | D03                       | 功能等价                  |
| Flash CS0        | AS_nCSO0 / MSEL0 on SDM_IO5 |                CF112 | FCS_B                     | 功能等价，但 Intel 复用 MSEL0 |
| Flash CS1/2/3    | AS_nCSO1/2/3                | BM102 / BM99 / CC102 | Xilinx x8 / 多 Flash 相关 CS | 不严格一一对应               |
| Flash reset      | AS_nRST on SDM_IO15         |                CA102 | 无直接 dedicated 等价          | Intel 特有              |
| 外部配置参考时钟         | OSC_CLK_1                   |                BR102 | EMCCLK                    | 近似，不完全等价              |
| SDM 参考电阻         | RREF_SDM                    |                CL103 | 无                         | Intel 特有              |
| SmartVID / PMBus | PWRMGT_SCL / PWRMGT_SDA     |         CF109 / CF99 | 无 XCKU dedicated 等价       | Intel 特有              |
| 配置 bank 电压选择     | 无同类 pin                     |                    - | CFGBVS                    | Xilinx 特有             |
| 配置期间上拉控制         | 无同类 pin                     |                    - | PUDC_B                    | Xilinx 特有             |
| 电池密钥备份           | 无同类 pin                     |                    - | VBATT                     | Xilinx 特有             |
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/A5ED065B B32A启动配置.md">
要从外部 QSPI flash 启动，A5ED052A/A5ED065B 这里应配置成 AS x4 Normal mode。

  核心设置：

  | 项目 | 设置 |
  |---|---|
  | 配置模式 | AS x4 Normal |
  | MSEL[2:0] | 011 |
  | 数据宽度 | x4 |
  | 推荐 flash | 1.8V QSPI flash，接到 VCCIO_SDM 域 |
  | Quartus 配置 | Device and Pin Options 里选 Active Serial / AS Normal |

  具体硬件连接：

  | FPGA ball | SDM pin | AS/QSPI 功能 | 连接 |
  |---:|---|---|---|
  | BK99 | SDM_IO2 | AS_CLK | Flash CLK/SCK |
  | BH99 | SDM_IO4 | AS_DATA0 | Flash IO0/DQ0 |
  | BK102 | SDM_IO1 | AS_DATA1 | Flash IO1/DQ1 |
  | CH99 | SDM_IO3 | AS_DATA2 | Flash IO2/DQ2 |
  | CF102 | SDM_IO6 | AS_DATA3 | Flash IO3/DQ3 |
  | CF112 | SDM_IO5 | AS_nCSO0 / MSEL0 | Flash CS#，同时 4.7k 上拉到 VCCIO_SDM |
  | CA102 | SDM_IO15 | AS_nRST | Flash RESET#，不要再接外部 host 控制 |
  | BM99 | SDM_IO7 | AS_nCSO2 / MSEL1 | 单 flash 时不接 flash，4.7k 上拉 |
  | BM102 | SDM_IO9 | AS_nCSO1 / MSEL2 | 单 flash 时不接 flash，4.7k 下拉 |
  | CC102 | SDM_IO8 | AS_nCSO3 | 单 flash 时可 TP/DNP，按 unused rule 处理 |

  所以 MSEL 电阻就是：

  | MSEL | Ball | 电平 | 电阻 |
  |---|---:|---|---|
  | MSEL0 | CF112 | 1 | 4.7k 上拉到 VCCIO_SDM |
  | MSEL1 | BM99 | 1 | 4.7k 上拉到 VCCIO_SDM |
  | MSEL2 | BM102 | 0 | 4.7k 下拉到 GND |

  也就是：MSEL[2:0] = 011。

  同时建议保留这些配置调试信号：

  | FPGA ball | 功能 | 建议 |
  |---:|---|---|
  | BU99 | nCONFIG | 10k 上拉到 VCCIO_SDM，可接 supervisor/debug |
  | BW99 | nSTATUS | 10k 上拉到 VCCIO_SDM，拉到测试点或 supervisor |
  | BP102 | CONF_DONE | 建议接测试点/supervisor |
  | CA99 | INIT_DONE | 建议接测试点/supervisor |
  | BR102 | OSC_CLK_1 | 接 1.8V free-running clock，参考板用 125 MHz |
  | CL103 | RREF_SDM | 2.00k 1% 到 GND |
  

  注意两点：

  1. MSEL0/1/2 上电采样后，会复用成 AS_nCSO0/2/1，所以 CF112 既是 MSEL0 又是 flash CS#。
  2. AS Normal 要求 VCCIO_SDM 在规定时间内稳定，官方文档写的是 10 ms；如果你没有强约束全电源 10 ms 内稳定，不要选 AS Fast。

  可靠性：这个配置是确认可靠的，来自 Altera 官方配置指南、A5ED052A/A5ED065B B32A 官方 pinout，以及 065B 官方 SOM 原理图的实际连接。
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/Agilex5和XCKU的SDM对比.md">
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
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/RREF_SDM.md">
 RREF_SDM 是 SDM 配置子系统的参考电阻管脚。

  在 A5ED052A/A5ED065B B32A 上：

  | 项目 | 值 |
  |---|---|
  | FPGA ball | CL103 |
  | Pin name | RREF_SDM |
  | 连接 | 通过 2.00 kΩ / 1% 电阻接 GND |
  | 是否可当 GPIO | 不可以 |
  | 是否接电源 | 不接电源，只接电阻到 GND |
  | 是否可悬空 | 不建议/不要悬空 |

  它的作用不是传输数字信号，而是给 SDM/config 相关模拟/校准电路提供参考。你可以理解成“配置管理模块的基准电阻”。

  原理图画法：

  CL103 / RREF_SDM -> 2.00k 1% -> GND

  布局要求：

  - 电阻靠近 FPGA
  - 走线短
  - 不要和高速线并行
  - 不要串测试点、跳线、连接器
  - 不要接到模拟复用网络

  官方 065B B32A 开发板原理图也是这么接的：R116 = 2K, 0201 接在 RREF_SDM 到 GND。
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/SDM系统时钟选择.md">
这里不要用 20 MHz。建议用 125 MHz, 1.8 V LVCMOS, free-running oscillator 接 BR102 / OSC_CLK_1。

  原因很直接：Agilex 5 官方支持的外部 OSC_CLK_1 输入频率是 25 MHz / 100 MHz / 125 MHz。20 MHz 不在支持列表里；如果在 Quartus 里启用 OSC_CLK_1 但实际输入 20 MHz，配置可能失败。

  OSC_CLK_1 用途

  OSC_CLK_1 不是普通用户逻辑时钟。它主要给 SDM/配置网络使用：

  - 外部 QSPI flash 启动时，SDM 可用它生成配置内部时钟。
  - 用 OSC_CLK_1 后，AS/QSPI 的 AS_CLK 可以跑更高频率。
  - 如果设计里用到 transceiver、EMIF、MIPI、PHY Lite，官方要求提供外部 OSC_CLK_1，并在 Quartus 里启用。
  - 对 HPS/HPS EMIF，它不是唯一时钟，HPS 还有自己的参考时钟要求。

  你这个应用前面已经涉及 LPDDR5 EMIF + MIPI + 外部 QSPI 启动，所以我建议 必须放外部 OSC_CLK_1，不要依赖内部 oscillator。

  推荐选择

  | 选项 | 是否推荐 | 说明 |
  |---|---|---|
  | 125 MHz | 推荐 | 官方 065B B32A 开发板也是 CLK_SDM_REFCLK_125M 接 BR102 / OSC_CLK_1，最贴近参考设计 |
  | 100 MHz | 可用 | 如果板上已有稳定 100 MHz 1.8V 时钟，也可以 |
  | 25 MHz | 可用但不优先 | 配置速度较低，除非系统已有 25 MHz 且想降低复杂度 |
  | 20 MHz | 不建议/不要用 | 不在官方支持频率列表 |

  器件选择规范

  建议选这种规格的有源晶振/oscillator：

  - 输出：LVCMOS
  - 电压：1.8 V
  - 频率：125 MHz
  - 精度：±50 ppm 或更好，普通配置时钟不需要超低 ppm
  - 输出使能：如果有 OE/STBY，默认应上电自动使能，不要依赖 FPGA 配置后控制
  - 上电启动：必须在 SDM 开始从 QSPI flash 读配置前稳定
  - 供电：建议来自稳定的 1.8 V 时钟电源域，电平必须兼容 VCCIO_SDM
  - 摆幅：标准 1.8V CMOS，不要用 LVDS/HCSL/差分输出直接接
  - 抖动：不是高速 SERDES reference clock，不需要超低抖动等级；但仍应选正规 XO，不要用 MCU GPIO 或可停振 PLL 输出

  原理图连接建议

  | 项目 | 建议 |
  |---|---|
  | XO 输出 | 直接或串 22R~33R 到 BR102 / OSC_CLK_1 |
  | XO 电源 | 1.8V，靠近 XO 放 0.1uF + 1uF 去耦 |
  | OE/STBY | 上拉到 1.8V，保证 free-running |
  | FPGA 端 | BR102 只作为 OSC_CLK_1，不要复用 |
  | Quartus | Device and Pin Options 里选择 125 MHz OSC_CLK_1 pin |
  | AS_CLK | 再在 Quartus 里设置 QSPI AS_CLK 频率，别超过 flash 和 speed grade 支持值 |

  一个容易混淆的点

  OSC_CLK_1 = 125 MHz 不代表 QSPI flash 的 AS_CLK 就一定是 125 MHz。
  AS_CLK 是 SDM 根据配置设置生成的，可以设置为 25/50/71.5/100/125/166 MHz 等支持值；实际要看 flash 能力和 FPGA speed grade。首版板子我建议先按稳妥值，比如 AS_CLK = 50 MHz 或
  100 MHz，bring-up 后再优化。

  来源：Altera Agilex 5 Device Configuration User Guide、Pin Connection Guidelines、E-Tile PHY User Guide，以及官方 065B B32A SOM 原理图。
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/SmartVID PMBus.md">
结论先说：你这里大概率需要做 SmartVID / PMBus，而且建议按 PMBus Master Mode 画。

  因为你讨论的料号是 A5ED052AB32AE2V，其中 2V 属于 Agilex 5 的 -V power option。官方文档明确：Agilex 5 -V / -E SmartVID 器件的 VCC、VCCP 不能用普通固定电压 regulator 直接供，
  要用 PMBus-compliant regulator 配合 SmartVID。否则器件可能无法正确配置或工作。

  SmartVID 是什么
  SmartVID = Smart Voltage Identification。每颗 FPGA 出厂时内部 fuse 里有一组该芯片自己的最佳核心电压信息。上电配置早期，SDM Power Manager 读取这个 VID 值，然后通过 PMBus 告诉
  外部电源芯片应该把 VCC/VCCP 调到多少。

  作用：

  - 补偿芯片工艺差异
  - 降低功耗
  - 保证该 speed grade 的性能
  - 运行中还可结合温度做电压调整

  你可以理解成：FPGA 不再吃一个固定 0.8V，而是由 FPGA 自己告诉电源芯片“我这颗芯片当前需要多少核心电压”。

  PMBus 是什么
  PMBus 是电源管理总线，物理上类似 I2C/SMBus，常见信号是：

  | 信号 | 含义 |
  |---|---|
  | PWRMGT_SCL | PMBus clock |
  | PWRMGT_SDA | PMBus data |
  | PWRMGT_ALERT | PMBus alert，主要用于 Slave mode |

  这些信号在 Agilex 5 上属于 SDM 管脚，不是普通 GPIO。

  你这里推荐怎么接
  推荐：PMBus Master Mode。也就是 FPGA/SDM 做 PMBus master，直接控制 VCC/VCCP 的 PMBus regulator。

  按 065B 官方参考原理图和官方推荐 pin，建议这样接：

  | FPGA ball | SDM pin | 功能 | 建议 net | 连接 |
  |---:|---|---|---|---|
  | CF109 | SDM_IO14 | PWRMGT_SCL | A5E_PWRMGT_SCL | 接 PMBus regulator SCL |
  | CF99 | SDM_IO11 | PWRMGT_SDA | A5E_PWRMGT_SDA | 接 PMBus regulator SDA |
  | BR99 | SDM_IO12 | PWRMGT_ALERT 可选 | A5E_PWRMGT_ALERT 或保留 | Master mode 通常不需要；Slave mode 才需要 |
  | BP102 | SDM_IO16 | CONF_DONE | A5E_CONF_DONE | 保留配置完成状态 |
  | CA99 | SDM_IO0 | INIT_DONE | A5E_INIT_DONE | 保留进入 user mode 状态 |

  电气要求：

  - PWRMGT_SCL/SDA 上拉到 1.8V / VCCIO_SDM
  - 上拉电阻：5.1k ~ 10k
  - 如果 regulator 的 PMBus 是 3.3V，必须加双向 level shifter
  - level shifter 默认应在上电/掉电期间关闭，避免 bus contention
  - PMBus 线不要和普通系统 I2C 随便混接，除非你确认多主仲裁和地址规划没问题

  VCC/VCCP 电源怎么做
  你需要选一个支持 PMBus 的核心电源 regulator/controller，给 VCC 和 VCCP 供电。

  关键要求：

  | 项目 | 要求 |
  |---|---|
  | 输出范围 | 至少覆盖约 0.6V ~ 1.0V |
  | 调压步进 | 5mV ~ 10mV 级别 |
  | 上电初始电压 | SmartVID 设备初始按 0.80V 供电 |
  | 控制协议 | PMBus |
  | 输出对象 | VCC 和 VCCP |
  | 电流能力 | 按 Quartus Power Analyzer / EPE 估算 |
  | 远端采样 | 建议支持 remote sense |

  还要接 sense：

  | FPGA ball | Pin | 连接 |
  |---:|---|---|
  | AV72 | VCCLSENSE | 接 VCC regulator remote sense+ |
  | AU72 | GNDSENSE | 接 VCC regulator remote sense- / remote GND sense |

  Quartus 里怎么配置
  在 Quartus Prime Pro：

  1. Assignments > Device > Device and Pin Options
  2. 进 Configuration
  3. VID Operation Mode 选 PMBus Master
  4. Configuration Pin Options：
      - PWRMGT_SCL = SDM_IO14
      - PWRMGT_SDA = SDM_IO11
      - PWRMGT_ALERT 不启用，除非你用 Slave mode
  5. Power Management and VID：
      - 选择 regulator type，例如官方下拉里有 TPS53676、LTC3882-1、ISL68223 等
      - 设置 PMBus address
      - bus speed 初版建议 100 kHz
      - voltage output format 按 regulator datasheet 选 Linear 或 Direct
      - bring-up 阶段建议打开 Diagnostic Boot

  QSF 示例方向类似：

  set_global_assignment -name USE_PWRMGT_SDA SDM_IO11
  set_global_assignment -name USE_PWRMGT_SCL SDM_IO14
  set_global_assignment -name VID_OPERATION_MODE "PMBUS MASTER"
  set_global_assignment -name PWRMGT_BUS_SPEED_MODE "100 KHZ"

  具体 regulator address、format、PAGE 参数要等你选定电源芯片后再填。

  什么时候用 PMBus Slave Mode
  只有在你板上已经有一个外部 PMIC/MCU/CPLD 做总电源管理，而且它能完整处理 Agilex 的 VID 流程时，才考虑 Slave mode。

  Slave mode 需要：

  - PWRMGT_SCL
  - PWRMGT_SDA
  - PWRMGT_ALERT
  - 外部 master 支持 clock stretching
  - 外部 master 处理 ARA/Alert Response
  - 在规定时间内给 SDM 返回/下发目标电压

  这比 Master mode 复杂很多。你现在做最小系统和首版硬件，我不建议优先用 Slave mode。

  你的设计建议
  按目前信息，我建议你这样定：

  - 必须预留 SmartVID/PMBus
  - 采用 PMBus Master Mode
  - CF109 = PWRMGT_SCL
  - CF99 = PWRMGT_SDA
  - BR99 先保留为 PWRMGT_ALERT/CAT_TRIP_N 兼容位，不作为必需项
  - BP102 保留 CONF_DONE
  - CA99 保留 INIT_DONE
  - 选择官方工具支持或 FAE 推荐的 PMBus regulator
  - 不要用固定 0.8V regulator 直接硬供 VCC/VCCP 当生产方案

  依据来源：Altera Agilex 5 Power Management User Guide、SmartVID Standard Power Devices、PMBus Master/Slave Mode、Configuration Pin Parameters、Pin Connection Guidelines。

Agilex 5 -V / -E SmartVID 器件的 VCC、VCCP 不能用普通固定电压 regulator 直接供，
  要用 PMBus-compliant regulator 配合 SmartVID。否则器件可能无法正确配置或工作
  这段要求具体出处？给我一个具体方案？








出处是明确的，来自 Altera 官方文档。

  最关键的是这句，位置在 Power Management User Guide: Agilex 5 FPGAs and SoCs → SmartVID Standard Power Devices：

  > Agilex 5 –1V / –2V / –2E / –3V power grades are SmartVID devices；VCC 和 VCCP 必须由连接到该 Agilex 5 器件的 dedicated PMBus-compliant regulator 供电；如果用 non-PMBus
  > fixed-output regulator，器件不能正确 configure/function。

  官方页面：
  https://docs.altera.com/r/docs/813161/current/power-management-user-guide-agilextm-5-fpgas-and-socs/smartvid-standard-power-devices

  同一页还说明：

  - PWRMGT_SCL、PWRMGT_SDA 在 PMBus Master/Slave 模式都必需。
  - PWRMGT_ALERT 只在 PMBus Slave 模式必需。
  - SmartVID 器件先以 0.80V 给 VCC/VCCP 上电，然后 SDM 读取 fuse VID，再通过 PMBus 调 regulator。

  另一个出处是 Altera SmartVID 页面，列了 Agilex 5 推荐 regulator：

  https://www.altera.com/design/resource/power/smartvid

  Agilex 5 fully validated regulator 包括：

  - TPS53676
  - LTC3882-1
  - ISL68223

  LTC7883 是 API validated only；官方 065B B32A 开发板用了 LTC7883，但从产品风险角度，我更建议你优先选 fully validated 列表里的器件。

  给你的具体方案

  我建议用：PMBus Master Mode + TPS53676 + 外部 power stage。

  原因：TPS53676 在 Altera Agilex 5 fully validated regulator 列表里，Quartus 也支持；比用普通固定 0.8V regulator 风险低。

  原理图结构：

  A5ED052A B32A
    VCC  --------+
                 +---- +V0P8_VCCP_VID ---- TPS53676 + power stage
    VCCP --------+

    CF109 / SDM_IO14 / PWRMGT_SCL ---- level shift if needed ---- TPS53676 PMBus SCL
    CF99  / SDM_IO11 / PWRMGT_SDA ---- level shift if needed ---- TPS53676 PMBus SDA

    AV72 / VCCLSENSE  ---- remote sense +
    AU72 / GNDSENSE   ---- remote sense -

    BP102 / SDM_IO16  ---- CONF_DONE
    CA99  / SDM_IO0   ---- INIT_DONE
    BR99  / SDM_IO12  ---- DNP/TP or PMBus ALERT reserve

  关键连接要求

  | 项目 | 建议 |
  |---|---|
  | VCC + VCCP | 合并为同一个 SmartVID core rail：+V0P8_VCCP_VID |
  | 初始电压 | regulator NVM 默认输出 0.80V |
  | VID 调压范围 | 覆盖约 0.70V ~ 0.90V |
  | PMBus 模式 | PMBus Master |
  | PWRMGT_SCL | CF109 / SDM_IO14 |
  | PWRMGT_SDA | CF99 / SDM_IO11 |
  | PMBus 上拉 | 5.1k ~ 10k 到 1.8V VCCIO_SDM |
  | PMBus 电平 | Agilex 侧是 1.8V single-ended |
  | Regulator PMBus 若是 3.3V | 加双向 level translator，默认 disabled，等电源稳定后再 enable |
  | PWRMGT_ALERT | Master mode 不需要，BR99 先预留 |
  | Remote sense | VCCLSENSE/GNDSENSE 接到 FPGA 负载点附近 |

  Quartus 设置方向

  set_global_assignment -name VID_OPERATION_MODE "PMBUS MASTER"

  set_global_assignment -name USE_PWRMGT_SCL SDM_IO14
  set_global_assignment -name USE_PWRMGT_SDA SDM_IO11
  set_global_assignment -name USE_CONF_DONE SDM_IO16

  set_global_assignment -name PWRMGT_BUS_SPEED_MODE "100 KHZ"
  set_global_assignment -name PWRMGT_SLAVE_DEVICE_TYPE TPS53676
  set_global_assignment -name PWRMGT_SLAVE_DEVICE0_ADDRESS <TPS53676_7bit_address>

  set_global_assignment -name PWRMGT_VOLTAGE_OUTPUT_FORMAT "LINEAR FORMAT"
  set_global_assignment -name PWRMGT_LINEAR_FORMAT_N "-10"
  set_global_assignment -name PWRMGT_TRANSLATED_VOLTAGE_VALUE_UNIT VOLTS

  <TPS53676_7bit_address> 要按你原理图里 TPS53676 地址脚配置填写。首版 bring-up 建议 PMBus 先用 100 kHz，并在 Quartus 里打开 Diagnostic Boot。

  我不建议的方案

  不要这样做：

  普通 0.8V Buck ---- VCC/VCCP
  PMBus 不接

  对 A5ED052AB32AE2V 这种 -2V SmartVID 器件，这是官方明确不支持的方向，风险是 FPGA 不配置或配置后工作不可靠。

  如果你想贴近官方 065B 开发板原理图，也可以用 LTC7883，Quartus 里按 Other + Linear N=-12 配；但它在 Altera SmartVID 页面上是 Agilex 5 的 API validated only，不是 fully
  validated。首版产品我会选 TPS53676 或 LTC3882-1。



| 项目(A5ED052AB32AE2V)        | 结论                                    |
| -------------------------- | ------------------------------------- |
| 是否属于 -1V/-2V/-2E/-3V 这一类   | **是**                                 |
| 具体属于哪一档                    | **-2V**                               |
| 是否 SmartVID                | **是**                                 |
| VCC / VCCP 能否用固定 0.8V DCDC | **不建议 / 按文档不可以**                      |
| 是否需要 PMBus 电源              | **需要，至少 VCC / VCCP 要按 SmartVID 方案处理** |
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/a5ed052a_b32a_vcc_reference_schematic_summary_zh.md">
# A5ED052A B32A 可参考原理图 VCC / SmartVID 方案汇总

日期：2026-05-11

目标器件：`A5ED052AB32AE2V`

本文只汇总目前本地可参考原理图里的 `VCC/VCCP/SmartVID` 相关方案，不替代最终电源完整设计。

## 1. 参考资料

| 优先级 | 文件 | 用途 |
|---:|---|---|
| 1 | `sources/reference_schematic/agilex-5e-mdevkit-som-sch-v2p1.pdf` | Altera 官方 Agilex 5 E-Series 065B B32A SOM 原理图，最高优先级实物参考 |
| 2 | `sources/vendor_reference/keim-a5esom_sch_rev1.10.pdf` | KEIm A5E SOM Rev1.10 原理图，供应商实际 SOM 参考 |
| 3 | `sources/vendor_reference/keim-a5esom_bom_rev1.10-.xlsx` | KEIm Rev1.10 BOM，用于确认器件料号 |
| 4 | `sources/vendor_reference/sulfur_type-a_sch_rev1.00.pdf` | Sulfur Type-A carrier 原理图，只能参考 SOM 供电入口和 PMBus 暴露方式 |
| 5 | `sources/official_pinouts/a5ed052a/a5ed052A.xlsx` | A5ED052A B32A 官方 pinout，用于确认本项目 ball/pin |

## 2. 总体结论

目前可参考原理图都支持同一个核心判断：

- `VCC/VCCP` 不是普通固定 0.8V buck 方案。
- 应设计成 SmartVID / PMBus 可调核心电源 rail。
- `VCCLSENSE` 和 `GNDSENSE` 要接入 regulator sense 网络，不能悬空。
- PMBus 要能被 Agilex SDM 或外部板级控制器访问。

对本项目建议的 rail 命名：

```text
A5E_VCC_VID
```

并把 A5ED052A B32A 的所有 `VCC` 和 `VCCP` balls 接到该 rail。

## 3. KEIm A5E SOM Rev1.10 方案

原理图位置：

- `keim-a5esom_sch_rev1.10.pdf`
- Sheet 13: `Power VID`
- Sheet 14: `Power 0.8V, 1.0V`
- Sheet 15: `Power 3.3V, 1.8V, 1.2V, 1.1V`

器件与封装：

- Hardware manual 标注 device：`A5ED065BB32AE5SR0`
- BOM 标注 FPGA package：`A5ED065BB32A` / `BGA1591`
- 因此 KEIm Rev1.10 是 `A5ED065B`、`B32A`、1591-ball BGA，不是 `A5ED052A`，但封装代码同为 `B32A`。

核心方案：

| 项目 | KEIm Rev1.10 做法 |
|---|---|
| SmartVID rail 名称 | `VCC_VID` |
| VID 控制器 | `LTC7883AY#PBF` |
| VCC_VID 功率级 | `NCP302035MNTWG` |
| VCC_VID 电流标注 | `27A/41A` |
| VCC/VCCP | 接到 `VCC_VID` |
| 远端采样 | `VCCLSENSE_AV72`、`GNDSENSE_AU72` 通过 0R 接入 `VID_VSNSA_P/N` |
| PMBus | 同时有 `SDM_PWRMGT_*_3V3` 和 `SOM_PMBUS_*_3V3` 路径，部分 0R 为可选/NoMount |
| 固定辅助低压 | 同一颗 `LTC7883` 的另一组通道还生成 `1.0V` 和 `0.8V` |

KEIm 的关键特征：

- 这是一个 SOM 设计，不是最小独立板设计。
- 它把 PMBus 暴露到 SOM 连接器，便于 carrier / 外部控制器管理。
- 它不是简单的“SDM 直接连 regulator PMBus”的最小方案。
- `LTC7883` 在这个设计中既做 `VCC_VID`，也参与固定 `1.0V/0.8V` rail。

因此，KEIm 方案对 `B32A` 封装下的 VCC/SmartVID 原理图拓扑参考价值很高；只是因为它的实际器件是 `A5ED065B` 而不是本项目的 `A5ED052A`，且它是 SOM 架构，所以不能直接照抄电流容量、PMBus 主控分工和所有辅助 rail 共轨方式。

## 4. Altera 官方 065B SOM 方案

原理图位置：

- `agilex-5e-mdevkit-som-sch-v2p1.pdf`
- Sheet 52/53: `POWER-LTC7883-CONTROLLER`
- Sheet 54: `POWER-VCCP_VID`
- Sheet 55: `POWER - +V1P0, +V0P8`

核心方案：

| 项目 | Altera 官方 SOM 做法 |
|---|---|
| SmartVID rail 名称 | `+V0P8_VCCP_VID` |
| VID 控制器 | `LTC7883` |
| VCCP_VID 功率级 | `LTC7050AV#PBF` |
| VCC/VCCP | 接到 `+V0P8_VCCP_VID` |
| 远端采样 | `VCCLSENSE/GNDSENSE` 接到 `VCCL_SENSE_R_P/N` sense 网络 |
| SDM PMBus SCL | `CF109 / SDM_IO14 / PWRMGT_SCL` -> `PMBUS_SCL_C2M_1V8` |
| SDM PMBus SDA | `CF99 / SDM_IO11 / PWRMGT_SDA` -> `PMBUS_SDA_C2M_1V8` |
| PMBus 电平 | 1.8V 侧经电平转换到 3.3V PMBus |
| PMBus 总线 | 同时连接多个 PMBus regulator / power IC |

官方方案的价值：

- 它是 Altera 官方开发套件 SOM 原理图，参考优先级最高。
- 它证明 `LTC7883` 在 Agilex 5 官方参考板上确实被采用。
- 但这不等于 `LTC7883` 是 Altera SmartVID 页面里的 fully validated 器件；官方页面仍把它归为 `API validated only`。

## 5. Sulfur Type-A Carrier 方案

原理图位置：

- `sulfur_type-a_sch_rev1.00.pdf`

它不是 FPGA VCC/SmartVID regulator 的核心参考。它主要提供：

- SOM 输入电源。
- carrier 到 SOM 的 PMBus 访问路径：
  - `SOM_PMBUS_SCL_3V3`
  - `SOM_PMBUS_SDA_3V3`
- 外设和 carrier 侧电源。

使用方式：

- 可以参考它如何把 PMBus 暴露到 carrier。
- 不应从它推导 A5ED052A 的 `VCC/VCCP` regulator 拓扑。

## 6. 方案对比

| 参考设计 | VCC/SmartVID rail | 控制器 | 功率级 | PMBus 主控倾向 | 对本项目价值 |
|---|---|---|---|---|---|
| Altera 065B SOM | `+V0P8_VCCP_VID` | `LTC7883` | `LTC7050AV#PBF` | FPGA SDM / C2M PMBus 体系 | 最高优先级参考 |
| KEIm A5E SOM Rev1.10 | `VCC_VID` | `LTC7883AY#PBF` | `NCP302035MNTWG` | SOM / carrier 可访问，SDM 路径可选 | 有实际 SOM 设计价值，但需确认 PMBus 架构 |
| Sulfur Type-A carrier | 不生成 FPGA `VCC_VID` | 不适用 | 不适用 | 暴露 `SOM_PMBUS_*` | 只参考 carrier 访问和输入电源 |

## 7. 对 A5ED052AB32AE2V 的建议

推荐把本项目先按以下方式画：

```text
PMBus-capable SmartVID regulator
  -> +A5E_VCC_VID
  -> A5ED052A VCC balls
  -> A5ED052A VCCP balls

CF109 / SDM_IO14 / PWRMGT_SCL -> regulator PMBus SCL
CF99  / SDM_IO11 / PWRMGT_SDA -> regulator PMBus SDA

AV72 / VCCLSENSE -> regulator remote sense+
AU72 / GNDSENSE  -> regulator remote sense-
```

器件选择有两条路线：

1. 低供应/支持风险路线：优先让 FAE 推荐 `TPS53676`、`LTC3882-1` 或 `ISL68223` 这类 Altera fully validated SmartVID regulator。
2. 参考设计复制路线：采用 `LTC7883`，但需要 FAE 明确确认本项目 Quartus 版本、PMBus 配置、PAGE/address、初始电压、NVM 配置和 power-up 时序。

当前我更建议：

- 原理图结构参考 Altera 官方 065B SOM。
- KEIm Rev1.10 作为第二交叉验证，尤其验证 `VCC/VCCP -> VCC_VID`、remote sense 和 `LTC7883` 实际使用方式。
- 最终 regulator 料号让 Altera/代理商 FAE 确认后冻结。

## 8. 需要继续确认的点

- `A5ED052AB32AE2V` 在当前采购渠道下是否明确按 SmartVID `-V/-E` 规则处理。
- 目标 Quartus 版本对所选 regulator 的支持状态。
- PMBus master 是 FPGA SDM 还是外部 MCU / carrier 控制器。
- `VCC/VCCP` 以外的其它 0.8V 类 rail 是否允许与 `A5E_VCC_VID` 共轨。
- `A5E_VCC_VID` 电流能力应由 Quartus Power Analyzer / EPE 重新计算，不能直接照抄 KEIm 的 `27A/41A` 或官方 SOM 的功率级容量。
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/a5ed052a_b32a_vcc_smartvid_power_design_report_zh.md">
# A5ED052A B32A VCC / SmartVID 供电设计报告

日期：2026-05-11

目标器件：`A5ED052AB32AE2V`

封装：`B32A`

状态：原理图设计建议版。最终 release 前仍需 FAE、Quartus、PDN 分析闭环确认。

## 1. 核心结论

`A5ED052AB32AE2V` 的 `VCC/VCCP` 不应按普通固定 `0.8 V` Buck 设计，而应按 **SmartVID 可调核心电源**设计。

推荐板级架构：

- 建立一个 SmartVID 核心电源轨，命名为 `A5E_VCC_VID`。
- FPGA 的 `VCC` 和 `VCCP` 全部接到 `A5E_VCC_VID`。
- regulator 初始/NVM 输出设为 `0.80 V`。
- 默认采用 `PMBus Master Mode`，除非项目明确有外部系统电源控制器负责 VID。
- Agilex SDM PMBus 管脚连接：
  - `CF109 / SDM_IO14 / PWRMGT_SCL` 接 regulator PMBus `SCL`。
  - `CF99 / SDM_IO11 / PWRMGT_SDA` 接 regulator PMBus `SDA`。
- 远端采样连接：
  - `AV72 / VCCLSENSE` 接 regulator sense positive，采样点靠近 FPGA 负载端。
  - `AU72 / GNDSENSE` 接 regulator sense negative / ground sense，采样点靠近 FPGA 负载端。
- 保留 `BP102 / SDM_IO16` 作为 `CONF_DONE`。
- 保留 `CA99 / SDM_IO0` 作为 `INIT_DONE`。
- `BR99 / SDM_IO12` 先作为可选 `PWRMGT_ALERT` / 状态信号 / DNP 兼容位，等 PMBus 模式冻结后再定。

推荐 regulator 路线：

1. 产品首版优先：选 Intel/Altera 对 Agilex 5 fully validated 的 SmartVID regulator，例如 `TPS53676`、`LTC3882-1` 或 `ISL68223`。
2. 参考设计复制路线：参考 KEIm 的 `LTC7883AY#PBF + NCP302035MNTWG` 拓扑，但仅在 FAE 对本项目和 Quartus 版本确认后采用。原因是 Altera 对 Agilex 5 把 `LTC7883` 标为 API validated only，不是 fully validated。

## 2. 资料优先级

本报告按以下优先级使用资料：

1. Intel/Altera 官方 Power Management 文档。
2. Intel/Altera 官方 A5ED052A B32A pinout。
3. Intel/Altera 官方 065B B32A SOM 参考原理图。
4. KEIm A5E SOM 供应商参考原理图和 BOM。
5. 本地派生 workbook 和 notes。

已核查的本地资料：

- `sources/official_pinouts/a5ed052a/a5ed052A.xlsx`
- `sources/reference_schematic/agilex-5e-mdevkit-som-sch-v2p1.pdf`
- `sources/vendor_reference/keim-a5esom_sch_rev1.10.pdf`
- `sources/vendor_reference/keim-a5esom_bom_rev1.10-.xlsx`
- `sources/vendor_reference/keim-a5esom_hardware_manual_EN_v1.1.pdf`

官方在线资料：

- Altera Power Management User Guide: Agilex 5 FPGAs and SoCs，SmartVID / PMBus 章节。
- Altera FPGA SmartVID regulator 页面。
- Altera Pin Connection Guidelines: Agilex 5 FPGAs and SoCs。
- Altera A5ED052A pin information document 830449。

## 3. 官方要求解读

Agilex 5 官方 Power Management 文档说明：Agilex 5 的 `-V` / `-E` SmartVID 器件，`VCC` 和 `VCCP` 需要由 PMBus-compliant voltage regulator 供电。SDM Power Manager 会读取器件内部的 VID fuse，然后在 FPGA 配置前通过 PMBus 调整 regulator 输出。

对本项目的解释：

- `A5ED052AB32AE2V` 包含 `-2V` speed/power suffix。
- 除非 FAE 明确证明不是 SmartVID 器件，否则应按 SmartVID 器件处理。
- 不应把 `VCC/VCCP` 设计成没有 PMBus 控制路径的固定 `0.8 V` 输出。
- SmartVID 不只是硬件问题，也必须在 Quartus 中配置。

Altera SmartVID 页面列出的 Agilex 5 推荐 PMBus regulator：

- Agilex 5 fully validated：
  - `TPS53676`
  - `LTC3882-1`
  - `ISL68223`
- API validated only：
  - `LTC7883`

因此，对新产品而言，`TPS53676 / LTC3882-1 / ISL68223` 风险更低；`LTC7883` 有参考价值，但更适合作为已有参考设计的佐证，而不是默认首选。

## 4. A5ED052A B32A 相关 pin

来自 A5ED052A B32A 官方 pinout：

| Rail / Pin | Ball 数量 | B32A ball |
|---|---:|---|
| `VCC` | 41 | `BA61, AY75, AY68, AY64, AY57, AY53, AW79, AW72, AW68, AW61, AW57, AV86, AV83, AV75, AV64, AV61, AV53, AU79, AU75, AU68, AU64, AU57, AU53, AT79, AT72, AT68, AT61, AT57, AR83, AR75, AR72, AR64, AR61, AR53, AP86, AP79, AP75, AP68, AP64, AN79, AN72` |
| `VCCP` | 14 | `BB72, BB68, BB61, BB57, BB50, BA64, BA53, AN68, AN57, AM75, AM72, AM64, AM61, AM53` |
| `VCCLSENSE` | 1 | `AV72` |
| `GNDSENSE` | 1 | `AU72` |
| `PWRMGT_SCL` | 1 | `CF109 / SDM_IO14` |
| `PWRMGT_SDA` | 1 | `CF99 / SDM_IO11` |
| 可选 `PWRMGT_ALERT` | 1 | `BR99 / SDM_IO12`，或其它 Quartus 支持的 SDM 选项 |

注意：不要看到某个 rail 是 `0.8 V` 就自动接到 `A5E_VCC_VID`。官方强制 SmartVID 的核心对象是 `VCC/VCCP`；其它低压 rail 必须根据当前 Pin Connection Guidelines 和 FAE 反馈单独确认。

## 5. 参考设计分析

### 5.1 Intel/Altera 065B B32A SOM 官方参考

官方 065B B32A SOM 参考设计使用的 SDM/JTAG/config ballout 与本项目相关 pin 一致。它确认了：

- `CF109` 可作为 PMBus `SCL`。
- `CF99` 可作为 PMBus `SDA`。
- `BP102` 可作为 `CONF_DONE`。
- `CA99` 可作为 `INIT_DONE`。
- 供电设计中存在 SmartVID 风格核心 rail。

这是最强的真实板级参考，因为它来自 Altera 官方开发板原理图。

### 5.2 KEIm A5E SOM 参考

供应商资料中包含 `keim-a5esom_sch_rev1.10.pdf` 和 BOM。与 VCC/SmartVID 相关的发现：

- 电源页明确命名为 `Power VID`。
- 主 VID controller 是 `LTC7883AY#PBF`。
- 功率级是 `NCP302035MNTWG`。
- 输出 rail 命名为 `VCC_VID`。
- 原理图标注 `VCC_VID` 电流能力为 `27A/41A`。
- 电压注释显示 `-1, -2, -3` power grade 使用 `VID`，更低 speed grade 使用固定电压。
- `VCC` 和 `VCCP` 接到 `VCC_VID`。
- `VCCLSENSE_AV72` 和 `GNDSENSE_AU72` 通过 0R 接到 VID sense 网络。
- PMBus 同时暴露了 SDM PMBus 路径和 SOM/carrier PMBus 路径。

重要限制：

KEIm 是模块设计，PMBus 架构包含 carrier / 系统管理访问，不是“独立最小系统板”的一比一模板。是否能直接复制，取决于启动时到底谁拥有 PMBus：Agilex SDM、外部系统控制器，还是带严格仲裁的多主系统。

## 6. 推荐原理图设计

### 6.1 核心电源命名

建议命名：

```text
A5E_VCC_VID
```

连接对象：

```text
FPGA VCC pins
FPGA VCCP pins
```

不建议简单命名为 `+0V8`。`A5E_VCC_VID` 能明确表达这是 VID 可调、PMBus 控制的核心电源。

### 6.2 Regulator 架构

推荐框图：

```text
5V or 12V input
  -> PMBus-capable multiphase regulator/controller
  -> power stage(s)
  -> +A5E_VCC_VID
  -> A5ED052A VCC/VCCP pins

A5ED052A SDM PMBus
  CF109 / PWRMGT_SCL
  CF99  / PWRMGT_SDA
  -> regulator PMBus interface
```

Regulator 选择：

- 优先 `TPS53676`、`LTC3882-1` 或 `ISL68223`，除非 FAE 推荐其它器件。
- 电流能力必须由 Quartus Power Analyzer / EPE 估算。
- 不要直接照抄 KEIm 的 `27A/41A` 电流能力。KEIm 板使用的是 `A5ED065B`，你的 `A5ED052A` 资源使用、频率、温度条件都可能不同。

### 6.3 PMBus 电气连接

如果 regulator PMBus 支持 `1.8 V`：

```text
CF109 / PWRMGT_SCL ---- regulator SCL
CF99  / PWRMGT_SDA ---- regulator SDA
两根线都上拉到 VCCIO_SDM / 1.8 V
```

如果 regulator PMBus 只能工作在 `3.3 V`：

```text
CF109 / CF99 at 1.8 V
  -> bidirectional level shifter
  -> regulator PMBus at 3.3 V
```

要求：

- 使用兼容 open-drain 的 PMBus/I2C 双向电平转换。
- Agilex 侧上拉建议 `5.1 kΩ` 到 `10 kΩ` 到 `VCCIO_SDM`。
- Regulator 侧上拉按 regulator datasheet，常见为 `3.3 V`。
- 避免 `VCCIO_SDM` 未上电时通过 PMBus 反灌电。
- 如果 level shifter 带 OE，必须定义 OE 默认状态。

### 6.4 PMBus 模式

推荐模式：

```text
PMBus Master Mode
```

原因：

- 最小系统更简单。
- Agilex SDM 可以直接设置核心 VID regulator。
- 不依赖外部 MCU/PMIC firmware 在 FPGA 配置早期就已经运行。

不要轻易选 PMBus Slave/Target Mode，除非：

- 外部控制器一定早于 Agilex 配置阶段启动。
- 外部控制器完整实现 VID/PMBus 流程。
- `PWRMGT_ALERT` 已连接，并且 Quartus 配置与之匹配。

### 6.5 Sense 连接

连接：

```text
AV72 / VCCLSENSE -> regulator remote sense positive
AU72 / GNDSENSE  -> regulator remote sense negative / ground sense
```

建议实现：

- 按 Kelvin sense 方式走到 FPGA 负载点。
- 增加 0R 选择：
  - 靠近 FPGA 的 load sense：默认贴。
  - 靠近 regulator 的 local sense：DNP 备选。
- 只有 regulator datasheet 或参考设计要求时，才增加 sense 滤波。
- Sense 走线远离开关节点、功率电感、SW copper。

### 6.6 相关状态 pin

最小系统页建议保留：

| FPGA ball | Pin / function | 推荐 net | 用途 |
|---|---|---|---|
| `BP102` | `SDM_IO16 / CONF_DONE` | `A5E_CONF_DONE` | 配置完成监测 |
| `CA99` | `SDM_IO0 / INIT_DONE` | `A5E_INIT_DONE` | 进入 user mode / 初始化完成监测 |
| `BR99` | `SDM_IO12 / PWRMGT_ALERT option` | `A5E_PWRMGT_ALERT_DNP` 或 `A5E_CAT_TRIP_N` | 等 PMBus 模式和状态策略冻结后再定 |

## 7. Quartus 配置方向

预期方向：

```tcl
set_global_assignment -name VID_OPERATION_MODE "PMBUS MASTER"
set_global_assignment -name USE_PWRMGT_SCL SDM_IO14
set_global_assignment -name USE_PWRMGT_SDA SDM_IO11
set_global_assignment -name PWRMGT_BUS_SPEED_MODE "100 KHZ"
```

Regulator 相关参数取决于最终选型：

```tcl
set_global_assignment -name PWRMGT_SLAVE_DEVICE_TYPE <selected_regulator>
set_global_assignment -name PWRMGT_SLAVE_DEVICE0_ADDRESS <7bit_address>
set_global_assignment -name PWRMGT_VOLTAGE_OUTPUT_FORMAT <linear_or_direct>
set_global_assignment -name PWRMGT_LINEAR_FORMAT_N <regulator_specific_N>
```

来自 Altera SmartVID 文档的 regulator format 方向：

| Regulator | Agilex 5 验证状态 | Voltage format 说明 |
|---|---|---|
| `TPS53676` | Fully validated | Linear，`N = -10` |
| `LTC3882-1` | Fully validated | Linear，`N = -12` |
| `ISL68223` | Fully validated | Direct format 系列 |
| `LTC7883` | API validated only | 需要 FAE 确认 Quartus 设置 |

Bring-up 建议：

- PMBus 初版用 `100 kHz`。
- 首板打开 Diagnostic Boot。
- 导出并归档 Quartus 生成的 pin/config report。

## 8. 上电时序和 Power-Good 要求

板级时序必须保证：

- `A5E_VCC_VID` 初始输出为 `0.80 V`。
- SDM 尝试 VID 通信时，regulator PMBus 接口已经可用。
- 依赖 SDM PMBus 通信前，`VCCIO_SDM` 已有效。
- PMBus 线不会被未上电 regulator、level shifter 或外部控制器拉低。
- Regulator PGOOD 纳入板级 power-good tree。
- `nSTATUS`、`CONF_DONE`、`INIT_DONE` 在 bring-up 时可观测。

建议暴露的 power-good / debug 信号：

- `A5E_VCC_VID_PGOOD`
- `A5E_1V8_SDM_PGOOD`
- `A5E_NSTATUS`
- `A5E_CONF_DONE`
- `A5E_INIT_DONE`
- PMBus 测试点或调试 header

## 9. Layout 要求

Regulator 区域：

- 功率级靠近 controller，电流环路短。
- 高频输入/输出电容靠近功率级。
- SW 节点面积受控，按 regulator 厂商 layout guide。
- PMBus 和 sense 线远离 SW 节点。

FPGA 负载区域：

- 按 PDN 结果放置 bulk 和高频去耦。
- 所有 `VCC` / `VCCP` ball 接低阻抗电源平面。
- `VCCLSENSE/GNDSENSE` 做安静 Kelvin sense。
- Sense return 不要和大电流地路径混在一起。
- `A5E_VCC_VID` 可以加测试点，但不要在 sense loop 上拉长 stub。

## 10. Do / Do Not

应该做：

- 使用 PMBus-compliant SmartVID regulator。
- 保证 SDM 到 regulator 的 PMBus 路径可用。
- 使用 `A5E_VCC_VID` 这种明确命名。
- 原理图中明确 regulator PMBus address。
- 给 sense fallback、PMBus debug 预留 DNP/0R。
- 归档 FAE 确认和 Quartus 报告。

不要做：

- 用普通 fixed-output 0.8 V Buck 直接供 `VCC/VCCP`。
- 把 `PWRMGT_SDA/SCL` 随意并到繁忙系统 I2C，而不做多主分析。
- 未确认系统管理架构时，直接复制 KEIm carrier-access PMBus 拓扑。
- 不跑 EPE / Quartus Power Analyzer 就照抄 `27A/41A`。
- 把所有 0.8V rail 都无脑接到 `A5E_VCC_VID`。

## 11. 推荐具体实现

如果这是独立最小系统板：

```text
Regulator:
  TPS53676 or LTC3882-1 or ISL68223

Rail:
  +A5E_VCC_VID
  default/NVM output = 0.80 V

Loads:
  A5ED052A VCC
  A5ED052A VCCP
  其它低压 rail 仅在当前 Pin Connection Guidelines 允许时接入

Control:
  PMBus Master Mode from SDM
  CF109 / SDM_IO14 / PWRMGT_SCL
  CF99  / SDM_IO11 / PWRMGT_SDA

Sense:
  AV72 / VCCLSENSE -> sense+
  AU72 / GNDSENSE  -> sense-

Debug:
  VCC_VID test point
  PMBus test pads
  regulator PGOOD
  nSTATUS / CONF_DONE / INIT_DONE
```

如果板上已经有系统控制器或 PMIC supervisor：

- 先决定 Agilex SDM 是否仍然是 PMBus master。
- 如果外部控制器控制 PMBus，则需要分析 PMBus Slave/Target Mode，并连接 `PWRMGT_ALERT`。
- 必须确认外部控制器 firmware 在 Agilex 配置前已可用。

## 12. FAE / 工具闭环项

原理图 release 前必须关闭：

1. 确认 `A5ED052AB32AE2V` 确实是 SmartVID `-2V` 器件，且 `VCC/VCCP` 必须 PMBus 供电。
2. 确认选定 regulator 被项目使用的 Quartus 版本支持。
3. 确认 regulator voltage format、PMBus address、PAGE 设置和初始 NVM voltage。
4. 确认 `VCCL_*`、`VCCPLLDIG_*`、HSSI、PLL 等其它低压 rail 的 rail-sharing 规则。
5. 用 Intel/Altera EPE 或 Quartus Power Analyzer 做电流预算。
6. 做 PDN 分析，确定去耦和电源平面阻抗。
7. 确认上电时序满足 Agilex 5 POR 要求。
8. 生成 Quartus `.pin` / configuration report 并和原理图交叉核对。

## 13. 评审 Checklist

原理图检查：

- [ ] `VCC` 和 `VCCP` 已连接到 `A5E_VCC_VID`。
- [ ] `A5E_VCC_VID` regulator 支持 PMBus。
- [ ] Regulator 默认输出为 `0.80 V`。
- [ ] `PWRMGT_SCL` 使用 `CF109 / SDM_IO14`。
- [ ] `PWRMGT_SDA` 使用 `CF99 / SDM_IO11`。
- [ ] PMBus 电压域正确，必要时已做 level shift。
- [ ] `VCCLSENSE / GNDSENSE` 连接正确。
- [ ] PMBus address strap 已在原理图标注。
- [ ] Regulator PGOOD 接入 power-good tree。
- [ ] `nSTATUS`、`CONF_DONE`、`INIT_DONE` 有测试点或 supervisor 监控。
- [ ] FAE 确认已归档到评审资料。

Layout 检查：

- [ ] Sense 走线是 Kelvin、低噪声路径。
- [ ] PMBus 线远离 SW 节点。
- [ ] 去耦符合 PDN 分析结果。
- [ ] 功率级热路径已评审。
- [ ] 测试点不会破坏 sense loop。

Bring-up 检查：

- [ ] 编程前测量 `A5E_VCC_VID` 初始电压。
- [ ] 确认 PMBus idle high，没有 stuck-low。
- [ ] 确认 regulator 在设定地址 ACK。
- [ ] 首次配置启用 Diagnostic Boot。
- [ ] 记录 `nSTATUS`、`CONF_DONE`、`INIT_DONE`。
- [ ] SDM VID 调压后读取 PMBus 输出电压。

## 14. 最终建议

本项目建议冻结的原理图方向：

```text
A5ED052AB32AE2V
VCC/VCCP = A5E_VCC_VID
SmartVID PMBus Master Mode
PWRMGT_SCL = CF109 / SDM_IO14
PWRMGT_SDA = CF99 / SDM_IO11
VCCLSENSE = AV72
GNDSENSE = AU72
Regulator = TPS53676 / LTC3882-1 / ISL68223 class, FAE-confirmed
```

KEIm `LTC7883 + NCP302035` 原理图可作为拓扑和容量设计参考，但不建议默认照抄为产品首版方案，除非 FAE 明确确认该方案适用于 `A5ED052AB32AE2V` 和项目使用的 Quartus 版本。

</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/a5ed065b_b32a_lpddr5_internal_supplier_drafts.md">
# A5ED065B B32A LPDDR5 沟通短稿

## 1. 内部项目群

各位，A5ED065B B32A 方案的 LPDDR5 寻样需求需要确认：

1. FPGA 最终型号是否确定为 `A5ED065B B32A`？
2. 是否接受单颗从 2GB 改为 4GB，即两颗后整板 LPDDR 容量从 4GB 变 8GB？
3. 是否确认只选普通 LPDDR5，不选 LPDDR5X？
4. `16bit die` 是否为硬性要求？请确认准确表达。
5. 短生命周期料号是否可接受？如果接受，必须要求供应商同时提供替代料号、兼容性说明和 PCN/EOL 切换计划。
6. 逻辑侧是否可以基于最终 FPGA 型号 + 候选 LPDDR5 料号跑 Quartus EMIF / Pin Planner / Fitter？

在逻辑验证和替代料确认前，硬件侧不冻结 LPDDR5 pin list。

## 2. 发给代理商/原厂

主题：LPDDR5 颗粒寻样需求更新

Hi <Name>，

请帮忙按以下条件重新推荐 LPDDR5 颗粒：

- 普通 LPDDR5，不选 LPDDR5X
- 单颗 4GB / 32Gb
- 优先 x32 package width
- 需要确认是否为 16bit die / die organization
- 商业级或工业级均可
- 主控：Intel / Altera Agilex 5，当前按 A5ED065B B32A 评估
- 每板暂按 2 颗规划

短生命周期料号可以接受评估，但必须同时提供替代料号，避免后续采购断料风险。

请按表格回复：

| 推荐料号 | LPDDR5/LPDDR5X | 容量 | package width | die organization | 封装 | 温度等级 | 生命周期/EOL 状态 | 替代料号 | 替代料兼容性 | 样品交期 | 量产交期 | MOQ/MPQ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

另外请提供 datasheet、package drawing、ball map、ordering guide、报价。

谢谢。

## 3. 发送注意

- 对外写“当前按 A5ED065B B32A 评估”，不要写最终已定。
- 短生命周期不是一票否决，但没有替代料和切换计划的料号不要作为主推。
- LPDDR5 pin list 等 Quartus / Fitter / FAE 结果后再冻结。
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/a5ed065b_b32a_lpddr5_sourcing_brief.md">
# A5ED065B B32A LPDDR5 寻样问题整理

日期：2026-05-11  
项目口径：A38 / DF108 Agilex 5  
报告类型：项目会议 + 采购跟进简报  
当前状态：`selected-not-frozen`，但 `A5ED065B B32A` 目标器件证据为 `TBD-evidence`

## 1. 当前结论

LPDDR5/LPDDR5X 寻样当前没有找到完全满足原始需求的料号：

| 原始需求 | 当前状态 |
|---|---|
| 单颗 2GB / 16Gb | 未找到长期稳定供货候选 |
| 单颗 x32 | 美光、三星候选均可到 x32 |
| LPDDR5 / LPDDR5X | 实际反馈主要转向 LPDDR5X |
| 商业级即可 | 三星 245FBGA 消费类生命周期不足；美光温度/等级仍待正式确认 |
| 5-8 年无 EOL 风险 | 旧 2GB 路线存在 EOL/停产风险；新 4GB 路线仍需供应商正式确认 |

当前可推进主线是美光 `MT62F1G32D2DS-020 WT:D`，但它是 `4GB / 32Gb x32 LPDDR5X`，不是原计划的 `2GB / 16Gb x32 LPDDR5`。如果每板仍按 2 颗 x32 规划，整板 LPDDR 容量会从原计划 4GB 上浮到 8GB。

## 2. A5ED065B B32A 证据缺口

本次在当前工作区、`my-daily`、本地 opendatasheet export 和 DF108 项目资料中，没有找到 `A5ED065B B32A` 的既有记录。现有 daily 与报告主要使用以下口径：

| 资料中出现的器件口径 | 状态 |
|---|---|
| `A5EC052A B32A` | 原理图/pin-net 工作表当前假设，daily 记录中用于 bank 2A/2B LPDDR5 x32 工作流 |
| `A5ED052A B32A` / `A5ED052AB32AE2V` | DF108 目标方案历史口径，仍有 A5EC/A5ED naming cleanup |
| `A5ED065B B32A` | `TBD-evidence`，需要确认是否为新的目标型号、口误，或后续器件升级 |

因此，不能把既有 `A5EC052A/A5ED052A B32A` 的 pin assign、bank 2A/2B、资源和 EMIF 结论直接签核迁移到 `A5ED065B B32A`。采购寻样结论可作为 LPDDR5/LPDDR5X 颗粒路线参考，但 FPGA 端可行性必须按最终确认为准的器件重新跑 Quartus / Pin Planner / Fitter。

## 3. 候选路线状态

| 路线 | 当前分类 | 证据状态 | 动作 |
|---|---|---|---|
| 美光 `MT62F1G32D2DS-020 WT:D` | Primary candidate | 已有供应商推荐和资料；生命周期、温度等级、价格、lead time、MOQ/MPQ、降频使用建议仍待正式回复 | 采购继续推进，作为主线寻样 |
| 三星 245FBGA `K3KL8L80DM-TGCT` | Rejected for mainline | 渠道反馈消费类、生命周期通常 2-3 年，不满足 5-8 年要求 | 不作为主推 |
| 三星 315FBGA x32 32Gb 路线 | Watchlist / parallel check | daily 中建议不要把三星全线关闭，但正式渠道证据仍待补 | 采购找正式渠道确认生命周期、样品、价格和 PCN/EOL 机制 |
| 南亚 / Nanya | Closed | 反馈没有 LPDDR5 | 关闭 |
| Henry / HSRP | Watchlist | 只见需求发出，未见回复 | 采购催一次 |
| 海力士 / Hynix | Watchlist | 当前无有效反馈 | 找其他渠道确认是否有 32Gb x32 LPDDR5X |

## 4. Daily 相关状态

| 日期 | 状态摘录 | 对寻样问题的影响 |
|---|---|---|
| 2026-05-08 | 完成 LPDDR5 采购寻样整理；美光主候选、三星/南亚/Henry 状态已形成报告 | 供应链侧进入“主线美光 + 三星正式渠道并行确认”的状态 |
| 2026-05-09 | `A38+agilex5方案的 lpddr5 fpga端网络连接好了` | 原理图 FPGA 端网络有进展，但只是 `schematic_connected` |
| 2026-05-09 | LP5 网络数量统计：U0 63、U1 63、总计 126 | 可作为 OrCAD/netlist 核对基线，不是签核证据 |
| 2026-05-09 | 架构评审后：two independent x32 + bank 2A/2B 继续作为主线，但 LPDDR5 原理图扩面暂停 | 继续推进前必须补 Quartus/Fitter/FAE 和封装确认 |
| 2026-05-09 | daily 明确提醒不要把美光 4GB 可评估写成料号已冻结 | 当前只能写 `selected-not-frozen` |

## 5. 必须拆开的三个决策

| 决策        | Owner          | 当前状态                                 | 输出物                                                |
| --------- | -------------- | ------------------------------------ | -------------------------------------------------- |
| 供应商正式回复   | 采购             | 待美光/WT/WPI、三星正式渠道、Henry/Hynix 补证     | 生命周期、温度等级、价格、lead time、MOQ/MPQ、降频建议、PCN/EOL 机制     |
| 容量是否接受上浮  | 项目 / 罗奇军       | 未确认                                  | 是否接受 2 颗 4GB x32 导致整板 8GB；成本、功耗、软件地址空间、初始化影响       |
| FPGA/逻辑验证 | 逻辑 / 吴志安 + FAE | 未见 Quartus / Pin Planner / Fitter 输出 | EMIF 配置、QSF、pin report、Fitter report、FAE review 结论 |

这三个决策不能合并成“LPDDR5 已确定”。供应商主候选、项目容量接受、FPGA pin/fitter 可行性是三个独立 gate。

## 6. 当前阻塞

| 阻塞项 | 影响 | 下一步 |
|---|---|---|
| `A5ED065B B32A` 未在本地资料中找到证据 | 无法判断既有 A5EC/A5ED052A pin/bank 假设是否适用 | 确认目标 FPGA 完整 ordering code，并补官方 pinout / package / power / EMIF 资料 |
| 2GB x32 长生命周期料号未找到 | 原始容量需求无法直接满足 | 决策是否接受 4GB x32 主流路线 |
| 美光主候选未获正式商务/生命周期闭环 | 不能冻结 BOM | 采购获取正式回复 |
| LPDDR5X 降频到 3733 MT/s 未经供应商和工具闭环 | 不能冻结时序和 SI 约束 | 要求供应商确认降频使用建议；逻辑跑 EMIF/Fitter |
| 最终封装未冻结 | memory-side ball mapping 可能变化 | 锁定料号/封装后重核 LPDDR5 颗粒侧 ball |
| LPDDR5 pin list 没有 Quartus/Fitter/FAE 证据 | 原理图继续扩面有返工风险 | 暂停扩面，先做 OrCAD 核对 + 最小工程验证 |

## 7. 采购问题清单

### 美光 / WT / WPI

请围绕 `MT62F1G32D2DS-020 WT:D` 要求供应商按表格回复：

| 问题 | 需要的回复格式 |
|---|---|
| 是否为长期主推料号 | Yes/No + roadmap/longevity 说明 |
| 是否支持未来 5-8 年供货 | 年限说明 + PCN/EOL 通知机制 |
| `WT:D` 温度等级和供货等级 | datasheet / ordering guide 截图或链接 |
| 样品、小批量、量产 lead time | 分别给周数 |
| 单价、MOQ、MPQ | 按数量阶梯 |
| 9600 Mb/s 料号是否可长期降频到 3733 MT/s | 原厂建议 + 初始化/ODT/training/SI 注意事项 |
| 是否仍有 2GB / 16Gb x32 长生命周期料号 | 料号 + 生命周期；没有则明确回复 No |

### 三星正式渠道

请不要只问 245FBGA 消费类料号，重点问 315FBGA / x32 / 32Gb LPDDR5X 路线：

| 问题 | 需要的回复格式 |
|---|---|
| 是否有 32Gb x32 315FBGA LPDDR5X 可供 | 料号 + datasheet/package |
| 料号生命周期是否能覆盖 5-8 年 | roadmap/longevity 或 PCN/EOL 机制 |
| 当前是否可供样 | sample lead time |
| 是否有工业级或扩展温度等级 | ordering code + 温度范围 |
| 是否适合 3733 MT/s 降频使用 | 原厂建议 |

## 8. 推荐下一步

1. 先确认 `A5ED065B B32A` 是否是最终目标器件；如果是，建立独立的器件证据包，不能沿用 `A5EC052A/A5ED052A` 的签核口径。
2. 采购继续以美光 `MT62F1G32D2DS-020 WT:D` 为主线拿正式回复，同时并行问三星 315FBGA x32 32Gb 路线。
3. 项目负责人明确是否接受整板 LPDDR 容量从 4GB 上浮到 8GB。
4. 逻辑侧用最终 FPGA 目标型号 + 美光主候选 + 三星并行候选各跑一次最小 Quartus EMIF / Pin Planner / Fitter。
5. 硬件侧保留当前 LPDDR5 网络为工作输入，标注 `schematic_connected / not_signoff / pending_quartus / pending_fae / pending_package_confirm`，不要冻结 pin list。

## 9. Source Links

- `/home/ubuntu/misc-tasks/lpddr5_report_decision.md`
- `/home/ubuntu/misc-tasks/lpddr5_report_procurement.md`
- `/home/ubuntu/misc-tasks/lpddr5_supplier_matrix.csv`
- `/home/ubuntu/my-daily/Daily/raw/2026-05-08/5月8日_extracted/lpddr5 情况群内反馈.md`
- `/home/ubuntu/my-daily/Daily/raw/2026-05-08/5月8日_extracted/lpddr5 情况群内反馈 2.md`
- `/home/ubuntu/my-daily/Daily/raw/2026-05-09/5月9日_extracted/今日完成项.md`
- `/home/ubuntu/my-daily/Daily/raw/2026-05-09/5月9日_extracted/LP5 网络数量统计.md`
- `/home/ubuntu/my-daily/Daily/compiled/2026-05-09/_cyberlog.md`
- `/home/ubuntu/my-daily/Daily/compiled/2026-05-09/_ai-context.md`

1. 先确认 `A5ED065B B32A` 是否是最终目标器件；如果是，建立独立的器件证据包，不能沿用 `A5EC052A/A5ED052A` 的签核口径。
2. 采购继续以美光 `MT62F1G32D2DS-020 WT:D` 为主线拿正式回复，同时并行问三星 315FBGA x32 32Gb 路线。
3. 项目负责人明确是否接受整板 LPDDR 容量从 4GB 上浮到 8GB。
4. 逻辑侧用最终 FPGA 目标型号 + 美光主候选 + 三星并行候选各跑一次最小 Quartus EMIF / Pin Planner / Fitter。
5. 硬件侧保留当前 LPDDR5 网络为工作输入，标注 `schematic_connected / not_signoff / pending_quartus / pending_fae / pending_package_confirm`，不要冻结 pin list。

这样的话我需要在公司内部项目群里面询问，来确定一些问题。你帮我撰写
以及需要回复各个代理商或者原厂邮件，我回复内容需要包括用4GB的颗粒，需要16bit die，选择普通的LPDDR5颗粒，不要选LPDDR5X颗粒。你帮我撰写
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/draft/LTC7883 + LTC7050.md">
LTC7883 + LTC7050 本质是一个分立式多相同步 Buck 电源：

  FPGA SDM PMBus
     |
     v
  LTC7883 数字电源控制器
     | PWM / EN / sense / fault
     v
  LTC7050 智能功率级
     | SW node
     v
  电感 + 输出电容
     |
     v
  A5E_VCC_VID / VCCP_VID -> FPGA VCC/VCCP

  1. LTC7883 是“大脑”

  它不直接给 FPGA 输出几十安培电流。它负责：

  - 通过 PMBus/I2C 和 FPGA SDM 通信；
  - 接收 SmartVID 电压设定；
  - 产生 PWM 信号；
  - 做软启动、时序、过压/欠压/过流保护；
  - 读取输出电压、电流、温度、fault；
  - 通过 EEPROM/NVM 保存默认配置。

  ADI 官方定义它是 Quad Output PolyPhase Step-Down DC/DC Voltage Mode Controller with Digital Power System Management，也就是四路/多相 buck 控制器，不是功率芯片。

  2. LTC7050 是“肌肉”

  它不懂 SmartVID，也不直接接 PMBus。它负责把 PWM 变成真正的大电流开关动作。

  每个 LTC7050 里面集成了：

  - high-side MOSFET；
  - low-side MOSFET；
  - gate driver；
  - current sense；
  - temperature / fault 监控；
  - 保护电路。

  ADI 官方叫它 Dual SilentMOS Smart Power Stage。简单理解：一个 LTC7050 里面有两个功率相位能力，每个相位再接一个电感，多个电感输出并到同一个 VCC rail。

  3. 多相是怎么来的

  一个 phase 大概是这样：

  LTC7883 PWMx
     -> LTC7050 channel x
     -> SWx
     -> Lx 电感
     -> VCCP_VID

  如果是 2-phase：

  PWM1 -> LTC7050 CH1 -> L1 -> VCCP_VID
  PWM2 -> LTC7050 CH2 -> L2 -> VCCP_VID

  如果电流更大，可以更多 phase 并联。多相的好处是：

  - 单颗功率器件压力低；
  - 热分布更好；
  - 输出纹波更低；
  - 瞬态响应更好；
  - 适合 FPGA core rail 这种大电流、低电压 rail。

  4. SmartVID 在这里怎么工作

  对 Agilex 5 SmartVID：

  FPGA 上电
    -> VCC/VCCP 先由 LTC7883 输出默认电压
    -> FPGA SDM 通过 PMBus 找到 regulator
    -> SDM 根据芯片 VID fuse 要求调整 VCC/VCCP 电压
    -> LTC7883 改变 PWM duty
    -> LTC7050 改变功率输出
    -> VCC/VCCP 到目标电压
    -> FPGA 继续配置

  所以 PMBus 只接到 LTC7883，不接 LTC7050。

  5. 原理图上要重点看这些连接

  | 类别 | 连接 |
  |---|---|
  | PMBus | FPGA PWRMGT_SCL/SDA -> LTC7883 SCL/SDA |
  | PWM | LTC7883 PWMx -> LTC7050 PWMx |
  | 功率路径 | 输入电源 -> LTC7050 VIN -> SW -> 电感 -> VCCP_VID |
  | 反馈采样 | FPGA VCCLSENSE/GNDSENSE 或 rail remote sense -> LTC7883 VSNS |
  | 电流/温度 | LTC7050 ISNS/TMON/FLT -> LTC7883 或监控网络 |
  | PGOOD/FAULT | LTC7883 -> sequencer / FPGA status |

  一句话理解：

  LTC7883 决定“输出多少伏、什么时候开、怎么保护”；
  LTC7050 负责“把输入电源高速开关成几十安培的 FPGA core 电源”。

  这个架构适合 Agilex 5 的 VCC/VCCP SmartVID，但最终相数、电感、电容、补偿、PMBus 配置和 NVM 默认电压必须按 Altera/ADI/FAE 确认。

  参考：

  - ADI LTC7883：PMBus 多相 buck 控制器
    https://www.analog.com/en/products/LTC7883.html
  - ADI LTC7050：dual smart power stage
    https://www.analog.com/en/products/LTC7050.html
  - Altera SmartVID：SmartVID 必须使用 PMBus-compliant regulator
    https://www.altera.com/design/resource/power/smartvid

给我找到封装原理图这些


前面我看的是 065B Modular Dev Kit SOM，不是你看的这个。现在我已下载并分析了：

  a5ed052a_min_system_pin_assign/sources/reference_schematic/065a_premium/agilex5e-065a-premium-devkit-b0-a3-altera.pdf

  在线来源：
  https://docs.altera.com/v/u/docs/r001645/agilextm-5-fpga-e-series-065a-premium-development-kit-dk-a5e065ab32aea-board-schematic

  核心结论：这份 065A Premium Devkit 里，确实大量用了 LTC7883AY#PBF + LTC7050AV#PBF。

  不是所有电源都用它，但主要 FPGA rail 很多都用了：

  | Rail | 方案 | 页 |
  |---|---|---|
  | FPGA_VCC / VCCcore | LTC7883 + LTC7050，两相 | Sheet 57/59/60 |
  | VCC_HSSI | LTC7883 + LTC7050 | Sheet 58/61 |
  | VCCERT_UX | LTC7883 + LTC7050 | Sheet 58/61 |
  | VCCPT | LTC7883 + LTC7050 | Sheet 62/64 |
  | VCCIO_3B_B | LTC7883 + LTC7050 | Sheet 62/64 |
  | VCCIO_2B3A3B_T | LTC7883 + LTC7050 | Sheet 63/65 |
  | VCCIO_HVIO | LTC7883 + LTC7050 | Sheet 63/65 |

  但还有一些 rail 不是这套：

  | Rail | 方案 |
  |---|---|
  | VCCIO_2A / 2V5_SYS | LTC3312SAAV#PBF |
  | 1V8_HVIO_6D / 1V8_LPDDR4 | MAX25302B |
  | DDR4 VTT/VREF | TPS51200DRCR |

  为什么 Premium Devkit 这么设计：

  - 它是完整 premium demo board，不是成本优化产品板。
  - 需要支持大量接口：DDR4、LPDDR4、FMC+、QSFP/SFP、MIPI、HPS 等。
  - 需要 PMBus 遥测、margin、fault、power-good、BTS 测试。
  - LTC7883 是控制器，LTC7050 是 smart power stage，适合低压大电流 rail。
  - 这套设计便于 Altera 做验证和调试，但客户产品可以按实际功耗缩放。原理图 Power Tree 页也明确写了 dev kit power tree 是 reference，建议客户按设计需求 scale。

  对你的 A5ED052AB32AE2V，这份 065A Premium Devkit 比 065B SOM 更值得重点参考，因为板上器件是 A5ED065AB32AE1V，和你的 A5ED052A... 更接近。但仍不能直接照抄相数和电流能力，052A
  规模比 065A 小，必须用 EPE/Quartus Power Analyzer 或 FAE 推荐重新估。

  我已整理成完整分析文件：
  a5ed052a_min_system_pin_assign/deliverables/altera_065a_premium_devkit_power_tree_explanation_zh.md
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/draft/agilex b32a 参考图.md">
 不是都一个芯片，应该分三层看：

  | 资料 | 实际器件 | 是否和你目标同芯片 | 主要用途 |
  |---|---|---:|---|
  | 你的目标 | A5ED052AB32AE2V | 是目标器件 | 最终设计对象 |
  | Altera 官方 065B SOM 原理图 | A5ED065B B32A | 不是 exact part，但同封装 B32A | 最高优先级参考：SDM、PMBus、VCC/SmartVID、启动配置 |
  | KEIm A5ESOM Rev1.10 | A5ED065BB32AE5SR0，B32A / BGA1591 | 不是 exact part，但同封装 B32A | 很有价值的实际 SOM 参考 |
  | Sulfur Type-A | carrier board，没有直接放 FPGA | 不是 FPGA 原理图 | 只参考 SOM 供电入口、PMBus 暴露、连接器使用 |

  关键点：

  A5ED052A 和 A5ED065B 不是同一个 die 规模。065B 资源更多，但它们都是 Agilex 5E Group B，并且都是 B32A 封装。所以 封装固定 pin、SDM/JTAG/配置、电源 ball、VCC/VCCP/SmartVID 这
  类连接参考价值很高。

  但不能说“完全一样”，因为：

  - 052A 和 065B 资源规模不同，某些 IO/硬核资源/NC/RFU 可能不同。
  - 官方 SOM、KEIm SOM、carrier 的板级架构不同。
  - VCC/SmartVID regulator 可以不一样：官方用 LTC7883 + LTC7050，KEIm 用 LTC7883 + NCP302035。
  - PMBus 主控关系不同：官方更像 SDM/板级 PMBus 体系，KEIm 是 SOM 暴露给 carrier，同时保留 SDM 路径。
  - DDR、eMMC、QSPI、时钟、复位、电源时序这些是板级方案，不是“同芯片就完全一样”。

  所以正确使用方式是：

  1. pin/ball 以 A5ED052A B32A 官方 pinout 为准。
  2. 原理图连接风格优先参考 Altera 官方 065B SOM。
  3. KEIm Rev1.10 作为同封装实际产品交叉验证，参考价值高。
  4. Sulfur Type-A 只看 carrier/SOM 连接和 PMBus 暴露，不拿它推 FPGA 内部电源方案。


</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/draft/lpddr5 pin assign 颗粒侧.md">
只看颗粒侧，用这几个文件：

  - lpddr5_315_DR_DS_U0_Bank2B_pin_net.tsv
    U0 颗粒侧 315-ball DS/DR ball -> net。
  - lpddr5_315_DR_DS_U1_Bank3A_pin_net.tsv
    U1 颗粒侧 315-ball DS/DR ball -> net。
  - orcad_hsio2b_lpddr5_x32_micron315b_side_aliases.csv
    更偏 OrCAD 符号用的颗粒侧 alias 表。
  - lpddr5_memory_pin_net_by_package_orcad_order.xlsx
    颗粒侧按 package / OrCAD 顺序整理的表，最适合画符号时用。

  颗粒侧重点：

  - A 通道 DQ0-DQ15：DQ*_A，ball 如 D1/C2/.../F11
  - B 通道 DQ0-DQ15：接系统 DQ16-DQ31，颗粒名是 DQ*_B
  - CA/CK/WCK/CS 是 A/B 共用 T-line，表里同一个 net 会对应 A/B 两个 ball
  - RESET_N 是单独 ball：H1
  - ZQ_A 是颗粒本地 240R 到 VDDQ，不接 FPGA
  - FPGA 的 RZQ、REFCLK 不属于 LPDDR5 颗粒侧，不要画到颗粒符号里

  你画 315-ball 颗粒符号时，优先用 lpddr5_memory_pin_net_by_package_orcad_order.xlsx。如果只要文本核对，用两个 lpddr5_315_DR_DS_U*_pin_net.tsv。





</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/draft/lpddr5 封装.md">
供应商问我用那个封装的，这个怎么判断？


• 封装判断原则很简单：先按“可采购 + 可布板 + 可替代”选，不是只看尺寸。

  建议你先这样定口径：

  优先封装：315-ball FBGA / TFBGA，x32。
  原因：

  1. 之前美光候选 MT62F1G32D2DS-020 WT:D 是 315-ball TFBGA，现有 pin/net 工作也基本围绕 315-ball 参考展开。
  2. 315-ball 比 245FBGA 更适合高速存储布线、扇出和后续替代料兼容。
  3. 三星那个 245FBGA 虽然也是 x32，但封装更小、ball map 不同，换上去等于 footprint / fanout / memory-side ball mapping 都要重做。
  4. 你现在还没冻结最终 LPDDR5 pin list，所以不应把 245FBGA 作为默认方向。

  可以直接回复供应商：

  > 我们优先考虑 315-ball FBGA / TFBGA 封装，x32 interface，单颗 4GB / 32Gb，普通 LPDDR5，16bit die。
  > 如果有多个 package option，请优先推荐 315-ball 版本，并提供 package drawing、ball map、datasheet 和可替代料号。
  > 245FBGA 暂不作为优先方案，除非没有 315-ball 可选，并且供应商能提供生命周期、替代料和兼容性说明。

  如果供应商继续追问 DS/DV 这类 package code，可以说：

  > 目前优先按 315-ball TFBGA 方向评估；具体 package code 以可供料号、生命周期、替代料和 ball map 为准，暂未冻结。

</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/draft/smartvid方案.md">
 推荐策略：不要在这两个参考方案之间盲选功率级，先让 FAE 帮你确认 SmartVID regulator 料号。
  如果必须先画原理图，我建议：

  1. 原理图架构优先按 Altera 官方 065B SOM：
     SDM PMBus -> SmartVID regulator -> VCC/VCCP，VCCLSENSE/GNDSENSE 做 remote sense。
  2. regulator 料号优先问 FAE 是否可用 fully validated 器件：
     TPS53676 / LTC3882-1 / ISL68223。Altera SmartVID 页面明确说 fully validated regulator 会随 Quartus Prime Pro release 做 regression validation；而 LTC7883 是 API validated
     only。
  3. 如果 FAE 同意用 LTC7883，再优先参考 Altera 官方 SOM 的 LTC7883 + LTC7050，KEIm 的 LTC7883 + NCP302035 做交叉参考。
     原因是 KEIm 是 SOM/Carrier 架构，PMBus 管理方式和你独立板未必一致。

  FAE 可以这样问，直接复制发：

  我们项目准备使用 Agilex 5E A5ED052AB32AE2V，B32A 封装，板上需要设计 VCC/VCCP SmartVID 电源。

  目前参考到两套 B32A 相关原理图：

  4. Altera Agilex 5E 065B Modular Development Kit SOM
     - FPGA: A5ED065B B32A
     - SmartVID rail: +V0P8_VCCP_VID
     - Controller: LTC7883
     - Power stage: LTC7050
     - PMBus: FPGA SDM PWRMGT_SCL/PWRMGT_SDA 参与管理

  5. KEIm A5ESOM Rev1.10
     - FPGA: A5ED065BB32AE5SR0, B32A / BGA1591
     - SmartVID rail: VCC_VID
     - Controller: LTC7883AY#PBF
     - Power stage: NCP302035MNTWG
     - PMBus 同时有 SOM_PMBUS 和 SDM_PWRMGT 路径，部分 0R 为可选

  请帮忙确认：

  6. 对 A5ED052AB32AE2V，VCC/VCCP 是否必须按 SmartVID PMBus regulator 设计？
  7. 新产品首版更推荐哪颗 regulator？
     - TPS53676
     - LTC3882-1
     - ISL68223
     - LTC7883
  8. 如果使用 LTC7883，是否可以按 Altera 065B SOM 的 LTC7883 + LTC7050 方案参考？
  9. KEIm 的 LTC7883 + NCP302035 方案是否也适用于 A5ED052AB32AE2V？是否有已验证限制？
  10. 本项目没有外部电源管理 MCU，是否建议使用 FPGA SDM PMBus Master Mode？
  11. 请确认 PMBus address、PAGE、Vout format coefficient、初始 VCC/VCCP 电压、NVM 配置和 Quartus 需要设置的参数。
  12. VCC/VCCP 之外的 0.8V 类 rail 是否允许与 SmartVID rail 共轨，还是必须独立供电？
  13. 是否有针对 A5ED052AB32AE2V + B32A 的官方 power tree / reference schematic / PDN checklist 可提供？

  一句话结论：默认方案选“Altera 官方 065B SOM 架构 + FAE 推荐 fully validated regulator”；只有 FAE 明确确认后，才把 LTC7883 作为最终方案。

  来源：Altera SmartVID 页面列出 Agilex 5 fully validated regulator 为 TPS53676 / LTC3882-1 / ISL68223，LTC7883 为 API validated only，并说明 SmartVID 必须使用 PMBus-compliant
  regulator。
  https://www.altera.com/design/resource/power/smartvid
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/draft/电源设计.md">
 不是所有 FPGA 电源都用 LTC7883 + LTC7050。官方 065B SOM demo 是这样分层的：

  | Rail | Demo 方案 | 标注能力 | 说明 |
  |---|---|---:|---|
  | +V0P8_VCCP_VID | LTC7883AY#PBF + LTC7050AV#PBF | 0.8V @ 36A | SmartVID 核心 rail，给 VCC/VCCP |
  | +V1P0 | LTC7883AY#PBF + LTC7050AV#PBF | 1.0V @ 14A | 大电流固定 rail |
  | +V0P8 | LTC7883AY#PBF + LTC7050AV#PBF | 0.8V @ 17A | 大电流固定 rail |
  | +V1P8 | MP8870GL-0012 | 1.8V @ 8.2A | PMBus buck |
  | +V1P2 | MP8796BGVT-0023 | 1.2V @ 12.5A | PMBus buck |
  | +V5P0_STBY/+V3P3_STBY/+V2P5_STBY | MPM54304GMN-0044 | 多路 standby | 上电/控制/待机电源 |
  | +V1P8_STBY | MPM3804GG | 1.8V @ 0.1A | 小 standby rail |
  | +V3P3/+V2P5 | MP5087GG-Z | load switch | 从 standby rail 受控打开 |
  | DDR VTT | MP20075DH | 0.6V @ 0.5A | DDR 终端电源 |

  为什么 LTC7883 + LTC7050 用在前三路：
  LTC7883 是 PMBus 数字控制器，负责 SmartVID、电压设定、PWM、保护和遥测；LTC7050 是功率级，负责真正输出大电流。这个组合适合 低电压、大电流、需要 PMBus 管理 的 FPGA core rail。

  所以 demo 的设计逻辑是：

  SmartVID / 大电流核心 rail -> LTC7883 + LTC7050
  普通 PMBus buck rail       -> MP8870 / MP8796B
  standby rail               -> MPM54304 / MPM3804
  受控 3.3V/2.5V             -> MP5087 load switch
  DDR VTT                    -> MP20075

  我已整理成文件：
  a5ed052a_min_system_pin_assign/deliverables/altera_065b_som_power_tree_explanation_zh.md

  对你的 A5ED052AB32AE2V，可复用的是架构思路，不要直接照抄电流值。052A 比 demo 的 065B 规模小，36A/14A/17A 这些要用 EPE/Quartus Power Analyzer 或 FAE 建议重新估。


你是看的哪个demo？我看的agilex5e-065a-premium-devkit-b0-a3-altera 这个原理图的，你也分析下？。
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/eDP眼图.md">
以下内容综合了 Keysight 《D9040EDPV eDP Test Application Methods of Implementation》手册（2020 年版）和 Tektronix 展示的眼图测量方法，对 8.1 Gbps（HBR3）速率下 eDP 接收端眼图的要求作出说明。

### 测量点

- **TP3_EQ（或 RX_EQ）**：eDP 接收端眼图在 TP3 端（经过 CTLE 均衡后）测量。测试使用 CP2520 码型，必须对信号进行均衡以模拟显示驱动芯片的连续时间线性均衡(CTLE)。
- **眼图位置**：标准要求动态生成眼图遮罩——遮罩沿 0 mV 处确定宽度，眼高测量区位于 0.375 UI 到 0.625 UI 之间。遮罩必须居中放置在眼图的最大开口位置。

### eDP 1.4/1.4b （HBR3 8.1 Gbps）接收端眼图遮罩

Keysight MOI 给出了 eDP 1.4/1.4b Sink 端的 TP3_EQ 眼图遮罩六个顶点，时间轴用 UI（Unit Interval）表示，电压单位为毫伏(mV)，具体如下：

|顶点|时间 (UI)|最小电压值（mV）|
|---|---|---|
|1|0.01|0|
|2|0.11|**+90**|
|3|0.89|**+90**|
|4|0.99|0|
|5|0.89|**–90**|
|6|0.11|**–90**|

这些坐标构成一个闭合多边形，规定了可接受的最小眼开口。根据图形：

- **眼宽（Eye Width）**：从 0.11 UI 到 0.89 UI 之间，即必须 ≥0.78 UI。这部分是“通过区”——信号轨迹不得触碰或进入遮罩。
- **眼高（Eye Height）**：垂直方向在 ±90 mV 处，遮罩顶端和底端的电压分别为 +90 mV 和 –90 mV。

相比源端（Source DUT）70 mV 的遮罩，接收端遮罩使用 90 mV 的高度。这是因为接收端在测试时通常需要更大的眼高裕量，以抵消均衡电路及噪声对信号的影响。

### 附加注意事项

1. **动态遮罩**：遮罩横向位置应自动调整至眼图的最大开口处；纵向顶点需放置在眼图最大幅度处。
2. **合格判定**：在测试过程中，应折叠 10 个以上的 UI 并观察眼图；如果任何信号轨迹进入遮罩区域则视为不合格。
3. **其他规范**：测试还需满足 eDP 1.4b 规定的差分峰峰值、电平和抖动等要求；例如，TP3_EQ 差分峰峰电压应至少 75 mV 并保持眼宽≥0.5 UI。
4. **工作在 8.1 Gbps 时**：单位间隔(UI)约 123.5 ps，遮罩坐标仍按 UI 表示；因此 0.78 UI 的宽度约 96.3 ps，眼高 ±90 mV 为信号幅度的净开口。

综上所述，8.1 Gbps eDP 接收端在 TP3_EQ 测量点的眼图遮罩要求是：在 ±90 mV 的高度和 0.11~0.89 UI 的宽度内建立一组六点的闭合多边形，信号波形折叠后必须完全位于该遮罩外；遮罩的宽度位置基于眼图最大开口处动态确定

8.1Gbps mainstream的眼图要求是怎么样的，眼宽眼高要求怎么样，需要多个数据源来进行高度可靠的确认
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/eDP眼图标准.md">
可信度高，可入知识库。

附件 eDP v1.4b：

HBR3 = 8.1Gbps/lane，1UI≈123ps。  
TP3_EQ EYE mask：**75mVpp differential / 0.5UI**。  
其中 75mVpp 来自 +37.5mV / -37.5mV，0.5UI≈61.5ps。

所以我们内部建议按：

**最低判断：75mVpp differential / 0.5UI**  
**更稳妥目标：90mVpp differential / 0.5UI**

之前看到的 **75mV / 0.35UI** 更偏普通 DP RX/接收能力测试资料，不能作为 eDP v1.4b 附件标准的主结论。

参考：

1. 附件 eDP v1.4b：Table 4-11 / Table 4-18
    
2. Intel / Altera AN745：HBR3 RX 75mV / 0.35UI  
    [https://docs.altera.com/r/docs/683623/current/an-745-design-guidelines-for-displayport-ip-interface/main-link-rx-electrical-specifications?contentId=hLW5MMuFf5GkETGJqJ~R2A](https://docs.altera.com/r/docs/683623/current/an-745-design-guidelines-for-displayport-ip-interface/main-link-rx-electrical-specifications?contentId=hLW5MMuFf5GkETGJqJ~R2A)
    
3. Tektronix DP1.4 RX：HBR3 RX 75mV / 0.35UI  
    [https://www.tek.com.cn/sites/default/files/2018-05/DisplayPort-1.4%20Challenges-and-Solutions%20Webinar-2017-61W-61165-0-170417.pdf](https://www.tek.com.cn/sites/default/files/2018-05/DisplayPort-1.4%20Challenges-and-Solutions%20Webinar-2017-61W-61165-0-170417.pdf)
    
4. Tektronix DP1.4 HBR3：90mV / 0.5UI  
    [https://www.tek.com.cn/sites/default/files/2018-05/DisplayPort%20over%20Type-C-TX-RX.pdf](https://www.tek.com.cn/sites/default/files/2018-05/DisplayPort%20over%20Type-C-TX-RX.pdf)

eDP 1.4b / HBR3 / 8.1Gbps 接收端眼图，建议以附件 eDP v1.4b 标准为准，不直接套普通 DP 的 RX 数值。

</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/lpddr5 群内沟通.md">
各位同步一下 A38 / A57 + Agilex 5 的 DDR / LPDDR5 方案评估。

1. 原 DF108 DDR4 方案
    

原 DF108 最大线速 2.5Gbps/lane，摄像头端最大数据量约 80Gbps。

原方案使用 4 颗 DDR4，型号 H5AN4G6NBJR，单颗规格 4Gb / x16，总位宽 64bit，总容量 2GB，理论峰值带宽约 153.6Gbps。

2. 当前 Agilex 5 LPDDR5 方案
    

当前最大线速提升到 4Gbps/lane，摄像头端最大数据量约 128Gbps。

初步 LPDDR5 方案为 2 颗 LPDDR5，单颗规格 4GB / 32Gb，x32，总位宽 64bit，总容量 8GB。按主控侧约 3733MT/s 计算，理论峰值带宽约 239Gbps。

目前我这边正在确认 LPDDR5 寻样和价格。

3. 当前需要确认的问题
    

问题一：LPDDR5 容量和速率都有一定过配。

目前 x32 LPDDR5 中，2GB / 16Gb 颗粒基本停产，市场上更容易找到的是 4GB / 32Gb 规格，而且这类颗粒速率通常在 7500MT/s 以上。因此 LPDDR5 方案带宽是够的，但容量和颗粒规格偏过配。

问题二：Agilex 5 LPDDR5 控制器位宽有限制。

Agilex 5 单个 LPDDR5 控制器最高支持 32bit。如果要做 64bit 总位宽，需要使用双 LPDDR5 控制器。这个需要软件侧确认是否好实现。

@何海山(hehs) @吴锋(wuf) @Candy|罗奇军(luoqj) @路阳(luy) @邱永恒(qiuyh)

4. A57 + Agilex 5 场景下的两种方案
    

由于 LPDDR5 x16 单颗极不主流，同时 Agilex 5 的 HSIO bank 资源有限。一个 HSIO bank 最多约 7 组 MIPI，总共 4 个 HSIO bank。如果两个 bank 给 MIPI，两个 bank 给 DDR/LPDDR5，就会影响 MIPI 数量。

方案一：使用 LPDDR5

大约 14 组 MIPI，2 × 32bit LPDDR5，理论峰值带宽约 239Gbps。

优点是带宽裕量大，颗粒方向相对主流。缺点是总容量偏大，需要双 LPDDR5 控制器，且 MIPI 数量会减少到约 14 组。

方案二：使用 DDR5

大约 16 组 MIPI，16bit + 32bit DDR5，按 3600MT/s 计算，理论峰值带宽约 173Gbps。

优点是可以保留更多 MIPI 通道。缺点是带宽裕量小于 LPDDR5，且 16bit + 32bit DDR5 的实现方式还需要进一步确认。

5. 当前核心取舍
    

这个问题本质上是在权衡 MIPI 数量、HSIO bank 资源、内存带宽、颗粒可采购性和控制器实现复杂度。

请大家重点帮忙确认：

1）双 LPDDR5 控制器软件侧是否好实现；  
2）A57 场景下是否必须保留 16 组 MIPI；  
3）DDR5 约 173Gbps 理论带宽是否够用；  
4）LPDDR5 8GB 容量过配是否可以接受。
</file>
<file path="Daily/raw/2026-05-11/5月11日_extracted/群内沟通 lpddr.md">
各位同步一下 **A38 / A57 + Agilex 5 的 DDR / LPDDR5 方案评估进展**。

### 一、原 DF108 DDR4 方案回顾

原 DF108 最大线速支持 **2.5Gbps/lane**，摄像头端最大数据量约 **80Gbps**。

原方案使用 **4 颗 DDR4**：

- 型号：H5AN4G6NBJR
    
- 单颗规格：4Gb / x16
    
- 颗粒数量：4 颗
    
- 总位宽：64bit
    
- 总容量：2GB
    
- 理论峰值带宽：约 **153.6Gbps**
    

---

### 二、当前 Agilex 5 方案需求

当前方案最大线速提升到 **4Gbps/lane**，摄像头端最大数据量约 **128Gbps**，因此内存带宽需要重新评估。

原计划 LPDDR5 方案如下：

- 颗粒数量：2 颗 LPDDR5
    
- 单颗规格：4GB / 32Gb，x32
    
- 总位宽：64bit
    
- 总容量：8GB
    
- 按主控侧约 **3733MT/s** 计算，理论峰值带宽约 **239Gbps**
    

目前我这边正在进行 LPDDR5 寻样和价格确认。

---

### 三、当前需要确认的两个问题

#### 问题 1：容量和速率都超过实际需求

目前 x32 LPDDR5 颗粒中，**2GB / 16Gb 规格基本停产或很难采购**，市场上更容易找到的是 **4GB / 32Gb、x32** 规格。

这样会带来两个结果：

1. 总容量变成 **8GB**，明显超过当前实际需求；
    
2. 颗粒标称速率通常在 **7500MT/s 以上**，也高于当前 Agilex 5 实际可用速率需求。
    

也就是说，LPDDR5 方案从带宽上是够的，但容量和颗粒规格存在一定“过配”。

#### 问题 2：Agilex 5 LPDDR5 控制器位宽限制

Agilex 5 单个 LPDDR5 控制器最高只支持 **32bit 位宽**。

如果要实现 **64bit 总位宽**，需要使用 **双 LPDDR5 控制器**，也就是：

- 1 颗 x32 LPDDR5 对应 1 个控制器；
    
- 2 颗 x32 LPDDR5 对应 2 个控制器；
    
- 系统侧需要软件/逻辑确认是否容易管理和使用。
    

这一点需要软件侧一起评估：  
@何海山(hehs) @吴锋(wuf) @Candy|罗奇军(luoqj) @路阳(luy) @邱永恒(qiuyh)

---

### 四、A57 + Agilex 5 摄像头方案下的 DDR 选择影响

对于 A57 + Agilex 5 方案，由于 **LPDDR5 x16 单颗极不主流**，而 Agilex 5 的 HSIO bank 资源又比较紧张：

- 一个 HSIO bank 最多支持约 7 组 MIPI；
    
- 总共有 4 个 HSIO bank；
    
- 如果其中 2 个 bank 给 MIPI，另外 2 个 bank 给 DDR/LPDDR5，则摄像头通道数和内存方案会互相影响。
    

目前可以看到两种方案：

---

#### 方案 1：使用 LPDDR5

资源分配：

- 2 个 HSIO bank 给 MIPI；
    
- 2 个 HSIO bank 给 LPDDR5；
    
- MIPI 数量约 **14 组**；
    
- 内存为 **2 × 32bit LPDDR5**；
    
- 理论峰值带宽约 **239Gbps**。
    

优点：

- 带宽裕量较大；
    
- LPDDR5 x32 颗粒更主流；
    
- 可以满足 128Gbps 摄像头数据量需求。
    

风险 / 代价：

- 总容量可能过大；
    
- 需要双 LPDDR5 控制器；
    
- MIPI 资源被压缩到约 14 组；
    
- 软件/逻辑侧需要确认双控制器使用复杂度。
    

---

#### 方案 2：使用 DDR5

资源分配：

- 可以保留约 **16 组 MIPI**；
    
- 内存方案为 **16bit + 32bit DDR5**；
    
- 按 3600MT/s 计算，理论峰值带宽约 **173Gbps**。
    

优点：

- MIPI 通道数更多，可支持约 16 组；
    
- 带宽相比原 DF108 DDR4 方案仍有提升；
    
- 可能更适合摄像头通道数优先的场景。
    

风险 / 代价：

- 带宽裕量小于 LPDDR5 方案；
    
- 16bit + 32bit 的 DDR5 组合方式需要进一步确认控制器、布线和软件支持；
    
- 后续需要评估是否足够覆盖 128Gbps 摄像头数据量及系统缓存需求。
    

---

### 五、当前初步判断

如果优先保证内存带宽裕量，LPDDR5 方案更稳妥：

> **14 组 MIPI + 2 × 32bit LPDDR5，理论带宽约 239Gbps。**

如果优先保证摄像头通道数量，DDR5 方案更有优势：

> **16 组 MIPI + 16bit + 32bit DDR5，理论带宽约 173Gbps。**

当前核心矛盾不是单纯选 DDR5 还是 LPDDR5，而是：

> **MIPI 通道数量、HSIO bank 资源、内存带宽、颗粒可采购性、控制器实现复杂度之间的取舍。**

请大家重点帮忙确认：

1. 双 LPDDR5 控制器在软件/逻辑侧是否好实现；
    
2. A57 场景下是否必须保留 16 组 MIPI；
    
3. 173Gbps DDR5 理论带宽是否足够覆盖当前系统需求；
    
4. LPDDR5 8GB 容量过配是否可以接受；
    
5. 当前 LPDDR5 / DDR5 颗粒供货、价格和生命周期是否可接受。


这几份参考原理图有什么区别，那不都是一个芯片吗
</file>
