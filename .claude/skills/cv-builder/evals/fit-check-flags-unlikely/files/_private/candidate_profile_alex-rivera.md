# Candidate Profile: <Your Name>

<!-- Copy this file to <workspace>/_private/candidate_profile_<your-name>.md and fill it in.
     The headings are a contract with the skill (see .claude/skills/cv-builder/05-profile-schema.md).
     Example lines use a fictional candidate, Alex Rivera. Replace them. -->

## Identity

- name: Alex Rivera
- location: Austin, TX, USA
- email: alex.rivera@example.com
- phone: +1 (555) 010-0142   <!-- only ever rendered inside <span class="private"> -->
- linkedin: linkedin.com/in/alexrivera
- github: github.com/alexrivera
- citizenship: US
- photo: _private/photo.jpg   <!-- optional; regional rules decide whether it is used -->

## Positioning profiles

### General
- headline: Senior backend engineer (Go, Python, AWS)
- summary: Go and Python backend engineer with 8 years of experience building payment and logistics services. Cut p95 API latency by 42% at a payments company and led its move from a monolith to services on AWS. Looking for a senior role where reliability and clear interfaces matter.
- flagship skill: Go
- leading proof points: 1, 2, 4
- photo: per region
- metrics: default

### Platform / SRE
- headline: Backend engineer who keeps services reliable
- summary: <50–70 words, written for this family>
- flagship skill: AWS (ECS, RDS)
- leading proof points: 2, 3, 5
- photo: per region
- metrics: default

## Proof points

1. Rebuilt a transaction-ledger API in Go and cut p95 latency 42% — evidence: before/after dashboards shared with the team, 2022 — serves: General, Platform
2. Led a monolith-to-services migration on AWS (6 services) — evidence: architecture docs, deploy time 50 → 9 min — year: 2023 — serves: General, Platform
3. Mentored 3 engineers, two promoted within 18 months — evidence: promotion dates — year: 2024 — serves: General
4. <claim> — evidence: <...> — year: <...> — serves: <...>

## Experience

### Senior Backend Engineer | Example Payments Inc. | Mar 2021 – Present | Austin, TX, USA
- context: Payments company, ~40 engineers; owned the ledger and settlement services.
- responsibilities: service design, on-call rotation, hiring loop.
- systems built: transaction-ledger API (Go), contract-test harness, canary release pipeline.
- verified metrics:
  - p95 latency 310 ms → 180 ms (42%) — measured on production dashboards — confirmed 2026-01-10
  - deploy time 50 min → 9 min — CI logs — confirmed 2026-01-10
- team: 6 engineers, reported to the Head of Platform; hired 2.

### Backend Engineer | Sample Logistics Co. | Jun 2017 – Feb 2021 | Dallas, TX, USA
- context: ...
- responsibilities: ...
- systems built: ...
- verified metrics: ...
- team: ...

## Projects

### Open Ledger | open source | 2020 – Present
- status: in development
- context: double-entry ledger library in Go.
- systems built: ...
- verified metrics: 1,200 GitHub stars — public repo — confirmed 2026-01-10

## Skills

<!-- depth: production | working | academic | evaluated | supervised -->

### Languages
- Go: production — primary language since 2019
- Python: production — services and tooling
- SQL: working — PostgreSQL queries and schema design; no DBA work

### Cloud and infrastructure
- AWS (ECS, RDS, S3, SQS): production
- Docker: production
- Kubernetes: evaluated — compared with ECS in 2023, never ran it in production
- Terraform: working — maintained existing modules

### Practices
- Contract testing: production
- Incident response: production — on-call rotation since 2021

## Education

- B.S. in Computer Science | Example State University, Austin, TX | 2011 – 2015
  - capstone: distributed key-value store with leader election (academic)
- Certificate in Site Reliability Engineering | Example Online Academy | 2019

## Languages and mobility

- English: native
- Spanish: professional
- work authorization: US citizen
- preference: hybrid or remote; on-site possible in Austin
- travel: up to one week per quarter
- rule: do not lead with location; discuss it once there is mutual interest

## Deal-breakers

- No relocation outside the US.
- No roles that are 100% on-site five days a week.

## Not claimable

- Kubernetes in production — confirmed 2026-03-14 (Northwind Labs posting) — "Only Docker and ECS, no Kubernetes."

## STAR stories

### Rollback storm
- Situation: ...
- Task: ...
- Action: ...
- Result: ...
- status: confirmed

## Preferences

- metrics: at most two percentages and two counts per CV; the rest in plain words
- tone: plain, specific, no stock phrases
- language: English unless the posting is in another language
- name format: Alex Rivera
- photo: never (US market)

## Open questions

- Exact month the ledger rewrite shipped (2022 or early 2023).
