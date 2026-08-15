# Resume & interview talking points

## One-line project title

**Secure SDLC Demo (Flask)** — end-to-end AppSec gates with Semgrep, Gitleaks, Trivy, and SBOM publishing.

## Resume bullets (pick 1–2)

- Built a Flask demo application with a GitHub Actions Secure SDLC pipeline enforcing secret scanning (Gitleaks), SAST (Semgrep), SCA/container scanning (Trivy), and CycloneDX SBOM generation on every PR.
- Implemented secure coding fixes for SQL injection, XSS-prone patterns, hardcoded secrets, and non-root containers; documented waiver policy with owner/expiry similar to commercial SCA exception workflows.
- Created an intentional vulnerable lab alongside the secure baseline to demonstrate scanner findings and remediation, strengthening hands-on AppSec skills beyond dashboard triage.

## Skills to list

`Secure SDLC` · `SAST` · `SCA` · `SBOM` · `Semgrep` · `Trivy` · `Gitleaks` · `GitHub Actions` · `Docker` · `Flask` · `Python` · `Threat modeling`

## Interview answers (short)

**Q: What did you build?**  
A small notes web app plus automated security gates that fail PRs on high-risk secrets, code issues, vulnerable deps, and risky images, and publish an SBOM.

**Q: How is this different from just running Wiz/Black Duck at work?**  
At work I often consume findings. Here I owned the application code, the CI policy, the remediations, and the exception process end-to-end.

**Q: Walk me through a finding.**  
Example: Semgrep flags string-built SQL → I switch to parameterized queries → add/adjust a unit test → PR re-runs → gate passes. If I must waive, I record ID/reason/owner/expiry in `suppressions.md`.

**Q: What’s an SBOM?**  
A software bill of materials — an inventory of components in what you shipped, used for vulnerability response and compliance.

## LinkedIn post starter

> I built a hands-on Secure SDLC project to go beyond scanner dashboards: a Flask app protected by Gitleaks + Semgrep + Trivy, with a broken lab for practice and a secure baseline that publishes an SBOM. Happy to share what’s in the repo if you’re learning AppSec too.
