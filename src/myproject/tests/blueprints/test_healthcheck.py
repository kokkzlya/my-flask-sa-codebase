from flask import Flask, url_for
from flask.testing import FlaskClient


def test_healthcheck(
        flask_app: Flask,
        client: FlaskClient,
        ):
    with flask_app.app_context():
        resp = client.get(url_for("root.health_check"))
        assert resp.status_code == 200
