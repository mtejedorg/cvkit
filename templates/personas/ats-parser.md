---
name: Applicant tracking parser
slug: ats-parser
scope: generic
families: [all]
reviews: [cv]
---

## Who they are
Not a person: the parser inside an applicant tracking system. It extracts name, contact, titles, employers, dates, skills and education into fields, then ranks by how many of the posting's terms appear. It has no judgement and no patience. Everything it cannot parse does not exist.

## What they look for in the first thirty seconds
- Contact details as plain text near the top.
- Section headings it recognises: Summary, Experience, Skills, Education.
- One role per block: title, employer, dates in a consistent format.
- The posting's terms, spelled the way the posting spells them.

## What makes them stop reading
- Text inside images, tables or multi-column layouts.
- Headings with creative names it has no field for.
- Dates in three different formats.
- Skills only implied by prose and never named.

## Questions they ask themselves
- Which field does this line go into?
- How many of the required terms did I find, and where?

## Known biases
- Rewards repetition of keywords, which a human reader punishes. The panel must not let this persona push the text toward stuffing; it only checks that each genuinely supported term appears once, in the posting's wording.
