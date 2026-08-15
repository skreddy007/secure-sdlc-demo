# Secure SDLC walkthrough

## The lifecycle (simple)

1. **Developer** writes code for a feature (here: notes create/search).
2. **Pull request** triggers automated checks.
3. **Security gates** look for classes of problems:
   - secrets in code
   - unsafe coding patterns (SAST)
   - vulnerable packages (SCA)
   - insecure container image
4. **Policy** decides fail vs warn (this repo: CRITICAL/HIGH fails).
5. **Remediation**: fix code/deps/image, or rare documented waiver.
6. **Release evidence**: tests pass + SBOM artifact uploaded.

That loop is “Secure SDLC.” Tools change (Veracode vs Semgrep, Black Duck vs Trivy); the loop does not.

---

## How this maps to enterprise tools you may already know

| This project | Enterprise cousins |
|--------------|--------------------|
| Semgrep | Veracode SAST, Checkmarx, Sonar security rules |
| Trivy FS | Black Duck, Snyk Open Source, Wiz vulnerability findings on deps |
| Trivy image / non-root | Harbor scanning, Wiz container posture |
| Gitleaks | GitHub secret scanning, TruffleHog |
| SBOM artifact | Customer/compliance software inventory requests |
| `suppressions.md` | Formal risk acceptance / waiver tickets |

---

## What “good” looks like on a PR

- Secrets job: green
- Semgrep: green (or only waived items listed)
- Trivy FS: no unfixed CRITICAL/HIGH (per policy)
- Image scan: green
- SBOM: produced even when you are not blocking on every medium finding
- Unit tests: green (security without tests is fragile)

---

## Common beginner mistakes

1. Ignoring findings because “it’s just a demo.”
2. Broad `.trivyignore` with no expiry.
3. Committing `.env` with real secrets.
4. Fixing a scanner alert by deleting the check instead of fixing the code.
5. Scanning only the secure app and never practicing on broken samples.

---

## Next upgrades (optional stretch)

- Add OIDC login (Okta) to practice secure authn
- Add Dependabot/Renovate for automated dependency PRs
- Convert Semgrep/Trivy outputs to SARIF and upload to GitHub code scanning
- Add a simple SOAR webhook that receives a failing gate summary JSON
