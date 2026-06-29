# Security Policy

Arbiter is a **clean-room reference implementation**, not a deployed service. It runs
locally on synthetic example data, ships no secrets, and makes no network calls. The
attack surface is correspondingly small — but security reports are still welcome.

## Reporting a vulnerability

If you find a security issue (for example, an injection or unsafe-deserialization path
in the engine, or a dependency advisory), please report it privately via GitHub's
[security advisory](https://github.com/SaintlyDrew/arbiter/security/advisories/new)
flow rather than opening a public issue. I aim to acknowledge within a few days.

## Scope notes

- The engine reads local CSV/JSON/JSONL fixtures and writes local JSONL/SQLite. It uses
  parameterized SQL and the standard-library `json`/`csv` parsers — no `eval`, `pickle`,
  `subprocess`, or untrusted-input deserialization.
- The sample data under `examples/**/data/` is entirely **synthetic** — no real persons,
  accounts, or PII.
- This is a portfolio/reference project; there is no production deployment, SLA, or
  managed credential surface.
