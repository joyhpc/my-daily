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
        _ai-request.md
        _cyberlog.md
        _tomorrow-boot.md
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
    weekly-review-prompt.md
    personal-operating-manual.md
    workflow-rules.md
  tools/
    cyberlog.py
  cyberlog.config.json
  README-cyberlog.md
```

## 核心原则

- 原始 notes 永不覆盖。
- AI 生成内容和原始内容分开。
- 所有 AI 生成文件使用 `_` 开头。
- 生成 daily feed 时会排除 `_` 开头的 markdown，避免把 AI 输出再次喂回去。
- 当前系统不直接调用 OpenAI API，但 Codex/agent 看到 `_ai-request.md` 时默认应完整处理并落盘结果。

## 初始化

在 my-daily 根目录运行：

```bash
python tools/cyberlog.py init
```

该命令会创建必要目录和模板文件。已有模板默认不会覆盖。需要重置模板时运行：

```bash
python tools/cyberlog.py init --force
```

## 每天怎么用

早上或开始工作前创建今天的 Daily 工作画布：

```bash
python tools/cyberlog.py today
```

它会创建：

- `Daily/raw/YYYY-MM-DD/`
- `Daily/compiled/YYYY-MM-DD/`

`today` 不会往当天 raw 目录写入任何模板文件，避免污染原始输入区。

白天继续按原来的习惯自由写 markdown。建议分两类放：

- `Daily/raw/YYYY-MM-DD/`：当天原始输入文件，只放你写入或导入的原始 markdown。
- `Daily/templates/`：可复制模板，不参与 daily 合并。

你可以新增任意非 `_` 开头的 `.md` 文件，例如 `04-meeting.md`、`05-debug.md`、`06-idea.md`。

晚上生成 AI request：

```bash
python tools/cyberlog.py daily --date 2026-05-07
```

它会生成：

- `Daily/compiled/2026-05-07/_ai-feed.md`
- `Daily/compiled/2026-05-07/_ai-request.md`
- `Daily/compiled/2026-05-07/_ai-audit.md`

## 默认完整处理

`_ai-request.md` 是给 AI 的任务包，不是整理结果。默认完成标准不是“生成 request”，而是当天目录里同时存在：

- `_ai-feed.md`
- `_ai-request.md`
- `_ai-audit.md`
- `_cyberlog.md`
- `_tomorrow-boot.md`
- `_ai-output-audit.md`

你可以用两种方式触发完整处理：

1. 在聊天窗口里打开当天的 `_ai-request.md`，复制全部内容，粘贴给 AI。
2. 在 Codex 工作区里直接说：`处理 Daily/compiled/YYYY-MM-DD/_ai-request.md，并保存 _cyberlog.md 和 _tomorrow-boot.md`。

如果 AI/Codex 有文件写入能力，它应该直接保存：

- `Daily/compiled/YYYY-MM-DD/_cyberlog.md`
- `Daily/compiled/YYYY-MM-DD/_tomorrow-boot.md`
- `Daily/compiled/YYYY-MM-DD/_ai-output-audit.md`

只有在 AI 没有文件写入能力时，才把结果完整输出到聊天窗口，由你手动保存。`_cyberlog.md` 保存完整日终整理，`_tomorrow-boot.md` 只保存明天启动包。

当前脚本不自动调用 AI API。这样可以避免 API key、费用、模型选择和自动覆盖结果的问题。`_ai-audit.md` 用来先审核任务包边界，真正的 AI 输出仍应在保存前过一遍人工检查。

`_ai-output-audit.md` 用于记录 AI 输出是否误读草稿状态、是否混入被排除目录、是否把推断升级成事实。

## 每周怎么用

周复盘只读取每天已经整理后的 `_cyberlog.md` 和 `_tomorrow-boot.md`，不会读取原始 daily notes。

```bash
python tools/cyberlog.py weekly --start 2026-05-01 --end 2026-05-07
```

它会生成类似：

```text
Reviews/weekly/2026-W19_ai-weekly-request.md
```

缺失的 `_cyberlog.md` 或 `_tomorrow-boot.md` 会作为 warning 写入 request，不会导致命令失败。

## 为什么不要覆盖原始 notes

原始 notes 是真实工作轨迹。它们保留了当时的混乱、上下文、误判、阻塞和决策过程。AI 输出是整理层，只能生成 `_` 开头的文件。如果让 AI 覆盖原始 notes，会污染事实来源，也会让后续分析无法判断哪些内容是真实记录、哪些是模型重写。

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

`today` 当前使用本机本地日期。`timezone` 字段暂时只是配置记录，脚本不会强制切换时区。

`weekly_week_basis` 默认是 `end`，因此 `2026-05-01` 到 `2026-05-07` 会生成 `2026-W19_ai-weekly-request.md`。如果你希望严格按 start 日期计算周号，可以改成 `start`。

## 命令速查

```bash
python tools/cyberlog.py init
python tools/cyberlog.py today
python tools/cyberlog.py daily --date 2026-05-07
python tools/cyberlog.py weekly --start 2026-05-01 --end 2026-05-07
```

如果你不在 my-daily 根目录运行，可以指定 root：

```bash
python /path/to/my-daily/tools/cyberlog.py --root /path/to/my-daily daily --date 2026-05-07
```

## 手动测试步骤

1. 运行 `python tools/cyberlog.py init`，确认模板创建。
2. 修改一个模板文件，再运行 `python tools/cyberlog.py init`，确认不会覆盖。
3. 运行 `python tools/cyberlog.py today`，确认今天的 Daily 文件夹和默认文件存在。
4. 在 `Daily/raw/YYYY-MM-DD/` 目录写入一个原始文件，并在 `Daily/compiled/YYYY-MM-DD/` 写入 `_cyberlog.md`，运行 `daily`，确认 `_ai-feed.md` 只包含 raw 中非 `_` 开头文件，且默认排除 `chatroom/`。
5. 检查 `_ai-feed.md` 中是否有 `<file path="...">` 文件边界。
6. 检查 `_ai-audit.md` 中的 included/excluded 文件清单和 prompt/request 检查。
7. 准备几天的 `_cyberlog.md` 和 `_tomorrow-boot.md`，运行 `weekly`，确认会收集存在的文件。
8. 删除某天的 `_tomorrow-boot.md` 后再运行 `weekly`，确认输出 warning 而不是失败。

也可以运行内置测试：

```bash
python tools/test_cyberlog.py
```

## 常见问题

### daily 提示 Daily 日期文件夹不存在

先运行 `python tools/cyberlog.py today` 创建今天目录，或手动创建 `Daily/raw/YYYY-MM-DD/`。

### daily 提示没有可合并的原始 md 文件

当天目录里只有 `_` 开头的生成文件，或没有 `.md` 文件。新增至少一个非 `_` 开头的 markdown。

### weekly 为什么不读取原始 notes

周复盘分析的是已经整理后的工作流状态，不应该重新吸入原始草稿。这样可以降低噪音，也避免把 AI 输出和原始内容混在同一层。

### AI 输出要不要自动写回文件

当前版本不自动调用 API，也不自动解析 AI 输出。建议先手动保存，保证你能审核内容质量。
