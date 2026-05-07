# AI Sync Request - 2026-05-07

## 使用说明

复制本文件全部内容，粘贴给 AI。

AI 输出后建议保存为：
- `Daily/compiled/2026-05-07/_cyberlog.md`
- `Daily/compiled/2026-05-07/_tomorrow-boot.md`

请先审核 AI 输出，不要让 AI 覆盖任何非下划线开头的原始 notes。

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

请输出以下结构：

# Cyberlog — 2026-05-07

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

# Tomorrow Boot Packet — 2026-05-08

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
- 输出要适合直接复制到 _cyberlog.md 和 _tomorrow-boot.md。

## AI Feed

<file path="Daily/raw/2026-05-07/5月7日_extracted/00当日规划.md">
1、将A57项目进度，会议，方案，节点，落地，测试，配套设备，
串行板等进行梳理规划。
2、设计intel altera agilex5原理图。给出框图。
3、同步当日事件。cyberlog。
4、workspace加入sop，demo等，需要可拓展，容易修改。
5、将github上的my wiki同步到本地。
6、做成skills。拿当日内容作为测试用例
7、sch reviewer中间可以输出一个解码层，即任意llm都可以看懂的原理图数据结构。
8、项目做成skills。以及agilex芯片也做成skills。这里
</file>
<file path="Daily/raw/2026-05-07/5月7日_extracted/A38 Intel Altera Agilex 5/00设计项plan.md">
  1. Power Tree 必须重做
     Agilex 5 的 power rail、sequencing、monitor、SmartVID/PMBus 等不能沿用 KU040。Intel 官方 Power Management Guide 明确把 power tree、power estimation、
     power generation、I/O sequencing 作为设计阶段内容。
  2. Pin / bank / transceiver 必须先规划再画图
     Intel Pin Connection Guidelines 覆盖 FPGA core pins、GTS transceiver pins、HPS pins、power sharing 等。你应该先用官方 pinout + Quartus pin planning 固
     化 bank/VCCIO/refclk/GTS，再回到原理图，不要先凭封装页连线。
  3. Boot 模式是架构决策，不是原理图细节
     Agilex 5 SoC 有 FPGA Configuration First 和 HPS Boot First 这类路径。官方 HPS boot 文档说明 FPGA first 会先完成 FPGA/I/O 配置再释放 HPS；这更接近
     KU040 原 fabric-centric 产品的迁移节奏。
  4. 外设保持矩阵是主线
     8 路 FAKRA、POC、DPS、机壳、光口物理形态是硬约束。每个接口都要有一张表：


</file>
<file path="Daily/raw/2026-05-07/5月7日_extracted/A38 Intel Altera Agilex 5/LPddr5需求 to 采购工程师 沟通.md">
【LPDDR5 存储颗粒选型需求】  
  
核心规格：LPDDR5 (Standard BGA Package)  
  
位宽要求：单颗要求为 32-bit 架构  
  
容量需求：单颗容量要求 2GB (16Gb)。  
  
速率匹配：  
  
主控端支持上限：3733 MT/s (Mbps)  
  
寻源建议：优先选择目前市面主流的 5500 MT/s 或 6400 MT/s 规格颗粒（硬件设计时会向下兼容降频运行）。  
  
温度等级：  
  
商业级即可。  
  
生命周期：需保证长期供应，务必确认所提供料号在未来 5-8 年内无 EOL。  
  
推荐品牌：美光、三星、海力士等一线大厂。

等待采购反馈。
</file>
<file path="Daily/raw/2026-05-07/5月7日_extracted/A38 Intel Altera Agilex 5/lpddr5 pin assign  项目群沟通.md">

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
</file>
<file path="Daily/raw/2026-05-07/5月7日_extracted/A38 Intel Altera Agilex 5/框图修改.md">
1、去掉HS/LP 切换开关，去掉buffer，MIPI是从解码板过来经过连接器后直连。全部连接到A5EC052A B32A的HSIO bank。
2、DDR4这里改为使用lpddr5，帮我看下lpddr5的实际应用速率可以到多少？参考文件在https://drive.google.com/drive/folders/1LBmcH09JFtY-A9iW-TYNtksNjdZ7o8wS?dmr=1&ec=wgc-drive-%5Bmodule%5D-goto
3、电源入口使用LM5060方案，这里我已经有成熟电路只需要迁移即可。
4、



  # DF108 快速第一版原理图推进计划

  ## Summary

  当前目标是推进 DF108 主控板第一版原理图改版，不做最终 sign-off。旧 DF108/KU040 原理图基线先按正确处理；当前工作是在旧图基础上加入 Agilex 5 方案占位，并
  保持设计状态清晰。

  当前状态：
 
  | 分类 | 内容 |
  |---|---|
  | 已确认 | MIPI 去掉 HS/LP switch 和 buffer，走解码板 -> 连接器 -> Agilex 5 MIPI-capable HSIO bank 直连方向 |
  | 已确认 | DDR4 改 LPDDR5；当前按 Agilex 5 E-Series Group A 口径，LPDDR5 上限按 3,733 Mbps/pin |
  | 已确认 | LPDDR5 第一版按 2 组规划，每组 1 个 LPDDR5 主控，对应 x32 颗粒 |
  | 已确认 | 24V 电源入口复用成熟 LM5060 拓扑，但参数必须按新电源树重算 |
  | 暂定假设 | A5EC052A B32A / A5ED052AB32AE2V 命名差异先按占位处理，不直接判为设计错误 |
  | 待补证 | Quartus EMIF、Pin Planner、官方 datasheet、reference design、MIPI D-PHY IP、LPDDR5 vendor datasheet |
  | 当前要画的页 | 主芯片符号分页、2 组 LPDDR5 主控资源、MIPI 直连页、电源入口和电源树页 |

  ## Key Changes

  - 新增当前 revision 下的 CSV 资源矩阵，建议路径：
    revisions/rev-20260506-df108-ku040-to-a5ed052ab32ae2v/02_design_evidence/a5ec052a_b32a_resource_allocation_matrix_20260507.csv
  - CSV 必须覆盖这些列：
    domain,group,signal_group,source,connector_or_device_pin,target_bank,target_pin_or_lane,rate_or_voltage,dependency,status,evidence_required,schematic
    _page,notes
  - group 用于区分 MIPI_n、LPDDR5_CTRL0_X32、LPDDR5_CTRL1_X32、POWER_SEQ、CLOCK_RESET_CONFIG、NAMING。
  - status 只允许使用：
    confirmed, assumed_for_rev1, pending_quartus, pending_pin_planner, pending_datasheet, pending_reference_design, naming_cleanup
  - 资源矩阵内容分五组：
    MIPI lane map, LPDDR5 EMIF bank/pin plan, power sequencing, clock/reset/config, A5EC/A5ED naming cleanup
  - 不覆盖旧 run，不把该 CSV 放到 sch-review 工具仓；它属于 DF108 当前 revision 的设计证据。

  ## Schematic Drawing Order

  技术层：

  1. 主芯片符号分页
     先按功能页拆 Agilex 5：power/GND、MIPI-capable HSIO、LPDDR5 EMIF、clock/reset/config、普通 IO/保持接口。A5EC/A5ED 名称全部标为占位待清理。
  2. LPDDR5
     第一版按 LPDDR5_CTRL0_X32 和 LPDDR5_CTRL1_X32 两组画。每组对应一个 LPDDR5 主控和一个 x32 颗粒资源域；具体 EMIF bank、byte lane、RZQ、refclk、reset、
     AC/data pin 必须等 Quartus EMIF + Pin Planner 输出后回填。
  3. MIPI
     画解码板连接器到 Agilex 5 HSIO 的直连框架；lane count、lane rate、clock lane、target bank/lane、RZQ/refclk 标为待确认。不能按普通 LVDS 差分 IO 处
     理。
  4. 电源入口
     迁移 LM5060 成熟电路拓扑，但 current limit、inrush、MOSFET SOA、PG/FLT、后级 bulk cap 不沿用旧值做关闭判断。
  5. 电源树
     画 Agilex 5 + 两组 LPDDR5 rail 分组、POL 列表、PG chain 和 enable dependency；电压/电流/时序来自官方 power guide/reference design 后再冻结。
  6. Clock/reset/config
     先画系统时钟、MIPI refclk、两组 EMIF refclk、POR/reset、config boot 基础页；具体频率、pin 和依赖全部进入资源矩阵待补证。
  7. 外设保持接口
     旧 DF108 外设域如 FAKRA、POC、DPS、光口物理形态先保持；只记录哪些信号迁移到 Agilex 5，避免在第一版误改外围。

  ## Test And Review Plan

  - 文档/规则入口修改后做一次链接和引用一致性检查。
  - 若后续修改 sch-review 代码，再运行：
    python3 -m pytest tests/unit/ -q
  - 第一版原理图检查只做快速 gate：
    MIPI 是否只连到 MIPI-capable HSIO、两组 LPDDR5 x32 是否各自有独立 EMIF 主控归属、LM5060 是否列出重算项、A5EC/A5ED 是否未混成正式结论。
  - 不使用 GitHub、不 git pull、不基于远端上下文判断。

  ## Assumptions

  - LPDDR5 第一版按 2 组 x32 颗粒规划，每组对应一个 LPDDR5 主控。
  - resource allocation matrix 第一版使用 CSV。
  - A5EC052A B32A 当前是封装/方案占位；正式发布前再统一到目标 A5ED052AB32AE2V 命名和证据。
  - 所有 pin、bank、速率、power sequencing 结论在第一版中只可标为待 Quartus/Pin Planner/官方资料确认，不能用推测替代。
</file>
<file path="Daily/raw/2026-05-07/5月7日_extracted/Issue4.md">
这是一份结合了最新讨论进展的 Issue 同步文案。最新的沟通中，一个非常关键的进展被确认：**后两通道的 AUX 通信握手其实是正常的**，排查焦点已经彻底从链路训练锁定到了“解码芯片未能正常输出有效数据”上。

文案中已将相关的责任人（包括新加入讨论的张纪琦、吴锋）以及具体的 Action Items 进行了更新分配，您可以直接复制发送：

---

### 🔴 A57 项目 Issue 同步：eDP 后两通道概率不出图最新排查结论与计划

@何鹏程 (hepc) @吴锋 (wuf) @路阳 (luy) @Candy|罗奇军 (luoqj) @吴志安 (wuzhian) @张纪琦 (zhangjq)

各位，基于今晚最新的沟通与底层状态核对，A57 eDP 后两通道（AU15P侧）概率不出图的问题有了更加明确的排查方向。底层逻辑排查已基本见底，确认**核心问题不在 FPGA 接收逻辑，而极大概率在于前端 eDP 解码芯片的配置或物理状态异常**。

以下是全盘梳理及明天的协同攻关计划：

#### 🔍 1. 当前底层最新确认事实与核心推断

目前 4 通道 eDP 分两个 FPGA 接收：前 2 通道 (eDP0/1) 在 KU3P，出图较好；后 2 通道 (eDP2/3) 在 AU15P，存在开关视频流概率不出图。底层核对确认以下两点事实：

- ✅ **AUX 通信及链路训练正常：** 经过核实，后 2 通道的 AUX 通信并未卡死，握手指令读写能一直正常走完，且与前 2 通道逻辑完全一致。
    
- ❌ **SerDes 接收异常且复位无效：** 直接异常表现为 SerDes CDR 不能锁定、COMOM 不能对齐且存在周期性异常。通常这类情况若输入源正常，通过手动复位 SerDes 即可解决（demo 板已验证）。但目前实测**手动复位毫无改善**。
    

**💡 核心推断：** 由于 AUX 握手正常，但底层真正采数据的源头（SerDes）在复位后仍无法锁定，说明 **eDP 解码芯片根本就没有输出正常/有效的图像数据**。目前高度怀疑后两通道 eDP 解码芯片没有被正常配置起来（上电时序、IIC 指令下发存在异常）。

#### 🛠️ 2. 下一步联合排查计划 (Action Items)

明天重点围绕“解码芯片为何未输出正常数据”展开多方排查：

**📌 硬件侧排查（@何鹏程 @吴锋）：**

1. **上电时序确认：** 吴锋明天帮忙用示波器抓取，重点核对后 2 通道 eDP 解码芯片的实际**上电时序**是否严格符合手册要求。
    
2. **物理输出量测：** 何鹏程继续配合，在 AP 出现不出图的故障态时，实测确认 eDP 解码芯片此时是否确实没有任何图像数据输出。
    

**📌 MCU / 软件侧排查（@张纪琦 @Candy|罗奇军）：**

1. **配置指令核查：** 确认开关视频流时，从解码芯片、Redriver 到 FPGA 的具体操作动作。用示波器辅助确认 MCU 对后 2 通道 eDP 解码芯片的 **IIC 参数下发**是否真实、正确地送达。
    
2. **双核控制变量验证：** 验证排查双核处理机制的影响（尝试前 2 通道让核 2 控制，后 2 通道让核 1 控制）。
    

---

#### 📎 附录：前期已知事实与排查记录（Context Backup）

为避免信息断层，汇总本 Issue 前期的异常现象与已排除项：

- **单点勾选异常：** 对于后 2 通道，单点 DEV3 对应的 SerDes 接收必然出问题；若同时勾选 DEV3 和 DEV4，对应接收情况会有所改善。
    
- **管脚初始状态差异：** 前期曾在 FPGA 侧抓到 4 组 `aux_in` 初始状态存在通道间差异，尝试在逻辑侧弱下拉统一电平但失效。此现象一度怀疑是外部链路漏电/电平转换芯片问题，但随着今晚确认 AUX 指令能正常跑完，此管脚初始电平差异被证明未阻塞底层的协议握手。当前主攻方向已转移至解码芯片源头。
</file>
<file path="Daily/raw/2026-05-07/5月7日_extracted/chatroom/未命名.md">
这种情况下，我重新跑一便，怎么确保不会和之前数据造成困扰？直接覆盖删除？
给我新旧架构图，并且告诉我你是怎么执行生成架构图的？

现在回到主路径，分析我应该如何设计。




可选方案

  A. 一步到位启用 A5ED HPS
  把 A5ED 当 SoC 用，HPS 接管一部分 MCU/管理/升级/boot/control path。

  优点：架构潜力最大，长期平台化更好。
  缺点：原理图、固件、boot、升级、量产测试全部复杂化。

  B. 先做 Fabric 主控替换，HPS 硬件预留但不承担关键功能
  A5ED 仍按最终目标器件设计，HPS 供电/boot/debug 基础条件留好，但第一版把 DF108 关键控制链路尽量保持在 FPGA fabric / 既有控制路径上。

  优点：风险最小，最符合“旧图正确 + 新封装占位”的当前阶段。
  缺点：A5ED 的 HPS 价值第一版没有完全释放。

  我建议你选

  选 B：HPS 预留、Fabric 先替换 KU040 主路径。

  也就是说，当前设计目标先写成：

  DF108 外设域保持不变；
  KU040 fabric 逻辑迁移到 Agilex 5 fabric；
  A5ED HPS 先完成硬件可用性预留，不作为第一版关键控制依赖；
  后续根据软件/升级/控制需求决定是否启用 HPS。

  为什么

  你的最大风险不在“C/D 名称没改”，也不在当前 raw error 数，而在架构耦合失控：

  1. Power Tree 必须重做
     Agilex 5 的 power rail、sequencing、monitor、SmartVID/PMBus 等不能沿用 KU040。Intel 官方 Power Management Guide 明确把 power tree、power estimation、
     power generation、I/O sequencing 作为设计阶段内容。
  2. Pin / bank / transceiver 必须先规划再画图
     Intel Pin Connection Guidelines 覆盖 FPGA core pins、GTS transceiver pins、HPS pins、power sharing 等。你应该先用官方 pinout + Quartus pin planning 固
     化 bank/VCCIO/refclk/GTS，再回到原理图，不要先凭封装页连线。
  3. Boot 模式是架构决策，不是原理图细节
     Agilex 5 SoC 有 FPGA Configuration First 和 HPS Boot First 这类路径。官方 HPS boot 文档说明 FPGA first 会先完成 FPGA/I/O 配置再释放 HPS；这更接近
     KU040 原 fabric-centric 产品的迁移节奏。
  4. 外设保持矩阵是主线
     8 路 FAKRA、POC、DPS、机壳、光口物理形态是硬约束。每个接口都要有一张表：

  旧 owner / 旧 net / 旧电平 / 旧时序 / 新 owner / 新 bank / 新约束 / 是否保持

  主设计路径

  1. 冻结任务边界
      - 旧 DF108 原理图 = 正确基线
      - U9 Agilex = 新封装/方案占位
      - A5EC/A5ED 名称后续统一
      - 当前不是 sign-off 图
  2. 做外设保持矩阵
      - FAKRA 8 路
      - POC 电源与控制
      - DPS
      - QSFP/光口
      - 风扇、DC24V、外壳出线、工装接口
      - 每项标：保持 / 重映射 / 待确认
  3. 做 A5ED pin planning
      - 官方 pinout
      - bank 电压
      - GTS lane/refclk
      - DDR/EMIF bank
      - config/JTAG/SDM pins
      - HPS pins 是否启用
      - Quartus 编译出 pin report 后再反推原理图
  4. 重做 Power Tree
      - rail list
      - 最大电流估算
      - sequencing group
      - PG/reset 关系
      - test point / sense / PMBus
      - HPS rail 即使暂不承担功能，也要按最终器件要求处理
  5. 定 Configuration / Reset / Boot
      - 第一版建议 FPGA Configuration First
      - 保留 JTAG
      - 明确 flash 类型、RSU 是否需要
      - 画出 POR -> config -> reset release -> user mode 的时序
  6. 迁移核心接口
      - DDR：Vivado MIG 不能复用，转 EMIF
      - GT/QSFP：转 Agilex GTS lane plan
      - PCIe/以太网/私有链路：逐项列 IP 等价物
      - I2C/SPI/UART/GPIO：先保持旧控制语义
  7. 再开始画正式原理图
     原理图页面建议：
      - 00_revision_assumptions
      - 01_a5ed_power
      - 02_a5ed_config_jtag_sdm
      - 03_a5ed_reset_clock
      - 04_a5ed_ddr_emif
      - 05_a5ed_gts_optical
      - 06_a5ed_hps_reserved
      - 07_peripheral_mapping
      - 08_debug_testpoints

  如果选错会怎样

  如果现在直接启用 HPS 做关键控制，风险是软件、boot、升级、量产测试一起爆炸。
  如果完全不管 HPS，又可能浪费 A5ED 选型，后续返工 HPS boot/debug/power。
  所以最稳的是：硬件按 A5ED SoC 留完整条件，第一版功能迁移按 fabric 主控走。

  你现在只要决定的 1 件事

  先定这条原则：

  本版 DF108 Agilex 5 改版，HPS 是否作为第一版关键功能路径？

  我的建议答案是：

  否。HPS 硬件预留，第一版主路径按 KU040 fabric -> Agilex fabric 迁移。


原厂FAE说这个lpddr5的pin assign最好是逻辑工程师，自己建一个工程，来配置lpddr5。整个fpga的管脚分配，都需要在工程里验证ok，再做硬件设计比较稳妥。我怎么在项目群里面询问
</file>
<file path="Daily/raw/2026-05-07/5月7日_extracted/今日完成项.md">
A5EC052AB32A_A38_MAIN 的原理图设计:
原理图框架：完成60%
MIPI：完成90%，缺FPGA仿真验证。
LPddr5：未启动
QSFP：已完成。
GPIO：未确定方案，当前GPIO过多，是否用拓展FPGA？或者用简单的拓展GPIO芯片。
电源树：未启动
时钟：未启动
复位：未启动
优化部分：未启动。预计优化思路见表[[历史debug]]，以及[[debug驱动的设计理念]]

</file>
