# Contributing

Sabha OS is tiny by design — a `CLAUDE.md`, a skill, three slash commands. The whole protocol fits on one page. PRs should preserve that.

## What we want

- **New profession presets** in `examples/` (lawyer, indie dev, teacher, real-estate broker, etc.).
- **Memory MCP integration snippets** — short blocks for `CLAUDE.md` that wire in popular memory tools.
- **Translations** of `CLAUDE.md` into other languages.
- **Real usage stories** in `docs/` — what role mix worked for you, what you cut.
- **Pramana enhancements** in `pramana/` — additional contrarian-view heuristics, source-quality tier refinements, framework tweaks (e.g., a sector-specific briefing template for medical-device or financial-services research). Pramana is in this repo at [`pramana/`](./pramana/) — same `skills/<name>/SKILL.md` + `references/` shape as everything else.

## What we don't want

- Long meta-documentation. The protocol is the product. If the docs get longer than the protocol, something is off.
- Extra dependencies *in the protocol path*. Sabha itself runs entirely on Claude's existing capabilities — no npm install, no python deps in `CLAUDE.md`, `skills/`, or `commands/`. The `evals/` directory is exempt and has its own `requirements.txt`.
- Hard-coded business logic in the skill. All customization should be doable by editing `CLAUDE.md`.

## How to PR

1. Fork.
2. Make your change. Keep it small and focused.
3. If you added an **example** preset: install your variant locally and ask 3–4 real questions; confirm Claude routes them correctly.
4. If you added a **deep skill** addition (a new framework, template, or playbook): include a short worked example showing it being applied with real numbers.
5. If you changed **routing** or **voice**: re-run the eval (`python evals/run_eval.py --limit 5` is fine for a smoke test). Don't merge a routing change that drops the pairwise win rate.
6. Open the PR with a one-paragraph explanation of who the change is for and what it changes.

## Where things live

| Goal | Touch |
|---|---|
| Add / change roles | `CLAUDE.md` |
| Add a framework to a role | `skills/roles/<role>/REFERENCE.md` |
| Add a template / playbook | `skills/roles/<role>/templates/` or `playbooks/` |
| Add a data-MCP integration | `skills/roles/<role>/data-hooks/<vendor>.md` |
| Add a new preset council | `examples/<name>.CLAUDE.md` |
| Change classification behavior | `skills/sabha-router/SKILL.md` |
| Add an eval question | `evals/questions.yaml` |
| Improve Pramana (the research agent) | `pramana/skills/pramana/SKILL.md` (workflow), `pramana/skills/pramana/references/*.md` (framework, template, source-quality tiers) |
| Add a sibling plugin (like Pramana) | new top-level subdirectory with its own `.claude-plugin/plugin.json`; register it in the root `.claude-plugin/marketplace.json` |

See [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) for the full picture of which file owns which concern.

## Style

- **Terse.** The protocol itself is terse; the docs should match.
- **Concrete.** Real vendors, real dollar amounts, real file paths beat hand-waving.
- **Tradeoff-aware.** If a doc recommends X, it should name what's given up.
- Markdown for docs, `.docx` only for filed reports (none in this repo).
- No emojis in protocol files. They're allowed in docs sparingly.

## Suggesting a feature without writing it yet

If you have an idea worth capturing but not ready to implement, file it as an issue with the `backlog` label, or open a PR adding an entry to [`docs/BACKLOG.md`](./docs/BACKLOG.md). The backlog is intentionally open — items live there until a trigger condition fires and they're promoted to the roadmap (or killed with a reason). The format is:

- **What it is** (one paragraph)
- **Why it might matter** (one paragraph)
- **Why not now** (the constraint)
- **Trigger to promote** (what would make this worth doing)

## Reporting bugs / security issues

- General bugs: open an issue at [github.com/Infinidatum-LLC/sabhaos/issues](https://github.com/Infinidatum-LLC/sabhaos/issues).
- Security: see [`SECURITY.md`](./SECURITY.md) if it exists, otherwise file a private issue.

## Code of conduct

Be kind. The internet is mean enough already.
