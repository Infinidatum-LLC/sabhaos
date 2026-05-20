# Quickstart — get Sabha working in 10 minutes (no installation needed)

> **This guide is for you if** you've used Claude.ai (the website) but you've never installed software from GitHub, never used a terminal, and don't know what `git clone` means. You'll be up and running in under 10 minutes.

> **Setup time:** ~10 minutes
> **Required:** a free Claude.ai account
> **Optional (for advanced users later):** Claude Code, a memory MCP

---

## What you'll be able to do

After this quickstart, you'll have a personalized AI council inside Claude.ai. Every substantive question you ask will get answered by the right "role" — a CFO for money questions, a CMO for marketing, a CIO for tech, and so on. Each answers in a decisive, tradeoff-aware voice — no more five-options-to-consider replies.

### What you'll get (no-install path)

| Feature | Available |
|---|---|
| The Sabha routing protocol (Routing: CFO, etc.) | ✓ Yes |
| Decisive answers with named tradeoffs | ✓ Yes |
| Nine role personas (CFO, CMO, CIO, CAIO, CSO, CXO, CHRO, CLC, CEO) | ✓ Yes |
| Deep CFO and CMO frameworks (Kahneman, Christensen, Porter, etc.) | ✓ Yes (with extra paste — Step 6) |
| Personal / Developer council presets | ✓ Yes |
| Memory across sessions (your Sakthi compounds) | ✗ No — needs technical setup |
| Slash commands like `/engage` and `/route` | ✗ No — Claude Code only |

You get roughly **70% of Sabha's value** with no installation. The memory layer (the "Sakthi" that accumulates over months) is the part you'd add later if you want to go deeper.

---

## Step 1 — Open Claude.ai

In your web browser, go to **[claude.ai](https://claude.ai)** and sign in. If you don't have an account, sign up — the free tier is enough to try Sabha.

---

## Step 2 — Create a new Project

A Claude Project is a private workspace where you can give Claude permanent instructions. This is where Sabha lives.

1. Click the **Projects** icon in the left sidebar.
2. Click **Create Project** (or the "+ New Project" button).
3. Give it a name — e.g., *"My Sabha"* or *"My Council"*.
4. Click **Create**.

You'll land in the new Project. Look for a section called **"Custom instructions"**, **"Project knowledge"**, or **"Instructions"** — this is where you'll paste Sabha.

---

## Step 3 — Pick the right council for you

Sabha ships with three reference councils. Pick the one that fits what you'll use it for most:

| Council | Pick this if you're... | Roles included |
|---|---|---|
| **Professional** | Running a business, making company decisions | CFO, CMO, CIO, CSO, CXO, CHRO, CAIO, CEO |
| **Personal** | Making life decisions (health, money, family, career) | Health, Finance, Family, Career, Time, Self |
| **Developer** | Doing software / engineering work | Architect, Reviewer, Security, Performance, QA, Mentor, Tech Lead |

You can change your mind later or set up separate Projects for each. For your first try, pick the one that matches the biggest chunk of your work.

---

## Step 4 — Copy the council file from GitHub

Each council is a single file you copy as-is.

1. Open the council you picked (right-click → open in new tab):
   - **Professional:** [examples/professional-sakthi.CLAUDE.md](../examples/professional-sakthi.CLAUDE.md)
   - **Personal:** [examples/personal-sakthi.CLAUDE.md](../examples/personal-sakthi.CLAUDE.md)
   - **Developer:** [examples/developer-sakthi.CLAUDE.md](../examples/developer-sakthi.CLAUDE.md)

2. On the GitHub page, click the **"Raw"** button (top-right of the file view). The page will now show plain text.

3. Select all the text (`Cmd+A` on Mac, `Ctrl+A` on Windows) and copy it (`Cmd+C` / `Ctrl+C`).

---

## Step 5 — Paste it into your Claude Project

1. Go back to your Claude.ai Project.
2. Find the **Custom instructions** field.
3. Paste (`Cmd+V` / `Ctrl+V`).
4. Click **Save** (or the equivalent).

Your council is now active. Every conversation in this Project will use the Sabha protocol.

---

## Step 6 — Fill in YOUR context (the bracketed parts)

Look in the text you just pasted for a section called **"MEMORY"**. You'll see something like this:

```
PEOPLE:      [your name], [co-founder], [key teammate], [key contractor]
COMPANIES:   [your company], [parent entity], [subsidiary]
PRODUCTS:    [product 1], [product 2], [internal codename]
PROJECTS:    [active initiative], [upcoming launch], [bet you're tracking]
```

Replace the bracketed text with your actual people, companies, products, and projects.

**Why this matters:** these are the names Sabha will use as anchors. When you mention "Project X" in a question, the council knows X is a real thing in your world, not a typo.

**Example, filled in for a fictional founder:**

```
PEOPLE:      Alice (me), Bob (co-founder), Maya (engineering lead)
COMPANIES:   Acme Co. (my company)
PRODUCTS:    Acme Cloud (main product)
PROJECTS:    Q3 enterprise launch, customer-onboarding rewrite
```

Save the changes.

### Want the deep CFO / CMO frameworks too? (optional, recommended for professional council)

If you picked the **Professional** council and want the deep CFO/CMO knowledge layer (the frameworks from Kahneman, Christensen, Porter, McKinsey, etc.), do this:

1. Open these two files on GitHub:
   - [skills/roles/cfo/REFERENCE.md](../skills/roles/cfo/REFERENCE.md)
   - [skills/roles/cmo/REFERENCE.md](../skills/roles/cmo/REFERENCE.md)
2. For each: click **Raw**, select all, copy.
3. In your Claude Project, scroll to the bottom of the custom instructions.
4. Paste both — separate them with a blank line.
5. Save.

This gives your CFO and CMO roles access to detailed frameworks instead of just role descriptions. It's the difference between a generic advisor and an experienced one.

---

## Step 7 — Ask your first question

Start a new conversation inside the Project and ask something substantive — a real decision you're facing, not trivia.

**Try one of these to see Sabha work:**

For the **Professional** council:
> *"We have $200K in the bank, burn is $35K/month, and a competitor just shipped the feature we were planning. Should I hire another engineer to ship faster, or pivot the feature?"*

For the **Personal** council:
> *"I'm being offered a remote contract role at 20% more than my current salary but it means giving up the office community I love. How should I think about this?"*

For the **Developer** council:
> *"Our service is at 800ms p99 latency. Should I refactor the database queries or add a Redis cache layer first?"*

### What a good Sabha reply looks like

You should see something like this at the top:

```
Routing: CFO (primary). CSO weighs in on the competitive pressure.

[The recommendation in one or two sentences, with numbers]

[The tradeoff — what you give up]

[The next concrete move]
```

If you see the `Routing:` line — it's working. If you don't, jump to the troubleshooting section below.

---

## Step 8 — Pick your mode: ask, engage, or deliberate

Sabha has three modes built in:

| Mode | When to use it | How to trigger |
|---|---|---|
| **Ask** (default) | Quick question, chat reply | Just ask normally |
| **Engage** | The decision matters enough to write down | Say *"file this as a memo"* or *"engage mode — write it up"* (Claude Code: `/engage`) |
| **Deliberate** | Two roles disagree and you want them to argue it out | Say *"let the council deliberate on X"* or *"have CFO and CSO debate this"* (Claude Code: `/deliberate <question>`) |

In **ask mode**, Claude gives you a tight inline answer.
In **engage mode**, Claude produces a document-grade write-up you can save, share, or come back to in 6 months. Engage mode also auto-writes a `SABHA_DIARY v1` entry to your memory so the decision compounds.
In **deliberate mode**, two or three roles open with opposed positions, rebut each other once, and the CEO synthesizes — output is a structured transcript (hard cap ~900 words for two roles). Deliberate mode also auto-writes a diary entry, with the full transcript in the body.

**Use engage mode when:**
- The decision involves real money, time, or risk
- You'll want to remember the reasoning later
- You're sending the output to someone else (investor, partner, customer)

**Use deliberate mode when:**
- Two roles obviously disagree and you want the contested tradeoff named (pricing — CFO vs CSO; build-vs-buy — CIO vs CSO; hire-now-or-wait — CHRO vs CFO)
- A single-role answer would smuggle in a contested assumption
- The call is engage-grade *and* genuinely cross-functional

For everything else — stay in ask mode. The default is fast and conversational.

---

## Troubleshooting

### "Claude isn't showing the `Routing:` line"

- Check that you saved the custom instructions in your Project. Some Claude.ai UIs require an explicit Save button after pasting.
- Make sure you started a **new conversation** after pasting — old conversations don't see new instructions.
- Verify the paste went through completely. Scroll to the bottom of the instructions; you should see *"github.com/rdmurugan/sabhaos"* at the very end. If not, the paste was cut off — try again.

### "Claude is still giving me five options to consider"

- Check the **ANSWER** section in the pasted instructions. It should say *"Decisive. Recommend, don't survey."* If it's missing, the paste was incomplete.
- Try asking a more concrete question. Sabha activates on **substantive** questions (decisions, tradeoffs, recommendations). It explicitly skips trivia, factual lookups, and chit-chat. "What's the weather?" won't route. "Should we hire X?" will.

### "It still doesn't know my project / people / company"

- Did you fill in the `[BRACKETS]` in the MEMORY section (Step 6)? If they still say `[your name]`, the council has nothing to anchor on.
- Each Project's memory is separate from other Projects. If you mention something in conversation, it lives in that conversation; it doesn't carry between Projects unless you also put it in the custom instructions.
- For memory that actually accumulates across sessions, you need a local memory MCP — that's the optional technical setup at the end.

### "The roles don't match my work"

- You probably want a different preset. Try the other councils (Personal / Developer). You can keep them in separate Projects.
- Or **customize** — open the council file, rename roles to match your situation. A consulting agency might rename CIO to "Creative Director." A researcher might use "Methodologist" instead of CAIO. Edit the role table; Claude will adapt.

### "I'm getting too much output"

- That's ask vs engage mode. If you accidentally triggered engage (by saying "write it up" or "draft a memo"), Claude is producing a doc-grade output. Just say *"keep it in ask mode"* and try again.

---

## When you're ready to go deeper

The no-install path covers ~70% of Sabha's value. If you find yourself using it daily, two next steps unlock the rest:

### Add memory (the "Sakthi" that compounds)

In a single conversation, Claude remembers what you told it. Across conversations, it forgets. To make memory accumulate over time, you install **Sakthi Graph** — a local memory MCP that ships in the same marketplace as Sabha. Sakthi is a fork of MemPalace, pre-shaped for the Sabha council (the 9 role wings are bootstrapped automatically).

If you're already using Claude Code, four terminal commands:

```bash
claude plugin marketplace add rdmurugan/sabhaos     # if not already added
claude plugin install sakthi-graph@sabha-marketplace
uv tool install sakthi-graph
# (alternative if you don't have uv: pip install sakthi-graph)
sakthi init --sabha ~/sakthi                         # bootstraps 9 role wings
```

The first two register the plugin and its MCP server config. The third installs the actual Python binary that runs the memory server. The fourth bootstraps the Sabha-shaped palace.

After that, restart Claude Code. Sabha will detect Sakthi and start grounding answers in your accumulated knowledge-graph. Every decision and conversation can be filed into a searchable graph that lives entirely on your machine — nothing leaves.

**If you're not using Claude Code** (just Claude.ai web), you can't run MemPalace today — memory MCPs require a local runtime. Sabha still works in Claude.ai's web Project as described in earlier steps; you just don't get the cross-session compounding. Most non-technical users skip this step.

**Don't want MemPalace specifically?** Sabha is memory-MCP-agnostic. mem0, Letta, Zep, and Pieces all work with the same protocol. See [`docs/CUSTOMIZATION.md`](./CUSTOMIZATION.md) for swap instructions.

### Use Claude Code instead of Claude.ai

[Claude Code](https://claude.com/claude-code) is the command-line version of Claude. It supports plugins (Sabha installs as one), slash commands (`/ask`, `/engage`, `/route`), and direct file operations. It's much faster for daily use once you're comfortable with a terminal.

If you want to make the jump, the [main README](../README.md) walks through the Claude Code installation path.

---

## Where to next

- **More council presets:** see [examples/](../examples/) for solo-founder, agency, researcher variants of the professional council
- **Customizing roles, voice, memory:** [docs/CUSTOMIZATION.md](./CUSTOMIZATION.md)
- **The philosophy behind the protocol:** [docs/PHILOSOPHY.md](./PHILOSOPHY.md)
- **What each role does in detail:** [docs/ROLES.md](./ROLES.md)
- **The full system view (council + memory + corpus-ingest):** [docs/ARCHITECTURE.md](./ARCHITECTURE.md)
- **Does it actually work?** [docs/EVALS.md](./EVALS.md) summarizes the results; full data in [evals/](../evals/)
- **Ingest folders into your Sakthi:** once you've installed Sakthi Graph, `sakthi sittham <folder>` files any folder's distilled graph into the right Sabha wing. Power-user feature; safe to skip until you want it.

---

## Questions / problems / feedback

- **Found a bug or have a question?** Open an issue at github.com/rdmurugan/sabhaos/issues
- **Want to share a council preset for your profession?** PRs welcome
- **Just want to say it helped?** Star the repo — it helps others find it

---

**Sabha OS · MIT License · github.com/rdmurugan/sabhaos**
