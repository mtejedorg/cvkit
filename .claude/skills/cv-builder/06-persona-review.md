# Persona review

A document that is true and well written can still fail with the person who reads it, because every reader screens for something different. A recruiter scans for the title, the years and the location in ten seconds. A hiring lead for a gameplay team looks for shipped work and asks "would I want this person debugging next to me". A head of AI engineering wants to see that the assistant reached production and how it was evaluated. Persona review puts the draft in front of those readers before the real ones see it.

Personas are files, not a skill. All three skills (cv-builder, portfolio, linkedin) run the same panel; the difference is which personas join.

## Where personas live

| Location | Scope | Who writes them |
|---|---|---|
| `templates/personas/` in cvkit | Generic readers every candidate meets: the recruiter screener, the applicant tracking parser, the hiring manager with no domain stated. Fictional, safe to publish. | The repo. Copy, do not edit in place. |
| `<workspace>/_private/personas/` | Readers specific to the role families the user targets: the people who would actually hire them. They encode what the user wants, so they stay private, like the profile. | The user, with the `create persona` command below. |

Both folders are read on every panel. A private persona with the same `slug` as a generic one replaces it.

## Persona file format

```markdown
---
name: Lead gameplay programmer hiring for a mobile studio
slug: mobile-gameplay-lead
scope: private
families: [Gameplay & Mobile]
reviews: [cv, cover-letter, project-portfolio, portfolio-site, linkedin]
seniority: [senior, lead]
---

## Who they are
Two or three sentences: their role, what their team ships, how many CVs they see a week, how long they spend on one.

## What they look for in the first thirty seconds
A short list of concrete signals. "Shipped a game on a store I can open." "A number I believe."

## What makes them stop reading
A short list. "A summary that says 'results-driven'." "Ten technologies and no outcome." "A phone number I did not ask for" (for public pages).

## Questions they ask themselves
Three to five questions the document must answer for them, in their words.

## Known biases
What they over- or under-weight, so the panel can discount it. "Discounts XR experience unless it names the platform and the frame rate."
```

`families` uses the names of the profile's `### <Family>` positioning profiles. `reviews` lists which artifacts the persona should look at. `seniority` is optional and matches the posting's level when known.

## Which personas join a panel

- **cv-builder (Phase 4):** the generic screener and parser always; private personas whose `families` include the positioning profile chosen in Phase 1 and whose `reviews` include the artifact; if `seniority` is set, it must include the posting's band. Cap at four. A CV for one posting has one reader in mind, so a persona from another family only adds noise.
- **portfolio (`check`, and `sync` before the final report) and linkedin (`audit`, `sync`, `post`):** every persona whose `reviews` lists the artifact, generic and private. These artifacts face everyone at once, so the panel must include everyone the user wants to reach.

## How the panel runs

1. For each persona, a fresh-context reviewer (a subagent with the `Task` tool, default model; sequential passes when subagents are unavailable) receives: the persona file verbatim, the artifact, and for a CV the posting. Nothing else, so it reads the way that person would: without the profile, without the drafting history.
2. It answers in this shape, in the persona's voice, under 250 words:
   - **First impression** (one sentence, after thirty seconds).
   - **Would I keep reading? Why or why not.**
   - **Three things I needed and did not find, or found too late.**
   - **Three concrete edits** (which line, what change).
3. The drafter collects the answers into a table: persona × finding. Findings that two or more personas share become edits. Findings from one persona are applied when they cost nothing to the others, otherwise reported to the user as a trade-off. An edit never changes a fact; a persona asking for a claim the profile lacks turns into a Phase 1 question.
4. After the edits, re-run the humanization checklist on the changed lines.
5. The report to the user lists the panel, the table, what was applied and what was left as a trade-off.

## Creating a persona (`create persona`)

Any of the three skills accepts "create a persona for `<role or company type>`". The skill:

1. Reads the profile's positioning profiles and the postings in `applications_log.md` for that family, to ground the persona in the roles the user actually applies to.
2. Drafts the file in the format above, with the `scope: private` header, and shows it.
3. Asks two questions at most: what this reader cares about most, and what makes them discard a candidate. The user's answers go in verbatim.
4. Writes it to `<workspace>/_private/personas/<slug>.md`. Never to the public repo.

Personas drift like profiles do; when an application outcome contradicts a persona ("rejected: not enough mobile titles" while the persona said XR counts), update the persona in Phase 9 and say so.
