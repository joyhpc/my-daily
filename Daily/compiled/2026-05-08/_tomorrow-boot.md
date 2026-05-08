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
