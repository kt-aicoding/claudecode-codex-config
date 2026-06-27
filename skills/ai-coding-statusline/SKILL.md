---
name: ai-coding-statusline
description: Configure matching status lines for Claude Code and Codex CLI. Use when the user asks to add, install, update, or standardize AI coding status bars/status lines showing model, reasoning effort, context used, 5-hour limit, weekly limit, and current git branch.
---

# AI Coding Statusline

## Workflow

Configure both tools with the upstream installer:

```bash
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/kt-aicoding/statusline-kit/main/scripts/install.py)"
```

This installs:

- Claude Code `statusLine` command at `~/.kt-aicoding/statusline-kit/kt-statusline`
- Codex CLI `[tui].status_line` in `~/.codex/config.toml`

The target display is:

```text
<model> <effort> · Context <n>% used · 5h <n>% left · weekly <n>% left · <git-branch>
```

Claude Code uses ANSI color warnings: context used turns yellow at 60% and red at 80%; 5h/weekly remaining turns yellow at 40% and red at 20%. Set `KT_STATUSLINE_NO_COLOR=1` to disable color.

After installation, tell the user to restart Claude Code and Codex so both tools reload their config.

## Local Development

When working inside this repository, prefer the local installer while testing changes:

```bash
python3 scripts/install.py
```

Run `python3 -m unittest` before committing changes.
