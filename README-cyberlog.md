# Daily Cyberlog / 工作画布 AI Sync 系统

这个系统把 Obsidian Daily 文件夹里的原始 markdown 合并成 AI 投喂包，并生成固定 prompt。它的目标不是改变白天的记录习惯，而是在一天结束时把工作画布、事件流、决策、阻塞、任务和自我迭代信号整理成可复用资产。

## 文件结构

```text
my-daily/
  Daily/
    raw/
      2026-05-07/
        04-imported.md
    compiled/
      2026-05-07/
        _ai-feed.md
        _ai-context.md
        _ai-request.md
        _ai-audit.md
        _run-state.json
        _cyberlog.md
        _tomorrow-boot.md
        _ai-output-audit.md
        _conflicts.md
        _validation.md
        _decisions.yml
        _comms.yml
    templates/
        00-canvas.md
        01-notes.md
        02-research.md
        03-agent.md
  Reviews/
    weekly/
      2026-W19_ai-weekly-request.md
  System/
    ai-sync-prompt.md
    projects.yml
    schemas.md
    decisions-active.md
    weekly-review-prompt.md
    personal-operating-manual.md
    workflow-rules.md
  tools/
    cyberlog.py
    cyberlog_core/
      cli.py
      app.py
      constants.py
      models.py
      templates.py
  cyberlog.config.json
  README-cyberlog.md
```

## 核心原则

- raw 在保留期内不覆盖，完整整理并审核 7 天后可清理。
- AI 生成内容和原始内容分开。
- 所有 AI 生成文件使用 `_` 开头。
- 生成 daily feed 时会排除 `_` 开头的 markdown，避免把 AI 输出再次喂回去。
- 当前系统不直接调用 OpenAI API，但 Codex/agent 看到 `_ai-request.md` 时默认应完整处理并落盘结果。
- 本仓库只作为 daily 内容维护和 AI 整理的底层数据，不作为项目工作空间、采购资料库、设计证据库或正式交付资料库。

## 代码结构

- `tools/cyberlog.py`：薄 CLI wrapper，只负责调用 runtime。
- `tools/cyberlog_core/cli.py`：参数解析和命令分发。
- `tools/cyberlog_core/app.py`：daily、validate、close-day、weekly、prune 等运行时命令实现。
- `tools/cyberlog_core/templates.py`：`init` 会落盘的内置 prompt / README / schema 模板。
- `tools/cyberlog_core/models.py`：共享 dataclass 模型。
- `tools/cyberlog_core/constants.py`：小型运行常量和默认配置。

## 初始化

在 my-daily 根目录运行：

```bash
python3 tools/cyberlog.py init
```

该命令会创建必要目录和模板文件。已有模板默认不会覆盖。需要重置模板时运行：

```bash
python3 tools/cyberlog.py init --force
```

## 每天怎么用

早上或开始工作前创建今天的 Daily 工作画布：

```bash
python3 tools/cyberlog.py today
```

它会创建：

- `Daily/raw/YYYY-MM-DD/`
- `Daily/compiled/YYYY-MM-DD/`

`today` 不会往当天 raw 目录写入任何模板文件，避免污染原始输入区。

如果昨天存在 `Daily/compiled/<昨天>/_tomorrow-boot.md`，`today` 会直接打印这份启动包，但不会复制到当天 raw 目录。这样昨天的 AI 输出只作为晨间启动提示，不会混入今天的原始事实来源。

白天继续按原来的习惯自由写 markdown。建议分两类放：

- `Daily/raw/YYYY-MM-DD/`：当天原始输入文件，只放你写入或导入的原始 markdown。
- `Daily/templates/`：可复制模板，不参与 daily 合并。

你可以新增任意非 `_` 开头的 `.md` 文件，例如 `04-meeting.md`、`05-debug.md`、`06-idea.md`。

也可以用 `capture` 快速记录一条 raw note：

```bash
python3 tools/cyberlog.py capture "跟进 A38 LPDDR5 供应商正式回复"
python3 tools/cyberlog.py capture --type blocker --project A38-DF108-Agilex5 "等待 FAE 确认 SmartVID regulator"
python3 tools/cyberlog.py capture --type sent --project A38-DF108-Agilex5 --sent-to FAE --subject "SmartVID 问题清单" --waiting-for "regulator confirmation" "已发送 FAE 问题清单"
printf "会议结论..." | python3 tools/cyberlog.py capture
```

`capture` 会写入 `Daily/raw/YYYY-MM-DD/HHMM-capture.md`。结构化类型会写入 `HHMM-<type>.md`，并带 front matter：`type`、`project`、`trust`、`sent_to`、`subject`、`waiting_for` 等。`daily` 生成 `_ai-feed.md` 时会把这些字段暴露在 `<file ...>` 标签上，帮助 AI 区分事实、草稿、发送、阻塞和普通 note。如果同一分钟已经存在文件，会自动使用 `-2` 后缀，不会覆盖已有 raw note。

`Daily/raw/` 适合保存工作状态、事实摘要、决策、阻塞、下一步和外部资料位置。不适合保存原厂邮件全文、报价、联系人、NDA/商务条款、正式设计源文件、项目交付物或需要长期受控归档的证据材料。这些内容应放在对应的邮箱、采购系统、项目资料库或受控工作空间；daily 中只保留可用于恢复上下文的脱敏摘要。

晚上生成 AI request：

```bash
python3 tools/cyberlog.py daily --date 2026-05-07
```

它会生成：

- `Daily/compiled/2026-05-07/_ai-feed.md`
- `Daily/compiled/2026-05-07/_ai-context.md`
- `Daily/compiled/2026-05-07/_ai-request.md`
- `Daily/compiled/2026-05-07/_ai-audit.md`
- `Daily/compiled/2026-05-07/_run-state.json`

`_ai-feed.md` 只包含当天 raw 目录中非 `_` 开头的 markdown。`_ai-context.md` 单独保存跨日上下文：昨天的 `_cyberlog.md` 和最近 3 天的 `_tomorrow-boot.md`。这些内容只用于识别连续任务和重复 blocker，不作为今天的 raw evidence。

如果存在 `System/projects.yml`，`daily` 会把它作为 `Project Registry` 注入 `_ai-request.md`。AI 输出应按 project id 分章节，并用 aliases / forbidden_aliases / constraints 做项目口径校验。

## 默认完整处理

`_ai-request.md` 是给 AI 的任务包，不是整理结果。`daily` 生成的 request package 包含：

- `_ai-feed.md`
- `_ai-context.md`
- `_ai-request.md`
- `_ai-audit.md`

这些是投喂与审计中间件，不是长期 daily record。`close-day` 运行前的核心输出 gate 是当天目录里同时存在：

- `_ai-audit.md`
- `_cyberlog.md`
- `_tomorrow-boot.md`
- `_ai-output-audit.md`

这 4 个文件表示：输入包已审计、AI 输出已落盘、明日启动包已生成、输出边界已自检。`_ai-feed.md`、`_ai-context.md`、`_ai-request.md` 通常也会存在，但不直接作为 raw 清理 gate。`prune-raw` 现在要求 `_run-state.json` 的 `phase` 为 `closed`，因此应先运行 `close-day`。

你可以用两种方式触发完整处理：

1. 在聊天窗口里打开当天的 `_ai-request.md`，复制全部内容，粘贴给 AI。
2. 在 Codex 工作区里直接说：`处理 Daily/compiled/YYYY-MM-DD/_ai-request.md，并保存 _cyberlog.md 和 _tomorrow-boot.md`。

如果 AI/Codex 有文件写入能力，它应该直接保存：

- `Daily/compiled/YYYY-MM-DD/_cyberlog.md`
- `Daily/compiled/YYYY-MM-DD/_tomorrow-boot.md`
- `Daily/compiled/YYYY-MM-DD/_ai-output-audit.md`

之后运行：

```bash
python3 tools/cyberlog.py conflict-scan --date YYYY-MM-DD
python3 tools/cyberlog.py decisions --rollup --through YYYY-MM-DD
python3 tools/cyberlog.py validate --date YYYY-MM-DD --write
python3 tools/cyberlog.py close-day --date YYYY-MM-DD
```

`conflict-scan` 会生成 `_conflicts.md`，先做静态口径检查：forbidden aliases、LPDDR5/LPDDR5X 共现、项目 constraints 冲突。`decisions --rollup` 会读取每天的 `_decisions.yml`，更新 `System/decisions-active.md`。`validate` 默认只读打印 gate 结果；需要落盘时加 `--write` 生成 `_validation.md`，需要 CI/脚本遇到 blocking 直接失败时加 `--strict`。`close-day` 会串起 conflict scan、decision rollup 和 validation；只有没有 blocking finding 时，才把 `_run-state.json` 标记为 `closed`。

`today`、`daily`、`validate --write` 和 `close-day` 会维护 `_run-state.json`。它记录当前 phase、状态转换、输入 raw 文件 hash，以及 prompt / workflow rules / projects / schemas / config 的 provenance hash。`prune-raw` 只清理 `phase == closed` 的日期。

如果当天有跨日决策或沟通状态变化，建议补：

- `Daily/compiled/YYYY-MM-DD/_decisions.yml`
- `Daily/compiled/YYYY-MM-DD/_comms.yml`

只有在 AI 没有文件写入能力时，才把结果完整输出到聊天窗口，由你手动保存。`_cyberlog.md` 保存完整日终整理，`_tomorrow-boot.md` 只保存明天启动包。

当前脚本不自动调用 AI API。这样可以避免 API key、费用、模型选择和自动覆盖结果的问题。`_ai-audit.md` 用来先审核任务包边界，真正的 AI 输出仍应在保存前过一遍人工检查。

`_ai-output-audit.md` 用于记录 AI 输出是否误读草稿状态、是否混入被排除目录、是否把推断升级成事实。

## 每周怎么用

周复盘只读取每天已经整理后的 compiled 输出，不会读取原始 daily notes。它会优先收集 `_cyberlog.md` 和 `_tomorrow-boot.md`，如果存在 `_decisions.yml`、`_comms.yml`、`_conflicts.md`，也会一起放入 weekly request。

```bash
python3 tools/cyberlog.py weekly --start 2026-05-01 --end 2026-05-07
```

它会生成类似：

```text
Reviews/weekly/2026-W19_ai-weekly-request.md
```

缺失的 `_cyberlog.md` 或 `_tomorrow-boot.md` 会作为 warning 写入 request，不会导致命令失败。

## 为什么 raw 可清理但不能覆盖

raw 是真实工作轨迹的短期输入层。它保留当时的混乱、上下文、误判、阻塞和决策过程，方便当天整理和短期纠错。AI 输出是整理层，只能生成 `_` 开头的文件，不能覆盖 raw。daily 完整生成并人工审核后，raw 不再作为永久记录；7 天后可以清理，只保留 compiled 和 `_raw-discard-log.md`。

## 配置

默认配置在 `cyberlog.config.json`：

```json
{
  "daily_root": "Daily",
  "daily_raw_root": "Daily/raw",
  "daily_compiled_root": "Daily/compiled",
  "daily_templates_root": "Daily/templates",
  "system_root": "System",
  "reviews_root": "Reviews/weekly",
  "generated_prefix": "_",
  "daily_exclude_dirs": ["chatroom"],
  "timezone": "local",
  "raw_retention_days": 7,
  "weekly_week_basis": "end"
}
```

常见修改：

- Daily 文件夹不叫 `Daily`：修改 `daily_root`。
- 原始输入区不叫 `Daily/raw`：修改 `daily_raw_root`。
- 编译输出区不叫 `Daily/compiled`：修改 `daily_compiled_root`。
- 模板区不叫 `Daily/templates`：修改 `daily_templates_root`。
- System 文件夹不叫 `System`：修改 `system_root`。
- 周复盘输出目录不叫 `Reviews/weekly`：修改 `reviews_root`。
- 生成文件前缀不想用 `_`：修改 `generated_prefix`。
- 不想把讨论草稿目录喂给 AI：修改 `daily_exclude_dirs`，默认排除 `chatroom`。
- raw 想保留更久或更短：修改 `raw_retention_days`。

`today` 和 `capture` 当前使用本机本地日期。需要指定日期时可以使用 `--date YYYY-MM-DD`。`timezone` 字段暂时只是配置记录，脚本不会强制切换时区。

`raw_retention_days` 默认是 `7`。raw 是临时事实输入层，不是永久记录层。当天完整生成、通过 `close-day` 标记为 `closed` 后，raw 可以在保留期之后用 `prune-raw` 清理；系统会在 compiled 目录保留 `_raw-discard-log.md`。

`weekly_week_basis` 默认是 `end`，因此 `2026-05-01` 到 `2026-05-07` 会生成 `2026-W19_ai-weekly-request.md`。如果你希望严格按 start 日期计算周号，可以改成 `start`。

## 命令速查

```bash
python3 tools/cyberlog.py init
python3 tools/cyberlog.py today
python3 tools/cyberlog.py capture "quick note"
python3 tools/cyberlog.py capture --type todo --project cyberlog-workflow "补 validate 引用追溯"
python3 tools/cyberlog.py daily --date 2026-05-07
python3 tools/cyberlog.py conflict-scan --date 2026-05-07
python3 tools/cyberlog.py decisions --rollup --through 2026-05-07
python3 tools/cyberlog.py validate --date 2026-05-07 --write
python3 tools/cyberlog.py close-day --date 2026-05-07
python3 tools/cyberlog.py prune-raw --older-than 7
python3 tools/cyberlog.py prune-raw --older-than 7 --apply
python3 tools/cyberlog.py weekly --start 2026-05-01 --end 2026-05-07
```

如果你不在 my-daily 根目录运行，可以指定 root：

```bash
python3 /path/to/my-daily/tools/cyberlog.py --root /path/to/my-daily daily --date 2026-05-07
```

## 手动测试步骤

1. 运行 `python3 tools/cyberlog.py init`，确认模板创建。
2. 修改一个模板文件，再运行 `python3 tools/cyberlog.py init`，确认不会覆盖。
3. 运行 `python3 tools/cyberlog.py today`，确认今天的 Daily 文件夹存在，并在昨天 `_tomorrow-boot.md` 存在时打印启动包。
4. 在 `Daily/raw/YYYY-MM-DD/` 目录写入一个原始文件，并在 `Daily/compiled/YYYY-MM-DD/` 写入 `_cyberlog.md`，运行 `daily`，确认 `_ai-feed.md` 只包含 raw 中非 `_` 开头文件，且默认排除 `chatroom/`。
5. 检查 `_ai-context.md` 只包含历史 compiled 输出，并和 `_ai-feed.md` 分开。
6. 检查 `_ai-feed.md` 中是否有 `<file path="...">` 文件边界。
7. 检查 `_ai-audit.md` 中的 included/excluded 文件清单、historical context 清单和 prompt/request 检查。
8. 运行 `conflict-scan --date YYYY-MM-DD`，确认会生成 `_conflicts.md` 并列出 forbidden alias / LPDDR5X 等静态冲突。
9. 准备 `_decisions.yml` 后运行 `decisions --rollup --through YYYY-MM-DD`，确认会生成 `System/decisions-active.md`。
10. 运行 `validate --date YYYY-MM-DD`，确认会打印 schema、AI output contract、conflict gate、decision integrity 和 comms aging 检查。
11. 运行 `close-day --date YYYY-MM-DD`，确认无 blocking 时 `_run-state.json` 进入 `closed`。
12. 运行 `prune-raw --older-than 7`，确认默认只预览；再用临时目录测试 `--apply` 只会删除 `phase == closed` 的 raw 并写 `_raw-discard-log.md`。
13. 准备几天的 `_cyberlog.md` 和 `_tomorrow-boot.md`，运行 `weekly`，确认会收集存在的文件。
14. 删除某天的 `_tomorrow-boot.md` 后再运行 `weekly`，确认输出 warning 而不是失败。

也可以运行内置测试：

```bash
python3 tools/test_cyberlog.py
```

## 常见问题

### daily 提示 Daily 日期文件夹不存在

先运行 `python3 tools/cyberlog.py today` 创建今天目录，或手动创建 `Daily/raw/YYYY-MM-DD/`。

### daily 提示没有可合并的原始 md 文件

当天目录里只有 `_` 开头的生成文件，或没有 `.md` 文件。新增至少一个非 `_` 开头的 markdown。

### weekly 为什么不读取原始 notes

周复盘分析的是已经整理后的工作流状态，不应该重新吸入原始草稿。这样可以降低噪音，也避免把 AI 输出和原始内容混在同一层。

### AI 输出要不要自动写回文件

当前版本不自动调用 API，也不自动解析 AI 输出。建议先手动保存，保证你能审核内容质量。
