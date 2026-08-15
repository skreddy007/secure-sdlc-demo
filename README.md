# Secure SDLC Demo — Team Notes

A beginner-friendly **AppSec / Secure SDLC** portfolio project.

You build a tiny Flask notes app, then protect it with the same *kinds* of controls used in industry:

| Gate | Tool | What it catches |
|------|------|-----------------|
| Secrets | Gitleaks | API keys / passwords committed to git |
| SAST | Semgrep | Risky code patterns (SQLi, XSS, debug mode) |
| SCA | Trivy (filesystem) | Vulnerable libraries |
| Container | Trivy (image) | Bad base images / root user issues |
| SBOM | Trivy CycloneDX | Inventory of what you shipped |

**Two trees in this repo**

- `app/` — **secure** version (resume demo, CI must pass)
- `learning/broken_app/` — **intentionally vulnerable** lab (practice seeing scanners fail)

Git activity for this repo is posted to Slack `#secure-sdlc-git-updates`.

---

## Start here (beginners)

Follow **[docs/LEARNING_PATH.md](docs/LEARNING_PATH.md)** step by step.

Supporting docs:

- [SDLC walkthrough](docs/sdlc-walkthrough.md) — the big picture
- [Before / after fixes](docs/before-after.md) — vulnerable vs secure code
- [Threat model](docs/threat-model.md) — what we protect and why
- [Resume talking points](docs/resume-talking-points.md) — how to describe this on a CV / interview

---

## Quick start (secure app)

### 1. Create a virtual environment

```powershell
cd D:\PersonalProjects\secure-sdlc-demo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Run locally

```powershell
copy .env.example .env
$env:SECRET_KEY = "local-dev-only"
python -m app.main
```

Open http://127.0.0.1:5000

### 3. Run tests

```powershell
pytest -q
```

### 4. Docker (optional)

```powershell
docker build -t secure-sdlc-demo .
docker run --rm -p 5000:5000 -e SECRET_KEY=local-dev-only secure-sdlc-demo
```

---

## What “Secure SDLC” means here

```text
Write code → open PR → automated security gates → fail or pass
                              ↓
                    fix or document waiver
                              ↓
                         merge / release + SBOM
```

This mirrors workflows you see with tools like Black Duck, Veracode, Harbor, and Wiz — except **you own the app and the gate**.

---

## Project layout

```text
app/                     Secure Flask application
learning/broken_app/     Vulnerable lab (excluded from main CI)
security/                Policies, suppressions, scanner configs
.github/workflows/       CI security gates
docs/                    Learning guides for your resume story
tests/                   Basic automated tests
```

---

## License

Personal portfolio / educational use.
