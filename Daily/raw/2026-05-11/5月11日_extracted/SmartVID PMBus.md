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