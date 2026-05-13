# AI 软件工程：为不确定计算单元设计确定性外壳

## 核心判断

模型能力进入软件系统运行时后，不再只是开发阶段的辅助工具，而是系统中的一类新型计算单元。

这个计算单元的本质特征是：

```text
不完全可预测，但可以被工程约束。
```

AI 软件工程的核心，不是把模型塞进系统，也不是只优化 prompt，而是围绕这个不确定推理单元设计确定性的外壳：

- 上下文边界
- 工具边界
- 状态边界
- 输出边界
- 验证闭环
- 审计回放

## 传统前提的变化

传统软件长期依赖三个默认前提：

- Schema-first：先定义数据结构。
- Logic-first：先定义执行路径。
- UI-first：先定义交互表单和流程。

AI 系统不是不要 schema、logic、UI，而是它们的位置发生变化。

更准确的重排是：

```text
Intent-first input
Context-bounded reasoning
Policy-controlled execution
Schema-validated output
Stateful audit trail
```

对应关系：

- Schema 从“入口字段约束”扩展为“输出、状态、验收和回写约束”。
- Logic 从“全部业务行为”转为“编排、策略、权限、失败处理和 gate”。
- UI 从“字段收集器”转为“目标表达、过程解释和结果审核界面”。

## AI 计算单元接口契约

如果模型是运行时计算单元，它也需要模块契约。

一个可工程化的 AI unit 至少应该定义：

| 层 | 内容 | 例子 |
|---|---|---|
| Input | 目标、上下文、证据、历史、约束 | goal, current files, historical context, project constraints |
| Policy | 允许工具、禁止动作、权限、审批点 | read-only, no raw overwrite, require human approval before send |
| Output | schema、引用、置信度、不确定性、下一步 | markdown sections, JSON fields, source citations, uncertainty |
| State | run id、prompt 版本、context hash、tool calls、validation result | `_run-state.json`, provenance hash, transitions |
| Failure | 重试、降级、人工升级、恢复点 | validation blocked, retry with smaller context, ask human |

没有这个契约，模型只是聊天窗口。

有了这个契约，模型能力才可能成为系统能力。

## 推荐运行路径

不要把模型输出直接当作业务状态。

主路径应该是：

```text
User Intent
  -> Input Normalization
  -> Context Builder
  -> Prompt / Policy Assembler
  -> Model Runtime
  -> Tool Sandbox
  -> Output Parser
  -> Validation / Conflict Scan
  -> State Store
  -> Human Review / Auto Writeback
  -> Audit / Eval / Replay
```

更短地说：

```text
input -> context -> model -> output -> validation -> writeback -> audit
```

而不是：

```text
input -> model -> output
```

没有 validation 的 AI output 不是系统结果，只是候选结果。

## 模型负责推理，系统负责状态

AI 系统最容易漂移的地方，不是单次回答，而是跨步骤、跨天、跨工具的状态。

因此要把这个边界写清楚：

```text
模型负责推理。
系统负责状态。
```

状态至少包括：

- 当前 phase
- 已使用上下文
- 已生成输出
- 已调用工具
- 已验证结果
- 未关闭问题
- 可恢复点

状态不能只靠“文件存在/不存在”隐式推断。重要流程应有显式状态文件或事件记录。

## 事实边界是第一道防线

AI 系统最大的风险通常不是“答不出来”，而是事实升级：

- 把历史写成当前事实。
- 把推断写成结论。
- 把建议写成已发生。
- 把草稿写成已发送。
- 把生成内容写成证据。

因此，AI 工程化的第一道防线不是 prompt，而是事实分层。

建议的事实层：

| 层 | 含义 |
|---|---|
| raw fact | 原始输入，未整理 |
| validated fact | 已校验事实 |
| historical context | 历史上下文，不是今天证据 |
| inference | 推断 |
| proposal | 建议或候选方案 |
| decision | 已记录决策 |
| external confirmation | 外部确认 |

如果系统无法区分这些层，模型迟早会把“看起来像事实”的内容升级成事实。

## 工具边界

工具调用必须被系统约束，而不是完全交给模型临场判断。

需要定义：

- 模型能看到哪些工具。
- 哪些工具只读，哪些会产生副作用。
- 哪些工具需要人工确认。
- 工具参数范围是什么。
- 工具结果如何回填上下文。
- 工具失败如何记录和恢复。

典型风险：

- 模型把草稿发出去了。
- 模型覆盖了 raw evidence。
- 模型读取了不该进入上下文的材料。
- 模型把工具失败当成任务完成。

## 输出边界

输出应尽量有结构。

不一定所有输出都要 JSON，但必须能被检查。

可用手段：

- 固定 section。
- 表格列数。
- 枚举值。
- source citation。
- required fields。
- validation report。
- conflict scan。

输出越可能进入后续系统状态，越需要强结构。

## 验证闭环

验证不是附属功能，而是主路径的一部分。

至少应检查：

- 输出结构是否完整。
- 引用来源是否存在。
- 是否混淆历史和当前。
- 是否把建议升级成事实。
- 是否违反项目约束。
- 是否存在跨日决策冲突。
- 是否有未关闭沟通或 blocker。

验证结果应该进入状态，而不是只打印在终端里。

## 成熟度模型

可以用下面的层级判断一个 AI 系统工程化到什么程度。

| Level | 名称 | 特征 |
|---|---|---|
| 0 | Chatbot | 只回答，不进入系统状态 |
| 1 | AI-assisted workflow | 生成候选结果，人复制和审核 |
| 2 | Governed AI workflow | 有上下文边界、输出 schema、validation、状态记录 |
| 3 | Agentic system | 能调用工具、推进任务、恢复失败，但有权限和审计边界 |
| 4 | Self-improving system | 能从失败、复盘、eval 中沉淀规则、模板、技能和自动化 |

多数系统不需要一开始追 Level 4。先把 Level 2 做扎实，通常收益最大。

## 设计检查表

设计一个 AI 功能前，先问：

- 输入边界是否清楚？
- 事实、历史、推断、建议是否分层？
- 上下文是否只包含必要材料？
- prompt 是否包含角色、目标、约束、禁止项和失败处理？
- 工具调用是否有权限和副作用边界？
- 输出是否可校验？
- 运行状态是否可恢复？
- 错误是否能回放？
- 决策是否能跨阶段流转？
- 成本、超时、安全、降级是否进入主体设计？

如果这些问题没有答案，系统只是把模型嵌进去了，还没有真正工程化。

## 反模式

常见反模式：

- 直接把模型输出写入业务状态。
- prompt 很长，但没有状态机。
- 有工具调用，但没有权限边界。
- 有总结，没有 source citation。
- 有结论，没有 validation。
- 有历史上下文，但没有标明历史身份。
- 有 agent，但没有 replay 和 audit。
- 有规则，但没有删除、合并和降级机制。

## 与 my-daily 的对应关系

这个仓库已经实践了部分结构：

- `Daily/raw/`：raw fact 输入层。
- `_ai-feed.md`：当天事实 feed。
- `_ai-context.md`：历史上下文，和当天证据分离。
- `_ai-request.md`：prompt / policy assembly。
- `_cyberlog.md`：人工可读输出。
- `_decisions.yml` / `_comms.yml`：跨日结构化状态。
- `_conflicts.md` / `_validation.md`：验证闭环。
- `_run-state.json`：phase、provenance、source hashes、validation result。
- `System/workflow-rules.md`：稳定规则。
- `Reviews/weekly/`：战术层诊断。
- `Reviews/monthly/`：系统层抽象和规则修剪。

还需要继续验证的地方：

- weekly/monthly 机制是否真的减少人工工作。
- 文档候选是否足够克制。
- 规则是否会越积越多。
- validation 是否覆盖最常见的事实升级错误。
- 历史 compiled 输出是否应该只做结构化补丁，而不全文重写。

## 一句话

AI 软件工程不是追求模型绝对确定，而是让系统能够调度模型、限制模型、验证模型、恢复模型、审计模型，并从失败中持续改进。
