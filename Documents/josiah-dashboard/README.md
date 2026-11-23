# Josiah application toolkit

This folder contains a first-pass GUTC-targeted resume, a branded local application dashboard, and a small local tool for preparing application drafts.

## Open the dashboard

Open `application_dashboard.html` in a browser. It provides:

- An overview of the application evidence and claim boundaries.
- A place to write answers with editable seed drafts, word and character counts, local browser save, and copy-to-clipboard.
- JSON question loading for the real form questions once they are available.
- A resume-fit view with links to the editable resume and CLI tool.
- A guardrail checklist and Markdown review-packet export.

The dashboard is intentionally local and review-first. It does not sign in, make hidden network calls, or submit a form.

The tool does not log in to Google, fill a live form, or submit an application. It creates a review packet from the exact questions supplied by the user. That boundary keeps personal claims, dates, word limits, and final consent visible before anything is sent.

## Create a draft packet

```text
python3 application_tool.py draft \
  --source "/path/to/dossier.txt" \
  --questions questions.json \
  --form-url "https://example.com/form" \
  --output application-review.md
```

The questions file can be a JSON list of strings:

```json
["Why are you applying?", "What do you hope to learn?"]
```

It can also include limits:

```json
[
  {"id": "interest", "question": "Why are you applying?", "word_limit": 300},
  {"id": "bio", "question": "Tell us about your background.", "character_limit": 1500}
]
```

## Audit a draft

```text
python3 application_tool.py audit application-review.md
```

The audit catches known risk patterns from the supplied dossier, including unsupported grant authority, treating the Trans Liberation Cohort as launched, treating Josiah as a John Jay organizer or moderator, using the anticipated NALAC workload as a completed count, and calling the NYU certificate complete.

## Before submission

1. Add the exact form questions and limits.
2. Replace contact placeholders.
3. Add Josiah's own examples and wording where the draft asks for them.
4. Check every date, role, public appearance, credential, and employer-related claim.
5. Review the final answers with Josiah and submit through the form manually.
