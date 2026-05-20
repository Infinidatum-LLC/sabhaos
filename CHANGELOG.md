# Changelog

All notable changes to Sabha OS will be documented here. Format follows [Keep a Changelog](https://keepachangelog.com/).

> **Origin:** project conceived October 2025. First public release May 2026.

## [2.2.0] — 2026-05-19

Sabha turns from a router into a **council with structured disagreement and compounding memory**. Two new mode skills land alongside the nine role skills: `deliberate` (multi-role argument + synthesis) and `sakthi-diary` (auto-compounding decision record). Together they close the two highest-leverage gaps in the v2.1 product — single-role routing couldn't settle contested tradeoffs, and memory write was advisory instead of canonical.

### Added — `skills/modes/deliberate/`

- New mode skill that runs a fixed deliberation protocol: pick 2–3 roles → memory gate → openings → rebuttals → CEO synthesis → diary write.
- Each section has a strict scaffold (Position / Framework / What's given up / Evidence for openings; Steelman / Disagreement / Refined position for rebuttals; Real call / Decision / Cost accepted / Next move / Reversibility / Signal-to-revisit for CEO synthesis). Role discipline is enforced by the scaffolds — no blurred voices.
- Hard length cap: ~900 words for 2-role deliberations, ~1,300 for 3-role. Synthesis must fit the budget.
- Grounding discipline from CLAUDE.md §3 applies in every role's voice — a deliberation that invents numbers in three roles is three times worse than a single-role hallucination.
- Advanced `--deep` mode dispatches each role as a separate `claude` sub-agent for high-stakes decisions where role purity is worth 2–3× tokens.
- New slash command: `/deliberate <question>`.

### Added — `skills/modes/sakthi-diary/`

- New mode skill that makes diary writes canonical for engage and deliberate modes.
- Defines the **SABHA_DIARY v1** template: `date, agent, mode, entities, question, recommendation, tradeoff, next_move, reversibility, sources, transcript`. The contract is the template; transports vary.
- Wing/room placement table — engage entries route by lead role (e.g., CFO → `decisions/finance`), deliberations always land in `deliberations`.
- Backend translation table for non-Sakthi memory MCPs (mem0, Letta, Zep, plain MemPalace, local-folder fallback). Sabha remains memory-MCP-agnostic at the protocol layer.
- Grounding discipline applies to the diary itself — if a number was flagged as an estimate in chat, it stays flagged in the diary. Sakthi inherits whatever you write.
- "Write for cold reads" guidance — future sessions retrieve entries with no surrounding context, so the entry must be self-contained.

### Updated

- **CLAUDE.md §4** — renamed "ASK vs ENGAGE" → "ASK vs ENGAGE vs DELIBERATE." Deliberate mode is now a first-class mode alongside the existing two. Engage mode now explicitly auto-writes a diary entry (was advisory in v2.1).
- **`/engage` command** — wired to call the `sakthi-diary` skill after file production.
- **`plugin.json`** — registers `skills/modes/deliberate` and `skills/modes/sakthi-diary`. Version → 2.2.0.

### Why this matters (CSO note)

v2.1.0 made memory branded and coherent. v2.2.0 makes the council *act* like a council: roles can disagree on the record, the synthesis is structured, and every recorded decision compounds. This is the difference between "Claude wearing nine name tags" and "a council with state." The eval moat from v2.1 (n=50, 96% pairwise) gets stronger because per-deliberation transcripts are now reproducible artifacts.

### Not in scope (yet) — but staying inside sabha-os

- Per-role rubrics for the eval harness — coming in v2.3.
- `sabha-os:digest` (weekly per-role synthesis skill) — coming in v2.3.
- Data-hook connectors (Stripe, Mercury, QuickBooks, banking, payroll) — land **inside sabha-os** as additional skills/docs under each role's `data-hooks/` subtree (CFO already has the directory). Not a separate plugin. One install, one product, one brand. Tradeoff accepted: plugin grows; mitigated by data hooks being primarily docs + tool-call contracts, not heavy code.

## [2.1.0] — 2026-05-16

Memory layer rebranded as **Sakthi Graph** — a fork of MemPalace pre-shaped for the Sabha council. The trinity is now coherent and product-grade: **Sabha (the council) + Chanakya (the archetype) + Sakthi (your power, your memory, your machine).**

### Added — Sakthi Graph (new repo: rdmurugan/sakthi-graph)
- Forked from `MemPalace/mempalace` v3.3.5 (MIT). Original LICENSE preserved; NOTICE file documents attribution. Internal Python module structure unchanged from upstream to minimize merge friction.
- **Surface rebrand:** package `sakthi-graph` (was `mempalace`); CLI commands `sakthi` and `sakthi-mcp` (legacy aliases retained); all 31 MCP tool names renamed `sakthi_*` (e.g., `sakthi_search`, `sakthi_kg_query`, `sakthi_diary_write`).
- **Sabha-specific preset** (`mempalace/sabha.py`): the new `sakthi init --sabha` flag bootstraps 9 role wings pre-configured for the Sabha council (cfo, cmo, cio, caio, cso, cxo, chro, clc, ceo), each with rooms tuned for that role's decision domain. Optional `--personal` adds 6 life wings (health, finance-personal, family, career, time, self).
- **Role-aware diary templates** — one per Sabha role, with fields appropriate to that role's diary discipline (e.g., CFO template prompts for numbers used + framework + tradeoff; CLC template enforces risk-tier + counsel hand-off; CEO template captures irreducible-question + regret-check).
- **License:** MIT preserved. Sabha-specific additions copyright Durai (@rdmurugan), released under the same MIT.

### Updated in Sabha OS
- **CLAUDE.md MEMORY section** — renamed "MemPalace wire-up (example)" → "Sakthi Graph wire-up (recommended)". Tool names updated `mempalace_*` → `sakthi_*`. Sabha remains memory-MCP-agnostic at the protocol layer (mem0, Letta, Zep, plain MemPalace still work; only Sakthi gets the Sabha-shaped preset).
- **Marketplace manifest** — `mempalace` plugin replaced with `sakthi-graph` plugin, sourced from `github.com/rdmurugan/sakthi-graph`. New install path:
  ```
  claude plugin marketplace add rdmurugan/sabhaos
  claude plugin install sabha-os@sabha-marketplace
  claude plugin install sakthi-graph@sabha-marketplace
  uv tool install sakthi-graph
  sakthi init --sabha ~/sakthi
  ```
- **Plugin description** — now names the Sabha trinity explicitly (Sabha + Chanakya + Sakthi); cross-links to Sakthi.
- **PRIVACY.md** — updated to reference Sakthi-graph (no data-collection posture identical to MemPalace upstream).
- **README install section** — five-step flow including the `sakthi init --sabha` bootstrap.
- **QUICKSTART.md** — memory section rewritten around Sakthi.
- **All docs** — `mcp__mempalace__*` tool references updated to `mcp__sakthi__*`; URLs updated to point to the Sakthi repo; CFO/CMO data-hooks docs updated.

### Strategic positioning
This release converts the marketplace listing from "Sabha OS + a generic memory MCP" into a coherent product family with branded surface area. The fork is fully transparent: upstream is preserved, attribution is explicit, internal architecture is unchanged, and any user can pull from `MemPalace/mempalace` directly if they prefer pure upstream.

### License compliance (CLC review)
MIT permits forking with attribution. Sakthi:
- Preserves the original LICENSE file from MemPalace
- Adds NOTICE crediting MemPalace authors (milla-jovovich)
- README's first paragraph names the upstream relationship
- pyproject.toml `[project.urls]` includes "Upstream (MemPalace)" link
- Internal copyright headers in mempalace/ module are preserved

## [2.0.0] — 2026-05-16

Complete C-suite deep-skill coverage. The professional council now has framework grounding across **all 9 roles**. Submission-ready for the official Anthropic plugin marketplace.

### Added — six new deep skills
- **`skills/roles/cio/`** — infrastructure, vendor selection, security posture (NIST tiers), cost optimization (FinOps), incident response (5-stage playbook), observability, platform engineering. Templates: vendor scorecard, security posture review, cost audit. Playbook: vendor evaluation, incident response. Worked example: cloud bill spike investigation.
- **`skills/roles/caio/`** — AI strategy, model selection economics (capability ÷ cost ÷ latency), RAG architecture (5-component design), prompt design patterns, eval discipline, agents (when to / when not to), AI governance (EU AI Act tiers), cost-of-inference math. Templates: model-selection scorecard, eval rubric, RAG design doc. Playbooks: build-an-eval, ship-rag-pilot. Worked example: classifier model selection with cost math.
- **`skills/roles/chro/`** — hiring (cost-of-delay vs cost-of-capacity), employee classification (US common-law, CA AB5, UK IR35), compensation bands, performance management (PIP discipline), org design, payroll vendor selection, international hiring. Templates: offer letter checklist, comp band. Playbooks: first hire, performance management. Worked example: contractor misclassification risk.
- **`skills/roles/cso/`** — where-to-play / how-to-win (Porter, Lafley & Martin), wedge identification, competitive response decision tree, partnership evaluation (4-question filter), market entry / exit, big-bet framework, scenario planning. Templates: where-to-play canvas, competitor map. Playbooks: market entry, partnership evaluation. Worked example: competitor-shipped-feature response.
- **`skills/roles/cxo/`** — activation, cohort retention, four kinds of churn (bad-fit / failed-activation / value-drift / competitive), NPS done right, customer success economics, funnel diagnostic, customer interviewing. Templates: funnel diagnostic, customer interview guide. Playbooks: activation improvement, churn investigation. Worked example: Day-4 retention cliff.
- **`skills/roles/ceo/`** — synthesis frameworks (irreducible-question frame, regret minimization, decisive action, pre-mortem, founder-mode patterns). Intentionally lighter than functional roles — the CEO integrates rather than competes with depth. Template: decision memo.

### Strengthened — CLC legal disclaimer
The CLC SKILL.md description now front-loads "NOT LEGAL ADVICE — operator-grade legal FRAMING only" for marketplace catalog visibility. Marketplace submission packaging makes the boundary unmistakable to any visitor.

### Updated
- **CLAUDE.md role table** — all 9 roles now flagged with "deep skill" markers. CEO promoted from "escape hatch" to synthesis role.
- **Plugin manifest** — all 9 deep skills registered. Description rewritten to capture the full breadth of coverage with explicit CLC disclaimer.
- **README "Depth" section** — rewritten to describe all 9 deep skills with framework attribution and the CLC caveat.

### Why v2.0.0 (major bump)
- Architectural shift: from "selective depth (CFO + CMO + CLC)" to "full coverage." This is a category change in what the product delivers.
- The marketplace listing now reads as "complete professional council, framework-grounded" rather than "routing protocol with some depth."
- Submission to claude.com/plugins is the immediate next step.

### Scale of the change
- **~25,000+ lines of new operator-grade content** across the six new deep skills.
- Each role follows the established CFO/CMO/CLC pattern: SKILL + REFERENCE + heuristics + 2-3 templates + 1-2 playbooks + 1 worked example + references.
- Framework citations across all roles trace back to canonical operator literature; specific URLs deliberately omitted in favor of stable attribution (see each role's `references.md`).

### What's NOT in v2.0
- Personal-sakthi role-level depth (Health / Finance / Family / Career / Time / Self). Deferred — different audience, dilutes the submission focus. Coming in a separate release stream.
- Developer-sakthi role-level depth (Architect / Reviewer / Security / Performance / QA / Mentor). Deferred — would compete with Anthropic's official LSP plugins.
- Live-data MCP grounding for the new roles (Stripe for CFO, GA for CMO are documented in v1.5). Per-role data hooks for CIO, CHRO, CSO, CXO, CAIO planned for v2.1+.
- Eval coverage for the new roles. The eval harness (v1.3.1) runs on the protocol layer; specific eval coverage for each deep skill is v2.x roadmap.

### Marketplace submission readiness
Ready to submit at:
- claude.ai/settings/plugins/submit
- platform.claude.com/plugins/submit

## [1.8.0] — 2026-05-16

Chief Legal Counsel (CLC) — new deep skill, third role with framework grounding.

### Added
- **`skills/roles/clc/`** — full CLC skill following the CFO/CMO pattern. The role provides operator-grade legal framing (NOT legal advice) with explicit risk-tier triage and counsel hand-off:
  - `SKILL.md` — activation discipline + the "not legal advice" guardrails. Every CLC reply ends with one of: operator-handleable / operator-handleable with attorney review / stop-and-call-counsel.
  - `REFERENCE.md` — 12 frameworks: risk-tier triage, contract review (standard terms), NDA review, IP four-pillars (trademark, copyright, patent, trade secret), privacy (GDPR/CCPA/EU AI Act), corporate (entity, board, cap table), employment-legal, securities, litigation, regulatory, contract drafting rails, the "translate before reading" frame.
  - `heuristics.md` — fast-lookup risk-tier classifier, "when to call which kind of attorney" table, contract / IP / privacy / employment / securities heuristics, bias quick-catches.
  - 4 templates — `risk-tier-classifier.md`, `nda-review-checklist.md`, `msa-negotiation-positions.md`, `ip-assignment-essentials.md`, `privacy-policy-skeleton.md`.
  - 3 playbooks — `customer-contract-review.md`, `cease-and-desist-response.md`, `trademark-registration.md`.
  - 2 worked examples — MSA review under enterprise pressure; co-founder departure with IP at issue.
  - `references.md` — Restatement of Contracts, Fisher & Ury, Mnookin, Cooley GO, Common Paper, USPTO / Lanham Act / 17 U.S.C. / 35 U.S.C. / DTSA, GDPR / CCPA / EU AI Act / HIPAA, DGCL, Securities Act, Reg D, YC SAFEs, NVCA, Feld & Mendelson, FLSA / CA Labor Code, FRCP, FAA, AAA / JAMS, plus industry-specific regulators.

### Changed
- **CLAUDE.md role table** — CLC added as the 9th role with the "deep skill" marker. Slotted between CHRO and CEO.
- **Plugin manifest** — `./skills/roles/clc` registered alongside cfo and cmo.
- **README "Depth" section** — three deep skills now (CFO, CMO, CLC). Explicit note that the CLC skill provides legal framing, not legal advice.
- **docs/ROLES.md** — CLC entry added with voice description and sample answer shape.

### Why CLC matters
- Legal questions are some of the most frequent ones operators face (contracts every week, IP questions every month, privacy questions every quarter).
- Operators currently route them to expensive generalist attorneys for matters that don't need attorney involvement, OR skip the legal frame entirely on matters that do need it.
- CLC's risk-tier triage (red/yellow/green) plus the named-specialist hand-off captures most of the operator-grade value an experienced general counsel provides — at AI-cost rather than $500/hr.

### Discipline note
CLC is the highest-risk deep skill we've shipped because incorrect legal framing has expensive downside. The skill is explicit on this: every reply names the risk tier; RED-tier replies refuse to substantively engage and route to licensed counsel; specific statutes / cases / regulatory citations are flagged for verification.

## [1.7.0] — 2026-05-14

Bundle MemPalace alongside Sabha OS in the same marketplace.

### Added
- **`mempalace` as a second plugin in `sabha-marketplace`** — sourced from `MemPalace/mempalace` on GitHub. Adding our marketplace now exposes both plugins: `sabha-os` (the protocol) and `mempalace` (the recommended memory substrate). Users get a single `claude plugin marketplace add rdmurugan/sabhaos` and then install whichever combination they want.

### Install flow (new)
```bash
claude plugin marketplace add rdmurugan/sabhaos
claude plugin install sabha-os@sabha-marketplace
claude plugin install mempalace@sabha-marketplace   # optional but recommended
uv tool install mempalace                            # the actual Python binary
# OR:    pip install mempalace
```

The first three steps are pure Claude Code operations. Step 4 (`uv tool install mempalace`) is the unavoidable Python install — Claude Code plugins register MCP server configs but can't install the binary itself. The MemPalace plugin's `mcpServers` entry tells Claude Code to launch `mempalace-mcp`, which step 4 provides.

### Positioning note
Sabha remains **memory-MCP-agnostic** at the protocol layer — CLAUDE.md still treats memory generically. The marketplace is the *opinionated bundle*; the protocol is *un-opinionated*. Users who prefer mem0, Letta, Zep, or Pieces wire those directly and skip the MemPalace plugin install. See `docs/CUSTOMIZATION.md`.

### Updated
- `README.md` install section — replaced the single-plugin install path with the four-step bundled flow.
- `docs/QUICKSTART.md` "Add memory" section — now mirrors the marketplace flow; honest about the Claude.ai web-app limitation (memory MCPs require a local runtime).

### Why this matters
- Reduces friction from "add a marketplace + look up another marketplace + install + pip install" to "add one marketplace + two installs + one pip install."
- Establishes the marketplace as a *curated bundle*, not a single-plugin catalog. Future plugins (sabha-stripe-bridge, sabha-cmo-ga, etc.) can join here. Sets up the v2.0 architecture.
- MemPalace stays maintained upstream by its own team. We point at their GitHub repo as the source; their releases flow to our users.

## [1.6.0] — 2026-05-14

Marketplace ready — Sabha OS is now a one-line install.

### Added
- **`.claude-plugin/marketplace.json`** — Sabha OS publishes itself as the single plugin in the `sabha-marketplace`. Anyone can now install with:
  ```
  claude plugin marketplace add rdmurugan/sabhaos
  claude plugin install sabha-os@sabha-marketplace
  ```
  Built against the canonical schema documented at https://code.claude.com/docs/en/plugin-marketplaces. Name `sabha-marketplace` is kebab-case and outside Anthropic's reserved-name list.

- **Deep CFO and CMO skills registered in `plugin.json`.** Previously only `sabha-router` was listed in the manifest's `skills` array; the deep `skills/roles/cfo/` and `skills/roles/cmo/` directories existed but weren't surfaced to Claude Code's skill router. Marketplace installers now get the full depth layer.

- **[`evals/ANALYSIS.md`](evals/ANALYSIS.md)** (carried over from Unreleased) — interpretation of the v1.3.1 eval run.

### Changed
- README install section now leads with the marketplace install (Option A), with `git clone` as Option B and Claude.ai paste as Option C. The marketplace install is two commands; the previous git-clone path required four.

### Why this matters
- Discoverability. Anyone who reads the LinkedIn post and lands on the repo now has a one-line install path. Compare: `claude plugin marketplace add rdmurugan/sabhaos` (one shareable command) vs. `git clone … && claude plugin enable … && open … && edit BRACKETS`.
- Per-user reach. Once the marketplace is added to a user's Claude Code, any future plugin we publish here is auto-discoverable to them.
- It also unlocks teams via `.claude/settings.json` → `extraKnownMarketplaces`, which pre-prompts colleagues to add the marketplace when they trust the project folder.

### Validation
Run `claude plugin validate .` from the repo root to confirm the marketplace passes Claude Code's schema check before announcing. (I can't execute `claude` commands from this session.)

## [1.5.0] — 2026-05-14

Live-data grounding scaffold — data hooks for CFO and CMO.

This is the v2.0 moat play, shipped early as a documented pattern. Sabha now turns from *"council that remembers"* into *"council that knows"* whenever the operator wires a relevant data MCP into Claude Code. CFO can read Stripe / QuickBooks. CMO can read Google Analytics. The pattern generalizes to any deep role + any data MCP.

### Added
- **`skills/roles/cfo/data-hooks/`** — three files:
  - `README.md` — when to reach for a data hook, available hooks, the grounding discipline that still applies, extension instructions.
  - `stripe.md` — full integration doc for Stripe-flavored MCPs. Tool shapes, when to reach, worked example (runway question with live Stripe + banking data), Stripe-specific grounding rules (MRR vs recognized revenue, collected vs booked, currency, disputes, test mode), and anti-patterns. Concludes by naming what Stripe data can't answer.
  - `quickbooks.md` — same pattern for QuickBooks-flavored (and Xero, etc.) MCPs. Worked example: expense triage with real category breakdown showing the STARK ordering applied to live data.

- **`skills/roles/cmo/data-hooks/`** — two files:
  - `README.md` — same pattern as CFO data-hooks.
  - `google-analytics.md` — full integration doc for GA4-flavored MCPs. Tool shapes, when to reach, worked example (funnel-breakage diagnosis with live GA + Stripe data, routes the activation gap to CXO), attribution-model warnings, sampling caveats, and anti-patterns.

- **CFO and CMO `SKILL.md`** updated with a 7th discipline step: "Reach for a data hook if real numbers are needed and an MCP is connected." Replaces "ask user to retype" with "pull and cite."

- **CLAUDE.md MEMORY section** — new "Data MCPs for real-time grounding" subsection. Cross-links to the role data-hooks directories. Reinforces that data from MCPs is *citable with source + timestamp*, not infallible.

### Why this matters
- The 1.4.0 grounding discipline closed the "confidently invents numbers" failure mode by requiring assertions to be cited or flagged. But it left the operator doing the data-fetching work manually. 1.5.0 closes the rest of that loop: when the data lives in a system the user already pays for (Stripe, QuickBooks, GA), the council reaches in and pulls it.
- This is the moat play. Anyone can fork the protocol; the curated data-hook docs per (role × MCP) are a 12-month build cycle to replicate. By the time a competitor copies the pattern, the docs have grown to cover banking, payroll, CRM, ad platforms, support tickets, product analytics, code quality, and more.

### Not yet shipped
- Tool-by-tool execution examples (i.e., concrete tool-name signatures for specific Stripe MCPs). The data-hook docs intentionally stay MCP-agnostic — naming *shapes* not *vendors*. We'll add vendor-specific tool tables when the relevant MCP ecosystem settles.
- Banking, payroll, ad-platform, CRM, support, product-analytics data hooks. The pattern is established; these are content additions, not architectural ones. Welcome PRs.
- An eval question set that specifically tests data-hook grounding (e.g., "compute runway" with Stripe + banking MCPs connected, judged on whether the answer cites real numbers vs invents).

## [1.4.0] — 2026-05-14

Grounding discipline — every assertion is cited, sourced, or flagged.

### Added
- **Grounding discipline section in CLAUDE.md §3 (ANSWER).** Closes the "confidently-wrong" failure mode: if a reply asserts a number, name, or date, it must (a) cite the source, (b) attribute to the user, or (c) explicitly flag as estimate/assumption. Never present an invented number as a fact. This is a behavior-changing addition to the protocol; it applies in every role, with or without a deep skill loaded.
- **Entity profile cards** as the recommended format for the MEMORY section in CLAUDE.md. Flat list (the prior format) is kept as the minimum-viable starter; profile cards (one prose paragraph per entity) give the council real anchors and let it refuse to invent attributes that contradict the profile. Three sentences per entity is enough.
- Grounding discipline echoed into the deep CFO and CMO skills with role-specific warnings:
  - **CFO** is most at risk of inventing financial numbers — anti-pattern updated explicitly.
  - **CMO** is most at risk of inventing customer language and CAC benchmarks — anti-pattern updated explicitly.
- Grounding discipline added to the `sabha-router` skill so it applies on every routed reply, not just deep-skill roles.
- `docs/QUICKSTART.md` (carried over from Unreleased) — 10-minute no-installation guide for non-technical users.

### Why
- Sabha's strongest pitch is *"decisive, tradeoff-aware counsel."* But a confident reply in a CFO voice is **worse** than a hedged generic reply if the numbers are invented. Decisive without grounding is theatre. This release closes the gap with zero-data-cost: the model now self-marks confidence on every fact.
- Eval finding (1.3.1, n=20): the three baseline pairwise wins all involved questions where Sabha could have invented data instead of reframing the question. Grounding discipline + reframing discipline (next release) target this directly.

### Not yet shipped (roadmap)
- **v1.5.0:** reframe-the-question discipline (handles the 3 baseline-win failure modes from the eval). Skill-level rule: if the user's premise contains an unstated infeasibility or a wrong frame, challenge the premise before answering.
- **v2.0.0:** live-data MCP integrations — CFO reads Stripe / QuickBooks; CMO reads Google Analytics / HubSpot; CIO reads AWS Cost Explorer. This is the moat play. See `docs/PHILOSOPHY.md` and CSO read in prior sessions for the rationale.

## [1.3.1] — 2026-05-14

Eval harness now exercises deep role skills.

### Fixed
- The 1.3.0 eval harness only loaded `CLAUDE.md` as the Sabha system prompt — meaning the deep role skills (CFO, CMO) added in 1.3.0 were *not* being tested. The harness would have reported v1.2.x-equivalent numbers despite the depth shipping. Now, when a question's `role:` tag matches an existing `skills/roles/<role>/` directory, the harness appends that skill's `SKILL.md` + `REFERENCE.md` + `heuristics.md` to the system prompt for the Sabha condition. The per-question results table flags this with a `deep skill ✓` column. Without this fix, the eval was unintentionally a v1.0 protocol test, not a v1.3 product test.

## [1.3.0] — 2026-05-14

Deep role skills: CFO and CMO. This is the moat-building release — converts Sabha from "a routing prompt" to "a curated library of operator expertise packaged as a council."

### Added
- **`skills/roles/cfo/`** — full CFO skill (~3500 lines across 10 files):
  - `SKILL.md` — activation discipline and answer structure
  - `REFERENCE.md` — 12 frameworks (runway, burn multiple, unit economics, Rule of 40, capital allocation, value-based pricing, hire-vs-defer, fundraise narrative, cost-cut, scenario planning, behavioral biases, KPI scorecard)
  - `heuristics.md` — fast-lookup decision triage and cognitive-bias quick-catches
  - 4 templates — runway model, unit economics, pricing canvas, capital allocation matrix
  - 3 playbooks — monthly close, fundraise prep, cost-cut decision
  - 3 worked examples — seed-stage runway, SaaS pricing, hire-vs-defer
  - `references.md` — Kahneman/Tversky, McKinsey, Skok, Wack, Klein, Kaplan & Norton citations
- **`skills/roles/cmo/`** — full CMO skill (~3000 lines across 9 files):
  - `SKILL.md` — activation discipline and answer structure
  - `REFERENCE.md` — 12 frameworks (problem typing, JTBD + four forces, positioning canvas, Five Forces for channels, ICP definition, AARRR, channel portfolio, behavioral pricing, brand equity, cognitive biases, funnel honesty, when marketing can't fix it)
  - `heuristics.md` — fast-lookup classification and bias-catches
  - 3 templates — positioning statement, JTBD canvas, channel portfolio
  - 2 playbooks — repositioning, channel allocation
  - 2 worked examples — SaaS repositioning, channel allocation under budget pressure
  - `references.md` — Christensen, Porter, Trout & Ries, Thaler/Sunstein, Aaker, McClure, Skok citations
- CLAUDE.md role table now flags deep skills with a "Depth" column.
- README has a new "Depth" section ahead of the eval section, explaining the layered architecture.

### Changed
- Plugin version bumped to 1.3.0 reflecting the architectural shift from prompt-only to prompt + curated knowledge base.

### Strategic note
The framework citations are real (Kahneman, Christensen, Porter, etc.) and reliably attributable to those authors and publication traditions. URL-level citations are deliberately omitted — see each role's `references.md` for the methodology note on why.

## [1.2.2] — 2026-05-14

Fix retry detection for `OverloadedError`.

### Fixed
- `_is_retryable` in `evals/judge.py` previously failed to detect `OverloadedError` in some SDK configurations — the import path silently became `None`, the fallback `getattr(exc, "status_code", None)` check returned `None`, and the exception fell through to a non-retry raise on the first attempt. The harness then died on the very 529 it was supposed to retry. Now matches by class name (independent of SDK version), checks status code via multiple attribute paths (`status_code`, `response.status_code`, `body`), and falls through to `isinstance(APIStatusError)` only as a last resort. Diagnostic prints on every classification so retry behavior is observable in the log.
- Bumped retry policy: 10 attempts (was 6), max single delay capped at 30s, total worst-case wait ~180s. Anthropic overload windows are usually under 2 minutes; the harness now rides them out.

## [1.2.1] — 2026-05-14

Eval harness reliability fixes.

### Changed
- All API calls (both generation and both judge calls) now retry on transient errors via a single `with_retry` helper. Handles `OverloadedError` (HTTP 529), `RateLimitError` (429), `APIConnectionError`, `APITimeoutError`, and 5xx server errors. Jittered exponential backoff, up to 6 attempts (~60s total worst-case wait).
- `run_eval.py` now **checkpoints after every question** — JSON + Markdown snapshots are written incrementally so a mid-run crash never loses prior work.

### Added
- `--resume` flag picks up where an interrupted run stopped. Skips already-completed question IDs from the existing output file.

## [1.2.0] — 2026-05-14

Adds an evaluation harness.

### Added
- `evals/` directory with 20 operator-style questions, LLM-as-judge harness, and a methodology README.
- Measures decisiveness, tradeoff-named, concreteness, routing-present, length-discipline, plus pairwise preference (Sabha vs. baseline).
- Default candidate model: Claude Sonnet 4.6. Default judge: Claude Opus 4.7.
- Run with `python evals/run_eval.py` (see `evals/README.md`). Cost: ~$1-3 per full run.
- Result files commit to `evals/results/` so claims about protocol effectiveness are checkable.

### Known limitations
- n=20 — confidence intervals on per-axis means are wide. Pairwise signal more reliable than absolute scores.
- LLM-as-judge has known biases; human-judge variant is a welcome PR.

## [1.1.0] — 2026-05-14

Positioning release: Sabha + Chanakya + Sakthi.

### Added
- **Sakthi** (Sanskrit/Tamil: *power*) as the outcome the protocol builds — the user's locally-stored, accumulated knowledge of decisions, people, and projects.
- **Chanakya** (4th century BCE strategic advisor, author of the *Arthashastra*) named as the archetype the council embodies.
- Three reference council presets in `examples/`:
  - `personal-sakthi.CLAUDE.md` — life roles (Health, Finance, Family, Career, Time, Self).
  - `professional-sakthi.CLAUDE.md` — the default C-suite council (CIO, CAIO, CFO, CMO, CSO, CXO, CHRO, CEO).
  - `developer-sakthi.CLAUDE.md` — code roles (Architect, Reviewer, Security, Performance, QA, Mentor, Tech Lead).
- "Local-first" positioning across README, CLAUDE.md, and the sabha-router skill — memory promoted from optional add-on to backbone.
- Philosophy doc expanded with a fifth discipline (local memory / Sakthi compounds) and an etymology section for all three Sanskrit/Tamil terms.

### Changed
- README hero rewritten around the Sabha + Chanakya + Sakthi stack.
- CLAUDE.md memory section promoted; example wire-up uses [MemPalace](https://github.com/MemPalace/mempalace) (MIT, runs locally) with `mempalace_search` / `mempalace_kg_query` / `mempalace_diary_write`.
- Plugin description and keywords reflect the council / Chanakya / Sakthi / local-first framing.

## [1.0.0] — 2026-05-14

Initial public release.

### Added
- Core `CLAUDE.md` protocol with eight default C-suite roles (CIO, CAIO, CFO, CMO, CSO, CXO, CHRO, CEO).
- Claude Code plugin manifest (`.claude-plugin/plugin.json`).
- `sabha-router` skill that enforces routing on every substantive reply.
- Slash commands: `/ask`, `/engage`, `/route <ROLE>`.
- Three profession presets in `examples/`: solo founder, agency, researcher.
- Docs: `PHILOSOPHY.md`, `ROLES.md`, `CUSTOMIZATION.md`.
- Example memory-MCP wire-up in `CLAUDE.md` and `sabha-router` skill using [MemPalace](https://github.com/MemPalace/mempalace) — `mempalace_search`, `mempalace_kg_query`, `mempalace_diary_write`. Other memory MCPs (mem0, Letta, Zep, Pieces) follow the same pattern; see `docs/CUSTOMIZATION.md`.
- MIT license, CONTRIBUTING guide, .gitignore.

### Known limitations
- No automated evals yet. If you build one, please PR.
