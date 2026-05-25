# Sabha OS: A Reproducible, Eval-Backed C-Suite AI Council in a Single System Prompt

*Medium · Technical · May 2026*

---

**TL;DR:** Sabha OS is an open-source protocol that turns a Claude workspace into a role-routed C-suite council. It produces decisive, tradeoff-aware, concrete replies instead of hedged option surveys. A reproducible eval (n=50, four stress buckets, LLM-as-judge) shows **96% pairwise preference** (48/50, Wilson 95% CI [86.5%, 98.9%]) for Sabha over baseline, with a +4.78 rubric improvement on a 20-point scale. The protocol is a CLAUDE.md file — no server, no data egress, MIT license. Here's how it works, how to configure it, and what the numbers actually say.

---

## Background: why role-routing matters

The core problem with general-purpose AI for business decisions isn't accuracy — it's *framing*. The same model that can pass a bar exam defaults to option-shaped replies for load-bearing questions. "Should I match the engineer's competing offer?" should produce a CFO/CHRO decision, not a five-consideration balanced view. The latter wastes cognitive load; the former is what an actual advisor delivers.

Sabha OS addresses this with a structural intervention: every substantive question is classified to a C-suite role *before* the answer is generated. The role commits the model to a domain, a recommendation posture, and a tradeoff-naming discipline. The result is systematically different output — measurably so.

This is not a persona hack or a character prompt. The roles aren't backstories — they're job functions with domains, decision heuristics, and full playbook libraries. The protocol is also memory-backend-agnostic: it works with Claude Memory, Sakthi Graph (local-first), mem0, Letta, Zep, plain markdown, or nothing at all.

---

## Architecture overview

Sabha OS has three layers:

```
┌─────────────────────────────────────────────────┐
│  CLAUDE.md  (system prompt — the protocol)      │
│  ┌──────────────────────────────────────────┐   │
│  │  1. Classify → route to role             │   │
│  │  2. Check memory before asserting facts  │   │
│  │  3. Answer in role voice:                │   │
│  │     - Recommend, don't survey            │   │
│  │     - Name the tradeoff                  │   │
│  │     - Concrete over abstract             │   │
│  │  4. Ask mode vs. Engage mode             │   │
│  └──────────────────────────────────────────┘   │
├─────────────────────────────────────────────────┤
│  Deep skills  (skills/roles/<role>/)            │
│  ┌──────────────────────────────────────────┐   │
│  │  SKILL.md — role activation instructions │   │
│  │  REFERENCE.md — frameworks + canon       │   │
│  │  heuristics.md — fast-lookup rules       │   │
│  │  templates/ — fillable frameworks        │   │
│  │  playbooks/ — end-to-end procedures      │   │
│  │  worked-examples/ — concrete prior art   │   │
│  │  data-hooks/ — live MCP grounding docs   │   │
│  └──────────────────────────────────────────┘   │
├─────────────────────────────────────────────────┤
│  Sakthi Graph  (optional local memory MCP)      │
│  ┌──────────────────────────────────────────┐   │
│  │  9 wings (one per role)                  │   │
│  │  diary entries per engage session        │   │
│  │  entity knowledge graph                  │   │
│  │  sittham — corpus ingest verb            │   │
│  │  32 MCP tools exposed                    │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

The protocol lives entirely in the system prompt. Deep skills are loaded by the router when the question's domain matches a role's directory. Sakthi Graph runs locally and is optional — Sabha works without it, degrading to session-only memory.

---

## The nine default roles

| Role | Domain | Voice (one-line) |
|------|--------|-----------------|
| **CFO** | Budget, pricing, runway, unit economics | "Numbers first. Runway in months, not 'comfortable cash position'." |
| **CIO** | Infrastructure, cloud, security, devops | "Names the actual tool. Has opinions about cost per GB." |
| **CAIO** | AI strategy, model selection, RAG, evals | "Names the actual model. Doesn't oversell LLMs." |
| **CMO** | Marketing, positioning, JTBD, channels | "Names the channel and the message. Allergic to jargon." |
| **CSO** | Strategy, competition, GTM, partnerships | "Asks 'what does winning look like' before tactics." |
| **CXO** | UX, onboarding, retention, churn | "Talks about the user's next click, not 'the experience'." |
| **CHRO** | Hiring, comp, HR law, org design | "Knows employment law is jurisdiction-specific. Flags lawyer." |
| **CLC** | Contracts, IP, privacy, compliance, regulatory | "Risk-tier triage (RED/YELLOW/GREEN). NOT legal advice." |
| **CEO** | Cross-role synthesis, founder-level judgment | "Names the irreducible tradeoff. Tells the user when it's their call." |

Each role's `skills/roles/<role>/` directory contains: `SKILL.md` (activation rules), `REFERENCE.md` (multi-framework knowledge base with numerical thresholds and citations), `heuristics.md` (fast-lookup decision rules), `templates/` (fillable frameworks — runway model, unit economics, positioning statement, JTBD canvas, contract redline package), `playbooks/` (end-to-end procedures), `worked-examples/` (prior art with real numbers), and `data-hooks/` (docs for grounding answers in live MCP data — Stripe for CFO, Google Analytics for CMO).

---

## The naming layer (Sanskrit/Tamil)

The four terms in the stack are worth understanding — they're not decorative:

| Term | Script | Meaning | Role in stack |
|------|--------|---------|--------------|
| **Sabha** | सभा / சபை | council / assembly | the routing protocol |
| **Chanakya** | चाणक्य / சாணக்கியர் | the 4th c. BCE strategist | the voice / archetype |
| **Sakthi** | शक्ति / சக்தி | power / accumulated capacity | the local memory |
| **Sittham** | चित्त / சித்தம் | consciousness / awareness | the corpus-ingest verb |

The metaphor is load-bearing: Sakthi is your accumulated power (memory). Sittham is what that memory is aware of (the corpora you've absorbed). Sabha is how the council uses both. Chanakya is the voice it speaks in.

---

## Configuration

### Minimum setup (10 minutes)

```bash
# Claude Code
claude plugin marketplace add Infinidatum-LLC/sabhaos
claude plugin install sabha-os@sabha-marketplace

# Any other surface: paste CLAUDE.md as system prompt
# git clone https://github.com/Infinidatum-LLC/sabhaos
```

### Entity table (required customization)

Replace the template in CLAUDE.md with your actual profile cards:

```markdown
### People
- **Alice** — me. Solo founder, CEO. Background: enterprise SaaS.
- **Bob** — CTO. Joined 2024. Owns engineering. Equity: 30%.

### Company
- **Acme Co.** — Delaware C-corp. $600K ARR, ~15%/mo growth.
  Mercury (operating), SVB (reserve). $32K/mo burn.

### Products
- **Acme Cloud** — $1,200/yr, 82% gross margin.
  ICP: 5–50 person eng teams.
- **Acme Sandbox** — free tier. 60% of qualified pipeline.

### Active projects
- **Q3 enterprise launch** — 2/5 design partners signed.
- **Onboarding rewrite** — ships Q2, target: 32% → 50% activation.

### Obligations
- SOC 2 Type II due Q4 2026.
```

Grounding discipline is strict: if an entity is named in a reply but not in the profile cards, Sabha either asks for clarification or explicitly flags the number as an estimate. It won't invent facts about your company.

### Sakthi Graph (optional, recommended)

```bash
claude plugin install sakthi-graph@sabha-marketplace
uv tool install sakthi-graph
sakthi init --sabha ~/sakthi   # bootstraps 9 role wings
```

The 32 MCP tools include:

- `sakthi_search` — semantic search across wings. Pass `wing` and `room` for targeted retrieval.
- `sakthi_kg_query` — entity lookup. Used before asserting facts about known entities.
- `sakthi_diary_write` — records the session decision at the end of engage mode.
- `sakthi_sittham` — corpus ingest: takes a graphified folder, auto-routes to the dominant role wing.

### Corpus ingest with `sittham`

```bash
/graphify ~/path/to/corpus          # one-time prep: any folder → knowledge graph
sakthi sittham ~/path/to/corpus     # auto-routed to the right role wing

# Preview routing before committing
sakthi sittham <path> --dry-run

# Override when auto-routing is wrong
sakthi sittham <path> --wing cfo --room pricing
```

Content is scored against the 9 role vocabularies via keyword matching; the dominant role's `decisions` room receives a compact drawer. Weak or split signals fall back to `ceo/synthesis-notes`. The council becomes aware of what you've fed it — and stays honest about what it hasn't seen.

### Custom role tables

```markdown
# Agency preset
| Role | Covers |
|------|--------|
| **Creative Director** | Visual design, creative strategy, brand voice |
| **Producer** | Project delivery, timelines, client management |
| **Growth** | New business, marketing, channel strategy |
| **Ops** | Finance, HR, tooling, vendor management |
| **Counsel** | Contracts, IP, NDAs, legal risk |
```

---

## The routing engine

The classifier is the CLAUDE.md itself — no code, no separate inference call. The model reads the role table, classifies the question inline, and declares the route at the top of the reply:

```
Routing: CFO (primary). CHRO weighs in on comp structure.

[Recommendation — one clear direction, not a survey]

[Math or evidence supporting the recommendation]

[Tradeoff: what you give up by taking this path]

[Next move: the specific action, today]
```

The two output modes:

**Ask mode (default):** Inline chat reply. No file. Most questions.

**Engage mode:** Triggered by "file this," "engage," "write it up," or stakes (dollar/time/risk consequences). Produces `.docx` for formal exec reports, `.md` for everything else. Also writes a diary entry to Sakthi.

Optional `/chanakya` skill overlays exactly one verse from a 76-verse Chanakya Neeti corpus on top of the role's reply. Opt-in only; it passed 4/4 activation tests and 3/3 discipline tests (model does not auto-fire it on strategic questions without explicit invocation).

---

## Evaluation methodology

### Setup

- **Candidate model:** `claude-sonnet-4-6`
- **Judge model:** `claude-opus-4-7` (different class — reduces same-model bias)
- **Question set:** 50 questions across 4 stress buckets, v3 rubric
- **Conditions:** Baseline (no system prompt) vs. Sabha (CLAUDE.md as system prompt)
- **Judge axes:** decisiveness, tradeoff_named, concreteness, routing_present (binary), length_discipline — each 0-5 (except binary), total 20-point scale
- **Pairwise judge:** separate judge call sees both replies in randomized order, picks the one a busy operator would find more useful
- **Reproducibility:** `pip install -r evals/requirements.txt && python evals/run_eval.py` — checkpointed, resumable, ~$1-3 per full run

### The four stress buckets

| Bucket | n | Design intent |
|--------|---|--------------|
| Original operator questions | 20 | Real decisions a founder or operator would face |
| Adversarial-reframing | 10 | Designed to trap Sabha into applying structure when reframing the question was more valuable |
| Cross-role / edge | 10 | Questions spanning multiple roles or sitting in gray zones between them |
| Underdog | 10 | Definitional or lookup questions where baseline should be competitive |

The adversarial bucket specifically targets the failure mode surfaced in the v1.3.1 eval (n=20, 85% pairwise): Sabha applied formal structure to three questions where the baseline won by *challenging the premise* instead. The v3 protocol closed that gap.

### Results — headline

| Metric | Baseline | Sabha | Δ |
|--------|----------|-------|---|
| total (20-pt scale) | 12.18 | 16.96 | +4.78 |
| **pairwise wins** | **2/50 (4%)** | **48/50 (96%)** | — |
| Wilson 95% CI | — | [86.5%, 98.9%] | — |

### Per stress-bucket breakdown

| Bucket | Sabha wins | Baseline wins |
|--------|-----------|--------------|
| Original operator (n=20) | 19/20 (95%) | 1/20 |
| Adversarial-reframing (n=10) | 10/10 (100%) | 0/10 |
| Cross-role / edge (n=10) | 10/10 (100%) | 0/10 |
| Underdog (n=10) | 9/10 (90%) | 1/10 |

### Per-role breakdown

8/9 roles at 100% pairwise win rate. CSO is the only role under 100% (4/6 wins). Both CSO losses are traceable: one was a harness bug (reply truncated at max_tokens, backlogged); one was a legitimate loss on a definitional question where the baseline added a Lafley & Martin framework attribution that Sabha omitted.

### The two losses — both catalogued

| Question | Why baseline won |
|----------|-----------------|
| `cso-02` | Harness bug — Sabha reply was truncated at max_tokens. Not a substantive loss. Fix is in BACKLOG. |
| `under-05` | Legitimate loss — definitional question where baseline added a framework attribution Sabha omitted. Traceable, not systemic. |

Neither loss reflects a systematic protocol failure. The adversarial-reframing bucket — built specifically to expose the v1 failure mode — held at 10/10.

### Retired baselines

- **v1.3.1 (n=20, 85% pairwise, +5.95 rubric)** — retired. Rubric saturated on decisiveness and tradeoff_named. Small n, no stress buckets.
- **v2 (n=20 re-run with all deep skills, 85% pairwise, +4.85 rubric)** — retired. Same rubric issues.

Numbers preserved in `evals/results/2026-05-14.json` and `2026-05-16.json` for audit. **Do not carry forward as current claims.**

### Methodology caveats (honest)

1. **LLM-as-judge has known biases** — verbosity preference, position effects. Mitigated by rubric + randomization, not eliminated.
2. **In-family judge.** Opus 4.7 judging Sonnet 4.6. Both Claude. Different class reduces self-bias; doesn't eliminate it. Cross-family judging run is the next pending credibility move.
3. **v3 sub-axis rubric prompt:** Opus 4.7 emitted JSON in v2 flat shape (reasoned about sub-criteria internally but didn't structure output). Fallback in `score_reply` handled it cleanly. Sub-axis slicing unavailable for this run. Tightening the judge prompt for structured output is in BACKLOG.
4. **Tested on Claude only.** The protocol likely transfers to other LLMs; cross-model data is not yet published.

---

## Reproducible claims for external citation

**One sentence:**
> *Sabha replies preferred 48/50 pairwise (96%, Wilson 95% CI [86.5%, 98.9%]) over baseline across a 50-question eval with four stress buckets — including adversarial-reframing and underdog questions — judged by a different Claude model class (Opus on Sonnet). Two losses are catalogued and traceable; neither is systemic.*

**For HN, with caveats:**
> *Headline: 96% pairwise preference (48/50) across a 50-question eval with four stress buckets: operator questions, adversarial-reframing, cross-role/edge, and underdog. Rubric improvement: +4.78 on a 20-point scale. Caveats: LLM-as-judge (Claude-on-Claude, different model class), v3 sub-axis rubric output not structured (fallback handled it). Two losses: one harness bug (max_tokens truncation), one legitimate definitional miss. Raw data, judge rationales, and harness all committed and reproducible: `python evals/run_eval.py`.*

---

## Side-by-side example (CFO question)

**Question:**
> *We have $180K in the bank, burn is $32K/month, and there's a $90K invoice that's been outstanding 40 days from a client we've worked with for two years. Should I take on a $40K bridge line of credit at 12% APR to cover payroll, or chase the invoice harder?*

**Sabha reply (condensed):**
> *Routing: CFO.*
>
> *Chase the invoice. The bridge line is a $4,800/year solution to a collections problem.*
>
> *Real runway: $180K / $32K = 5.6 months — below the seed-stage floor of 6 months. If the invoice clears: ($180K + $90K) / $32K = 8.4 months. The problem isn't structural; it's a receivables problem wearing a cash-flow costume.*
>
> *Call, don't email. Script: "We're 40 days out on the $90K. I need to understand what's holding it — approval queue, dispute, or cash-flow issue on your end?"*
>
> *Tradeoff: you're betting the client pays within 30 days. Set a 10-day internal deadline: if no commitment, open the credit line and escalate to a collections demand letter simultaneously.*
>
> *Next move: call today. Payment date in writing by end of week.*

**Pairwise winner:** Sabha — decisive, concrete script, specific fallback math, named trigger (10-day deadline).

---

## Roadmap

| Priority | Move | Signal |
|----------|------|--------|
| 1 | Cross-family judge run (GPT or Gemini judging Sonnet) | Removes in-family bias from the credibility claim |
| 2 | Tighten v3 judge prompt for structured sub-axis output | Sub-axis slicing currently unavailable |
| 3 | Fix max_tokens harness bug (cso-02) | Removes known harness artifact from results |
| 4 | Premium skill packs (SaaS-CFO, healthcare-CLC) — scaffold only | Validates commercial overlay without committing content |
| 5 | Council preset expansion (lawyer, healthcare-founder, indie-dev) | Responding to pull from early users |

**Held by founder:** LLM-agnostic SDK (Anthropic + OpenAI + Google adapters + cross-model eval) — the council recommended Q3 2026; founder held it. Sabha stays Claude-focused for now. Recorded in `docs/ROADMAP.md`.

---

## What Sabha is not

- **Not domain expertise.** CFO framing isn't a CPA credential. License-regulated decisions still need licensed professionals.
- **Not a chain-of-thought hack.** It changes what the model outputs, not how it reasons internally.
- **Not a personality skin.** Roles are job functions, not characters. CIO doesn't have a backstory; CIO has a domain.
- **Not tested on non-Claude models.** Transfer is likely but unmeasured. Cross-model data is the next pending work.
- **Not hosted anywhere.** No cloud product; defeats the local-first thesis.

---

## Get started

```bash
# Install
claude plugin marketplace add Infinidatum-LLC/sabhaos
claude plugin install sabha-os@sabha-marketplace

# Optional: add local memory
claude plugin install sakthi-graph@sabha-marketplace
uv tool install sakthi-graph
sakthi init --sabha ~/sakthi

# Run the eval on your own questions
cd ~/.claude/plugins/cache/sabha-marketplace/sabha-os
python -m venv .venv && source .venv/bin/activate
pip install -r evals/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python evals/run_eval.py --limit 5   # smoke test (~$0.10)
python evals/run_eval.py              # full 50-question run (~$1-3)
```

MIT license. No server. No data egress. The council is yours.

---

*Raw eval data: `evals/results/2026-05-16.json` in the repo. Every claim in this article is cited to that file or to `evals/ANALYSIS.md`. The methodology is in `evals/README.md` and `docs/EVALS.md`. The v1.3.1 numbers (n=20, 85% pairwise) are preserved in `evals/results/2026-05-14.json` for audit but are retired as current claims.*

*Sabha OS · [github.com/Infinidatum-LLC/sabhaos](https://github.com/Infinidatum-LLC/sabhaos) · MIT*
*Sakthi Graph · [github.com/Infinidatum-LLC/sakthi-graph](https://github.com/Infinidatum-LLC/sakthi-graph) · MIT*
