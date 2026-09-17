"""Reject conditions for the B2B recognition-tier Telegram approve step.

From social-engine-post-constraints.md. Mechanical checks cover the failures
that can be detected without inventing a reviewer. Conditions 1, 2, and 9
still need a human read; this module does not auto-regenerate.
"""

from __future__ import annotations

import re
from typing import Optional

from app.models import B2B_CTA_LINE

# Documented approve-step failures. Numbering matches the constraints file.
B2B_REJECT_CONDITIONS: tuple[str, ...] = (
    "1. Explained. Any sentence tells the reader why.",
    "2. Sarcastic setup. Beat 1 mocks the tool or the buyer.",
    "3. Blame. A department, vendor, executive or person is at fault.",
    "4. A number appeared. Anything quantified that wasn't in the brief.",
    "5. Multiple parentheticals. Dilutes the hinge.",
    "6. Product leak. Any brand, framework or internal term.",
    "7. Question CTA. Asking the reader anything.",
    "8. Handoff drift. The final line is paraphrased rather than exact.",
    "9. Sounds written. Expanded forms, inverted clauses, a listy rhythm.",
)

# Never-name list from the B2B system prompt, plus ArVA (hard naming, not public).
_PRODUCT_LEAK_TERMS: tuple[str, ...] = (
    "digital fog",
    "digital friction",
    "infrastructure",
    "operational architecture",
    "transformby10x",
    "tbtx",
    "bizbuilders",
    "bbai",
    "bizbot mrktng",
    "bbm",
    "proof",
    "flow agent as",
    "quad keystones",
    "mr. nobody",
    "mr nobody",
    "arva",
)

_BANNED_VOCAB: tuple[str, ...] = (
    "supercharge",
    "unlock",
    "10x",
    "game-changing",
    "revolutionary",
    "seamless",
    "leverage",
    "optimize",
    "streamline",
    "transform",
    "empower",
    "drive efficiency",
    "operational alignment",
    "governance layer",
    "digital transformation",
    "synergy",
)

_EXPANDED_FORMS: tuple[str, ...] = (
    "do not",
    "does not",
    "is not",
    "are not",
    "cannot",
    "it is",
    "there is",
    "they are",
    "you are",
    "we are",
    "will not",
    "would not",
)


def _last_content_line(post: str) -> str:
    lines = [line.strip() for line in (post or "").splitlines() if line.strip()]
    return lines[-1] if lines else ""


def mechanical_b2b_flags(post: str, brief_text: Optional[str] = None) -> list[str]:
    """Return mechanical fail labels. Empty means no automatic flag.

    Does not attempt explained / sarcastic / sounds-written beyond dashes and
    expanded forms. Does not regenerate.
    """
    flags: list[str] = []
    body = post or ""
    brief = brief_text or ""
    brief_lower = brief.lower()

    parens = body.count("(")
    if parens != 1:
        flags.append("5. Multiple parentheticals.")

    if "?" in body:
        flags.append("7. Question CTA.")

    if _last_content_line(body) != B2B_CTA_LINE:
        flags.append("8. Handoff drift.")

    if "\u2014" in body or "\u2013" in body:
        flags.append("9. Sounds written.")

    lowered = body.lower()
    leaked = [term for term in _PRODUCT_LEAK_TERMS if re.search(rf"\b{re.escape(term)}\b", lowered)]
    leaked.extend(term for term in _BANNED_VOCAB if term in lowered)
    if leaked:
        flags.append("6. Product leak.")

    lowered_for_forms = re.sub(r"[^a-z\s]", " ", lowered)
    if any(re.search(rf"\b{re.escape(form)}\b", lowered_for_forms) for form in _EXPANDED_FORMS):
        if "9. Sounds written." not in flags:
            flags.append("9. Sounds written.")

    invented_numbers = []
    for match in re.finditer(r"\d+(?:[.,]\d+)?%?", body):
        token = match.group(0)
        if token.lower() not in brief_lower:
            invented_numbers.append(token)
    if invented_numbers:
        flags.append("4. A number appeared.")

    return flags
