# Drafter/Reviewer Workflow

After drafting (Phase 2) and the humanization pass (Phase 3), get a second opinion from a reviewer with no memory of the drafting. The pattern comes from the open-source `ai-job-search` project by Mads Lorentzen: a second agent, spawned with a fresh context, critiques the drafts.

## How to spawn it

Use the `Task` tool with a general-purpose subagent (default model; no model override). Hand it, inline in the prompt:

- The job description, verbatim.
- The drafted CV, cover letter and project portfolio Markdown, post-humanization.
- The profile sections this posting drew on: the chosen `### <Family>` positioning profile, the three proof points, the relevant Experience/Project entries and Skills rows. Not the whole file.
- The length budget from `01-structure-and-style.md` section B and the banned-phrase list from `02-humanization-checklist.md`.
- The ATS score from Phase 5 if already computed, or ask it to hold off.

Ask for a structured critique with these headings:

1. **Missed keywords.** JD terms the profile supports that the draft did not surface, with the profile line that supports each.
2. **Proof-point placement.** Are the three proof points in the summary and bullets 1–3? Is anything stronger buried lower?
3. **Weak or generic framing.** True claims stated vaguely when the profile holds a more specific version.
4. **Length and density.** Anything over budget; bullets over 30 words; more numbers than the profile's `metrics:` preference allows.
5. **Residual AI tells.** Anything the humanization checklist would flag.
6. **Consistency.** The same fact phrased two ways across CV, letter and portfolio.

Tell the reviewer explicitly: it reviews, it does not research the company and it does not propose anything about the candidate that is not in the excerpt it was given.

## Applying the critique

1. Apply changes that improve targeting, clarity or length without changing facts.
2. A suggestion that adds a claim not in the profile is a gap: ask the user (Phase 1 rule), and add the answer to the Phase 7 list.
3. Re-run the humanization checklist on anything rewritten.
4. Proceed to Phase 5 on the final text.
