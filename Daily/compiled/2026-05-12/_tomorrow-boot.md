# Tomorrow Boot Packet - 2026-05-13

## 明日主线

- A57 eDP：围绕 AUX_EN 4.7K 上拉做证据闭环，先补齐测试元数据，再决定是否进入原理图/固件修改。
- A38 GPIO：把 205 个低速 GPIO 从数量评估推进到 bank/VDDIO 分配表，优先锁定 37 个 3.3V 控制类 GPIO 的 HVIO 位置。
- A38/A57 memory：收集 DDR4 / DDR5 / LPDDR4 / LPDDR5 器件侧候选回复，并保持“器件侧评估”和“主控兼容性验证”分离。

## 背景

- A57 eDP 当前最强实验结果：TX/RX 未改动，仅 AUX_EN 加 4.7K 上拉后，探头测试不出图未复现，RX 异常波形消失，50 多次循环、约 1 小时运行和重启测试均稳定。
- 该结果还不是最终根因签核：仍需确认 AUX_EN 上拉位置、实测 4.7K、双方 bit/bin/JTAG 内容、固件版本、AUX_EN 上电/配置/初始化默认电平，以及 AP 工具在不出图时是否必然报错。
- 直接用示波器表笔点测 AUX_RX / AUX_TX / AUX_EN 可能扰动 AUX 通信，明天不要继续把直接探测结果当作无扰动事实。
- A38 GPIO 当前总需求是 205 个，可统计资源约 256 个，理论余量约 51 个；`256 - 168 = 88` 只是解码板主体 GPIO 口径。
- 37 个 3.3V 低速控制 GPIO 应优先放 HVIO；168 个解码板主体 GPIO 可根据 1.2V / 1.8V 要求分配到 HSIO 与 HVIO。
- Memory 外部评估请求已经形成，但 raw 未明确发送状态；如果已经发出，需要补状态记录。

## 当前状态

- A57 eDP：方向从 AUX_RX/TX 转向 AUX_EN 默认状态/高阻风险；4.7K 上拉是当前有效实验变量。
- A38 GPIO：数量层面满足，VDDIO/bank/复用限制仍未闭环。
- A38/A57 memory：DDR4/DDR5/LPDDR4/LPDDR5 只是进入器件侧评估请求阶段，尚未冻结。
- 外部正式工作空间有 high-speed GPIO allocation URL，但今日 daily 没有读取该文档内容。

## 第一动作

- 先建 `A57_AUX_EN_4K7_Verification` 表，列：
  - 板号
  - AUX_EN 上拉位置
  - 实测电阻
  - bit / bin / JTAG 版本
  - 是否存在 bin1 升级差异
  - 是否直接探测 AUX
  - 循环次数
  - 运行时长
  - 重启次数
  - 是否出图
  - RX 异常波形是否存在
  - AP 工具是否报采集错误
  - 结论

填完这张表后，再决定是否把 AUX_EN 外部上拉写入原理图修改项，或先要求固件把 EN 初始化为确定电平。

## 注意事项

- 不要把 4.7K 上拉直接写成最终根因；当前只能写成最有效实验变量。
- 不要同时改 AUX_RX、AUX_TX 和 AUX_EN。
- 不要继续用直接点测 AUX 原始管脚的结果做无扰动判断。
- A38 GPIO 余量统一按 205 总需求口径写 51，不要再混用 88。
- HSIO Bank 3B 右 half 的 48 个资源仍是待确认项，不能直接全量使用。
- LPDDR4/LPDDR5 供应商回复必须写清 package width 和 die organization，不要只写 x32。
- Memory 沟通如果已经发送，必须补 `sent_to`、`sent_time`、`waiting_for`、`expected_output`。

## 不要重复踩的坑

- 把测量扰动当成真实电路状态。
- 现场 debug 只记录结果，不记录板号、固件、烧录方式和测试条件。
- 把 AUX_EN 上拉有效误写成 AUX_RX/TX 已经无风险。
- 把 GPIO 数量满足误写成 pin/bank/VDDIO 已经签核。
- 把供应商评估请求误写成供应商已回复。
- 把 daily 中的外部链接当成 daily 已经审核过的正式证据。

## 可以交给 AI / agent 的部分

- 生成 A57 AUX_EN 4.7K 验证表模板。
- 生成 A57 AUX_RX / AUX_TX / AUX_EN 非侵入式测量 checklist。
- 生成 A38 205 GPIO bank/VDDIO 分配表模板。
- 生成 DDR4 / DDR5 / LPDDR4 / LPDDR5 供应商回复对比表。
- 审核 memory 沟通文本是否具备明确 `draft/sent/waiting-feedback` 状态。

## 必须由我亲自判断的部分

- AUX_EN 4.7K 上拉是否进入正式原理图修改。
- AUX_EN 默认状态是否通过硬件上拉解决，还是优先要求固件初始化。
- 37 个 3.3V GPIO 的 HVIO 资源是否足够并符合整板 pinout。
- 是否接受某些解码板 GPIO 使用 1.2V/1.8V。
- DDR4 / DDR5 / LPDDR4 / LPDDR5 哪条路线继续作为架构主线。
- 是否需要回到正式工作空间审核 high-speed GPIO allocation 文档并同步口径。
