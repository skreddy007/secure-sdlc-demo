# Security suppressions / exceptions

Use this file like a real waiver register (Black Duck / Veracode style).

## Rules

1. Prefer **fix** over suppress.
2. Every suppress needs: finding ID, tool, reason, owner, expiry.
3. Expired entries must be re-reviewed or removed.
4. Never suppress secrets — rotate and remove them.

## Active suppressions

| ID | Tool | Reason | Owner | Expiry | Status |
|----|------|--------|-------|--------|--------|
| _(none)_ | — | — | — | — | — |

## Closed examples (learning)

| ID | Tool | Reason | Outcome |
|----|------|--------|---------|
| Hardcoded `sk_live_...` | Gitleaks | Was a planted lab secret in early draft | Moved to `learning/broken_app/` and removed from `app/` |
| SQL string concat search | Semgrep | Planted SQLi | Replaced with parameterized `?` placeholders |
| Flask `debug=True` | Semgrep | Planted misconfig | Gated by env var; default off |
