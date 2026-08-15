"""
Team Notes — a tiny Flask app used to practice Secure SDLC.

This is the SECURE version (safe for resume demos and CI).
Compare with learning/broken_app/ to see what NOT to do.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from markupsafe import escape

BASE_DIR = Path(__file__).resolve().parent


def _db_path() -> Path:
    # Read on each use so tests can point at a temp database via env var.
    return Path(os.environ.get("NOTES_DB_PATH", BASE_DIR / "notes.db"))


def create_app() -> Flask:
    app = Flask(__name__)

    # SECRET_KEY must come from the environment in real deployments.
    # Fallback is only for local learning — never commit a real production secret.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")

    _init_db()

    @app.get("/")
    def index():
        notes = _list_notes()
        return render_template("index.html", notes=notes)

    @app.post("/notes")
    def create_note():
        title = (request.form.get("title") or "").strip()
        body = (request.form.get("body") or "").strip()
        if not title or not body:
            flash("Title and body are required.", "error")
            return redirect(url_for("index"))

        _insert_note(title, body)
        flash("Note created.", "ok")
        return redirect(url_for("index"))

    @app.get("/notes/search")
    def search_notes():
        # Parameterized query — safe against SQL injection.
        q = (request.args.get("q") or "").strip()
        notes = _search_notes(q) if q else []
        # escape() keeps reflected search text from becoming XSS in templates
        # when we also avoid |safe in Jinja.
        return render_template("search.html", q=escape(q), notes=notes)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def _init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def _list_notes() -> list[sqlite3.Row]:
    with _connect() as conn:
        return list(
            conn.execute(
                "SELECT id, title, body, created_at FROM notes ORDER BY id DESC"
            )
        )


def _insert_note(title: str, body: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO notes (title, body) VALUES (?, ?)",
            (title, body),
        )


def _search_notes(query: str) -> list[sqlite3.Row]:
    # IMPORTANT: use placeholders (?,) — never build SQL with f-strings or +.
    like = f"%{query}%"
    with _connect() as conn:
        return list(
            conn.execute(
                "SELECT id, title, body, created_at FROM notes "
                "WHERE title LIKE ? OR body LIKE ? ORDER BY id DESC",
                (like, like),
            )
        )


# Local run:  python -m app.main   OR   flask --app app.main:create_app run
app = create_app()

if __name__ == "__main__":
    # debug=False by default for safer local demos.
    # Set FLASK_DEBUG=1 only on your machine while learning.
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=debug)
