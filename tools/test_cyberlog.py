#!/usr/bin/env python3
"""Smoke tests for tools/cyberlog.py.

Run from the my-daily root with:
    python3 tools/test_cyberlog.py
"""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path

import cyberlog


class CyberlogTests(unittest.TestCase):
    def run_cli(self, root: Path, *args: str) -> int:
        return cyberlog.main(["--root", str(root), *args])

    def run_cli_output(self, root: Path, *args: str) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = cyberlog.main(["--root", str(root), *args])
        return result, output.getvalue()

    def test_init_creates_templates_and_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)

            prompt = root / "System" / "ai-sync-prompt.md"
            self.assertTrue(prompt.exists())
            prompt.write_text("KEEP ME\n", encoding="utf-8")

            self.assertEqual(self.run_cli(root, "init"), 0)
            self.assertEqual(prompt.read_text(encoding="utf-8"), "KEEP ME\n")

    def test_today_creates_daily_folders_without_polluting_raw(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)

            old_value = os.environ.get("CYBERLOG_TODAY")
            os.environ["CYBERLOG_TODAY"] = "2026-05-07"
            try:
                result, output = self.run_cli_output(root, "today")
                self.assertEqual(result, 0)
                raw_dir = root / "Daily" / "raw" / "2026-05-07"
                compiled_dir = root / "Daily" / "compiled" / "2026-05-07"
                self.assertTrue(raw_dir.is_dir())
                self.assertTrue(compiled_dir.is_dir())
                self.assertEqual(list(raw_dir.iterdir()), [])
                self.assertIn("Previous boot packet not found", output)

                marker = raw_dir / "04-imported.md"
                marker.write_text("KEEP RAW\n", encoding="utf-8")
                self.assertEqual(self.run_cli(root, "today"), 0)
                self.assertEqual(marker.read_text(encoding="utf-8"), "KEEP RAW\n")
            finally:
                if old_value is None:
                    os.environ.pop("CYBERLOG_TODAY", None)
                else:
                    os.environ["CYBERLOG_TODAY"] = old_value

    def test_today_prints_previous_boot_without_polluting_raw(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)
            previous = root / "Daily" / "compiled" / "2026-05-06"
            previous.mkdir(parents=True)
            (previous / "_tomorrow-boot.md").write_text("boot me\n", encoding="utf-8")

            result, output = self.run_cli_output(root, "today", "--date", "2026-05-07")

            self.assertEqual(result, 0)
            self.assertIn("Previous boot packet: Daily/compiled/2026-05-06/_tomorrow-boot.md", output)
            self.assertIn("boot me", output)
            self.assertEqual(list((root / "Daily" / "raw" / "2026-05-07").iterdir()), [])

    def test_daily_merges_raw_markdown_and_excludes_generated_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)
            raw = root / "Daily" / "raw" / "2026-05-07"
            compiled = root / "Daily" / "compiled" / "2026-05-07"
            raw.mkdir(parents=True)
            compiled.mkdir(parents=True)
            (raw / "00-canvas.md").write_text("canvas\n", encoding="utf-8")
            (raw / "01-imported.md").write_text("raw notes\n", encoding="utf-8")
            (raw / "_generated.md").write_text("generated should be excluded\n", encoding="utf-8")
            chatroom = raw / "chatroom"
            chatroom.mkdir()
            (chatroom / "未命名.md").write_text("chatroom should be excluded\n", encoding="utf-8")

            self.assertEqual(self.run_cli(root, "daily", "--date", "2026-05-07"), 0)

            feed = (compiled / "_ai-feed.md").read_text(encoding="utf-8")
            self.assertIn('<file path="Daily/raw/2026-05-07/00-canvas.md">', feed)
            self.assertIn('<file path="Daily/raw/2026-05-07/01-imported.md">', feed)
            self.assertNotIn("generated should be excluded", feed)
            self.assertNotIn("chatroom should be excluded", feed)
            self.assertLess(feed.index("00-canvas.md"), feed.index("01-imported.md"))

            request = (compiled / "_ai-request.md").read_text(encoding="utf-8")
            self.assertIn("# Cyberlog — 2026-05-07", request)
            self.assertIn("## Codex / Agent 执行模式", request)
            self.assertIn("_ai-output-audit.md", request)
            self.assertIn("canvas", request)

            context = (compiled / "_ai-context.md").read_text(encoding="utf-8")
            self.assertIn("# AI Historical Context - 2026-05-07", context)
            self.assertIn("not today's raw evidence", context)

            audit = (compiled / "_ai-audit.md").read_text(encoding="utf-8")
            self.assertIn("Included source files: 2", audit)
            self.assertIn("Excluded markdown files: 2", audit)
            self.assertIn("Daily/raw/2026-05-07/chatroom/未命名.md", audit)
            self.assertIn("excluded directory `chatroom`", audit)

    def test_daily_adds_historical_context_without_polluting_feed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)
            raw = root / "Daily" / "raw" / "2026-05-08"
            compiled = root / "Daily" / "compiled" / "2026-05-08"
            previous = root / "Daily" / "compiled" / "2026-05-07"
            raw.mkdir(parents=True)
            compiled.mkdir(parents=True)
            previous.mkdir(parents=True)
            (raw / "00-canvas.md").write_text("today raw\n", encoding="utf-8")
            (previous / "_cyberlog.md").write_text("yesterday cyberlog\n", encoding="utf-8")
            (previous / "_tomorrow-boot.md").write_text("yesterday boot\n", encoding="utf-8")

            self.assertEqual(self.run_cli(root, "daily", "--date", "2026-05-08"), 0)

            feed = (compiled / "_ai-feed.md").read_text(encoding="utf-8")
            context = (compiled / "_ai-context.md").read_text(encoding="utf-8")
            request = (compiled / "_ai-request.md").read_text(encoding="utf-8")
            audit = (compiled / "_ai-audit.md").read_text(encoding="utf-8")
            self.assertIn("today raw", feed)
            self.assertNotIn("yesterday cyberlog", feed)
            self.assertIn("yesterday cyberlog", context)
            self.assertIn("yesterday boot", context)
            self.assertIn("## Historical Context", request)
            self.assertIn("不是今天的 raw evidence", request)
            self.assertIn("Included historical context files: 2", audit)

    def test_capture_writes_timestamped_raw_note(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)

            old_now = os.environ.get("CYBERLOG_NOW")
            os.environ["CYBERLOG_NOW"] = "2026-05-07T14:23:00"
            try:
                self.assertEqual(self.run_cli(root, "capture", "quick note"), 0)
                raw = root / "Daily" / "raw" / "2026-05-07"
                first = raw / "1423-capture.md"
                self.assertEqual(first.read_text(encoding="utf-8"), "quick note\n")

                self.assertEqual(self.run_cli(root, "capture", "second note"), 0)
                second = raw / "1423-capture-2.md"
                self.assertEqual(second.read_text(encoding="utf-8"), "second note\n")
            finally:
                if old_now is None:
                    os.environ.pop("CYBERLOG_NOW", None)
                else:
                    os.environ["CYBERLOG_NOW"] = old_now

    def test_prune_raw_dry_run_and_apply_respects_completion_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)

            complete_raw = root / "Daily" / "raw" / "2026-05-01"
            complete_raw.mkdir(parents=True)
            (complete_raw / "note.md").write_text("raw note\n", encoding="utf-8")
            complete_compiled = root / "Daily" / "compiled" / "2026-05-01"
            complete_compiled.mkdir(parents=True)
            for name in ("_ai-audit.md", "_cyberlog.md", "_tomorrow-boot.md", "_ai-output-audit.md"):
                (complete_compiled / name).write_text(f"{name}\n", encoding="utf-8")

            incomplete_raw = root / "Daily" / "raw" / "2026-05-02"
            incomplete_raw.mkdir(parents=True)
            (incomplete_raw / "note.md").write_text("keep me\n", encoding="utf-8")
            incomplete_compiled = root / "Daily" / "compiled" / "2026-05-02"
            incomplete_compiled.mkdir(parents=True)
            (incomplete_compiled / "_cyberlog.md").write_text("not enough\n", encoding="utf-8")

            result, output = self.run_cli_output(root, "prune-raw", "--before", "2026-05-03")
            self.assertEqual(result, 0)
            self.assertIn("Would delete Daily/raw/2026-05-01", output)
            self.assertIn("Skip Daily/raw/2026-05-02", output)
            self.assertTrue(complete_raw.exists())
            self.assertFalse((complete_compiled / "_raw-discard-log.md").exists())

            result, output = self.run_cli_output(root, "prune-raw", "--before", "2026-05-03", "--apply")
            self.assertEqual(result, 0)
            self.assertIn("Deleted Daily/raw/2026-05-01", output)
            self.assertFalse(complete_raw.exists())
            self.assertTrue(incomplete_raw.exists())
            discard_log = complete_compiled / "_raw-discard-log.md"
            self.assertTrue(discard_log.exists())
            log_text = discard_log.read_text(encoding="utf-8")
            self.assertIn("Raw Discard Log - 2026-05-01", log_text)
            self.assertIn("Daily/raw/2026-05-01/note.md", log_text)
            self.assertIn("sha256:", log_text)

    def test_weekly_collects_existing_outputs_and_warns_for_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)

            day1 = root / "Daily" / "compiled" / "2026-05-01"
            day1.mkdir(parents=True)
            (day1 / "_cyberlog.md").write_text("cyberlog day 1\n", encoding="utf-8")
            (day1 / "_tomorrow-boot.md").write_text("boot day 1\n", encoding="utf-8")

            day2 = root / "Daily" / "compiled" / "2026-05-02"
            day2.mkdir(parents=True)
            (day2 / "_cyberlog.md").write_text("cyberlog day 2\n", encoding="utf-8")

            self.assertEqual(
                self.run_cli(root, "weekly", "--start", "2026-05-01", "--end", "2026-05-07"),
                0,
            )

            output = root / "Reviews" / "weekly" / "2026-W19_ai-weekly-request.md"
            self.assertTrue(output.exists())
            text = output.read_text(encoding="utf-8")
            self.assertIn('<file path="Daily/compiled/2026-05-01/_cyberlog.md">', text)
            self.assertIn('<file path="Daily/compiled/2026-05-01/_tomorrow-boot.md">', text)
            self.assertIn('<file path="Daily/compiled/2026-05-02/_cyberlog.md">', text)
            self.assertIn("Missing weekly source: Daily/compiled/2026-05-02/_tomorrow-boot.md", text)
            self.assertIn("Missing daily compiled folder: Daily/compiled/2026-05-03", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
