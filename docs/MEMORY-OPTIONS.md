# Memory backends

Sabha is the protocol. The memory backend is a choice. This page is the honest comparison — pick the one that fits your trust model, your operational reality, and your stack.

> **The protocol works with no memory at all.** Sabha is decision discipline first; memory is what makes the decisions compound. If you're not sure which backend you want, start with no backend, then add one when you feel the friction.

---

## TL;DR pick-by-need

| Your situation | Use |
|---|---|
| Just want Claude to remember me across chats. Default user. | **Claude Memory** (built-in; zero-config) |
| Solo founder / family office / boutique advisory. Want institutional memory that never leaves my machine. | **Sakthi Graph** |
| Working in health, legal, finance, defense, or regulated industries. Compliance matters. | **Sakthi Graph** — see [`FOR-REGULATED-INDUSTRIES.md`](./FOR-REGULATED-INDUSTRIES.md) |
| Already invested in mem0 / Letta / Zep / Pieces. | **Your existing memory MCP** (Sabha is memory-MCP-agnostic) |
| Minimalist; just want a folder of markdown the AI reads. | **Plain `memory/` folder** |
| Want a memory layer that isn't tied to one LLM vendor (future-proofing). | **Sakthi Graph** or **mem0** — both are LLM-agnostic at the storage layer. Note: Sabha-the-protocol is currently Claude-focused; cross-model SDK is not on the active roadmap. |

---

## The five real options

### 1. Claude Memory (Anthropic-built, default)

What it is: Anthropic's cross-conversation memory feature, server-side, woven into Claude.ai, Projects, and Claude Code. Semantic recall of prior context.

| Dimension | Verdict |
|---|---|
| Cost | Included in your Claude plan |
| Where it lives | Anthropic's servers |
| Shape | Semantic / unstructured |
| Audit | Opaque (Anthropic-managed) |
| Portability | Claude-only |
| Setup | Zero-config |

**Best for:** Default user. Personal assistant use cases. Casual continuity. If you don't have a strong privacy or auditability requirement, this is the path of least resistance — and it'll keep getting better as Anthropic ships.

**Sabha + Claude Memory:** They compose cleanly. Sabha routes the question; the role queries memory via Claude's built-in mechanism; the council answers. No wiring needed in `CLAUDE.md`.

**Limits to be honest about:**
- Your accumulated knowledge lives on someone else's server. That's a fact, not a flaw — just know it.
- Memory is semantic, not structured. You cannot deterministically ask "all CFO decisions from Q1."
- Tethered to Claude. If you ever want to run the same questions through GPT-5 or Gemini Ultra, the memory doesn't migrate.

---

### 2. Sakthi Graph (local-first, recommended for power users)

What it is: A fork of [MemPalace](https://github.com/MemPalace/mempalace), MIT-licensed, ChromaDB-backed, pre-shaped for the Sabha 9-role taxonomy. Runs locally; no cloud.

| Dimension | Verdict |
|---|---|
| Cost | Free; ~300MB embedding model + your disk space for the palace |
| Where it lives | Your machine (`~/sakthi` by default) |
| Shape | Graph-shaped: wings (role-scoped) → rooms → drawers; entity relationships |
| Audit | Fully open; `ls ~/sakthi`, grep your own data |
| Portability | LLM-agnostic; works with any LLM that supports MCP |
| Setup | 5 commands; `sakthi init --sabha ~/sakthi` |

**Best for:**
- Privacy-sensitive users (regulated industries, deal-flow data, IP-heavy work, government-adjacent).
- Power users who want structured queries (`wing="cfo"`, `room="decisions"`) not just semantic recall.
- Operators who want their council's institutional memory to be a durable, portable asset — a directory on their disk, not a cloud subscription. (The memory layer is LLM-agnostic via MCP; the Sabha protocol layer is currently Claude-focused, with cross-model support held for a future quarter.)

**Install:** `claude plugin install sakthi-graph@sabha-marketplace && uv tool install sakthi-graph && sakthi init --sabha ~/sakthi`

**Bonus capability:** [`sakthi sittham`](https://github.com/rdmurugan/sakthi-graph/blob/develop/docs/SITTHAM.md) ingests any folder (code, papers, transcripts) into the right Sabha role wing. Single command. No equivalent in any cloud memory product.

**Limits to be honest about:**
- Not zero-config. 5 commands. Some users will bounce.
- Lives on your machine — that's the point, but it also means no automatic sync across your devices. If you want your council's memory on both your laptop and desktop, you need to sync `~/sakthi` yourself (rsync, syncthing, iCloud Drive, etc.).
- The embedding model download is ~300MB on first run.

---

### 3. mem0 / Letta / Zep / Pieces (existing memory MCPs)

What they are: Third-party memory products with MCP support. Each has its own shape and trust model.

| Product | What it's good at | Cloud / Local |
|---|---|---|
| [mem0](https://mem0.ai) | Fast key-value semantic memory | Cloud or self-host |
| [Letta](https://letta.com) | Stateful agents with structured memory | Cloud or self-host |
| [Zep](https://www.getzep.com) | Temporal knowledge graph for agents | Cloud or self-host |
| [Pieces](https://pieces.app) | Desktop-app memory, code-snippet focus | Local (desktop) |

**Best for:** You already use one of these. Don't migrate just for Sabha. Sabha is memory-MCP-agnostic at the protocol layer — wire yours in.

**How to wire:** edit the `MEMORY` section of `CLAUDE.md` to name your tool's MCP tools:

```markdown
## 2. MEMORY — your memory layer

A memory layer is connected: **mem0**. Before asserting facts about my known
entities, query mem0. Tools to use:
- `mcp__mem0__search` — for any entity I name
- `mcp__mem0__add` — when I tell you something new
```

The protocol will use those tool names instead of `sakthi_*`.

---

### 4. Plain `memory/` folder (minimalist)

What it is: A folder of markdown files. No MCP. The AI reads them as files via the existing filesystem tools.

| Dimension | Verdict |
|---|---|
| Cost | Free |
| Where it lives | Your machine |
| Shape | Whatever folder structure you create |
| Audit | Your files |
| Portability | Anywhere |
| Setup | `mkdir memory/` |

**Best for:** People who don't trust any MCP. People who want the AI to read a curated note-set, not a probabilistic recall. Researchers managing a paper corpus.

**How to wire:** point `CLAUDE.md` at the folder:

```markdown
## 2. MEMORY — your memory layer

A `memory/` folder lives at the project root. Before asserting facts about
known entities, read the relevant files. Index:
- memory/people.md       — who I work with
- memory/products.md     — what we're building
- memory/decisions/      — one file per decision, dated
```

**Limits to be honest about:**
- No semantic search. The AI grep-reads. Fine for <100 small files; degrades after that.
- No diary tool call — but the [`sakthi-diary`](../skills/modes/sakthi-diary/SKILL.md) skill still emits the `SABHA_DIARY v1` yaml block as a chat artifact on engage/deliberate mode; append it to `memory/decisions/<date>-<topic>.md` yourself.
- No graph queries.

---

### 5. No memory backend at all

What it is: Just Sabha. The protocol still works — you just don't get cross-session compounding.

**Best for:**
- Trying Sabha out for the first time. Get comfortable with the routing discipline before adding memory.
- One-off projects where memory isn't worth setting up.
- Privacy-maximalists who don't want *any* memory persistence.

The CLAUDE.md acknowledges this with a one-line note: *"No memory layer in this surface — answering from charter only."*

---

## Can I use multiple memory backends?

Yes, with a caveat. Most usefully:

- **Claude Memory + Sakthi Graph.** Claude Memory handles casual personalization (your name, your timezone, your communication preferences). Sakthi handles structured institutional memory (the actual decisions, the role-specific facts). They coexist without conflict because they answer different kinds of questions.
- **Sakthi + plain `memory/`.** Sakthi for searchable institutional memory. `memory/` for hand-curated reference docs you want read verbatim (vision docs, principles, the latest cap table).

What doesn't work: two semantic memory MCPs at the same time (mem0 + Letta). The protocol can only query one at a time and you'll get conflicting facts. Pick one.

---

## How to switch later

You can move from one backend to another at any time. The protocol cares about the *shape* of the memory call (search → results → cite), not which tool fulfills it. To migrate Claude Memory → Sakthi:

1. Install Sakthi (as above).
2. Edit `CLAUDE.md` `MEMORY` section to name the `sakthi_*` tools.
3. Optionally, ingest your existing context: paste a session summary to Sabha and say *"file this as a memo to my Sakthi."* Engage mode will write a `SABHA_DIARY v1` entry via the [`sakthi-diary`](../skills/modes/sakthi-diary/SKILL.md) skill.

There is no automatic migration tool. Memory is your data; you decide what gets carried over.

---

## The diary contract (v2.2.0+)

Whatever backend you pick, the diary entry shape is the same — a `SABHA_DIARY v1` yaml block with these fields: `date, agent, mode, entities, question, recommendation, tradeoff, next_move, reversibility, sources, transcript` (transcript only on deliberate mode). The `sakthi-diary` skill defines the template once; per-backend transport is a translation table:

| Backend | Diary write |
|---|---|
| **Sakthi Graph** | `sakthi_diary_write(agent_name=<role>, entry=<yaml>, topic=<room>)` — note: upstream tool currently expects AAAK-compressed format; v1 yaml adapter is a v2.3 stretch item |
| **mem0** | `mem0_add(content=<yaml>, metadata={wing, room, agent})` |
| **Letta** | `letta_archival_memory_insert(text=<yaml>, tags=[wing, room, agent])` |
| **Zep** | `zep_add_memory(session_id=<wing>, content=<yaml>, metadata={room, agent})` |
| **plain folder** | Append yaml block to `memory/<wing>/<room>.md` |

This means: if you switch backends, your diary entries remain readable across the switch. The template is the contract; transports are interchangeable.

---

## The honest read

For 80% of users, **Claude Memory + Sabha** is the right pairing. Easy, default, good enough.

For 15% of users — privacy-sensitive operators, regulated industries, multi-LLM power users — **Sakthi Graph + Sabha** is the right pairing. It costs setup time; it pays back in durability.

For 5% — minimalists, researchers, integration-shy users — **`memory/` folder + Sabha** or **no memory + Sabha** is fine.

There is no "best" backend. There is the one that fits your operating reality. Pick it and stop optimizing.

---

## Related reading

- [`docs/FOR-REGULATED-INDUSTRIES.md`](./FOR-REGULATED-INDUSTRIES.md) — the privacy / compliance wedge in detail
- [`docs/ARCHITECTURE.md`](./ARCHITECTURE.md) — how memory plugs into the full stack
- [`docs/CUSTOMIZATION.md`](./CUSTOMIZATION.md) — how to wire a non-default memory MCP
- [Sakthi Graph](https://github.com/rdmurugan/sakthi-graph) — the local-first option in detail
