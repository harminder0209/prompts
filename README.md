# prompts
list of prompts

## Skills

| Skill | What it does |
| --- | --- |
| [`stock-report`](skills/stock-report/SKILL.md) | Evidence-based stock research report: business, financials, valuation, what the price assumes, bull/base/bear scenarios and tripwires. A researcher subagent builds a sourced **facts ledger**, bull and bear subagents debate it (case + rebuttal), the main session writes only from the ledger, and a fresh reviewer subagent checks every number, calculation and claim. Run `/stock-report NFLX`. |

`skills/stock-report/` files: `SKILL.md` (the flow) · `report-spec.md` (report content and style) · `researcher.md` (research brief + ledger format) · `debater.md` (bull/bear debate brief) · `reviewer.md` (review checklist).

### Install a skill in Claude Code

```sh
mkdir -p ~/.claude/skills/stock-report
for f in SKILL.md report-spec.md researcher.md debater.md reviewer.md; do
  curl -fsSL "https://raw.githubusercontent.com/harminder0209/prompts/main/skills/stock-report/$f" \
    -o ~/.claude/skills/stock-report/$f
done
```

Paste-ready prompt for any chat model: [`stock_research.md`](stock_research.md). Change only the last line (`STOCK: <TICKER>`).
