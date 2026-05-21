# Backlog

Ideas captured for future consideration. **Distinct from [`ROADMAP.md`](./ROADMAP.md):**
- **Roadmap** = decided commitments and explicit founder-level holds (with rationale).
- **Backlog** = ideas worth keeping but not yet ranked, sized, or committed. Items move from backlog → roadmap when a triggering condition occurs.

Each entry includes: **what it is**, **why it might matter**, **the trigger** that would promote it to active work, and (where useful) **a sketch of the approach**.

Newest items at the top of each section.

---

## Cross-surface continuity

### Cross-surface context card (`sakthi context-card`)

**What:** A `sakthi context-card` command that exports the user's current Sakthi state as a paste-able ~2–3K-token markdown blob (single doc) and/or as a folder of 9 role-wing markdown files (for upload to Claude.ai Project knowledge). Lets a user paste their Sakthi state into Claude.ai Projects, Cowork, ChatGPT, or any other surface that accepts a system prompt or knowledge files.

**Why it might matter:** Claude.ai chat, Cowork, and ChatGPT all run in the cloud and cannot reach a local MCP server. Today, Sabha + Sakthi work natively in Claude Code only; other surfaces fall back to charter-only. The context card is the pragmatic bridge — not real-time sync, but a curated paste-able snapshot. Solves the most-asked likely-future question: *"Can I use my Sakthi in Claude.ai too?"*

**Why not now:**
- The product is shipping; no operator has actually asked for this in writing yet
- Local-first thesis is the wedge — exporting Sakthi to a cloud surface is a small but real compromise that should not be the default messaging
- Implementation is ~150 LOC + docs + a privacy-posture note; medium effort, not trivial

**Trigger to promote:**
- First operator who installs Sabha + Sakthi asks how to use them in Claude.ai
- A user writing a usage story on a heterogeneous workflow (Claude Code at the desk, Claude.ai on the phone)
- Cross-surface continuity becomes a competitive ask vs Claude Memory

**Approach sketch:**
- New module: `mempalace/context_card.py`
- For each of the 9 wings: top-N recent drawers from `decisions` room + top-N recent diary entries
- Plus a header from `CLAUDE.md` profile cards (named entities, obligations, financial anchors)
- Token-count and trim oldest until under `--max-tokens` (default 2800)
- Three surfaces: MCP tool `sakthi_context_card`, CLI `sakthi context-card`, Python entry point
- Optional auto-refresh hook on every `tool_diary_write`
- `--as-files <dir>` mode writes 9 separate markdown files for Project-knowledge upload
- Document the privacy posture honestly in `docs/MEMORY-OPTIONS.md`: card content enters Anthropic's logs when pasted; regulated-industry users should stay Claude-Code-only

---

## Eval rigor

### Cross-model judging (defeat in-family bias) — ⚙️ HARNESS SHIPPED 2026-05-18

**Status update:** The judge-provider abstraction shipped in `evals/judge_clients.py` with the `--judge-provider {anthropic,openai,google}` flag in `run_eval.py`. **The harness is ready; the run is pending an API key for a non-Anthropic provider.**

This was de-coupled from the founder-held LLM-agnostic SDK item because **using a non-Anthropic model as a *judge* is not the same as running Sabha *as candidate* on a non-Anthropic model.** The judge is a measurement instrument; the candidate is the protocol-under-test.

**Trigger to promote** (now: just run it):
- User has access to an OpenAI or Google API key
- Willing to spend ~$30-80 on a cross-model judge run

**To run:**

```bash
export ANTHROPIC_API_KEY=...
export OPENAI_API_KEY=...
pip install 'openai>=1.0'
python evals/run_eval.py --judge-provider openai --judge-model gpt-5 --out-name 2026-MM-DD-openai-judge
```

### Expand chanakya eval to N=15

**What:** Grow the chanakya activation eval from 7 to 15 questions: more invocation phrasings, more adversarial topics, more roles.

**Why it might matter:** Current N=7 means a single failure swings the headline by 14pp. The 100% activation / 100% discipline numbers from the 2026-05-17 re-run are *consistent with* the skill being excellent and *consistent with* it being mediocre — CI is wide.

**Why not now:**
- The eval is doing its job at small N (caught a real discipline leak)
- The skill itself is more stable than the headline number suggests
- Cheap to run when ready (~$1 in API per run), so the cost of waiting is low

**Trigger to promote:**
- About to broadcast eval numbers publicly (LinkedIn post, conference talk, paper)
- A discipline leak shows up in real usage that the current 7-question set doesn't catch

**Approach sketch:**
- Add 5 invocation phrasings: "channel Chanakya," "use a neeti," "answer like Chanakya," "in the Chanakya tradition," "what would the Arthashastra say"
- Add 3 negative controls: phrases that *look* like invocation but aren't ("Chanakya was a strategist" in a question about strategy, etc.)
- Add 3 cross-role topics that don't currently appear

### Operator-judged eval (the human-judgment lever)

**What:** Recruit 5–10 real founders/operators. Each rates 10 reply pairs (baseline vs Sabha) blind. Compare against LLM-judge results.

**Why it might matter:** All eval numbers today are LLM-judged. Even with cross-model judges, the methodology has the same shape. A small panel of real operators rating real questions is the strongest single piece of evidence Sabha actually helps decision-making — not just rubric scores.

**Why not now:**
- Recruiting operators is a manual effort; needs a small comp budget ($50–200 per rater)
- Best done after the product has some real usage so the questions are operator-shaped, not invented
- Premature evaluation before adoption signals would be reading tea leaves

**Trigger to promote:**
- 20+ real users on Sabha (organic install signal)
- A real operator volunteers to rate
- Investor / grant conversation requires human-judged data

---

## Protocol tuning (from main-eval findings)

### Length-discipline patch for deep-skill loading

**What:** A short rule added to `CLAUDE.md` §3 (ANSWER section) that says: *"When a deep skill is loaded, the reply length should not exceed the no-skill baseline — the skill informs, it doesn't fill the reply."*

**Why it might matter:** The 2026-05-16 eval re-run (all 9 deep skills loaded vs the v1.3.1 5-of-20) showed `length_discipline` dropping from 3.15 → 2.85. Deep-skill content is tempting the model to render more, not just reason with more. The cso-02 truncation was the smoking gun — the reply was cut off mid-sentence at the 1200 max_tokens limit.

**Why not now:**
- Need to confirm whether this is a real protocol-tuning fix or whether the eval just needs `max_tokens` bumped (see next item)
- Risk: over-tightening length discipline may erode the concreteness gains deep skills provide

**Trigger to promote:**
- After the max_tokens bump, re-run the eval; if `length_discipline` doesn't recover to ~3.15, this is the next intervention

### Bump eval harness `max_tokens` from 1200 → 2000 — **🔼 PROMOTION CRITERION FIRED 2026-05-18**

**Status:** cso-02 was truncated in *two consecutive* runs (2026-05-16 and 2026-05-18 n=50). Both times the judge rationale cited the truncation explicitly. This is no longer "wait for a triggering reason" — it's blocking eval accuracy. Promote to immediate work.

**What:** A one-line change in `evals/run_eval.py` to give replies more room. Bump `max_tokens=1200` → `max_tokens=2000` in `generate_reply`.

**Tradeoff:** bigger replies use more tokens (~$5 more per full run) and risk *real* length-discipline regression — i.e., the model fills the available space. Mitigation: pair the bump with a re-emphasis of length discipline in CLAUDE.md (also in BACKLOG).

**Expected effect:** cso-02 should flip to Sabha. n=50 pairwise should go 48/50 → 49/50 (only legitimate baseline win remains: under-05 attribution gap).

### Tighten v3 judge prompt for structured sub-criteria output — *NEW 2026-05-18*

**What:** The v3 sub-axis rubric prompt (in `evals/judge.py`) asks the judge to return JSON with three `*_sub` dict fields containing 5 binary sub-criteria each. In the 2026-05-18 live run, Opus 4.7 reasoned about the sub-criteria mentally (rationales reference them) but emitted JSON in the v2 flat-composite shape. The fallback path in `score_reply` handled it cleanly — the run completed with v2-equivalent scoring — but the v3 sub-axis decomposition didn't activate, so we can't slice *which* sub-criteria are saturating.

**Why it might matter:** the whole point of v3 was to defeat rubric saturation by forcing the judge to score discrete binary criteria. If the judge defaults to the v2 holistic format, the saturation problem persists (decisiveness still hits 5/5 in 33/50 = 66% of Sabha replies). Without sub-criterion slicing, we can't tell whether Sabha is winning on *every* sub-criterion or just one or two that drag the composite up.

**Approach sketch (any of these may work; try in order):**
1. Add a worked example to the judge prompt showing the exact JSON structure expected, with all sub-criteria filled in.
2. Switch the response format to "schema-enforced JSON" using Anthropic's tool-use API (force structured output via tool calls).
3. Use a less-capable judge model (e.g., Haiku 4.5) which may follow the schema more literally; trade off some judgment quality for format compliance.
4. Multi-step prompt: first ask for sub-criteria one at a time, then synthesize.

**Trigger to promote:**
- After the max_tokens fix above runs (need a fresh eval anyway)
- Before any external broadcast that cites sub-criterion-level data

### CIO `cio-01` challenge-the-premise heuristic

### CIO `cio-01` challenge-the-premise heuristic

**What:** Add to `skills/roles/cio/heuristics.md` an explicit rule: *"Before recommending a vendor migration, audit whether the current bill is correct given the usage. Cite the math."*

**Why it might matter:** cio-01 has been a baseline-win across two eval runs. The judge reward was the baseline reply challenging the $2,400 bill as suspicious for 800K req/mo before committing to migration advice. The CIO deep skill teaches frameworks; it does not (yet) teach *question challenge*. This heuristic addition tests whether the meta-disposition is teachable.

**Why not now:**
- One eval-question signal isn't a strong basis for a protocol change
- Risk: an explicit "challenge the bill" heuristic may make the role more contrarian on simple questions, hurting other replies

**Trigger to promote:**
- Real operator reports a "the council didn't question my premise" failure
- A separate eval question with a similar reframe-needed shape lands and Sabha loses it

### Reference-mode skill loading

**What:** Currently the eval harness injects `SKILL.md + REFERENCE.md + heuristics.md` verbatim into the system prompt (~5,000+ tokens per role). Alternative: load only `SKILL.md`; let the model query the deeper files via filesystem read when needed. Tests whether deep content informing vs being rendered.

**Why it might matter:** Hypothesis from the 2026-05-16 eval: more content in the system prompt → more content rendered into the reply. Reference-mode would let the deep skills *inform* without *bulking*.

**Why not now:**
- Significant harness rework; not a one-line change
- Claude Code skill router likely already loads them this way in production (only the eval harness loads all three files)
- May not move the headline meaningfully

**Trigger to promote:**
- Length-discipline patch (above) doesn't recover the metric
- The eval harness and real Claude Code behavior diverge measurably

---

## Content + ergonomics

### More profession-specific preset councils

**What:** Add presets to `examples/`:
- `lawyer.CLAUDE.md` — solo attorney / boutique firm partner
- `healthcare-founder.CLAUDE.md` — health-tech founder (HIPAA-aware)
- `indie-dev.CLAUDE.md` — single-developer SaaS or game dev
- `real-estate.CLAUDE.md` — broker / agency principal
- `k12-educator.CLAUDE.md` — teacher or admin
- Translations of `professional-sakthi.CLAUDE.md` into Hindi, Tamil, Japanese, Spanish

**Why it might matter:** The protocol's value compounds with usage. Every working preset is evidence the protocol generalizes beyond the founder/exec default.

**Why not now:**
- Speculative without operator pull — better to respond to actual requests
- Translation quality requires native speakers, not Claude-translated drafts

**Trigger to promote:**
- A user from that profession asks
- A community contributor PRs one and it works in practice

### Web UI for previewing a Sabha reply (no-install)

**What:** A small static web page (single HTML file or simple Cloudflare Worker) where someone can type a question and see what a Sabha-routed reply looks like, without installing the plugin.

**Why it might matter:** Reduces the "I have to install a plugin to try this" friction. The single highest-leverage demo asset.

**Why not now:**
- Requires Anthropic API access on the server side (cost / auth complexity)
- Risk of running up an unattended API bill
- Distracts from operator-grade positioning toward consumer-demo positioning

**Trigger to promote:**
- A real adoption conversation where the lead asks "show me what it does"
- A conference talk where a live demo is needed

### Premium skill packs — actual content (not just scaffold)

**What:** Vertical packs of role-deep skills. Initial candidate: **SaaS-CFO** (deeper unit economics, fundraise prep for specific stages, board-deck templates, SaaS-specific KPIs). Possible additions: **healthcare-CLC** (HIPAA, FERPA, FDA paths), **agency-CMO** (creative-shop-specific positioning).

**Why it might matter:** Open-source core stays MIT; premium packs become an optional revenue line. Doesn't compromise the project; adds an operator-paid layer.

**Why not now:**
- Speculative — no commercial demand signal yet
- The scaffold-only bet on the roadmap is the first test of whether there's pull

**Trigger to promote:**
- An operator pays for or asks to pay for a vertical pack
- Inbound from agencies / consulting firms wanting to license

### CLI/MCP for "what does my council currently know about me?"

**What:** A read-only `sakthi profile` command that reads the user's `CLAUDE.md` profile cards + recent diary entries and renders a one-page snapshot. Different from `sakthi context-card` — that one's for paste-into-AI; this one is for the human user reviewing their own Sakthi.

**Why it might matter:** Once Sakthi has months of decisions, "what is in here?" becomes a real ergonomic ask.

**Why not now:**
- No user with deep Sakthi history yet
- Adjacent to `sakthi list-drawers` + `sakthi search` which already exist

**Trigger to promote:**
- A user reports their Sakthi has > 50 drawers and they want a state-of-the-council view

---

## Distribution + community

### Public LinkedIn / X launch announcement

**What:** A long-form LinkedIn post (already drafted earlier in session) + the infographic outputs from the Cowork session.

**Why it might matter:** The repo is camera-ready. The eval numbers are honest. The work this session has been substantial; not posting it leaves it invisible.

**Why not now:**
- The infographic files (`sabha-os-infographic.html`, `sabha-os-linkedin.{jpg,svg}`) are untracked in the working tree; need a decision on whether to commit them or keep them out of the repo
- Founder may want a clearer head before broadcast; LinkedIn-tired audience is more forgiving of a one-day delay than a tired post

**Trigger to promote:**
- Founder is ready to ship
- Eval results are validated against the discipline patch (re-run pending the cso-02 fix bundle)

### Add a `SECURITY.md`

**What:** Standard GitHub security disclosure file. Currently the PRIVACY.md handles data-handling; no formal vulnerability-disclosure path documented.

**Why it might matter:** Low-effort, signals operational maturity. Required for some downstream compliance reviews.

**Why not now:**
- No real attack surface in the protocol layer (markdown). Sakthi has some surface but is small.
- Cosmetic until there's a meaningful security ask.

**Trigger to promote:**
- A serious enterprise review asks for it
- A vulnerability is reported (in which case write it on the day of)

---

## Pramana follow-on ideas

The Pramana research agent shipped at 0.1.0 with the core workflow (3+ searches, mandatory contrarian pass, 9-section briefing, A/B/C/D source tiers, citation-graph self-check). These items are deferred refinements — captured here, not blocking 1.0.

### Source-tier weighting in council decisions

**What:** When a Pramana briefing is brought to the Sabha council, allow tagging each cited claim by tier ("this comes from Tier-A primary docs, that from Tier-C navigation"). The council weights recommendation confidence accordingly, and the reply explicitly notes when a decision rests on weak-tier evidence.

**Why it might matter:** A decision grounded only in Tier-C sources should say so. A decision grounded in Tier-A primary documents can be more confident. Currently the tiers exist in the briefing but don't propagate into council reasoning.

**Why not now:** Pramana 0.1.0 produces the tiers; integrating them into council confidence-scoring is post-1.0 refinement and probably benefits from real usage data first.

**Trigger to promote:**
- An operator reports making a decision on Tier-C evidence and wishes they'd known
- A CSO or CFO reply flags weak-source risk in a real engagement and the friction is repeatable

### Persist Pramana briefings into Sakthi

**What:** A Sakthi MCP tool (`sakthi_file_pramana_briefing` or similar) that takes a Pramana markdown output and files it into the appropriate role wing (a competitive briefing lands in `cso/research`, a regulatory brief lands in `clc/research`). Auto-classification by content, manual override available.

**Why it might matter:** Pramana briefings are valuable research artifacts; filing them into Sakthi makes "what did I research about X six months ago?" a searchable graph query rather than a folder-scrubbing exercise. Closes the loop between the *fetch* layer (Pramana) and the *remember* layer (Sakthi).

**Why not now:** Pramana and Sakthi are intentionally independent — each works without the other. Tight integration adds coupling that should be earned by a real workflow demand.

**Trigger to promote:**
- An operator with both installed asks how to file Pramana output into Sakthi
- The "what did I find on X a month ago?" query becomes a repeated pain point

### Sector-specific briefing templates

**What:** Alternate `briefing-template.md` variants for common research domains where the generic 9-section template wants tuning — e.g., a `medical-device-template.md` that adds a "Predicate / 510(k) lineage" section, a `financial-services-template.md` that adds a "Capital / regulatory tier" section, a `competitive-template.md` that adds a "Battlecard / objection-handling" section.

**Why it might matter:** Operators in regulated industries already have implicit templates for these — making them explicit and switchable inside Pramana would save reformatting work and reduce the "I always forget to ask about X" failure mode.

**Why not now:** The 9-section default works for ~80% of briefings. Building variants before usage data is template-fitting in the dark.

**Trigger to promote:**
- 3+ briefings produced in the same vertical where the user has consistently added the same custom sections post-hoc
- An external contributor proposes a sector variant

### Cross-judge eval for Pramana briefings

**What:** An LLM-as-judge eval harness analogous to the main Sabha eval — pairs of (Pramana briefing vs. no-system-prompt baseline) on a fixed question set, judged on rubric axes specific to Pramana (citation accuracy, contrarian-view depth, tier-balance, recommendation specificity).

**Why it might matter:** Sabha has a credible eval story (96% pairwise win rate, cross-model judge harness). Pramana ships with no eval — currently it's "looks good in a few hand-tested cases." Without measurement, claims about the contrarian search and tier discipline are aspirational.

**Why not now:** Eval design is expensive (n=50 took multiple iterations on the rubric). The contrarian-view dimension in particular is hard to grade reliably. Better to ship Pramana, see what real usage looks like, and design the eval against actual failure patterns than to over-engineer one in advance.

**Trigger to promote:**
- A contributor proposes a Pramana eval design and is willing to drive it
- A user-reported failure pattern that the eval would catch (e.g., "Pramana keeps citing Tier-C sources for time-sensitive claims")

---

## How items move from backlog → roadmap

1. The trigger condition fires.
2. Founder makes the call: promote, defer further, or kill.
3. If promoted, the entry moves into [`ROADMAP.md`](./ROADMAP.md) under the appropriate quarter with sized scope, kill criteria, and the explicit named tradeoff.
4. The backlog entry stays here with a one-line annotation: *"Promoted to roadmap 2026-MM-DD; see ROADMAP.md §<quarter>."*

Items can also be killed from the backlog directly when they become obsolete or wrong. Killed items stay in the file with a strikethrough and a one-line *"Killed YYYY-MM-DD because <reason>"* note — preserves the audit trail of *"why we didn't do this"* which is often more valuable than the do-list.

## Why this file exists

Three reasons:

1. **Capture-without-commit.** Operator-grade projects accumulate ideas faster than they can be ranked. Without a backlog, ideas either get forgotten or jam the roadmap. This file is the parking lot.
2. **The council recommends; the founder decides.** A backlog lets the council surface things without forcing decisions. Items sit here until the founder calls.
3. **Public-facing transparency.** Contributors and curious readers can see what's been considered. Sometimes the most useful artifact in an open-source project is the list of *what we chose not to build, and why*.
