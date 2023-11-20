from contextlib import contextmanager
from datetime import datetime
import json

from flask import Flask, url_for
from flask.testing import FlaskClient
from passlib.hash import argon2
from pytest_mock import MockerFixture
from sqlalchemy import select, update
import pytest
import shortuuid

from myproject.app import create_app
from myproject.domain.datatypes import User
from myproject.repository.db import Session
from myproject.repository.model import User as UserModel


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


def _create_or_update_tester_account(flask_app: Flask) -> User:
    with flask_app.app_context(), Session.begin():
        stmt = select(UserModel).where(UserModel.username == "tester")
        tester_account = Session.scalars(stmt).first()
        if tester_account is None:
            tester_account = UserModel(
                name="tester",
                email="tester@mail.dev",
                username="tester",
                password=argon2.hash(shortuuid.uuid()),
                created=datetime.utcnow(),
                updated=datetime.utcnow(),
            )
            Session.add(tester_account)
        else:
            stmt = update(UserModel).where(UserModel.username == "tester") \
                .values(banned_until=None)
            Session.execute(stmt)

        Session.flush()
        return User.from_dict({
            col.name: getattr(tester_account, col.name)
            for col in tester_account.__table__.columns
        })


@pytest.fixture(scope="session")
def tester_account(request: any, flask_app: Flask) -> User:
    account = _create_or_update_tester_account(flask_app)

    def _freeze_tester_account():
        with flask_app.app_context(), Session.begin():
            stmt = update(UserModel).where(UserModel.username == "tester") \
                .values(
                    banned_until=datetime(9999, 12, 31, 23, 59, 59, 999),
                    updated=datetime.utcnow(),
                )
            Session.execute(stmt)

    request.addfinalizer(_freeze_tester_account)
    return account


@contextmanager
def _authenticate_user(
        mocker: MockerFixture,
        flask_app: Flask,
        client: FlaskClient,
        account: User,
        ):
    with flask_app.app_context():
        mocker.patch(
            "myproject.usecases.user.argon2.verify",
            return_value=True,
        )
        resp = client.post(url_for("api.auth.login"), data=json.dumps({
            'user_id': account.username,
            'password': "doesn't matter",
        }))
        assert resp.status_code == 201, \
            "must successfully logging in the tester_account"
    yield client


@pytest.fixture
def authenticate_client(
        mocker: MockerFixture,
        flask_app: Flask,
        client: FlaskClient,
        ):
    @contextmanager
    def wrapper(account: User):
        with (
            _authenticate_user(mocker, flask_app, client, account)
            as _authenticated_client
        ):
            yield _authenticated_client
    return wrapper
