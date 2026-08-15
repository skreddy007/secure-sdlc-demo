# Before / after — vulnerable vs secure

This is the heart of the portfolio story: **find → understand → fix → prove**.

---

## 1) Hardcoded secret

### Before (`learning/broken_app/app.py`)

```python
API_KEY = "sk_live_demo_hardcoded_secret_do_not_use_12345"
app.config["SECRET_KEY"] = "also-hardcoded-flask-secret"
```

**Why bad:** Anyone with repo access (or a leaked git history) gets credentials. Secret scanners (Gitleaks) exist for this.

### After (`app/main.py` + `.env.example`)

```python
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
```

**Fix idea:** Load secrets from environment / CI secrets / vault. Never commit real keys. Rotate if leaked.

---

## 2) SQL injection

### Before

```python
q = request.args.get("q", "")
sql = f"SELECT id, title, body FROM notes WHERE title LIKE '%{q}%'"
rows = conn.execute(sql).fetchall()
```

**Why bad:** Attacker can craft `q` to change the meaning of the SQL (read/modify data).

Example mental model: if `q` is `x' OR '1'='1`, the filter may become always true.

### After

```python
like = f"%{query}%"
conn.execute(
    "SELECT ... FROM notes WHERE title LIKE ? OR body LIKE ?",
    (like, like),
)
```

**Fix idea:** Parameterized queries. The database driver treats user data as *values*, not *code*.

---

## 3) Cross-site scripting (XSS) risk

### Before

```python
name = request.args.get("name", "guest")
return render_template_string(f"<h1>Welcome {name}</h1>...")
```

**Why bad:** If `name` contains HTML/JS, the browser may execute it in your users’ sessions.

### After

Use a real template file (`templates/search.html`) and Jinja auto-escaping. Do not mark user content `|safe` unless you fully trust and sanitize it.

---

## 4) Debug mode & container privilege

### Before

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

```dockerfile
FROM python:3.11
# no USER — runs as root
CMD ["python", "app.py"]
```

**Why bad:** Debug mode can expose an interactive debugger; binding `0.0.0.0` increases exposure; root containers increase blast radius.

### After

```python
debug = os.environ.get("FLASK_DEBUG", "0") == "1"
app.run(host="127.0.0.1", port=..., debug=debug)
```

```dockerfile
USER appuser
```

---

## 5) Vulnerable dependencies (SCA)

### Before (`learning/broken_app/requirements-broken.txt`)

Old Flask/Jinja/Werkzeug pins — useful to watch Trivy report CVEs.

### After (`requirements.txt`)

Current pinned versions used by the secure app and main CI.

**Fix idea:** Upgrade, retest, regenerate SBOM, confirm Trivy goes green (or document accepted risk with expiry).

---

## Interview soundbite

> “I kept a broken lab to show how Gitleaks/Semgrep/Trivy fail, and a secure `app/` branch of the design that passes the same gates. Suppressions require owner, reason, and expiry — same discipline as commercial SCA waivers.”
