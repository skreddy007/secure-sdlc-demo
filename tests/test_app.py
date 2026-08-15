"""Smoke tests for the secure Team Notes app."""

from app.main import create_app


def test_health():
    client = create_app().test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_create_and_search_note(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("NOTES_DB_PATH", str(db_file))

    client = create_app().test_client()

    create = client.post(
        "/notes",
        data={"title": "Patch Friday", "body": "Ship security fixes"},
        follow_redirects=True,
    )
    assert create.status_code == 200

    search = client.get("/notes/search?q=Patch")
    assert search.status_code == 200
    assert b"Patch Friday" in search.data
