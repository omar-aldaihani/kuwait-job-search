# Kuwait job market guide

Reference for `/search`, `/apply` and `/interview`. Rules, programs and amounts in
Kuwait change often. **Treat anything here about government rules, allowances or
fees as a lead to check, not a fact:** confirm it on the official site (or a
recent news source) before telling the user, and say how recent your source is.

## Where jobs are posted

| Source | Best for | How `/search` uses it |
| --- | --- | --- |
| [Bayt.com](https://www.bayt.com/en/kuwait/jobs/) | Largest Gulf board; private sector, all levels | `site:bayt.com` searches + the Kuwait jobs listing |
| [LinkedIn Jobs](https://www.linkedin.com/jobs/) | Multinationals, banks, telecom, tech | `site:linkedin.com/jobs` searches (no automated login or scraping) |
| [GulfTalent](https://www.gulftalent.com/kuwait/jobs) | Professional and mid-level roles | `site:gulftalent.com` searches |
| [NaukriGulf](https://www.naukrigulf.com/) | High volume, many engineering and IT roles | `site:naukrigulf.com` searches |
| Employer career pages | Oil sector, banks, telecom; often posted here first | listed below, fetched directly |

Search engines index these boards well, so `/search` uses web search with `site:`
filters and then opens individual postings. It never logs in to a site, never
bypasses a block, and stops if a site refuses access.

## Large employers worth checking directly

These change; verify a careers page exists before linking it.

- **Oil and gas (Kuwait Petroleum Corporation group):** KPC, Kuwait Oil Company (KOC),
  Kuwait National Petroleum Company (KNPC), Kuwait Integrated Petroleum Industries
  Company (KIPIC), Petrochemical Industries Company (PIC), Kuwait Gulf Oil Company (KGOC),
  Kuwait Oil Tanker Company (KOTC), KUFPEC, Kuwait Petroleum International (Q8).
  These often recruit in announced rounds, frequently for Kuwaiti graduates, with
  aptitude tests and set document lists.
- **Telecom:** Zain Kuwait, Ooredoo Kuwait, stc Kuwait.
- **Banks:** NBK, Kuwait Finance House (KFH), Boubyan Bank, Gulf Bank, Burgan Bank,
  Warba Bank, Al Ahli Bank of Kuwait (ABK), Commercial Bank of Kuwait (CBK). Banks run
  large IT, cybersecurity and digital teams.
- **Government technology and regulation:** Central Agency for Information Technology
  (CAIT), Communication and Information Technology Regulatory Authority (CITRA).
- **Large groups:** Agility, Alghanim Industries, Alshaya Group, Kuwait Airways,
  Jazeera Airways.
- **IT services and system integrators:** many small and mid-size firms hire IT
  support, network and POS technicians; Bayt and LinkedIn are the main channel.

## Paths that depend on nationality

Ask the user (in `/setup`) whether they are a Kuwaiti citizen, because the routes differ.
Do not assume, and do not put nationality on a CV unless the user asks for it.

**Kuwaiti citizens**
- **Government jobs:** registered through the Civil Service Commission (CSC, "Diwan")
  job registration e-service on the Kuwait government portal
  ([e.gov.kw: Register for a job](https://www.e.gov.kw/sites/kgoenglish/Pages/eServices/CSC/RegisterForJob.aspx)).
  The CSC nominates registered applicants to ministries in rounds.
- **Private sector:** Kuwaiti employees in the private sector have received a monthly
  national labor support allowance managed by the Public Authority for Manpower (PAM),
  scaled by education level. Amounts and eligibility have been reviewed over the years
  ([Kuwait Times, 2022](https://kuwaittimes.com/kuwaitis-private-sector-allowance-will-not-stop)),
  so check PAM's current rules before quoting a number.
- **Graduates of foreign universities** usually need a degree equivalency
  certificate from the Ministry of Higher Education for government and many oil-sector jobs.
  Start this early; it can take weeks.

**Non-Kuwaiti residents and people moving to Kuwait**
- The employer sponsors the work permit. Engineering job titles have required degree
  accreditation with the Kuwait Society of Engineers (KSE) for permit issue or renewal
  ([Gulf News](https://gulfnews.com/world/gulf/kuwait/kuwait-degree-accreditation-a-must-for-work-permit-renewal-1.76526867)).
  Check the current KSE rules for the user's degree and country of study.
- Some roles and sectors are reserved for or prioritize Kuwaiti nationals; flag postings
  that say "Kuwaiti nationals only" as a deal-breaker for non-Kuwaitis.

## Documents employers commonly ask for

Civil ID copy, passport copy, degree certificate and transcript (with equivalency for
foreign degrees where required), KSE membership/accreditation for engineering titles,
experience letters, and sometimes a good-conduct (police clearance) certificate.
`/apply` lists the ones a posting mentions in the application checklist.

## CV conventions in Kuwait

- English CV for most private-sector roles; Arabic is expected for many government
  bodies and Arabic-language postings (use `templates/cover_letter_ar.html`).
- Kuwaiti mobile numbers are written `+965 XXXX XXXX`.
- A photo, date of birth, marital status and nationality are common on Gulf CVs but
  **optional**. Include them only if the user chooses to; they are personal data.
- Keep it to 1 page for 0-3 years of experience, 2 pages maximum otherwise.
- Many employers use applicant-tracking software: one column, plain section headings,
  real text for contact details.

## Scam warning signs

Real employers in Kuwait do not charge candidates for a job, visa, medical test or
"processing". Treat these as red flags and tell the user: requests for any payment,
WhatsApp-only contact, personal email domains (gmail/yahoo/hotmail) for a large
company, offers with no interview, and "guaranteed visa" promises.
`tools/posting_guard.py` flags many of these automatically.

## Interview norms

- Interviews often start with relationship-building small talk; let the interviewer
  set the pace.
- Expect questions on availability, notice period, and (for Kuwaitis) whether you are
  registered with the CSC or already in a government job.
- Salary is usually discussed in Kuwaiti dinar (KWD) per month; know the market range
  for the role before the interview (Bayt and GulfTalent publish salary guides).
- Technical roles may include a practical test or a panel with a technical lead.
