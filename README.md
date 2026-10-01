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

The prompt body (everything after the `---` divider in `SKILL.md`) also works pasted into any chat model; put the ticker on the last line as `STOCK: <TICKER>`.
