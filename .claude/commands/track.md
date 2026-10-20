---
description: Show your application pipeline, update statuses and draft follow-ups
argument-hint: "[e.g. '3 applied', '5 rejected', 'followups']"
---

# /track – pipeline

- With no arguments: run `python tools/tracker.py stats` and
  `python tools/tracker.py list`, and show them as a short summary
  (counts by status, then a table of open applications, newest first).
- With `<id> <status>` (e.g. `3 applied`): run
  `python tools/tracker.py update <id> --status <status>` and confirm.
  Valid statuses: found, shortlisted, applied, interview, offer, accepted, rejected, withdrawn, skipped.
- With `followups`: run `python tools/tracker.py followups --days 10 --json`. For each result,
  draft a short, polite follow-up email (English, or Arabic if the application was in Arabic)
  and show it for the user to send themselves. Never send anything.
- After a rejection, offer one useful lesson from the evaluation (e.g. a skill to build),
  without dwelling on it.
