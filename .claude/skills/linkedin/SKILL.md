---
name: linkedin
description: Keep a LinkedIn presence consistent with the candidate profile and write LinkedIn text that is true. Use this whenever the user mentions LinkedIn in any form: updating their headline, About, experience entries, skills or featured section; checking that the live profile does not overclaim; writing a LinkedIn post about a project, launch or lesson; replying to a recruiter message; a connection note, follow-up or thank-you; or deciding what open-to-work and contact settings to show. Trigger even when they only say "my profile" or "a post about the game" and the platform is LinkedIn in context.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# LinkedIn

LinkedIn has no write API for a personal profile, so this skill produces **paste-ready text**, section by section, each within the platform's limit, and keeps a record of what is live so the next change starts from the truth. It is the public counterpart of the cv-builder skill and obeys the same three principles:

1. **Never lie.** Every claim comes from `<workspace>/_private/candidate_profile_<name>.md` (schema in the cv-builder skill's `05-profile-schema.md`). Skills appear only at `production` or `working` depth; numbers only from `verified metrics`; nothing under `## Not claimable`. A profile is read by future colleagues, so overclaiming costs more here than on a CV.
2. **Lead with the strongest proof.** The headline and the first two lines of About carry the top proof points of the `### General` positioning profile, because LinkedIn shows one profile to every audience. The user may pick another positioning profile for a specific push.
3. **Written for people.** The humanization checklist in the cv-builder skill (`02-humanization-checklist.md`) applies to every section, post and message. First person, plain sentences, one idea per paragraph.

Limits, section rules and post patterns are in [references/sections.md](references/sections.md) and [references/posts.md](references/posts.md). Read the one you need.

## Requires the cvkit repo

This skill is text only, but it reads files that live in the cvkit repo. `<cvkit>` below is the root of a clone of `https://github.com/mtejedorg/cvkit` (or a fork). Locate it at the start of every run: the current directory if it holds `privacy_check.py` and `cvtool/`, else the folder the `CVKIT_HOME` environment variable names, else ask the user (offer `git clone`, and wait for a yes).

| What | Path |
|---|---|
| Profile schema, depth levels | `<cvkit>/.claude/skills/cv-builder/05-profile-schema.md` |
| Humanization checklist | `<cvkit>/.claude/skills/cv-builder/02-humanization-checklist.md` |
| Persona panel rules | `<cvkit>/.claude/skills/cv-builder/06-persona-review.md` |
| Generic personas | `<cvkit>/templates/personas/` |
| Privacy scan | `python <cvkit>/privacy_check.py` |

## Reading and editing the live profile

LinkedIn has no personal-profile API, so the skill works through a browser, and the user never copies text by hand:

1. Open the user's public profile URL (from `## Identity`) in the built-in browser pane. If LinkedIn asks for a login, stop and ask the user to sign in themselves in the pane; the skill never types credentials.
2. Read the sections from the page (headline, About, each experience entry, skills, featured, education, contact info) with the page-reading tools, expanding "see more" where needed, and write them to `live.md` with today's date. That is the seed for `audit`.
3. Editing stays with the user by default: the skill produces the approved text and the user pastes it. Only when the user explicitly asks the skill to apply an edit in the browser does it open the section's edit dialog, fill the approved text, show the result, and wait for a yes before saving. One section per approval; never a bulk save.
4. Settings (open-to-work, contact visibility) are read the same way and changed only on an explicit per-setting yes.

If the browser pane is unavailable, fall back to a LinkedIn data export (Settings → Data privacy → "Get a copy of your data") that the user provides.

## Workspace files

- `<workspace>/_private/linkedin/live.md`: the text currently on the profile, one `## Section` per LinkedIn section, with a `last pasted:` date. Seed it from the user's pasted sections or a LinkedIn data export; if absent, `audit` asks for it. Only the user confirms a paste; the skill never marks something live on its own.
- `<workspace>/_generated/LinkedIn/<YYYY-MM-DD>/`: proposed sections, one file each, plus `CHANGES.md` (what differs from live and why).
- `<workspace>/_generated/LinkedIn/posts/` and `.../messages/`: drafts, dated and slugged.

## Commands

- **audit**: compare `live.md` with the profile. Flag any live claim the profile does not back, numbers not in `verified metrics`, banned phrases, sections over limit, and missing proof points. Then run the **persona panel** with every persona whose `reviews` lists `linkedin` (generic ones in `<cvkit>/templates/personas/`, the user's in `<workspace>/_private/personas/`), per the cv-builder skill's `06-persona-review.md`: a LinkedIn profile is read by every kind of reader, so all of them join. Output a table: section, finding, persona(s), fix. Nothing is rewritten yet.
- **sync**: rewrite the sections that `audit` flagged (or all, on request) within limits, from the chosen positioning profile. Each section goes to its own file with a character count line at the top. `CHANGES.md` lists old and new per section. Ask before touching a section the user wrote in a voice they like; the profile owner's phrasing beats the skill's.
- **post**: draft a post from a source the user names: a project manifest (`portfolio.json`), a repo README, a CV folder, an event. Three variants with different hooks, each with its character count, a suggested real image (a capture, never generated), and the facts it relies on with their source. See `references/posts.md`.
- **message**: a reply to a recruiter, a connection note, a follow-up after applying, or a thank-you after an interview. Short, specific, one ask. The connection note respects the 300-character cap. Never includes the phone number unless the user says to.
- **settings**: recommend the open-to-work visibility, the contact-info exposure and the featured items from the profile's `## Languages and mobility` and `## Preferences` (phone off, email to connections only, a public generic CV only if a `_public.pdf` exists). Output a checklist for the user to click through.

## Workflow for `sync` and `post`

1. Resolve the workspace (same order as cv-builder: `CV_WORKSPACE`, `cvkit.config.json` in the root of `<cvkit>`, `<cvkit>` itself). Read the profile in full and `live.md` if present.
2. Draft. Keep each section under its limit with a safety margin of about five percent; the editor counts differently from a text file.
3. Humanization pass, style only.
4. Truth gate: every sentence traceable to the profile (or, for a post, to the named source). A claim without a source is a question for the user, asked in one `AskUserQuestion`, and the answer is written back to the profile the way cv-builder's Phase 7 does.
4b. Persona panel on the drafted sections or post (all personas whose `reviews` lists `linkedin`); shared findings become edits, single-persona findings are reported as trade-offs. Facts never change here.
5. Write the files, show the character counts and the diff against live, and stop. Pasting is the user's step. When they confirm, update `live.md` with the pasted text and the date.

## Approval model

Nothing on LinkedIn changes without the user pasting it, so the skill's job is to make every decision explicit before that moment. Mechanical steps run without asking: reading the profile and `live.md`, counting characters, checking limits, running the humanization and truth checks, running the persona panel. Everything else is shown and done only on a yes: which sections to rewrite, each rewritten section, each post variant chosen, each message, each settings recommendation, and the update of `live.md` after a paste. `settings` asks the user for open-to-work visibility, contact exposure and featured items the first time, then stores the answers under the profile's `## Preferences` (`linkedin open-to-work:`, `linkedin language:`) and uses them without re-asking until the user changes them.

## Boundaries

- Never fabricate engagement, follower counts, endorsements or recommendations. Recommendation requests are drafted as messages to a named person the user chooses.
- No hashtag stuffing, no engagement bait ("agree?", "comment YES"), no emoji walls. At most three hashtags, none required.
- Do not post, message or change settings through a browser on the user's behalf unless the user explicitly asks in that session; even then, show the final text and wait for a yes.
