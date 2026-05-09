<file path="Daily/raw/2026-05-09/1726-capture.md">
A38 LPDDR5 架构评审后决策：当前 two independent x32 + bank 2A/2B 架构继续作为主线，但 LPDDR5 原理图扩面暂停。当前状态标记为 schematic_connected, not_signoff, pending_quartus, pending_fae, pending_package_confirm。明天第一优先级改为 OrCAD 网络核对 + Quartus 最小 EMIF/Fitter 验证 + FAE review，不再把 126 网络已连接视为 sign-off。注意：超级 LLM 评审中“标准支持场景之一”只能作为待验证判断，不能当事实；若 8GB 容量不被接受，应寻找 2GB x32/16Gb x32 长生命周期料号或重评容量/位宽，而不是换更大密度。
</file>
<file path="Daily/raw/2026-05-09/5月9日_extracted/A5EC052A B32A lpddr5 pin assign.md">
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

</file>
<file path="Daily/raw/2026-05-09/5月9日_extracted/Issue4 A57 edp问题 今日新增.md">


Issue4 A57 edp问题有如下补充。你看下基于这些补充可以去做什么？首先是输入文件可以优化，然后输出可以重跑一次。
补充架构信息： edp1,2对应解码板上的一块ds90ub984解码芯片，edp3,4对应另一块ds90ub984解码芯片。
多解码板验证：
edp1,edp2,edp3,edp4都有概率出现问题。
一共测试了4块解码板，板间表现出差异。
有一块是3,4出图异常概率较高
另外三块是1,2出图异常概率较高。
对应同一解码芯片的edp1,2没有表现出严格的一致性，又出现一个好，一个不好的情况。edp3,4同样。

edp高速链路mainstream中间有个redriver，这个redriver在设备上电后就已经配置好，后续并未进行重新配置。

所做的重复测试，其重复方式是对解码芯片进行重新上下电和重新配置。


当前的计划：
### A57项目事项汇总

| 分类    | 事项                                           | 进度                                                                                                                   | 责任人    | 时间       |
| :---- | :------------------------------------------- | :------------------------------------------------------------------------------------------------------------------- | :----- | :------- |
| EDP出图 | edp上电时序测量-含serdes参考时钟                        |                                                                                                                      | 吴峰     | 2026/5/9 |
| EDP出图 | 前后2通道edp serdes电路差异确认;                       | 已确认无差异                                                                                                               |        |          |
| EDP出图 | redirver4通道上电pwdn信号及I2C/出图PWDN信号有没有问题【上电初始化】 |                                                                                                                      | 吴峰     | 2026/5/9 |
| EDP出图 | 1，多测试几块984解码板;【6块】                           | 2块板子多块板子测试，大多数是EDP3、4比EDP1、2上下电更容易出图，但有一块板子，EDP1、2比EDP3、4上下电更容易出图，其余3块有问题。<br><br>1、现象：单独勾选无法出图<br>2、目前没有一块可以稳定4通道出图 | 吴志安    |          |
| EDP出图 | 另外2块984解码板-确认一下出图情况及参数确认                     |                                                                                                                      | 陈斌     | 2026/5/9 |
| EDP出图 | 前2通道edp 解码芯片984-iic指令与后2通道edp iic指令对比        | 对比指令和ini/-参数下发没问题；完成                                                                                                 | 罗奇军、陈斌 |          |
| EDP出图 | 读edp解码芯片相关寄存器;-和模拟出图输出的寄存器需和厂家确认是否有          |                                                                                                                      | 陈斌     | 2026/5/9 |
| EDP出图 | 984解码芯片-关键管脚测量【稍后硬件确认】                       |                                                                                                                      | 陈斌、吴峰  | 2026/5/9 |

</file>
<file path="Daily/raw/2026-05-09/5月9日_extracted/LP5 网络数量统计.md">


**一共 126 个网络。**

## 1. 总体结论

| 项目 | 数量 |
|---|---:|
| LP5_U0 网络数量 | 63 |
| LP5_U1 网络数量 | 63 |
| **总计** | **126** |

## 2. 分类统计

| 分类 | U0 数量 | U1 数量 | 合计 |
|---|---:|---:|---:|
| DQ0 ~ DQ31 | 32 | 32 | 64 |
| DMI0 ~ DMI3 | 4 | 4 | 8 |
| RDQS0 ~ RDQS3，C/T | 8 | 8 | 16 |
| WCK0 / WCK1，C/T | 4 | 4 | 8 |
| CK，C/T | 2 | 2 | 4 |
| CS0 / CS1 | 2 | 2 | 4 |
| CA0 ~ CA6 | 7 | 7 | 14 |
| RESET_N | 1 | 1 | 2 |
| FPGA_RZQ | 1 | 1 | 2 |
| REFCLK_P / REFCLK_N | 2 | 2 | 4 |
| **合计** | **63** | **63** | **126** |

## 3. 说明

这里的统计口径是：

- 空白单元格不计入网络数量；
- `0` 只作为占位符，不计入网络数量；
- 只统计类似 `LP5_U0_DQ31`、`LP5_U1_CA0` 这种实际网络名。

因此：

```text
LP5_U0 = 63 个网络
LP5_U1 = 63 个网络
总计    = 126 个网络
</file>
<file path="Daily/raw/2026-05-09/5月9日_extracted/agilex5 lpddr5 pin assign.md">
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
</file>
<file path="Daily/raw/2026-05-09/5月9日_extracted/issue5 AU15P + winbond flash 用jtag+vivado方式无法固化问题.md">
KU3P + W25Q256JWEIQ 可固化
AU15P + W25Q256JWEIQ 不可固化
AU15P + W25Q128JWSIQ 不可固化
报错都是
There was one error message while Program Configuration Memory Device.

**Messages** [Labtools 27-3347] Flash Programming Unsuccessful: SPI flash sector at address 0x0000 is locked for erase/program.
</file>
<file path="Daily/raw/2026-05-09/5月9日_extracted/今日完成项.md">

A38+agilex5方案的 lpddr5 fpga端网络连接好了
A57域控 edp问题：
1、烧录和升级，注册了主板以及解码板。
2、解码芯片上电时序确认，电源，PWDN，I2C看起来没问题。但是MODE配置有问题，三个mode都是0V，说明软件那边没有进行处理。

</file>
