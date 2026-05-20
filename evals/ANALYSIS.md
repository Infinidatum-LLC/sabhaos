# Sabha OS — eval analysis

> **⚠️ RETIRED — this file analyzes the v1.3.1 run (n=20, v1 rubric, 2026-05-14).**
>
> **The current shipped result is n=50 / v3 rubric / 2026-05-18 → 48/50 pairwise (96%), Wilson 95% CI [86.5%, 98.9%].** See [`results/latest.md`](./results/latest.md) for the rendered current run and [`../docs/EVALS.md`](../docs/EVALS.md) for the current analysis. The v1.3.1 numbers below (+5.95 rubric Δ, 17/20 pairwise) are preserved for audit only and **must not be cited as ongoing claims** — the v1 rubric saturated, and the n=20 CIs were too wide to support magnitude claims. See [`../docs/EVALS.md` § "Retired baselines"](../docs/EVALS.md) for why these were retired.
>
> **What this file is.** Interpretation of the v1.3.1 eval results. The raw data is in [`results/2026-05-14.json`](./results/2026-05-14.json) (machine-readable). This file is the *read* — what the numbers meant at the time, what was signal vs noise, and what was roadmapped next. Frozen as historical context.
>
> **Run metadata.**
> - Source: `evals/results/2026-05-14.json`
> - Run date: 2026-05-14
> - Candidate model: `claude-sonnet-4-6`
> - Judge model: `claude-opus-4-7`
> - Question set: v1, n = 20
> - Status: **retired** (see banner above)

---

## Headline

Across 20 operator-style questions, Sabha-routed replies scored **+5.95 on a 20-point rubric** (baseline 10.85 → Sabha 16.80) and won **17/20 pairwise (85%)** against a no-system-prompt baseline.

Breaking that down by whether a deep skill was loaded:

- **Deep-skill questions (CFO, CMO, n=5):** 100% pairwise win rate, +6.60 mean rubric gap.
- **No-deep-skill questions (CIO, CSO, CAIO, CXO, CHRO, CEO, n=15):** 80% pairwise win rate, +5.73 mean rubric gap.

The deep-skill layer adds only **+0.87 on rubric** but **+20 percentage points on pairwise**. The framework grounding doesn't just push replies higher — it makes them *consistently win* when the operator-judge compares.

The three baseline pairwise wins (cio-01, cio-02, ceo-03) all share one pattern: **Sabha applied formal structure to questions that needed reframing**. All three are no-deep-skill roles. The deep skills do contain reframe-the-question patterns; the bare protocol doesn't enforce them strongly enough yet. This is the v1.6 roadmap signal.

---

## Per-axis breakdown

| Axis | Baseline mean | Sabha mean | Δ | Sabha stdev | Sabha at ceiling (5/5) | Read |
|---|---:|---:|---:|---:|---:|---|
| decisiveness | 3.00 | 4.65 | +1.65 | 0.81 | 16 / 20 | Saturated. Rubric stops discriminating. |
| tradeoff_named | 3.20 | 4.70 | +1.50 | 0.57 | 15 / 20 | Saturated. Same. |
| concreteness | 3.05 | 4.30 | +1.25 | 0.73 | 9 / 20 | **Most discriminating axis.** Real variance. |
| length_discipline | 1.60 | 3.15 | +1.55 | 0.75 | 0 / 20 | Hardest axis. Even Sabha doesn't fully nail terseness. |
| routing_present | 0.00 | 1.00 | +1.00 | 0.00 | n/a (binary) | Sanity check passed. |
| **total** | **10.85** | **16.80** | **+5.95** | 2.33 | — | Sabha is more consistent (lower stdev) than baseline. |

**Methodology flag:** `decisiveness` and `tradeoff_named` are *saturated* — the rubric awards 5/5 too easily. For v2 of the eval, tighten the 5/5 threshold so Sabha has room to be *less than perfect*. The current rubric understates differentiation between strong and very-strong Sabha replies.

**Length-discipline asymmetry:** baseline stdev on this axis is 0.60 — almost all baseline replies cluster at "padding everywhere." Reading the actual baselines, they're not *that* padded; the judge may be reading section headers as inflation. Possible judge bias on this axis specifically. Worth flagging in any external claim.

---

## Per-role breakdown

| Role | n | Deep? | Sabha mean | Baseline mean | Gap | Pairwise wins |
|---|---:|---|---:|---:|---:|---|
| CMO | 2 | ✓ | 16.0 | 8.0 | **+8.0** | 2/2 |
| CAIO | 2 | — | 18.0 | 10.5 | +7.5 | 2/2 |
| CIO | 3 | — | 18.3 | 12.0 | +6.3 | 1/3 |
| CSO | 3 | — | 15.3 | 9.3 | +6.0 | 3/3 |
| CFO | 3 | ✓ | 18.7 | 13.0 | +5.7 | 3/3 |
| CHRO | 2 | — | 17.0 | 11.5 | +5.5 | 2/2 |
| CXO | 2 | — | 15.0 | 10.0 | +5.0 | 2/2 |
| CEO | 3 | — | 15.7 | 11.3 | **+4.3** | 2/3 |

Three observations:

1. **CMO has the highest gap (+8.0)** despite small n=2. The marketing canon (Jobs-to-be-Done, positioning, channel portfolio) provides *more* uplift over the baseline than the financial frameworks do for CFO. Reason: baseline Claude already gives passable financial answers, but is genuinely weak on positioning reasoning. The deep CMO skill closes a bigger gap.

2. **CEO has the lowest gap (+4.3) and the most losses (1/3 pairwise lost).** CEO is the "doesn't fit any other role" route — questions that need synthesis, not framework application. The protocol's structured format helps less here. **Real:** the CEO role is where Sabha's structure becomes friction.

3. **CIO is the strangest pattern.** Rubric gap is large (+6.3), but pairwise is the worst non-CEO row (1/3). All three CIO questions had no deep skill loaded. Sabha won on form, lost on substance twice. **Clearest "build the CIO deep skill next" signal in the data.**

---

## The three baseline pairwise wins — all signal, no noise

Each of these has Sabha scoring *higher* on the rubric but losing the pairwise comparison. That contradiction is the most useful finding in the dataset.

| Question | Sabha rubric | Baseline rubric | Why baseline won (per judge rationale) |
|---|---:|---:|---|
| `cio-01` (CIO, no deep skill) | 19 | 15 | Baseline *challenged the premise* — asked whether the $2,400 vendor bill was even legitimate before recommending migration. Sabha optimized the migration plan as-asked. |
| `cio-02` (CIO, no deep skill) | 18 | 10 | Baseline surfaced that the user's 4-month SOC 2 timeline was infeasible. Sabha "commits decisively but glosses over [that] fundamental constraint." |
| `ceo-03` (CEO, no deep skill) | 17 | 11 | Baseline went diagnostic-first; Sabha went structured-first. Pairwise judge: *"Reply B's meta-commentary and routing header add noise without operator value."* |

**Pattern:** Sabha consistently rewards form over substance. All three losses are where **reframing the question was more valuable than answering it as posed**. All three are no-deep-skill roles, and the deep skills *do* contain reframe-the-question patterns (see [`../skills/roles/cfo/worked-examples/01-seed-stage-runway.md`](../skills/roles/cfo/worked-examples/01-seed-stage-runway.md) — Step 3 is literally "Reframe the question").

**This is the clearest v1.6 roadmap signal in the data:**

- Add a reframe-discipline rule to [`../skills/sabha-router/SKILL.md`](../skills/sabha-router/SKILL.md) so it applies to *all* roles, not just deep-skilled ones.
- Rule shape: *"If the user's premise contains an unstated infeasibility OR the question would be better posed differently, challenge the premise* **before** *applying the protocol structure."*

---

## Top / bottom lift — where Sabha helps most and least

**Biggest lifts:**

- `caio-01` (+9, no deep skill) — model-selection question. Sabha forces specifics ("use Haiku 4.5 for the classifier, not Sonnet — 4× latency, 2pp accuracy cost") that baseline misses.
- `cio-02` (+8, no deep skill) — but still lost pairwise. Rubric loved the structure; operator-judge saw the substantive miss.
- `cmo-01` (+8, with deep skill) — positioning question. Deep CMO skill activated; JTBD framing visible in answer.

**Smallest lifts (still all positive):**

- `ceo-01` (+2) — cross-cutting CEO question. Both replies were decent; Sabha's structure added marginal value.
- `cio-01` (+4) — lost pairwise. Same pattern as above.
- `cxo-01` (+4) — retention question. Both replies converged on similar recommendations.

**Reading:** Sabha's rubric lift is most valuable on questions where baseline Claude is hedge-prone (CAIO model selection, CMO positioning). It's least valuable on questions where baseline already commits (some CEO synthesis questions).

---

## CAIO recommendations — what to do with this

| Priority | Move | Why |
|---|---|---|
| **1** | Build the **CIO deep skill** next | Highest pairwise-loss role; data points directly at it. Pattern: cio-01 + cio-02 baseline wins both in no-deep-skill CIO domain. |
| **2** | Add **reframe-the-question discipline** to [`../skills/sabha-router/SKILL.md`](../skills/sabha-router/SKILL.md) | Closes the gap surfaced by all 3 baseline wins. Charter-level rule; no per-role work needed. |
| **3** | **Tighten v2 rubric** | Decisiveness and tradeoff_named are saturated. Make 5/5 harder; differentiate top-tier Sabha replies. Add an explicit "challenged the premise / didn't" axis. |
| **4** | **Re-run the eval at v1.6.x** (after #1 and #2 ship) | Hypothesis: pairwise rises from 85% → 92-95% with reframe discipline + CIO deep skill. Falsifiable. |
| **5** | Add a **human-judge spot-check** on a random 5-question subset | LLM-as-judge bias is real; one human pass adds credibility. |

---

## Methodology caveats to disclose honestly

1. **n = 20.** Confidence intervals on per-axis means are wide. **Pairwise signal is more reliable than absolute scores.**
2. **Length_discipline = 1.6 for baseline is suspiciously harsh.** Possible judge bias on this axis specifically.
3. **Decisiveness and tradeoff_named are saturated** (16/20 and 15/20 Sabha replies at ceiling). Rubric needs tightening at the top end.
4. **Both candidates are Claude.** Results may not transfer to GPT/Gemini.
5. **Judge is also Claude (Opus, different class than candidate Sonnet, but same model family).** Some self-bias is inherent. Different model class reduces but doesn't eliminate.
6. **The three baseline wins are real findings**, not bugs. They expose a substantive gap (reframe discipline) that the deep skills partially close.

---

## Honest claims for launch copy

The strongest defensible claim, in three lengths:

**One sentence:**
> *Sabha replies preferred 17/20 pairwise (85%) over baseline with a +5.95 rubric improvement on a 20-point scale, judged by a different Claude model class (Opus on Sonnet). Three losses surfaced specific gaps now roadmapped for v1.6.*

**One paragraph:**
> *We ran a 20-question operator-style evaluation. Claude Sonnet 4.6 generated replies twice — once with no system prompt (baseline), once with the Sabha protocol as the system prompt. Claude Opus 4.7 judged each reply on five axes (decisiveness, tradeoff-named, concreteness, length discipline, routing) and picked a pairwise winner. Sabha replies were preferred 17/20 (85%), with +5.95 mean improvement on the rubric. The three losses were all on roles where Sabha hadn't yet built a deep skill — and they showed the same failure mode: Sabha applied formal structure when the question needed reframing. That gap is roadmapped for v1.6.*

**For HN, with the methodology caveats:**
> *Headline: 85% pairwise preference for Sabha across 20 operator questions, +5.95 rubric improvement. Caveats: n=20 (small), LLM-judged (Claude-on-Claude, different model class), the rubric is saturated on two of five axes (need v2). The three baseline wins are real signal, not noise — they expose a reframe-discipline gap now roadmapped. Raw data, judge rationales, methodology all in `evals/`. Reproducible: `pip install -r evals/requirements.txt && python evals/run_eval.py`.*

---

## Where to look in the repo

| File | What it has |
|---|---|
| `evals/results/2026-05-14.json` | Raw machine-readable: per-question scores, judge rationales, sabha+baseline replies in full |
| `evals/results/2026-05-14.md` | Same data rendered with sample replies inline |
| `evals/results/latest.md` | Alias for the most recent run |
| `evals/questions.yaml` | The 20-question set (operator-style decisions, role-tagged) |
| `evals/judge.py` | LLM-as-judge module — rubric, pairwise preference, retry logic |
| `evals/run_eval.py` | Harness — generation + scoring + checkpointing + `--resume` |
| `evals/README.md` | Methodology, how to run, limitations |
| **This file** | Interpretation of the most recent run |

To re-analyze a new run, regenerate the headline numbers with:

```bash
python3 -c "
import json
from statistics import mean
with open('evals/results/<run>.json') as f:
    data = json.load(f)
records = data['records']
print(f'n={len(records)}')
sabha = mean(r['scores']['sabha']['total'] for r in records)
base = mean(r['scores']['baseline']['total'] for r in records)
wins = sum(1 for r in records if r['pairwise']['winner']=='sabha')
print(f'Sabha total: {sabha:.2f}, baseline {base:.2f}, gap +{sabha-base:.2f}')
print(f'Pairwise: {wins}/{len(records)} ({100*wins/len(records):.1f}%)')
"
```

---

*This analysis follows the Sabha v1.4 grounding discipline: every number is cited to its source file. No claim above is unsourced. The dataset is `evals/results/2026-05-14.json`.*
