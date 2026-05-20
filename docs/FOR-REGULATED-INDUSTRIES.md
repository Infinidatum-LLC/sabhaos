# Sabha + Sakthi for regulated industries

For operators building in health, legal, finance, defense, government-adjacent, or any space where institutional memory **cannot** live on someone else's server.

This page is for the founder, the compliance officer, the IT lead, and the security reviewer who needs to evaluate whether Sabha + Sakthi can be approved for use with sensitive data. It's not a marketing page; it's a posture statement with the receipts.

> **Plain English, up front.** Sabha is an open-source AI protocol; Sakthi is its optional local memory backend. The protocol layer makes routing/voice decisions. The memory layer stores your accumulated knowledge **on your machine**, in a database you control, in files you can read with `ls`. No telemetry. No phone-home. No cloud sync. Verifiable in the source.

---

## Who this is for

If any of these apply, Sakthi (the local-first memory backend) is the right choice — Claude Memory is structurally not viable for you:

- **Healthcare** — patient data, clinical workflows, anything that touches PHI.
- **Legal / IP-sensitive** — client matter, deal flow, M&A in flight, patent strategy.
- **Financial advisory** — family offices, boutique wealth, hedge fund research, private credit.
- **Defense / government-adjacent** — contracts with ITAR, EAR, FedRAMP, or CMMC reach; export-controlled tech.
- **Regulated SaaS** — fintech, healthtech, edtech under FERPA, EU AI Act high-risk classification.
- **Anyone with a board obligation** to not put accumulated institutional knowledge on a third-party cloud.

Common thread: you may freely use a hosted LLM for *the question in front of you*, but the *accumulated memory* of every decision your council has made is a different asset class. That asset belongs on your machine, under your access controls, auditable by you.

---

## What Sabha + Sakthi gives you

1. **Local-first by design.** The memory palace lives at `~/sakthi` (or wherever you point `$PALACE`). It is a directory on your disk. No replication, no sync, no cloud component.
2. **No telemetry.** The Sabha protocol layer does not make outbound calls. The Sakthi MCP server does not phone home. Verifiable in the source — `grep -r "http" mempalace/` returns only docstrings and URL references in comments.
3. **No auto-update.** Plugin install is explicit. You decide when to upgrade. Pin the version that passed your review; don't auto-pull.
4. **MIT-licensed end to end.** Both Sabha OS and Sakthi Graph are MIT. You can fork, modify, sublicense, redistribute. No usage analytics. No EULA gotchas.
5. **Auditable storage.** The palace is a ChromaDB database (SQLite + on-disk vector files). You can connect to it with standard tools, dump it, back it up, encrypt it at rest.
6. **Structured retrieval.** Drawers are scoped by `wing` (role) and `room` (topic). Queries can be deterministic, not just semantic — *"all CFO decisions from Q1"* is one tool call.
7. **Portable.** Your Sakthi is your data. If you change LLM providers, switch hosts, or shut Sabha down entirely, your knowledge graph remains a directory of files you own.
8. **Auditable decision trail (v2.2.0+).** Every engage-mode and deliberate-mode answer auto-writes a `SABHA_DIARY v1` entry with mandatory `sources` field. Deliberate mode additionally records the full multi-role transcript (CFO opening, CSO rebuttal, CEO synthesis) as a `transcript` field in the same entry. For regulated industries this is a substantive artifact: *"why did the team decide X on date Y"* has a structured, queryable, locally-stored answer — not a Slack archive search. The diary contract is defined once in [`skills/modes/sakthi-diary/SKILL.md`](../skills/modes/sakthi-diary/SKILL.md) and is backend-agnostic; if your auditors want it exported, the yaml block is human-readable and tool-friendly.

---

## Threat model

| Threat | Posture |
|---|---|
| Cloud LLM provider sees the question and reply | **Acknowledged, out of scope.** This is the cost of using a hosted LLM. Choose your provider's data-use agreement accordingly (Anthropic offers zero-data-retention tiers for enterprise). For air-gapped operation, pair Sabha with a locally-run model. |
| Cloud LLM provider sees your accumulated knowledge | **Mitigated.** Sakthi lives on your machine; nothing is uploaded. Only the *snippets retrieved per query* enter the LLM context — the LLM does not see your full memory. |
| A future Sabha update exfiltrates Sakthi data | **Mitigated by open source + pinning.** Audit the diff before upgrading; pin the known-good version. The plugin install path does not auto-update. |
| Sakthi corpus contains data you shouldn't compound | **User-controlled.** Don't ingest it. Or `sakthi_delete_drawer` after the fact. Or use a separate palace (`sakthi init --palace ~/sealed-palace`) for sensitive material. |
| Teammate's machine contains different Sakthi state | **Expected and acceptable.** Each person's Sakthi is their own. No central truth. Use git or your team's existing knowledge system for shared material. |
| Filesystem-level data exposure | **Your responsibility.** Sakthi is a directory. Encrypt your disk (FileVault, LUKS, BitLocker). Apply your org's existing endpoint-protection posture. |
| Memory poisoning via malicious corpus ingest | **Partially mitigated.** Graphify's audit trail (EXTRACTED / INFERRED / AMBIGUOUS edges) flags inferred content. `sakthi sittham` is idempotent and previewable (`--dry-run`). For untrusted corpora, use a separate palace. |
| LLM-extraction step in `/graphify` calls a cloud LLM | **User-controlled.** Graphify can use the user's API key with a cloud LLM, or run with a local model (Ollama, vLLM). For sensitive corpora, configure graphify with a local model. |

**What Sabha + Sakthi explicitly do not do:**
- No telemetry. (Verifiable.)
- No auto-update.
- No call-home in the protocol layer.
- No outbound network egress from the MCP server.
- No storage outside the user-specified palace path.

---

## Compliance framing (operator-grade — NOT legal advice)

The CLC role's discipline applies here too: *operator framing, not legal advice*. For your actual compliance program, you need licensed counsel in your jurisdiction. What follows is the framing for that conversation.

### HIPAA (US health)

- **Sabha protocol layer:** no PHI handling; it routes and structures. Not a covered system.
- **Sakthi:** lives on your machine. If your machine is BAA-covered infrastructure, Sakthi inherits that posture. The palace path can be placed inside an existing encrypted, audited storage location.
- **Cloud LLM:** the LLM provider's BAA (or absence of one) is the determining factor for any PHI in queries. Anthropic offers HIPAA-eligible tiers for enterprise; verify with your account team. **Do not put PHI in a Sabha query without a BAA in place.**
- **Sittham:** corpus ingest creates drawers from extracted content. If the corpus contains PHI, the drawers contain PHI. Treat them with the same controls.

### GDPR / UK GDPR / CCPA / similar privacy regimes

- **Sabha + Sakthi:** the data is on the user's machine; the user is the controller. The user decides what gets stored, what gets deleted, what gets exported. `sakthi_delete_drawer` provides right-to-erasure on a per-drawer basis. `~/sakthi` can be wholesale exported as a tarball for data portability.
- **The LLM provider** is a processor for the queries that go to it. Honor your DPA with the provider.
- **Mixed-controller scenarios:** if you're the controller for client X's data and you ingest it via Sittham, your existing DPA with X governs. The fact that Sakthi is local doesn't change controllership; it changes infrastructure.

### EU AI Act

- Sabha is a general-purpose decision-support protocol; not a high-risk system on its own.
- If you deploy Sabha *into* a high-risk system (hiring decisions, credit scoring, healthcare diagnosis), the high-risk obligations attach to your system, not to Sabha-the-library.
- The CLC role's deep skill includes EU AI Act framing for operators building AI products — use it as a starting point, not a final answer.

### SOC 2 (vendor-evaluation framing)

If your buyer asks you for a SOC 2 report covering your use of Sabha:
- The protocol layer is a markdown file (CLAUDE.md). There's no SOC 2 boundary for a markdown file.
- The Sakthi MCP server runs on the user's endpoint. Endpoint controls (your existing posture: MDM, EDR, disk encryption) cover it.
- The LLM provider is a subprocessor. Use their SOC 2 report.
- Your SOC 2 narrative reads: *"We use the Sabha OS protocol (open source, MIT) with the Sakthi Graph local memory backend (MIT, runs on employee endpoints under our existing endpoint controls). All LLM calls go to [Anthropic / your vendor] under [their data-use agreement]."*

### ITAR / EAR / export-controlled

- Local Sakthi is helpful here: the *accumulated knowledge* doesn't leave the controlled environment.
- The LLM step is the question: cloud LLMs are problematic for export-controlled material. The mitigations are (a) air-gap with a local model, (b) use an FedRAMP/IL-classified provider if your data permits, or (c) keep the controlled material out of LLM queries and use Sabha purely on derived/unclassified content.
- This is exactly the kind of conversation you have with a licensed export-control attorney, not with a doc page.

---

## Deployment patterns by industry

### Solo founder, healthcare-adjacent startup

```
~/sakthi               ← all institutional memory
                         (encrypted disk, BitLocker/FileVault)
Sabha CLAUDE.md        ← council protocol, public knowledge
Cloud LLM              ← under your BAA / DPA / contractual posture
                         do not query PHI without a BAA
```

You write decisions, you write diary entries, your council learns. Patient data stays in your EHR; you reference *types* of patient situations in Sakthi without identifiers.

### Family office / boutique advisory

```
Sakthi palace per client     ← deal flow segregated by client
                               (sakthi init --palace ~/sakthi-clients/<id>)
Sabha CLAUDE.md              ← shared protocol
Engage-mode memos            ← filed locally; can be exported to your DMS
```

Each client gets a sealed palace. Cross-client contamination is structurally prevented. Memos can be reviewed by partners before filing to the document management system.

### Defense / government contractor

```
Air-gapped workstation       ← local LLM (Ollama, vLLM with Llama-3 or similar)
Sakthi palace                ← on the air-gapped machine
Sabha CLAUDE.md              ← protocol
Sittham                      ← optional; runs purely on local files
```

No cloud LLM. No data leaves the workstation. The Sabha protocol-as-text (CLAUDE.md) can be used as a system prompt with any model that accepts one — Claude is the primary tested target; a local Llama or similar can serve the air-gapped use case, though cross-model eval data is not yet published. The memory layer (Sakthi) is fully MCP-based and works with any MCP-capable LLM.

### Regulated SaaS company (fintech / healthtech / edtech)

```
Per-developer Sakthi         ← engineer's own council memory
                               (own laptop; own posture)
Sabha CLAUDE.md              ← shared via repo
Production data              ← stays in production systems; not in Sakthi
                               (Sakthi gets the decisions, not the data)
```

The principle: Sakthi stores the *meta-knowledge* about decisions (which vendor we chose, why we cut feature X, what the customer interview said), not the *operational data* of the regulated system itself.

---

## What we will not pretend

A few things would be marketing-comfortable to claim but are not honest:

- **"Sabha is HIPAA-compliant."** No software is HIPAA-compliant in a vacuum. Compliance is a property of your deployment, your BAAs, your endpoint controls, and your operational practice. Sabha + Sakthi can be a piece of a HIPAA-compliant workflow. It cannot be one on its own.
- **"Local-first means safe."** Local-first means *the cloud-provider attack surface is removed*. The endpoint attack surface is now yours. You still need disk encryption, endpoint protection, and your existing posture.
- **"You don't need a lawyer."** You do. For real compliance work in a regulated industry, you need licensed counsel in your jurisdiction. The CLC deep skill is operator framing, not legal advice — that boundary is explicit in every CLC reply.

---

## How to evaluate this for your org

A reasonable evaluation path:

1. **Read [`PRIVACY.md`](../PRIVACY.md)** — the no-data-collection disclosure.
2. **Read [`docs/ARCHITECTURE.md`](./ARCHITECTURE.md) § Threat Model** — the threat-by-mitigation table.
3. **Audit the source.** Both repos are MIT and small enough to read:
   - [github.com/rdmurugan/sabhaos](https://github.com/rdmurugan/sabhaos) — the protocol (mostly markdown).
   - [github.com/rdmurugan/sakthi-graph](https://github.com/rdmurugan/sakthi-graph) — the memory layer (Python; the relevant module is `mempalace/`).
4. **Run it isolated.** `sakthi init --sabha ~/eval-palace` on a test machine. Confirm no network calls (`tcpdump`, `lsof`).
5. **Pin a version.** Once approved, pin the plugin version and the `sakthi-graph` package version. Re-audit on upgrade.
6. **Document the deployment in your compliance program.** Use the SOC 2 narrative template above as a starting point; adapt for your auditor's framework.
7. **Talk to your counsel.** Specifically for HIPAA, EU AI Act, ITAR, sector-regulated workflows. The CLC framing in this doc is a starting point, not a substitute.

---

## Getting help

- **General questions:** open an issue at [github.com/rdmurugan/sabhaos/issues](https://github.com/rdmurugan/sabhaos/issues).
- **Security questions:** see [`SECURITY.md`](../SECURITY.md) if present; otherwise file a private issue.
- **Compliance reviews:** Sabha is MIT and audit-friendly. Your counsel and your auditor can examine the source directly — there's no NDA gate.

---

## The honest pitch

Most users don't need this page. They install Sabha, get the routing discipline, and use Claude Memory or no memory at all. That's fine.

If you're in the group that *does* need this page — because your work touches data that legally or contractually cannot live on a third-party cloud — Sabha + Sakthi gives you the AI council framing *and* the local-first memory posture, without forcing you to build either from scratch.

The price you pay: 5 commands of setup instead of zero. Endpoint controls you already have. A documented evaluation.

The benefit: an institutional memory of every decision your council has made, on your machine, MIT-licensed, auditable, MCP-based (so portable across MCP-capable LLMs at the storage layer), and structurally aligned with the compliance regime you already live under.

Nothing about that is magic. It's just a reasonable architecture for the operators who need it.
