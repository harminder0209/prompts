# prompts
list of prompts

## Skills

| Skill | What it does |
| --- | --- |
| [`stock-report`](skills/stock-report/SKILL.md) | Evidence-based stock research report: business, financials, valuation, what the price assumes, bull/base/bear scenarios and tripwires. Run `/stock-report NFLX`. |

### Install a skill in Claude Code

```sh
mkdir -p ~/.claude/skills/stock-report
curl -fsSL https://raw.githubusercontent.com/harminder0209/prompts/main/skills/stock-report/SKILL.md \
  -o ~/.claude/skills/stock-report/SKILL.md
```

Paste-ready prompt for any chat model: [`sotck_research`](sotck_research). Change only the last line (`STOCK: <TICKER>`).
