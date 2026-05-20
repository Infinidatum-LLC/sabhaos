# Sabha OS

> An open-source **protocol** for a Claude-native AI council. Decisive, tradeoff-aware, grounded — in the Chanakya tradition. Works with any memory backend, including Claude Memory.

> 👋 **New here and not a developer?** Start with [docs/QUICKSTART.md](./docs/QUICKSTART.md) — a 10-minute, no-installation guide to get Sabha working inside Claude.ai. No terminal, no Git, no command-line.

**Sabha** (சபை, सभा, Sanskrit for *council*) is a routing protocol for Claude. Every load-bearing question gets classified into a C-suite role, answered in the **Chanakya** tradition — terse, decisive, recommendation-first, tradeoff-aware, grounded.

Most AI replies are option-shaped: *"here are five approaches with pros and cons."* That's exhausting when you're running something. Sabha forces a different reply:

```
Routing: CFO. Cut the SaaS line 40%. You lose the analytics tier.
         Worth it because that tier isn't driving renewals.
```

## The stack

```
Category:    AI council protocol
─────────────────────────────────────────────────────────────
Protocol:    Sabha OS              ← how the council thinks
Archetype:   Chanakya              ← the voice it speaks in
Memory:      pluggable backend     ← Claude Memory, Sakthi Graph,
                                     mem0, Letta, Zep, plain markdown
─────────────────────────────────────────────────────────────
Optional:    Sakthi Graph          ← local-first memory backend
             Sittham                  + corpus ingest verb
                                     (when you want institutional
                                     memory that never leaves your
                                     machine)
```

**The protocol is the product.** It's a structured way of asking and answering questions — 9 roles, deep skills per role, an engage/ask mode discipline, a grounding rule. It runs on top of any memory backend you trust.

The most common pairings:

| Memory backend | Best for | What you get |
|---|---|---|
| **Claude Memory** | Default for most users | Zero-config; lives on Anthropic's servers; cross-conversation semantic recall |
| **Sakthi Graph** | Privacy / regulated / power users | Local-first, role-shaped, graph-queryable; runs on your machine |
| **mem0 / Letta / Zep / Pieces** | Existing memory-MCP investment | Sabha is memory-MCP-agnostic; plug yours in |
| **Plain `memory/` markdown** | Minimalists | No MCP at all; just a folder of files |

See [`docs/MEMORY-OPTIONS.md`](./docs/MEMORY-OPTIONS.md) for the full comparison and tradeoffs.

## What it does

Every load-bearing question (strategy, finance, hiring, infra, marketing, product) gets routed at the top of the reply:

```
Routing: CFO (primary). CSO weighs in on the partnership angle.

[role-voice answer, drawing on your Sakthi]
```

Nine built-in roles (CFO · CMO · CIO · CAIO · CSO · CXO · CHRO · CLC · CEO), fully customizable. Three modes — **ask** (chat reply), **engage** (document-grade deliverable, auto-files to Sakthi), and **deliberate** (two or three roles argue, CEO synthesizes, transcript filed). A memory hook so the council remembers your projects, people, and prior decisions — locally, on your machine.

> **New in v2.2.0** — `/deliberate <question>` invokes structured multi-role argument with a fixed protocol (openings → rebuttals → CEO synthesis). Every engage and deliberate answer auto-writes a `SABHA_DIARY v1` entry, so decisions compound. See [`skills/modes/deliberate/SKILL.md`](skills/modes/deliberate/SKILL.md) and [`skills/modes/sakthi-diary/SKILL.md`](skills/modes/sakthi-diary/SKILL.md).

## Sabha + Claude Memory — they work together

Claude has shipped its own cross-conversation memory. **Sabha is compatible with it, not competitive.** Most users should run Sabha *on top of* Claude Memory and get both: the council's routing discipline + Anthropic's built-in cross-session recall. No configuration changes needed — the protocol queries memory generically.

```
USER QUESTION ──► Sabha routes to <ROLE> ──► role queries memory backend ──► reply
                                                  │
                          ┌───────────────────────┴───────────────────────┐
                          ▼                                               ▼
                    Claude Memory                              Sakthi / mem0 / Letta / ...
                  (default, server-side,                       (local, structured, optional)
                   semantic recall)
```

You don't have to pick. They serve different purposes:
- **Claude Memory** handles casual cross-session recall and personalization — it's the default and it's fine.
- **Sakthi Graph** is the local-first, graph-shaped, role-segmented option for users who want institutional memory that never leaves their machine — useful for regulated industries (health, legal, finance, defense) or anyone who wants auditable, portable, LLM-agnostic memory. See [`docs/FOR-REGULATED-INDUSTRIES.md`](./docs/FOR-REGULATED-INDUSTRIES.md).

The default `CLAUDE.md` is memory-MCP-agnostic at the protocol layer. Wire in whichever memory you want, or use Claude Memory and skip the wiring entirely.

## Install

### Option A — Claude Code marketplace (recommended)

Minimum install — just the protocol. Works with Claude Memory (or no memory at all):

```bash
claude plugin marketplace add rdmurugan/sabhaos
claude plugin install sabha-os@sabha-marketplace
```

Then personalize — open `~/.claude/plugins/cache/sabha-marketplace/sabha-os/CLAUDE.md` and fill in the `[BRACKETS]` with your entities, people, and projects.

Open a new Claude Code session and ask anything substantive — you'll see the routing line at the top of the reply.

### Optional: add the local-first memory backend

If you want institutional memory that never leaves your machine — graph-shaped, role-segmented, LLM-agnostic — add Sakthi Graph:

```bash
claude plugin install sakthi-graph@sabha-marketplace
uv tool install sakthi-graph   # or: pip install sakthi-graph
sakthi init --sabha ~/sakthi   # bootstraps the 9 role wings
```

When to add Sakthi vs stick with Claude Memory: see [`docs/MEMORY-OPTIONS.md`](./docs/MEMORY-OPTIONS.md). Short version: Sakthi is for privacy-sensitive users, regulated industries, and operators who want auditable, portable, graph-queryable memory. For most casual use, Claude Memory is fine and zero-config.

#### Sittham — bring a folder into the council's consciousness

If you've installed Sakthi Graph, `sakthi sittham` (சித்தம், Tamil for *consciousness / awareness*) files any folder's distilled graph into the matching Sabha role wing:

```bash
/graphify ~/path/to/corpus            # one-time prep
sakthi sittham ~/path/to/corpus       # bring into cfo / cmo / caio / ... by content
```

Corpus content scores against the 9 role vocabularies; the dominant role's `decisions` room receives a compact summary drawer. Weak or split signals fall back to `ceo/synthesis-notes`. Power-user feature; safe to skip until you need it.

### Option B — Direct git clone (if you prefer)

```bash
git clone https://github.com/rdmurugan/sabhaos.git ~/.claude/plugins/sabha-os
claude plugin enable sabha-os
```

Same result; just bypasses the marketplace layer.

### Option C — Plain Claude (Claude.ai, Cowork, API)

If you don't use Claude Code, copy the contents of [`CLAUDE.md`](./CLAUDE.md) into:

- **Claude.ai** — paste into a Project's custom instructions
- **Cowork** — paste into a global `CLAUDE.md` in your workspace
- **API** — prepend it as a system prompt

Fill in the `[BRACKETS]` with your own entities before pasting. For a step-by-step walkthrough, see [`docs/QUICKSTART.md`](./docs/QUICKSTART.md).

## Three reference councils

Sabha is a protocol, not a fixed cast of characters. Three preset councils ship in `examples/`, each tuned for a different life:

- [`examples/personal-sakthi.CLAUDE.md`](./examples/personal-sakthi.CLAUDE.md) — life roles: Health, Finance, Family, Career, Time, Self.
- [`examples/professional-sakthi.CLAUDE.md`](./examples/professional-sakthi.CLAUDE.md) — the default C-suite council: CIO, CAIO, CFO, CMO, CSO, CXO, CHRO, CEO.
- [`examples/developer-sakthi.CLAUDE.md`](./examples/developer-sakthi.CLAUDE.md) — code roles: Architect, Reviewer, Security, Performance, QA, Mentor.

Three reference implementations of one protocol. Fork any of them. The point is *your* council, not ours.

## Customize

The protocol lives in one file: [`CLAUDE.md`](./CLAUDE.md). Edit it.

**Common customizations:**

- **Rename roles** — running an agency? Swap CIO for "Creative Director." A solo founder might collapse CFO+CSO into "Operator."
- **Add domain keywords** — under each role, the bracketed list is what Claude uses to classify. Add your specific tools, vendors, projects.
- **Swap the memory MCP** — the protocol calls memory generically. Wire it to MemPalace, mem0, Letta, Zep, Pieces, or a `memory/` folder. See [`docs/CUSTOMIZATION.md`](./docs/CUSTOMIZATION.md).
- **Tune the voice** — the default is *terse, decisive, recommendation-first*. If you want warmer or more exploratory, edit the "ANSWER" section.

See [`docs/CUSTOMIZATION.md`](./docs/CUSTOMIZATION.md) for walkthroughs.

## Why use this

Most AI replies are *option-shaped*: *"here are three approaches, with pros and cons."* That's exhausting when you're trying to run something. Sabha forces:

1. **A role.** Treating the question as belonging to a real job function narrows the answer.
2. **A recommendation.** The role has to commit, not survey.
3. **A tradeoff.** Naming what you give up keeps the answer honest.
4. **Mode discipline.** Ask = chat. Engage = file it. No fifteen-page replies to a one-line question.
5. **A memory of you.** With a local memory MCP wired in, every reply draws on your accumulated Sakthi — your decisions, your people, your projects.

## Depth — each role is a skill, not a voice tweak

**All 9 C-suite roles are now built out as deep skills.** Each ships with a SKILL definition, a multi-framework REFERENCE knowledge base, heuristics for fast-lookup, fillable templates, procedural playbooks, end-to-end worked examples, and source references.

- [`skills/roles/cfo/`](./skills/roles/cfo/) — runway, unit economics, capital allocation, pricing canvas, fundraise prep, cost-cut. Draws on Kahneman/Tversky, McKinsey on capital allocation, Skok on SaaS unit economics, Wack on scenario planning, Kaplan & Norton on performance.
- [`skills/roles/cmo/`](./skills/roles/cmo/) — positioning, Jobs-to-be-Done, channel portfolio, repositioning, behavioral pricing. Draws on Christensen, Porter, Trout & Ries, Thaler & Sunstein, Aaker, McClure.
- [`skills/roles/cio/`](./skills/roles/cio/) — infrastructure, vendor selection, security posture, cost optimization, incident response, observability, platform engineering. Draws on AWS Well-Architected, Google SRE, DORA / Accelerate, FinOps Foundation, NIST.
- [`skills/roles/caio/`](./skills/roles/caio/) — AI strategy, model selection economics, RAG architecture, prompt design, eval discipline, agents, AI governance (EU AI Act, NIST AI RMF). Draws on Anthropic / OpenAI / Google docs, Christensen on JTBD applied to AI, and the operator AI canon.
- [`skills/roles/cso/`](./skills/roles/cso/) — where-to-play / how-to-win, wedge identification, competitive response, partnership evaluation, market entry, big-bet framework. Draws on Porter, Lafley & Martin, Rumelt, Wack on scenarios, Klein on pre-mortems.
- [`skills/roles/cxo/`](./skills/roles/cxo/) — UX, activation, cohort retention, the four kinds of churn, NPS done right, customer success economics, funnel diagnostic. Draws on McClure (pirate metrics), Reichheld (NPS), Eyal (Hooked), Skok (SaaS metrics), Fitzpatrick (customer interviewing).
- [`skills/roles/chro/`](./skills/roles/chro/) — hiring, classification (ABC test, IR35), compensation bands, performance management, offer letters, severance, layoff playbook. Jurisdiction-aware; cross-routes to CLC for legal exposure.
- [`skills/roles/clc/`](./skills/roles/clc/) — Chief Legal Counsel framing (NOT legal advice). Contracts (MSA, NDA, SOW), IP (trademark, copyright, patent, trade secret, IP assignment), privacy (GDPR, CCPA, EU AI Act), corporate, securities, employment-legal, regulatory, litigation framing. Risk-tier triage (red/yellow/green) on every reply, explicit hand-off to licensed counsel where required.
- [`skills/roles/ceo/`](./skills/roles/ceo/) — synthesis when functional roles disagree, irreducible-question framing, founder-mode patterns, decision-memo template. Intentionally lighter than functional roles — the CEO integrates rather than competes with depth.

**The CLC skill provides operator-grade legal framing, not legal advice.** Practicing law is licensed and jurisdiction-specific.

Each deep skill ships with:

- A **REFERENCE** layer of frameworks with numerical thresholds and citations.
- A **heuristics** layer for fast triage and bias-catching.
- **Templates** — fillable artifacts (runway model, unit economics sheet, pricing canvas, capital allocation matrix, positioning statement, JTBD canvas, channel portfolio).
- **Playbooks** — procedural workflows (monthly close, fundraise prep, cost-cut decision, repositioning, channel allocation).
- **Worked examples** — end-to-end scenarios showing the framework being applied with real numbers.
- **References** — citations to the body of work each framework draws from.

This is what differentiates Sabha from a system prompt. The protocol routes; the deep skills *answer*.

## Does it actually work?

**Sabha-vs-baseline at n=50 (v3 rubric, Anthropic judge, 2026-05-18): 48/50 pairwise (96%), Wilson 95% CI [86.5%, 98.9%].** Lower bound jumped from 64% at n=20 to 86.5% at n=50 — direction was already clear; magnitude is now defensible. Per bucket:

- Original operator questions: **19/20 (95%)**
- Adversarial reframing (challenge-the-premise tests): **10/10 (100%)** — closes the v1.3.1 historical loss pattern at scale
- Cross-role / edge: **10/10 (100%)**
- Underdog (definitional / lookup where baseline should be competitive): **9/10 (90%)** — Sabha generalizes beyond its sweet spot

Methodology: 50 operator-style questions across 4 buckets, 2 conditions per question (no-system-prompt baseline vs Sabha charter loaded), 5-axis rubric + pairwise preference, judged by Claude Opus 4.7. The **v3 sub-axis rubric** decomposes 3 previously-saturated axes (decisiveness, tradeoff_named, length_discipline) into 5 binary sub-criteria each. **Cross-model judge harness** supports `--judge-provider {anthropic,openai,google}` to defeat in-family bias — cross-model run pending. The two losses (`cso-02`, `under-05`) are catalogued and traceable; details in [`docs/EVALS.md`](./docs/EVALS.md). Reproducible: harness, questions, and results are committed.

Methodology, rubric, and limitations: [`evals/README.md`](./evals/README.md). Run it yourself:

```bash
pip install -r evals/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python evals/run_eval.py
```

Results are committed to [`evals/results/`](./evals/results/). The interpretation — what the numbers mean, where the protocol fails, what's roadmapped — is in [`evals/ANALYSIS.md`](./evals/ANALYSIS.md). If the numbers don't move, the protocol isn't earning its keep — that data lives in the repo, not in marketing copy.

## What's in this repo

```
sabha-os/
├── CLAUDE.md                          # The protocol — this IS Sabha
├── .claude-plugin/
│   ├── plugin.json                    # Claude Code plugin manifest
│   └── marketplace.json               # Marketplace manifest (ships sabha-os + sakthi-graph)
├── skills/
│   ├── sabha-router/SKILL.md          # Forces the routing on every reply
│   └── roles/                         # 9 deep skills (one per role)
│       ├── cfo/                       # runway · pricing · unit economics · capital allocation
│       ├── cmo/                       # positioning · JTBD · channels · behavioral pricing
│       ├── cio/                       # infra · vendors · SRE · FinOps · incidents
│       ├── caio/                      # LLM strategy · RAG · evals · model selection · governance
│       ├── cso/                       # where-to-play · wedge · partnerships · scenarios
│       ├── cxo/                       # activation · retention · churn · NPS · customer success
│       ├── chro/                      # hiring · classification · comp · performance · severance
│       ├── clc/                       # contracts · IP · privacy · corporate · regulatory (NOT legal advice)
│       └── ceo/                       # synthesis · founder-mode · decision memos
├── commands/
│   ├── engage.md                      # /engage — switch to engage mode
│   ├── ask.md                         # /ask — back to chat mode
│   └── route.md                       # /route <ROLE> — force a specific role
├── docs/
│   ├── QUICKSTART.md                  # No-install path for non-technical users
│   ├── ARCHITECTURE.md                # Full system view (folder → graphify → sittham → Sakthi → Sabha)
│   ├── ROLES.md                       # The 9 roles, voices, and what each deep skill ships
│   ├── MEMORY-OPTIONS.md              # Claude Memory vs Sakthi vs mem0/Letta vs plain markdown — pick-by-need
│   ├── FOR-REGULATED-INDUSTRIES.md    # Health, legal, finance, defense — local-first posture + compliance framing
│   ├── CUSTOMIZATION.md               # Renaming roles, swapping memory, multiple Sabhas
│   ├── PHILOSOPHY.md                  # Why these 5 disciplines; the Chanakya tradition
│   ├── EVALS.md                       # Eval methodology + results summary
│   ├── ROADMAP.md                     # What's shipped, Q3 bets, founder-level overrides
│   └── BACKLOG.md                     # Captured ideas; trigger conditions for promotion to roadmap
├── examples/
│   ├── personal-sakthi.CLAUDE.md      # Life council (Health · Finance · Family · Career · Time · Self)
│   ├── professional-sakthi.CLAUDE.md  # C-suite council (default — 9 roles)
│   ├── developer-sakthi.CLAUDE.md     # Code council (Architect · Reviewer · Security · QA · Mentor)
│   ├── solo-founder.CLAUDE.md         # Profession preset
│   ├── agency.CLAUDE.md               # Profession preset
│   └── researcher.CLAUDE.md           # Profession preset
├── evals/
│   ├── questions.yaml                 # 50 operator-style questions (4 buckets)
│   ├── run_eval.py                    # The harness (with --resume + retries)
│   ├── judge.py                       # LLM-as-judge rubric + pairwise
│   ├── README.md                      # Methodology
│   ├── ANALYSIS.md                    # Results interpretation
│   └── results/                       # JSON + Markdown reports
├── LICENSE                            # MIT, © 2025-2026 Durai Rajamanickam (@rdmurugan)
├── PRIVACY.md                         # No data collection. Local-first by design.
├── CHANGELOG.md
├── CONTRIBUTING.md
└── README.md
```

## Optional: `/chanakya` — add a Chanakya Neeti verse to a reply

A purely opt-in skill layers exactly one verse from Chanakya's *Neeti* on top of the routed role's answer. Fires only when explicitly invoked — `/chanakya`, "add a Chanakya verse", or "what would Chanakya say." 76 verses across all 9 role domains. A [dedicated eval](./evals/chanakya/) (v2 grader, 2026-05-17, 7 questions): **activation 4/4 (incl. an adversarial branch-naming case where the model gracefully bridged the metaphor), discipline 2/3, attribution-accuracy 100% with the skill loaded vs. 0% without.** The one discipline failure (cofounder-conflict topic that "looked Chanakya-shaped" leaked a verse without invocation) drove a guardrail tightening in `skills/chanakya-neeti/SKILL.md` to make topic-relevance an explicit anti-pattern. Re-eval pending.

```
/chanakya
Should we accept the term sheet at a 30% down round, or push back?

Routing: CFO.

> *"Wealth comes from circulating, not from hoarding."*
> — Chanakya Neeti 5.12

Take the round. Push back only on the no-shop and the liquidation
preference. You lose option value on price; you gain 18 months. Worth it
because a runway you don't have isn't optionality.
```

See [`skills/chanakya-neeti/SKILL.md`](./skills/chanakya-neeti/SKILL.md) for the full verse corpus and activation rules.

## Documentation map

| Doc | What's in it |
|---|---|
| [`docs/CONTEXT.md`](./docs/CONTEXT.md) | **Single-document context reference.** Self-contained, dense, paste-into-any-AI-surface. Use to bring a fresh Claude.ai / Cowork / ChatGPT session up to speed on the whole project in one shot. |
| [`docs/QUICKSTART.md`](./docs/QUICKSTART.md) | No-install path. 10 minutes inside Claude.ai. For non-developers. |
| [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) | The full system: how the council, memory, and corpus-ingest layers compose. |
| [`docs/ROLES.md`](./docs/ROLES.md) | The 9 roles, their voices, and what each deep skill ships. |
| [`docs/MEMORY-OPTIONS.md`](./docs/MEMORY-OPTIONS.md) | Memory backend comparison — Claude Memory, Sakthi, mem0, Letta, plain markdown. Pick-by-need. |
| [`docs/FOR-REGULATED-INDUSTRIES.md`](./docs/FOR-REGULATED-INDUSTRIES.md) | For healthcare, legal, finance, defense — local-first posture, threat model, compliance framing. |
| [`docs/CUSTOMIZATION.md`](./docs/CUSTOMIZATION.md) | Renaming roles, swapping memory MCPs, multiple Sabhas, sharing presets. |
| [`docs/PHILOSOPHY.md`](./docs/PHILOSOPHY.md) | Why these 5 disciplines. What Sabha is and isn't. The Chanakya tradition. |
| [`docs/EVALS.md`](./docs/EVALS.md) | Eval methodology, current results, how to run it yourself. |
| [`docs/ROADMAP.md`](./docs/ROADMAP.md) | What's shipped, what's bet on Q3, what comes next. Founder-level overrides logged here. |
| [`docs/BACKLOG.md`](./docs/BACKLOG.md) | Ideas captured but not yet ranked. Includes trigger conditions for promotion to roadmap. |
| [`CONTRIBUTING.md`](./CONTRIBUTING.md) | PR conventions; what kinds of contributions help. |
| [`PRIVACY.md`](./PRIVACY.md) | No data collection. Local-first by design. |
| [`CHANGELOG.md`](./CHANGELOG.md) | Version history. |

## Sister project: Sabha Code (for GitHub Copilot users)

If you also use GitHub Copilot — for engineering work rather than C-suite operator decisions — there's a developer-focused sibling: [**Sabha Code**](https://github.com/rdmurugan/sabha-code). Same Chanakya tradition. Different role set (Architect / Reviewer / Security / Performance / QA / Mentor / Tech Lead). Different surface (`.github/copilot-instructions.md` instead of a Claude Code plugin).

The two projects are independent but complementary:
- **Sabha OS** (this repo) — for non-engineering decisions in Claude Code (pricing, hiring, strategy, contracts)
- **Sabha Code** — for engineering decisions in GitHub Copilot (architecture, code review, security, performance)

**Sabha Code's own eval (n=30, 2026-05-18, same v3 sub-axis rubric methodology):** 28/30 pairwise (93.3%, Wilson 95% CI [78.7%, 98.2%]); role-core bucket 20/20 = 100%. The two projects' Wilson CIs overlap substantially — directional evidence the protocol shape generalizes from operator work to engineering work.

Install Sabha Code alongside Sabha OS if you straddle both worlds:

```bash
# In any repo where you use Copilot
npx degit rdmurugan/sabha-code .github
```

## Compatibility

- Claude Code (any version with plugin support)
- Claude.ai Projects
- Cowork mode
- Claude API (as system prompt)
- Works with any Claude model — Opus, Sonnet, Haiku

## Contributing

PRs welcome. Especially: new council presets for professions or life situations we haven't covered, memory MCP integration snippets, real usage stories.

## License

MIT. See [LICENSE](./LICENSE). Use it, fork it, sell services on top of it — just keep the copyright notice.

## Credits

Designed and developed by **Durai (@rdmurugan)** as a solo project — protocol, deep skills, eval harness, plugin packaging, and the Sakthi Graph fork. MIT-licensed, started October 2025. The protocol is distilled from many sources — C-suite operating experience, decision-making heuristics, the Chanakya tradition of advisor-counsel, and knowledge shared across the open internet. Contributions welcome.

Copyright © 2025–2026 Durai (@rdmurugan). Released under MIT.

## Acknowledgments

Sabha OS is memory-MCP-agnostic — any layer that exposes search and write tools works. The examples in [`CLAUDE.md`](./CLAUDE.md) and [`skills/sabha-router/SKILL.md`](./skills/sabha-router/SKILL.md) use [Sakthi Graph](https://github.com/rdmurugan/sakthi-graph) (MIT) to show concrete tool calls, but the same pattern applies to mem0, Letta, Zep, Pieces, or a plain `memory/` folder. Thanks to the open-source memory-MCP projects that make a locally-owned Sakthi possible.
