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
