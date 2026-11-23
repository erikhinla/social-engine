#!/usr/bin/env python3
"""Build a reviewable application packet from supplied source text.

This tool drafts and audits application materials. It does not log in to,
complete, or submit an external form.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_RESUME = ROOT / "Josiah_Vasquez_GUTC_Resume.md"

SUPPORTED_CLAIMS = {
    "Ford Foundation": "Ford Foundation role and portfolio support are documented in the supplied dossier.",
    "NALAC": "The 2025 NALAC panelist role is documented; exact application counts and awards are not.",
    "BAAD!": "BAAD! employment, development, operations, and communications work are documented.",
    "AfroResistance": "Participation in the 2026 Cali delegation is documented; organizer or founder claims are not.",
    "John Jay": "Panelist participation is documented; moderator or organizer claims are not.",
    "NYU": "The certificate is documented as in progress through 2026 and must not be called completed without confirmation.",
}

RISK_PATTERNS = [
    (r"\b(founded|co-founded|launched|delivered)\b.{0,60}\b(Trans Liberation Cohort|TLC)\b", "The dossier describes TLC as a concept or planning effort, not a confirmed launch."),
    (r"\b(approved|directed|awarded|controlled)\b.{0,80}\b(Ford|grant|funding)\b", "Do not imply independent Ford grant authority or control of a funding portfolio."),
    (r"\b(organized|moderated|convened)\b.{0,60}\b(John Jay|Rooted in Solidarity)\b", "The documented role is panelist."),
    (r"\b(founded|organized)\b.{0,60}\bAfroResistance\b", "The dossier documents delegation participation, not founding or organizing AfroResistance."),
    (r"\b(70|seventy)\b.{0,30}\b(applications|proposals)\b", "Seventy was an anticipated reviewer workload, not a confirmed completed count."),
    (r"\b(under|less than)\s+five years\b.{0,50}\b(experience|office)\b", "Do not claim fewer than five years of total office experience."),
    (r"\b(completed|earned|received)\b.{0,40}\b(NYU|Global Affairs certificate)\b", "The supplied dossier treats the NYU certificate as in progress through 2026."),
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Cannot read {path}: {exc}") from exc


def load_questions(path: Path) -> list[dict[str, Any]]:
    try:
        raw = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Questions file is not valid JSON: {exc}") from exc
    if isinstance(raw, dict):
        raw = raw.get("questions", [])
    if not isinstance(raw, list):
        raise SystemExit("Questions JSON must be a list or an object with a questions list.")
    questions: list[dict[str, Any]] = []
    for index, item in enumerate(raw, start=1):
        if isinstance(item, str):
            questions.append({"id": f"q{index}", "question": item})
        elif isinstance(item, dict) and item.get("question"):
            questions.append(item)
        else:
            raise SystemExit(f"Question {index} must be a string or an object with a question field.")
    return questions


def evidence_for(question: str) -> list[str]:
    q = question.lower()
    evidence: list[str] = []
    if any(word in q for word in ("why", "interest", "motivat", "fit", "leadership")):
        evidence += [
            "Ford Foundation program support across GREJ-I and CEG-I since November 2023.",
            "Direct 2025 NALAC grant-review panel experience.",
            "Community-based arts and development experience at BAAD! Bronx Academy of Arts and Dance.",
            "Interest in material, sustained support for trans-led movements and stronger grantmaking practice.",
        ]
    if any(word in q for word in ("experience", "work", "role", "professional", "background")):
        evidence += [
            "Program operations, partner coordination, convening logistics, contracts, invoices, and knowledge management at Ford Foundation.",
            "Donor database, annual appeal, communications, programming, and operations work at BAAD!.",
            "Proposal review and panel deliberation for the 2025 NALAC Fund for the Arts.",
        ]
    if any(word in q for word in ("goal", "learn", "develop", "growth", "future", "need")):
        evidence += [
            "Named learning goals include grantmaking strategy, equitable resource allocation, feedback, leadership, mentorship, and professional community.",
            "NYU Global Affairs certificate is listed as in progress through 2026 and requires confirmation before final use.",
        ]
    if any(word in q for word in ("community", "trans", "racial", "justice", "movement", "identity")):
        evidence += [
            "Self-described queer, non-binary, Afro-Latine identity and Bronx roots.",
            "2026 AfroResistance transnational solidarity delegation participation and John Jay panelist participation.",
            "Focus on trans liberation, Black trans liberation, racial justice, human rights, and community-led philanthropy.",
        ]
    return list(dict.fromkeys(evidence))


def draft_for(question: str) -> str:
    q = question.lower()
    if any(word in q for word in ("why", "interest", "motiv", "fit")):
        return ("I am applying because I want to deepen the grantmaking knowledge and leadership practice "
                "that can help move resources toward trans-led communities. In my role at the Ford Foundation, "
                "I support two international portfolios and see how relationships, systems, convenings, and "
                "follow-through shape philanthropic work. My 2025 NALAC panel experience also gave me direct "
                "exposure to proposal review and deliberation. I would bring the perspective of someone who has "
                "worked inside a foundation, in a community-based arts organization, and in movement and cultural "
                "spaces, while still building the technical and relational skills needed for deeper grantmaking leadership.\n\n"
                "[Add one personal example and confirm the final word limit.]" )
    if any(word in q for word in ("goal", "learn", "develop", "growth", "future")):
        return ("I want to strengthen my understanding of grantmaking strategy, equitable resource allocation, "
                "feedback, and leadership. I am also looking for sustained mentorship and a peer community of "
                "trans and gender-nonconforming people working in philanthropy. The fellowship would help me connect "
                "my operational experience to more substantive participation in how institutions support movements, "
                "without losing sight of accountability to the communities those resources are meant to serve.\n\n"
                "[Specify the next role or responsibility Josiah wants to grow toward.]" )
    if any(word in q for word in ("experience", "background", "leadership")):
        return ("My experience has moved across community-based arts administration, development, organizing, and "
                "international philanthropy. At the Ford Foundation, I support program officers across two global "
                "portfolios through coordination, partner communication, convening logistics, contracts, expenses, "
                "and knowledge management. At BAAD!, I managed donor and communications systems while supporting "
                "programming and daily operations. As a 2025 NALAC Fund for the Arts panelist, I reviewed proposals "
                "and participated in deliberations to recommend awardees. These roles have taught me that the systems "
                "behind resourcing matter, and that they should remain accountable to community knowledge.\n\n"
                "[Add a specific example if the form asks for a leadership story.]" )
    return ("[Draft required after reviewing the exact form question.]\n\n"
            "Relevant evidence to consider: Ford Foundation international program support, 2025 NALAC grant review, "
            "BAAD! development and operations, AfroResistance delegation participation, and John Jay panelist participation.")


def audit_text(text: str) -> list[str]:
    findings: list[str] = []
    for pattern, message in RISK_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            findings.append(message)
    if "[Add" in text or "[Confirm" in text or "[email]" in text or "[phone]" in text:
        findings.append("The draft still contains review placeholders.")
    return list(dict.fromkeys(findings))


def measure(text: str) -> tuple[int, int]:
    words = len(re.findall(r"\b[\w’'-]+\b", text))
    return words, len(text)


def build_packet(args: argparse.Namespace) -> int:
    source = read_text(Path(args.source))
    questions = load_questions(Path(args.questions))
    lines = [
        "# Application Review Packet",
        "",
        f"Application: {args.name}",
        f"Form URL: {args.form_url or '[add form URL if applicable]'}",
        "",
        "This packet is a draft for Josiah's review. It does not submit an application.",
        "The supplied dossier is the source context. The exact form questions and limits govern the final answers.",
        "",
        "## Source checks",
        "",
        "- Source text loaded: " + str(Path(args.source)),
        "- Resume draft: " + str(DEFAULT_RESUME),
        "- Contact details: not supplied",
        "- Exact form questions: supplied by the user through the questions JSON used for this packet",
        "",
    ]
    for index, item in enumerate(questions, start=1):
        question = str(item["question"]).strip()
        limit = item.get("word_limit") or item.get("character_limit")
        limit_label = f" | limit: {limit}" if limit else ""
        draft = draft_for(question)
        evidence = evidence_for(question)
        draft_words, draft_chars = measure(draft)
        count_label = f"Draft count: {draft_words} words, {draft_chars} characters."
        lines += [f"## {index}. {question}{limit_label}", "", "### Suggested draft", "", count_label, "", draft, "", "### Evidence to verify", ""]
        lines += [f"- {entry}" for entry in evidence] or ["- No automatic evidence match. Review the dossier manually."]
        lines += ["", "### Josiah's review", "", "- [ ] Draft reflects my experience and voice", "- [ ] All dates, roles, and claims are accurate", "- [ ] Word or character limit checked", "- [ ] I have added any personal example requested", ""]
    output = "\n".join(lines)
    findings = audit_text(output)
    output += "\n## Audit findings\n\n"
    output += "\n".join(f"- {finding}" for finding in findings) if findings else "- No automated risk pattern matched. Human review is still required."
    Path(args.output).write_text(output + "\n", encoding="utf-8")
    return 0


def run_audit(path: Path) -> int:
    text = read_text(path)
    findings = audit_text(text)
    print(f"Auditing {path}")
    if findings:
        for finding in findings:
            print(f"- REVIEW: {finding}")
        return 1
    print("No automated findings. Human review is still required.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Draft and audit reviewable application materials.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    draft_parser = subparsers.add_parser("draft", help="Build a review packet from questions JSON.")
    draft_parser.add_argument("--source", required=True, help="Path to supplied dossier or source text.")
    draft_parser.add_argument("--questions", required=True, help="JSON list of question strings or question objects.")
    draft_parser.add_argument("--output", required=True, help="Output Markdown packet path.")
    draft_parser.add_argument("--name", default="GUTC Leaders Fellowship", help="Application name.")
    draft_parser.add_argument("--form-url", default="", help="External form URL, stored for reference only.")
    draft_parser.set_defaults(handler=build_packet)

    audit_parser = subparsers.add_parser("audit", help="Scan a draft for known unsupported-claim patterns.")
    audit_parser.add_argument("path", help="Draft Markdown or text file.")
    audit_parser.set_defaults(handler=lambda args: run_audit(Path(args.path)))

    args = parser.parse_args()
    return int(args.handler(args))


if __name__ == "__main__":
    sys.exit(main())
