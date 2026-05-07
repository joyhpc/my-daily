
详细版本，但是我没有发送
各位，我目前在设计DF108+A5ED052A B32A方案的原理图。
使用的是lpddr5，但是无相关的原理图参考设计。
FAE 建议不要由硬件侧单独手工定 pin，最好由 FPGA/逻辑侧先建 Quartus 验证工程，把关键高速接口一起放进去验证。
 这次建议一次性验证：

  1. LPDDR5 / EMIF
  2. MIPI D-PHY
  3. QSFP / transceiver

  原因是这些接口都会占用特定 bank/lane/PLL/RZQ/refclk/电压域资源，单独看某一个接口可能没问题，但组合到同一个 FPGA 后可能出现资源冲突或 fitter 约束不过。为
  了避免原理图和 PCB 做完后再返工，建议先由逻辑侧建一个最小工程完成 pin planning/fitter 验证。

  请 FPGA/逻辑同事协助输出：

  4. A5ED052A B32A 最小 Quartus 工程；
  5. LPDDR5 + MIPI + QSFP 的组合配置；
  6. 通过编译或至少 Pin Planner/Fitter 规则检查；
  7. 可用于硬件设计的 pin assignment / QSF / pin report；
  8. 明确 DDR、MIPI、QSFP 是否存在 bank/lane/PLL/refclk/RZQ/电压域冲突；
  9. 给出“可用于原理图设计”的最终 pin list。

  硬件侧可以提供 LPDDR5 颗粒型号、位宽、速率、ECC 配置，MIPI lane 数/方向/速率，QSFP 速率和通道数等输入。请问这部分由哪位逻辑同事主导比较合适？我们希望关键
  接口在工程验证通过后再锁定原理图。



我最终发送的简版
**各位好，DF108+A5ED052A B32A 原理图设计需要逻辑团队协助前置验证一下高速接口。**

**背景：** FAE 强烈建议 LPDDR5、MIPI D-PHY、QSFP 不要由硬件盲分 Pin 脚，否则极易出现 Bank/PLL/电压域等底层资源冲突，导致后期 Fitter 失败和 PCB 大改。 **诉求：** 需要逻辑侧帮忙建一个最小 Quartus 工程，把这几个接口一起放进去跑一下综合验证，确保没有资源冲突。

**协同步骤：**

1. 硬件侧提供：LPDDR5、MIPI、QSFP 的型号、速率、位宽及通道数等参数。
    
2. 逻辑侧输出：通过 Fitter 检查的最小工程，以及**最终可用于原理图设计的 Pin list**。
    

请问逻辑组这边哪位兄弟（**@吴志安** ？）方便主导一下这个前置验证？我们等验证通过后再锁定原理图。辛苦评估下时间，谢谢！