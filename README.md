# prompts
list of prompts

## Skills

| Skill | What it does |
| --- | --- |
| [`stock-report`](.claude/skills/stock-report/SKILL.md) | Evidence-based stock research report: business, financials, valuation, what the price assumes, bull/base/bear scenarios and tripwires. A researcher subagent builds a sourced **facts ledger**, bull and bear subagents debate it (case + rebuttal), the main session writes only from the ledger, and a fresh reviewer subagent checks every number, calculation and claim. Run `/stock-report NFLX`. |

`.claude/skills/stock-report/` files: `SKILL.md` (the flow) · `report-spec.md` (report content and style) · `researcher.md` (research brief + ledger format) · `debater.md` (bull/bear debate brief) · `reviewer.md` (review checklist).

### Run it remotely (phone or web)

The skill lives in `.claude/skills/`, so any Claude Code session opened on this repo loads it automatically. That includes cloud sessions at claude.ai/code and the Claude mobile app.
Open a session on `harminder0209/prompts`, type `/stock-report NFLX`, and the report is published as a claude.ai artifact you can read on your phone.

### Install a skill in Claude Code (local, any project)

```sh
mkdir -p ~/.claude/skills/stock-report
for f in SKILL.md report-spec.md researcher.md debater.md reviewer.md; do
  curl -fsSL "https://raw.githubusercontent.com/harminder0209/prompts/main/.claude/skills/stock-report/$f" \
    -o ~/.claude/skills/stock-report/$f
done
```

Paste-ready prompt for any chat model: [`stock_research.md`](stock_research.md). Change only the last line (`STOCK: <TICKER>`).
