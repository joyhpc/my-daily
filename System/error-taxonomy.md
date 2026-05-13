# Cyberlog Error Taxonomy

Purpose: turn AI/output mistakes into repeatable categories so validation, golden days, and workflow rules can improve without extra daily bookkeeping.

| Code | Name | Meaning | Usual Fix |
|---|---|---|---|
| `E1` | factual_upgrade | Drafts, guesses, or `#待确认` content were upgraded into facts | Tighten raw tags or prompt boundary |
| `E2` | source_hallucination | Output cites missing or unsupported sources | Fix citation, source path, or validation rule |
| `E3` | context_leak | Historical context was written as today's progress | Move item to continuity / background |
| `E4` | project_boundary | Project id, alias, forbidden alias, or constraint boundary drifted | Update `projects.yml` or flag conflict |
| `E5` | state_drift | Draft/sent/waiting/replied/closed communication state drifted | Update `_comms.yml` or raw capture |
| `E6` | decision_drift | Decision status, supersedes chain, owner, next action, or evidence drifted | Update `_decisions.yml` |
| `E7` | output_contract | Required output file or section contract failed | Regenerate or repair AI output |

## Low-manual workflow

1. Run `python3 tools/cyberlog.py validate --date YYYY-MM-DD --write`.
2. Read the error code labels in `_validation.md`.
3. If the same code repeats, fix one of three places:
   - input contract: raw tags or capture habit
   - deterministic gate: validation/conflict-scan
   - durable rule: `System/workflow-rules.md`
4. For an important regression, run `python3 tools/cyberlog.py golden add --date YYYY-MM-DD` and edit only the assertions that matter.
