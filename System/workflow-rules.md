# Workflow Rules

## Rule 1: 原始 notes 永不覆盖

触发条件：任何 AI 整理、同步、压缩、改写动作。
规则：AI 只能生成下划线开头的新文件，不能覆盖原始 notes。
原因：保留真实工作轨迹，避免 AI 误写污染事实。

## Rule 2: 只记录影响系统状态的事件

触发条件：白天记录 event stream。
规则：优先记录决策、阻塞、产出、上下文切换、重要信息、下一步。
原因：cyberlog 的目标不是流水账，而是可分析的工作流遥测。

## Rule 3: 每天必须生成明日启动包

触发条件：当天结束前。
规则：生成 _tomorrow-boot.md 或至少在 _cyberlog.md 中保留 Tomorrow Boot Packet。
原因：降低第二天恢复上下文的成本。

## Rule 4: 重复 3 次的阻塞必须转成规则、模板或脚本

触发条件：同类 blocker/friction 在一周内重复出现。
规则：不要只复盘，要把它沉淀为 workflow rule、template、checklist 或 automation。
原因：自我迭代必须改变系统，而不是只改变意愿。
