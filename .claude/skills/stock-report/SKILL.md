---
name: stock-report
description: Write an evidence-based stock research report (business, financials, valuation, what the price assumes, bull/base/bear scenarios, tripwires) for a reader with no finance background, using a researcher → facts ledger → bull/bear debate → writer → reviewer flow. Use when the user asks to research, analyse or summarise a stock or ticker, or types /stock-report <TICKER>.
argument-hint: <TICKER or company> [link to a previous report] [--no-debate]
---

# Stock report

Build a stock research report for the ticker in the arguments in three roles:

```
Researcher ──► facts ledger ──┬─► Bull debater ─┐  round 1: cases
  (subagent)     (JSON)       └─► Bear debater ─┤  round 2: rebuttals
                                                ▼
                         Writer (you) ──► report doc ──► Reviewer (fresh subagent)
                              ▲                                   │
                              └────────────── fixes ──────────────┘
```

- **The rule that makes this work:** the writer uses only numbers that are in the ledger. Need a number that isn't there? Get it into the ledger first (look it up and add an entry), then use it.
- **No ticker given?** Ask for one and nothing else.

The files in this skill's folder:
- `report-spec.md`: what the report contains and how it's written.
- `researcher.md`: the research agent's brief and the ledger format.
- `debater.md`: the bull/bear debaters' brief (case, then rebuttal).
- `reviewer.md`: the reviewer's checks and output format.
- `yahoo.py`: the researcher's script that pulls consensus, revisions, surprises and peer multiples from Yahoo Finance (via `yfinance`).

Pass subagents the **absolute paths** to these files.

## Step 0: Set up

- Working folder: the session scratchpad if there is one, else `./stock-reports/<TICKER>-<YYYY-MM-DD>/`.
- Ledger path: `<working folder>/<TICKER>-ledger.json`.
- If the user passed a previous report, note its link for the researcher and for section 10.

## Step 1: Make the doc and start the researcher, in parallel

- **Report = a published Artifact, always.** The user reads it on mobile and may run this skill from a remote session, so the report must end up at a claude.ai artifact link, never only in a local file or in chat. Use the first route that is available:
  1. **Claude Docs connector** (first-party docs tools): create the doc with the title, an as-of date and one pending placeholder per section from `report-spec.md`, then open it. The doc is itself an artifact, and its link works on mobile.
  2. **Artifact tool** (no docs connector):
     - Load the `artifact-design` skill first.
     - Write `<working folder>/<TICKER>-report.html` as a mobile-first page: a single column, tables that scroll inside their own box rather than the page, readable at phone width, with light and dark themes.
     - Publish it right away with just the title and section headings, so the link exists early. Use `icon: "chart"` and a one-line description, e.g. `"<Company> stock research, as of <date>"`.
     - Republish the same file path after each section is filled. The URL stays the same.
  3. **Neither available:** write the HTML file and say plainly that it could not be published. Never claim a link you don't have.
  - Title for all routes: `<Company> (<TICKER>) — Stock Research Report`.
- **Researcher:** start a subagent in the background (Agent tool, `general-purpose`, model `sonnet` unless the user said otherwise) with:
  > Read `<abs path>/researcher.md` and follow it. Ticker: `<TICKER>`. Today: `<date>`. Write the ledger to `<ledger path>`. Previous report: `<link or none>`. Spec: `<abs path>/report-spec.md`.

  While it runs, tell the user in one line that research is under way. Don't research the same things yourself.

## Step 2: Bull vs bear debate (two subagents, two rounds)

When the researcher reports back, read the ledger whole. Then start the debate.

**Round 1.** Start the two debaters in parallel, in the background (`general-purpose`, model `sonnet`):
> Read `<abs path>/debater.md` and follow it. Side: BULL (or BEAR). Round 1. Ledger: `<ledger path>`. Spec: `<abs path>/report-spec.md`. Write to `<working folder>/<TICKER>-bull.md` (or `-bear.md`).

While they argue, write sections 1–7 of the report (they don't depend on the debate).

**Round 2.** When both cases are in, send each debater the other side's file for its rebuttal:
- Preferred: continue the same agent with SendMessage.
- Otherwise: start a new agent with both file paths, "Round 2".

**Then, before using anything from the debate:**
- **Proposed facts:** check each one against its URL. Add the ones that hold to the ledger, and drop the rest.
- **Read both rebuttals:**
  - a point the other side **conceded**, or couldn't refute with evidence, is a surviving point;
  - a point refuted with ledger evidence is dropped.

## Step 3: Write (you)

Finish the remaining sections one at a time, in the order of `report-spec.md` (sections 1–7 were written during the debate). These rules apply to every section:

- **Bull and bear scenarios (section 11):** take the growth, margin and P/E assumptions from each debater's **revised** scenario. Adjust any that a rebuttal undermined, and say so in the report.
- **Base case:** stays consensus.
- **Tripwires (section 12):** use the debaters' "what would prove you wrong" items as the starting list.
- **Under the scenario table, add:**
  - the strongest surviving point for each side;
  - each side's own admitted weakest point.
- Every number comes from a ledger entry, carries its label (Reported / Consensus / My calculation / My scenario assumption) and states its period.
- Your own new calculations (the "what today's price assumes" back-solve, the scenario chain) go into the ledger as `My calculation` entries with formulas **before** they go in the doc.
- Present `one_offs` as reported vs underlying wherever they distort a figure.
- Write `unavailable` items as a one-line "not reliably available". Raise `conflicts` in the data-limitations section.
- Doc formatting: avoid two `~` characters in one paragraph, because some renderers turn the text between them into strikethrough. Write "about" instead.

## Step 4: Review (fresh subagent)

Start a new subagent, not the researcher or a debater, so it brings fresh eyes (`general-purpose`, model `sonnet`):
> Read `<abs path>/reviewer.md` and follow it. Report: `<doc link or file path>`. Ledger: `<ledger path>`. Debate: `<bull path>`, `<bear path>`. Spec: `<abs path>/report-spec.md`.

Subagents can't read a docs or artifact link. Give the reviewer a local copy instead:
- **Artifact route:** the HTML file itself.
- **Docs route:** export or copy the report text to `<working folder>/<TICKER>-report.md`.

## Step 5: Fix, then hand over

- Apply every confirmed fix from the reviewer. Where you disagree with one, check it against the ledger or source. The evidence decides, not you.
- If any **WRONG**, **UNSOURCED** or **UNSUPPORTED** items were fixed, run the reviewer once more on the changed sections only. Stop after two review rounds and list anything still open in the data-limitations section.
- Make sure the final version is published:
  - **Docs route:** the doc is live already.
  - **Artifact route:** republish the HTML after the fixes.
- Reply in chat with:
  - the artifact link, first and on its own line, so it is easy to tap on mobile;
  - what the price assumes;
  - the scenario range vs the current price;
  - the biggest positive and biggest risk;
  - the next dated check;
  - what the review caught and fixed, in one line.

  No buy/sell call.

## Cost note

This flow uses five subagent runs (researcher, two debaters × two rounds, reviewer) and costs about 3x the tokens of a single pass. Offer the cheaper versions when they fit:
- `--no-debate`: skip Step 2 and write the bull and bear cases yourself, as before.
- **Quick take:** follow `report-spec.md` directly, with no subagents at all.
