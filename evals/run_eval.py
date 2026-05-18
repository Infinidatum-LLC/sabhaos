"""Sabha OS eval harness.

Runs the question set in evals/questions.yaml twice — once with no system
prompt (baseline) and once with CLAUDE.md as the system prompt (sabha) — and
judges both with an LLM-as-judge. Writes JSON + Markdown results to
evals/results/.

Usage:
    pip install -r evals/requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python evals/run_eval.py
    python evals/run_eval.py --candidate-model claude-sonnet-4-6
    python evals/run_eval.py --judge-model claude-opus-4-7
    python evals/run_eval.py --limit 5    # smoke test
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Optional

import yaml
from anthropic import Anthropic

# Allow running as a script regardless of CWD.
sys.path.insert(0, str(Path(__file__).parent))
from judge import (  # noqa: E402
    JudgeScore,
    PairwiseResult,
    pairwise_preference,
    score_reply,
    with_retry,
)


REPO_ROOT = Path(__file__).parent.parent
QUESTIONS_PATH = REPO_ROOT / "evals" / "questions.yaml"
CLAUDE_MD_PATH = REPO_ROOT / "CLAUDE.md"
RESULTS_DIR = REPO_ROOT / "evals" / "results"

DEFAULT_CANDIDATE_MODEL = "claude-sonnet-4-6"
DEFAULT_JUDGE_MODEL = "claude-opus-4-7"

CONDITIONS = ("baseline", "sabha")


def load_questions(limit: Optional[int] = None) -> list[dict]:
    with QUESTIONS_PATH.open() as f:
        raw = yaml.safe_load(f)
    qs = raw["questions"]
    return qs[:limit] if limit else qs


def load_sabha_system_prompt() -> str:
    return CLAUDE_MD_PATH.read_text()


ROLES_DIR = REPO_ROOT / "skills" / "roles"
# Files from a deep role skill that should be loaded into context to simulate
# the skill having activated. SKILL.md tells the model HOW to use the deep
# content; REFERENCE.md and heuristics.md ARE the deep content. Templates,
# playbooks, and worked examples are referenced by name and don't need to be
# pre-loaded.
_DEEP_SKILL_FILES = ("SKILL.md", "REFERENCE.md", "heuristics.md")


def load_deep_skill_for_role(role: Optional[str]) -> str:
    """Return concatenated deep-skill content for a role, or '' if no deep skill exists.

    In Claude Code, deep role skills activate via the skill router. The eval
    harness uses the raw API, so we simulate activation by appending the deep
    skill's core files (SKILL + REFERENCE + heuristics) to the system prompt
    for the matching role. This makes the eval test what users actually
    experience with sabha-os installed, not just the bare CLAUDE.md.
    """
    if not role:
        return ""
    role_dir = ROLES_DIR / role.lower()
    if not role_dir.exists():
        return ""
    parts: list[str] = [f"\n\n---\n# DEEP SKILL: {role.upper()}\n---\n"]
    for fname in _DEEP_SKILL_FILES:
        path = role_dir / fname
        if path.exists():
            parts.append(f"\n\n## {fname}\n\n{path.read_text()}")
    return "".join(parts) if len(parts) > 1 else ""


def generate_reply(
    candidate_client,
    model: str,
    question: str,
    condition: str,
    sabha_system: str,
    role: Optional[str] = None,
) -> str:
    """Run the candidate model under the given condition (with retries on transient errors).

    When `condition == "sabha"` and the question has a tagged role with a
    matching deep skill on disk, the deep skill's content is appended to the
    system prompt to simulate skill activation in Claude Code.

    The candidate is always Anthropic-shaped — the Sabha protocol is currently
    tested against Claude as the candidate model. The cross-model knob is on
    the *judge* (see `--judge-provider`), not the candidate.
    """
    kwargs = {
        "model": model,
        "max_tokens": 1200,
        "messages": [{"role": "user", "content": question}],
    }
    if condition == "sabha":
        kwargs["system"] = sabha_system + load_deep_skill_for_role(role)
    response = with_retry(
        lambda: candidate_client.messages.create(**kwargs),
        label=f"gen:{condition}",
    )
    return response.content[0].text


def run_question(
    candidate_client,
    judge_client,
    candidate_model: str,
    judge_model: str,
    sabha_system: str,
    question: dict,
    seed: int,
) -> dict:
    """Generate both replies, score both, run pairwise judge. Return per-question record."""
    qid = question["id"]
    prompt = question["prompt"]
    print(f"  [{qid}] generating...", flush=True)

    replies: dict[str, str] = {}
    for condition in CONDITIONS:
        replies[condition] = generate_reply(
            candidate_client,
            candidate_model,
            prompt,
            condition,
            sabha_system,
            role=question.get("role"),
        )

    print(f"  [{qid}] judging...", flush=True)
    scores: dict[str, JudgeScore] = {}
    for condition in CONDITIONS:
        scores[condition] = score_reply(
            judge_client, prompt, replies[condition], judge_model
        )

    pairwise: PairwiseResult = pairwise_preference(
        judge_client,
        prompt,
        sabha_reply=replies["sabha"],
        baseline_reply=replies["baseline"],
        judge_model=judge_model,
        seed=seed,
    )

    deep_skill_loaded = bool(load_deep_skill_for_role(question.get("role")))
    return {
        "id": qid,
        "role": question.get("role"),
        "category": question.get("category"),
        "deep_skill_loaded": deep_skill_loaded,
        "prompt": prompt,
        "replies": replies,
        "scores": {
            cond: {
                "decisiveness": s.decisiveness,
                "tradeoff_named": s.tradeoff_named,
                "concreteness": s.concreteness,
                "routing_present": s.routing_present,
                "length_discipline": s.length_discipline,
                "total": s.total,
                "rationale": s.rationale,
            }
            for cond, s in scores.items()
        },
        "pairwise": {"winner": pairwise.winner, "rationale": pairwise.rationale},
    }


def aggregate(records: list[dict]) -> dict:
    """Roll up per-question scores into condition-level aggregates."""
    agg: dict[str, dict[str, float]] = {
        "baseline": {
            "decisiveness": 0.0,
            "tradeoff_named": 0.0,
            "concreteness": 0.0,
            "routing_present": 0.0,
            "length_discipline": 0.0,
            "total": 0.0,
        },
        "sabha": {
            "decisiveness": 0.0,
            "tradeoff_named": 0.0,
            "concreteness": 0.0,
            "routing_present": 0.0,
            "length_discipline": 0.0,
            "total": 0.0,
        },
    }
    n = len(records)
    if n == 0:
        return {"per_condition": agg, "pairwise": {}, "n": 0}

    for rec in records:
        for cond in CONDITIONS:
            s = rec["scores"][cond]
            for k in agg[cond]:
                agg[cond][k] += s[k]

    for cond in CONDITIONS:
        for k in agg[cond]:
            agg[cond][k] = round(agg[cond][k] / n, 2)

    pairwise = {"sabha": 0, "baseline": 0, "tie": 0}
    for rec in records:
        pairwise[rec["pairwise"]["winner"]] += 1

    return {"per_condition": agg, "pairwise": pairwise, "n": n}


def render_markdown(records: list[dict], summary: dict, meta: dict) -> str:
    lines: list[str] = []
    lines.append("# Sabha OS — eval results")
    lines.append("")
    lines.append(f"- **Run date:** {meta['run_date']}")
    lines.append(f"- **Candidate model:** `{meta['candidate_model']}`")
    lines.append(f"- **Judge model:** `{meta['judge_model']}`")
    lines.append(f"- **Question set:** v1 ({summary['n']} questions)")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Baseline | Sabha | Δ |")
    lines.append("|---|---:|---:|---:|")
    per = summary["per_condition"]
    for key in (
        "decisiveness",
        "tradeoff_named",
        "concreteness",
        "routing_present",
        "length_discipline",
        "total",
    ):
        b = per["baseline"][key]
        s = per["sabha"][key]
        delta = round(s - b, 2)
        sign = "+" if delta > 0 else ""
        lines.append(f"| {key.replace('_', ' ')} | {b} | {s} | {sign}{delta} |")
    lines.append("")
    pw = summary["pairwise"]
    lines.append("### Pairwise preference")
    lines.append("")
    lines.append(
        f"- **Sabha preferred:** {pw['sabha']} / {summary['n']} "
        f"({round(100 * pw['sabha'] / summary['n'], 1)}%)"
    )
    lines.append(
        f"- **Baseline preferred:** {pw['baseline']} / {summary['n']} "
        f"({round(100 * pw['baseline'] / summary['n'], 1)}%)"
    )
    lines.append(
        f"- **Tie:** {pw['tie']} / {summary['n']} "
        f"({round(100 * pw['tie'] / summary['n'], 1)}%)"
    )
    lines.append("")
    lines.append("## Per-question results")
    lines.append("")
    lines.append("| id | role | deep skill | pairwise winner | Sabha total | Baseline total |")
    lines.append("|---|---|---|---|---:|---:|")
    for rec in records:
        deep = "✓" if rec.get("deep_skill_loaded") else "—"
        lines.append(
            f"| `{rec['id']}` | {rec['role']} | {deep} "
            f"| **{rec['pairwise']['winner']}** "
            f"| {rec['scores']['sabha']['total']} "
            f"| {rec['scores']['baseline']['total']} |"
        )
    lines.append("")
    lines.append("## Sample side-by-side (first three questions)")
    lines.append("")
    for rec in records[:3]:
        lines.append(f"### `{rec['id']}` — {rec['role']}")
        lines.append("")
        lines.append("**Question:**")
        lines.append("")
        lines.append("> " + rec["prompt"].strip().replace("\n", "\n> "))
        lines.append("")
        lines.append("**Baseline reply:**")
        lines.append("")
        lines.append("```")
        lines.append(rec["replies"]["baseline"].strip())
        lines.append("```")
        lines.append("")
        lines.append("**Sabha reply:**")
        lines.append("")
        lines.append("```")
        lines.append(rec["replies"]["sabha"].strip())
        lines.append("```")
        lines.append("")
        lines.append(
            f"**Pairwise:** winner = `{rec['pairwise']['winner']}` — "
            f"{rec['pairwise']['rationale']}"
        )
        lines.append("")
    return "\n".join(lines)


def save_checkpoint(records: list[dict], basename: str, meta: dict) -> None:
    """Write JSON + Markdown snapshots after each completed question.

    Idempotent: overwrites existing files. Always also refreshes latest.md
    so the most recent run is easy to find.
    """
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    summary = aggregate(records)
    json_path = RESULTS_DIR / f"{basename}.json"
    md_path = RESULTS_DIR / f"{basename}.md"
    latest_md = RESULTS_DIR / "latest.md"

    with json_path.open("w") as f:
        json.dump({"meta": meta, "summary": summary, "records": records}, f, indent=2)
    md = render_markdown(records, summary, meta)
    md_path.write_text(md)
    latest_md.write_text(md)


def load_checkpoint(basename: str) -> tuple[list[dict], Optional[dict]]:
    """Load existing records if a checkpoint exists. Returns ([], None) if not."""
    json_path = RESULTS_DIR / f"{basename}.json"
    if not json_path.exists():
        return [], None
    with json_path.open() as f:
        data = json.load(f)
    return data.get("records", []), data.get("meta")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Sabha OS eval.")
    parser.add_argument("--candidate-model", default=DEFAULT_CANDIDATE_MODEL)
    parser.add_argument("--judge-model", default=None,
        help="Judge model. If omitted, defaults per --judge-provider.")
    parser.add_argument(
        "--judge-provider",
        choices=["anthropic", "openai", "google"],
        default="anthropic",
        help=(
            "Which provider hosts the judge model. Default 'anthropic' "
            "preserves the v1.3.1 + v3 in-family run. Use 'openai' or "
            "'google' to defeat in-family bias — requires the corresponding "
            "API key (OPENAI_API_KEY or GOOGLE_API_KEY) and SDK installed."
        ),
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Only run the first N questions."
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--out-name",
        default=None,
        help="Override the result file basename (default: YYYY-MM-DD).",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="If the output file already exists, skip questions already completed.",
    )
    args = parser.parse_args()

    # The candidate is always Anthropic (Sabha-on-Claude is the tested
    # configuration; LLM-agnostic candidate is held per docs/ROADMAP.md).
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set. Export it and re-run.", file=sys.stderr)
        return 1
    candidate_client = Anthropic()

    # The judge can be any supported provider; defeats in-family bias.
    from evals.judge_clients import build_judge_client, default_judge_model
    judge_client = build_judge_client(args.judge_provider)
    judge_model = args.judge_model or default_judge_model(args.judge_provider) or DEFAULT_JUDGE_MODEL

    sabha_system = load_sabha_system_prompt()
    questions = load_questions(args.limit)

    run_date = dt.date.today().isoformat()
    basename = args.out_name or run_date
    meta = {
        "run_date": run_date,
        "candidate_model": args.candidate_model,
        "judge_provider": args.judge_provider,
        "judge_model": judge_model,
        "rubric_version": "v3",
    }

    if args.resume:
        existing, existing_meta = load_checkpoint(basename)
        done_ids = {r["id"] for r in existing}
        records: list[dict] = list(existing)
        if existing_meta:
            # Preserve original run_date so the report stays coherent on resume.
            meta["run_date"] = existing_meta.get("run_date", run_date)
        if done_ids:
            print(
                f"Resuming '{basename}': {len(done_ids)} of {len(questions)} "
                f"questions already complete; will skip those."
            )
    else:
        records = []
        done_ids = set()

    print(
        f"Running {len(questions)} questions "
        f"(candidate={args.candidate_model}, "
        f"judge={args.judge_provider}:{judge_model}, rubric=v3)..."
    )

    for i, q in enumerate(questions, start=1):
        if q["id"] in done_ids:
            print(f"[{i}/{len(questions)}] {q['id']} (cached, skipping)")
            continue
        print(f"[{i}/{len(questions)}] {q['id']}")
        rec = run_question(
            candidate_client=candidate_client,
            judge_client=judge_client,
            candidate_model=args.candidate_model,
            judge_model=judge_model,
            sabha_system=sabha_system,
            question=q,
            seed=args.seed + i,
        )
        records.append(rec)
        # Checkpoint after every question so a mid-run crash never loses prior work.
        save_checkpoint(records, basename, meta)

    summary = aggregate(records)
    json_path = RESULTS_DIR / f"{basename}.json"
    md_path = RESULTS_DIR / f"{basename}.md"
    latest_md = RESULTS_DIR / "latest.md"

    print(f"\nDone. Wrote:\n  {json_path}\n  {md_path}\n  {latest_md}")
    pw = summary["pairwise"]
    print(
        f"Pairwise preference: sabha={pw['sabha']} baseline={pw['baseline']} "
        f"tie={pw['tie']} (n={summary['n']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
