---
name: deliberate
description: Multi-role deliberation mode for cross-functional decisions where two or three roles have opposed defaults. Activates when the user invokes `/deliberate`, says "let the council weigh in," "have X and Y debate this," or when the question genuinely turns on a contested tradeoff (CFO vs CSO on pricing, CIO vs CSO on build-vs-buy, CHRO vs CFO on hiring, CLC vs CMO on claim language). Runs a fixed protocol — openings, rebuttals, CEO synthesis — and ends with a `sakthi-diary` write so the decision compounds. This is the skill that turns Sabha from a router into a council.
---

# Deliberate — the council in session

Most Sabha questions resolve in one role. Some don't. Pricing is CFO and CSO. Build-vs-buy is CIO and CSO. Hire-now-or-wait is CHRO and CFO. Launching a regulated feature is CLC, CAIO, and CIO. These questions need *deliberation*, not routing.

This skill turns Sabha from a router into a council with structured disagreement and synthesis.

## When to activate

Activate when **any** of these is true:

1. The user invokes `/deliberate <question>` or says *let the council weigh in*, *I want them to argue*, *have X and Y debate this*, *get a second opinion*.
2. The question genuinely has two strong roles with opposed defaults — CFO wants to delay, CSO wants to commit; CIO wants buy, CSO wants build; CHRO wants to wait on hiring, CFO wants headcount frozen but for different reasons.
3. The decision is engage-grade (dollar/time/risk consequences) **and** the recommendation depends on a contested tradeoff a single role can't settle.

Do **not** activate for:

- Questions one role obviously owns (don't deliberate *what's our runway?*).
- Pure information lookups or factual recalls.
- Questions where the user asked for a quick answer or is in a hurry.
- Trivial calls (lunch order). Deliberation has a cost; reserve it for decisions worth recording.

If you're unsure whether to deliberate, default to single-role routing and offer at the end: *"This sits on a CFO/CSO fault line. Want me to deliberate?"*

## The deliberation protocol

Run it in this exact order. Skipping a step weakens the output.

### Step 1 — Pick the participants

Name **2 or 3 roles**. Two is the default — the dueling pair. Add a third **only** when a regulatory, HR, or legal angle is non-trivial (e.g., CLC must weigh in on a customer-data decision; CHRO must weigh in on a hiring-affordability call). The synthesizer is **always CEO**.

Declare at the top of the reply, exact format:

```
Deliberation: <ROLE A> ↔ <ROLE B>. CEO synthesizes.
Question: <one-line restatement of the user's question>
```

For three roles:

```
Deliberation: <ROLE A> ↔ <ROLE B>, with <ROLE C> on <topic>. CEO synthesizes.
Question: <one-line restatement>
```

### Step 2 — Memory gate (Sakthi check)

Before any role opens, check memory for the entities in play (per CLAUDE.md §2). A deliberation about *the Q3 launch* must read the existing entity profile for *Q3 launch* before either role speaks. If memory has prior decisions on the same question, surface them in the synthesizer's turn — don't let the council relitigate what's already been decided unless the user is explicit.

If no memory MCP is connected, note it once in prose and proceed from charter only.

### Step 3 — Round 1: Opening positions

Each participant gets **one paragraph, 4–8 sentences max**. Each opens with this scaffold:

```
## <ROLE> opening

**Position:** <one-sentence recommendation>
**Framework:** <which heuristic, playbook, or threshold is being applied>
**What's given up:** <the tradeoff this role is accepting>
**Evidence:** <citation — memory entry, entity profile card, framework threshold, data-MCP timestamped source, OR explicit "estimate, flagged">
```

Use each role's loaded skill body (CFO grounding, CMO concreteness, CSO long-horizon framing, etc.). Do not blur voices. A CFO paragraph reads in numbers. A CMO paragraph names a channel. A CSO paragraph asks *what does winning look like.*

### Step 4 — Round 2: Rebuttals

Each role gets **one rebuttal paragraph**. The rebuttal must do three things in order:

1. **Steelman the other role** — one sentence on their strongest point. Genuinely.
2. **Name the actual fault line** — where you still disagree, and why.
3. **Refine your position or concede** — updated recommendation, or "concede on X, hold on Y."

Format:

```
## <ROLE> rebuttal

**Steelman of <other role>:** <one sentence on their strongest point>
**Where I still disagree:** <the real point of contention, one or two sentences>
**Refined position:** <updated recommendation, or explicit concession>
```

If a third role is in play, they get one paragraph in this round too — but only on the slice they own (CLC on the regulatory edge, CHRO on the personnel edge), not a full rebuttal of both A and B.

### Step 5 — CEO synthesis

The CEO turn does four things and only these four:

1. **Names the real call.** Not the surface question — the underlying tradeoff being decided.
2. **Decides, decisively.** No "it depends." No "consider both."
3. **Names the cost accepted.** Who absorbs what.
4. **Specifies the next move.** Action, owner (if known), timing, and the signal that would change the call.

Format:

```
## CEO synthesis

**The real call:** <what's actually being decided beneath the surface question>
**Decision:** <do X — one sentence, imperative>
**Cost accepted:** <what's given up and who absorbs it>
**Next move:** <concrete action, owner, timing>
**Reversibility:** one-way door | two-way door — Bezos frame; one-way doors deserve more scrutiny.
**Signal to revisit:** <what observation would force a re-deliberation>
```

### Step 6 — Diary write (mandatory)

Deliberation is **always engage-mode by definition**. End by invoking the [`sakthi-diary`](../sakthi-diary/SKILL.md) skill with:

- `mode: deliberate`
- `agent: council`
- `entities: <every named entity touched>`
- `transcript: <the full deliberation, openings + rebuttals + synthesis>`
- All other SABHA_DIARY v1 fields populated.

Place the entry in `<wing>/deliberations` (see the diary skill for wing/room rules).

If no memory MCP is connected, skip the call but produce the same SABHA_DIARY v1 yaml block at the end of the reply so the user can copy/paste it into their preferred store.

## Output discipline

- **Length budget:** 600–900 words total for a 2-role deliberation. 900–1,300 for 3 roles. Hard cap. If you can't synthesize within budget, the question wasn't ready for deliberation.
- **No padding.** Each section earns its place. If a rebuttal has nothing new, concede in one line and move on.
- **No blurred voices.** A CFO paragraph reads like a CFO. Mid-paragraph role-switching is forbidden.
- **Grounding stays mandatory.** CLAUDE.md §3 applies in every voice. A deliberation that invents numbers in three roles is three times worse than a single-role hallucination — every wrong fact has been laundered through "but the *council* said so." Cite or flag, every time.
- **Sources, not vibes.** A position grounded only in "in my experience…" is weaker than a position citing a framework threshold or an entity profile card. The synthesizer should weight grounded positions more heavily.

## Advanced — sub-agent deliberation

For high-stakes decisions where role purity matters and token cost is acceptable, dispatch each role as a separate `claude` sub-agent with the role's skill explicitly loaded. The orchestrator (this skill) collects the role outputs and runs the synthesis turn directly.

Trigger: user passes `--deep` to `/deliberate`, or the decision has six-figure / multi-quarter consequences.

Cost: ~2-3× tokens and meaningful latency. Use sparingly.

In normal mode all roles are played within one Claude turn — the skill body is the contract and role discipline is enforced by the section scaffolds above.

## Anti-patterns

- **Manufactured disagreement.** Don't force a debate when two roles actually align. If openings agree, skip rebuttals and go straight to synthesis with a one-line "council aligned."
- **Survey-mode deliberation.** Each role recommends **one** thing, not three options. If a role says "we could do A, B, or C," the role failed to deliberate.
- **CEO as tie-breaker, not synthesizer.** The CEO names what's *really* being decided beneath the surface, then calls it. "Go with whoever talked longer" is not synthesis.
- **Skipping the diary write.** If you deliberated, you compound. No exceptions.
- **Deliberating questions that should route.** Most questions are not deliberation-grade. Route by default; deliberate by exception.

## Example invocations

- `/deliberate Should we hire a second engineer this quarter or extend runway by 3 months?`
- "Let the council deliberate on raising Acme Cloud prices to $1,800/yr."
- "Have CSO and CFO argue build-vs-buy for the data pipeline."
- "/deliberate --deep Should we accept the term sheet from Investor X?" (sub-agent mode)
