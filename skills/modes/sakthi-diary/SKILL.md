---
name: sakthi-diary
description: Auto-compounding diary that turns every engage-mode and deliberate-mode answer into a persistent Sakthi entry. Activates on engage mode, on deliberation completion, or when the user says "file this," "log it," "diary this," "save the decision," "remember this call." Writes via `sakthi_diary_write` (or the equivalent for the user's configured memory MCP) using the SABHA_DIARY v1 template. This is how Sakthi compounds — every recorded decision becomes a queryable memory in future sessions.
---

# Sakthi diary — how the council compounds

Sabha without compounding is a stateless chatbot in a vest. The diary is the difference.

Every engage-mode and deliberate-mode answer must end with a diary write. Over weeks and months, those entries become the council's memory of *this* user — who they are, what they've decided, why they accepted the tradeoffs they did. New sessions begin warm because the diary is queryable.

## When to write — the firing rules

| Trigger | Write the diary? |
|---|---|
| Ask mode (default chat) | **No** — unless the user explicitly says "file/log/diary/save this" |
| Engage mode (`/engage`, "file this," doc produced) | **Yes — always** |
| Deliberate mode (`/deliberate`, council session) | **Yes — always**, with the full transcript in `body` |
| User says "file this," "log it," "save the decision," "remember this" | **Yes** |
| User explicitly says "don't log this" | **No**, and confirm in one line |
| No memory MCP connected | **No call**. Emit the SABHA_DIARY v1 yaml block at the end of the reply so the user can copy/paste it. Note the absence once per session in prose (not echoed each reply). |

If you're unsure, ask in one line: *"File this as a diary entry?"*

## The SABHA_DIARY v1 template

Every diary entry — regardless of mode or memory backend — uses this shape. The contract is the template; the transport varies.

```yaml
# SABHA_DIARY v1
date: YYYY-MM-DD                  # today, absolute (never "yesterday" or "last week")
agent: <lead role>                # cfo, cso, ceo, ..., or "council" for deliberations
mode: ask | engage | deliberate
entities: [Entity1, Entity2, ...] # every known entity touched (people, companies, products, projects)
question: |
  <one-line restatement of what the user asked — written so a future session reads it cold>
recommendation: |
  <the council's call — 1–3 sentences, with numbers and named tradeoffs>
tradeoff: |
  <what's accepted in exchange — one or two sentences>
next_move: |
  <concrete action: who does what by when, or "none" if information-only>
reversibility: one-way | two-way | n/a
sources:
  - <entity-profile-card-name>
  - <framework-name e.g. "Skok LTV/CAC ≥ 3">
  - <data-mcp-source@timestamp e.g. "Stripe MRR pulled 2026-05-14 09:00 UTC">
  - <"user-stated">
  - <"estimate, flagged">
transcript: |
  <full deliberation transcript if mode=deliberate; otherwise omit this field>
```

**Field discipline:**

- `date` is always today's date in YYYY-MM-DD. Never relative.
- `agent` is the *lead* role; for deliberations the lead is `council`.
- `entities` is a list of *named* entities — write them the way they're registered in the user's profile cards. Don't invent.
- `question` should read well cold — a future session pulling this back must understand the call without re-reading the chat.
- `sources` is mandatory and non-empty. If the only source is the user's own statement, write `user-stated`. If a number was a guess, write `estimate, flagged`. A diary entry with no sources is corrupting Sakthi — refuse to write it.
- `transcript` exists only for deliberations. For engage entries, omit.

## Wing / room placement

The diary goes somewhere. Sakthi Graph uses wings and rooms; other backends use folders, tags, or namespaces. Map as follows:

| Mode + lead role | wing | room |
|---|---|---|
| engage, lead = CFO | `<user-wing>` | `decisions/finance` |
| engage, lead = CMO | `<user-wing>` | `decisions/marketing` |
| engage, lead = CSO | `<user-wing>` | `decisions/strategy` |
| engage, lead = CIO | `<user-wing>` | `decisions/infra` |
| engage, lead = CAIO | `<user-wing>` | `decisions/ai` |
| engage, lead = CXO | `<user-wing>` | `decisions/experience` |
| engage, lead = CHRO | `<user-wing>` | `decisions/people` |
| engage, lead = CLC | `<user-wing>` | `decisions/legal` |
| engage, lead = CEO | `<user-wing>` | `decisions/ceo` |
| deliberate (any roles) | `<user-wing>` | `deliberations` |
| user-instructed "file this" with no clear lead | `<user-wing>` | `inbox` |

`<user-wing>` defaults are:

- Sabha OS contributors / repo work → `sabha-os`
- Infinidatum work → `infinidatum`
- Personal / unspecified → `personal`
- New user with no configuration → `sabha`

If the user has explicitly configured wings (e.g., `/sakthi config wing=acme`), honor that.

## Tool call shape — Sakthi Graph (reference implementation)

```
sakthi_diary_write(
  wing="<wing>",
  room="<room>",
  agent_name="<role-lowercase>",        # "cfo", "council", etc.
  body="<the SABHA_DIARY v1 yaml block, verbatim>"
)
```

For Sakthi Graph today the MCP tool prefix is `mempalace_` (legacy upstream name; the conceptual product is Sakthi Graph). Call `mempalace_diary_write` with the same arguments. This will rename when the upstream MCP rebrands; the template stays stable.

## Other memory backends

The contract is the SABHA_DIARY v1 template; the transport varies.

| Backend | Write shape |
|---|---|
| **mem0** | `mem0_add(content=<yaml>, metadata={wing, room, agent})` |
| **Letta** | `letta_archival_memory_insert(text=<yaml>, tags=[wing, room, agent])` |
| **Zep** | `zep_add_memory(session_id=<wing>, content=<yaml>, metadata={room, agent})` |
| **plain MemPalace** (no Sakthi shaping) | `mempalace_add_drawer(wing, room, body=<yaml>, agent_name)` |
| **Local folder fallback** | Append `<yaml>` block to `memory/<wing>/<room>.md` |

If the user's backend isn't listed, follow the same pattern: pass the SABHA_DIARY v1 yaml as the body/content field, populate metadata with `wing`, `room`, `agent`.

## Grounding the diary itself

The diary is not a place to invent. If the recommendation in chat cited a number, the diary cites the same number with the same source. If the recommendation flagged an estimate, the diary records it as an estimate. A diary that smooths over uncertainty corrupts future sessions — Sakthi inherits whatever you write, and a fabricated number written today will be retrieved as a "fact" six months from now.

If you can't write a grounded diary entry, write a *shorter* one — drop fields rather than invent values. Better an entry that reads "next_move: undetermined — pending user input" than one that invents an action.

## Querying back — write for cold reads

In future sessions, the diary is read by `sakthi_search` (semantic, wing/room-scoped) and `sakthi_kg_query` (entity-scoped). Future-you will retrieve these entries with no surrounding context. Write accordingly:

- Full sentences in `question`, `recommendation`, `tradeoff`. Not phrases.
- Named entities, not pronouns. "Aadhav" not "the employee."
- Dates absolute. Numbers with units.
- The recommendation should be readable as a standalone statement: "On 2026-05-19 council recommended raising Acme Cloud price to $1,800/yr, accepting ~12% trial drop-off, because LTV/CAC was 2.1 (below Skok 3.0 threshold)."

## Anti-patterns

- **Vague entries.** *"Talked about pricing."* Worthless. Write the recommendation and the tradeoff.
- **Skipping fields.** If `next_move` is *none*, write `none` — don't omit.
- **Echoing the chat reply verbatim.** The diary is a compressed canonical record, not a transcript dump. (Deliberations are the exception — the transcript *is* the record for deliberations.)
- **Writing on every ask reply.** Ask mode does **not** auto-diary. Only engage / deliberate / explicit user instruction.
- **Inventing entities.** If a name appears in the chat that isn't in the user's profile cards or Sakthi entity graph, do not register it in `entities`. Flag it for the user instead: *"I noticed you mentioned 'Project Helix' — should I add it to your project entities?"*
- **Backdating.** `date` is today. Never write a diary entry stamped with an earlier date.

## One-line summary

> Engage produces a deliverable. Deliberate produces a transcript. The diary is what makes either of them *persist* — so the next session walks in knowing what this session decided.
