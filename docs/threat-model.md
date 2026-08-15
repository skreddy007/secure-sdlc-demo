# Threat model (lightweight)

This is a **beginner threat model** — short enough to put in a portfolio, serious enough to discuss in interviews.

## 1. What we are protecting

| Asset | Why it matters |
|-------|----------------|
| Note contents | User/business data confidentiality & integrity |
| `SECRET_KEY` / any API keys | Session trust and credential theft |
| Database file | Persistence of notes |
| CI/CD pipeline | Supply-chain trust (poisoned build = poisoned app) |
| Container image | Runtime trust in whatever you deploy |

## 2. Trust boundaries

```text
[ Browser ]  --HTTP-->  [ Flask app ]  --SQL-->  [ SQLite file ]
     ^                       ^
     |                       |
 attacker user          compromised host / malicious package
```

Also: **developer laptop → git → GitHub Actions → image artifact**.

## 3. Top risks (STRIDE-ish, plain language)

| Risk | Example | Mitigations in this repo |
|------|---------|--------------------------|
| Spoofing | Steal session via leaked secret | Env-based `SECRET_KEY`, Gitleaks |
| Tampering | Change notes via SQLi | Parameterized SQL, Semgrep |
| Repudiation | (light) unclear who changed what | Keep git history; extend with auth later |
| Information disclosure | Debug pages, XSS | debug off, escaped templates |
| Denial of service | (not deeply covered) | Keep app tiny; stretch: rate limits |
| Elevation of privilege | Root container escape | Non-root `USER` in Dockerfile |

## 4. Out of scope for v1

- Full authentication/authorization (IAM/Okta)
- Multi-tenant isolation
- Formal penetration test
- Production cloud hardening (WAF, private networking)

## 5. Residual risk statement

This is an educational portfolio app. Residual risk is accepted for local/demo use. Do not store real personal data in it.
