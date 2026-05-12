# Workflow Rules

## Rule 1: 原始 notes 在保留期内不可覆盖

触发条件：任何 AI 整理、同步、压缩、改写动作。
规则：AI 只能生成下划线开头的新文件，不能覆盖原始 notes。raw 是临时事实输入层，不是永久记录层；daily 完整生成并人工审核后，raw 可在 7 天后删除。
原因：保留短期纠错所需的真实工作轨迹，同时避免 repo 长期堆积低价值原始碎片。

## Rule 2: 只记录影响系统状态的事件

触发条件：白天记录 event stream。
规则：优先记录决策、阻塞、产出、上下文切换、重要信息、下一步。
原因：cyberlog 的目标不是流水账，而是可分析的工作流遥测。

## Rule 3: 每天必须生成明日启动包

触发条件：当天结束前。
规则：生成 _tomorrow-boot.md 或至少在 _cyberlog.md 中保留 Tomorrow Boot Packet。
原因：降低第二天恢复上下文的成本。

## Rule 4: Daily AI request 默认完整处理

触发条件：用户要求处理 daily、cyberlog、_ai-request.md，或当天结束流程。
规则：不要停在 _ai-request.md。默认生成 _cyberlog.md、_tomorrow-boot.md 和 _ai-output-audit.md；如果有写入权限，直接保存到 Daily/compiled/YYYY-MM-DD/。
原因：_ai-request.md 只是任务包，不是用户最终要看的整理结果。完整处理才能降低查看和恢复上下文成本。

## Rule 5: 重复 3 次的阻塞必须转成规则、模板或脚本

触发条件：同类 blocker/friction 在一周内重复出现。
规则：不要只复盘，要把它沉淀为 workflow rule、template、checklist 或 automation。
原因：自我迭代必须改变系统，而不是只改变意愿。

## Rule 6: Daily repo 只做底层记录，不做工作空间

触发条件：记录项目资料、采购反馈、设计证据、供应商邮件、外部协作材料时。
规则：本 repo 只维护 daily 内容和 AI 整理所需的底层数据；只记录状态、结论摘要、阻塞、下一步和外部资料位置，不保存原始工作资产。
原因：daily cyberlog 的价值是恢复上下文和分析工作流。如果把正式项目资料、采购证据、邮件全文、报价、设计源文件放进来，会污染 raw/compiled 管线，并让 AI feed、weekly review 和 Git 历史反复扩散不该扩散的信息。

## Rule 7: raw 清理必须留下 discard log

触发条件：清理 `Daily/raw/YYYY-MM-DD/`。
规则：只清理已经完整生成并人工审核的日期目录；删除前默认 dry-run，实际删除必须写入 `Daily/compiled/YYYY-MM-DD/_raw-discard-log.md`，记录文件名、大小和 hash。
原因：raw 不再永久保存，但清理行为本身要可解释，未来能知道当时丢弃了哪些输入。

## Rule 8: 有价值生成物默认同步远端

触发条件：AI/Codex 生成了有保留价值的 compiled 输出、规则、手册、审计、复盘、模板或其它可复用生成物。
规则：完成本地验证后，默认把相关文件提交并推送到远端；不要等用户再次提醒。提交前先看 `git status`，只纳入本次任务相关文件，不夹带无关改动。
原因：daily repo 的价值在于可恢复、可跨设备同步和可追溯。生成物只停留在本地会增加丢失和上下文断裂风险。
