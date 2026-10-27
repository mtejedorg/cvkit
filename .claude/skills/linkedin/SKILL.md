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

## Workspace files

- `<workspace>/_private/linkedin/live.md`: the text currently on the profile, one `## Section` per LinkedIn section, with a `last pasted:` date. Seed it from the user's pasted sections or a LinkedIn data export; if absent, `audit` asks for it. Only the user confirms a paste; the skill never marks something live on its own.
- `<workspace>/_generated/LinkedIn/<YYYY-MM-DD>/`: proposed sections, one file each, plus `CHANGES.md` (what differs from live and why).
- `<workspace>/_generated/LinkedIn/posts/` and `.../messages/`: drafts, dated and slugged.

## Commands

- **audit**: compare `live.md` with the profile. Flag any live claim the profile does not back, numbers not in `verified metrics`, banned phrases, sections over limit, and missing proof points. Output a table: section, finding, fix. Nothing is rewritten yet.
- **sync**: rewrite the sections that `audit` flagged (or all, on request) within limits, from the chosen positioning profile. Each section goes to its own file with a character count line at the top. `CHANGES.md` lists old and new per section. Ask before touching a section the user wrote in a voice they like; the profile owner's phrasing beats the skill's.
- **post**: draft a post from a source the user names: a project manifest (`portfolio.json`), a repo README, a CV folder, an event. Three variants with different hooks, each with its character count, a suggested real image (a capture, never generated), and the facts it relies on with their source. See `references/posts.md`.
- **message**: a reply to a recruiter, a connection note, a follow-up after applying, or a thank-you after an interview. Short, specific, one ask. The connection note respects the 300-character cap. Never includes the phone number unless the user says to.
- **settings**: recommend the open-to-work visibility, the contact-info exposure and the featured items from the profile's `## Languages and mobility` and `## Preferences` (phone off, email to connections only, a public generic CV only if a `_public.pdf` exists). Output a checklist for the user to click through.

## Workflow for `sync` and `post`

1. Resolve the workspace (same order as cv-builder: `CV_WORKSPACE`, `cvkit.config.json`, repo). Read the profile in full and `live.md` if present.
2. Draft. Keep each section under its limit with a safety margin of about five percent; the editor counts differently from a text file.
3. Humanization pass, style only.
4. Truth gate: every sentence traceable to the profile (or, for a post, to the named source). A claim without a source is a question for the user, asked in one `AskUserQuestion`, and the answer is written back to the profile the way cv-builder's Phase 7 does.
5. Write the files, show the character counts and the diff against live, and stop. Pasting is the user's step. When they confirm, update `live.md` with the pasted text and the date.

## Boundaries

- Never fabricate engagement, follower counts, endorsements or recommendations. Recommendation requests are drafted as messages to a named person the user chooses.
- No hashtag stuffing, no engagement bait ("agree?", "comment YES"), no emoji walls. At most three hashtags, none required.
- Do not post, message or change settings through a browser on the user's behalf unless the user explicitly asks in that session; even then, show the final text and wait for a yes.
