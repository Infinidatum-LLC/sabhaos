# Chanakya activation eval — 2026-05-17 (grader v2)

- Candidate model: `claude-sonnet-4-6`
- Question set: 7 (4 invoke / 3 control)
- Corpus size: 76 verses

## Headline

- **Activation** (invoke + skill → exactly 1 in-corpus verse): **4/4 (100%)**
- **Discipline with skill loaded** (no invoke → no verse): **3/3 (100%)**
- **Attribution accuracy** — *new in v2 grader.* When the model is asked for Chanakya in plain English and produces a verse:
  - Without the skill loaded (baseline, training-data only):   0/4 verses in-corpus (0%)
  - With the skill loaded:   4/4 verses in-corpus (100%)

## Per-question results

| ID | Role | Invoke? | sabha verses | sabha attribution | sabha+chanakya verses | activation | discipline |
|---|---|---|---|---|---|---|---|
| chanakya-01 | CSO | YES | 6.2 | hallucinated | 10.16 | ✓ | — |
| chanakya-02 | CFO | YES | 1.6 | hallucinated | 5.12 | ✓ | — |
| chanakya-03 | CHRO | YES | 1.19 | hallucinated | 9.24 | ✓ | — |
| chanakya-04 | CSO | no | — | — | — | — | ✓ |
| chanakya-05 | CFO | no | — | — | — | — | ✓ |
| chanakya-06 | CHRO | no | — | — | — | — | ✓ |
| chanakya-07 | CIO | YES | 10.7 | hallucinated | 10.4 | ✓ | — |

**Reading the attribution column:** for the `sabha` condition (no skill loaded), the model produces Chanakya verses from training-data knowledge when explicitly asked. The attribution column flags whether those cited verse numbers exist in our curated 76-verse corpus. Hallucinated = the cited number isn't in the corpus, so either the model invented a plausible-looking number, or it's a real verse outside our curated set.

