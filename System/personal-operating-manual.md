# Personal Operating Manual

这个 manual 记录稳定有效的个人工作流规则。它不是日记，也不是任务清单；只沉淀能重复使用的操作方式。

## 我如何启动一天

1. 把今天的原始文件放入 `Daily/raw/YYYY-MM-DD/`。
2. 如需模板，可从 `Daily/templates/` 复制到当天 raw 目录后再写。
3. 写下今日主线：今天最希望推进的 1-3 件事。
4. 从昨天的 `_tomorrow-boot.md` 拿第一动作，直接进入执行。

## 我如何关闭一天

1. 保留所有原始 notes，不重写、不清理事实轨迹。
2. 运行 `python tools/cyberlog.py daily --date YYYY-MM-DD` 生成 `_ai-request.md`。
3. 默认让 Codex/agent 完整处理 `_ai-request.md`，并保存 `_cyberlog.md`、`_tomorrow-boot.md`、`_ai-output-audit.md`。
4. 审核 `_ai-audit.md` 和 `_ai-output-audit.md`，确认没有混入被排除目录、没有把草稿或推断升级成事实。
5. 把明确值得复用的规则候选手动写入 `System/workflow-rules.md`。

当天关闭完成标准：
- `_ai-feed.md`
- `_ai-request.md`
- `_ai-audit.md`
- `_cyberlog.md`
- `_tomorrow-boot.md`
- `_ai-output-audit.md`

## 我如何处理阻塞

阻塞必须写清楚四件事：原因、解除方式、owner、下一步。

如果同类阻塞重复出现，不再只写复盘结论，而是沉淀为规则、模板、checklist 或脚本。

## 我如何把任务交给 AI / agent

适合交给 AI / agent 的任务通常具备：
- 输入材料清楚。
- 完成标准可以描述。
- 判断风险低，或可以由我最后审核。
- 输出可以被复制、修改或丢弃。

不适合直接交给 AI / agent 的任务通常包括：
- 需要个人偏好或战略取舍的判断。
- 事实来源不足但后果较大的决策。
- 会影响真实资产、账号、生产系统或他人承诺的动作。

## 我如何判断任务是否完成

一个任务完成至少要满足：
- 产出已经落到明确位置。
- 下一步不存在，或已经写入后续任务。
- 风险、阻塞、未决问题已经显式记录。
- 未来恢复上下文不需要重新推理整段过程。

对 daily cyberlog 来说，只生成 `_ai-request.md` 不算完成；必须生成并审核 `_cyberlog.md`、`_tomorrow-boot.md` 和 `_ai-output-audit.md`。

## 我如何做周复盘

1. 确保每天都有 `_cyberlog.md` 和 `_tomorrow-boot.md`，缺失可以接受但要知道缺口。
2. 运行 `python tools/cyberlog.py weekly --start YYYY-MM-DD --end YYYY-MM-DD`。
3. 把生成的 weekly request 投喂给 AI。
4. 只提取能改变下周行为的结论，不保存流水账总结。

## 我如何沉淀规则

规则必须包含触发条件、执行动作、原因和证据。

只有当规则能减少未来摩擦、降低上下文恢复成本、改善决策质量或减少重复劳动时，才写入 `System/workflow-rules.md`。
