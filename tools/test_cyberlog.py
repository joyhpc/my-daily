#!/usr/bin/env python3
"""Smoke tests for tools/cyberlog.py.

Run from the my-daily root with:
    python tools/test_cyberlog.py
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

import cyberlog


class CyberlogTests(unittest.TestCase):
    def run_cli(self, root: Path, *args: str) -> int:
        return cyberlog.main(["--root", str(root), *args])

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
                self.assertEqual(self.run_cli(root, "today"), 0)
                raw_dir = root / "Daily" / "raw" / "2026-05-07"
                compiled_dir = root / "Daily" / "compiled" / "2026-05-07"
                self.assertTrue(raw_dir.is_dir())
                self.assertTrue(compiled_dir.is_dir())
                self.assertEqual(list(raw_dir.iterdir()), [])

                marker = raw_dir / "04-imported.md"
                marker.write_text("KEEP RAW\n", encoding="utf-8")
                self.assertEqual(self.run_cli(root, "today"), 0)
                self.assertEqual(marker.read_text(encoding="utf-8"), "KEEP RAW\n")
            finally:
                if old_value is None:
                    os.environ.pop("CYBERLOG_TODAY", None)
                else:
                    os.environ["CYBERLOG_TODAY"] = old_value

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
            self.assertIn("canvas", request)

            audit = (compiled / "_ai-audit.md").read_text(encoding="utf-8")
            self.assertIn("Included source files: 2", audit)
            self.assertIn("Excluded markdown files: 2", audit)
            self.assertIn("Daily/raw/2026-05-07/chatroom/未命名.md", audit)
            self.assertIn("excluded directory `chatroom`", audit)

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
