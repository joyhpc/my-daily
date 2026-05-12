# Personal Operating Manual

这个 manual 记录稳定有效的个人工作流规则。它不是日记，也不是任务清单；只沉淀能重复使用的操作方式。

## 我如何启动一天

1. 把今天的原始文件放入 `Daily/raw/YYYY-MM-DD/`。
2. 如需模板，可从 `Daily/templates/` 复制到当天 raw 目录后再写。
3. 写下今日主线：今天最希望推进的 1-3 件事。
4. 从昨天的 `_tomorrow-boot.md` 拿第一动作，直接进入执行。

## 我如何判断 daily 边界

这个 repo 只作为 daily 内容维护和 AI 整理的底层数据，不作为真实工作空间。

可以进入 daily 的内容：
- 工作状态、事实摘要、决策、阻塞、下一步。
- 已发送/待发送沟通的状态标记和脱敏摘要。
- 外部资料的位置或引用线索。

不进入 daily 的内容：
- 原厂邮件全文、报价、联系人、NDA 或商务条款。
- 正式设计源文件、项目交付物、采购证据、需要受控归档的原始材料。
- 会因为进入 `_ai-feed.md`、`_ai-request.md`、`_cyberlog.md` 或 weekly review 而产生扩散风险的内容。

## 我如何关闭一天

1. 保留当天 raw，不重写、不覆盖事实输入。
2. 运行 `python3 tools/cyberlog.py daily --date YYYY-MM-DD` 生成 `_ai-request.md` 和 `_ai-context.md`。
3. 默认让 Codex/agent 完整处理 `_ai-request.md`，并保存 `_cyberlog.md`、`_tomorrow-boot.md`、`_ai-output-audit.md`。
4. 审核 `_ai-audit.md` 和 `_ai-output-audit.md`，确认没有混入被排除目录、没有把草稿或推断升级成事实。
5. 把明确值得复用的规则候选手动写入 `System/workflow-rules.md`。
6. raw 只作为临时事实输入层。daily 完整生成、审核并通过 `close-day` 标记为 `closed` 后，7 天后可以运行 `python3 tools/cyberlog.py prune-raw --older-than 7 --apply` 清理，只保留 compiled 和 `_raw-discard-log.md`。

`close-day` 运行前的核心输出 gate：
- `_ai-audit.md`
- `_cyberlog.md`
- `_tomorrow-boot.md`
- `_ai-output-audit.md`

`_ai-feed.md`、`_ai-context.md`、`_ai-request.md` 是 `daily` 生成的投喂中间件，通常应存在，但不是直接 raw 清理 gate。`prune-raw` 只清理 `_run-state.json` 中 `phase == closed` 的日期。

当天有对应状态时还应生成或更新：
- `_conflicts.md`（运行 `python3 tools/cyberlog.py conflict-scan --date YYYY-MM-DD` 后生成）
- `_decisions.yml`（当天有关键决策、状态变化或 supersedes 时必须更新）
- `_comms.yml`（当天有 draft / sent / waiting_for_reply / replied / closed 沟通状态时必须更新）

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
2. 运行 `python3 tools/cyberlog.py weekly --start YYYY-MM-DD --end YYYY-MM-DD`。
3. 把生成的 weekly request 投喂给 AI。
4. 只提取能改变下周行为的结论，不保存流水账总结。

## 我如何沉淀规则

规则必须包含触发条件、执行动作、原因和证据。

只有当规则能减少未来摩擦、降低上下文恢复成本、改善决策质量或减少重复劳动时，才写入 `System/workflow-rules.md`。

## 我如何关闭一天的冲突

1. 先运行 `python3 tools/cyberlog.py daily --date YYYY-MM-DD` 生成 request 和 audit。
2. 完成 `_cyberlog.md`、`_tomorrow-boot.md`、`_ai-output-audit.md` 后，运行 `python3 tools/cyberlog.py conflict-scan --date YYYY-MM-DD`。
3. 审核 `_conflicts.md` 中的 forbidden alias、LPDDR5/LPDDR5X、constraints 冲突；不能当天解决的，必须进入 `_cyberlog.md` 的 Blocked / 未完成任务。
4. 当天新增或改变的跨日决策写入 `_decisions.yml`；如果替代旧决策，必须写 `supersedes`。
5. 沟通稿、邮件、群内同步只要影响项目状态，就在 `_comms.yml` 写明 `draft / sent / waiting_for_reply / replied / closed`。
6. 最后运行 `python3 tools/cyberlog.py decisions --rollup --through YYYY-MM-DD`，更新 `System/decisions-active.md`，作为第二天早上的第一眼视图。
7. 运行 `python3 tools/cyberlog.py validate --date YYYY-MM-DD`；如需留档，使用 `--write` 生成 `_validation.md`。
8. 运行 `python3 tools/cyberlog.py close-day --date YYYY-MM-DD`；无 blocking finding 时会把 `_run-state.json` 标记为 `closed`。

## Daily flow 的定义/执行分离

流程定义固定为：

`daily -> AI output -> conflict-scan -> decisions rollup -> validate -> close-day -> prune/weekly`

每一步的职责边界：
- `_run-state.json`：由 `today`、`daily`、`validate --write`、`close-day` 维护，记录 phase、状态转换、输入 hash 和规则/provenance hash；`prune-raw` 只清理 `closed` 日期。
- `daily`：只组装输入和 audit，不替 AI 做判断。
- `AI output`：生成 `_cyberlog.md`、`_tomorrow-boot.md`、`_ai-output-audit.md`，必须人工审核。
- `conflict-scan`：生成 `_conflicts.md`，把口径冲突从叙述中抽成 gate finding。
- `decisions rollup`：生成 `System/decisions-active.md`，只展示未 frozen / superseded 的决策。
- `validate`：只读校验 schema、AI output contract、conflict gate、decision integrity、comms aging；默认打印，不写文件。
- `close-day`：串起 conflict scan、decision rollup 和 validation；只有无 blocking finding 才关闭当天。
- `weekly`：只读取 compiled 输出和结构化状态，不回读 raw。

如果 `validate --date YYYY-MM-DD` 出现 `blocking`，当天不能视作关闭；必须解决、显式接受，或把它记录为下一天的阻塞。
