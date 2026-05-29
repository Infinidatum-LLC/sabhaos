# Sabha OS Roadmap

> Sabha OS is a Claude-native routing protocol + 9 deep C-suite skills + a memory-MCP-agnostic substrate. This roadmap tracks the open-source protocol and the v1.0 commercial desktop. Items not listed are not promised. Items here are bets, not guarantees — the roadmap is a contract about *intent*, not delivery dates.

Two related but distinct surfaces:

| Surface | Tier | Repo / artifact | Status |
|---|---|---|---|
| **Sabha OS protocol** (`CLAUDE.md` + 9 deep skills + sabha-router) | Open source, MIT | this repo · `claude plugin install sabha-os@sabha-marketplace` | shipping continuously |
| **Sabha OS desktop** (the v1.0 commercial app with Ed25519 ledger + policy enforcement + CFO Workflow Preset) | Commercial, proprietary | separate private repo · waitlist at [runsabha.com](https://runsabha.com) | in development |

The OSS protocol stays MIT forever. The commercial desktop is built *on top of* the same protocol — it is not a fork, it is a packaging of (protocol + memory + ledger + enforcement + license layer) into a one-binary, one-install product for operators who don't want to wire up Claude Code themselves.

---

## What's shipped (current state)

The OSS layer is real, installed, and used. Specifically:

- **The routing protocol** — `CLAUDE.md` ships the discipline; `skills/sabha-router/SKILL.md` enforces it on every reply.
- **All 9 C-suite roles as deep skills** — `skills/roles/{cfo,cmo,cio,caio,cso,cxo,chro,clc,ceo}/` — each with REFERENCE, heuristics, templates, playbooks, worked examples, source citations.
- **`/ask` · `/engage` · `/route` mode controls** — chat reply vs document-grade deliverable; per-turn role override.
- **`/chanakya`** — opt-in verse layer (76-verse Neeti corpus, role-mapped).
- **Pramana** — sibling research agent shipped in `pramana/` with the 9-section briefing framework (TL;DR, Context, Key facts, Players, Dynamics, **Contrarian view**, Outlook, Recommendation, Sources).
- **Three reference councils** — `examples/personal-sakthi.CLAUDE.md`, `examples/professional-sakthi.CLAUDE.md`, `examples/developer-sakthi.CLAUDE.md`.
- **Eval harness + results** — `evals/` runs reproducibly; current pairwise-vs-baseline result is **48/50 (96.0%, Wilson 95% CI [86.5%, 98.9%])** on the v3 sub-axis rubric, judged by Claude Opus 4.7.
- **Marketplace packaging** — installable in one line via `claude plugin marketplace add Infinidatum-LLC/sabhaos`.
- **Compatible memory backends** — Claude Memory (default), [Sakthi Graph](https://github.com/Infinidatum-LLC/sakthi-graph) (local-first recommended), mem0, Letta, Zep, Pieces, plain markdown.

---

## v0.next — Protocol polish

The next minor releases of the OSS protocol. These items strengthen routing accuracy, fix known eval losses, and expand the deep-skill coverage.

- **Cross-model judge harness** — the current 96.0% number uses an Anthropic judge. The harness already supports `--judge-provider {anthropic,openai,google}`; the cross-model run is queued. If it holds across families, the in-family-bias concern is closed.
- **Address the 2 catalogued eval losses** — `cso-02` (where-to-play question that under-routed) and `under-05` (lookup question where the bare baseline was sharper). Both have failure analyses in `evals/ANALYSIS.md`.
- **Adversarial-eval expansion** — current adversarial bucket is 10/10 at n=10; expand to n=25 to tighten the CI on the "challenge-the-premise" robustness claim.
- **Per-role mini-evals** — each role gets a 10-question scenario suite so we can detect regressions at the role granularity, not just protocol-wide pairwise.
- **Memory-MCP integration snippets** — `docs/MEMORY-OPTIONS.md` already covers tradeoffs; add ready-to-paste `CLAUDE.md` blocks for the top three non-Sakthi memory MCPs.
- **More profession presets** — `examples/lawyer.CLAUDE.md`, `examples/agency.CLAUDE.md`, `examples/researcher.CLAUDE.md`, `examples/teacher.CLAUDE.md`. Already partially present; round them out.

---

## v1.0 — Commercial desktop (Q3 2026 target)

The commercial product packages the OSS protocol into a one-binary desktop app for operators who want the council without wiring up Claude Code, MCPs, and memory layers themselves. **In active development; waitlist at [runsabha.com](https://runsabha.com).**

What's bundled into v1.0:

- **The full Sabha protocol** (the OSS layer of this repo) running natively.
- **Sakthi Graph memory** ([sister repo](https://github.com/Infinidatum-LLC/sakthi-graph), MIT) embedded — zero-config local-first knowledge graph.
- **Ed25519 decision ledger** — every `/engage` decision gets cryptographically signed and appended to a tamper-evident SQLite log. Export to PDF for audit. The verifier ships in Sakthi Graph (MIT) so the audit story is independently checkable.
- **Policy enforcement primitive** — declarative rules (`runway_floor`, `vendor_threshold`, `hire_blocker`, `quiet_hours`) that the council *enforces*, not just *advises*. Override requires a modal with a ≥20-character justification, which is also signed and ledger-locked.
- **BYOK LLM** — Claude (recommended), OpenAI, Gemini, or a local model via Ollama / LM Studio. Your key, your spend, your data.
- **License layer** — Ed25519-signed JWT license, 30-day offline cache, soft 3-machine binding, refundable revocation via webhook.
- **Onboarding flow** — 90-second first-run wizard that bootstraps the 9 role wings, imports past decisions if you point it at a folder, and runs a guided first `/engage`.

### CFO Workflow Preset *(commercial v1.0)*

The first packaged workflow preset for the desktop. Turns the council's CFO role into a runway-floor enforcer — useful for solo founders, fractional CFOs, and small-team operators who want a hard "no" wired into their workflow, not just a soft recommendation.

What the preset declares (as policy, not as advice):

```yaml
# cfo-workflow-preset.yaml
runway_floor:
  months: 9                   # block any spend decision that would drop runway under 9 months
hire_blocker:
  unless_revenue_above: 50000 # MRR threshold above which a hire is auto-allowed
  required_role: CFO          # CFO must sign every hire memo
vendor_threshold:
  annual_usd: 5000            # any vendor > $5K/yr requires a /engage memo + ledger entry
quiet_hours:                  # no /engage between 10pm and 7am local — protects against tired decisions
  start: "22:00"
  end:   "07:00"
```

When a user tries to engage a hire memo or a vendor approval, the CFO role checks the policy *before* drafting. If a rule is violated, the council blocks with a modal explaining which rule fired, what the current state is, and what override would require. Override → ≥20-character reason → signed & ledgered.

Why this is the *CFO Workflow* preset, not the "Finance Industry" preset: the rules are about the **finance function** — runway, hiring economics, vendor spend, decision hygiene — not about who you sell to. The preset is industry-agnostic; a solo founder running a healthcare-software startup, an indie SaaS dev, and a fractional-CFO consultancy all benefit equally.

Future presets (post-v1.0): Engineering Workflow (incident-response gating), Hiring Workflow (offer-letter + comp-band enforcement), Legal Workflow (NDA / MSA triage gating). The framework is generic; the CFO preset is the first one wired up because it has the cleanest enforcement surface.

---

## v1.x — Post-launch (post-2026 Q3)

Items that wait for v1.0 to ship before they're scheduled.

- **Workflow preset library** — Engineering, Hiring, Legal (see above).
- **Multi-user shared license** — Family tier (3-seat, shared decision ledger) and Pro tier (single-operator, hosted control plane optional).
- **Audit-export API** — paid Enterprise tier: streaming ledger export to S3 / R2 for SOC2-style external audit consumption.
- **Cross-device sync** — encrypted, user-owned (S3 / R2 / Dropbox / iCloud folder, client-side encrypted). Not a SaaS.

---

## v2.x — Sabha Sentinel (separate product line, post-v1.0)

A second product built on the same Sabha + Sakthi + Ledger substrate, targeted at AI-agent governance rather than human-operator decisions. Ratified as a product line on 2026-05-25; engineering work begins after v1.0 ships. See the [Sabha Sentinel product-line decision memo](https://github.com/Infinidatum-LLC/sabhaos/blob/main/docs/sentinel-product-line.md) — *coming with v1.0 launch*.

Sentinel reuses ~85% of the Sabha OS substrate (ledger, policy engine, Sakthi memory). It is **not** a feature of Sabha OS — it ships as its own MCP-distributed governance layer that any AI agent (Claude, GPT, local-LLM) can call before executing a high-consequence action. Sentinel is the operationalization of the [Five Pillars of AI Accountability](https://www.amazon.com/dp/) framework — Named Decision Owner, Consequence Classification, Decision Architecture, Outcome Monitoring, Accountability Reporting.

This roadmap entry is forward-looking; nothing about Sentinel is on the v1.0 critical path.

---

## 60-second demo build

The hero of both READMEs ([sabha-os](./README.md) · [sakthi-graph](https://github.com/Infinidatum-LLC/sakthi-graph/blob/main/README.md)) currently shows the demo as "coming in the next release." The build is queued and will ship before the v1.0 desktop announcement. Target: a single screencap that walks through:

1. Operator asks a multi-domain question ("burn vs hiring tradeoff").
2. Sabha routes to CFO + CHRO advisory.
3. The CFO answer pulls from a Sakthi Graph wing on screen (with the actual drawer card showing).
4. Operator hits `/engage`; the engagement is signed and ledgered, with the resulting `.docx` shown.
5. A second question shows the policy enforcer firing (CFO Workflow Preset) and blocking a hire that would breach runway floor.

---

## Branch model

```
main      ← tagged releases of the OSS protocol
develop   ← active PRs land here
```

The commercial desktop is in a separate private repository (private for license-key infrastructure + sensitive build artifacts); when something from the desktop is generalizable and MIT-compatible, it gets backported into this OSS repo or into Sakthi Graph.

---

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md). PRs target the OSS layer of this repo (`main` / `develop`). The commercial desktop accepts feedback via the waitlist at [runsabha.com](https://runsabha.com) but does not accept PRs against its private codebase.

The MIT-licensed substrate (protocol + skills + eval harness + Sakthi Graph) will stay MIT forever, regardless of where the commercial product goes. That commitment is the whole point of the public-tier / private-tier split.
