# Learning guide

Study path, vulnerable vs secure patterns, and how to run scanners on the lab.  
How to run the **secure** app: [README](../README.md). What shipped for work/resume: [PROJECT.md](PROJECT.md).

Flask is the sample product. The skill is the **Secure SDLC process**.

---

## Path (in order)

### 1. Orient

- Skim the README and `app/main.py` comments.
- Name the five gates without looking: secrets, SAST, SCA, container, SBOM.

### 2. Run the secure app

Use the README commands. Create a note, search for it. Hit `/health`.

`$env:SECRET_KEY = "local-dev-only"` is a **terminal** environment variable. It does not write `.env`. If you skip it, the app uses the local fallback `dev-only-change-me`.

### 3. Compare broken vs secure

Open side by side:

- `learning/broken_app/app.py`
- `app/main.py`

Then read the **Before / after** section below.

### 4. Read the CI file

Open `.github/workflows/security.yml`. For each job: “This fails the PR when …”

Open `security/suppressions.md`. If Trivy finds HIGH with no fix: document a waiver (id, reason, owner, expiry) — do not silently ignore.

### 5. Make scanners fail (lab only)

Lab is **excluded** from main CI on purpose.

```powershell
# Secrets
gitleaks detect --source learning/broken_app --no-git -v

# SAST
semgrep --config p/python --config p/flask learning/broken_app

# SCA
trivy fs --severity CRITICAL,HIGH learning/broken_app

# Container (after build)
docker build -t notes-broken ./learning/broken_app
trivy image --severity CRITICAL,HIGH notes-broken
```

Which job catches what: hardcoded key → **Gitleaks**. SQL string-glue / XSS / `debug=True` → **Semgrep**. Old libraries / image issues → **Trivy**.

### 6. Watch GitHub Actions

Actions tab → **Security Gates**. Download the **sbom-cyclonedx** artifact from a green container job.

An **SBOM** is a software bill of materials — inventory of what you shipped, used for vuln response and compliance.

---

## Before / after

Story: **find → understand → fix → prove.**

### Hardcoded secret

Broken:

```python
API_KEY = "sk_live_demo_hardcoded_secret_do_not_use_12345"
app.config["SECRET_KEY"] = "also-hardcoded-flask-secret"
```

Secure: `os.environ.get("SECRET_KEY", ...)`. Anyone with the repo (or git history) can steal a hardcoded key.

### SQL injection

Broken: user text is pasted into the SQL string.

```python
sql = f"SELECT ... WHERE title LIKE '%{q}%'"
```

Secure: SQL is a fixed template with `?`; user data is passed separately. That is a **parameterized query** — command and data stay apart.

### XSS

Broken: `render_template_string(f"<h1>Welcome {name}</h1>...")`  
Secure: real templates (`app/templates/`) with auto-escape. Do not use `|safe` on user content.

### Debug and container privilege

Broken: `debug=True`, `host="0.0.0.0"`, Docker runs as root.  
Secure: debug off unless `FLASK_DEBUG=1`; listen on `127.0.0.1` locally; `USER appuser`.

### Vulnerable dependencies

Broken: old pins in `learning/broken_app/requirements-broken.txt`.  
Secure: current pins in `requirements.txt`. Fix = upgrade, retest, regenerate SBOM (or waive with expiry).

---

## Practice later

1. Add a Semgrep rule (e.g. ban `eval(`).
2. Upgrade a dependency and think about what changed in the SBOM.
3. Add a fake secret in `app/`, watch Gitleaks fail, then remove it.
4. Quiz yourself: walk a HIGH Semgrep finding from PR fail to merge.

Ask Cursor to *explain* findings. Struggle 5–10 minutes before asking it to fix.
