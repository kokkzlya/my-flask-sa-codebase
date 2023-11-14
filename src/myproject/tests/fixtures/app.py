import pytest
from flask import Flask
from flask.testing import FlaskClient

from myproject.app import create_app


@pytest.fixture(scope="session", autouse=True)
def flask_app():
    app = create_app("myproject.config.Testing")
    app.config.update({
        'TESTING':               True,
        'SERVER_NAME':           "myproject.127.0.0.1.nip.io:5000",
        'SESSION_COOKIE_DOMAIN': None,
    })
    yield app


@pytest.fixture()
def client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()
