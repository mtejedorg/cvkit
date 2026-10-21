# Humanization Pass

A style-rewrite step that runs after drafting (Phase 3) and again after the reviewer's critique (Phase 4). It catches text that reads as generic or machine-written. It also applies to the generic CV and to any website or portfolio copy written from the profile.

## Hard constraint (read this first)

**This is a style-only pass. No fact, claim, number, date, title or meaning may change.** Humanizing is about *how* something true is said, never about *what* is said. If a rewrite would need to add, remove or soften a factual claim to sound natural, do not make it: flag it as a Phase 1 question instead.

## Why this is not a detector-evasion pipeline

Some humanizer tools push text through chains of machine translation to fool AI-content detectors. That was rejected here: nobody scans a CV for detector signals (a recruiter or a text parser reads it), and every extra hop risks drifting a tool name, a metric or a date in a document where each claim must stay true. This pass exists so the text reads like a person wrote it, not to hide that AI helped.

## Checklist

- [ ] **Banned stock phrases.** None of: "proven track record", "extensive background", "delve", "testament", "orchestrated", "aligns perfectly", "leverage" (as a verb), "seamless", "seamlessly", "robust solution", "cutting-edge" (unless the JD uses it), "in today's fast-paced world", "passionate about", "results-driven", "dynamic professional", "synergy", "game-changer", "unlock the potential", "pioneering", "high-performance" (as a self-description), "spearheaded", "utilize", "best-in-class", "world-class", "state-of-the-art", "visionary".
- [ ] **Opening-verb rhythm.** Consecutive bullets under one role do not start with the same verb or pattern.
- [ ] **Sentence length varies.** Summaries and letter paragraphs mix short and long sentences.
- [ ] **Connectors.** At most one of "moreover", "furthermore", "additionally", "in addition" per document; none is better.
- [ ] **Em-dashes.** At most two per document; a period or comma usually does the job.
- [ ] **Sentence shape varies.** Not every sentence is subject-verb-object; some lead with the outcome or the method.
- [ ] **Adjective stacks.** No run of two or more evaluative adjectives ("innovative, scalable, high-impact").
- [ ] **Intensifiers.** No "truly", "deeply", "incredibly", "highly" unless a fact needs it.
- [ ] **Specific over abstract.** "Rebuilt the UI as a data-driven system edited from a CMS" beats "delivered scalable UI solutions".

## Process

1. Read the full text once, looking only for the patterns above. Do it as a separate pass, not while drafting.
2. Rewrite flagged spots for natural variation, preserving every fact exactly.
3. If a factual question comes up ("was it really 8 engineers, or would 'a small team' be truer?"), that is a Phase 1 question. Ask; do not quietly make a claim vaguer or stronger.
