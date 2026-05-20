# Sabha OS — evals

A reproducible eval comparing Claude's replies with and without the Sabha protocol on **50 operator-style questions** across four buckets (original-operator / adversarial-reframing / cross-role-edge / underdog). Current results live in [`results/latest.md`](./results/latest.md); historical runs preserved alongside.

**Latest headline (v3 rubric, n=50, Anthropic judge, 2026-05-18):** Sabha wins **48/50 pairwise (96%)**, Wilson 95% CI **[86.5%, 98.9%]**. Per-bucket: original 19/20, adversarial 10/10, cross-role 10/10, underdog 9/10.

> **Note:** the eval harness has Python dependencies (`anthropic`, `PyYAML`). The Sabha *protocol itself* has no runtime dependencies — these are only for running the eval. Keeping that boundary clean is intentional; see [`../CONTRIBUTING.md`](../CONTRIBUTING.md).

## What's measured

Each question is sent to the same candidate model twice:

- **Baseline** — no system prompt.
- **Sabha** — [`../CLAUDE.md`](../CLAUDE.md) loaded as the system prompt.

Each reply is judged by an LLM-as-judge (default: Claude Opus 4.7) on the **v3 sub-axis rubric** — five axes, three of which are decomposed into 5 binary sub-criteria each to defeat the rubric saturation seen in v1/v2:

| Axis | Scale | What it measures |
|---|---|---|
| `decisiveness` | 0-5 (sum of 5 binary sub-criteria) | made_clear_recommendation, stated_confidence_or_conditions, named_alternative_rejected, committed_specific_next_move, avoided_hedging_language |
| `tradeoff_named` | 0-5 (sum of 5 binary sub-criteria) | named_what_is_given_up, quantified_the_cost, named_who_is_affected, stated_time_horizon, gave_reasoning_to_accept |
| `concreteness` | 0-5 | Real vendors, dollar amounts, dates, file paths? |
| `routing_present` | 0/1 | Does the reply open with `Routing: <ROLE>`? |
| `length_discipline` | 0-5 (sum of 5 binary sub-criteria) | no_three_paragraph_windup, no_padding_phrases, no_unnecessary_disclaimers, no_redundancy, every_paragraph_advances |

Then a **pairwise preference** judge sees both replies (in randomized order) and picks the one a busy operator would find more useful.

## What we expect to see

- `routing_present`: baseline ≈ 0.0, sabha ≈ 1.0 (this is a sanity check; the protocol exists or it doesn't).
- `decisiveness`, `tradeoff_named`, `concreteness`, `length_discipline`: meaningful lift under Sabha — typically +1.0 to +2.0 per axis on a 0-5 scale.
- `pairwise`: Sabha wins ≥ 70% of paired comparisons. Below that and the protocol isn't earning its keep.

The actual numbers live in [`results/latest.md`](./results/latest.md). The interpretation of the most-recent run — what's signal, what's noise, what to fix next — is in [`ANALYSIS.md`](./ANALYSIS.md).

## Running the eval

```bash
# 1. Install deps in a venv
python -m venv .venv
source .venv/bin/activate
pip install -r evals/requirements.txt

# 2. Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Run it
python evals/run_eval.py

# Options
python evals/run_eval.py --limit 5                    # smoke test
python evals/run_eval.py --candidate-model claude-sonnet-4-6
python evals/run_eval.py --judge-model claude-opus-4-7
python evals/run_eval.py --out-name 2026-05-15-sonnet

# If a run was interrupted (network, API overload, Ctrl-C), resume it:
python evals/run_eval.py --resume                     # picks up today's run
python evals/run_eval.py --resume --out-name <name>   # resume a named run
```

Cost for a full 50-question run: roughly **$3-7** (Sonnet candidate × 100 generations + Opus judge × 150 calls). For a smoke test, `--limit 5` runs in ~$0.50.

### Reliability

The harness checkpoints **after every question** — JSON + Markdown snapshots are written to `results/` as the run progresses. If the API gets overloaded (HTTP 529), rate-limited, or your connection drops, you won't lose prior work; `--resume` picks up where it stopped. All API calls (both generation and judging) retry with jittered exponential backoff (up to 6 attempts, ~60s total) on transient errors.

## Methodology notes (for the reviewer who wants to nitpick)

- **Candidate model held constant across conditions.** Only the system prompt differs. We're testing the *protocol's* effect, not the model's.
- **Deep role skills (v1.3.0+) are simulated.** In Claude Code, deep role skills under `skills/roles/<role>/` activate via the skill router. The eval harness uses the raw Anthropic API and has no router, so when a question's `role:` tag matches an existing deep skill directory, the harness appends that skill's `SKILL.md` + `REFERENCE.md` + `heuristics.md` to the system prompt for the Sabha condition. The `deep_skill_loaded` column in the per-question results table flags which rows included this content. Without this simulation, the eval would test only CLAUDE.md and miss the v1.3.0 depth layer entirely.
- **Judge is a different model class than candidate** by default (Opus judges Sonnet) to reduce self-bias. You can flip with `--judge-model claude-sonnet-4-6`.
- **Pairwise order randomized** per question, seeded by `--seed`. Avoids position bias.
- **Three retries on API errors** with exponential backoff. Network blips don't kill a run.
- **No fine-tuning, no few-shot examples** are introduced — the only thing the model sees beyond the question is the protocol charter.
- **Question set is at v2 (n=50, four buckets).** v1 (n=20) is retired; raw data preserved in `results/2026-05-14.{json,md}` and `results/2026-05-16.{json,md}` for audit. Future revisions live in `questions.yaml` with a version bump; results carry the version they were run against.
- **Rubric is at v3 (sub-axis decomposition).** v1 and v2 retired because `decisiveness` and `tradeoff_named` saturated at 5/5. The v3 binary sub-criteria split lets the judge discriminate between strong and very-strong replies. Numbers from v1/v2 rubrics (e.g., the old "+5.95 rubric Δ") are not comparable to v3 numbers and should not be cited as ongoing claims.

## Limitations (be honest about these)

- **n=50 still has finite CI width** (~12pp at 95% on a 96% point estimate). The pairwise lower bound (86.5%) is the defensible claim, not the point estimate.
- **LLM-as-judge has known biases** — verbosity preference, position effects, agreement with formatted text. We mitigate (rubric, randomization) but don't eliminate. A human-judged spot-check on a random 10-question subset is the right complement.
- **In-family judge bias** — current results use an Anthropic judge against an Anthropic candidate. The cross-model judge harness ships (`--judge-provider {anthropic,openai,google}`) but a cross-family run is the next credibility move.
- **Sabha is tested on Claude.** The protocol may transfer to other models, but we haven't measured that.
- **Operator-style questions only.** Sabha is explicitly *not* designed for trivia, code-only tasks, or exploratory research — those questions aren't in the set.

## Contributing

Want to add questions? PRs welcome. Two rules:

1. Operator-style — a real decision an operator would face, not a quiz question.
2. No single "correct" answer — we're measuring *reply shape*, not factual accuracy.

If you find a category we're under-representing, add 3-5 questions for it and bump the question-set version in the YAML.

If you build a human-judge variant, even better — drop it in as `evals/human_judge.py` and PR.
