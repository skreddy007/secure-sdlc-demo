# Project record (work)

Read this if you come back later and need: *what was this, what did I ship, how do I talk about it.*

For the study path and vulnerable vs secure code, use [LEARNING.md](LEARNING.md).

---

## One-sentence summary

I built a Flask notes app and a GitHub Actions Secure SDLC pipeline that fails PRs on secrets, risky code, vulnerable dependencies, and risky images, then publishes a CycloneDX SBOM.

**Why:** At work I consume scanner findings (Wiz, Black Duck, Veracode, Harbor). This repo is the other seat — application code, CI policy, remediations, and waivers.

**GitHub:** https://github.com/skreddy007/secure-sdlc-demo  
**Slack:** `#secure-sdlc-git-updates` (GitHub app subscribe)

---

## What shipped

1. Secure Team Notes app (`app/`) — parameterized SQL, env-based secrets, escaped templates, debug off by default, non-root Docker user.
2. Security Gates workflow (`.github/workflows/security.yml`):
   - **Gitleaks** — committed secrets
   - **Semgrep** — SAST (`p/python`, `p/flask`, plus `security/semgrep.yml`)
   - **Trivy filesystem** — SCA on dependencies (CRITICAL/HIGH fails)
   - **Trivy image** — container vulns (CRITICAL/HIGH fails)
   - **SBOM** — CycloneDX artifact on the container job
   - **pytest**
3. Waiver process: `security/suppressions.md` (id, tool, reason, owner, expiry). Prefer fix over ignore.
4. Broken lab under `learning/` so scanners can be demonstrated without failing main CI.

Trivy Action is pinned by **commit SHA** (`v0.36.0`) so tags cannot be silently moved (relevant after the 2026 trivy-action tag compromise).

---

## How the loop works

```text
Write code → PR → gates → fail or pass
                 ↓
           fix or documented waiver
                 ↓
           merge + SBOM artifact
```

Policy: CRITICAL/HIGH fails. Secrets are never waived — rotate and remove.

| This repo | Enterprise cousins |
|-----------|--------------------|
| Semgrep | Veracode SAST, Checkmarx, Sonar |
| Trivy FS | Black Duck, Snyk, Wiz on dependencies |
| Trivy image / non-root | Harbor, Wiz container posture |
| Gitleaks | GitHub secret scanning |
| SBOM artifact | Compliance / customer inventory |
| `suppressions.md` | SCA/SAST waiver tickets |

---

## Threat model (short)

**Assets:** note data, `SECRET_KEY`, SQLite file, CI pipeline, container image.

**Boundaries:** browser → Flask → SQLite; laptop → git → Actions → image.

| Risk | Mitigation here |
|------|-----------------|
| Stolen secret / session | Env `SECRET_KEY`, Gitleaks |
| SQL injection | Parameterized queries, Semgrep |
| XSS | Jinja templates, no `|safe` on user text |
| Debug / info leak | `debug` off unless `FLASK_DEBUG=1` |
| Root container | `USER appuser` in Dockerfile |

**Out of scope:** real auth (Okta), multi-tenant, pentest, production cloud hardening.  
**Residual risk:** demo only; no real personal data.

---

## Resume

**Title:** Secure SDLC Demo (Flask) — Semgrep, Gitleaks, Trivy, SBOM.

**Bullet (pick one):**

- Built a Flask demo with GitHub Actions gates for secret scanning (Gitleaks), SAST (Semgrep), SCA/container scanning (Trivy), and CycloneDX SBOM on every PR.
- Implemented fixes for SQL injection, XSS-prone patterns, hardcoded secrets, and non-root containers; waivers require owner, reason, and expiry.

**Skills:** Secure SDLC, SAST, SCA, SBOM, Semgrep, Trivy, Gitleaks, GitHub Actions, Docker, Flask, Python, threat modeling.

**Interview:** At work I triage findings. Here I owned code, policy, fix, and exception. Example: Semgrep flags string-built SQL → parameterized query → test → gate passes. If waived: record in `suppressions.md`.

---

## Optional later upgrades

OIDC/Okta login, Dependabot, SARIF → GitHub code scanning, SOAR webhook on failed gates.
