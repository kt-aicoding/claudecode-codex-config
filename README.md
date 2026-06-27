# statusline-kit

Claude Code 和 Codex CLI 的统一状态栏配置。

## 一句话配置

复制下面这一行运行即可同时配置 Claude Code 和 Codex CLI：

```bash
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/kt-aicoding/statusline-kit/main/scripts/install.py)"
```

配置完成后，重启 Claude Code 和 Codex。

## 状态栏样式

目标效果：

```text
gpt-5.5 high · Context 25% used · 5h 67% left · weekly 71% left · main
```

字段顺序：

```text
模型 effort · Context 已用百分比 · 5h 剩余百分比 · weekly 剩余百分比 · 当前 Git 分支
```

Claude Code 的状态栏会使用 ANSI 颜色做预警：

| 字段 | 绿色 | 黄色 | 红色 |
| --- | --- | --- | --- |
| Context used | `< 60%` | `60-79%` | `>= 80%` |
| 5h / weekly left | `> 40%` | `21-40%` | `<= 20%` |

如果不想显示颜色：

```bash
KT_STATUSLINE_NO_COLOR=1
```

## 会改什么

安装脚本会写入一个本地状态栏命令：

```text
~/.kt-aicoding/statusline-kit/kt-statusline
```

并更新 Claude Code 配置：

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.kt-aicoding/statusline-kit/kt-statusline claude"
  }
}
```

同时更新 Codex CLI 配置：

```toml
[tui]
status_line = [
  "model-with-reasoning",
  "context-used",
  "five-hour-limit",
  "weekly-limit",
  "git-branch",
]
status_line_use_colors = true
```

写入前会自动生成带时间戳的备份文件。

Claude Code 官方 statusLine 支持 ANSI 颜色；Codex CLI 这里使用内置 TUI 状态栏项和 `status_line_use_colors = true`。

## Skill

本仓库内置一个可复制的 Codex Skill：

```text
skills/ai-coding-statusline/SKILL.md
```

这个 Skill 的用途是让 Codex 在用户要求配置 Claude Code / Codex CLI 状态栏时，直接运行本仓库的一句话安装命令。

## 本地开发

克隆仓库后可以用本地脚本安装：

```bash
python3 scripts/install.py
```

运行测试：

```bash
python3 -m unittest
```

## 链接

- Claude Code status line 文档：https://code.claude.com/docs/en/statusline
