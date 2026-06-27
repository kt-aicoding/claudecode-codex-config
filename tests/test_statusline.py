import unittest
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from statusline_kit.cli import (
    format_claude_status,
    is_warp_terminal,
    main,
    should_use_color,
    terminal_summary,
    upsert_codex_config,
    upsert_tui_status_line,
)


class ClaudeStatusTests(unittest.TestCase):
    def test_formats_available_fields(self):
        status = format_claude_status(
            {
                "model": {"display_name": "Claude Sonnet"},
                "effort": {"level": "medium"},
                "context_window": {"used_percentage": 37.5},
                "rate_limits": {
                    "five_hour": {"used_percentage": 12},
                    "seven_day": {"used_percentage": 64},
                },
                "cost": {"total_cost_usd": 0.0214},
            }
        )

        self.assertEqual(
            "Claude Sonnet medium · Context 37.5% used · 5h 88% left · weekly 36% left",
            status,
        )

    def test_tolerates_missing_json_fields(self):
        self.assertEqual("Claude", format_claude_status({}))

    def test_formats_fractional_percentages_and_list_rate_limits(self):
        status = format_claude_status(
            {
                "model": "Claude Sonnet",
                "effort": "high",
                "context_window": {"used_percent": 0.42},
                "rate_limits": [
                    {"name": "5h", "used_percent": 0.25},
                    {"name": "weekly", "used_percent": 0.75},
                ],
            }
        )

        self.assertEqual(
            "Claude Sonnet high · Context 42% used · 5h 75% left · weekly 25% left",
            status,
        )

    def test_colors_claude_risk_segments_when_enabled(self):
        status = format_claude_status(
            {
                "model": "Claude Sonnet",
                "effort": "high",
                "context_window": {"used_percentage": 90},
                "rate_limits": {
                    "five_hour": {"remaining_percentage": 10},
                    "weekly": {"remaining_percentage": 35},
                },
            },
            use_color=True,
        )

        self.assertIn("\033[1mClaude Sonnet high\033[0m", status)
        self.assertIn("\033[31mContext 90% used\033[0m", status)
        self.assertIn("\033[31m5h 10% left\033[0m", status)
        self.assertIn("\033[33mweekly 35% left\033[0m", status)


class CodexConfigTests(unittest.TestCase):
    def test_adds_tui_section_when_missing(self):
        result = upsert_tui_status_line('model = "gpt-5-codex"\n')

        self.assertIn("[tui]", result)
        self.assertIn('"model-with-reasoning"', result)
        self.assertIn('"context-used"', result)
        self.assertIn('"five-hour-limit"', result)
        self.assertIn('"weekly-limit"', result)
        self.assertIn('"git-branch"', result)
        self.assertIn("status_line_use_colors = true", result)

    def test_replaces_status_line_and_preserves_other_tui_keys(self):
        original = """model = "gpt-5-codex"

[tui]
theme = "dark"
status_line = [
  "old",
]
status_line_use_colors = false

[tui.model_availability_nux]
gpt-5-codex = "seen"
"""
        result = upsert_tui_status_line(original)

        self.assertIn('theme = "dark"', result)
        self.assertIn('"model-with-reasoning"', result)
        self.assertNotIn('"old"', result)
        self.assertIn("[tui.model_availability_nux]", result)
        self.assertIn('gpt-5-codex = "seen"', result)

    def test_installs_safe_codex_preferences(self):
        result = upsert_codex_config('model = "gpt-5.5"\n')

        self.assertIn('model = "gpt-5.5"', result)
        self.assertIn('model_reasoning_effort = "xhigh"', result)
        self.assertIn('approval_policy = "on-request"', result)
        self.assertIn('sandbox_mode = "workspace-write"', result)
        self.assertIn("check_for_update_on_startup = false", result)
        self.assertIn('project_doc_fallback_filenames = ["CLAUDE.md", "README.md"]', result)
        self.assertIn("[sandbox_workspace_write]", result)
        self.assertIn("network_access = false", result)
        self.assertIn("[history]", result)
        self.assertIn('persistence = "save-all"', result)
        self.assertIn("[shell_environment_policy]", result)
        self.assertIn('"*TOKEN*"', result)
        self.assertIn("[agents]", result)
        self.assertIn("max_threads = 6", result)
        self.assertIn('[plugins."vercel@openai-curated"]', result)
        self.assertIn("[mcp_servers.context7]", result)
        self.assertIn("[mcp_servers.playwright]", result)

    def test_full_codex_config_preserves_nested_tables(self):
        original = """model = "gpt-5.5"

[tui]
theme = "dark"
status_line = ["old"]

[tui.model_availability_nux]
gpt-5.5 = 1

[plugins."vercel@openai-curated"]
enabled = true
"""
        result = upsert_codex_config(original)

        self.assertIn('theme = "dark"', result)
        self.assertIn("[tui.model_availability_nux]", result)
        self.assertIn("gpt-5.5 = 1", result)
        self.assertIn('[plugins."vercel@openai-curated"]', result)
        self.assertIn("enabled = true", result)


class CliDispatchTests(unittest.TestCase):
    def test_install_claude_dispatch_uses_status_command_arg(self):
        with tempfile.TemporaryDirectory() as tempdir:
            settings = Path(tempdir) / "settings.json"

            code = main(
                [
                    "install-claude",
                    "--settings",
                    str(settings),
                    "--command",
                    "custom-statusline claude",
                ]
            )

            self.assertEqual(0, code)
            self.assertIn("custom-statusline claude", settings.read_text())


class WarpEnvironmentTests(unittest.TestCase):
    def test_detects_warp_terminal(self):
        with patch.dict("os.environ", {"TERM_PROGRAM": "WarpTerminal", "WARP_CLIENT_VERSION": "v1"}, clear=True):
            self.assertTrue(is_warp_terminal())
            self.assertIn("WarpTerminal", terminal_summary())

    def test_no_color_does_not_disable_statusline_colors_in_warp(self):
        with patch.dict("os.environ", {"NO_COLOR": "1", "TERM_PROGRAM": "WarpTerminal"}, clear=True):
            self.assertTrue(should_use_color())

    def test_tool_specific_color_disable_still_works(self):
        with patch.dict("os.environ", {"KT_STATUSLINE_NO_COLOR": "1", "TERM_PROGRAM": "WarpTerminal"}, clear=True):
            self.assertFalse(should_use_color())

    def test_optional_claude_segments_are_env_gated(self):
        payload = {
            "model": "Claude Sonnet",
            "context_window": {
                "used_percentage": 25,
                "total_input_tokens": 1_420_000,
                "total_output_tokens": 49_100,
            },
            "cost": {"total_cost_usd": 0.1234},
            "workspace": {"current_dir": "/tmp/example-project"},
            "version": "1.2.3",
        }
        with patch.dict(
            "os.environ",
            {
                "KT_STATUSLINE_SHOW_CWD": "1",
                "KT_STATUSLINE_SHOW_TOKENS": "1",
                "KT_STATUSLINE_SHOW_COST": "1",
                "KT_STATUSLINE_SHOW_VERSION": "1",
            },
            clear=True,
        ):
            status = format_claude_status(payload)

        self.assertIn("example-project", status)
        self.assertIn("in 1.4M out 49.1K", status)
        self.assertIn("$0.1234", status)
        self.assertIn("cc 1.2.3", status)


if __name__ == "__main__":
    unittest.main()
