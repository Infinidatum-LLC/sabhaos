# Sabha OS — single-document context reference

> **What this file is.** A self-contained, dense, paste-into-any-AI-surface reference for Sabha OS. Use this when you're starting a fresh conversation (Claude.ai, Cowork, ChatGPT, a new Claude Code session) and want the AI to have full context about the project in one shot. Slightly longer than the README; structured for one-shot ingestion, not for browsing.
>
> **Canonical sources of truth:**
> - GitHub front door for humans: [`README.md`](../README.md)
> - GitHub plugin marketplace: `claude plugin marketplace add rdmurugan/sabhaos`
> - This doc: cross-AI-chat context. Stays in sync with the rest of the repo.
>
> **Repos:**
> - Protocol: [github.com/rdmurugan/sabhaos](https://github.com/rdmurugan/sabhaos)
> - Memory layer (optional): [github.com/rdmurugan/sakthi-graph](https://github.com/rdmurugan/sakthi-graph)
> - Developer-focused sibling for GitHub Copilot: [github.com/rdmurugan/sabha-code](https://github.com/rdmurugan/sabha-code)
>
> **License:** MIT. Copyright © 2025–2026 Durai Rajamanickam (@rdmurugan).
>
> **Date of this writing:** 2026-05-17.

---

## 1. What Sabha OS is, in one paragraph

Sabha OS is an open-source **protocol** that turns Claude (or any LLM with a system prompt) into a structured council of nine C-suite advisors. Every substantive question is routed to a specific role (CFO, CMO, CIO, CAIO, CSO, CXO, CHRO, CLC, or CEO), answered in the Chanakya tradition — decisive, terse, recommendation-first, tradeoff-aware, grounded — and (optionally) compounded into a local memory layer (Sakthi Graph) so the council remembers your decisions over time. Each role ships as a **deep skill** with a reference knowledge base, fast-lookup heuristics, fillable templates, procedural playbooks, and worked examples. The protocol works on top of any memory backend (Claude Memory, Sakthi Graph, mem0, Letta, plain markdown, or none). It's MIT-licensed end-to-end and has a reproducible eval harness.

## 2. The naming (Sanskrit/Tamil tradition)

| Term | Script | Meaning | Role in the stack |
|---|---|---|---|
| **Sabha** | सभा / சபை | council / assembly | the routing protocol itself |
| **Chanakya** | चाणक्य / சாணக்கியர் | the strategist (4th c. BCE, author of *Arthashastra*) | the voice / archetype |
| **Sakthi** | शक्ति / சக்தி | power | the (optional) local memory |
| **Sittham** | चित्त / சித்தம் | consciousness / awareness | the corpus-ingest verb |

The metaphor lands: Sakthi is your accumulated *power* (memory). Sittham is what that memory *is aware of* (the corpora you've absorbed). Sabha is how the council uses both. Chanakya is the voice it speaks in.

## 3. The protocol — what it does, mechanically

For every load-bearing question, Sabha forces five disciplines:

1. **A role.** Declared at the top of the reply: `Routing: <ROLE> (primary). <other role> weighs in on <topic>.`
2. **A recommendation.** Not a survey of options. The role commits.
3. **A tradeoff.** "Do X. You lose Y. Worth it because Z."
4. **Mode discipline.** *Ask* mode (chat reply, default) vs *engage* mode (filed `.docx` or `.md` deliverable + memory diary write).
5. **Local memory.** When connected, the role queries the memory layer *before* asserting facts about known entities.

Plus a **grounding rule**: if the role asserts a number, name, or date, it must (a) cite the source, (b) mark it as the user's input, or (c) flag it explicitly as an estimate. Never invent.

The protocol skips chit-chat, trivia, meta-questions about Sabha, and cases where the user names a different skill or role.

## 4. The nine roles

| Role | Covers | Voice (one-line) |
|---|---|---|
| **CFO** | Runway, pricing, unit economics, capital allocation, fundraise | "Numbers first. Runway in months, not 'comfortable cash position'." |
| **CMO** | Positioning, JTBD, channels, content, behavioral pricing | "Names the channel and the message. Allergic to jargon." |
| **CIO** | Infrastructure, vendors, security, SRE, FinOps, incidents | "Names the actual tool. Has opinions about cost per GB." |
| **CAIO** | AI strategy, LLMs, RAG, evals, model selection, governance | "Names the actual model. Doesn't oversell LLMs." |
| **CSO** | Strategy, competition, partnerships, GTM, big bets, M&A | "Asks 'what does winning look like' before tactics." |
| **CXO** | UX, activation, retention, NPS, churn, customer success | "Talks about the user's next click, not 'the experience'." |
| **CHRO** | Hiring, classification, comp, performance, severance, org design | "Knows employment law is jurisdiction-specific. Flags lawyer." |
| **CLC** | Contracts, IP, privacy, corporate, securities, regulatory framing | "Risk-tier triage (RED/YELLOW/GREEN). NOT legal advice." |
| **CEO** | Synthesis when roles disagree, founder-mode irreducibles, board memos | "Names the irreducible tradeoff. Tells the user when it's their call." |

All nine ship as **deep skills**, not voice tweaks. Each role's `skills/roles/<role>/` folder contains:
- `SKILL.md` — the activation rules and one-line summary
- `REFERENCE.md` — multi-framework knowledge base with numerical thresholds and citations
- `heuristics.md` — fast-lookup triage rules
- `templates/` — fillable artifacts (runway model, unit economics, pricing canvas, positioning statement, JTBD canvas, contract redline package, etc.)
- `playbooks/` — procedural workflows (monthly close, fundraise prep, cost-cut decision, repositioning, hire-to-classify, trademark registration)
- `worked-examples/` — end-to-end scenarios with real numbers
- `references.md` — citations to the body of work each framework draws from

Frameworks drawn from: Kahneman/Tversky, Christensen (JTBD), Porter (Five Forces), McKinsey (capital allocation), Skok (SaaS unit economics), Reichheld (NPS), McClure (pirate metrics), Lafley & Martin (Playing to Win), AWS Well-Architected, Google SRE, DORA/Accelerate, FinOps Foundation, NIST AI RMF, GDPR / EU AI Act, USPTO, and the operator canon.

## 5. Memory backends — pluggable

Sabha is memory-backend-agnostic. Pick the one that fits your trust model:

| Backend | When to use | Where it lives |
|---|---|---|
| **Claude Memory** | Default; casual users | Anthropic's servers |
| **Sakthi Graph** | Privacy-sensitive, regulated industries, multi-LLM users | Your machine (`~/sakthi`) |
| **mem0 / Letta / Zep / Pieces** | Existing investment in those tools | Cloud or self-host (vendor-dependent) |
| **Plain `memory/*.md`** | Minimalists | A folder on your machine |
| **None** | Trying Sabha out, or privacy-maximalist | n/a |

Sabha and Claude Memory **compose** — most users should run Sabha on top of Claude Memory by default. Sakthi Graph is the recommended *additional* layer for privacy-sensitive operators who want institutional memory that never leaves their machine.

## 6. Sakthi Graph (optional local memory) — quick architecture

Forked from MemPalace (MIT). ChromaDB-backed. Pre-shaped for the Sabha council:

```
~/sakthi/                    ← the local palace
├── wings/
│   ├── cfo/decisions/       ← runway, pricing, unit economics decisions
│   ├── cmo/decisions/       ← positioning, channel, repositioning notes
│   ├── cio/decisions/       ← vendor evals, incidents, infra decisions
│   ├── caio/decisions/      ← model selection, eval results, RAG notes
│   ├── cso/decisions/       ← strategy decisions, big bets, partnerships
│   ├── cxo/decisions/       ← activation experiments, retention findings
│   ├── chro/decisions/      ← hires, classification, comp decisions
│   ├── clc/decisions/       ← contract decisions, IP, regulatory hand-offs
│   └── ceo/{decisions,synthesis-notes}/  ← synthesis, board memos, pivots
```

Bootstrap with `sakthi init --sabha ~/sakthi`. Exposes 32 MCP tools (`sakthi_search`, `sakthi_kg_query`, `sakthi_diary_write`, `sakthi_add_drawer`, `sakthi_sittham`, etc.).

## 7. `sakthi sittham` — corpus ingest verb

`sittham` (சித்தம், Tamil for *consciousness / awareness*) takes any folder that's been run through [`/graphify`](https://github.com/karpathy-inspired/graphify) and files a compact summary drawer into the right Sabha role wing of your Sakthi:

```bash
/graphify ~/path/to/corpus            # one-time prep
sakthi sittham ~/path/to/corpus       # auto-routed to cfo / cmo / caio / ...
sakthi sittham <path> --dry-run       # preview routing
sakthi sittham <path> --wing cfo --room pricing   # override
```

Corpus content is scored against the 9 role vocabularies via keyword matching; the dominant role's `decisions` room receives a compact drawer (counts, top god nodes, role-signal breakdown, report excerpt). Weak or split signals fall back to `ceo/synthesis-notes`. Three surfaces (MCP tool `sakthi_sittham`, CLI, Python `mempalace.sittham.sittham`), one implementation.

## 8. Optional `/chanakya` skill — opt-in verse layer

A separate opt-in skill (`chanakya-neeti`) layers exactly one verse from Chanakya's *Neeti* on top of the routed role's answer. **Fires only when explicitly invoked** — `/chanakya`, "add a Chanakya verse", "what would Chanakya say." 76 verses across all 9 role domains. Format:

```
Routing: <ROLE>.

> *"[Chanakya verse — exact words]"*
> — Chanakya Neeti [N.N]

[Executive answer in role's voice]
```

## 9. Architecture diagram

```
ANY FOLDER ─/graphify─▶ graphify-out/ ─sakthi sittham─▶ SAKTHI (9 wings) ─▶ SABHA (council)
                                                          ▲                     │
                                                          └── diary writes ─────┘
                                                                (engage mode)
```

Three layers:
1. **graphify** — wide-funnel ingest (any folder → knowledge graph)
2. **Sakthi Graph** — durable, role-shaped retrieval surface
3. **Sabha OS** — the routing protocol on top

## 10. Eval results — current honest numbers (2026-05-18)

### Main eval (n=50, v3 rubric, Anthropic judge)
- **Pairwise win rate: 48/50 (96%)**, Wilson 95% CI [86.5%, 98.9%]
- Rubric Δ: +4.78 / 20 (Sabha mean 16.96 vs baseline 12.18)
- Distribution across 4 stress buckets:
  - Original operator questions: 19/20 (95%)
  - Adversarial-reframing: 10/10 (100%)
  - Cross-role / edge: 10/10 (100%)
  - Underdog (definitional / lookup, baseline should be competitive): 9/10 (90%)
- Per-role: 8/9 roles at 100% pairwise; CSO at 4/6 (only role under 100%, both losses traceable)
- The 2 losses: `cso-02` was truncated at max_tokens (harness bug, in BACKLOG); `under-05` was a legitimate loss (baseline added a Lafley & Martin attribution Sabha omitted on a definitional question)

**Caveat:** the v3 sub-axis rubric prompt was used, but Opus 4.7 emitted JSON in v2 flat shape (the judge mentally reasoned about sub-criteria — rationales reference them — but didn't structure the output). The fallback in `score_reply` handled it cleanly. Sub-axis slicing is therefore unavailable for this run; "tighten v3 judge prompt for structured output" is in BACKLOG.

**Retired baselines:** v1.3.1 (n=20, 85% pairwise, +5.95 rubric) and v2 (n=20 re-run with all deep skills, 85% pairwise, +4.85 rubric) used the v1/v2 rubric where decisiveness and tradeoff_named saturated. Numbers preserved in `evals/results/2026-05-14.json` and `2026-05-16.json` for audit; **don't carry them forward as ongoing claims**.

### Chanakya eval (7 questions, opt-in discipline test)
- Activation: **4/4 (100%)** — including adversarial "/chanakya should I name the branch staging or stage" (model gracefully bridged the metaphor)
- Discipline: **3/3 (100%)** after a guardrail patch that closed an earlier 2/3 leak
- Attribution: **0% baseline → 100% with skill loaded** — the model hallucinates Chanakya verse numbers when asked without the skill; the skill provides correctly-numbered citations from a curated corpus

### Methodology
- LLM-as-judge: Opus 4.7 judging Sonnet 4.6 outputs on 5-axis rubric + pairwise preference
- Reproducible: `python evals/run_eval.py` and `python evals/chanakya/run_eval.py`
- Known limits: in-family judge bias (both Claude), small N (95% CI on 17/20 pairwise ≈ 64–95%), rubric saturation on `decisiveness` and `tradeoff_named`
- Full read: [`evals/ANALYSIS.md`](../evals/ANALYSIS.md), [`docs/EVALS.md`](./EVALS.md)

## 11. Install path (Claude Code)

```bash
# Minimum (protocol only; works with Claude Memory zero-config)
claude plugin marketplace add rdmurugan/sabhaos
claude plugin install sabha-os@sabha-marketplace

# Optional: add the local-first memory backend
claude plugin install sakthi-graph@sabha-marketplace
uv tool install sakthi-graph
sakthi init --sabha ~/sakthi
```

Then personalize `~/.claude/plugins/cache/sabha-marketplace/sabha-os/CLAUDE.md` with your entities. Or, for non-Claude-Code surfaces, paste the contents of `CLAUDE.md` into a Claude.ai Project's custom instructions / a Cowork system prompt / the API's system field.

## 12. What's shipped (state as of 2026-05-17)

- ✅ All 9 C-suite deep skills (CFO, CMO, CIO, CAIO, CSO, CXO, CHRO, CLC, CEO)
- ✅ Sabha-router skill enforcing routing-at-top-of-reply
- ✅ Reproducible 20-question LLM-as-judge eval (rubric + pairwise) with `--resume` and retry-on-overload
- ✅ Dedicated Chanakya activation eval (corpus-correctness check + opt-in discipline test)
- ✅ Sakthi Graph fork with `--sabha` preset (9 role wings auto-bootstrapped)
- ✅ `sakthi sittham` corpus-ingest verb (graphify → Sakthi role wing)
- ✅ Optional `chanakya-neeti` opt-in skill (76 verses, `/chanakya` slash command)
- ✅ Marketplace plugins for Claude Code (`sabha-os` + `sakthi-graph`)
- ✅ Memory-backend-agnostic positioning (compatible with Claude Memory, Sakthi, mem0, Letta, plain markdown)
- ✅ Full doc surface: README, QUICKSTART (non-tech), ARCHITECTURE, ROLES, MEMORY-OPTIONS, FOR-REGULATED-INDUSTRIES, CUSTOMIZATION, PHILOSOPHY, EVALS, ROADMAP, CONTEXT (this doc), CONTRIBUTING, PRIVACY, CHANGELOG
- ✅ MIT-licensed; copyright restored to Durai (@rdmurugan) as solo developer; upstream MemPalace attribution preserved per MIT terms

## 13. What's NOT on the active roadmap

Founder-level decisions worth knowing:

| Item | Status | Reason |
|---|---|---|
| **LLM-agnostic SDK (Anthropic + OpenAI + Google adapters + cross-model eval)** | HELD by founder | Council (CSO + CMO + CAIO) recommended Q3 2026; founder held it. Sabha stays Claude-focused for now. Recorded in `docs/ROADMAP.md`. |
| Hosted Sabha cloud product | Not building | Defeats local-first thesis. |
| Sabha "team" with shared memory | Not building | Sakthi is one-user-one-machine by design. |
| GUI over CLAUDE.md | Not building | The protocol is 200 lines of markdown; a GUI would be more code than the thing. |
| Auto-updates | Not building | Trust violation. Users pin and audit. |
| End-consumer pivot | Not building | Wrong audience. Sabha is operator-grade. |

## 14. The current bets (Q3 2026)

- **Premium skill packs — scaffold only.** Build the directory structure for vertical packs (SaaS-CFO, healthcare-CLC) without yet shipping content. Validates the architecture for a commercial overlay without committing.
- **Council preset expansion.** Add presets for lawyer, healthcare-founder, indie-dev, real-estate, K-12 educator — responding to pull, not speculatively.

## 15. Repository layout (high-level)

```
sabha-os/                         (https://github.com/rdmurugan/sabhaos)
├── CLAUDE.md                     ← the protocol; this IS Sabha
├── .claude-plugin/               ← Claude Code plugin + marketplace manifests
├── skills/
│   ├── sabha-router/SKILL.md     ← enforces routing-at-top-of-reply
│   ├── chanakya-neeti/SKILL.md   ← opt-in verse layer (76 verses)
│   └── roles/{cfo,cmo,cio,caio,cso,cxo,chro,clc,ceo}/  ← 9 deep skills
├── commands/
│   ├── ask.md / engage.md / route.md / chanakya.md  ← slash commands
├── docs/
│   ├── QUICKSTART.md             ← no-install, Claude.ai web path
│   ├── ARCHITECTURE.md           ← full system view
│   ├── ROLES.md                  ← the 9 roles in detail
│   ├── MEMORY-OPTIONS.md         ← Claude Memory vs Sakthi vs mem0 vs ...
│   ├── FOR-REGULATED-INDUSTRIES.md  ← healthcare/legal/finance/defense
│   ├── CUSTOMIZATION.md          ← renaming roles, swapping memory
│   ├── PHILOSOPHY.md             ← why these 5 disciplines
│   ├── EVALS.md                  ← eval methodology + current results
│   ├── ROADMAP.md                ← what's shipped, what's held, what's next
│   └── CONTEXT.md                ← this file
├── evals/
│   ├── run_eval.py / questions.yaml / judge.py / ANALYSIS.md
│   ├── results/2026-05-16.json     ← main eval (all 9 deep skills)
│   └── chanakya/                   ← dedicated opt-in discipline eval
├── examples/                     ← preset councils (professional, personal, developer, solo-founder, agency, researcher)
├── LICENSE  PRIVACY.md  CHANGELOG.md  CONTRIBUTING.md  README.md

sakthi-graph/                     (https://github.com/rdmurugan/sakthi-graph)
├── mempalace/                    ← preserved internal module structure from upstream fork
│   ├── sabha.py                  ← the --sabha preset definitions
│   ├── sittham.py                ← the corpus-ingest verb implementation
│   ├── mcp_server.py             ← 32 MCP tools
│   └── cli.py                    ← `sakthi` + `sakthi-mcp` commands
├── docs/SITTHAM.md               ← detailed sittham reference
├── tests/test_sittham.py         ← unit tests
├── LICENSE (MIT, dual: upstream MemPalace + Durai)
└── NOTICE (attribution to MemPalace upstream)
```

## 16. The honest pitch (for use across surfaces)

For a default user: **"Sabha makes Claude answer load-bearing questions like a C-suite advisor — decisive, tradeoff-aware, grounded — instead of as a hedging research assistant."**

For a privacy-sensitive operator: **"Sabha + Sakthi gives you an AI council with institutional memory that never leaves your machine. MIT-licensed, auditable, local-first."**

For an eval-skeptical reader: **"Sabha-routed replies win 48/50 pairwise (96%, Wilson 95% CI [86.5%, 98.9%]) against no-system-prompt baselines on a 50-question reproducible eval that includes adversarial-reframing and underdog buckets specifically built to stress the protocol. Holds at 10/10 on adversarial questions where the original v1.3.1 run lost 3/3. Harness, questions, results, and the v3 sub-axis rubric all committed. Two losses (cso-02, under-05) are catalogued and traceable. Cross-model judge harness shipped; cross-family judging run is the next pending credibility move."**

For an operator in regulated industries: **"The protocol layer is MIT markdown. The memory layer (Sakthi) is a directory on your disk; no telemetry, no auto-update, no cloud sync. Pair with a HIPAA-eligible LLM tier and your existing endpoint controls."**

## 17. Anti-pitches (what Sabha is NOT)

- **Not domain expertise.** The CFO role gives Claude *a CFO's framing*. You still need real CPAs for tax filings.
- **Not legal advice.** The CLC role is operator-grade framing. Practicing law is licensed and jurisdiction-specific.
- **Not a personality skin.** The roles are job functions, not characters. No backstories.
- **Not a chain-of-thought hack.** It changes what the model *outputs*, not how it reasons.
- **Not magic for trivia.** Sabha skips chit-chat and lookups.
- **Not Claude-locked at the storage layer**, but the *protocol* layer is currently Claude-focused; cross-model SDK is held by founder.

## 18. How to use this document

| Surface | Use this doc by … |
|---|---|
| **Claude.ai Projects** | Paste into a Project's custom instructions. Optionally also paste `CLAUDE.md`. |
| **Claude Code (already installed)** | You don't need this doc — `CLAUDE.md` is the protocol. Use this doc to explain Sabha to others. |
| **Cowork** | Paste into the workspace's `CLAUDE.md` or system prompt. |
| **API / programmatic use** | Use as a system prompt prefix; the AI now has full context. |
| **ChatGPT / Gemini / other LLMs** | Paste at the start of a conversation. The protocol-as-text works on any system-prompt-capable LLM, though cross-model eval data isn't published yet. |
| **Onboarding a teammate / collaborator** | Send them this file. It's the single best "what is this project" doc. |

## 19. The single-line summary

**Sabha is the protocol (the council). Chanakya is the voice (the strategist). Sakthi is your memory (your power). Sittham is your awareness (the corpus). MIT-licensed end to end. 9 deep skills, reproducible evals, local-first by default, Claude-focused for now.**
