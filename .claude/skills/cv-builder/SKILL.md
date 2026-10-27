---
name: cv-builder
description: Tailor a CV, cover letter and project portfolio to a specific job posting, using the candidate profile as the only source of truth, then check fit, review, score, compile verified A4 PDFs and record the application. Use this for anything about applying to a job: a posting URL or pasted text, "apply to this", "is this role a fit", a resume or CV rewrite, a cover letter, a generic CV, a phone-less public CV, an ATS or fit score, interview prep for an application, or updating what happened to applications already sent. Trigger even when the user only pastes a job description without asking for anything.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
---

# CV Builder

Turns a job description (JD) into a tailored CV, cover letter and project portfolio, then checks the fit, reviews, scores, compiles and verifies them. Three principles decide every choice:

1. **Never lie.** Every claim comes from the candidate profile. A posting item the profile does not back is a question for the user, never an assumption. See `01-structure-and-style.md` section C and `05-profile-schema.md`.
2. **Lead with the strongest proof.** Each run picks the three proof points that matter most for this posting and puts them where a reader looks first: the summary, the first bullets, the cover letter's opening.
3. **Adapt to the offer.** The run names a positioning profile, orders the content by what the posting values, and stays within a length budget so the result reads well on paper.

**Source of truth:** `<workspace>/_private/candidate_profile_<name>.md`, shaped per [05-profile-schema.md](05-profile-schema.md). **First time?** Copy `templates/candidate_profile_template.md` there and follow [CLAUDE.md](../../../CLAUDE.md).

**Output:** `<workspace>/_generated/<Company_Role>/` with `CV_<First>_<Last>.md` + `.pdf`, `Cover_Letter_<First>_<Last>.md` + `.pdf`, `Project_Portfolio_<First>_<Last>.md` + `.pdf`, and `JD.md` (the posting as seen). These folders are sent applications: never delete or overwrite one without being asked to revise that application.

## Reference files

| File | Covers |
|---|---|
| [01-structure-and-style.md](01-structure-and-style.md) | Section order, header convention, length budget, proof-point placement, bullet formula, photo rules, writing style, portfolio rules |
| [02-humanization-checklist.md](02-humanization-checklist.md) | The humanization pass: AI-tell checklist and the no-fact-drift constraint |
| [03-pdf-compilation-and-verification.md](03-pdf-compilation-and-verification.md) | A4 compilation, the public variant, verification commands, the ATS rubric |
| [04-drafter-reviewer-workflow.md](04-drafter-reviewer-workflow.md) | The fresh-context reviewer subagent |
| [05-profile-schema.md](05-profile-schema.md) | Profile sections, skill depth levels, what counts as a gap |
| [06-persona-review.md](06-persona-review.md) | Reviewer personas: file format, where they live (generic in `templates/personas/`, yours in the private workspace), which join a CV panel versus a public-page panel, how the panel runs, how to create one |

## Workflow

### Phase 0 — Workspace
1. Resolve the workspace: `CV_WORKSPACE` env var, else `cvkit.config.json` next to this repo, else the repo itself. `_private/` and `_generated/` live there.
2. Read the profile in full and `<workspace>/_private/applications_log.md` if it exists (previous postings and the answers they produced).

### Phase 1 — JD analysis, fit check and mandatory clarification
1. Read the JD (URL or pasted text). **Save it first** as `<workspace>/_generated/<Folder>/JD.md` from `templates/JD_template.md`: source URL, channel, date seen, then the full posting text. Without the posting nobody can re-score the application or learn from its outcome. Check it against `## Deal-breakers` and say so if it conflicts.
2. **Fit check**, before any drafting. Rate each line `ok`, `risk` or `block`, with the profile line or fact behind it, per [03](03-pdf-compilation-and-verification.md#fit-check):
   - location and work permit against `## Languages and mobility` and `## Identity`;
   - seniority band: the posting's level (lead, manager, staff, mid…) against the titles and years in `## Experience`;
   - years in the named domain, counted from the profile, not from skills lists;
   - language required against the profile's languages;
   - title or credential the posting treats as mandatory (e.g. a named discipline) against the profile.

   The verdict is `strong`, `workable` or `unlikely`. On `unlikely`, say why and ask whether to continue; never stop silently and never continue silently.
3. Cross-reference every requirement, preference, tool, methodology and soft skill in the JD with `## Skills` and `## Experience`. Write the must-haves as a ranked list (this feeds the evidence-coverage score). An item is a **gap** when it has no profile row, or only one at `academic`, `evaluated` or `supervised` depth. Items under `## Not claimable` are settled: never claim, never re-ask.
4. **Ask about every gap in one `AskUserQuestion`**, hard or soft (agile/Scrum, a tool, a process, a soft skill). Never decide alone that something is "not claimable" or "not worth mentioning". Include relevant `## Open questions` entries. Show the weakest three must-haves and the fit verdict in the same question, so the answer to "apply and how?" is informed.
5. Choose the **positioning profile** (`## Positioning profiles`) and the **three leading proof points** (`## Proof points`) for this posting. State both to the user in one line before drafting; adjust if they object.
6. Decide photo (regional rule, unless the profile's `photo:` overrides) and output language (English unless the posting requires another, or the profile says otherwise).
7. Keep a running list of every answer, in the user's words, for Phase 7.

### Phase 2 — Drafting
1. Draft the CV, cover letter and project portfolio in Markdown per `01-structure-and-style.md`: header convention, section order, **length budget**, proof points in the summary and bullets 1–3, metrics per `## Preferences`.
2. Self-check: every claim traceable to the profile; no number outside `verified metrics`; a blank line before every list; no "Tailored for…" meta text.
3. Do not compile yet.

### Phase 3 — Humanization pass
Re-read against `02-humanization-checklist.md`. Style only: no fact, number, date, title or meaning changes.

### Phase 4 — Reviewer subagent and persona panel
1. Spawn the fresh-context reviewer per `04-drafter-reviewer-workflow.md` (quality: missed keywords, proof-point placement, length, AI tells, consistency).
2. Run the **persona panel** per `06-persona-review.md`: the generic screener and parser from `templates/personas/`, plus the private personas in `<workspace>/_private/personas/` whose `families` include the positioning profile chosen in Phase 1 (at most four in total). A CV has one reader in mind, so personas from other families stay out.
3. Apply what improves targeting without changing facts; shared persona findings become edits, single-persona findings are reported as trade-offs. A suggested new claim is a Phase 1 question. Re-run the humanization check on anything rewritten.

### Phase 5 — Gates and score
Run the two pass/fail gates (format, truth), then score evidence coverage, placement, content and keywords per the rubric in `03-pdf-compilation-and-verification.md`. A claim the profile does not back fails the truth gate: go back to Phase 1 and ask instead of deleting it quietly. Report gates, score, breakdown and the fit verdict from Phase 1 together.

### Phase 6 — Compile and verify
1. `python compile_all_pdfs.py "<Folder>"` (A4 pages). Add `--public` when a phone-less variant is needed.
2. `python verify_pdf.py` on each PDF with the page caps and the `--order` headings from `03-…`; for a public PDF add `--forbids "<phone>"`.
3. Read the PDF and check it by eye against the visual checklist. Iterate on the Markdown, never on the PDF.

### Phase 7 — State update (the profile learns)
Every answer the user gave in this run goes into the profile, in their words:
1. A confirmed skill goes to `## Skills` at the depth they described, with the scope in the note; a confirmed fact goes to the Experience/Project entry it belongs to; a confirmed number goes under that entry's `verified metrics` with today's date.
2. A "no" goes to `## Not claimable` with the date and the posting.
3. Nothing is inferred or upgraded. Show the exact lines added or changed.
4. Append one row to `<workspace>/_private/applications_log.md` (columns in `templates/applications_log_template.md`): date, folder, role, positioning, channel, fit verdict, score, sent date, outcome, nuances (gaps asked and the answers). Score and fit come from Phases 1 and 5. `sent` stays blank and `outcome` is `draft` until the user says the application went out; never guess either.
5. Runs this even after partial commands (a score-only check that asked a question).

### Phase 8 — Interview prep (optional)
On request: STAR-method prep from `## STAR stories` (say which are still `draft`), the JD and the final documents.

### Phase 9 — Outcomes (on request, or when a log row is stale)
Update `sent` and `outcome` for open rows. With a mail connector available, search the mailbox by company and read the reply; otherwise ask the user. Outcome values: `draft`, `sent`, `viewed`, `no-reply` (21+ days), `rejected`, `interview`, `offer`, `withdrawn`; add the date and the reason when the email gives one. Then compare score and fit against outcomes and report what held up and what did not. With fewer than 10 decided rows, say the sample is too small to change the rubric.

## Privacy rules

- The phone number is written only inside `<span class="private">` in document headers. The `--public` build removes it; use that build for anything that goes on a website.
- Never paste profile content into a file outside `<workspace>/_private/` or `<workspace>/_generated/`.
- `python privacy_check.py` must pass before any commit in the skill repo.

## Quick commands

- "Tailor my CV for `<JD or URL>`" → Phases 0–7.
- "Regenerate my generic CV" → Phases 0, 2–6 with the `### General` positioning profile into `_generated/Generic/`, compiled both normally and with `--public`.
- "What's the fit and score for `<company>`'s posting?" → Phases 0, 1 and 5 (plus 7 if a question was asked).
- "Update my application outcomes" → Phase 9.
- "Recompile `<Folder>`" → Phase 6.
- "Humanize `<file>`" → Phase 3 on an existing file.
- "Interview prep for `<Folder>`" → Phase 8.
- "Create a persona for `<role or company type>`" → the `create persona` flow in `06-persona-review.md`; writes to `<workspace>/_private/personas/`.
