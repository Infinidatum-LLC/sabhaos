---
description: Invoke deliberation mode — two or three roles argue their positions, CEO synthesizes, transcript and decision auto-file to Sakthi.
---

For this turn, operate in **deliberate mode** per the [`deliberate`](skills/modes/deliberate/SKILL.md) skill.

- Pick 2 roles (3 only if a regulatory/HR/legal angle is non-trivial). Synthesizer is always CEO.
- Run the protocol exactly: memory gate → openings → rebuttals → CEO synthesis.
- Each role gets one paragraph per round. Hard length cap: ~900 words for 2 roles, ~1,300 for 3.
- On completion, call the [`sakthi-diary`](skills/modes/sakthi-diary/SKILL.md) skill with `mode: deliberate` — deliberation is engage-mode by definition.
- If `$ARGUMENTS` starts with `--deep`, dispatch each role as a separate `claude` sub-agent (advanced — costs 2-3× tokens, use only when role purity is worth it).

Question for deliberation:
$ARGUMENTS
