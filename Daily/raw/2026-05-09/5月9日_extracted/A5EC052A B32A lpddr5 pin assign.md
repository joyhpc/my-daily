lpddr5_x32_a5ec052a_b32a_2chips.csv 不是原始下载文件，是我合成的连接表，来源
  是：

  1. FPGA ball 位置
     Altera 官方 A5EC052A B32A pinout xlsx：

  https://docs.altera.com/v/u/resources/830445/pin-information-for-the-agilextm-5-a5ec052a-device-xlsx-format-alt.-format-pdf

  (https://docs.altera.com/v/u/resources/830445/pin-information-for-the-agilextm-5-a5ec052a-device-xlsx-format-alt.-format-pdf)
  2. LPDDR5 EMIF pin/index 规则
     Altera EMIF User Guide 817467_D842785.pdf，主要用 LPDDR5 Pin Placement、
     Address and Command Pin Placement、LPDDR5 Data Width Mapping。

  https://docs.altera.com/r/docs/817467/25.3.1/external-memory-interfaces-emif-ip-user-guide-agilextm-5-fpgas-and-socs/lpddr5-data-width-mapping

  (https://docs.altera.com/r/docs/817467/25.3.1/external-memory-interfaces-emif-ip-user-guide-agilextm-5-fpgas-and-socs/lpddr5-data-width-mapping)
  3. LPDDR5 颗粒封装 ball mapping
     Antmicro 开源 LPDDR5 testbed，Micron MT62F1G32D4DR-031，315-ball package。
     https://github.com/antmicro/lpddr5-testbed
     (https://github.com/antmicro/lpddr5-testbed)

  其中 U_LPDDR5_0 -> bank 2A、U_LPDDR5_1 -> bank 2B 是我按两颗 x32 独立接口做的
  分配假设。

x32 LPDDR5 的信号到 index 的规则来自另一个官方文档：

  External Memory Interfaces (EMIF) IP User Guide Agilex 5
  章节/表：

  - Table 22. LPDDR5 Pin Placement
  - 9.2.4.2 LPDDR5 Data Width Mapping
  - Figure 34. LPDDR5 1chx32, Single Rank

  组合方式是：

  EMIF User Guide: x32 index 0 = MEM_DQ[0]
  加上
  A5EC052A B32A pinout: bank 2A index 0 = CL91
  所以得到
  MEM_DQ[0] -> FPGA ball CL91
Table 22. LPDDR5 Pin Placement 里面的pin index，x32,2channel x16分别是什么意思，和我使用的场景对应吗




Table 22 里的 Pin Index 是 FPGA 某个 IO96 bank 内的 0-95 号位置，不是 LPDDR5
  颗粒的 ball number。

  含义：

  - x32：一个 LPDDR5 x32 interface。
    对应一颗 x32 LPDDR5 颗粒作为一个 32-bit EMIF 接口使用。
    DQ[0:15] 接 LPDDR5 channel A，DQ[16:31] 接 channel B，CA/CK/CS/WCK 按 x32 拓
    扑共享/T-line 到 A/B。
  - 2 Channel x16：两个独立 x16 channel。
    表里会变成 MEM_0_* 和 MEM_1_*。每个 x16 channel 有自己的 CA/CK/CS/WCK。它不
    是“32-bit 总线”的同一种连接方式，而是双 x16 独立通道拓扑。

  你的场景如果是 两颗 x32 LPDDR5，每颗作为一个 32-bit interface，那应该用：

  - 第一颗：选一个 IO96 bank，用 x32 column
  - 第二颗：另一个 IO96 bank，再用一次 x32 column

  所以我之前的 FPGA 侧 assign 是按 x32 column 套到 bank 2A、bank 2B 得来的。

  如果你的真实需求是 把一颗 x32 LPDDR5 当成两个独立 x16 channel 来用，那才用 2
  Channel x16 column；这种情况下之前那份 CSV 的 CA/CK/WCK 分配就不对，需要重出。


EMIF 规则里的 Pin Index
          ↓ 查 FPGA pinout xlsx
  FPGA package ball / pin number
          ↓ 画原理图连接
  LPDDR5 颗粒 pin name / ball

  举例，假设用 A5EC052A B32A 的 bank 2A，并按 LPDDR5 x32：

  Table 22:
  Pin Index 0 = MEM_DQ[0]

  A5EC052A B32A pinout:
  bank 2A, index 0 = FPGA ball CL91

  LPDDR5 颗粒 ballout:
  MEM_DQ[0] 应接到颗粒 DQ0_A，比如 Micron 315-ball 是 D1

  所以原理图上实际画的是：

  FPGA ball CL91  ->  LPDDR5 DQ0_A / ball D1

  Pin Index 本身不会出现在原理图封装上。它只是 Altera 用来描述 IO96 bank 内部固
  定位置的编号，用来告诉你“哪个 EMIF 信号必须放在 bank 里的哪个相对位置”。


我现在需要用HISO 2B来画进行pin assign，画原理图时我用的orcad，我怎么很快利用这个pin和网络对应的关系，把这部分原理图画完。我不想手动输入。要及其高效。



优先选 FPGA 厂家已经验证过、Quartus EMIF 能 test-fit 通过、且供应链可买到的封
  装。如果两者都支持，做板优先级通常是：

  1. 有 FPGA/板厂 reference design 的封装
  2. 量产可供货、生命周期更稳的料号
  3. PCB 更好走线的封装
  4. 你的工厂能稳定焊接/返修的封装

  对你这种 两颗 x32 LPDDR5 接 Agilex 5 的场景，如果没有别的限制，我会倾向先问清
  楚并优先考虑 315-ball x32，因为它常见于 x32 LPDDR5，封装尺寸 12.4 x 15 mm，
  ball pad/pitch 相对更友好；Micron 资料里 441-ball 是 14 x 14 mm、ball 更多、
  pitch 更密，未必对两颗 x32 更简单。来源：Micron LPDDR5 multi-package datasheet
  里列了 315-ball TFBGA 和 441-ball TFBGA 封装选项。

  但最终不能只按封装尺寸选，要让 FPGA FAE 给你确认。

  你可以这样问 FPGA 厂家/FAE：

  我们准备用 A5EC052A B32A，外接两颗 x32 LPDDR5，每颗作为一个独立 1ch x32 EMIF
  interface。

  请帮忙确认：

  1. Agilex 5 EMIF IP 是否支持该 topology：two independent LPDDR5 x32
  interfaces？
  2. 推荐使用哪些 IO96 banks？例如 2A + 2B 是否合适？
  3. 是否有经过验证的 LPDDR5 memory vendor/package/part number list？
  4. 对 Micron 315-ball 和 441-ball LPDDR5，哪种封装在 Agilex 5 上有验证记录或
  reference design？
  5. 请提供推荐 pin assignment / QSF / example design，或者确认我们按 EMIF User
  Guide 的 x32 Pin Placement + A5EC052A B32A pinout 生成的 pin assign 是否可用。
  6. 是否需要我们先提交 Quartus EMIF test-fit report、pin planner report、board
  stackup 和拓扑给你们 review？
  7. 对 LPDDR5 CA/CK/WCK T-line、DQ byte lane、RZQ、REFCLK、VDDQ/VDD2 电源和 SI/
  PI 有哪些必须遵守的 layout constraints？

  重点：FPGA 端 pin assign 由 Altera EMIF x32 pin placement 决定，不由 LPDDR5 封
  装直接决定。不同 LPDDR5 封装主要改变的是 memory 颗粒端 ball mapping 和 PCB
  escape/routing 难度。

  参考：

  - Altera A5EC052A pinout：https://docs.altera.com/v/u/resources/830445/pin-in
    formation-for-the-agilextm-5-a5ec052a-device-xlsx-format-alt.-format-pdf

  (https://docs.altera.com/v/u/resources/830445/pin-information-for-the-agilextm-5-a5ec052a-device-xlsx-format-alt.-format-pdf)
  - Altera LPDDR5 data width mapping：https://docs.altera.com/r/docs/817467/25.
    3.1/external-memory-interfaces-emif-ip-user-guide-agilextm-5-fpgas-and-socs
    /lpddr5-data-width-mapping

  (https://docs.altera.com/r/docs/817467/25.3.1/external-memory-interfaces-emif-ip-user-guide-agilextm-5-fpgas-and-socs/lpddr5-data-width-mapping)
  - Micron LPDDR5 package info：https://mm.digikey.com/Volume0/opasdata/d220001
    /medias/docus/8885/441b-315b-y31m-lpddr5-multi-pkg.pdf

  (https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8885/441b-315b-y31m-lpddr5-multi-pkg.pdf)

