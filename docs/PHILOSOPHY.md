# Philosophy

Most AI replies are *option-shaped*. You ask "should I do X?" and get "well, here are five ways to think about it." That's exhausting when you're running something. You don't need a survey of possibilities — you need a recommendation, the tradeoff, and the next move.

Sabha forces five disciplines on every load-bearing reply.

## 1. A role

Real questions have real domains. "Should I move our database to a cheaper provider?" is a CIO question. "Should we hire a part-time bookkeeper or use Pilot?" is a CFO/CHRO question. Generic AI replies blur these — Sabha makes the model commit to a domain before opening its mouth. That commitment alone narrows the answer.

## 2. A recommendation

A doctor says "take this." A lawyer says "sign this." Executives say "do this." A board of advisors that only "presents options" is fired. Sabha makes the role *recommend*. The user can override — they always can — but the default output is a decision, not a menu.

## 3. A tradeoff

The fastest way to spot a bad recommendation is to make the recommender name what they're giving up. "Do X. You lose Y. Worth it because Z." If a role can't name the Y, the recommendation isn't ready.

## 4. Mode discipline

Two modes, and only two. *Ask* is a chat reply — quick, inline, no file. *Engage* is a document — filed, dated, kept. Most questions are ask-mode questions. Sabha defaults to ask, and only escalates to engage when the user signals it ("file this," "make it a goal") or when the stakes warrant it (dollars, time, risk).

This stops the dreaded "I asked a one-line question and got back a fifteen-page treatise."

## 5. Local memory — your Sakthi compounds

A council that forgets you between sessions is a *generic* council. Sabha is built around a memory MCP that runs on your machine — your **Sakthi** (Sanskrit/Tamil: *power*). Every decision, every person, every project compounds there. Three sessions in, your CFO role knows your runway. Ten sessions in, your CSO knows which bets you killed and why. A year in, your council has the institutional memory of a real C-suite — but only you can read it.

This is the difference between renting an opinion and building an asset.

---

## Why "Sabha," "Chanakya," "Sakthi," "Pramana"?

**Sabha** (सभा). Sanskrit for *assembly* or *council*. In the Mahabharata, the *Sabha Parva* describes the assembly hall where strategy gets debated and decisions get made. The metaphor is precise: you're not asking an oracle, you're convening a council. The council has roles. Each role has a domain and a voice. The council can disagree. The user — the king, the founder, the operator — makes the final call.

**Chanakya** (4th century BCE). The archetype the council embodies. Author of the *Arthashastra* — the original treatise on statecraft, economics, and strategy. The architect behind Chandragupta Maurya's rise. The world's first systematic strategic advisor. Sabha's voice is shaped by his disposition: decisive, tradeoff-aware, allergic to flattery, comfortable naming hard truths.

**Sakthi** (शक्ति). Sanskrit/Tamil for *power*. Not power-over, but power-of — the capacity built from accumulated experience, decisions, and the company you keep. The outcome of running a council over time. The memory layer is where your Sakthi lives.

**Pramana** (प्रमाण). Sanskrit for *means of valid knowledge* or *standard of evidence*. The epistemological doctrine in Nyaya and Mimamsa names a small list of admissible knowledge-sources: *pratyaksha* (perception), *anumana* (inference), *upamana* (comparison), *shabda* (testimony). The sibling research agent enforces a software version of that discipline — tiered sources (primary documents over reputable analysis over navigation aids over content mills), a mandatory contrarian-view pass, an inline citation for every factual claim, and a self-check on the citation graph before delivery. Where the council *decides*, Pramana *brings back what the council needs to decide on*, with the means of its validity marked. The naming is precise: pramana isn't "knowledge" — it's the *standard by which something is admitted as knowledge*. The tiers and contrarian search are that standard, encoded.

Together: **a Sabha (council) in the Chanakya tradition that builds your Sakthi (power) over time, with local memory — and reaches for Pramana (evidence-grounded research) when the council needs more than what it already knows.**

The protocol doesn't replace your judgment. It improves the inputs, remembers what you've already decided, and — when needed — fetches what it doesn't yet know with sources cited.

---

## What Sabha is not

- **Not a chain-of-thought hack.** It changes what the model *outputs*, not how it reasons internally.
- **Not domain expertise.** A CFO role doesn't give Claude actual CPA credentials. It gives Claude *a CFO's framing*. You still need real experts for tax filings, legal opinions, regulated decisions.
- **Not a personality skin.** The roles aren't characters. They're job functions. CIO doesn't have a backstory. CIO has a domain.
- **Not magic for trivia.** Sabha skips chit-chat and lookups. Asking "what year did X ship?" should not produce `Routing: CSO.` That would be ridiculous.

---

## When Sabha works best

- One-person companies and small teams where the user genuinely needs a "rest of the C-suite."
- Founders who think faster than they can hire.
- Operators who want decisions, not options.
- Anyone whose AI replies have gotten so hedged and balanced that they no longer help.

## When Sabha is overkill

- Pure coding tasks (use a coding-focused setup).
- Research and exploration where you genuinely want options.
- Teaching scenarios where you want the model to be expansive.

You can keep Sabha installed and just not invoke it — by default it only fires on substantive questions.
