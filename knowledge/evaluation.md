# How to score a job against the profile

Used by `/search` (quick score) and `/apply` (full evaluation). The score is out of
100 and must be explained, not just stated.

## 1. Gates (check first; any failure ends the evaluation)

| Gate | Fails when |
| --- | --- |
| Nationality | Posting says "Kuwaiti nationals only" and the user is not Kuwaiti (or the reverse: "expatriates only") |
| Language | Posting requires a language the profile does not list |
| Deal-breakers | Anything in the profile's deal-breaker list (e.g. night shifts, outside Kuwait, commission-only) |
| Sharia compliance | User chose **required** and the employer is classified **not compliant** in `knowledge/sharia-compliance.md`. If it is **unclear**, ask the user before scoring |
| Legitimacy | `posting_guard.py` reports scam signs that the user has not dismissed |
| Expired | Posting's deadline has passed or the page says the job is closed |

## 2. Score (100 points)

| Area | Points | What earns them |
| --- | --- | --- |
| Must-have skills | 35 | Each required skill the profile proves (degree, job, project, certificate). Partial credit for close equivalents, stated as such |
| Experience level | 20 | Years and seniority match. An entry-level user applying to "3+ years" loses points but is not auto-rejected if the rest is strong |
| Domain and tools | 15 | Same industry, systems or tools (e.g. Cisco, Windows Server, POS, embedded C) |
| Nice-to-haves | 10 | Preferred qualifications the profile meets |
| Goals and preferences | 10 | Matches the target roles, sectors and locations in `profile/search.md` |
| Growth | 10 | Realistic stretch that builds toward the user's goals |

**Sharia preference:** if the user chose **preferred**, add 5 points to compliant employers
(cap at 100) and label non-compliant or unclear ones in the results. If the user chose
**no preference**, skip this check and don't mention it.

## 3. Verdict bands

- **80-100: Strong fit.** Apply now.
- **65-79: Good fit.** Apply, and address the gaps in the cover letter.
- **50-64: Stretch.** Apply only if the user wants this employer; be honest about gaps.
- **Below 50: Skip.** Explain why in one line.

## 4. How to present it

Show: score and band, the 3 strongest matches (with the profile evidence for each),
the gaps (with a realistic way to address each), and anything Kuwait-specific the user
must know (documents, nationality requirement, Arabic needed, deadline). Keep it
short enough to read in under a minute.
