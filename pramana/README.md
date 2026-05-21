# Pramana

**Pramana** (प्रमाण — Sanskrit for *means of valid knowledge / standard of evidence*) is a research agent that turns any topic into a structured, source-cited briefing.

## What Pramana does

When you ask Pramana to research a topic, it runs a fixed workflow:

1. **Scope** — confirms the topic and angle in one line
2. **Source gathering** — at least three varied web searches, then 3–6 primary sources fetched
3. **Contrarian pass** — a dedicated search for opposing/skeptical views (mandatory)
4. **Draft** — fills a 9-section briefing template with every claim cited
5. **Self-check** — verifies coverage and citation integrity before delivery

The output is one markdown file with these sections:

1. TL;DR
2. Context
3. Key facts
4. Players / landscape
5. Dynamics
6. **Contrarian view**
7. Outlook
8. Recommendation
9. Sources

## How to summon Pramana

Ask Claude any of:

- "Pramana, <topic>"
- "Ask Pramana about <topic>"
- "Run Pramana on <topic>"
- "Deep dive on <topic>"
- "Research <topic>"
- "Brief me on <topic>"
- "What's going on with <topic>?"

The skill auto-loads on those phrasings. For one-line factual lookups, Pramana stays out of the way — it's for topics that warrant multi-source synthesis.

## What Pramana produces

A markdown file named `pramana-<topic-slug>.md` in your current working directory, opening with:

```
# Pramana Briefing: <Topic>

*Prepared by Pramana · YYYY-MM-DD · Angle: <one phrase>*
```

Target length is 800–1500 words for the body, plus a numbered Sources list with full URLs.

Every factual claim in the body has an inline `[Source N]` citation pointing to the numbered Sources list. The self-check phase verifies the citation graph before delivery — no uncited claims, no orphan sources, no `[Source N]` references that don't resolve.

## Why a fixed framework

The 9-section structure forces consistent depth on every briefing. The **Contrarian view** section in particular is non-optional — it's the part of the workflow that prevents the rest from becoming an echo chamber of whatever the first three searches surfaced. Pramana runs a dedicated contrarian search before drafting the Outlook and Recommendation; if the strongest opposing case doesn't show up in that search, Pramana says so in the section rather than fabricating one.

## Voice

Pramana speaks like an advisor in the Chanakya tradition:

- Terse over verbose.
- Concrete over abstract — names vendors, dollar amounts, dates.
- Recommends, doesn't survey.
- Names tradeoffs explicitly.
- Never disclaims. The agent sources or flags — it doesn't hedge.

## Files

- `.claude-plugin/plugin.json` — manifest
- `skills/pramana/SKILL.md` — the workflow, triggers, and self-check rules
- `skills/pramana/references/framework.md` — per-section content guidance
- `skills/pramana/references/briefing-template.md` — the markdown skeleton
- `skills/pramana/references/source-quality.md` — heuristics for source evaluation

## Requirements

Uses the built-in `WebSearch` and `WebFetch` tools. No external services or credentials needed.
