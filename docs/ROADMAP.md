# Roadmap

What's next, by quarter. Subject to change — this is a roadmap, not a contract.

> **Companion file:** ideas that have been *captured* but not yet *ranked* live in [`BACKLOG.md`](./BACKLOG.md). Items move backlog → roadmap when a triggering condition fires. Killed items stay in the backlog with a strike-through and a reason — *"why we didn't build this"* is often more valuable than *"what we built."*

> **Calling the shots that aren't built yet is part of the discipline.** This page names the bets, the timing, and the kill criteria. If something here doesn't ship by its quarter, the next ROADMAP entry will say *why* and either re-commit or kill it.

---

## Now (Q2 2026) — shipped

- ✅ All 9 C-suite deep skills (CFO, CMO, CIO, CAIO, CSO, CXO, CHRO, CLC, CEO)
- ✅ Sabha-router skill enforcing routing-at-top-of-reply
- ✅ Reproducible eval harness with LLM-as-judge + pairwise (`evals/`)
- ✅ Sakthi Graph fork (`sakthi-graph`) with `--sabha` preset
- ✅ `sakthi sittham` corpus-ingest verb (graphify → Sakthi role wing)
- ✅ Marketplace plugins for Claude Code (`sabha-os` + `sakthi-graph`)
- ✅ Memory-backend-agnostic positioning (Claude Memory + Sakthi + mem0 + Letta + plain markdown)
- ✅ Public-release documentation surface (ARCHITECTURE, ROLES, EVALS, MEMORY-OPTIONS, FOR-REGULATED-INDUSTRIES, CUSTOMIZATION, PHILOSOPHY, QUICKSTART)
- ✅ Optional `chanakya-neeti` opt-in skill (76 verses, `/chanakya` slash command)
- ✅ Dedicated Chanakya activation eval (`evals/chanakya/`) — v2 grader with corpus-correctness check. Latest results (2026-05-17, 7 questions): activation 4/4, discipline 3/3 (after guardrail patch validated re-run), baseline attribution 0% vs skill-loaded 100%.
- ✅ **Main eval v2** — rubric v3 (sub-axis decomposition fixes saturation on decisiveness / tradeoff_named / length_discipline), question set expanded n=20 → n=50 (added 10 adversarial-reframing + 10 cross-role-edge + 10 underdog), cross-model judge harness shipped (`--judge-provider {anthropic,openai,google}` in `run_eval.py`). v1.3.1 and v2 baselines retired; v3 measurement floor is the canonical comparison going forward.

The protocol layer is feature-complete for v2.x. From here, the work shifts from *building* to *opening up* — more LLMs, more memory backends, more council presets.

---

## Q3 2026

### 🛑 LLM-agnostic SDK — HELD by founder (2026-05-16)

**Status:** Deferred. No timeline.

**Council recommendation (CSO + CMO + CAIO):** Ship `sabha-sdk` with Anthropic + OpenAI + Google adapters in Q3, plus cross-model eval data, to prevent "Sabha = Claude plugin" from becoming the cached association as Claude Memory's brand grows.

**Founder override:** Held for now. Sabha continues to be primarily a Claude-Code protocol. The cross-model bet is real but not the priority this quarter. Other work (presets, content, possibly commercial scaffolding) takes precedence.

**What this means concretely:**
- No `sabha-sdk` Python package this quarter.
- No cross-model eval data committed.
- README and MEMORY-OPTIONS.md continue to describe Sakthi as technically LLM-agnostic (it's an MCP server; any MCP-capable LLM can use it) but **do not** claim cross-model eval parity for the Sabha protocol layer.
- The protocol-as-text (CLAUDE.md as a system prompt) remains portable in principle; that's not the same as a tested, eval-backed cross-model release.

**Re-evaluate when:** Claude Memory's positioning forces the question, or an operator/customer asks for cross-model support specifically. Until then, hold.

### Bet: Premium skill packs — scaffold only

**The bet:** Ship the *infrastructure* for premium skill packs (industry-vertical role deep skills) without yet shipping any premium content.

**Why:** if there's commercial demand for, say, a SaaS-specific CFO pack, a healthcare-specific CLC pack, or a developer-tools-specific CSO pack — the open-source core remains MIT and free, and premium packs become an optional revenue line.

**Scope:**
- A `premium-skills/` directory with the same skill-folder shape (REFERENCE / heuristics / templates / playbooks / worked-examples).
- A `LICENSING.md` clarifying that anything in `skills/roles/` is MIT, and that future `premium-skills/` content may be commercial.
- No actual premium content yet. Scaffold only. Validates the architecture for commercial overlay.

**Kill criteria:** if no operator asks for vertical packs by end of Q3, the directory stays empty and we revisit in Q4.

### Bet: Council presets — more professions

**The bet:** Expand `examples/` with profession-specific presets distilled from real operator requests.

**Scope:** lawyer, healthcare-founder, indie-dev, real-estate, K-12 educator — whichever ones get pulled by the community via issues or PRs. Don't write speculative presets; respond to demand.

**Why:** the protocol's value compounds with usage. Every working preset that ships is a piece of evidence the protocol generalizes beyond founder/exec work.

---

## Q4 2026 — depending on Q3 signal

Branches based on Q3 outcomes:

### If commercial demand materializes (premium skill scaffold gets pull)

- **First premium pack.** Likely candidate based on inbound: SaaS-CFO pack (deeper unit economics, fundraise prep for specific stages, board-deck templates).
- **License + delivery infrastructure.** A way to sell, deliver, and update premium packs that doesn't break the open-source posture.

### If the privacy / regulated wedge gets pull

- **Sakthi Enterprise edition?** A version of Sakthi with built-in encryption at rest, audit logging, multi-user palace support, and a deployment package for compliance review. Open-core; the existing Sakthi stays MIT.
- **First reference customer in healthcare or legal.** Case study.

### Default (no clear signal from any of the above)

- **More council presets.** Industry-specific CLAUDE.md presets in `examples/` (lawyer, healthcare-founder, indie-dev, real-estate, K-12 educator). Community-contributable.
- **Translations.** CLAUDE.md in non-English (Hindi, Tamil, Japanese, Spanish) for non-English-first founders.
- **A small web UI** for previewing what your Sabha would say to a question, without installing anything. Reduces the "I have to install a plugin to try this" friction.

---

## Q1 2027 — too far to commit

The honest answer: no plan should claim certainty 2+ quarters out. By Q1 2027:

- Claude's memory feature surface will have evolved (more structured? team-shared?). Re-evaluate Sakthi positioning.
- The MCP standard may have matured (or fragmented). Adjust accordingly.
- The cross-model question (currently held) may force itself onto the roadmap by external pressure — a customer ask, a competitor move, or Claude Memory's brand crowding out the protocol-agnostic claim.

What stays true regardless: **the protocol layer (the routing, the voice, the deep skills, the engage/ask discipline) is the durable asset.** Everything else is implementation that adapts to the surrounding ecosystem.

---

## What is *not* on the roadmap

Things we've thought about and intentionally chose not to build, with reasons:

| Not building | Why |
|---|---|
| A hosted Sabha cloud product | Defeats the local-first thesis. Compete on positioning we'd lose, not the one we own. |
| A Sabha "team" feature with shared memory | Sakthi's whole point is one-user-one-machine. If you want shared knowledge, use your existing org tools (Notion, Confluence) and let Sabha reference them through its memory hook. |
| A GUI layer over CLAUDE.md | The protocol is 200 lines of markdown. A GUI would be more code than the thing it edits. Don't build. |
| Voice / chat / image modalities | Out of scope. Sabha is a text-protocol for text-LLM councils. |
| A "Sabha for end consumers" pivot | Wrong audience. Sabha is operator-grade. Don't dilute. |
| Auto-updates | Trust violation. Users pin and audit; we ship versioned releases. |

---

## How decisions get made

The roadmap reflects the council's read; the user (Durai, as founder/CEO of this project) makes the final call. Disagreements with the council go in the next ROADMAP iteration as *"the council recommended X; founder overrode to Y because Z."* That's how the protocol applies to its own development.

When you (a contributor, a user, a potential collaborator) want to influence the roadmap:

- **Open an issue** describing your use case and what'd be valuable.
- **Send a real usage story.** What worked, what didn't, what'd unblock you. These directly shape priorities.
- **Send a PR** for a council preset or a deep-skill addition; that bypasses the roadmap entirely (the contribution path is open).

---

## Tradeoff named (on the roadmap as a whole)

Holding the LLM-agnostic SDK means leaning into the Claude-Code positioning for now. You give up the protocol-agnostic moat (a future where Sabha runs cleanly on GPT and Gemini with eval data to prove it). You gain Q3 capacity for content velocity (presets, premium-skill scaffolding) and a tighter posture as a Claude-native operator-grade plugin.

The risk we accept by holding: "Sabha = Claude plugin" may become the cached association before we ever prove otherwise. If that happens, the eventual cross-model bet becomes a harder repositioning, not a fresh launch.

The reason holding can be the right call anyway: depth in the Claude ecosystem (more presets, deeper skills, the eval discipline, the regulated-industry wedge) is also a moat. It just isn't the same moat.

This is the founder's call. The council recorded its disagreement; the founder overrode it. Logged in this document for accountability.
