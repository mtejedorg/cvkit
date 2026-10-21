# Humanization Pass

A dedicated style-rewrite step that runs after drafting (Phase 3) and after the reviewer's critique (Phase 4), catching text that reads as generic or AI-generated. The anti-cliché list in `01-structure-and-style.md` section H alone wasn't enough in practice, so this checklist adds a concrete, repeatable pass on top of it.

## Hard constraint (read this first)

**This is a style-only pass. No fact, claim, number, date, title, or meaning may change.** Same spirit as the "ASK BEFORE LYING" rule in `01-structure-and-style.md` — humanizing is about *how* something true is said, never about *what* is said. If a rewrite would need to add, remove, or soften a factual claim to sound more natural, don't make that rewrite — flag it instead.

## Why this isn't a translation-chain / detector-evasion pipeline

Some humanizer tools work by rewriting text through a chain of translations (e.g. English → Chinese → Turkish → optionally Japanese → back to the original language) specifically to defeat AI-content detectors. That approach was considered and rejected for this project:
- It needs 2–3 paid external API keys for no benefit here — nothing is scanning these documents for "AI-detector" signals, they're read by a human recruiter or an ATS text parser.
- Multi-hop lossy translation risks drifting exact facts (a tool name, a metric, a date) in a document where every claim must stay verifiably true.

Humanizing a CV means "don't sound like a template," not "evade detection." Do it with a direct rewrite pass, in the original language, with the constraint above.

## Checklist

Re-read the drafted CV / cover letter / project portfolio text and check for:

- [ ] **Banned stock phrases** — none of: "proven track record", "extensive background", "delve", "testament", "orchestrated", "aligns perfectly", "leverage" (as a verb), "seamless", "seamlessly", "robust solution", "cutting-edge" (unless the JD itself uses it), "in today's fast-paced world", "passionate about", "results-driven", "dynamic professional", "synergy", "game-changer", "unlock the potential".
- [ ] **Bullet-opening-verb rhythm** — consecutive bullets under the same role don't all start with the same verb or verb pattern (e.g., not "Architected... / Architected... / Engineered..." back to back — vary it).
- [ ] **Sentence-length variety** — not every sentence in a paragraph (summary, cover letter body) is the same length/structure; mix short and long.
- [ ] **Overused connectors** — no more than one of "moreover", "furthermore", "additionally", "in addition" per document; prefer no connector at all where the logic is already clear from context.
- [ ] **Em-dash overuse** — no more than 1-2 per document; most of what an em-dash does can be a period or comma instead.
- [ ] **Varied sentence structure** — not every sentence follows the same subject-verb-object shape; some can lead with the outcome, some with the method.

## Process

1. After drafting (Phase 3) and again after incorporating reviewer feedback (end of Phase 4), read the full text once specifically looking for the above patterns — not while drafting, as a separate pass.
2. Rewrite flagged spots for natural variation, preserving every fact exactly.
3. If a fact-checking question comes up during this pass (e.g., "was it really 8 engineers or would 'a small team' read better and is it still true?"), that's a Phase 1 question, not a humanization edit — ask the user rather than quietly rewording a factual claim into vaguer language.
