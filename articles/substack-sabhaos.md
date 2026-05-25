# I Stopped Asking AI for Opinions. I Built a Council Instead.

*Substack · May 2026*

---

There's a pattern in AI replies that took me a while to name. You ask something load-bearing — "should I take on bridge debt or chase the outstanding invoice?" — and you get back what I now call *option-shaped* text.

Five considerations. Three frameworks. A balanced view. A gentle nudge toward "it depends."

It doesn't help. Not because the AI is wrong, exactly, but because **that's not how advisors talk**. A lawyer says "sign this." A CFO says "chase the invoice, here's why." A doctor says "take this." They don't survey the option space and send you back to figure it out. They commit.

I got tired of AI-as-encyclopedia. So I built something different: **Sabha OS** — a C-suite council protocol that runs entirely in your system prompt, owns no data, and remembers what you've already decided.

---

## What is Sabha?

**Sabha** (सभा / சபை) is Sanskrit/Tamil for *assembly* — specifically the deliberative council in the Mahabharata where strategy got debated and decisions got made. The metaphor is exact: you're not querying an oracle, you're convening a council.

Every substantive question gets classified to a domain before the model opens its mouth:

- **CFO** — budget, pricing, runway, unit economics
- **CIO** — infrastructure, cloud, security, tooling
- **CAIO** — AI strategy, model selection, RAG, evals
- **CMO** — marketing, positioning, content, channels
- **CSO** — strategy, competition, GTM, partnerships
- **CXO** — UX, onboarding, retention, churn
- **CHRO** — hiring, comp, HR law, org design
- **CLC** — contracts, IP, privacy, compliance, regulatory
- **CEO** — synthesis when roles disagree, or irreducibly founder-level calls

Every reply starts with a routing declaration — `Routing: CFO.` or `Routing: CFO (primary). CHRO weighs in on comp structure.` — and then commits to a recommendation, names the tradeoff, and stops.

No "here are five ways to think about it." One recommendation. One tradeoff named. Next move.

---

## The archetype is Chanakya

The voice is shaped by **Chanakya** (चाणक्य / சாணக்கியர்) — the 4th century BCE strategist and author of the *Arthashastra*, the world's first systematic treatise on statecraft and economics. He architected Chandragupta Maurya's rise. He was decisive, tradeoff-aware, allergic to flattery, and comfortable naming hard truths.

There's even an optional `/chanakya` skill that layers exactly one Chanakya Neeti verse on top of the role's answer — drawn from a curated 76-verse corpus with correctly numbered citations. Opt-in only; it doesn't auto-fire on every strategic question. But when you want that layer: *"Before beginning a task, ask yourself — is this a task I should be doing?"* lands differently when the council's CFO just told you not to take the bridge loan.

---

## The memory layer is called Sakthi

**Sakthi** (शक्ति / சக்தி) — Sanskrit/Tamil for *power*. Not power-over, but power-of: the capacity built from accumulated decisions, institutional memory, and the advisors you keep close.

Sabha is built around a local-first memory layer called **Sakthi Graph** that runs on your machine. Every session that ends in an *engage* (a filed decision, a written-up memo) gets a diary entry. Three sessions in, your CFO knows your burn rate. Ten sessions in, your CSO knows which bets you killed and why. A year in, your council has the institutional memory of a real C-suite — but only you can read it.

There's also a corpus-ingest verb called `sittham` (சித்தம் — Tamil for *consciousness/awareness*). It takes any document folder, runs it through a knowledge graph prep step, and files it into the right Sabha role wing automatically. Your market research lands in the CMO wing. Your financial models land in the CFO wing. The council becomes aware of what you've fed it.

This is the difference between renting an opinion and building an asset.

---

## What the eval showed

I ran a reproducible benchmark: 50 operator-style questions sent to Claude Sonnet 4.6 twice — once with no system prompt (baseline), once with the Sabha protocol loaded. Claude Opus 4.7 judged each reply on a five-axis rubric plus pairwise preference.

The 50 questions weren't all easy layups. They were split across four stress buckets:

- **Original operator questions** (20 questions) — real decisions a founder or operator would face
- **Adversarial-reframing** (10 questions) — questions designed to trap Sabha into applying structure where reframing was needed
- **Cross-role / edge** (10 questions) — questions that span multiple roles or sit in gray zones
- **Underdog** (10 questions) — definitional or lookup questions where baseline *should* be competitive

**Sabha replies were preferred 48/50 (96%) in pairwise comparison.** Wilson 95% CI: [86.5%, 98.9%].

Per stress bucket: 19/20 on operator questions (95%), **10/10 on adversarial-reframing** (100%), 10/10 on cross-role/edge (100%), 9/10 on underdog (90%).

The adversarial bucket is the one worth pausing on. The v1 eval (20 questions, 85% win rate) had a known gap: Sabha applied structure when reframing the question would have been more useful. The v3 protocol closed that gap. It now holds at 100% even when questions are specifically designed to exploit it.

The two losses are catalogued: one was a harness bug (the reply was truncated at max_tokens, a known issue now in the backlog). One was a legitimate loss — a definitional question where the baseline added a framework attribution that Sabha omitted. Both traceable. Neither systemic.

---

## How it works (the 60-second version)

Sabha is a CLAUDE.md file — a system prompt. No server, no third-party API key, no subscription, no data leaving your machine. You install it via the Claude Code plugin marketplace:

```
claude plugin marketplace add Infinidatum-LLC/sabhaos
```

Or paste CLAUDE.md into any Claude surface (Claude.ai Projects, Cowork, the API). The protocol has zero runtime dependencies — it's text.

Define your known entities (company, people, products, active projects), and the council is live.

The two modes:

**Ask mode** (default) — a chat reply. Quick, inline, no file. Most questions live here.

**Engage mode** — a document-grade deliverable, filed and dated. Triggered when you say "file this," "engage," or when the decision has dollar/time/risk consequences worth recording. When engaging, it also writes a diary entry to Sakthi so the decision compounds.

You can customize the roles entirely. A solo founder might collapse CFO+CSO into "Operator." An agency might rename CIO to "Creative Director." A personal council might run Health/Finance/Career/Family/Self. The protocol is the frame; you shape the council.

---

## Who it's for

Sabha works best for:

- **One-person companies and small teams** where you genuinely need the rest of the C-suite.
- **Founders who think faster than they can hire** — you can't afford a full-time CFO, but you need CFO-quality framing on a pricing call tomorrow.
- **Operators who want decisions, not options** — whose AI replies have gotten so hedged that they've stopped helping.
- **Privacy-sensitive operators** — the memory layer is local-first, MIT-licensed, auditable, and never syncs to anyone's cloud.

It's overkill for pure coding tasks, exploratory research where you want expansive options, or teaching contexts where hedging is appropriate. Sabha skips those automatically — chit-chat and trivial lookups are exempt from routing.

---

## The underlying shift

Most AI usage today is *prompt-and-pray* — ask a question, hope the answer is useful. Sabha is a protocol: a consistent frame that produces consistent output quality across domains. The council doesn't replace your judgment. It improves the inputs and remembers what you've already decided.

Three months ago I asked Claude for help with a pricing decision. I got five considerations. I made the call anyway.

Last week I asked Sabha's CFO the same kind of question. I got a recommendation, the tradeoff named, the exact pricing page copy to ship, and a 10-day decision trigger.

That's not a style difference. That's a different kind of tool.

---

Sabha OS is MIT-licensed and lives at [github.com/Infinidatum-LLC/sabhaos](https://github.com/Infinidatum-LLC/sabhaos). The council is live in under 10 minutes. The eval harness is in `evals/` if you want to run your own numbers — the full 50-question set, the v3 rubric, and all results are committed and reproducible.

Your Sakthi compounds. Build it.
