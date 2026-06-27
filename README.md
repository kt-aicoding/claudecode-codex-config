# statusline-kit

Status line kit for Claude Code and Codex CLI.

This repository contains the first `kt-aicoding` CLI component: a small, dependency-free helper that makes model, effort, context usage, rate-limit usage, and cost visible in day-to-day AI coding tools.

## What It Does

- Claude Code: installs a `statusLine` command that renders `model | effort | context % | 5h % | 7d % | cost` when those fields are present in the status input.
- Codex CLI: installs a recommended `[tui]` status line configuration using Codex's built-in model/effort, context, 5-hour limit, and weekly limit items.
- Doctor: prints the detected local config paths and command path.

## Install

```bash
git clone https://github.com/kt-aicoding/statusline-kit.git
cd statusline-kit
chmod +x bin/kt-statusline
```

Install Claude Code status line:

```bash
./bin/kt-statusline install-claude
```

Install Codex CLI status line:

```bash
./bin/kt-statusline install-codex
```

Both installers create timestamped backups before writing config files.

## Commands

```bash
./bin/kt-statusline claude
./bin/kt-statusline install-claude
./bin/kt-statusline install-codex
./bin/kt-statusline doctor
```

## Preview

```bash
printf '{"model":{"display_name":"Claude Sonnet"},"effort":{"level":"medium"},"context_window":{"used_percentage":37.5},"rate_limits":{"five_hour":{"used_percentage":12},"seven_day":{"used_percentage":64}},"cost":{"total_cost_usd":0.0214}}' \
  | ./bin/kt-statusline claude
```

Example output:

```text
Claude Sonnet | effort medium | context 37.5% | 5h 12% | 7d 64% | $0.0214
```

## Claude Code Config

`install-claude` writes this shape into `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "/absolute/path/to/bin/kt-statusline claude"
  }
}
```

Claude Code sends session data to the command over stdin. The renderer is intentionally defensive and only displays fields that are present.

## Codex CLI Config

`install-codex` writes this block into `~/.codex/config.toml`:

```toml
[tui]
status_line = [
  "model-with-reasoning",
  "context-used",
  "five-hour-limit",
  "weekly-limit",
]
status_line_use_colors = true
```

If `[tui]` already exists, only `status_line` and `status_line_use_colors` are replaced. Other keys in the section are preserved.

Codex CLI currently exposes model/effort, context, 5-hour usage, and weekly usage as built-in status line items. This kit does not add a custom Codex cost renderer because Codex status lines are configured from built-in TUI items.

## Development

Run tests with the standard library:

```bash
python3 -m unittest
```

## Links

- Chinese README: [README.zh-CN.md](README.zh-CN.md)
- Claude Code status line docs: https://code.claude.com/docs/en/statusline
