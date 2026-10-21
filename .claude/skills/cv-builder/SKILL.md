---
name: cv-builder
description: Tailor a CV, cover letter, and project portfolio to a specific job posting, using candidate_profile_<your-name>.md as the factual source of truth. Triggers on requests to apply, tailor a CV/resume, write a cover letter, build a project portfolio, or check an ATS score for a job description.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
---

# CV Builder

This skill runs the full pipeline for turning a job description (JD) into a tailored CV, cover letter, and project portfolio: draft → humanize → review → score → compile → verify.
**Source of truth for facts:** `_private/candidate_profile_<your-name>.md`. This is the single authoritative source of all your experience, skills, and positioning — the skill reads from it, never invents. Never add a skill, tool, title, or achievement that isn't documented there; see `01-structure-and-style.md`'s "ASK BEFORE LYING" rule. **First time setting up?** [See CLAUDE.md for detailed instructions on populating your candidate profile](../../CLAUDE.md#2-create-your-candidate-profile-in-_private).

**Output:** a folder named after the company/role inside `_generated/` (e.g. `_generated/Acme_Corp/`, `_generated/Example_Platform_Lead/`), containing `CV_<Name>.md`/`.pdf`, `Cover_Letter_<Name>.md`/`.pdf`, and `Project_Portfolio_<Name>.md`/`.pdf`. These folders hold real, already-submitted application materials — never delete or silently overwrite an existing one; ask before touching a folder that already has content, unless the user is explicitly asking to revise that specific application.

## Reference files

| File | Covers |
|---|---|
| [01-structure-and-style.md](01-structure-and-style.md) | Section order, bullet formula, ASK BEFORE LYING, flagship-skill rule, regional photo rules, HTML header requirement, writing-style/anti-cliché rules, Project Portfolio rules |
| [02-humanization-checklist.md](02-humanization-checklist.md) | The humanization pass: AI-tell checklist and the hard no-fact-drift constraint |
| [03-pdf-compilation-and-verification.md](03-pdf-compilation-and-verification.md) | How to compile, crop, and verify the PDFs; the ATS Scoring Engine rubric |
| [04-drafter-reviewer-workflow.md](04-drafter-reviewer-workflow.md) | How to spawn and use the fresh-context reviewer subagent |

## Workflow

### Phase 1 — JD Analysis & Mandatory Clarification
1. Read the JD (URL fetch or pasted text) and your `_private/candidate_profile_<your-name>.md`.
2. Cross-reference: which required/preferred skills does the profile support, which are missing or ambiguous? Skills listed under the profile's `Confirmed gaps` section are settled: never claim them, and don't ask about them again unless the user says things changed.
3. **HALT if the JD requires something not in the profile.** Use `AskUserQuestion` to ask before drafting — never assume or invent. This is non-negotiable; see `01-structure-and-style.md` section C.
4. Once clarified (or confirmed no gaps), proceed. Keep a running list of every answer the user gave, in their own words, for Phase 7.

### Phase 2 — Drafting
1. Draft CV, Cover Letter, and Project Portfolio in Markdown per `01-structure-and-style.md`.
2. Self-critique against: truthfulness, flagship-skill prominence, bullet ordering, section hierarchy, blank-line-before-list formatting.
3. Revise. Stop here — do not compile to PDF yet (compilation happens once, in Phase 6, after humanization and review, not before).

### Phase 3 — Humanization Pass
Re-read the drafted Markdown against `02-humanization-checklist.md`. Rewrite for natural variation. **Hard constraint: no fact, claim, number, or meaning changes in this phase — style only.**

### Phase 4 — Reviewer Subagent Critique
Spawn a fresh-context subagent per `04-drafter-reviewer-workflow.md`. Apply its feedback (missed keywords, weak framing, generic language, residual AI-sounding text) back into the Markdown. Re-run the humanization check on anything the reviewer rewrote.

### Phase 5 — ATS Scoring
Score the final Markdown per the 0–100 rubric in `03-pdf-compilation-and-verification.md`. A hallucinated skill/claim is an automatic -100 — if you find one at this stage, go back to Phase 1 and ask the user instead of silently removing it.

### Phase 6 — Compile & Verify PDFs
1. `python compile_all_pdfs.py "<FolderName>"` to compile just this folder's Markdown files (output goes to `_generated/<FolderName>/`).
2. `python verify_pdf.py "<path>.pdf" --contains "<full name>" --contains "<email>"` for each generated PDF (pull name/email/phone from your candidate profile).
3. Read the PDF (the Read tool renders it) and visually inspect: content complete, no trailing whitespace, header renders as a flexbox row not broken text, fonts consistent.
4. Iterate (edit Markdown, recompile) until all of `03-pdf-compilation-and-verification.md`'s checklist passes.

### Phase 7 — State Update (the profile learns)
Every answer the user gave during the run (Phase 1 clarifications, plus anything asked again in Phase 4 or 5) must end up in `_private/candidate_profile_<your-name>.md`, so the next application starts from better facts and the same question isn't asked twice. This is a rule, not an extra: don't finish a run that asked questions without doing it.

1. **Only what the user stated.** Write their own words and scope. Never infer, round up, or upgrade an answer ("used Kubernetes once in a tutorial" is recorded as exactly that, not as "Kubernetes").
2. **Put it where it belongs.** A confirmed skill or detail goes in the matching profile section (Technical Skills, or the role it came from). A confirmed *no* goes under a `Confirmed gaps` section with the date and the posting that prompted it, so it is never claimed later. If the user says it changed, update the entry.
3. **Show what changed.** List the exact lines added or edited so the user can correct or revert anything.
4. **Run it on partial commands too.** An ATS-only or analysis-only run that asked questions still writes its answers back.

### Phase 8 — Interview Prep (optional)
If the user wants it, offer a STAR-method interview prep pass based on the JD and the final CV/cover letter.

## Quick commands

- "Tailor my CV for `<JD or URL>`" → full Phase 1–7 workflow.
- "What's the ATS score for `<company>`'s posting against my current CV?" → Phase 1 + 5 only, no drafting (plus Phase 7 if you answered any question).
- "Recompile `<FolderName>`" → Phase 6 only (useful after a manual Markdown edit).
- "Humanize `<file>`" → Phase 3 only, against an already-drafted file.
