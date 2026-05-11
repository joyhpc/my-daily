# AI Historical Context - 2026-05-11

This file is generated from previous compiled outputs. It is context only, not today's raw evidence.

## Boundary

- Use this context to detect continuity, repeated blockers, and yesterday's intended boot path.
- Do not treat historical context as proof that something happened today.
- Today's raw evidence remains `_ai-feed.md`.

## Warnings

- Missing historical context: Daily/compiled/2026-05-10/_cyberlog.md
- Missing historical context: Daily/compiled/2026-05-10/_tomorrow-boot.md

## Sources

<context role="recent-tomorrow-boot" date="2026-05-08">
<file path="Daily/compiled/2026-05-08/_tomorrow-boot.md">
# Tomorrow Boot Packet - 2026-05-09

## 明日主线

- A38 / DF108 LPDDR5 决策闭环：同时推进供应商正式回复、项目容量接受、逻辑 Quartus/Fitter 验证；在这三项完成前不冻结 LPDDR5 pin list。
- A57 / AU15P 两个 P0 阻塞只做证据收敛：A57 先做多板复现和 PWDN 实测，AU15P 先补烧录失败证据。

## 背景

- A38 原需求是 2 颗 2GB / 16Gb x32 LPDDR5，总容量 4GB，主控侧约 3733 MT/s。
- 当前未找到满足 5-8 年生命周期的 2GB x32 LPDDR5 料号；美光明确主候选是 `MT62F1G32D2DS-020 WT:D`，4GB / 32Gb x32 LPDDR5X，9600 Mb/s per pin，315-ball TFBGA。
- 如果使用 4GB x32 颗粒，两颗组成 x64 后整板容量会从 4GB 上浮到 8GB。
- 三星 245FBGA 消费类 `K3KL8L80DM-TGCT` 不作为主推；但三星 315FBGA x32 32Gb LPDDR5X 正式渠道仍可并行确认，不能把两条路线混为一个结论。
- LPDDR5 pin assignment 需要看 Agilex 5 EMIF IP User Guide Chapter 9.2.3 / 9.2.4；`altera-pbc-b32a-a5e.xlsx` 只是 package ball coordinate，不是 LPDDR5 pin assignment。
- A57 984 解码板 eDP 后两通道异常目前只基于 1 块板；前 1、2 通道开关视频流 1000 次正常。
- AU15P 固件固化失败：0x0000 地址 locked，擦除和烧写不了；KU3P 同样步骤正常。

## 当前状态

- A38 美光主候选：可推进，但生命周期、温度等级、lead time、价格、MOQ/MPQ、降频使用建议未正式确认。
- A38 项目容量决策：未确认是否接受整板容量从 4GB 上浮到 8GB。
- A38 逻辑验证：未看到 Quartus EMIF / Pin Planner / Fitter 输出，pin list 不能冻结。
- A38 采购路线：南亚关闭；Henry 未见回复；三星消费类 245FBGA 不适合作主推；三星 315FBGA 正式渠道待确认。
- A57 Issue4：待反馈多板测试、IIC 指令对比、寄存器读值、上电时序、SerDes 差异、Redriver PWDN 实测电平。
- AU15P：只有失败现象，缺少工具、命令、错误码、protect/lock 状态和日志。

## 第一动作

- 先建一个 A38 LPDDR5 P0 决策表，列三行：
  - 供应商正式回复：owner 采购，输入美光/WT/WPI 问题清单，输出生命周期/温度/价格/lead time/MOQ/MPQ/降频建议。
  - 项目容量接受：owner 项目/罗奇军，输入 4GB -> 8GB 整板容量变化，输出是否接受及成本/软件/初始化/功耗影响。
  - 逻辑 Quartus 验证：owner 吴志安/逻辑侧，输入美光和三星各一个候选料号，输出 EMIF 配置、Pin Planner、Fitter、QSF / pin report。

完成这张表后，再处理 A57 和 AU15P，不要先进入 LPDDR5 原理图 pin 绘制。

## 注意事项

- 不要把“美光 4GB x32 可评估”写成“料号已冻结”。
- 不要把“供应商没找到 2GB x32”写成“项目已经接受 8GB 整板容量”。
- 不要把“三星 245FBGA 消费类不推进”扩大成“三星所有 LPDDR5X 都不推进”。
- 不要在没有 Quartus / Fitter 证据前冻结 LPDDR5 pin list。
- 不要把 A57 Issue4 的群内同步文案当成已发送事实，原文未明确已发送。
- AU15P 不要继续盲试烧录；先把 lock/protect 状态和错误日志补齐。

## 不要重复踩的坑

- 用 package ball coordinate 代替 pin assignment 规范。
- 把采购料号选择、项目容量决策、逻辑 Fitter 验证混成同一个“已确定”结论。
- 单板复现就判断为共性硬件问题。
- 对外文案不标 draft/sent/confirmed 状态。
- 烧录失败没有记录命令和错误码，只留下“烧不进去”。

## 可以交给 AI / agent 的部分

- 生成 A38 LPDDR5 P0 决策表和 owner/action/output 模板。
- 起草给美光/WT/WPI 的补充问题邮件。
- 起草给三星正式渠道的 315FBGA x32 LPDDR5X 询问清单，同时明确 245FBGA 消费类不是主推。
- 生成 A57 多板测试记录表、IIC 指令对比表、寄存器读值对比表。
- 生成 AU15P 固化失败最小记录表。
- 审核当天文案是否标记 draft/sent/waiting-feedback/confirmed。

## 必须由我亲自判断的部分

- 是否接受 A38 LPDDR5 整板容量从 4GB 上浮到 8GB。
- 美光主候选在成本、生命周期和降频使用上是否足以进入设计主线。
- 三星 315FBGA 料号是否值得作为并行候选继续投入时间。
- A57 多板测试结果是否足以把问题定义为共性问题。
- AU15P locked 地址问题是否需要切换工具、改保护配置、返查板级连接或找供应商支持。
</file>
</context>
<context role="recent-tomorrow-boot" date="2026-05-09">
<file path="Daily/compiled/2026-05-09/_tomorrow-boot.md">
# Tomorrow Boot Packet - 2026-05-10

## 明日主线

- A38 / Agilex 5 LPDDR5：当前 two independent x32 + bank 2A/2B 继续作为主线，但 LPDDR5 原理图扩面暂停；先做 OrCAD 网络核对，再补 Quartus / Fitter / FAE 验证闭环。
- A57 / 984 eDP：围绕 MODE 三个 0V 和多板概率性异常收敛证据，优先做矩阵，不要继续沿用“后两通道问题”的旧框架。
- AU15P / Winbond Flash：先读取和解除 Flash lock/protection 状态，再继续 Vivado Program Configuration Memory Device。

## 背景

- A38 LPDDR5 当前工作假设是 A5EC052A B32A + 两颗独立 x32 LPDDR5，U_LPDDR5_0 -> IO96 bank 2A，U_LPDDR5_1 -> IO96 bank 2B。
- 今日记录显示 A38 LPDDR5 FPGA 端网络已经连接完成，并统计出 U0 63 个、U1 63 个、总计 126 个网络。
- 当前 pin/net 表来源是 Altera A5EC052A pinout、Agilex 5 EMIF LPDDR5 pin placement / data width mapping，以及 Micron / Antmicro 315-ball 参考。它是工作输入，不是最终签核。
- 架构评审后的执行决策：当前架构可作为主线，但状态必须标为 `schematic_connected`, `not_signoff`, `pending_quartus`, `pending_fae`, `pending_package_confirm`；“标准支持场景之一”不能当事实写入设计结论，必须等 Quartus / FAE 证据。
- A57 新增架构信息：eDP1/2 对应一颗 DS90UB984，eDP3/4 对应另一颗 DS90UB984。
- A57 多板测试显示 eDP1/2/3/4 都有概率异常，板间表现不同，目前没有一块板稳定 4 通道出图。
- A57 已完成或初步完成的排查：前后通道 SerDes 电路无差异；IIC 指令和 ini / 参数下发对比无问题；电源、PWDN、I2C 看起来没问题。
- A57 新疑点：三个 MODE 都是 0V，记录中判断软件侧没有处理。
- AU15P + W25Q256JWEIQ 和 AU15P + W25Q128JWSIQ 都固化失败；KU3P + W25Q256JWEIQ 可固化；失败报错指向 `0x0000` sector locked。

## 当前状态

- A38 原理图网络：FPGA 端 LPDDR5 网络已连接，但扩面暂停；需要 ERC / netlist / 数量核对。
- A38 pin assign：状态是 `schematic_connected` + `not_signoff`，缺 Quartus EMIF / Pin Planner / Fitter 和 FAE review。
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
  - 每组标注状态：`schematic_connected`、`not_signoff`、`pending_quartus`、`pending_fae`、`pending_package_confirm`。

完成这张表后，直接启动 Quartus 最小 EMIF/Fitter 验证并准备 FAE review 包；不要直接继续扩展 LPDDR5 原理图范围。

## 注意事项

- 不要把 Table 22 的 Pin Index 当成 LPDDR5 颗粒 ball。
- 当前两颗 x32 LPDDR5 场景使用 x32 column；不要误用 2 Channel x16 column。
- `FPGA_RZQ` 是 FPGA OCT 电阻脚，不是 LPDDR5 颗粒 ZQ。
- `REFCLK_P/N` 接 EMIF PLL reference clock，不接内存颗粒。
- 不要把“FPGA 端网络连接好了”写成“LPDDR5 pin assign 已签核”。
- 不要把“two independent x32 是标准支持场景之一”写成已确认事实；当前只能写成待 Quartus / FAE 验证的主线方案。
- 如果 8GB 容量不被接受，方向是找 2GB x32 / 16Gb x32 长生命周期料号或重评容量/位宽，不是换更大密度。
- A57 MODE 三个 0V 是强疑点，但还不能直接写成最终根因。
- AU15P 不要继续重复烧录；先读保护状态。

## 不要重复踩的坑

- 用 AI 生成的 CSV 代替 Quartus / Fitter / FAE 证据。
- 原理图扩面快于验证闭环，把小的 test-fit 风险放大成 126 网络级返工。
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
- 是否接受 LPDDR5 原理图扩面暂停，直到 Quartus / FAE 证据到位。
- A57 MODE 三个 0V 是否由软件配置、硬件拉电阻、采样时机或 DS90UB984 模式设置导致。
- AU15P 是否需要切换 Vivado 流程、改约束、换配置器件识别方式，或找芯片/板级支持。
</file>
</context>
