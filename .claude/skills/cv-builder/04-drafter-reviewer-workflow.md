# Drafter/Reviewer Workflow

After drafting (Phase 2) and the humanization pass (Phase 3), spawn a second opinion before finalizing. Inspired by the reviewer-agent pattern in the open-source `ai-job-search` project by Mads Lorentzen: "a second Claude agent, spawned with a fresh context, researches the company and critiques the drafts."

## How to spawn it

Use the `Task` tool with a general-purpose subagent. No dedicated `.claude/agents/*.md` file is needed at this scope — one cohesive workflow doesn't need a named persistent agent definition, unlike `ai-job-search`'s multi-command surface.

**Hand it, inline in the prompt (a fresh subagent has no memory of this conversation):**
- The job description (verbatim).
- The drafted CV, Cover Letter, and Project Portfolio Markdown (verbatim, post-humanization).
- A short excerpt of your candidate profile — just the sections relevant to this JD (skills/experience it drew on), not the whole file.
- The ATS score from Phase 5, if already computed, or ask it to hold off until after its critique.

**Ask it to return a structured critique covering:**
- Missed keywords from the JD that the profile genuinely supports but the draft didn't surface.
- Weak or generic framing — claims that are true but stated vaguely when a more specific, JD-relevant framing exists in the profile.
- Any language that still reads as templated or AI-generated (a second pass at what `02-humanization-checklist.md` is meant to catch — catches what the first pass missed).
- Any factual inconsistency between the CV, Cover Letter, and Project Portfolio (e.g., different phrasing of the same metric that could look like two different numbers).

**Explicitly tell the reviewer subagent:** it is reviewing, not researching the company or fabricating anything about the candidate — it should ground every suggestion in the profile excerpt and JD text it was given, not invent additional context.

## Applying the critique

1. Read the reviewer's critique.
2. Apply changes that improve targeting/clarity without changing facts.
3. If the critique suggests adding a claim not present in your candidate profile, treat it like any other gap — ask the user (Phase 1's "ask before lying" rule applies here too, not just to the JD's own requirements), and add their answer to the Phase 7 write-back list.
4. Re-run the humanization checklist on anything the reviewer's suggestions changed, since a rewrite can reintroduce a cliché or awkward phrasing.
5. Proceed to Phase 5 (ATS Scoring) on the final text.
