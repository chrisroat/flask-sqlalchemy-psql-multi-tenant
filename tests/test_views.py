from flask import Flask


def test_data(app: Flask):
    """Basic test of functionality."""

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
