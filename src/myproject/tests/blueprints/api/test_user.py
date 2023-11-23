from flask import Flask, url_for
import shortuuid

from myproject.domain.datatypes import NewUser, User


def test_create_user(
        flask_app: Flask,
        tester_account: User,
        authenticate_client,
        ):
    with (
        flask_app.app_context(),
        authenticate_client(tester_account) as client,
    ):
        new_user = NewUser(
            name=shortuuid.uuid(),
            email="%s@mail.test" % shortuuid.uuid(),
            username=shortuuid.uuid(),
            password=shortuuid.uuid(),
        )
        resp = client.post(
            url_for("api.users.create_user"),
            data=new_user.to_json(),
        )
        assert resp.status_code == 201
        saved_user = NewUser.from_json(resp.get_data(as_text=True))
        assert saved_user.id is not None
        assert saved_user.name == new_user.name
        assert saved_user.email == new_user.email
        assert saved_user.username == new_user.username
        assert saved_user.password is None
        assert saved_user.created is not None
        assert saved_user.updated is not None

        # fetch by ID
        resp = client.get(
            url_for("api.users.fetch_user", user_id=saved_user.id)
        )
        assert resp.status_code == 200
        fetched_user = User.from_json(resp.get_data(as_text=True))
        assert fetched_user.id == saved_user.id

        # fetch by username
        resp = client.get(
            url_for("api.users.fetch_user", user_id=saved_user.username)
        )
        assert resp.status_code == 200
        fetched_user = User.from_json(resp.get_data(as_text=True))
        assert fetched_user.id == saved_user.id

        # fetch by email
        resp = client.get(
            url_for("api.users.fetch_user", user_id=saved_user.email)
        )
        assert resp.status_code == 200
        fetched_user = User.from_json(resp.get_data(as_text=True))
        assert fetched_user.id == saved_user.id
