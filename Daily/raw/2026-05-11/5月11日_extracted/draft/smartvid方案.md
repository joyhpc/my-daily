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
