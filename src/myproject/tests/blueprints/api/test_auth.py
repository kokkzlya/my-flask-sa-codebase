from flask import Flask, url_for

from myproject.domain.datatypes import User


def test_whoami(
        flask_app: Flask,
        tester_account: User,
        authenticate_client,
        ):
    with (
        flask_app.app_context(),
        authenticate_client(tester_account) as client,
    ):
        resp = client.get(url_for("api.auth.whoami"))
        assert resp.status_code == 200
        authed_user = User.from_json(resp.get_data(as_text=True))
        assert authed_user.id == tester_account.id
        assert authed_user.username == tester_account.username
