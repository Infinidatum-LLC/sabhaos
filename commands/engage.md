---
description: Switch to engage mode — produce a document-grade deliverable (.docx for formal exec reports, .md for everything else).
---

For this turn, operate in **engage mode**:

- Produce a real file. Use `.docx` for formal exec reports (board memos, investor updates, vendor proposals). Use `.md` for everything else.
- Still route to a role at the top of both the chat reply and the document.
- Document is for the record — include date, role, decision, tradeoffs, and next steps.
- Keep the chat reply itself brief: announce the file, link it, give a one-line summary.
- After the file is produced, call the [`sakthi-diary`](../skills/modes/sakthi-diary/SKILL.md) skill with `mode: engage` so the decision compounds into Sakthi. If no memory MCP is connected, emit the SABHA_DIARY v1 yaml block at the end of the reply so the user can copy/paste.

User's brief follows:
$ARGUMENTS
