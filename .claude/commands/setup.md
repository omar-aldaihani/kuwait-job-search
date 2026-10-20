---
description: Build your candidate profile and search preferences (run this first)
argument-hint: "[search]  (optional: only redo search preferences)"
---

# /setup – build the profile

Goal: create `profile/profile.md` and `profile/search.md` from the templates in
`profile/*.template.md`, filled with the user's real information. If `$ARGUMENTS` is
`search`, only redo `profile/search.md`.

## Step 1 – Gather what already exists

1. If `profile/profile.md` already exists, read it and ask whether to update it or start over.
2. Look in `documents/` for CVs, transcripts or certificates (`.pdf`, `.docx`, `.txt`, `.md`).
   Read them. For `.docx`, extract the text with Python (`zipfile` + the `word/document.xml`
   part) if no other reader is available.
3. If there is nothing in `documents/`, ask the user to either paste their CV or answer a
   short interview. Do not continue until you have one or the other.

## Step 2 – Fill the gaps with a short interview

Ask only for what is still missing, a few questions at a time. Always ask:

- Are you a Kuwaiti citizen? (Explain in one line that it decides which job routes apply –
  government CSC registration, private-sector support, oil-sector rounds – and that it will
  not appear on the CV unless they choose.)
- Which personal details, if any, do you want on your CV: nationality, photo, date of birth?
- Do you want to work only for Sharia-compliant employers? Offer three answers: **required**
  (skip non-compliant employers such as conventional banks), **preferred** (flag them but still
  show them) or **no preference**. Ask this neutrally for every user; never assume it from their
  name, nationality or religion. Explain in one line what it changes, using
  `knowledge/sharia-compliance.md`.
- Languages and level.
- For foreign degrees: has the Ministry of Higher Education equivalency been done?
- Target roles, sectors, dream employers, deal-breakers, minimum salary (optional).

Never ask for Civil ID numbers, passport numbers, bank details or passwords, and never store them.

## Step 3 – Write the files

1. Copy `profile/profile.template.md` to `profile/profile.md` and replace every `[PLACEHOLDER]`.
   Delete lines that do not apply instead of leaving placeholders.
2. Copy `profile/search.template.md` to `profile/search.md` and fill it in. Suggest search
   keywords (English and Arabic) based on the target roles, and let the user edit them.
3. Make sure `applications/` exists and run `python tools/tracker.py stats` once to confirm
   the tools work.

## Step 4 – Confirm

Show a short summary (name, target roles, top skills, what is missing such as
certificates or equivalency) and point out 2-3 things that would most strengthen
applications in Kuwait, using `knowledge/kuwait-job-market.md` (verify anything
rule-related before stating it). Finish with: "Next: run /search".
