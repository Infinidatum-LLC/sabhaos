# Sabha OS — User Guide

> **For novice users after installation.** You've installed the Sabha OS plugin (or cloned the repo into your Claude Code config). This guide walks you from your first question to a council that genuinely knows your work — the **compounding intelligence loop** that makes Sabha different from a chatbot.
>
> **Reading time:** 25 minutes. **Time-to-first-useful-answer:** under 5 minutes. **Time-to-compounding:** about 3 weeks of regular use.

---

## What you'll learn

1. The mental model — you have a council, not a chatbot
2. Your first 5 minutes — verify install, ask the first question, see the role badge
3. The nine roles and when each is used
4. Ask mode vs. Engage mode — when each is appropriate
5. The slash commands you actually need
6. **Wiring up memory — the Sakthi Graph (or any memory MCP)**
7. **The compounding intelligence loop — why week-10 Sabha is qualitatively different from week-1**
8. Customizing the council for your work
9. Anti-patterns (what *not* to do)
10. Troubleshooting and going deeper

---

## 1. The mental model — you have a council, not a chatbot

Most AI replies are option-shaped: *"here are five approaches with pros and cons."* That's exhausting when you're actually trying to decide something.

Sabha forces a different shape:

```
Routing: CFO. Cut the SaaS line 40%. You lose the analytics tier.
         Worth it because that tier isn't driving renewals.
```

**Three things to notice:**

- **Routing line at the top.** Every substantive reply names which "role" answered — CFO, CMO, CIO, etc. You see the seat before the answer.
- **One recommendation, not five options.** The council is built to commit. If the question is genuinely a five-option tradeoff, the role names the tradeoff explicitly — never *"it depends."*
- **Named tradeoff.** Every recommendation says what you're giving up. The Chanakya tradition: decisive, but honest about cost.

Sabha is the *protocol* (how the council thinks). The **roles** are nine domain-specific advisors. The **memory** is whatever backend you pair with it — Claude Memory, Sakthi Graph, mem0, Letta, or a plain `memory/` folder. **Sabha is memory-MCP-agnostic.** This guide uses Sakthi Graph for the memory examples because it's the most full-featured open-source pairing, but every concept maps to the other backends.

---

## 2. Your first 5 minutes

### 2.1 Verify the install

Open a new Claude Code conversation in the directory where you installed Sabha OS. Ask:

```
What is the Sabha protocol?
```

You should see a reply that **does not** start with "Routing:" — because asking *about* Sabha is a meta-question, and the protocol exempts those. Good. The skill is loaded and self-aware.

Now ask something substantive:

```
Should I rewrite my product's authentication layer from scratch, or refactor in place?
```

You should see something like:

```
Routing: CIO (primary). CSO weighs in on the timing.

Refactor in place. You ship in 6 weeks instead of 6 months,
keep your existing test surface, and don't burn the team on
a rewrite that historically slips 3×. You lose the chance to
clean up the deeper schema debt — worth it because that debt
isn't blocking the next two quarters.
```

**If you see the routing line** — Sabha is working. If you see a generic answer with no routing, the skill isn't loading. Skip to §10 Troubleshooting.

### 2.2 Try a different role

```
What's a reasonable runway floor before approving a new hire?
```

Routing should switch to **CFO**. You should get a number with reasoning, not a survey of frameworks.

### 2.3 Try the override

```
/route CHRO
What's a reasonable runway floor before approving a new hire?
```

Same question, but you forced the **CHRO** seat. The answer will frame the same problem through hiring-process and labor-cost lenses, not cash-floor lenses. This is how you steer the council when you disagree with the auto-routing.

You're done with the first 5 minutes. Sabha works.

---

## 3. The nine roles and when each is used

| Role | When it picks up the question | Example trigger phrase |
|---|---|---|
| **CIO** | Infrastructure, deployment, hosting, security, IT, vendors | *"Should we move off AWS?"* |
| **CAIO** | AI strategy, model selection, LLMs, RAG, evals, agents | *"Which model for our RAG pipeline?"* |
| **CFO** | Budget, pricing, runway, cash, P&L, taxes | *"Can we afford a marketing hire?"* |
| **CMO** | Marketing, brand, content, channels, lead gen, copy | *"What's our positioning vs. Competitor X?"* |
| **CSO** | Strategy, competition, GTM, partnerships, growth, big bets | *"Should we enter the EU market?"* |
| **CXO** | UX, onboarding, retention, churn, service delivery | *"Why is our 30-day retention dropping?"* |
| **CHRO** | HR, hiring, payroll, labor law, contractors, org design | *"Can a 17-year-old be a W-2 employee?"* |
| **CLC** | Contracts, IP, privacy/compliance, regulatory, securities | *"Is our DPA template GDPR-current?"* |
| **CEO** | Synthesis when roles disagree, or founder-level judgment | *"Should we take the acquisition offer?"* |

You don't memorize this. **You ask the question, the protocol routes.** The table is for when you want to predict who'll answer.

**Multi-role replies are common.** A question like *"Should we acquire Competitor X?"* might route as:

```
Routing: CSO (primary). CFO weighs in on cash impact.
         CLC weighs in on antitrust exposure.
```

Read the primary answer first, then the advisory voices.

---

## 4. Ask mode vs. Engage mode

Sabha has two modes. Picking the right one is the single most useful discipline you can build.

### Ask mode (default)

A chat reply. Inline. No file produced. **Most questions live here.**

Use ask mode when:
- You're thinking out loud
- You want a quick recommendation
- You're not sure if you'll act on the answer
- The decision is reversible

### Engage mode

A document-grade deliverable. `.docx` for formal executive reports; `.md` for everything else. **Use Engage mode when the output needs to survive the conversation.**

Trigger Engage mode by:

- Saying *"file this"*, *"make it a goal"*, *"write it up"*, *"draft a memo"*, *"engage"*
- Using the explicit `/engage` slash command
- The decision has dollar, time, or risk consequences worth recording
- The output will be sent to a third party (investor, board, vendor, customer)

In Engage mode, Sabha will:
1. Produce the actual `.docx` or `.md` file
2. Write a one-paragraph diary entry to your memory backend so the decision compounds
3. Tell you the file path

**Heuristic when in doubt:** stay in ask mode. At the end, ask Sabha *"want me to engage this as a memo?"*

---

## 5. The slash commands you actually need

There are four. Memorize these and ignore the rest.

| Command | What it does | When to use |
|---|---|---|
| `/ask` | Force ask mode (chat only, no file) | When you don't want Sabha to produce a file even if your phrasing sounds engagement-y |
| `/engage` | Force engage mode (produce a file + diary entry) | When you want a deliverable |
| `/route CFO` | Override the auto-routing — replace `CFO` with any role code | When you disagree with which seat is answering |
| `/chanakya` | Add a Chanakya Neeti verse on top of the role's reply | When you want classical-strategist flavor on a substantive answer |

That's it. Everything else is decoration.

---

## 6. Wiring up memory — the Sakthi Graph

This is the step that turns Sabha from "well-styled chatbot" into a compounding intelligence.

Without memory, every conversation starts from zero. The council can be sharp inside one chat, but it forgets you the moment you close the window.

With memory wired up, the council:

- Remembers your projects, people, products, and obligations
- Recalls prior decisions when a related question comes up
- Updates its understanding when something changes
- Refuses to invent facts about entities it has on file (the "grounding discipline")

### 6.1 What "memory" actually means

Sabha is **memory-MCP-agnostic**. Five reasonable options exist:

| Backend | Best for | Setup |
|---|---|---|
| **Claude Memory** | Most users — zero config | Already on by default in claude.ai / Claude Code |
| **Sakthi Graph** | Local-first, privacy-sensitive, power users | `uv tool install sakthi-graph && sakthi init --sabha ~/sakthi` |
| **mem0 / Letta / Zep / Pieces** | You already use one | Install the relevant MCP, name swap in your config |
| **Plain `memory/` folder** | Minimalist, no MCP | Create `memory/` in your project, write markdown files |
| **Nothing** | Just trying Sabha out | Skip this section, the council still works (just doesn't compound) |

This guide uses **Sakthi Graph** for the rest of the examples because it's the most full-featured open-source pairing and matches the protocol's design tightly. Substitute your backend's tool names where appropriate.

### 6.2 Install Sakthi Graph

```bash
# Install (one-time)
uv tool install sakthi-graph

# Bootstrap a memory store shaped for the Sabha council
sakthi init --sabha ~/sakthi
```

This creates 9 role "wings" (one per C-suite seat) plus a personal wing, ready to be filled. See [github.com/Infinidatum-LLC/sakthi-graph](https://github.com/Infinidatum-LLC/sakthi-graph) for the full install guide and other configuration options.

### 6.3 Seed your council with who you are (the profile cards)

Open the `CLAUDE.md` file in your Sabha install. Find the `Known entities` block. There are two formats — start with the **flat list** for fast setup, upgrade to **profile cards** when you have 5 minutes.

**Flat list (minimum viable):**

```
PEOPLE:      [your name], [co-founder], [key teammate]
COMPANIES:   [your company]
PRODUCTS:    [your main product]
PROJECTS:    [your biggest active initiative]
OBLIGATIONS: [GDPR / SOC2 / HIPAA / EU AI Act — whichever applies]
FINANCIAL:   [primary bank, brokerage]
```

**Profile cards (recommended):**

```
### People
- **You** — name. Solo founder / CEO. Background: 10 years in enterprise SaaS sales.
- **Your co-founder** — role, equity %, what they own.

### Company
- **Acme Co.** — Delaware C-corp. $600K ARR, growing ~15%/month. Bootstrapped.
  Operating at Mercury, reserve at SVB.

### Active projects
- **Q3 launch** — bet for the year. Targets 5 design partners by end of Q3.
  2 signed so far.

### Obligations
- SOC 2 Type II audit due Q4. No HIPAA exposure.

### Financial anchors
- Trailing 3-mo burn: $32K/mo. Last close runway: 5.6 months.
```

The council reads these like a new advisor would — references them in answers, asks when something contradicts what's written, **refuses to invent facts** that contradict your profile cards.

**Update them when reality changes.** Stale profile cards are worse than no cards.

---

## 7. The compounding intelligence loop

This is the section the rest of this guide was building toward.

Compounding intelligence is the difference between *Sabha on day 1* and *Sabha on day 90*. The mechanism is straightforward: every Engage-mode reply writes a paragraph to your memory backend. Every substantive question pulls relevant entries forward. **The council doesn't get smarter — your council gets smarter, about your work specifically.**

### 7.1 What week 1 feels like

You ask a question. Sabha routes to the right role. The answer is sharp on framework, generic on specifics. It treats you like a new client at a strategy consulting firm — competent advice on what *anyone* in your situation should consider, weak on what *you specifically* should do.

This is normal. The council has no history with you yet.

### 7.2 What week 4 feels like

You ask:

```
Should I take the SOC 2 Type II audit budget out of Q3 or push it to Q4?
```

The CFO replies:

```
Routing: CFO. Push to Q4.

Per your profile, runway is 5.6 months and burn is $32K/mo.
Adding ~$18K in Type II audit costs to Q3 pushes runway under
5 months — below the 6-month healthy floor you've been tracking
since the 2026-03-12 board update. Q4 gives you 60 more days
to close the Series A bridge that's in your active-projects list.
You lose ~30 days of Type II audit credibility for the Q4
enterprise pipeline. Worth it because the runway floor is
load-bearing this quarter.
```

**Notice what just happened:** the CFO cited your runway figure, your burn figure, a prior board-update date, an active project, and named the tradeoff in your specific context. None of that came from the question itself — it came from your accumulated Sakthi.

This level of grounding doesn't exist in a stateless chatbot. It only emerges from compounding.

### 7.3 What week 26 feels like (the real moat)

Six months in, the council recalls patterns you've forgotten you set:

- The CSO declines to recommend a partnership with a vendor type you said you wouldn't work with in week 3
- The CHRO flags a hiring approach you tried last year and parked
- The CIO references the exact week you migrated off a particular service and how the migration went
- The CFO knows your trailing 12-month burn shape, not just the current quarter
- The CXO points to two onboarding decisions you made that correlated with retention changes
- The CEO synthesizes role disagreements using *your* prior judgment patterns, not generic frameworks

**This is the compounding asset.** It is the entire reason to run Sabha instead of asking the same questions to a fresh ChatGPT window every week.

### 7.4 How to feed the loop deliberately

Compounding works whether you think about it or not, but you can accelerate it.

**Use Engage mode for load-bearing decisions.** Engage-mode replies write diary entries; ask-mode replies don't. If you decide something that matters, engage it. Yes, you'll have a `.docx` or `.md` file you may never reread. That's fine — the diary entry is what compounds, not the file.

**Update the profile cards when reality changes.** New hire? Update People. Closed a round? Update Financial. New product line? Update Products. Stale cards quietly corrode the grounding.

**Periodically ask the council what it remembers.** A useful prompt:

```
What do you remember about our pricing decisions over the last six months?
```

The reply tells you what's actually in the graph. If something important is missing, file it now via `/engage`.

**Don't fight the grounding discipline.** When the council says *"using the $32K/mo burn you stated"*, that's the protocol working. If the burn has changed, update the profile card — don't ask the council to ignore it.

### 7.5 The math, briefly

A solo operator who runs Sabha across 200 substantive decisions over a year — about 4 per week — and engages ~30 of them (load-bearing ones), ends the year with:

- 30 diary entries indexed and searchable
- 200+ KG triples ambient-updated
- A profile-card stack that's been refined ~12 times
- A council that, by month 6, demonstrably recalls and uses prior decisions in new answers

That asset is not portable to a competitor's tool. It is not held on a SaaS server you can be locked out of. It is yours, on your machine, exportable as JSON whenever you want.

**This is the compounding moat.** Sabha's job is to make the council answer well today. Memory's job is to make the council answer *better* tomorrow because you used it today.

---

## 8. Customizing the council for your work

Three levels of customization, from quickest to deepest.

### 8.1 Level 1 — Just edit `CLAUDE.md` (5 minutes)

Open `CLAUDE.md`. Edit:
- The role table — rename, add, or remove roles to match your situation
- The known entities — your real people, products, projects
- The voice notes if you want the council more or less terse

See [CUSTOMIZATION.md](./CUSTOMIZATION.md) for examples (solo founder, agency, researcher, personal-life council).

### 8.2 Level 2 — Pick a different preset (10 minutes)

Three reference councils ship in `examples/`:

- `personal-sakthi.CLAUDE.md` — life roles (Health, Finance, Family, Career, Time, Self)
- `professional-sakthi.CLAUDE.md` — default C-suite (the 9 roles)
- `developer-sakthi.CLAUDE.md` — engineering roles (Architect, Reviewer, Security, Performance, QA, Mentor)

Copy the closest preset to your `CLAUDE.md`, then personalize.

### 8.3 Level 3 — Author a custom skill (~half a day)

For a role that needs a deep skill (frameworks, decision heuristics, templates, worked examples), create a new directory under `skills/roles/<your-role>/` following the pattern of the shipped CFO or CMO skills. Each deep skill has subtrees for `playbooks/`, `templates/`, `references/`, and `worked-examples/`. The router will pick up the new role at next launch.

If you'd like the skill to be auto-routed, add the role to the routing table in `CLAUDE.md`.

---

## 9. Anti-patterns (what NOT to do)

Five mistakes will make Sabha feel worse than a chatbot. Avoid all five.

1. **Don't ignore the routing line.** If the wrong role is answering, override with `/route`. Don't reword the question and hope.
2. **Don't engage everything.** Engage mode is for load-bearing decisions. Engaging routine questions clutters your diary and slows the compounding signal.
3. **Don't ask the council to "be less decisive" or "give me options."** That defeats the protocol. If you genuinely want a survey, you're in the wrong tool — open a fresh ChatGPT window.
4. **Don't let profile cards rot.** Outdated entity facts are worse than no entity facts because the council will confidently cite stale numbers.
5. **Don't bypass the grounding discipline.** When the council says *"using the burn figure you stated,"* update the figure if it's wrong — don't tell the council to ignore your own data.

---

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Replies have no `Routing:` line | Sabha skill not loading | Check that the plugin is installed and the project's `CLAUDE.md` references Sabha. Restart Claude Code. |
| Wrong role keeps answering | Auto-routing misfires for your phrasing | Use `/route <ROLE>` to override. The router learns from explicit corrections over time. |
| The council "invents" numbers | Memory backend not connected, or profile cards empty | Wire up memory (§6). Seed the profile cards. The grounding discipline can't ground against nothing. |
| Engage mode doesn't produce a file | Skill version too old, or write permissions blocked | Update to latest Sabha OS. Check that the working directory is writable. |
| Slash commands return "unknown command" | You're on Claude.ai web, not Claude Code | Slash commands are Claude Code only. On web, use natural-language equivalents ("file this as a memo"). |
| Sakthi Graph search returns nothing relevant | Drawer count too low yet, or wrong wing | Sakthi compounds — week 1 is sparse. Try broader queries. Specify a `wing` filter only when you're sure. |
| The MIT package and a private overlay disagree | You have both versions of a role | Public skill is source of truth for the framework; private overlay carries your specific facts. Read the public one first. |

---

## 11. Going deeper

You've hit the floor of useful familiarity. Six directions from here:

- **[FOR-REGULATED-INDUSTRIES.md](./FOR-REGULATED-INDUSTRIES.md)** — running Sabha in finance, healthcare, legal, public-sector contexts. Compliance grounding, audit posture, what to wire up.
- **[MEMORY-OPTIONS.md](./MEMORY-OPTIONS.md)** — the full comparison of Sakthi Graph vs. Claude Memory vs. mem0 vs. Letta vs. Zep vs. plain markdown. Pick the right one for your situation.
- **[ROLES.md](./ROLES.md)** — deep dive on each of the nine seats. What they're tuned for, what their reference frameworks are, how they hand off to each other.
- **[PHILOSOPHY.md](./PHILOSOPHY.md)** — the Chanakya tradition, the protocol design intent, the "decisive over option-shaped" principle in detail.
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** — how the protocol, skills, and memory layer fit together. Read this when you want to build something on top of Sabha.
- **[ROADMAP.md](./ROADMAP.md)** — what's planned for v3.0 and beyond. The shape of where this is going.

---

## Closing note

Sabha is opinionated software. Some of you will love it. Some will find the terseness abrasive and the no-survey rule constraining. **That's the design.** A council that hedges is a council you ignore.

The compounding loop is the long game. Week 1 you're using a sharper chatbot. Month 6 you're using something that knows your work. Year 1 you're using something whose value would take a competitor a year to replicate.

Use Engage mode for load-bearing decisions. Update your profile cards when reality changes. Trust the routing, override when you disagree. Let the diary entries accumulate.

The council recommends. Memory compounds. **Sakthi belongs to you.**

---

*Sabha OS · MIT License · [github.com/Infinidatum-LLC/sabhaos](https://github.com/Infinidatum-LLC/sabhaos)*
