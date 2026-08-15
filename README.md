# Secure SDLC Demo

A small Flask **Team Notes** app plus GitHub Actions **security gates**.  
Portfolio project: own the app *and* the scan/fix/waive loop (SAST, SCA, secrets, container, SBOM).

| If you want… | Open |
|--------------|------|
| What this is, what shipped, interviews | [docs/PROJECT.md](docs/PROJECT.md) |
| How to learn the vulns and scanners | [docs/LEARNING.md](docs/LEARNING.md) |

Live repo: https://github.com/skreddy007/secure-sdlc-demo

---

## What is in this repo

| Path | Role |
|------|------|
| `app/` | Secure app (CI must pass) |
| `learning/broken_app/` | Intentional vulnerable lab (excluded from CI) |
| `security/` | Scanner policy and waiver register |
| `.github/workflows/security.yml` | Gates: Gitleaks, Semgrep, Trivy, SBOM, tests |
| `docs/PROJECT.md` | Work record |
| `docs/LEARNING.md` | Study guide |

---

## Run locally (Windows)

If `Activate.ps1` is blocked, call the venv Python directly:

```powershell
cd D:\PersonalProjects\secure-sdlc-demo
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:SECRET_KEY = "local-dev-only"
.\.venv\Scripts\python.exe -m app.main
```

`$env:SECRET_KEY` sets a variable **in this terminal only**. It does not edit `.env`.  
Open http://127.0.0.1:5000

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Docker:

```powershell
docker build -t secure-sdlc-demo .
docker run --rm -p 5000:5000 -e SECRET_KEY=local-dev-only secure-sdlc-demo
```

---

## License

Personal portfolio / educational use. Do not store real personal data in this app.
