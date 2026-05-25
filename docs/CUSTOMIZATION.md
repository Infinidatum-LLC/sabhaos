# Customization

Sabha is a single file — `CLAUDE.md` — plus a thin shell of skills and slash commands. Everything you'd want to change lives in `CLAUDE.md`.

## Picking a starting council

Three reference councils ship in `examples/`. Pick the one closest to what you want, copy it to your project's `CLAUDE.md`, and edit:

- **`personal-sakthi.CLAUDE.md`** — life roles (Health, Finance, Family, Career, Time, Self). Use this when Sabha is helping you run your life, not a business.
- **`professional-sakthi.CLAUDE.md`** — the default C-suite council (CIO, CAIO, CFO, CMO, CSO, CXO, CHRO, CEO). Use this for company / business work.
- **`developer-sakthi.CLAUDE.md`** — code roles (Architect, Reviewer, Security, Performance, QA, Mentor). Use this for engineering-heavy work where the questions are mostly about code, not business.

Profession-specific variants — `solo-founder.CLAUDE.md`, `agency.CLAUDE.md`, `researcher.CLAUDE.md` — are tuned subsets of the professional council.

## Quick personalization (5 minutes)

Open `CLAUDE.md`. Find the `Known entities` block:

```
PEOPLE:      [your name], [co-founder], [key teammate], [key contractor]
COMPANIES:   [your company], [parent entity], [subsidiary]
PRODUCTS:    [product 1], [product 2], [internal codename]
PROJECTS:    [active initiative], [upcoming launch], [bet you're tracking]
OBLIGATIONS: [key compliance frame, e.g. GDPR / SOC2 / EU AI Act]
FINANCIAL:   [bank, brokerage, runway-relevant accounts]
```

Replace the brackets with your real entities. These act as anchors — when you say "what's left on Project X?" the model knows X is a real thing, not a typo.

## Renaming or removing roles

The role table in `CLAUDE.md` is the source of truth. Edit it.

**Example — solo founder, no employees, no AI product:**

```markdown
| Role | Covers |
|------|--------|
| **Operator** | Day-to-day ops, infra, tools, vendors, finances. |
| **Strategist** | Long-horizon bets, positioning, partnerships. |
| **CMO**  | Marketing, brand, content, channels. |
| **CXO**  | UX, onboarding, support. |
| **CEO**  | The call when the others disagree. |
```

You don't have to use C-suite titles at all. "Strategist / Marketer / Builder / Editor" works fine.

## Tuning the voice

Find the `ANSWER` section. Defaults are:

- Professional
- Decisive
- Terse over verbose
- Concrete over abstract
- Tradeoff-aware

To make it warmer, swap "Terse over verbose" for "Conversational but on-point." To make it more exploratory, swap "Recommend, don't survey" for "Recommend, then sketch two alternatives." Both work — they just change the texture.

## Wiring in a memory MCP — where your Sakthi lives

Sabha is local-first by design: your accumulated knowledge — your **Sakthi** — should live on your machine, not in someone else's database. The `MEMORY` section in `CLAUDE.md` is intentionally generic so you can wire in any MCP that exposes search and write tools.

The default example uses [**Sakthi Graph**](https://github.com/Infinidatum-LLC/sakthi-graph) — MIT, open-source, graph-shaped, runs locally. Other options that work the same way:

- **mem0** — semantic key-value memory, hosted or self-host
- **Letta** — stateful agents with memory
- **Zep** — temporal knowledge graph memory
- **Pieces** — desktop-app memory with MCP support
- **plain `memory/*.md`** — a folder of markdown files, no MCP at all

To swap memory providers, edit the `MEMORY` section to name your tool:

```markdown
## 2. MEMORY — your Sakthi lives here

A memory layer is connected: **mem0**. Before asserting facts about my known
entities, query mem0. Tools to use:
- `mcp__mem0__search` — for any entity I name
- `mcp__mem0__add` — when I tell you something new about an entity

Known entities (these have records in memory):
PEOPLE: ...
```

The model will then prefer the memory MCP over guessing, and every engage-mode session will write back so your Sakthi compounds.

## Adding domain knowledge

If your work has heavy domain content (a regulatory frame, a product taxonomy, a unique sales motion), add a section to `CLAUDE.md`:

```markdown
## Domain context

Our product is X. Our customers are Y. Our pricing is Z (free / pro / enterprise).
Our top three competitors are A, B, C. We never compare to D — they're a partner.
```

Keep it under 500 words. Anything bigger goes into `memory/` files referenced by an MCP.

## Multiple Sabhas

You can have one Sabha per project — Claude Code reads `CLAUDE.md` from the project root. A consulting Sabha (CMO/CSO/CXO) and a coding-side Sabha (CIO/CAIO/CEO) can coexist on the same machine. Just give each project its own `CLAUDE.md`.

## Disabling Sabha temporarily

- `claude plugin disable sabha-os` — turn it off entirely
- Use a project without `CLAUDE.md` — Sabha defaults to off when there's no protocol file
- Or: just ask "no Sabha for this — explain X like a tutor." The skill will skip routing when explicitly waived.

## Sharing your CLAUDE.md

If you build a great preset for a specific profession (lawyer, real estate agent, indie game dev, K-12 teacher), please PR it into `examples/`. The goal is a library of starting points.
