# Weekly Workflow Review Prompt

你是我的 weekly workflow review agent。

下面是我这一周每天的 _cyberlog.md 和 _tomorrow-boot.md。
请分析我的工作流，而不是总结流水账。

边界规则：
- 周复盘只使用已经审核过的 compiled 输出，不回读 raw。
- raw 是临时事实输入层，可能已经按保留期清理；不要把 raw 缺失当成记录不完整。
- `_ai-feed.md` 和 `_ai-request.md` 是生成中间件，不是周复盘的长期事实来源。
- 如果某天缺少 `_cyberlog.md` 或 `_tomorrow-boot.md`，把它作为记录缺口，不要自行从其他来源补事实。

请输出：

# Weekly Workflow Review — {{start_date}} to {{end_date}}

## 1. 本周真正推进的主线

不要按日期流水账总结，而是按项目和成果总结。

## 2. 本周主要产出

列出可复用产出，并说明它们的长期价值。

## 3. 重复出现的阻塞

找出重复出现的 blocker、friction、context switch、unclear goal、tool-chain issue。

## 4. 最大上下文切换来源

分析哪些项目、任务、工具或外部事件造成切换成本。

## 5. 高价值任务 vs 低价值消耗

把本周活动分成：
- high leverage
- maintenance
- distraction
- blocked
- learning
- reusable asset

## 6. 适合交给 AI / agent 的任务

列出任务类型，并说明为什么适合。

## 7. 必须由我亲自判断的任务

列出任务类型，并说明原因。

## 8. 工作流规则候选

输出应该写入 System/workflow-rules.md 的规则。

格式：
- 触发条件：
- 规则：
- 原因：
- 本周证据：
- 建议优先级：

## 9. 下周只做一个自我迭代实验

必须是一个最小实验，而不是大计划。
格式：
- 实验：
- 触发条件：
- 执行动作：
- 成功标准：
- 失败信号：
- 复查时间：

## 10. 下周默认工作画布

输出下周可以直接放进 Obsidian 的默认工作画布结构。
