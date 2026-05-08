# AI Sync Request - 2026-05-08

## 使用说明

复制本文件全部内容，粘贴给 AI。

AI 输出后建议保存为：
- `Daily/compiled/2026-05-08/_cyberlog.md`
- `Daily/compiled/2026-05-08/_tomorrow-boot.md`
- `Daily/compiled/2026-05-08/_ai-output-audit.md`

请先审核 AI 输出，不要让 AI 覆盖任何非下划线开头的原始 notes。

## Codex / Agent 执行模式

如果你是 Codex、agent，或者任何可以读写此仓库文件的 AI，请默认完整处理，不要只返回文本答案：

1. 读取本 request 和同目录 `_ai-audit.md`。
2. 生成并保存 `Daily/compiled/2026-05-08/_cyberlog.md`。
3. 生成并保存 `Daily/compiled/2026-05-08/_tomorrow-boot.md`。
4. 生成并保存 `Daily/compiled/2026-05-08/_ai-output-audit.md`，说明是否发现误读草稿状态、混入被排除目录、把推断升级成事实等问题。
5. 不覆盖任何非 `_` 开头的原始 notes。

只有在没有文件写入能力时，才把结果完整输出到聊天窗口。

## Prompt

# Daily Cyberlog / 工作画布 AI Sync Prompt

你是我的 cyberlog 整理 agent 和工作流分析 agent。

下面是我今天 Obsidian Daily 文件夹里的所有 markdown 内容。
这些内容是原始草稿，可能混乱、重复、不完整。

你的任务不是做普通总结，而是从中提取我的工作状态、任务流、决策、阻塞、产出和自我迭代信号。

请严格区分：
- 明确事实
- 合理推断
- 建议
- 不确定信息

不要编造。找不到就写“未发现”。

在正式输出前，请先在内部完成一次信息清洗，但不要展开这部分过程：
1. 按项目聚类：例如 A38 / A57 / cyberlog-workflow / workspace-skills / wiki-sync / 其他。
2. 给每条信息标记类型：fact / draft / sent-message / ai-suggestion / decision / todo / blocked / closed。
3. `chatroom`、`未命名`、历史 AI 回答、方案建议类内容，默认只能作为 `ai-suggestion` 或 `合理推断`，不能直接当作事实；只有原文明确出现“已完成 / 已发送 / 已确认 / 等待反馈 / 实测 / 核实”等状态词时，才可升级为事实。
4. 同一文件里如果同时出现“未发送版本”和“最终发送版本”，必须分别标记，不能合并成一个已发送事实。
5. 如果一个任务跨多个项目出现，请优先归入最具体项目，不要重复计算推进。

请输出以下结构：

# FILE: _cyberlog.md

# Cyberlog — 2026-05-08

## 1. 今日真实推进

列出今天真正产生推进的事项，而不是所有活动。

## 2. 当前工作画布

### Active

当前正在推进的任务。

### Queue

排队但未真正开始的任务。

### Blocked

被阻塞的任务。每个阻塞需要说明：
- 阻塞原因
- 解除方式
- owner
- 下一步

### Closed

今天已经关闭或完成的事项。

## 3. 关键决策

用表格输出：

| 决策 | 背景 | 理由 | 风险 | 后续动作 | 来源文件 |
|---|---|---|---|---|---|

## 4. 重要信息

提取今天记录中值得保留的信息、链接、材料、观点或上下文。
不要把所有信息都搬运过来，只保留未来仍有用的信息。

## 5. 今日产出

列出今天产生的可复用产出，例如：
- 文档
- 代码
- prompt
- 模板
- 设计
- 判断
- 结论
- 决策资产

每个产出需要说明：
- 产出是什么
- 属于哪个项目
- 位置或来源
- 可复用价值

## 6. 未完成任务

只列出仍然需要行动的事项。
每个任务给出：
- 任务
- 所属项目
- 下一步动作
- 优先级：P0 / P1 / P2
- 是否适合交给 AI / agent
- 为什么

## 7. 明日启动包

输出明天早上可以直接使用的启动信息：

# FILE: _tomorrow-boot.md

# Tomorrow Boot Packet — 2026-05-09

## 明日主线
-

## 背景
-

## 当前状态
-

## 第一动作
-

## 注意事项
-

## 不要重复踩的坑
-

## 可以交给 AI / agent 的部分
-

## 必须由我亲自判断的部分
-

## 8. 工作流摩擦

分析今天工作流中出现的摩擦，例如：
- 目标不清
- 上下文切换
- 工具链问题
- 决策拖延
- 范围膨胀
- 信息分散
- 执行中断
- 任务入口不清
- 缺少完成标准

每个摩擦请说明：
- 现象
- 可能原因
- 对推进的影响
- 明天的修正动作

## 9. 自我迭代建议

只给 1-3 条最有价值的建议。
每条建议必须能转化为明天或本周的具体行为。
不要给泛泛建议。

## 10. 规则候选

提取今天应该沉淀进 personal operating manual 的规则。
格式：

### 规则候选 N
- 触发条件：
- 规则：
- 原因：
- 例子：
- 是否建议写入 System/workflow-rules.md：yes / no

输出要求：
- 不要编造事实。
- 不确定就标记为“不确定”。
- 尽量引用来源文件名。
- 原始内容里没有的信息不要假装存在。
- 严格保留 `# FILE: _cyberlog.md` 和 `# FILE: _tomorrow-boot.md` 两个分隔标题，方便拆分保存。
- 输出要适合直接复制到 _cyberlog.md 和 _tomorrow-boot.md。

## AI Feed

<file path="Daily/raw/2026-05-08/5月8日_extracted/Issue4.md">
 ## 【项目背景】

  - 项目：A57 项目
  - 板卡：984 解码板
  - 问题：eDP 后两通道存在出图异常，需要排查是否为单板问题、软件配置问题、硬件时序/电路问题，或 Redriver 相关使能/控制问题。
  - 对照现象：前 1、2 通道开关视频流测试 1000 次，未出现不出图问题。
  - 关键限制：当前后两通道异常判断仅基于 1 块单板测试结果，样本量不足，不能判断为普遍性问题。

  ## 【已确认事实】

  1. 09:03，吴志安反馈：1，2通道开关视频流测试1000次，没问题。
  2. 当前讨论对象是 A57 项目 eDP 后两通道出图异常。
  3. 当前涉及板卡为 984 解码板。
  4. 09:24，吴志安同步上午讨论形成 5 个排查项，并 @何鹏程、吴锋、Candy/罗奇军、陈斌。
  5. 初始 5 个排查项为：
      - 多测试几块 984 解码板，原始记录归类为软件侧。
      - 对比前 2 通道 eDP IIC 指令与后 2 通道 eDP IIC 指令，软件侧。
      - 读取 eDP 解码芯片相关寄存器，软件侧。
      - 测量 eDP 上电时序，硬件侧。
      - 确认前后 2 通道 eDP SerDes 电路差异，硬件侧。
  6. 09:25，邱永恒提醒：Redriver 芯片控制也需要对比分析。
  7. 09:25，Candy/罗奇军反馈：Redriver 芯片已经抓过波形，控制是一样的。
  8. 09:26，邱永恒在得知 Redriver 控制波形已分析后反馈：分析过就行。
  9. 09:37，Candy/罗奇军补充：Redriver 的 PWDN 可能也需要看一下，并 @何鹏程。
  10. Candy/罗奇军反馈手册信息：Redriver 的 PWDN 是拉低使能。
  11. Redriver PWDN 管脚实际板上电平状态，聊天记录中尚未确认。
  12. 11:07，吴锋提醒：以上结论基于测试 1 块板的结果，需要先多测试几块，确认是否所有板都是这个问题。
  13. 陈斌被纳入上午讨论同步对象，但原始记录中未明确分配具体任务。

  ## 【当前判断与疑点】

  判断

  14. 由于当前只有 1 块板的测试结果，不能判断该问题是普遍问题。
  15. 当前需要优先确认：后两通道异常是单板个体不良，还是多块 984 解码板共性问题。
  16. Redriver 控制波形前后通道一致，因此“Redriver 控制波形差异”目前不是已知差异点。

  疑点 / 待验证

  17. Redriver 控制波形一致，不能等价于排除 Redriver 相关问题，因为 PWDN 实际电平尚未确认。
  18. Redriver PWDN 是否已正确拉低使能，待实测。
  19. 前 2 通道与后 2 通道 eDP IIC 指令是否存在差异，待对比。
  20. eDP 解码芯片寄存器状态是否异常，待读取和对比。
  21. eDP 上电时序是否满足要求，待测量。
  22. 前后 2 通道 eDP SerDes 电路是否存在差异，待确认。
  23. 多块 984 解码板是否均复现后两通道异常，待测试。

  当前不能下结论的原因

  - 样本量只有 1 块板。
  - IIC 指令对比结果未反馈。
  - eDP 解码芯片寄存器读值未反馈。
  - eDP 上电时序实测结果未反馈。
  - 前后 2 通道 SerDes 电路差异未反馈。
  - Redriver PWDN 实测电平未反馈。

  ## 【排查方法与行动计划】

  | 分类 | 排查项 | 目的 | 当前状态 | 需要输出的结果 |
  |---|---|---|---|---|
  | 软件侧 | 多测试几块 984 解码板 | 扩大样本量，确认是否多板复现 | 待执行/待反馈 | 每块板测试结果、是否复现、复现通道、复现条件 |
  | 软件侧 | 对比前 2 通道与后 2 通道 eDP IIC 下发指令 | 确认初始化/配置是否存在差异 | 待执行/待反馈 | IIC 指令对比表，标记相同项和差异项 |
  | 软件侧 | 读取 eDP 解码芯片相关寄存器 | 确认芯片内部状态是否异常 | 待执行/待反馈 | 前后通道寄存器读值对比、异常位说明 |
  | 硬件侧 | 测量 eDP 上电时序 | 确认上电、复位、时钟、使能时序是否满足规格 | 待执行/待反馈 | 实测波形、时序参数、是否符合规格 |
  | 硬件侧 | 确认前后 2 通道 eDP SerDes 电路差异 | 检查原理图、器件、连接、供电、端接、走线差异 | 待执行/待反馈 | 电路差异清单；若无差异需明确说明 |
  | 硬件侧 | 测量 Redriver PWDN 管脚状态 | 确认 Redriver 是否被正确拉低使能 | 待测，@何鹏程 被关注 | PWDN 实测电平、测量时机、是否满足拉低使能 |

  ## 【责任人与关注项】

  - 吴志安：
      - 09:03 反馈 1、2 通道开关视频流测试 1000 次正常。
      - 09:24 同步上午讨论形成的 5 个排查项。
  - 吴锋：
      - 11:07 提醒当前结论仅基于 1 块板。
      - 建议先多测试几块板，确认是否所有板都有该问题。
  - 邱永恒：
      - 09:25 提醒关注 Redriver 芯片控制对比分析。
      - 09:26 在得知 Redriver 控制波形已分析后反馈“分析过就行”。
  - Candy / 罗奇军：
      - 09:25 反馈 Redriver 芯片控制波形已抓过，前后控制一样。
      - 09:37 补充 Redriver PWDN 需要检查。
      - 反馈手册显示 Redriver PWDN 为拉低使能。
  - 何鹏程：
      - 被 @ 关注 Redriver PWDN 测量项。
      - 需要确认 Redriver PWDN 管脚实际状态。
  - 陈斌：
      - 被纳入上午讨论同步对象。
      - 原始记录中未明确分配具体任务。

  ## 【待反馈结果清单】

  1. 多块 984 解码板测试结果。
  2. 前 2 通道与后 2 通道 eDP IIC 指令对比结果。
  3. eDP 解码芯片相关寄存器读取结果。
  4. eDP 上电时序测量结果。
  5. 前后 2 通道 eDP SerDes 电路差异确认结果。
  6. Redriver PWDN 管脚实测电平结果。

  ## 【适合发群里的同步版本】

  各位，A57 项目 984 解码板 eDP 后两通道出图异常目前信息整理如下：

  已确认事实：

  1. 吴志安 09:03 反馈：前 1、2 通道开关视频流测试 1000 次，未出现问题。
  2. 当前后两通道异常判断仅基于 1 块板测试结果，吴锋 11:07 已提醒需要多测几块板，确认是否为共性问题。
  3. 上午讨论形成 5 个初始排查项：多板测试、前后通道 IIC 指令对比、读取 eDP 解码芯片寄存器、测量 eDP 上电时序、确认前后 2 通道 SerDes 电路差异。
  4. 邱永恒提醒关注 Redriver 控制对比；Candy/罗奇军反馈 Redriver 控制波形已抓过，前后控制一样。
  5. Candy/罗奇军补充 Redriver PWDN 需要检查，手册显示 PWDN 为拉低使能；实际板上 PWDN 电平目前待确认，@何鹏程 关注该项。

  当前判断/疑点：

  6. 目前不能判断该问题是普遍问题，原因是样本量只有 1 块板。
  7. Redriver 控制波形一致，目前不是已知差异点，但不能排除 Redriver 相关问题，因为 PWDN 实际电平还未确认。
  8. 后 2 通道与前 2 通道差异仍需从 IIC 指令、寄存器状态、上电时序、SerDes 电路差异、Redriver PWDN、多板复现情况继续确认。

  行动计划 / 待反馈：

  9. 软件侧：多测试几块 984 解码板，输出每块板是否复现、复现通道和复现条件。
  10. 软件侧：对比前 2 通道与后 2 通道 eDP IIC 指令，输出差异表。
  11. 软件侧：读取 eDP 解码芯片相关寄存器，输出前后通道读值对比和异常位说明。
  12. 硬件侧：测量 eDP 上电时序，输出实测波形和是否满足规格。
  13. 硬件侧：确认前后 2 通道 eDP SerDes 电路差异，输出差异清单。
  14. 硬件侧：实测 Redriver PWDN 电平，确认是否满足拉低使能要求。


用你内部工具跑一遍，注意不要受到解析内容中的主观部分的过度影响，始终保持自己的判断能力。

远端有agent进行了更新，你同步到本地。
</file>
<file path="Daily/raw/2026-05-08/5月8日_extracted/LPDDR5 PIN ASSIGN.md">
LPDDR5 pin assign / pin placement 规范在这个文件：

  External Memory Interfaces (EMIF) IP User Guide Agilex™ 5 FPGAs and SoCs 817467_D842785.pdf
  (https://drive.google.com/file/d/1xbcT4cdCmZ0dgqwX9zzrEvWQ5DXGSVPA/view)

  重点位置：

  - Chapter 9. Agilex 5 FPGA EMIF IP - LPDDR5 Support
  - 9.2.3 Pin Guidelines for Agilex 5 FPGA EMIF IP，PDF 第 237 页左右
  - 9.2.4 Pin Placements for Agilex 5 FPGA LPDDR5 EMIF IP，PDF 第 240 页左右
  - 9.2.4.1 Address and Command Pin Placement for LPDDR5
  - 9.2.4.2 LPDDR5 Data Width Mapping
  - 9.2.4.3 LPDDR5 Byte Lane Swapping

  官方在线版本也在这里：

  - LPDDR5 Support 目录

  (https://docs.altera.com/r/docs/817467/25.3.1/external-memory-interfaces-emif-ip-user-guide-agilextm-5-fpgas-and-socs/agilextm-5-fpga-emif-ip-lpddr5-support)
  - Address and Command Pin Placement for LPDDR5

  (https://docs.altera.com/r/docs/817467/25.3.1/external-memory-interfaces-emif-ip-user-guide-agilextm-5-fpgas-and-socs/address-and-command-pin-placement-for-lpddr5?contentId=aMXZgx5RXexgoj~e2joi7A)
  - LPDDR5 Data Width Mapping

  (https://docs.altera.com/r/docs/817467/25.3.1/external-memory-interfaces-emif-ip-user-guide-agilextm-5-fpgas-and-socs/lpddr5-data-width-mapping?contentId=kZhHwBujCfglRh7hbL_OyA)

  我也核了一下：文件夹里的 altera-pbc-b32a-a5e.xlsx 只是 package ball coordinate，不是 LPDDR5 pin assignment；开发板 schematic/user guide 主要是 LPDDR4，不
  是你要的 LPDDR5 规范。

</file>
<file path="Daily/raw/2026-05-08/5月8日_extracted/lpddr5 情况群内反馈 2.md">
各位，同步一下目前 LPDDR5/5X 采购寻样与方案评估的进展：

**背景与现状**

为满足当前 128Gbps 的数据量需求，我们需要寻找 LPDDR5/5X 方案。原计划找 2GB x32 颗粒（总容量 4GB），但市面上该规格多有 EOL 风险，难以满足项目 5-8 年长期供货要求。

目前明确且长生命周期的候选，基本都是 **4GB (32Gb) x32** 起步。

**核心备选料号（需评估降频使用）**

- **美光：** MT62F1G32D2DS-020 WT:D (32Gb, x32, 315-TFBGA)
    
- **三星：** K3KL8L80QM-MFCT / K3KL8L80CM-MGCT 等 (32Gb, x32, 315 FBGA)
    

**下一步 Action Items：**

1. **@采购** 请继续并行跟进美光和三星的上述 32Gb 料号。重点确认：**5-8年生命周期（是否有明确的 EOL 风险/PCN 通知周期）**、单价、交期及 MOQ。三星不要仅因“偏消费级”就排除，需通过正式渠道核实其工业级/长期供货能力。
    
2. **@项目 / @罗奇军** 容量变更确认：如果采用上述方案，整板总容量将从 4GB 上浮至 **8GB**（2颗 4GB x32 组成 x64）。请确认是否接受容量上浮（需评估成本、软件地址空间、启动初始化等影响）。
    
3. **@吴志安** 请协助选定美光和三星各一个候选料号，进行 Quartus EMIF / Pin Planner / Fitter 验证。重点确认：Agilex 5 是否支持该器件配置、Bank/Pin 分配能否收敛、目标速率时序是否可实现。
    
4. **硬件侧（我这边）** 在志安完成 FPGA 验证前，暂时**不冻结** LPDDR5 的 pin list，等确认可行后，再进入原理图与 PCB SI 约束冻结，避免返工。
    

大家看下有没有问题，没有的话咱们先按这个方向并行推进。
</file>
<file path="Daily/raw/2026-05-08/5月8日_extracted/lpddr5 情况群内反馈.md">
 各位同步一下 LPDDR5 / LPDDR5X 采购寻样与方案评估进展。

  一、原 DF108 DDR4 方案回顾

  之前 DF108 最大线速支持 2.5Gbps/lane，摄像头端最大数据量约 80Gbps。

  原方案使用 4 颗 16bit DDR4：H5AN4G6NBJR
  - 颗粒配置：4Gb / x16 × 4
  - 总位宽：64bit
  - 总容量：2GB
  - 理论峰值带宽：约 153.6Gbps

  二、当前 Altera / Agilex 方案需求

  当前方案最大线速提升到 4Gbps/lane，摄像头端最大数据量约 128Gbps。

  原计划使用：
  - 2 颗 LPDDR5
  - 单颗规格：2GB / 16Gb，x32
  - 总位宽：64bit
  - 总容量：4GB
  - 按主控侧约 3733MT/s 计算，理论峰值带宽约 239Gbps

  该带宽相对 128Gbps 摄像头端输入有一定余量。

  三、采购寻样反馈

  原始寻样需求是：
  - 单颗 2GB / 16Gb
  - x32 位宽
  - LPDDR5 或 LPDDR5X
  - 商业级即可
  - 希望未来 5–8 年无 EOL 风险

  目前供应商反馈来看，暂时还没有找到完全匹配 2GB x32 且长期供货稳定的料号。

  1. 美光
  - 旧款 2GB x32 相关料号存在 EOL / 停产风险，不适合作为长期项目方案。
  - 目前比较明确、可继续评估的候选料号是：
    MT62F1G32D2DS-020 WT:D
  - 规格大致为：
    LPDDR5X，单颗 4GB / 32Gb，x32，9600Mbps/pin，315-ball TFBGA。
  - 该料号容量高于原始需求，速率也高于当前主控侧计划使用速率，需要按降频使用评估。

  2. 三星
  - 之前代理反馈的 245-ball LP5X 更偏消费类，生命周期通常 2–3 年，不能直接满足 5–8 年长期供货要求。
  - 但三星路线不建议完全排除。LPDDR5/LPDDR5X 本身很多料号都是移动端/消费类供货模式，不管哪个品牌都需要单独确认生命周期和 PCN/EOL 机制，不能只因为“消费级”就
  排除三星。
  - 公开资料里能看到三星也有 32Gb / x32 / 315 FBGA 的 LPDDR5X 料号，例如：
    K3KL8L80QM-MFCT：32Gb，x32，315 FBGA，7500Mbps，-40~95°C，量产状态
    K3KL8L80CM-MGCT：32Gb，x32，315 FBGA，7500Mbps，-25~85°C，量产状态
  - 所以建议采购继续找三星正式渠道或其他代理确认 315FBGA、x32、32Gb 这类料号的供货、价格、生命周期和样品情况。三星可以作为并行优先候选，而不是直接关闭。

  3. 南亚
  - 反馈目前没有 LPDDR5 可供选择。

  4. 海力士
  - 当前代理未有效响应，暂时没有可用反馈。
  - 建议继续找其他海力士渠道确认是否有 32Gb / x32 / LPDDR5X / 315FBGA 或类似规格可供。

  四、市场替代料初筛

  目前可以并行询价/确认的方向如下：

  A. 三星优先候选
  - K3KL8L80QM-MFCT
    32Gb / x32 / LPDDR5X / 315 FBGA / 7500Mbps / -40~95°C / 量产
  - K3KL8L80CM-MGCT
    32Gb / x32 / LPDDR5X / 315 FBGA / 7500Mbps / -25~85°C / 量产
  - K3KL8L80DM-MFCU
    32Gb / x32 / LPDDR5X / 315 FBGA / 8533Mbps / -40~95°C / 样品
  - K3KL8L80EM-MHCV
    32Gb / x32 / LPDDR5X / 315 FBGA / 9600Mbps / -40~105°C / 样品

  B. 美光候选
  - MT62F1G32D2DS-020 WT:D
    32Gb / x32 / LPDDR5X / 315-ball TFBGA / 9600Mbps/pin
  - 美光这条资料最明确，但容量同样是 4GB 起步，需要确认成本和生命周期。

  五、当前主要风险点

  1. 容量高于实际需求，价格可能更贵
  原计划是 2 颗 2GB x32，总容量 4GB。
  如果改用 32Gb / 4GB x32 颗粒，则 2 颗组成 x64 后整板 LPDDR 容量变为 8GB。
  项目侧需要确认是否接受容量从 4GB 上浮到 8GB。

  2. 速率匹配风险
  美光候选是 9600Mbps/pin，三星候选有 7500 / 8533 / 9600Mbps 等不同档位。
  当前主控侧计划约 3733MT/s，需要确认这些高速料号是否可以稳定降频使用。

  3. 封装与布局风险
  优先考虑 315 FBGA / 315-ball TFBGA 这类更接近 FPGA 高速存储应用的封装。
  需要进一步确认：
  - Agilex 5 EMIF 是否支持该器件配置
  - Bank / pin / byte lane 分配是否可行
  - PCB 扇出、层数、阻抗、等长约束是否可接受

  4. 生命周期风险
  本项目希望 5–8 年供货稳定，所以无论美光、三星还是海力士，都必须让供应商明确提供：
  - 生命周期 / Longevity
  - EOL 风险
  - PCN/EOL 通知周期
  - 样品交期
  - 量产交期
  - MOQ / MPQ
  - 价格阶梯

  六、建议下一步动作

  1. 采购侧
  请继续并行确认美光和三星：
  - 美光：MT62F1G32D2DS-020 WT:D
  - 三星：优先问 K3KL8L80QM-MFCT / K3KL8L80CM-MGCT，以及是否有更适合长期供货的 32Gb x32 315FBGA LPDDR5X 料号

  重点确认：
  - 生命周期 / Longevity
  - 是否有明确 EOL 风险
  - 商业级或工业级温度等级
  - 单价
  - 样品交期
  - 量产交期
  - MOQ / MPQ
  - 是否有长期供货承诺或 PCN/EOL 通知周期

  2. 项目侧
  需要确认是否接受容量调整：
  - 原计划：2 颗 2GB x32，总容量 4GB
  - 当前主流候选：2 颗 4GB x32，总容量 8GB

  如果容量上浮对成本、软件地址空间、启动初始化、功耗没有明显负面影响，可以把 32Gb / x32 LPDDR5X 作为当前主方向继续评估。

  3. 逻辑 / FPGA 侧
  建议先选 1 个美光候选和 1 个三星候选，做 Quartus EMIF / Pin Planner / Fitter 验证：
  - 美光：MT62F1G32D2DS-020 WT:D
  - 三星：优先 K3KL8L80QM-MFCT 或 K3KL8L80CM-MGCT

  重点确认：
  - Agilex 5 是否支持该 LPDDR5X 器件配置
  - x32 × 2 组成 x64 是否可行
  - Bank 资源是否足够
  - Pin 分配是否能收敛
  - Fitter 是否能通过
  - 目标速率下时序是否有可实现性

  4. 硬件侧
  在 Quartus EMIF / Pin Planner / Fitter 验证完成前，建议暂时不要冻结 LPDDR5 pin list。
  LPDDR5/LPDDR5X 的 pin 分配会直接影响 Bank 选择、字节组、走线拓扑、扇出和 SI 约束，建议等 FPGA 侧初步验证通过后，再进入原理图与 PCB 约束冻结。

  公开资料我查到的三星备选主要来自三星半导体官网：K3KL8L80QM-MFCT 是 32Gb、x32、315 FBGA、7500Mbps、-40~95°C、量产；K3KL8L80CM-MGCT 是 32Gb、x32、315
  FBGA、7500Mbps、-25~85°C、量产；K3KL8L80EM-MHCV 是 32Gb、x32、315 FBGA、9600Mbps、-40~105°C、样品；K3KL8L80DM-MFCU 是 32Gb、x32、315 FBGA、
  8533Mbps、-40~95°C、样品。Micron 公共渠道也能看到同系列 32Gbit x32 315-TFBGA 料号，但库存/价格状态需要采购再确认。来源：三星官网 K3KL8L80QM-MFCT、
  K3KL8L80CM-MGCT、K3KL8L80EM-MHCV、K3KL8L80DM-MFCU 页面，以及 DigiKey 的 Micron MT62F1G32D2DS-020 AUT:F 页面。


</file>
<file path="Daily/raw/2026-05-08/5月8日_extracted/lpddr5_report_decision.md">
# A38 / DF108 LPDDR5 采购寻样内部决策报告

日期：2026-05-08
范围：Gmail 转发邮件，时间窗口 2026-05-07 至 2026-05-08
项目：A38 / DF108 Agilex 5
用途：内部项目决策、采购下一步动作、硬件/逻辑侧可行性输入

## 1. 结论摘要

本轮邮件没有找到完全匹配原始需求的料号：`单颗 2GB / 16Gb、x32、LPDDR5、商业级、未来 5-8 年无 EOL`。

当前唯一可继续推进的主候选是美光 LPDDR5X：

| 项目 | 内容 |
| --- | --- |
| 推荐料号 | `MT62F1G32D2DS-020 WT:D` |
| 厂商 | Micron / 美光 |
| 类型 | LPDDR5X，兼容 LPDDR5/LPDDR5X data interface |
| 容量 | 4GB / 32Gb |
| 位宽 | x32 |
| 速率 | 9600 Mb/s per pin |
| 封装 | 315-ball TFBGA，package code DS |
| 当前判断 | 可作为 primary candidate，但不是原始 2GB 方案 |

建议决策：接受“4GB x32 LPDDR5X 降频使用”作为主线评估方向，同时把“2GB x32 长生命周期 LPDDR5”标记为供应链高风险或当前不可满足。

## 2. 原始需求基线

采购寻样的原始需求如下：

| 需求项 | 原始要求 |
| --- | --- |
| 核心规格 | LPDDR5，Standard BGA Package |
| 位宽 | 单颗 x32 |
| 容量 | 单颗 2GB / 16Gb |
| 主控支持上限 | 3733 MT/s |
| 寻源建议 | 市面主流 5500 MT/s 或 6400 MT/s 料号，硬件设计降频使用 |
| 温度等级 | 商业级即可 |
| 生命周期 | 未来 5-8 年无 EOL 风险 |
| 目标品牌 | 美光、三星、海力士等一线大厂 |

本轮供应商反馈暴露出的核心矛盾是：主流一线厂商 x32 LPDDR5/LPDDR5X 已经向更高容量、更高速率产品迁移，2GB / 16Gb x32 长生命周期料号不可得或存在 EOL 风险。

## 3. 供应商反馈结论

### 3.1 美光路线

来源邮件：

- `19e065cdbd67077e`：Kun Cao / WT Microelectronics，2026-05-08 08:59
- `19e065df94f3cfec`：Vince Huo / WPI，2026-05-07 17:13

关键事实：

- 美光 x32 LPDDR5/LPDDR5X 当前从 4GB 起步。
- 推荐 4GB LPDDR5X Y62P：`MT62F1G32D2DS-020 WT:D`。
- 美光后续主推 9600 MT/s 产品。
- 原 8533 速率型号将停产；7500 以下已停产。
- 供应商要求补充：终端客户、项目名称、应用、试产时间、量产时间、主芯片、年用量、每片用几颗。

判断：

- 美光是唯一给出明确候选料号和 datasheet/PCN 资料的路线。
- 但推荐料号容量为 4GB，不满足原始 2GB 要求。
- 由于旧代 2GB x32 料号存在 EOL 信息，强行坚持 2GB 会显著增加供应风险。

### 3.2 三星路线

来源邮件：

- `19e065c771a63d06`：Link Liu / Golden Supreme，2026-05-08 14:18

关键事实：

- 三星渠道明确反馈：目前出货 LP5X 产品从容量和生命周期看都没有能匹配需求的产品。
- 提到的最小容量产品为消费类 245ball，预计 2026 年 5 月底或 6 月中出样品。
- 附件料号：`K3KL8L80DM-TGCT`。
- Datasheet 字段：32Gb / x32 / 245FBGA / 7500 Mbps / Tc -25 to 85 C。
- 供应商明确说明消费类生命周期通常 2-3 年。

判断：

- 不适合作为 A38 当前主推料号。
- 可保留为备选调研项，但不满足 5-8 年生命周期要求。

### 3.3 南亚路线

来源邮件：

- `19e065d03c1d5052`：Fifi Lin / WT Microelectronics，2026-05-07 23:56

关键事实：

- Nanya 没有 LPDDR5。

判断：

- 关闭南亚路线。

### 3.4 Henry / HSRP 路线

来源邮件：

- `19e065c87163f67f`：采购在 2026-05-08 10:10 发出需求。

关键事实：

- 当前 Gmail 搜索范围内只看到发出的寻样需求，没有看到 Henry 回复。

判断：

- 采购可催一次，但不能把 Henry 路线计入当前可用候选。

## 4. 候选方案对比

| 方案                    | 料号/来源                    | 匹配度    | 优点                               | 主要问题                                         | 建议              |
| --------------------- | ------------------------ | ------ | -------------------------------- | -------------------------------------------- | --------------- |
| A. 美光 4GB x32 LPDDR5X | `MT62F1G32D2DS-020 WT:D` | 部分匹配   | 一线厂商；x32；资料明确；主推 9600 MT/s，可降频评估 | 容量从 2GB 上浮到 4GB；生命周期、温度等级、价格、lead time 待正式确认 | 主线推进            |
| B. 继续坚持 2GB x32       | 旧代美光或其他待寻源               | 当前不可确认 | 满足原始容量目标                         | 美光旧代 2GB x32 存在 EOL/停产风险；暂无一线厂商推荐            | 标记高风险，不建议作为唯一方案 |
| C. 三星 245FBGA 消费类     | `K3KL8L80DM-TGCT`        | 不推荐    | x32，32Gb，7500 Mbps               | 消费类；生命周期 2-3 年；样品未稳定；封装 245FBGA；供应商已说明不匹配    | 不作为主推           |
| D. 南亚                 | 无                        | 不匹配    | 无                                | 没有 LPDDR5                                    | 关闭              |

## 5. 关键风险

### 5.1 容量上浮风险

美光可推进方案是 4GB，而原始需求是 2GB。

影响：

- 单板内存容量翻倍，可能影响 BOM 成本。
- 初始化参数、地址映射、软件/逻辑配置可能需要调整。
- 如果系统原本只需要 2GB，额外容量是成本换供应安全。

需要确认：

- 系统是否接受单颗 4GB。
- 每板 2 颗 x32 规划下，总容量是否仍在系统和 BOM 可接受范围内。

### 5.2 LPDDR5X 降频使用风险

候选料号是 LPDDR5X 9600 Mb/s per pin，主控端当前按 3733 MT/s 上限评估。

影响：

- 理论上高速料号可低速运行，但仍需供应商确认长期降频使用建议。
- Agilex 5 EMIF 配置、training、ODT、SI 约束不能靠采购邮件冻结。

需要确认：

- 供应商确认是否适合 3733 MT/s 降频运行。
- 逻辑侧用 Quartus EMIF / Pin Planner / Fitter 验证。

### 5.3 生命周期风险

原始要求是未来 5-8 年无 EOL 风险。

已知风险：

- 美光 PCN 显示 Y52P specific 315b packages EOL：Published 2026-02-04，Last Order Date 2026-08-04，Last Ship Date 2027-02-04。
- 邮件正文引用 Y52Q 315b x32 2GB SDP 等 EOL：Published 2026-04-22，Last Order Date 2026-10-23，Last Ship Date 2028-12-31。
- 三星渠道明确说明消费类生命周期通常 2-3 年。

需要确认：

- `MT62F1G32D2DS-020 WT:D` 是否属于美光长期主推 Y62P 路线。
- 是否有正式生命周期承诺或 PCN 风险说明。

### 5.4 封装和 pinout 风险

LPDDR5/LPDDR5X 连接不能只按料号采购决定。

需要确认：

- 315-ball TFBGA DS 封装尺寸和原理图库。
- byte lane、CA、CK、CS、DMI、DQ、DQS、RESET、RZQ、VREF/供电 rail。
- 与 Agilex 5 EMIF bank/pin 规划、MIPI/QSFP 共存资源是否冲突。

## 6. 推荐决策

建议做如下内部决策：

1. 采购侧继续以美光 `MT62F1G32D2DS-020 WT:D` 为主线寻样和确认。
2. 硬件侧接受“容量上浮到 4GB”的评估输入，但在正式冻结前保留成本和系统确认项。
3. 逻辑侧尽快将该料号作为 LPDDR5/LPDDR5X x32 候选参数进入 Quartus EMIF / Pin Planner / Fitter 验证。
4. 三星路线暂不推进，除非后续给出长期生命周期料号。
5. 南亚路线关闭。
6. Henry 路线由采购催一次，作为补充渠道，不影响美光主线推进。

## 7. 下一步行动清单

| Owner | 动作                                                  | 输出物                                     | 优先级 |
| ----- | --------------------------------------------------- | --------------------------------------- | --- |
| 采购    | 向美光/WT 补充项目信息并询问生命周期、价格、sample/MP lead time、MOQ/MPQ | 供应商正式回复                                 | P0  |
| 硬件    | 评估 4GB x32 方案对 BOM、封装、原理图页、电源 rail、板级空间的影响          | 硬件可接受性结论                                | P0  |
| 逻辑    | 用 `MT62F1G32D2DS-020 WT:D` 方向建最小 Quartus EMIF 验证    | Fitter / Pin Planner / QSF / pin report | P0  |
| 项目负责人 | 决定是否接受容量从 2GB 上浮到 4GB                               | 需求变更确认                                  | P0  |
| 采购    | 催 Henry / HSRP 是否有 2GB x32 长生命周期料号                  | 补充渠道反馈                                  | P1  |

## 8. 附件和证据

当前工作目录附件：

- `attachments/PCN 36290.pdf`
- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x_19e065df94f3cfec.pdf`
- `attachments/315b-441b-561b-y6cp-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- `attachments/[Datasheet]LP5X_32Gb_D_245F_8.2x12.4_K3KL8L80DM-TGCT_Rev0.0.pdf`

关联整理文件：

- `lpddr5_supplier_matrix.csv`
- `lpddr5_reply_drafts.md`
- `lpddr5_mail_summary.md`

</file>
<file path="Daily/raw/2026-05-08/5月8日_extracted/lpddr5_report_engineering_evidence.md">
# A38 / DF108 LPDDR5 采购寻样工程证据报告

日期：2026-05-08
报告类型：工程证据版
用途：设计评审、原理图选型依据、Quartus EMIF / Pin Planner 输入、风险归档

## 1. 证据范围和方法

本报告基于以下本地工作空间证据整理：

- Gmail 只读搜索范围：`purehpc@gmail.com`
- 时间窗口：2026-05-07 至 2026-05-08
- 搜索语句：`in:anywhere after:2026/05/06 before:2026/05/09`
- 关键词：`LPDDR5 / LPDDR / 采购 / 寻样 / 存储颗粒 / Micron / Samsung / Hynix / 美光 / 三星 / 南亚 / Henry`
- 原始需求文件：`LPddr5需求 to 采购工程师 沟通.md`
- 附件目录：`attachments/`

本报告只做技术和供应链证据整理，不代表料号已冻结。LPDDR5/LPDDR5X 最终 pin list、bank 分配和时序配置必须以 Quartus EMIF / Pin Planner / Fitter 结果为准。

## 2. 需求追踪矩阵

| 需求项     | 原始需求                          | 当前证据状态                                                             | 工程判断                            |
| ------- | ----------------------------- | ------------------------------------------------------------------ | ------------------------------- |
| DRAM 类型 | LPDDR5                        | 美光和三星反馈均为 LPDDR5X 路线；美光 datasheet 标注 LPDDR5X/LPDDR5 data interface | 可以评估 LPDDR5X 降频/兼容使用，但需 EMIF 验证 |
| 位宽      | 单颗 x32                        | 美光 `MT62F1G32D2DS-020 WT:D` 为 x32；三星 `K3KL8L80DM-TGCT` 为 x32       | x32 可满足                         |
| 容量      | 2GB / 16Gb                    | 美光 x32 从 4GB 起步；三星附件为 32Gb / 4GB                                   | 原 2GB 不满足；需需求变更或继续寻源            |
| 速率      | 主控 3733 MT/s；优先 5500/6400 可降频 | 美光候选为 9600 Mb/s per pin；三星候选为 7500 Mbps                            | 可降频假设需供应商和 Quartus 双重确认         |
| 温度等级    | 商业级                           | 三星 datasheet 显示 Tc -25 to 85 C；美光 `WT:D` 温度/等级待正式确认                | 美光温度等级是 P0 待确认项                 |
| 生命周期    | 5-8 年无 EOL                    | 美光旧 2GB 相关料号有 EOL/停产风险；三星渠道称消费类 2-3 年                              | 2GB 路线风险高；美光 Y62P 4GB 需正式生命周期确认 |
| 封装      | Standard BGA                  | 美光 315-ball TFBGA DS；三星 245FBGA 8.2x12.4                           | 原理图库、封装、pinout 需重新评估            |

## 3. 邮件证据索引

| Gmail Message ID | 时间 | 来源 | 主题 | 证据价值 |
| --- | --- | --- | --- | --- |
| `19e065df94f3cfec` | 2026-05-08 14:53:57 +0800 | 何鹏程转发，原始来源 Vince Huo / WPI | 转发：回复: LPDDR5 存储颗粒选型需求 | 美光 PCN / 主推 9600 MT/s 产品 / 多容量候选 |
| `19e065cdbd67077e` | 2026-05-08 14:53:09 +0800 | 何鹏程转发，原始来源 Kun Cao / WT Microelectronics | 转发：回复: LPDDR5 存储颗粒选型需求 | 美光 4GB x32 推荐料号和项目资料需求 |
| `19e065d03c1d5052` | 2026-05-08 14:53:28 +0800 | 何鹏程转发，原始来源 Fifi Lin / WT Microelectronics | 转发：Re: LPDDR5 存储颗粒选型需求 | 南亚无 LPDDR5 |
| `19e065c771a63d06` | 2026-05-08 14:52:31 +0800 | 何鹏程转发，原始来源 Link Liu / Golden Supreme | 转发：回复: LPDDR5 存储颗粒选型需求 | 三星 LP5X 不匹配、生命周期 2-3 年、附件料号 |
| `19e065c87163f67f` | 2026-05-08 14:53:00 +0800 | 何鹏程转发，采购发给 Henry | 转发：LPDDR5 存储颗粒选型需求 | Henry 渠道仅见发出需求，未见回复 |

## 4. 美光证据

### 4.1 邮件反馈

Kun Cao / WT Microelectronics 反馈：

- 美光 x32 LPDDR5/LPDDR5X 从 4GB 起步。
- 推荐：`MT62F1G32D2DS-020 WT:D`。
- 需要补充项目信息：终端客户、项目名称、应用、试产时间、量产时间、主芯片、年用量、每片用几颗。

Vince Huo / WPI 反馈：

- 美光后续主推 9600 MT/s 产品。
- 原 8533 速率型号将停产。
- 7500 以下已经停产。
- 列出 Y62P / Y6CP 系列候选。

### 4.2 Datasheet 证据

附件：

- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x.pdf`

从附件抽取到的关键字段：

| 字段 | 内容 |
| --- | --- |
| 标题 | Y62P LPDDR5X SDRAM |
| 接口 | LPDDR5X/LPDDR5 data interface |
| 推荐料号 | `MT62F1G32D2DS-020 WT:D` |
| 总容量 | 4GB / 32Gb |
| 数据速率 | 9600 Mb/s per pin |
| 封装 | 315-ball TFBGA，package code DS |
| 文档版本 | Rev. G 03/2026 |

相关扩展候选：

| 料号 | 容量 | 备注 |
| --- | --- | --- |
| `MT62F1G32D2DS-020 WT:D` | 4GB / 32Gb | 当前最接近候选 |
| `MT62F2G32D4DS-020 WT:D` | 8GB / 64Gb | 容量更大 |
| `MT62F4G32D8DV-020 WT:D` | 16GB | 容量更大 |
| `MT62F6G32D8DV-020 WT:B` | 24GB | Y6CP 路线，容量过大 |

### 4.3 PCN / EOL 证据

附件：

- `attachments/PCN 36290.pdf`

抽取到的关键字段：

| 字段 | 内容 |
| --- | --- |
| PCN | 36290 |
| 标题 | End of Life Notification for Y52P Specific 315b Packages |
| Published | 2026-02-04 |
| Description | Micron discontinuing specific LPDDR5 Y52P 315b DDP/QDP/8DP packages |
| Last Order Date | 2026-08-04 |
| Last Ship Date | 2027-02-04 |
| NCNR Date | 2026-05-06 |

邮件正文还引用 PCN_36383：

| 字段 | 内容 |
| --- | --- |
| PCN | 36383 |
| Published | 2026-04-22 |
| 标题 | End of Life of LPDDR5 Y52Q Embedded Automotive and Non-Automotive |
| 影响 | Y52Q 315b x32 2GB SDP、441b x64 4GB DDP 等 |
| Last Order Date | 2026-10-23 |
| Last Ship Date | 2028-12-31 |
| NCNR Date | 2026-07-25 |

工程判断：

- 旧代 2GB x32 路线与 5-8 年生命周期目标冲突。
- 若项目坚持 2GB，需要供应商给出非 EOL、可长期供货的正式替代料号，否则不能冻结。

## 5. 三星证据

### 5.1 邮件反馈

Link Liu / Golden Supreme 反馈：

- 三星目前出货 LP5X 产品，从容量和生命周期角度都没有能匹配需求的产品。
- 最小容量产品预计 2026 年 5 月底或 6 月中出样品。
- 该产品为消费类。
- 消费类生命周期通常 2-3 年。

### 5.2 Datasheet 证据

附件：

- `attachments/[Datasheet]LP5X_32Gb_D_245F_8.2x12.4_K3KL8L80DM-TGCT_Rev0.0.pdf`

抽取到的关键字段：

| 字段 | 内容 |
| --- | --- |
| 料号 | `K3KL8L80DM-TGCT` |
| 类型 | LPDDR5X SDRAM |
| 容量 | 32Gb / 4GB |
| 组织 | x32 |
| 封装 | 245FBGA，8.2 x 12.4 mm |
| 最大频率 | 7500 Mbps |
| 温度 | Tc -25 to 85 C |

工程判断：

- 该料号容量和位宽接近美光 4GB x32 方向，但供应商已明确生命周期不匹配。
- 245FBGA 封装不同于美光 315-ball TFBGA，不能无缝替代。
- 不建议进入主设计路径。

## 6. 南亚证据

Fifi Lin / WT Microelectronics 反馈：Nanya 没有 LPDDR5。

工程判断：南亚路线关闭。

## 7. Henry / HSRP 证据

采购于 2026-05-08 10:10 向 Henry 发出 LPDDR5 需求。当前 Gmail 搜索范围内未见回复。

工程判断：不可计入可用候选。采购可催一次作为补充渠道。

## 8. 工程风险登记

| 风险 ID | 风险 | 影响 | 当前状态 | 缓解措施 |
| --- | --- | --- | --- | --- |
| R1 | 2GB x32 长生命周期料号不可得 | 原始需求无法直接满足 | 已发生 | 接受 4GB x32 或扩大供应商范围 |
| R2 | 美光候选容量上浮至 4GB | BOM、系统内存映射、初始化配置可能变化 | 待决策 | 项目负责人确认需求变更 |
| R3 | LPDDR5X 9600 降频到 3733 使用 | EMIF 参数、training、ODT、SI 需验证 | 待验证 | 供应商确认 + Quartus EMIF 验证 |
| R4 | 旧代美光料号 EOL | 生命周期不满足 5-8 年 | 已有 PCN 证据 | 不选旧代 2GB 料号 |
| R5 | 三星消费类生命周期短 | 量产后供应风险 | 已明确 | 不作为主推料号 |
| R6 | pin/bank/PLL/RZQ 资源冲突 | Fitter 失败或 PCB 返工 | 待验证 | 逻辑侧建立最小 Quartus 工程 |
| R7 | 封装差异 | 原理图库、PCB footprint、SI 模型不同 | 待验证 | 只冻结一个主料号后再建库 |

## 9. Quartus / 原理图验证建议

建议逻辑侧先按美光 `MT62F1G32D2DS-020 WT:D` 做最小验证：

输入参数：

- Device：Intel Agilex 5，当前按 A5ED052A B32A 方向评估。
- Memory：LPDDR5/LPDDR5X x32。
- Candidate：`MT62F1G32D2DS-020 WT:D`。
- Data rate：先按主控可支持上限 3733 MT/s 建立目标约束。
- Topology：每组一个 LPDDR5 主控，对应一个 x32 颗粒；项目当前按两组 x32 规划。

逻辑侧输出：

- EMIF 配置截图或参数导出。
- Pin Planner 结果。
- Fitter 规则检查结果。
- QSF / pin report。
- 与 MIPI D-PHY、QSFP、clock/reset/config 共存的资源冲突说明。

硬件侧输出：

- 315-ball TFBGA DS footprint 和符号页。
- 电源 rail、RZQ、reset、refclk、ODT/termination、VREF/相关接口设计检查。
- 与板级空间和 SI 约束的初步结论。

## 10. 工程验收标准

在进入原理图 pin list 冻结前，至少满足：

1. 供应商正式确认 `MT62F1G32D2DS-020 WT:D` 的生命周期、温度等级、供货周期和价格。
2. 项目负责人确认可接受 4GB x32 方案。
3. 逻辑侧完成 Quartus EMIF + Pin Planner / Fitter 验证。
4. 硬件侧确认封装、供电、pinout、原理图资源和 PCB 可实现性。
5. 采购确认是否存在 2GB x32 长生命周期替代料号；如无，则在需求中正式记录容量变更。

## 11. 附录：当前工作文件

- `lpddr5_mail_summary.md`
- `lpddr5_supplier_matrix.csv`
- `lpddr5_reply_drafts.md`
- `attachments/PCN 36290.pdf`
- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x_19e065df94f3cfec.pdf`
- `attachments/315b-441b-561b-y6cp-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- `attachments/[Datasheet]LP5X_32Gb_D_245F_8.2x12.4_K3KL8L80DM-TGCT_Rev0.0.pdf`

</file>
<file path="Daily/raw/2026-05-08/5月8日_extracted/lpddr5_report_procurement.md">
# LPDDR5 采购沟通报告

日期：2026-05-08
用途：给采购内部同步、推动供应商继续确认、形成邮件回复基础

## 1. 一句话结论

当前供应商反馈没有找到完全匹配 `2GB / 16Gb、x32、LPDDR5、商业级、未来 5-8 年无 EOL` 的料号。建议采购把美光 `MT62F1G32D2DS-020 WT:D` 作为主线继续确认，但该料号是 `4GB / 32Gb x32 LPDDR5X`，需要项目确认是否接受容量上浮。

## 2. 供应商反馈汇总

| 供应商/渠道 | 反馈结论 | 是否继续推进 |
| --- | --- | --- |
| 美光 / WT / WPI | 有可推进料号 `MT62F1G32D2DS-020 WT:D`，4GB x32 LPDDR5X，9600 Mb/s。美光 x32 当前 4GB 起步，旧 2GB 相关料号有 EOL/停产风险。 | 继续推进，作为主线 |
| 三星 / Golden Supreme | 当前出货产品从容量和生命周期看不匹配。`K3KL8L80DM-TGCT` 是消费类 32Gb x32 245FBGA，生命周期通常 2-3 年。 | 暂不推进 |
| 南亚 / Nanya | 没有 LPDDR5。 | 关闭 |
| Henry / HSRP | 目前只看到需求发出，未看到回复。 | 催一次 |

## 3. 当前主推候选

| 项目 | 内容 |
| --- | --- |
| 厂商 | Micron / 美光 |
| 料号 | `MT62F1G32D2DS-020 WT:D` |
| 类型 | LPDDR5X |
| 容量 | 4GB / 32Gb |
| 位宽 | x32 |
| 速率 | 9600 Mb/s per pin |
| 封装 | 315-ball TFBGA DS |
| 当前问题 | 不是原需求 2GB，需要确认容量上浮和生命周期 |

## 4. 采购需要向美光确认的问题

请优先向美光/WT/WPI 确认：

1. `MT62F1G32D2DS-020 WT:D` 是否为长期主推料号。
2. 是否可以支持未来 5-8 年供货周期。
3. `WT:D` 对应温度等级和供货等级。
4. sample、小批量、量产 lead time。
5. 价格阶梯、MOQ、MPQ。
6. 如果坚持 2GB / 16Gb x32，是否还有非 EOL、可长期供货的替代料号。
7. 9600 Mb/s 料号降频到 3733 MT/s 长期使用是否有原厂建议或限制。

## 5. 需要补给美光的项目信息

供应商已要求补充以下信息：

| 项目 | 建议填写 |
| --- | --- |
| 终端客户 | 待项目确认 |
| 项目名称 | A38 / DF108 Agilex 5 |
| 应用 | 工业相机 / FPGA 图像处理板卡 |
| 试产时间 | 待项目确认 |
| 量产时间 | 待项目确认 |
| 主芯片 | Intel Agilex 5，当前按 A5ED052A B32A 方向评估 |
| 年用量 | 待采购/项目确认 |
| 每片用几颗 | 当前暂按 2 颗 x32 LPDDR5/LPDDR5X 规划，最终以原理图和 Quartus EMIF 验证为准 |

## 6. 建议发给美光/WT 的邮件

Hi Kun / Brandon，

感谢推荐。我们这边初步可以评估 `MT62F1G32D2DS-020 WT:D`，但需要先确认几个问题：

1. 该料号是否为长期主推料号？是否可以支持未来 5-8 年供货周期？
2. `WT:D` 对应的温度等级和供货等级请帮忙确认一下。
3. 当前样品、小批量和量产 lead time 分别是多少？
4. 请提供价格阶梯和 MOQ / MPQ。
5. 如果我们原需求坚持 2GB / 16Gb、x32、LPDDR5/LPDDR5X、商业级、5-8 年无 EOL，是否还有其他可推荐料号？
6. 该 9600 MT/s 料号是否适合在 3733 MT/s 主控下长期降频使用？是否有需要注意的初始化、ODT、training 或 SI 要点？

项目信息如下，供原厂评估：

- 终端客户：待确认
- 项目名称：A38 / DF108 Agilex 5
- 应用：工业相机 / FPGA 图像处理板卡
- 试产时间：待确认
- 量产时间：待确认
- 主芯片：Intel Agilex 5，当前按 A5ED052A B32A 方向评估
- 年用量：待采购/项目确认
- 每片用量：暂按 2 颗 x32 LPDDR5/LPDDR5X 规划，最终以原理图和 Quartus EMIF 验证为准

谢谢。

## 7. 建议回复三星渠道

Hi Link，

收到，谢谢确认。由于我们这个项目要求未来 5-8 年生命周期，目前消费类 2-3 年生命周期的 LP5X 245ball 产品暂时不适合作为主推方案。

这边先不按该料号推进。如果后续三星有 x32、长期供货、商业级或工业级、生命周期可覆盖 5-8 年的 LPDDR5/LPDDR5X 料号，请再帮忙推荐。

谢谢。

## 8. 建议催 Henry

Hi Henry，

麻烦帮忙确认一下是否有符合以下条件的 LPDDR5/LPDDR5X 颗粒：

- 单颗 2GB / 16Gb
- x32
- Standard BGA
- 商业级即可
- 主控最高 3733 MT/s，可接受 5500/6400/更高速率料号降频使用
- 要求未来 5-8 年无 EOL 风险

如果 2GB x32 已经无长期供货方案，也请直接帮忙反馈可替代的 x32 4GB 长生命周期料号。

谢谢。

## 9. 采购内部提醒

- 不建议继续把“三星消费类 245ball LP5X”作为主线，因为生命周期只有 2-3 年，不满足项目要求。
- 不建议把旧代美光 2GB x32 作为主线，因为 PCN/EOL 风险明确。
- 采购推进前需要项目负责人确认：是否接受容量从 2GB 上浮到 4GB。
- 硬件/逻辑确认前，不要冻结最终 LPDDR5 pin list 或封装设计。

## 10. 附件清单

- `attachments/PCN 36290.pdf`
- `attachments/315b-441b-561b-y62p-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- `attachments/315b-441b-561b-y6cp-ddp-qdp-8dp-non-auto-lpddr5x.pdf`
- `attachments/[Datasheet]LP5X_32Gb_D_245F_8.2x12.4_K3KL8L80DM-TGCT_Rev0.0.pdf`
</file>
<file path="Daily/raw/2026-05-08/5月8日_extracted/今日完成项.md">
处理issue4，负责固件烧录未完成。出现了au15P无法固化问题。
烧写不成功，0x0000地址被锁住了，lock住了，擦除，烧写不了
步骤和KU3P固化的一样，但ku3p没问题

寻样和整理lpddr5的情况。见其它文件。
</file>
