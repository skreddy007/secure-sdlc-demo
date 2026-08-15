"""
INTENTIONAL VULNERABILITIES — for learning only.
Do NOT deploy this file. Security CI excludes learning/broken_app.

Walk through docs/LEARNING_PATH.md and docs/before-after.md
to understand each issue and the secure fix in app/main.py.
"""

from __future__ import annotations

import os
import sqlite3

from flask import Flask, request, render_template_string

# VULN 1 — Hardcoded secret (secret scanning / Gitleaks)
# Real apps load secrets from environment or a secret manager.
API_KEY = "sk_live_demo_hardcoded_secret_do_not_use_12345"

app = Flask(__name__)
app.config["SECRET_KEY"] = "also-hardcoded-flask-secret"
DB_PATH = "broken_notes.db"


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS notes "
            "(id INTEGER PRIMARY KEY, title TEXT, body TEXT)"
        )


@app.get("/")
def index():
    # VULN 2 — XSS via render_template_string with unsanitized user input
    name = request.args.get("name", "guest")
    return render_template_string(
        f"<h1>Welcome {name}</h1><p>API key prefix: {API_KEY[:8]}...</p>"
        "<p>Try /search?q=test</p>"
    )


@app.get("/search")
def search():
    # VULN 3 — SQL injection via string concatenation
    q = request.args.get("q", "")
    sql = f"SELECT id, title, body FROM notes WHERE title LIKE '%{q}%'"
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(sql).fetchall()
    return {"query": q, "results": rows, "debug": True}


@app.post("/notes")
def create():
    title = request.form.get("title", "")
    body = request.form.get("body", "")
    # Still vulnerable pattern if someone later concatenates here.
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO notes (title, body) VALUES (?, ?)",
            (title, body),
        )
    return {"ok": True}


if __name__ == "__main__":
    init_db()
    # VULN 4 — debug mode enabled (information disclosure / code execution risk)
    app.run(host="0.0.0.0", port=5000, debug=True)
