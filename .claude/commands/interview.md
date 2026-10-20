---
description: Build an interview prep pack for a tracked application
argument-hint: "<tracker id> [date/time and format, e.g. 'Sunday 10am panel']"
---

# /interview – prep pack

1. Find the application: `python tools/tracker.py list --json` and pick id `$ARGUMENTS`.
   Read its folder in `applications/` (posting, evaluation, CV, cover letter) and `profile/profile.md`.
2. Update the tracker: `python tools/tracker.py update <id> --status interview --note "<when/format>"`.
3. Research the company again by name on its own site and recent news (last 12 months).
4. Write `applications/<folder>/interview_prep.md` with:
   - **The 60-second introduction** in English (and Arabic if the posting or employer is Arabic-speaking).
   - **8-10 likely questions** for this role (technical and behavioral), each with a suggested answer
     built only from the profile, using the STAR format for behavioral ones.
   - **Gap questions:** the weak spots from the evaluation and an honest, positive answer for each.
   - **Technical refresh list:** topics from the posting to review, with one-line explanations.
   - **Kuwait specifics** from `knowledge/kuwait-job-market.md`: documents to bring, notice
     period/availability, salary in KWD per month (give a researched range with sources, or
     say none was found).
   - **5 questions to ask them.**
   - **Logistics checklist:** location or link, what to wear, arrive 10-15 minutes early.
5. Offer a mock interview: ask the questions one at a time and give feedback after each answer.
