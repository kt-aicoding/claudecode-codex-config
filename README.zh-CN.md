# cc-codex-config

我的 Claude Code（cc）和 Codex CLI 配置仓库：状态栏、偏好、可复制 Skill、安装脚本和可审计配置片段。

这个仓库不再只定位为 `statusline` 工具。状态栏是第一个模块，后续所有和 cc / Codex 相关的安全配置、个人偏好、Skill、MCP、profile 模板都放在这里统一维护。

## 一句话配置

复制下面这一行运行即可同时配置 Claude Code 和 Codex CLI：

```bash
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/kt-aicoding/cc-codex-config/main/scripts/install.py)"
```

配置完成后，重启 Claude Code 和 Codex。

## 当前会配置什么

### Warp 终端

- 自动检测 Warp 环境：`TERM_PROGRAM=WarpTerminal` 或 `WARP_*` 环境变量。
- Claude Code 状态栏颜色不会被 Warp 默认导出的 `NO_COLOR=1` 关闭。
- 如需关闭本工具颜色，只设置 `KT_STATUSLINE_NO_COLOR=1`。
- 额外说明见 [configs/warp/README.md](configs/warp/README.md)。

### Claude Code

- 安装本地状态栏命令：`~/.kt-aicoding/cc-codex-config/kt-statusline`
- 写入 `~/.claude/settings.json` 的 `statusLine`
- 状态栏支持 ANSI 颜色预警

### Codex CLI

- 写入 `[tui].status_line`
- 开启 `status_line_use_colors`
- 写入安全的通用偏好：
  - `model = "gpt-5.5"`
  - `model_reasoning_effort = "xhigh"`
  - `model_verbosity = "medium"`
  - `review_model = "gpt-5.5"`
  - `approval_policy = "on-request"`
  - `sandbox_mode = "workspace-write"`
  - `check_for_update_on_startup = false`
  - `project_doc_fallback_filenames = ["CLAUDE.md", "README.md"]`
  - `project_doc_max_bytes = 100000`
  - `tool_output_token_limit = 40000`
  - `[sandbox_workspace_write]` 默认禁用网络并排除临时目录
  - `[history]` 保存历史
  - `[shell_environment_policy]` 过滤 token / secret / key / password
  - `[agents]` 设置并发和运行时间上限
  - 常用 OpenAI curated plugins：Vercel、Supabase、Build Web Apps、Expo
  - 常用 MCP servers：context7、playwright

写入前会自动生成带时间戳的备份文件。

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

## 仓库结构

```text
configs/                         可公开审计的配置片段
configs/claude/                  Claude Code 配置片段
configs/codex/                   Codex CLI 配置片段
configs/warp/                    Warp 终端使用建议
configs/codex/profiles/          Codex profile 模板
docs/related-projects.md         相关项目调研和取舍
scripts/install.py               一句话安装脚本
skills/ai-coding-config/         可复制的 Codex Skill
src/statusline_kit/              Claude Code 状态栏渲染器和本地 CLI
```

### Claude Code 可选状态栏字段

默认状态栏保持短。如果需要临时显示更多信息，可以在启动 Claude Code 前设置：

```bash
export KT_STATUSLINE_SHOW_CWD=1
export KT_STATUSLINE_SHOW_TOKENS=1
export KT_STATUSLINE_SHOW_COST=1
export KT_STATUSLINE_SHOW_VERSION=1
```

这些字段只影响 Claude Code 的本地 statusLine 渲染器，不影响 Codex CLI 内置状态栏。

## Skill

本仓库内置一个可复制的 Codex Skill：

```text
skills/ai-coding-config/SKILL.md
```

这个 Skill 的用途是让 Codex 在用户要求配置 Claude Code / Codex CLI 偏好、状态栏或通用 AI Coding 环境时，直接运行本仓库的一句话安装命令。

## 安全边界

这个仓库只提交可公开配置：

- 不提交 API token、密钥、供应商鉴权配置。
- 不提交个人机器上的项目 trust 列表。
- 不提交包含私有路径或敏感业务上下文的配置。
- 安装脚本优先做增量写入和备份，不直接覆盖整个配置文件。

## 本地开发

克隆仓库后可以用本地脚本安装：

```bash
python3 scripts/install.py
```

运行测试：

```bash
python3 -m unittest
```

检查当前终端和配置路径：

```bash
./bin/kt-aicoding-config doctor
```

## 链接

- Claude Code status line 文档：https://code.claude.com/docs/en/statusline
