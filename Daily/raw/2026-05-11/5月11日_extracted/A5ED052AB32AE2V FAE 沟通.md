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
