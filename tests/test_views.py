from flask import Flask

from app.models import _add_tenant


def test_tenant_isolation(app: Flask):
    """Basic test of multi-tenant functionality."""
    with app.app_context():
        _add_tenant("one.com", "one")
        _add_tenant("two.com", "two")

    # First tenant
    app.config["SERVER_NAME"] = "one.com"

    # No data has been inserted yet.
    resp = app.test_client().get("/data/get/5")
    assert resp.status_code == 404

    # Successful insert
    resp = app.test_client().post("/data/insert/5/42")
    assert resp.status_code == 200
    assert resp.json["status"] == "success"

    # Data can be retreived.
    resp = app.test_client().get("/data/get/5")
    assert resp.status_code == 200
    assert resp.json["value"] == 42

    # Data cannot be added twice.
    resp = app.test_client().post("/data/insert/5/42")
    assert resp.status_code == 400

    # Second tenant
    app.config["SERVER_NAME"] = "two.com"

    # Can insert with same key.
    resp = app.test_client().post("/data/insert/5/43")
    assert resp.status_code == 200
    assert resp.json["status"] == "success"

    # Retreive correct key tenant two.
    resp = app.test_client().get("/data/get/5")
    assert resp.status_code == 200
    assert resp.json["value"] == 43

    # Verify value for tenant one hasn't been modified.
    app.config["SERVER_NAME"] = "one.com"
    resp = app.test_client().get("/data/get/5")
    assert resp.status_code == 200
    assert resp.json["value"] == 42
