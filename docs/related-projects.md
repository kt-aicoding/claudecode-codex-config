# 相关项目与取舍

本项目定位为个人 cc / Codex 配置仓库，不追求做通用状态栏生态。

## 已参考的方向

### Claude Code statusLine

Claude Code 官方支持通过 `settings.json` 的 `statusLine` 运行本地命令，并向命令 stdin 传入会话 JSON。官方也支持 ANSI 颜色输出。

参考：https://code.claude.com/docs/en/statusline

本项目采用：

- 无依赖 Python 渲染器。
- 默认显示模型、effort、context、5h、weekly、Git 分支。
- Claude Code 独有 ANSI 风险颜色。
- Warp 下忽略通用 `NO_COLOR`，只用 `KT_STATUSLINE_NO_COLOR` 关闭本工具颜色。

### Claude Code 社区状态栏

社区常见做法会展示 token、cost、目录、git 信息，有些项目会依赖 `jq`、`ccusage`、npm 包或 shell pipeline。

本项目取舍：

- 默认不展示 token/cost/cwd，保持 Warp 状态栏短。
- 提供环境变量开关：
  - `KT_STATUSLINE_SHOW_CWD=1`
  - `KT_STATUSLINE_SHOW_TOKENS=1`
  - `KT_STATUSLINE_SHOW_COST=1`
  - `KT_STATUSLINE_SHOW_VERSION=1`
- 不引入 jq / npm / ccusage 作为运行时依赖。

### Codex CLI config

Codex CLI 当前使用内置 `[tui].status_line` 项；外部命令式 status line 不是稳定配置面。

参考：https://github.com/openai/codex/blob/main/docs/config.md

本项目采用：

- 只写入 Codex 已有的内置 status line 项。
- 不尝试为 Codex 注入自定义外部 status line 命令。
- 使用 profile 模板保存轻量可选配置。

### Warp

Warp 会导出 `TERM_PROGRAM=WarpTerminal`、`WARP_*` 以及常见的 `NO_COLOR=1`。

参考：https://docs.warp.dev/knowledge-and-collaboration/warp-drive/environment-variables/

本项目采用：

- `doctor` 和安装脚本检测 Warp。
- 文档说明 Warp 下颜色策略。
- Claude Code 状态栏颜色不被 `NO_COLOR=1` 关闭。

## 不放进仓库的内容

- API token、provider key、OAuth token。
- 私有项目 trust 列表。
- 特定机器路径。
- 大段私有开发者指令。

## 后续候选

- 把常用 prompt / profile 拆成更细的 `configs/codex/profiles/*.config.toml`。
- 增加本地导入命令，把当前配置中的安全项同步回 `configs/`。
- 如果 Codex 将来支持外部 status line command，再统一 cc / Codex 的渲染器。
