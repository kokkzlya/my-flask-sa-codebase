from flask import Flask, url_for
from flask.testing import FlaskClient


def test_create_app(
        flask_app: Flask,
        client: FlaskClient,
        ):
    with flask_app.app_context():
        resp = client.get(url_for("root.landing"))
        assert resp.status_code == 200
        assert resp.text is not None
