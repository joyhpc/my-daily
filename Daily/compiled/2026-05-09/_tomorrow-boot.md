# Tomorrow Boot Packet - 2026-05-10

## 明日主线

- A38 / Agilex 5 LPDDR5：先核对已连接的 FPGA 端网络，再补 Quartus / FAE 验证路径；不要把 OrCAD 网络连好等同于 pin assign 签核。
- A57 / 984 eDP：围绕 MODE 三个 0V 和多板概率性异常收敛证据，优先做矩阵，不要继续沿用“后两通道问题”的旧框架。
- AU15P / Winbond Flash：先读取和解除 Flash lock/protection 状态，再继续 Vivado Program Configuration Memory Device。

## 背景

- A38 LPDDR5 当前工作假设是 A5EC052A B32A + 两颗独立 x32 LPDDR5，U_LPDDR5_0 -> IO96 bank 2A，U_LPDDR5_1 -> IO96 bank 2B。
- 今日记录显示 A38 LPDDR5 FPGA 端网络已经连接完成，并统计出 U0 63 个、U1 63 个、总计 126 个网络。
- 当前 pin/net 表来源是 Altera A5EC052A pinout、Agilex 5 EMIF LPDDR5 pin placement / data width mapping，以及 Micron / Antmicro 315-ball 参考。它是工作输入，不是最终签核。
- A57 新增架构信息：eDP1/2 对应一颗 DS90UB984，eDP3/4 对应另一颗 DS90UB984。
- A57 多板测试显示 eDP1/2/3/4 都有概率异常，板间表现不同，目前没有一块板稳定 4 通道出图。
- A57 已完成或初步完成的排查：前后通道 SerDes 电路无差异；IIC 指令和 ini / 参数下发对比无问题；电源、PWDN、I2C 看起来没问题。
- A57 新疑点：三个 MODE 都是 0V，记录中判断软件侧没有处理。
- AU15P + W25Q256JWEIQ 和 AU15P + W25Q128JWSIQ 都固化失败；KU3P + W25Q256JWEIQ 可固化；失败报错指向 `0x0000` sector locked。

## 当前状态

- A38 原理图网络：FPGA 端 LPDDR5 网络已连接，需要 ERC / netlist / 数量核对。
- A38 pin assign：仍是 `working_table` 状态，缺 Quartus EMIF / Pin Planner / Fitter 和 FAE review。
- A38 memory-side ball：如果最终 LPDDR5 料号或封装不是当前参考的 Micron 315-ball 类封装，需要重核 memory-side ball mapping。
- A57 问题框架：已经不是单纯后两通道异常，而是多板、多通道、概率性异常。
- A57 当前最明确的新疑点：MODE 三个 0V。
- AU15P：失败现象清楚，但还缺 Flash status/protection register、unlock/erase 过程和完整工具日志。

## 第一动作

- 先做 A38 LPDDR5 原理图核对表：
  - U0 网络数应为 63。
  - U1 网络数应为 63。
  - 总网络数应为 126。
  - 每组分类核对 DQ、DMI、RDQS、WCK、CK、CS、CA、RESET_N、FPGA_RZQ、REFCLK_P/N。
  - 每组标注状态：`schematic_connected`、`pending_quartus`、`pending_fae`、`pending_memory_package`。

完成这张表后，再切到 A57 MODE 和 AU15P lock，不要直接继续扩展 LPDDR5 原理图范围。

## 注意事项

- 不要把 Table 22 的 Pin Index 当成 LPDDR5 颗粒 ball。
- 当前两颗 x32 LPDDR5 场景使用 x32 column；不要误用 2 Channel x16 column。
- `FPGA_RZQ` 是 FPGA OCT 电阻脚，不是 LPDDR5 颗粒 ZQ。
- `REFCLK_P/N` 接 EMIF PLL reference clock，不接内存颗粒。
- 不要把“FPGA 端网络连接好了”写成“LPDDR5 pin assign 已签核”。
- A57 MODE 三个 0V 是强疑点，但还不能直接写成最终根因。
- AU15P 不要继续重复烧录；先读保护状态。

## 不要重复踩的坑

- 用 AI 生成的 CSV 代替 Quartus / Fitter / FAE 证据。
- 最终 LPDDR5 封装未定时，把参考 memory ballout 画成不可变事实。
- 用昨天的“后两通道异常”旧叙述覆盖今天的多板概率性事实。
- A57 测试表不区分已测 4 块、计划 6 块和待测 2 块。
- AU15P 只保存一句报错，不保存 status register 和 unlock 过程。

## 可以交给 AI / agent 的部分

- 生成 A38 LPDDR5 OrCAD 网络核对表。
- 生成发给 FPGA FAE 的 LPDDR5 topology / bank / package / QSF / Fitter review 问题清单。
- 把 A57 做成 6 板 x 4 eDP x 2 颗 984 x MODE / register / 出图状态矩阵。
- 生成 AU15P Flash lock 排查 checklist，包括 status register、BP/TB/CMP/SRP/WPS、unlock、erase、program 和日志字段。
- 审核 daily note 里哪些是 AI 生成建议、哪些是已完成事实。

## 必须由我亲自判断的部分

- A38 当前 bank 2A / 2B x32 方案是否继续作为原理图主线。
- 是否接受在 Quartus / FAE 证据前继续扩大 LPDDR5 原理图绘制范围。
- A57 MODE 三个 0V 是否由软件配置、硬件拉电阻、采样时机或 DS90UB984 模式设置导致。
- AU15P 是否需要切换 Vivado 流程、改约束、换配置器件识别方式，或找芯片/板级支持。
