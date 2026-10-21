# cv-builder design notes (2026-10-21)

Why the skill is shaped the way it is. Companion to `CLAUDE.md` (setup) and `.claude/skills/cv-builder/` (the rules themselves).

## 1. Three principles

**Never lie.** AI-written applications fail in two ways: they invent things, and they sound like every other AI-written application. The first failure is the dangerous one, so the skill has one source of truth (the profile), a hard stop for anything the profile does not back, a −100 scoring penalty, and a write-back step so that a "no" is remembered. Skills carry a depth level (`production`, `working`, `academic`, `evaluated`, `supervised`) because most lies in CVs are upgrades, not inventions: a tutorial becomes "experience", supervision becomes authorship. The depth level fixes the wording.

**Lead with the strongest proof.** A CV that lists everything hides its best evidence in bullet seven. The profile holds ranked proof points with the evidence behind each; every run picks three for the posting and places them in the summary, the first bullets and the letter's opening. The reviewer checks placement.

**Adapt to the offer.** Candidates with more than one plausible role family (say, gameplay engineering and AI engineering) need different summaries, not one summary that mentions both. Positioning profiles make that choice explicit and reviewable before drafting. A length budget keeps the result on two pages.

## 2. Why A4 pages instead of a continuous page

An earlier version rendered each document on one tall page and cropped it to its content. Parsers read it fine; people did not: viewers show a long strip, printing is unpredictable, and the shape itself signals "generated". Real A4 pages with CSS break rules (a role title never sits alone at a page bottom) and a verifier that enforces page caps give the same linear single column with a document people recognize.

## 3. Privacy model

- The workspace (profile, applications, logs) lives outside the public repo by default, located through `CV_WORKSPACE` or a gitignored config file.
- The phone number appears only inside `<span class="private">`; the `--public` build removes it, so the same Markdown yields the PDF a recruiter gets and the PDF a website can serve.
- `privacy_check.py` scans tracked files for the user's patterns and runs as a pre-commit hook. Gitignore is one lock; the check is the second.
- Examples in the repo are fictional and labelled as such.

## 4. The profile learns

Every clarification answer is written back into the profile in the user's words: a confirmed skill at the stated depth, a confirmed number under `verified metrics` with its date, a "no" under `Not claimable` with the posting that prompted it. The skill shows the exact lines it adds. An applications log records, per posting, which profile was used, what was asked and what was answered, so the user can trace any claim in any sent document back to a confirmed fact.

## 5. What it deliberately does not do

- Hide that AI was involved. Humanizing is about reading like a person wrote it, not about evading detectors.
- Measure anything against a real applicant tracking system. The ATS score is a rubric.
- Guarantee interviews.
