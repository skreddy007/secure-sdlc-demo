# Learning path (beginner → resume-ready)

Do these steps **in order**. Each step has a goal, actions, and a “check you learned it” prompt.

Estimated time: **1–2 evenings** for a first pass; longer if you experiment with the broken lab.

---

## Step 0 — What you are building

**Goal:** Understand the story in one sentence.

> I built a small web app and an automated security pipeline that blocks risky secrets, code patterns, vulnerable packages, and insecure containers — and I can explain how each finding gets fixed.

You do **not** need to be an expert in Flask. Flask is just the sample product. The product for your resume is the **Secure SDLC process**.

---

## Step 1 — Open the repo and orient yourself

**Actions**

1. Open `D:\PersonalProjects\secure-sdlc-demo` in Cursor.
2. Skim `README.md`.
3. Open `app/main.py` and read the comments.

**Check:** Can you name the five security gates in the README table without looking?

---

## Step 2 — Run the secure app locally

**Why:** Security work starts with a running system. If you cannot run it, you cannot verify a fix.

**Actions (PowerShell)**

```powershell
cd D:\PersonalProjects\secure-sdlc-demo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SECRET_KEY = "local-dev-only"
python -m app.main
```

Visit http://127.0.0.1:5000 — create a note, then search for it.

**Check:** What does `/health` return? Why is that useful for ops/security monitoring later?

---

## Step 3 — Study insecure vs secure code

**Actions**

1. Open `learning/broken_app/app.py` (vulnerable).
2. Open `app/main.py` (secure).
3. Read `docs/before-after.md`.

Focus on four patterns:

| # | Broken pattern | Secure pattern |
|---|----------------|----------------|
| 1 | Hardcoded API key | Environment variable / secret manager |
| 2 | SQL string concat | Parameterized query `?` |
| 3 | `render_template_string` + user input | Jinja templates (auto-escape) |
| 4 | `debug=True` / run as root | debug off by default / non-root container |

**Check:** Explain SQL injection in plain English to an imaginary teammate in under 60 seconds.

---

## Step 4 — Understand the CI gates

**Actions**

1. Open `.github/workflows/security.yml`.
2. For each job, write one line in your notes: “This job fails the PR when …”
3. Open `security/suppressions.md` and read the waiver rules.

**Check:** If Trivy finds a HIGH CVE with no fix available, what process should you follow before adding `.trivyignore`?

---

## Step 5 — Practice making scanners fail (lab)

Install tools when ready (one at a time is fine):

- [Gitleaks](https://github.com/gitleaks/gitleaks)
- [Semgrep](https://semgrep.dev/docs/getting-started/)
- [Trivy](https://trivy.dev/)

From `learning/broken_app/README.md`, run the suggested commands.

**Check:** Paste (into your private notes) one finding from each tool and write the fix in one sentence.

---

## Step 6 — Push to GitHub and watch CI

**Actions**

1. Create a GitHub repo (private or public).
2. Push this project.
3. Open the **Actions** tab and watch `Security Gates`.
4. Download the **SBOM** artifact from a successful `Container scan + SBOM` run.

**Check:** What is an SBOM, and why would a security or compliance team ask for one?

---

## Step 7 — Write your resume bullet

Use `docs/resume-talking-points.md`. Pick **one** bullet and customize it with your name/date.

**Check:** Can you answer: “Walk me through how a HIGH Semgrep finding goes from PR failure to merge”?

---

## How to learn with Cursor (important)

Ask the agent things like:

- “Explain this Semgrep rule like I’m new to AppSec.”
- “I ran Trivy and got X — is this a real risk for this app?”
- “Quiz me on SQL injection using this repo.”

Avoid: “Just fix everything for me” on every finding — struggle for 5–10 minutes first, then ask.

---

## Suggested weekly practice after the first pass

1. Add one new Semgrep custom rule (e.g. ban `eval(`).
2. Upgrade a dependency and regenerate mental “what changed in SBOM.”
3. Add a fake secret, watch Gitleaks fail, then remove it.
4. Write a short LinkedIn post from `docs/sdlc-walkthrough.md`.
