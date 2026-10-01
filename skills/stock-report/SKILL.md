---
name: stock-report
description: Write an evidence-based stock research report (business, financials, valuation, what the price assumes, bull/base/bear scenarios, tripwires) for a reader with no finance background, using a researcher → facts ledger → writer → reviewer flow. Use when the user asks to research, analyse or summarise a stock or ticker, or types /stock-report <TICKER>.
argument-hint: <TICKER or company> [link to a previous report]
---

# Stock report

Build a stock research report for the ticker in the arguments in three roles:

```
Researcher (subagent) ──► facts ledger (JSON) ──► Writer (you) ──► report doc
                                                        ▲                 │
                                                        └── fixes ── Reviewer (fresh subagent)
```

- **The rule that makes this work:** the writer uses only numbers that are in the ledger. Need a number that isn't there? Get it into the ledger first (look it up and add an entry), then use it.
- **No ticker given?** Ask for one and nothing else.

The files in this skill's folder:
- `report-spec.md`: what the report contains and how it's written.
- `researcher.md`: the research agent's brief and the ledger format.
- `reviewer.md`: the reviewer's checks and output format.

Pass subagents the **absolute paths** to these files.

## Step 0: Set up

- Working folder: the session scratchpad if there is one, else `./stock-reports/<TICKER>-<YYYY-MM-DD>/`.
- Ledger path: `<working folder>/<TICKER>-ledger.json`.
- If the user passed a previous report, note its link for the researcher and for section 10.

## Step 1: Make the doc and start the researcher, in parallel

- **Doc:** create a shareable doc with the Claude Docs connector if available, otherwise an HTML or Markdown file in the working folder.
  - Title: `<Company> (<TICKER>) — Stock Research Report`.
  - Add an as-of date and one placeholder per section from `report-spec.md`.
  - Open the doc for the user.
- **Researcher:** start a subagent in the background (Agent tool, `general-purpose`, model `sonnet` unless the user said otherwise) with:
  > Read `<abs path>/researcher.md` and follow it. Ticker: `<TICKER>`. Today: `<date>`. Write the ledger to `<ledger path>`. Previous report: `<link or none>`. Spec: `<abs path>/report-spec.md`.

  While it runs, tell the user in one line that research is under way. Don't research the same things yourself.

## Step 2: Write (you)

When the researcher reports back, read the ledger whole. Then fill the doc one section at a time, in the order of `report-spec.md`.

- Every number comes from a ledger entry, carries its label (Reported / Consensus / My calculation / My scenario assumption) and states its period.
- Your own new calculations (the "what today's price assumes" back-solve, the scenario chain) go into the ledger as `My calculation` entries with formulas **before** they go in the doc.
- Present `one_offs` as reported vs underlying wherever they distort a figure.
- Write `unavailable` items as a one-line "not reliably available". Raise `conflicts` in the data-limitations section.
- Doc formatting: avoid two `~` characters in one paragraph, because some renderers turn the text between them into strikethrough. Write "about" instead.

## Step 3: Review (fresh subagent)

Start a new subagent, not the researcher, so it brings fresh eyes (`general-purpose`, model `sonnet`):
> Read `<abs path>/reviewer.md` and follow it. Report: `<doc link or file path>`. Ledger: `<ledger path>`. Spec: `<abs path>/report-spec.md`.

Docs links can only be read with docs tools. If the subagent can't read the doc, export or copy the report text to `<working folder>/<TICKER>-report.md` and give it that path.

## Step 4: Fix, then hand over

- Apply every confirmed fix from the reviewer. Where you disagree with one, check it against the ledger or source. The evidence decides, not you.
- If any **WRONG**, **UNSOURCED** or **UNSUPPORTED** items were fixed, run the reviewer once more on the changed sections only. Stop after two review rounds and list anything still open in the data-limitations section.
- Reply in chat with:
  - the doc link;
  - what the price assumes;
  - the scenario range vs the current price;
  - the biggest positive and biggest risk;
  - the next dated check;
  - what the review caught and fixed, in one line.

  No buy/sell call.

## Cost note

This flow costs about 2x the tokens of a single pass. If the user only wants a quick take, offer the single-pass version instead: follow `report-spec.md` directly without the subagents.
