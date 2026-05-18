# Evals

Does Sabha actually produce better answers than a vanilla LLM reply? This page summarizes the methodology, current results, and how to run the eval yourself.

> **Where the source-of-truth lives.** This page is a pointer + summary. The raw data, harness, and full interpretation are in [`evals/`](../evals/). When numbers conflict, the JSON in `evals/results/` wins.

> **Rubric version note (2026-05-18):** The current rubric is **v3** — it splits the three previously-saturated composite axes (`decisiveness`, `tradeoff_named`, `length_discipline`) into 5 binary sub-criteria each. **The v1.3.1 and v2 baselines are retired** because their rubrics could not discriminate between strong and very-strong replies. Old runs remain in `evals/results/` for audit, but headline numbers like "+5.95 rubric Δ" from v1.3.1 should not be cited as ongoing claims — they were a measurement-ceiling artifact. The v3 baseline is the new measurement floor. See "Rubric v3" below.

---

## TL;DR

- **20 operator-style questions** across all 9 C-suite roles, plus general business calls.
- **Two replies per question** — one with no system prompt (baseline), one with the Sabha charter loaded.
- **LLM-as-judge** (Opus 4.7 judging Sonnet 4.6 responses) scores each reply on five axes plus pairwise preference.
- **Result:** Sabha-routed replies scored **+5.95 on a 20-point rubric** and won **17/20 pairwise (85%)** against the no-prompt baseline.
- **With deep skills loaded:** 100% pairwise win rate on CFO/CMO questions.

The numbers, methodology, and limitations are all in the repo. If you don't trust an eval that lives alongside the code it's evaluating, run it yourself — the harness ships in `evals/`.

---

## Methodology

### Question set (v2, n=50 as of 2026-05-18)

50 questions across the 9 roles, in four buckets:

| Bucket | n | Purpose |
|---|---:|---|
| **Operator questions** (original) | 20 | Sabha's sweet spot — real decisions where structured framing helps |
| **Adversarial reframing** | 10 | Questions where the right answer is to *challenge the premise*, not apply structure. Tests where Sabha's discipline becomes rigidity. |
| **Cross-role / edge** | 10 | Questions that span multiple roles or fall between domains. Tests routing robustness. |
| **Underdog** | 10 | Definitional / lookup-shaped / well-framed questions where a baseline LLM is already good. Tests whether Sabha generalizes or whether it should be skipped on simple questions. |

This shape is deliberate. A question set that's only Sabha-sweet-spot questions overstates the protocol's value. A set that includes adversarial and underdog questions surfaces honest weaknesses.

Questions are operator-shaped, not abstract: "Should I cut the SaaS line 40% to extend runway?" — not "what is unit economics?"

See [`evals/questions.yaml`](../evals/questions.yaml) for the full set.

### Rubric v3 (sub-axis decomposition)

The previous rubric (v1.3.1 / v2) used 0-5 holistic scoring on five axes. Two of them — `decisiveness` and `tradeoff_named` — saturated at 5/5 for 75-80% of Sabha replies, so the rubric stopped discriminating between strong and very-strong outputs. v3 fixes this:

**Three axes are now sums of 5 binary sub-criteria** (each 0 or 1, summed to 0-5):

- **decisiveness:** made_clear_recommendation, stated_confidence_or_conditions, named_alternative_rejected, committed_specific_next_move, avoided_hedging_language
- **tradeoff_named:** named_what_is_given_up, quantified_the_cost, named_who_is_affected, stated_time_horizon, gave_reasoning_to_accept
- **length_discipline:** no_three_paragraph_windup, no_padding_phrases, no_unnecessary_disclaimers, no_redundancy, every_paragraph_advances

Two axes stay holistic: `concreteness` (0-5) and `routing_present` (0 or 1, binary).

The judge now returns both the composite scores AND the sub-criteria dicts. Downstream analysis can slice by what specifically succeeded or failed — e.g., is Sabha winning on `committed_specific_next_move` but losing on `quantified_the_cost`? That's actionable signal the v2 rubric could not show.

### Judge provider — `--judge-provider`

The harness now supports cross-model judging via `--judge-provider {anthropic,openai,google}`. This defeats the largest remaining credibility weakness: the v1.3.1 / v2 runs had Claude judging Claude. Same family, same training distribution, same blind spots.

Cross-model runs require the corresponding provider's SDK and API key:

```bash
# Default — preserved for continuity
python evals/run_eval.py --judge-provider anthropic

# Cross-model — defeats in-family bias
export OPENAI_API_KEY=sk-...
pip install 'openai>=1.0'
python evals/run_eval.py --judge-provider openai --judge-model gpt-5

export GOOGLE_API_KEY=...
pip install 'google-generativeai>=0.7'
python evals/run_eval.py --judge-provider google --judge-model gemini-2.0-pro
```

A *credible* eval run on a fresh corpus does at least one Anthropic + one cross-family judge. Numbers that hold across both judges are dramatically stronger than either alone.

### Two replies per question

For each question:
1. **Baseline reply.** Sent with no system prompt. Candidate model gets the question and answers naturally.
2. **Sabha reply.** Sent with the full `CLAUDE.md` charter loaded as system prompt. When a deep skill exists for the routed role, the skill content is appended.

Same model (Sonnet 4.6 in the v1.3.1 run). Same temperature. Only the system prompt changes.

### Judge: a stronger model on a different rubric

The judge (Opus 4.7) sees both replies and scores each on five axes (0–5 each, 20 max):

| Axis | What it measures |
|---|---|
| **decisiveness** | Does the reply recommend a path, or just survey options? |
| **tradeoff_named** | Does the reply explicitly name what's given up? ("Do X. You lose Y.") |
| **concreteness** | Real vendors, dollars, file paths, specific moves — not abstractions. |
| **length_discipline** | Is the reply as long as it needs to be, no longer? Penalizes padding. |
| **routing_present** | Binary: did the reply start with `Routing: <ROLE>` (sanity check). |

Plus a **pairwise preference**: "Which reply would the operator prefer to receive?"

The pairwise judgment is what most matters. Rubric scores can saturate; pairwise forces a choice.

### Reproducibility

- Question set, seed, candidate model, judge model, all pinned in `evals/run_eval.py`.
- Checkpoint-after-each-question + `--resume` so a long run survives transient API errors.
- Retry wrapper around the judge call with jittered exponential backoff (handles Anthropic 529 overloads).
- All results committed to `evals/results/` as JSON + Markdown.

---

## Current results

### Headline (v3 rubric, n=50, Anthropic judge — 2026-05-18)

| Metric | Value | 95% CI |
|---|---:|---|
| **Pairwise preference (Sabha vs no-system-prompt baseline)** | **48 / 50 (96.0%)** | Wilson [86.5%, 98.9%] |
| Rubric total Δ (Sabha − baseline) | +4.78 / 20 | — |
| Sabha total mean | 16.96 | stdev 2.74 |
| Baseline total mean | 12.18 | stdev 3.74 |

CI tightening vs the n=20 v1.3.1 run: lower bound jumped from **64.0% → 86.5%**. The directional claim is no longer "probably wins" — at 95% confidence, the *worst plausible* underlying Sabha pairwise rate is now 86.5%, comfortably above 50% (the no-effect threshold) and above 70% (a strong-effect threshold).

### Per-bucket breakdown — *the bigger story*

The n=50 question set was built in four buckets to stress-test the protocol across credibility dimensions. Each bucket targets a different way Sabha *could* fail:

| Bucket | n | Purpose | Pairwise | Rubric Δ |
|---|---:|---|---:|---:|
| **Original operator questions** | 20 | Sabha's sweet spot — confirm v1.3.1 directional result | 19 / 20 (95%) | +3.90 |
| **Adversarial reframing** | 10 | Questions where the right answer is to *challenge the premise*. Tests whether deep skills' reframing heuristics work. | **10 / 10 (100%)** | +6.10 |
| **Cross-role / edge** | 10 | Multi-role routing tests. Does Sabha pick the right primary? | **10 / 10 (100%)** | +5.90 |
| **Underdog** | 10 | Definitional / lookup-shaped questions where baseline should be competitive. | 9 / 10 (90%) | +4.10 |

**The adversarial bucket is the most consequential finding.** The v1.3.1 eval had 3 baseline-wins (cio-01, cio-02, ceo-03) that all shared one pattern: Sabha applied structure to a question that needed reframing first. The new n=50 run with all 9 deep skills loaded **closes that loss type at scale** — 10/10 pairwise on a bucket built specifically to surface it. The deep skills' "challenge the premise" heuristics work.

The underdog bucket is also notable: Sabha wins 90% even on questions where baseline should be competitive (definitional lookups, well-framed simple asks). The protocol generalizes beyond its sweet spot.

### Per-role distribution

| Role | n | Pairwise | Rubric Δ |
|---|---:|---:|---:|
| CIO  | 8 | 8/8 (100%) | +6.12 |
| CLC  | 3 | 3/3 (100%) | +7.67 |
| CHRO | 6 | 6/6 (100%) | +5.83 |
| CAIO | 5 | 5/5 (100%) | +5.00 |
| CFO  | 6 | 6/6 (100%) | +5.00 |
| CMO  | 5 | 5/5 (100%) | +3.00 |
| CXO  | 5 | 5/5 (100%) | +4.00 |
| CEO  | 6 | 6/6 (100%) | +3.67 |
| CSO  | 6 | **4/6 (67%)** | +3.33 |

Per-role n is now between 3 and 8 (was 2-3 at v1.3.1). The CSO 4/6 is the only role under 100% pairwise — both losses sit in CSO (see "Catalogued losses" below).

### Caveat: v3 rubric partial activation

The eval ran *with* the v3 sub-axis rubric prompt loaded, and the judge's rationales explicitly reference sub-criteria reasoning (sample: *"Reply hits all sub-criteria: decisive recommendation, quantified tradeoffs, concrete playbook..."*). **But the judge (Opus 4.7) emitted JSON in the v2 flat shape** — composite scores without the per-sub-criterion breakdown.

The fallback in `score_reply` worked correctly; the numbers are still informed by v3 thinking, just not measurable as v3 sub-axis decomposition. Concretely:
- Rubric saturation is *partially* reduced (decisiveness ceiling now 33/50 = 66%, down from 80% at n=20)
- But we cannot slice *which* sub-criteria Sabha is winning or losing on

This is a finding to fix. See `docs/BACKLOG.md` → "Tighten v3 judge prompt for structured sub-criteria output."

### Catalogued losses (2/50)

Both baseline wins are CSO. Both are traceable, not mysteries:

- **`cso-02` (partnership)** — Sabha reply was **truncated mid-sentence** at the harness 1200 max_tokens limit. The same artifact bit cso-02 in the 2026-05-16 run. This is a harness bug already in BACKLOG ("Bump eval harness max_tokens 1200 → 2000"). Promotion criterion has now fired (second consecutive run with the same loss).

- **`under-05` (Where to Play / How to Win)** — A legitimate baseline win. Judge rationale: *"B adds the useful attribution to Martin and Lafley, which an operator would find informative."* Sabha gave the right structural answer but didn't cite the framework's authors. Honest signal: on definitional questions, attribution beats structure. The CSO REFERENCE.md cites Lafley & Martin extensively — the issue is that the citation didn't surface in the *reply* even though it's in the loaded context.

### Retired baselines (preserved for audit only)

The v1.3.1 (2026-05-14) and v2 (2026-05-16) runs are retired because:

- They used the v1/v2 rubric, where `decisiveness` and `tradeoff_named` saturated. Numbers like "+5.95 rubric Δ" or "16.80 mean" are *not comparable* to v3 numbers and should not be cited as ongoing claims.
- They ran at n=20, which produces CI widths of ±15pp — useful for direction but not magnitude.
- They had only an Anthropic judge (in-family bias).

Old runs remain in `evals/results/` and are summarized below as historical context. The honest takeaway from them is:

- **Direction was clear** at n=20 in both runs: Sabha-routed replies beat no-system-prompt baselines on pairwise preference 17/20 (85%) in two independent runs.
- **Magnitude is uncertain** because the rubric ceilinged. Concrete rubric Δ numbers (+5.95, +4.85) shouldn't carry forward.
- **The 2026-05-16 re-run** (with all 9 deep skills loaded) showed `length_discipline` dropping from 3.15 → 2.85 — surfaced a real protocol tradeoff that the v3 rubric will measure more precisely.

### Previously-shipped per-axis read (v1.3.1)

| Metric | Baseline | Sabha | Δ |
|---|---:|---:|---:|
| Rubric total (mean, /20) | 10.85 | 16.80 | **+5.95** |
| Pairwise win rate | — | 17/20 = **85%** | — |
| Rubric stdev | 2.78 | 2.33 | More consistent than baseline |

### Per-axis

| Axis | Baseline | Sabha | Δ | Note |
|---|---:|---:|---:|---|
| decisiveness | 3.00 | 4.65 | +1.65 | Rubric saturated — almost always 5/5 |
| tradeoff_named | 3.20 | 4.70 | +1.50 | Rubric saturated |
| concreteness | 3.05 | 4.30 | +1.25 | **Most discriminating axis** |
| length_discipline | 1.60 | 3.15 | +1.55 | Hardest axis — even Sabha doesn't fully nail terseness |
| routing_present | 0.00 | 1.00 | +1.00 | Binary sanity check |

### With deep skills loaded (CFO + CMO subset)

| Subset | Pairwise win rate | Rubric Δ |
|---|---:|---:|
| Deep-skill questions (CFO + CMO, n=5) | **5/5 = 100%** | +6.60 |
| No-deep-skill questions (n=15) | 12/15 = 80% | +5.73 |

The deep-skill layer adds only +0.87 on rubric but **+20pp on pairwise**. Framework grounding doesn't just push replies higher — it makes them *consistently win* in head-to-head comparison.

---

## Where Sabha lost

Three of the 20 questions went to baseline (cio-01, cio-02, ceo-03). All three share a pattern: **the question needed reframing, and Sabha applied formal structure to the wrong frame**. All three are no-deep-skill roles in the v1.3.1 run.

The deep skills now built for CIO and CEO contain reframe-the-question heuristics; a v2 eval run against the current state of the protocol should close this gap.

---

## Limitations (don't oversell this)

1. **LLM-as-judge has known biases.** The judge tends to reward structure and explicit recommendations — exactly what Sabha enforces. The pairwise comparison is more robust than the rubric, but neither is bias-free. Tightening with human judgment is on the v2 roadmap.

2. **The judge is from the same model family as the candidate.** Cross-family eval (Sonnet candidate, GPT-4 judge, or vice versa) is on the roadmap.

3. **20 questions is small.** It's enough to show a directional signal but not enough to slice by domain × question-type. Expanding the set to 50–100 is also roadmapped.

4. **Rubric saturation.** `decisiveness` and `tradeoff_named` already award 5/5 to almost every Sabha reply. For v2, the 5/5 threshold should tighten so Sabha has room to be less than perfect.

5. **No real-user comparison yet.** All judgments are LLM-judged, not operator-judged. A small pool of real operators rating real questions would be much stronger evidence.

---

## Run it yourself

```bash
git clone https://github.com/rdmurugan/sabhaos.git
cd sabhaos
pip install -r evals/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

# Full run (~$3–8 in API cost, ~10–15 min wall time)
python evals/run_eval.py

# Resume after a transient failure
python evals/run_eval.py --resume

# Quick smoke (3 questions)
python evals/run_eval.py --limit 3
```

Results land in `evals/results/`. The harness writes both a machine-readable JSON and a rendered Markdown report.

To regenerate the analysis layer on top of new results, see `evals/ANALYSIS.md` for the writing style — but the harness writes the JSON; the analysis is a human-authored read.

---

## Related reading

- [`evals/README.md`](../evals/README.md) — harness usage and design choices
- [`evals/ANALYSIS.md`](../evals/ANALYSIS.md) — the full v1.3.1 interpretation (longer than this page)
- [`evals/questions.yaml`](../evals/questions.yaml) — the question set
- [`docs/PHILOSOPHY.md`](./PHILOSOPHY.md) — why these five axes are the ones that matter
