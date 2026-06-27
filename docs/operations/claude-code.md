# Claude Code

来源：

- Claude Code interactive mode 官方文档：https://code.claude.com/docs/en/interactive-mode
- Claude Code slash commands 官方文档：https://code.claude.com/docs/en/slash-commands
- Claude Code statusLine 官方文档：https://code.claude.com/docs/en/statusline

## 高频快捷键

| 操作 | 快捷键 |
| --- | --- |
| 取消当前输入或生成 | `Ctrl+C` |
| 退出 Claude Code | `Ctrl+D` |
| 切换 plan mode | `Shift+Tab` |
| 编辑上一条消息 | `Esc` |
| 显示/隐藏 todo list | `Ctrl+T` |
| 显示详细输出 | `Ctrl+R` |
| 切换 alt screen | `Ctrl+O` |
| 后台运行长任务时控制 shell | `Ctrl+B` |

## 输入前缀

| 前缀 | 用途 |
| --- | --- |
| `/` | Slash commands |
| `@` | 文件或路径引用 |
| `#` | 记忆/指令相关输入 |
| `!` | Bash mode |

## 常用操作

| 操作 | 命令 |
| --- | --- |
| 继续最近会话 | `claude --continue` |
| 恢复历史会话 | `claude --resume` |
| 使用指定模型 | `claude --model <model>` |
| 打印模式 | `claude -p "<prompt>"` |
| 添加额外目录 | `claude --add-dir <path>` |
| 启用 MCP 调试日志 | `claude --mcp-debug` |

## 状态栏

本项目会配置 Claude Code `statusLine`：

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.kt-aicoding/claudecode-codex-config/kt-statusline claude"
  }
}
```

默认显示：

```text
模型 effort · Context used · 5h left · weekly left · branch
```

可选增强字段：

```bash
export KT_STATUSLINE_SHOW_CWD=1
export KT_STATUSLINE_SHOW_TOKENS=1
export KT_STATUSLINE_SHOW_COST=1
export KT_STATUSLINE_SHOW_VERSION=1
```

颜色关闭：

```bash
export KT_STATUSLINE_NO_COLOR=1
```

## Warp 注意

- Claude Code 文档里提到 `Shift+Enter` 默认适配 Warp 等终端。
- Warp 会导出 `NO_COLOR=1`，但本项目状态栏默认不受它影响。
- 如果快捷键被 Warp 占用，在 Warp Settings 的 Keyboard Shortcuts 里改 Warp 侧绑定。
