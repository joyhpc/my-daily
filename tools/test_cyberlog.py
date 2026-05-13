#!/usr/bin/env python3
"""Smoke tests for tools/cyberlog.py.

Run from the my-daily root with:
    python3 tools/test_cyberlog.py
"""

from __future__ import annotations

import contextlib
import io
import json
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
            projects = root / "System" / "projects.yml"
            schemas = root / "System" / "schemas.md"
            taxonomy = root / "System" / "error-taxonomy.md"
            monthly_prompt = root / "System" / "monthly-review-prompt.md"
            self.assertTrue(prompt.exists())
            self.assertTrue(projects.exists())
            self.assertTrue(schemas.exists())
            self.assertTrue(taxonomy.exists())
            self.assertTrue(monthly_prompt.exists())
            self.assertTrue((root / "Reviews" / "monthly").is_dir())
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
                run_state = json.loads((compiled_dir / "_run-state.json").read_text(encoding="utf-8"))
                self.assertEqual(run_state["phase"], "open")
                self.assertEqual(run_state["transitions"][0]["by"], "today")

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
            self.assertIn("## Project Registry", request)
            self.assertIn("cyberlog-workflow", request)
            self.assertIn("_ai-output-audit.md", request)
            self.assertIn("canvas", request)
            self.assertNotIn("chatroom should be excluded", request)
            self.assertNotIn("Daily/raw/2026-05-07/chatroom/未命名.md", request)

            context = (compiled / "_ai-context.md").read_text(encoding="utf-8")
            self.assertIn("# AI Historical Context - 2026-05-07", context)
            self.assertIn("not today's raw evidence", context)

            audit = (compiled / "_ai-audit.md").read_text(encoding="utf-8")
            self.assertIn("Included source files: 2", audit)
            self.assertIn("Excluded markdown files: 2", audit)
            self.assertIn("Project registry included: yes", audit)
            self.assertIn("## Provenance", audit)
            self.assertIn("System/ai-sync-prompt.md", audit)
            self.assertIn("request includes System/projects.yml content", audit)
            self.assertIn("request omits files from configured excluded directories", audit)
            self.assertIn("Daily/raw/2026-05-07/chatroom/未命名.md", audit)
            self.assertIn("excluded directory `chatroom`", audit)

            run_state = json.loads((compiled / "_run-state.json").read_text(encoding="utf-8"))
            self.assertEqual(run_state["phase"], "packaged")
            self.assertIn("provenance", run_state)
            self.assertIn("System/ai-sync-prompt.md", run_state["provenance"])
            self.assertIn("Daily/raw/2026-05-07/00-canvas.md", run_state["source_files_sha256"])
            self.assertTrue(run_state["outputs"]["Daily/compiled/2026-05-07/_ai-request.md"])

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

    def test_capture_uses_cyberlog_today_when_now_is_not_overridden(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)

            old_today = os.environ.get("CYBERLOG_TODAY")
            old_now = os.environ.get("CYBERLOG_NOW")
            os.environ["CYBERLOG_TODAY"] = "2026-05-07"
            os.environ.pop("CYBERLOG_NOW", None)
            try:
                self.assertEqual(self.run_cli(root, "capture", "today-controlled note"), 0)
                raw = root / "Daily" / "raw" / "2026-05-07"
                self.assertTrue(any(path.read_text(encoding="utf-8") == "today-controlled note\n" for path in raw.glob("*-capture.md")))
            finally:
                if old_today is None:
                    os.environ.pop("CYBERLOG_TODAY", None)
                else:
                    os.environ["CYBERLOG_TODAY"] = old_today
                if old_now is None:
                    os.environ.pop("CYBERLOG_NOW", None)
                else:
                    os.environ["CYBERLOG_NOW"] = old_now

    def test_capture_type_writes_structured_front_matter_and_feed_attrs(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)

            old_now = os.environ.get("CYBERLOG_NOW")
            os.environ["CYBERLOG_NOW"] = "2026-05-07T14:23:00"
            try:
                self.assertEqual(
                    self.run_cli(
                        root,
                        "capture",
                        "--type",
                        "sent",
                        "--project",
                        "A38-DF108-Agilex5",
                        "--sent-to",
                        "FAE",
                        "--subject",
                        "SmartVID",
                        "--waiting-for",
                        "regulator confirmation",
                        "sent message body",
                    ),
                    0,
                )
            finally:
                if old_now is None:
                    os.environ.pop("CYBERLOG_NOW", None)
                else:
                    os.environ["CYBERLOG_NOW"] = old_now

            raw = root / "Daily" / "raw" / "2026-05-07"
            note = raw / "1423-sent.md"
            self.assertTrue(note.exists())
            text = note.read_text(encoding="utf-8")
            self.assertIn("type: sent", text)
            self.assertIn("project: A38-DF108-Agilex5", text)
            self.assertIn("sent_to: FAE", text)

            compiled = root / "Daily" / "compiled" / "2026-05-07"
            compiled.mkdir(parents=True)
            self.assertEqual(self.run_cli(root, "daily", "--date", "2026-05-07"), 0)
            feed = (compiled / "_ai-feed.md").read_text(encoding="utf-8")
            self.assertIn('type="sent"', feed)
            self.assertIn('project="A38-DF108-Agilex5"', feed)
            self.assertIn('trust="high"', feed)

    def test_daily_promotes_lightweight_hash_tags_to_feed_attrs(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)
            raw = root / "Daily" / "raw" / "2026-05-07"
            raw.mkdir(parents=True)
            (raw / "note.md").write_text("#可信 #已发送\nFAE question list was sent.\n", encoding="utf-8")

            self.assertEqual(self.run_cli(root, "daily", "--date", "2026-05-07"), 0)

            feed = (root / "Daily" / "compiled" / "2026-05-07" / "_ai-feed.md").read_text(encoding="utf-8")
            self.assertIn('type="sent"', feed)
            self.assertIn('trust="high"', feed)
            self.assertIn('tags="#可信 #已发送"', feed)

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
            (complete_compiled / "_run-state.json").write_text('{"date":"2026-05-01","phase":"closed","transitions":[]}\n', encoding="utf-8")

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

    def test_conflict_scan_writes_static_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)
            (root / "System" / "projects.yml").write_text(
                "projects:\n"
                "  - id: A38-DF108-Agilex5\n"
                "    aliases: [A38]\n"
                "    priority: P1\n"
                "    devices:\n"
                "      forbidden_aliases:\n"
                "        - A5EC052A B32A\n"
                "    constraints:\n"
                "      memory: \"LPDDR5 (NOT LPDDR5X)\"\n",
                encoding="utf-8",
            )
            raw = root / "Daily" / "raw" / "2026-05-11"
            raw.mkdir(parents=True)
            (raw / "memory.md").write_text(
                "A5EC052A B32A appeared in old notes.\n"
                "Candidate says LPDDR5X, but request says LPDDR5 only.\n",
                encoding="utf-8",
            )

            self.assertEqual(self.run_cli(root, "conflict-scan", "--date", "2026-05-11"), 0)

            report = root / "Daily" / "compiled" / "2026-05-11" / "_conflicts.md"
            self.assertTrue(report.exists())
            text = report.read_text(encoding="utf-8")
            self.assertIn("Conflict Scan - 2026-05-11", text)
            self.assertIn("Gate result: BLOCKED", text)
            self.assertIn("[blocking] E4/forbidden_alias", text)
            self.assertIn("A5EC052A B32A", text)
            self.assertIn("LPDDR5 / LPDDR5X", text)

    def test_decisions_rollup_writes_active_decisions(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)
            day = root / "Daily" / "compiled" / "2026-05-11"
            day.mkdir(parents=True)
            (day / "_decisions.yml").write_text(
                "- id: A38/2026-05-11-001\n"
                "  project: A38-DF108-Agilex5\n"
                "  topic: Keep SmartVID proposed\n"
                "  status: proposed\n"
                "  blockers: [FAE confirmation]\n"
                "  owner: HW\n"
                "  next: Send FAE questions\n"
                "  supersedes: []\n"
                "  evidence: [SmartVID PMBus.md]\n"
                "- id: A57/2026-05-11-001\n"
                "  project: A57-eDP\n"
                "  topic: eDP threshold frozen\n"
                "  status: frozen\n"
                "  blockers: []\n"
                "  owner: HW\n"
                "  next: Use in test table\n"
                "  supersedes: []\n"
                "  evidence: [eDP眼图标准.md]\n",
                encoding="utf-8",
            )

            self.assertEqual(self.run_cli(root, "decisions", "--rollup", "--through", "2026-05-11"), 0)

            rollup = root / "System" / "decisions-active.md"
            self.assertTrue(rollup.exists())
            text = rollup.read_text(encoding="utf-8")
            self.assertIn("Active Decisions - through 2026-05-11", text)
            self.assertIn("Integrity gate result: PASS", text)
            self.assertIn("A38/2026-05-11-001", text)
            self.assertNotIn("A57/2026-05-11-001", text)

    def test_validate_reports_gate_and_comms_aging_without_writing_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)
            (root / "System" / "projects.yml").write_text(
                "projects:\n"
                "  - id: A38-DF108-Agilex5\n"
                "    aliases: [A38]\n"
                "    priority: P1\n"
                "    devices:\n"
                "      forbidden_aliases:\n"
                "        - A5EC052A B32A\n"
                "    constraints:\n"
                "      memory: \"LPDDR5 (NOT LPDDR5X)\"\n",
                encoding="utf-8",
            )
            raw = root / "Daily" / "raw" / "2026-05-11"
            raw.mkdir(parents=True)
            (raw / "memory.md").write_text(
                "A5EC052A B32A appeared in old notes.\n"
                "Candidate says LPDDR5X, but request says LPDDR5 only.\n",
                encoding="utf-8",
            )
            compiled = root / "Daily" / "compiled" / "2026-05-11"
            compiled.mkdir(parents=True)
            (compiled / "_decisions.yml").write_text(
                "- id: A38-DF108-Agilex5/2026-05-11-001\n"
                "  project: A38-DF108-Agilex5\n"
                "  topic: LPDDR5 gate\n"
                "  status: proposed\n"
                "  blockers: [supplier reply]\n"
                "  owner: HW\n"
                "  next: Ask supplier\n"
                "  supersedes: []\n"
                "  evidence: [memory.md]\n",
                encoding="utf-8",
            )
            (compiled / "_comms.yml").write_text(
                "- id: A38-DF108-Agilex5/supplier-2026-05-07\n"
                "  project: A38-DF108-Agilex5\n"
                "  channel: supplier_email\n"
                "  status: draft\n"
                "  waiting_for: supplier reply\n"
                "  expected_reply_by: null\n"
                "- id: A38-DF108-Agilex5/fae-2026-05-11\n"
                "  project: A38-DF108-Agilex5\n"
                "  channel: fae_message\n"
                "  status: waiting_for_reply\n"
                "  waiting_for: regulator confirmation\n"
                "  expected_reply_by: null\n",
                encoding="utf-8",
            )

            result, output = self.run_cli_output(root, "validate", "--date", "2026-05-11")

            self.assertEqual(result, 0)
            self.assertIn("Cyberlog Validation - 2026-05-11", output)
            self.assertIn("Gate result: BLOCKED", output)
            self.assertIn("Error codes: E4 project_boundary, E5 state_drift, E7 output_contract", output)
            self.assertIn("[blocking] E4/forbidden_alias", output)
            self.assertIn("LPDDR5", output)
            self.assertIn("[warning] E5/comms_draft_aging", output)
            self.assertIn("draft for 4 day(s)", output)
            self.assertIn("[warning] E5/comms_missing_expected_reply_by", output)
            self.assertIn("P0/P1 waiting_for_reply", output)
            self.assertFalse((compiled / "_validation.md").exists())

            strict_result = self.run_cli(root, "validate", "--date", "2026-05-11", "--strict")
            self.assertEqual(strict_result, 1)

            self.assertEqual(self.run_cli(root, "validate", "--date", "2026-05-11", "--write"), 0)
            self.assertTrue((compiled / "_validation.md").exists())
            run_state = json.loads((compiled / "_run-state.json").read_text(encoding="utf-8"))
            self.assertEqual(run_state["phase"], "validation_blocked")
            self.assertEqual(run_state["validation"]["gate_result"], "BLOCKED")
            self.assertTrue(run_state["outputs"]["Daily/compiled/2026-05-11/_validation.md"])

    def test_validate_checks_ai_output_contract_and_source_references(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)
            raw = root / "Daily" / "raw" / "2026-05-07"
            compiled = root / "Daily" / "compiled" / "2026-05-07"
            raw.mkdir(parents=True)
            compiled.mkdir(parents=True)
            (raw / "note.md").write_text("source note\n", encoding="utf-8")
            self.assertEqual(self.run_cli(root, "daily", "--date", "2026-05-07"), 0)
            (compiled / "_cyberlog.md").write_text(
                "# Cyberlog — 2026-05-07\n\n"
                "## 0. 项目索引\n\n"
                "See `missing.md`.\n",
                encoding="utf-8",
            )
            (compiled / "_tomorrow-boot.md").write_text("# Tomorrow Boot Packet — 2026-05-08\n\n## 明日主线\n-\n", encoding="utf-8")
            (compiled / "_ai-output-audit.md").write_text("checked\n", encoding="utf-8")

            result, output = self.run_cli_output(root, "validate", "--date", "2026-05-07")

            self.assertEqual(result, 0)
            self.assertIn("[blocking] E7/cyberlog_structure", output)
            self.assertIn("[blocking] E7/tomorrow_boot_structure", output)
            self.assertIn("[warning] E2/source_reference", output)

    def test_golden_add_scaffolds_and_check_enforces_assertions(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)

            self.assertEqual(self.run_cli(root, "golden", "add", "--date", "2026-05-07"), 0)

            contract_path = root / "Reviews" / "golden-days" / "2026-05-07.json"
            self.assertTrue(contract_path.exists())
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            self.assertIn("E7", contract["observed_error_codes"])

            contract["assertions"]["required_error_codes"] = ["E7"]
            contract_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result, output = self.run_cli_output(root, "golden", "check", "--date", "2026-05-07", "--strict")
            self.assertEqual(result, 0)
            self.assertIn("Golden Days Report", output)
            self.assertIn("Observed error codes:", output)
            self.assertIn("E7", output)

            contract["assertions"]["forbidden_error_codes"] = ["E7"]
            contract_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            self.assertEqual(self.run_cli(root, "golden", "check", "--date", "2026-05-07", "--strict"), 1)

    def test_close_day_marks_closed_and_prune_requires_closed_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)
            raw = root / "Daily" / "raw" / "2026-05-07"
            compiled = root / "Daily" / "compiled" / "2026-05-07"
            raw.mkdir(parents=True)
            compiled.mkdir(parents=True)
            (raw / "note.md").write_text("finished source\n", encoding="utf-8")
            self.assertEqual(self.run_cli(root, "daily", "--date", "2026-05-07"), 0)
            (compiled / "_cyberlog.md").write_text(
                "# Cyberlog — 2026-05-07\n\n"
                "## 0. 项目索引\n- cyberlog-workflow / yes / closed / 未发现\n\n"
                "## 1. 今日真实推进\n### cyberlog-workflow\n- Finished from `note.md`.\n\n"
                "## 2. 当前工作画布\n### Active\n- 未发现\n\n### Queue\n- 未发现\n\n### Blocked\n- 未发现\n\n### Closed\n- Finished.\n\n"
                "## 3. 关键决策\n| 项目 | 决策 | 状态 | 背景 | 理由 | 风险 | 后续动作 | 来源文件 |\n|---|---|---|---|---|---|---|---|\n| cyberlog-workflow | close day | validated | note | test | none | none | note.md |\n\n"
                "## 4. 重要信息\n- 未发现\n\n"
                "## 5. 今日产出\n- `_cyberlog.md`\n\n"
                "## 6. 未完成任务\n- 未发现\n\n"
                "## 7. 明日启动包\n- See `_tomorrow-boot.md`.\n\n"
                "## 8. 工作流摩擦\n- 未发现\n\n"
                "## 9. 自我迭代建议\n- 未发现\n\n"
                "## 10. 规则候选\n- 未发现\n",
                encoding="utf-8",
            )
            (compiled / "_tomorrow-boot.md").write_text(
                "# Tomorrow Boot Packet — 2026-05-08\n\n"
                "## 明日主线\n-\n\n"
                "## 背景\n-\n\n"
                "## 当前状态\n-\n\n"
                "## 第一动作\n-\n\n"
                "## 注意事项\n-\n\n"
                "## 不要重复踩的坑\n-\n\n"
                "## 可以交给 AI / agent 的部分\n-\n\n"
                "## 必须由我亲自判断的部分\n-\n",
                encoding="utf-8",
            )
            (compiled / "_ai-output-audit.md").write_text("checked\n", encoding="utf-8")

            result, output = self.run_cli_output(root, "close-day", "--date", "2026-05-07")

            self.assertEqual(result, 0)
            self.assertIn("Closed 2026-05-07", output)
            state = json.loads((compiled / "_run-state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["phase"], "closed")
            self.assertEqual(state["validation"]["gate_result"], "PASS")

            self.assertEqual(self.run_cli(root, "prune-raw", "--before", "2026-05-08", "--apply"), 0)
            self.assertFalse(raw.exists())

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

    def test_monthly_collects_weekly_reviews_and_durable_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.run_cli(root, "init"), 0)

            weekly = root / "Reviews" / "weekly"
            weekly.mkdir(parents=True, exist_ok=True)
            (weekly / "2026-W19_weekly-review.md").write_text("weekly diagnosis\n", encoding="utf-8")
            (root / "System" / "decisions-active.md").write_text("active decisions\n", encoding="utf-8")

            self.assertEqual(
                self.run_cli(root, "monthly", "--start", "2026-05-04", "--end", "2026-05-10"),
                0,
            )

            output = root / "Reviews" / "monthly" / "2026-05_ai-monthly-request.md"
            self.assertTrue(output.exists())
            text = output.read_text(encoding="utf-8")
            self.assertIn("AI Monthly Review Request - 2026-05-04 to 2026-05-10", text)
            self.assertIn("Monthly Workflow Intelligence", text)
            self.assertIn('<file path="Reviews/weekly/2026-W19_weekly-review.md">', text)
            self.assertIn('<file path="System/decisions-active.md">', text)
            self.assertIn("weekly diagnosis", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
