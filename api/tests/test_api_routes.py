from datetime import datetime, timedelta

import pytest

from app import create_app
from app.models import Stats, db


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    db_path = tmp_path / "test.db"

    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        }
    )

    with application.app_context():
        db.drop_all()
        db.create_all()

    yield application

    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers():
    return {"X-API-Key": "test-key"}


def _valid_stat_payload(hostname="host-a", disk_usage=10.5):
    return {
        "hostname": hostname,
        "disk_usage": disk_usage,
        "cpu_usage": 15.2,
        "ram_usage": 33.4,
        "network_sent": 100,
        "network_recv": 200,
    }


def test_unauthorized_without_api_key(client):
    response = client.get("/api/v1/stats")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Unauthorized"}


def test_add_stats_missing_required_fields_returns_400(client, auth_headers):
    response = client.post(
        "/api/v1/stats",
        headers=auth_headers,
        json={"hostname": "host-a"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing required fields"}


def test_add_stats_creates_record(client, auth_headers):
    payload = _valid_stat_payload(hostname="host-a", disk_usage=42.0)

    response = client.post("/api/v1/stats", headers=auth_headers, json=payload)
    body = response.get_json()

    assert response.status_code == 201
    assert body["hostname"] == "host-a"
    assert body["disk_usage"] == 42.0
    assert body["cpu_usage"] == payload["cpu_usage"]


def test_get_stats_returns_latest_per_hostname_sorted(client, auth_headers):
    client.post(
        "/api/v1/stats",
        headers=auth_headers,
        json=_valid_stat_payload(hostname="zeta", disk_usage=10.0),
    )
    client.post(
        "/api/v1/stats",
        headers=auth_headers,
        json=_valid_stat_payload(hostname="alpha", disk_usage=20.0),
    )
    client.post(
        "/api/v1/stats",
        headers=auth_headers,
        json=_valid_stat_payload(hostname="zeta", disk_usage=99.0),
    )

    response = client.get("/api/v1/stats", headers=auth_headers)
    body = response.get_json()

    assert response.status_code == 200
    assert [item["hostname"] for item in body] == ["alpha", "zeta"]
    assert body[1]["disk_usage"] == 99.0


def test_get_stats_by_hostname_returns_ascending_and_limited(client, app, auth_headers):
    start = datetime(2024, 1, 1, 0, 0, 0)

    with app.app_context():
        for i in range(105):
            db.session.add(
                Stats(
                    hostname="alpha",
                    timestamp=start + timedelta(seconds=i),
                    disk_usage=float(i),
                    cpu_usage=1.0,
                    ram_usage=2.0,
                    network_sent=100 + i,
                    network_recv=200 + i,
                )
            )
        db.session.commit()

    response = client.get("/api/v1/stats/alpha", headers=auth_headers)
    body = response.get_json()

    assert response.status_code == 200
    assert len(body) == 100
    assert body[0]["disk_usage"] == 5.0
    assert body[-1]["disk_usage"] == 104.0
    timestamps = [item["timestamp"] for item in body]
    assert timestamps == sorted(timestamps)
