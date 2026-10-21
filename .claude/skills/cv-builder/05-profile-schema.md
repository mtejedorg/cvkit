# Candidate Profile Schema

The profile is the only thing the skill is allowed to believe. This file defines its shape so that every phase can find what it needs by section name, and so that "can I claim X?" is answered by the profile itself instead of by a guess.

A blank, commented copy lives at [`templates/candidate_profile_template.md`](../../../templates/candidate_profile_template.md). Copy it to `<workspace>/_private/candidate_profile_<your-name>.md`.

## Sections (the headings are a contract)

| # | Heading | Holds |
|---|---|---|
| 1 | `## Identity` | Name, location, email, phone, links, citizenship, photo path. The phone goes in a `<span class="private">` in every generated header. |
| 2 | `## Positioning profiles` | One `### <Family>` per role family you apply to (e.g. Backend, Platform, Engineering Management, plus `### General` for the generic CV). Each has: `headline`, a 50–70 word `summary`, `flagship skill`, `leading proof points` (three, by number from section 3), `photo` (default per region or always/never), `metrics` (how many numbers, see Preferences). |
| 3 | `## Proof points` | A ranked list of the strongest, verifiable claims. Each line: `N. <claim> — evidence: <what proves it> — year: <YYYY> — serves: <families>`. The summary's first sentence and bullets 1–3 of the main role may only use claims from here. |
| 4 | `## Experience` | `### <Title> \| <Company> \| <Mon YYYY – Mon YYYY> \| <City, Country>`, then: `context` (two lines on the company and your scope), `responsibilities`, `systems built`, `verified metrics` (each: value, what it measured, how it was confirmed, date confirmed), `team` (size, whether you hired, who you reported to). Gaps in employment get their own entry (e.g. `### Independent Developer`) rather than silence. |
| 5 | `## Projects` | Same shape as Experience plus `status: shipped \| in development \| academic \| abandoned` and `years`. Personal, open-source and academic work. |
| 6 | `## Skills` | One row per skill: `- <Skill>: <depth> — <one-line note>`. Depth levels are defined below. Group rows under `###` subheadings freely; the depth is what matters. |
| 7 | `## Education` | Degree, institution, city, dates, and anything claimable from it (capstone, relevant coursework with its own depth level). |
| 8 | `## Languages and mobility` | Spoken languages with level; citizenship/work permits; remote/hybrid/on-site preference; travel and relocation willingness; a `rule` line if you want the skill to hold location back (e.g. "do not lead with location"). |
| 9 | `## Deal-breakers` | Hard constraints. Phase 1 reports a conflict between the posting and this section before anything else. |
| 10 | `## Not claimable` | Dated entries: `- <item> — confirmed <YYYY-MM-DD> (<posting>) — "<your words>"`. The skill never claims these and never asks about them again unless you reopen them. |
| 11 | `## STAR stories` | `### <Title>` with `Situation`, `Task`, `Action`, `Result` lines and `status: confirmed \| draft`. Drafts are proposals the skill wrote from facts above; it must not use a draft in interview prep without saying it is unconfirmed. |
| 12 | `## Preferences` | `metrics:` (e.g. "at most two percentages and two counts per CV"), `tone:` notes, `language:` of output, `name format:`, `photo:` overrides, anything about how you like your documents. |
| 13 | `## Open questions` | Facts the skill found in old documents but could not verify. Phase 1 asks about any of these the posting would touch. |

## Depth levels (section 6)

| Depth | Meaning | How the skill may word it |
|---|---|---|
| `production` | Shipped it, owned it, could be interviewed on it in depth | As experience: "built", "owned", "shipped" |
| `working` | Used it regularly but did not own it, or used it for a limited scope | "experience with", "worked with", or state the scope |
| `academic` | Coursework or a student project only | Must say "academic" or name the course/project |
| `evaluated` | Tried, benchmarked or compared it; no delivery | "evaluated", "tested", "prototyped with" |
| `supervised` | Reviewed or managed others' work in it; did not write it | "supervised", "reviewed" |

A posting item is a **gap** when the profile has no row for it, or only a row at `academic`, `evaluated` or `supervised` depth. Every gap is a Phase 1 question, however small.

## Rules the schema enforces

1. **Numbers live in one place.** A metric is claimable only if it appears under `verified metrics` of an Experience or Project entry, with how it was confirmed. Anything else is a question.
2. **Proof points lead.** Summaries and the first bullets draw from section 3. If a posting needs a proof point that is not there, the skill asks whether one exists instead of promoting a weaker claim.
3. **Positioning is explicit.** Phase 1 names which `### <Family>` profile it is using. If none fits, it proposes one and asks.
4. **The profile learns.** Phase 7 writes every answer back into the matching section, in the user's words. "No" goes to section 10; "yes, but only X" goes to section 6 at the right depth with the scope in the note.
5. **Nothing is inferred upward.** "Used it once in a tutorial" is `academic`, not `working`. The skill shows the exact lines it adds.
