<div class="cv-header">
  <div class="cv-header-text">
    <h1>Alex Rivera</h1>
    <p class="cv-contact">Austin, TX, USA · alex.rivera@example.com · <span class="private">+1 (555) 010-0142 · </span>linkedin.com/in/alexrivera · github.com/alexrivera</p>
  </div>
</div>

## Professional Summary

Go and Python backend engineer with 8 years of experience building payment and logistics services. Cut p95 API latency by 42% at a payments company and led its move from a monolith to services on AWS. Looking for a senior role where reliability and clear interfaces matter.

## Professional Experience

**Senior Backend Engineer** | Example Payments Inc. *(2021 – Present, Austin, TX)*

- Rebuilt the transaction-ledger API in Go, cutting p95 latency from 310 ms to 180 ms while the service absorbed 3x peak traffic.
- Split a Python monolith into 6 services on AWS (ECS, RDS PostgreSQL), reducing deploy time from 50 minutes to 9.
- Added contract tests and canary releases, which brought rollbacks down from 11 per quarter to 2.
- Mentored 3 engineers; two were promoted within 18 months.
- Wrote the on-call runbook used by 4 teams and cut median incident time from 40 to 15 minutes.
- Introduced structured logging and tracing across 6 services so every request can be followed end to end.
- Ran the quarterly load test and documented the capacity model the finance team uses for forecasting.

**Backend Engineer** | Sample Logistics Co. *(2017 – 2021, Dallas, TX)*

- Wrote route-planning services in Python that shortened average delivery estimates by 12%, using PostgreSQL window queries instead of an in-memory cache.
- Containerized 9 batch jobs with Docker, so any engineer could reproduce a failed run locally in minutes.
- Cut a nightly reporting job from 4 hours to 35 minutes by moving aggregation into the database.
- Built the driver-app sync endpoint that handled intermittent connectivity without duplicate deliveries.
- Paired weekly with the data team to keep the warehouse schema in step with the service models.
- Replaced a hand-rolled job scheduler with a documented cron layer and removed 2,000 lines of code.
- Added integration tests for every external carrier API, catching three breaking changes before release.

**Junior Developer** | Example Web Studio *(2015 – 2017, Houston, TX)*

- Built and maintained 12 client websites in Python and JavaScript.
- Set up the studio's first continuous integration pipeline.
- Wrote the internal style guide for Python code.
- Migrated client sites from shared hosting to containers.
- Handled support tickets and documented recurring fixes.
- Automated weekly backups and restore drills for every client.

## Additional Experience & Projects

**Open Ledger** | Personal project *(2020 – Present)*

- A double-entry ledger library in Go with 1,200 GitHub stars and 14 contributors.
- Maintains a public changelog and semantic versioning across 30 releases.
- Added fuzz tests that found two rounding bugs in the first week.

**Route Viz** | Hackathon winner *(2019)*

- Visualizes delivery routes on a map from a CSV export.
- Built in 24 hours with two teammates; still used by the logistics team.
- Ported to a browser build the following year.

## Core Competencies & Technical Skills

- **Languages:** Go, Python, SQL
- **Data & Cloud:** PostgreSQL, AWS (ECS, RDS, S3, SQS), Docker
- **Practices:** Contract testing, canary releases, code review, on-call incident response
- **Observability:** Structured logging, OpenTelemetry tracing, dashboards
- **Tooling:** Git, GitHub Actions, Terraform

## Education

**B.S. in Computer Science** | Example State University, Austin, TX *(2011 – 2015)*

Capstone: a distributed key-value store with leader election.

**Certificate in Site Reliability Engineering** | Example Online Academy *(2019)*

## Languages

- **English:** Native
- **Spanish:** Professional
