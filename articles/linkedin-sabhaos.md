# Sabha OS: How to Configure a C-Suite AI Council That Actually Recommends Instead of Lists

*LinkedIn Article · May 2026*

---

Most AI replies are *option-shaped*. You ask a business question — whether to match an engineer's competing offer, which pricing tier to set, how to handle a cash-flow crunch — and you get back a balanced survey. Five considerations. Hedged language. A nudge toward "it depends."

A real CFO says "match the offer, here's the math." A real CMO says "go to market on Channel X, here's why Channel Y is a trap." Sabha OS turns your AI assistant into a council that talks like that.

Here's what it is, how to configure it, and how to evaluate whether it's working.

---

## What Sabha OS Is

Sabha OS is an open-source system prompt protocol — a CLAUDE.md file you drop into your Claude workspace. No server. No third-party API subscription. No data leaving your machine.

When loaded, it routes every substantive question to a C-suite role before answering:

| Role | Domain |
|------|--------|
| **CFO** | Budget, runway, pricing, unit economics |
| **CIO** | Infrastructure, cloud, security, tooling |
| **CAIO** | AI strategy, model selection, RAG, agents |
| **CMO** | Marketing, positioning, content, channels |
| **CSO** | Strategy, competition, GTM, partnerships |
| **CXO** | UX, onboarding, retention, churn |
| **CHRO** | Hiring, comp, HR law, org design |
| **CLC** | Contracts, IP, privacy, compliance, regulatory |
| **CEO** | Cross-role synthesis, founder-level calls |

Every reply opens with `Routing: CFO.` or `Routing: CFO (primary). CHRO weighs in on comp structure.` — then commits to one recommendation, names the tradeoff explicitly, and stops.

---

## Step 1: Install in Under 10 Minutes

**Option A — Claude Code (marketplace)**

```bash
claude plugin marketplace add Infinidatum-LLC/sabhaos
claude plugin install sabha-os@sabha-marketplace
```

**Option B — Claude Desktop / Cowork**

Clone the repo and place CLAUDE.md in your project workspace. It auto-loads as the system prompt.

**Option C — API / any surface**

Copy the contents of CLAUDE.md and use it as your `system_prompt`. Zero runtime dependencies — it's text.

---

## Step 2: Define Your Known Entities

The most important customization step. Sabha's grounding discipline says: never invent facts about a named entity. To enforce that, you give it anchors.

In CLAUDE.md, replace the template with your actual profile cards:

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

### Active projects
- **Q3 enterprise launch** — 2/5 design partners signed.

### Obligations
- SOC 2 Type II due Q4 2026.
```

The council reads these and won't contradict them. If you ask a CFO question and haven't disclosed your burn rate, it asks rather than inventing a number.

---

## Step 3: Customize the Roles

The council is yours to reshape.

**Solo founder:** Collapse CFO+CSO into "Operator."

**Agency:** Rename CIO to "Creative Director." Add a "Client Lead" role.

**Personal life council:** Replace all nine with Health, Finance, Career, Family, Time, Self.

```markdown
# Personal council preset
| Role | Covers |
|------|--------|
| **Finance**  | Budget, savings, investments, real estate |
| **Health**   | Fitness, nutrition, sleep, medical decisions |
| **Career**   | Job strategy, skills, comp negotiation |
| **Family**   | Relationships, parenting, caregiving |
| **Time**     | Prioritization, habits, calendar, energy |
```

---

## Step 4: Wire Up Sakthi Graph (Optional, Recommended)

Sabha without memory is still significantly better than unstructured AI. With memory it's qualitatively different — a council that knows your company.

```bash
claude plugin install sakthi-graph@sabha-marketplace
uv tool install sakthi-graph
sakthi init --sabha ~/sakthi
```

This bootstraps nine role wings on your local machine. After each *engage* session, Sabha writes a diary entry to the lead role's wing. Over time:

- Your CFO knows your historical burn, open invoices, and prior pricing decisions
- Your CSO knows which market bets you killed and why
- Your CHRO knows your comp bands and hiring history

There's also a corpus-ingest verb — `sakthi sittham` — that takes any document folder and automatically routes its content into the right role wing. Run it on your market research docs and they land in the CMO wing. Run it on your financial models and they land in the CFO wing. The council becomes aware of what you've read.

The memory compounds. The more you use it, the sharper the council gets — locally, never in anyone's cloud.

---

## Step 5: Understand the Two Modes

**Ask mode (default):** A chat reply. No file produced. The right mode for 90% of questions.

**Engage mode:** A document-grade deliverable — `.docx` for formal reports, `.md` for everything else. Triggers when you say "file this," "engage," or "write it up," or when the decision has dollar/time/risk consequences.

Slash commands for Claude Code users:
- `/ask` — force ask mode
- `/engage` — force engage mode, produce a file
- `/route CFO` — override the classifier
- `/chanakya` — add a Chanakya Neeti verse to this reply (opt-in; draws from a 76-verse curated corpus)

---

## How to Evaluate If It's Working

The repo ships a built-in eval harness:

```bash
cd sabhaos
python -m venv .venv && source .venv/bin/activate
pip install -r evals/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python evals/run_eval.py --limit 5   # smoke test
python evals/run_eval.py              # full 50-question run
```

The harness sends 50 operator-style questions to the same model twice — baseline (no system prompt) vs. Sabha — then has Claude Opus 4.7 score each reply on five axes and pick a pairwise winner.

The 50 questions span four stress buckets: original operator questions, adversarial-reframing (designed to trap Sabha into applying structure when reframing was needed), cross-role/edge cases, and underdog questions where baseline should be competitive.

### Current results (v3 eval, n=50, 2026-05-18)

| Metric | Baseline | Sabha | Δ |
|--------|----------|-------|---|
| decisiveness | — | — | +significant |
| concreteness | — | — | most discriminating axis |
| length_discipline | — | — | hardest axis |
| **total (20-pt scale)** | **12.18** | **16.96** | **+4.78** |

**Pairwise preference: 48/50 (96%)**, Wilson 95% CI [86.5%, 98.9%].

Stress-bucket breakdown:
- Original operator questions: **19/20 (95%)**
- Adversarial-reframing: **10/10 (100%)**
- Cross-role / edge: **10/10 (100%)**
- Underdog (definitional / lookup): **9/10 (90%)**

The two losses are catalogued: one was a harness bug (reply truncated at max_tokens, now in backlog); one was a legitimate loss on a definitional question where baseline added a framework attribution Sabha omitted. Neither is systemic.

Cost for a full run: ~$1–3 in API credits.

---

## What Sabha Is Not

- **Not domain expertise.** CFO framing isn't a CPA credential. It's the right framing. You still need licensed professionals for tax filings, legal opinions, regulated decisions.
- **Not a walled garden.** MIT license. No server. Your data never leaves your machine.
- **Not magic for every question.** Trivial lookups, pure coding tasks, and exploratory research don't benefit from routing. Sabha skips those automatically.

---

## The Shift in Practice

Before Sabha, I asked a pricing question and got five considerations. I made the call anyway.

After Sabha, I asked the same type of question and got: a recommendation (`$140/mo, not $120`), the math (monthly carries 2–4× churn vs. annual), the exact pricing page copy to ship, and a tradeoff named (`you may lose 1-in-10 price-sensitive leads — fine, you're optimizing for LTV`).

That's not a style difference. That's a different kind of tool.

---

**Sabha OS is MIT-licensed at [github.com/Infinidatum-LLC/sabhaos](https://github.com/Infinidatum-LLC/sabhaos).** Install via `claude plugin marketplace add Infinidatum-LLC/sabhaos` or paste CLAUDE.md into any Claude surface. The council is live in under 10 minutes.

Your Sakthi compounds. Build it intentionally.

---

*Have you built something similar — role-structured prompting, local memory for AI, council-style multi-agent systems? I'd like to compare notes. Comments open.*
