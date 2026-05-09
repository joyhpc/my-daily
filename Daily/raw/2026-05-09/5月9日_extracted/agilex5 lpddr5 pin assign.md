我按这个假设给你落表了：A5EC052A B32A，两颗独立 x32 LPDDR5，分别放在 IO96 bank
  2A 和 2B。

  具体 pin assign 已生成成 CSV：

  - lpddr5_x32_a5ec052a_b32a_2chips.csv
  - lpddr5_x32_a5ec052a_b32a_all_io96_banks.csv

  关键分配是：

  - U_LPDDR5_0 -> FPGA IO96 bank 2A
  - U_LPDDR5_1 -> FPGA IO96 bank 2B
  - MEM_DQ[0:15] -> LPDDR5 channel A
  - MEM_DQ[16:31] -> LPDDR5 channel B
  - CA/CK/CS/WCK 是 T-line，同一 FPGA 信号要同时接 LPDDR5 A/B channel 对应 ball
  - FPGA_RZQ 是 FPGA OCT 电阻脚，不是 LPDDR5 颗粒的 ZQ
  - REFCLK_P/N 接 EMIF PLL reference clock，不接内存颗粒

  我找到的公开 LPDDR5 颗粒参考是 Micron MT62F1G32D4DR-031 WT:B，x32，315-ball，
  Antmicro 有完整开源 KiCad 和原理图。Antmicro 页面写明它是 315-ball WFBGA 12.4
  mm x 15.0 mm LPDDR5 footprint，并列了该 Micron 料号；原理图 PDF 里也能看到 A/B
  channel 的 ball，例如 CA0_A@G4、CA0_B@R12、DQ0_A@D1、DQ0_B@V15 等。我已把这些
  memory-side balls 一并放进 CSV。

  资料来源：

  - Altera A5EC052A 官方 pinout：https://docs.altera.com/v/u/resources/830445/p
  in-information-for-the-agilextm-5-a5ec052a-device-xlsx-format-alt.-format-pdf
  (https://docs.altera.com/v/u/resources/830445/pin-information-for-the-agilextm-5-a5ec052a-device-xlsx-format-alt.-format-pdf)
  - Altera LPDDR5 pin placement / data width mapping：https://docs.altera.com/r
  /docs/817467/25.3.1/external-memory-interfaces-emif-ip-user-guide-agilextm-5-
  fpgas-and-socs/lpddr5-data-width-mapping
  (https://docs.altera.com/r/docs/817467/25.3.1/external-memory-interfaces-emif-ip-user-guide-agilextm-5-fpgas-and-socs/lpddr5-data-width-mapping)
  - Antmicro LPDDR5 Testbed 原理图：https://openhardware.antmicro.com/imported/
  boards/lpddr5-testbed/doc/lpddr5-testbed-main-cea331b8-schematic.pdf
  (https://openhardware.antmicro.com/imported/boards/lpddr5-testbed/doc/lpddr5-testbed-main-cea331b8-schematic.pdf)
  - Antmicro GitHub/KiCad：https://github.com/antmicro/lpddr5-testbed
  (https://github.com/antmicro/lpddr5-testbed)
  - Micron/DigiKey 封装信息参考：https://www.digikey.com/en/products/detail/mic
  ron-technology-inc/MT62F1G32D2DS-020-WT-F-TR/26955302
  (https://www.digikey.com/en/products/detail/micron-technology-inc/MT62F1G32D2DS-020-WT-F-TR/26955302)

  注意：如果你实际 FPGA 不是 A5EC052A B32A，FPGA ball 会变；如果实际 LPDDR5 不是
  Micron 315-ball 这类封装，memory-side ball 会变，但 Altera 侧 EMIF lane 规则不
  变。下板前还要在 Quartus 里用目标 EMIF IP 做一次 fitter test-fit。
