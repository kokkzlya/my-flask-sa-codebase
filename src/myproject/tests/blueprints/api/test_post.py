from flask import Flask, url_for
from flask.testing import FlaskClient

from myproject.domain.datatypes import Post, User


def test_create_post(
        flask_app: Flask,
        tester_account: User,
        authenticate_client,
        ):
    with (
        flask_app.app_context(),
        authenticate_client(tester_account) as client,
    ):
        # Try to create a new post
        new_post = Post(
            title="Test A New Post",
            content="Test a new post",
        )
        resp = client.post(
            url_for("api.posts.create_post"),
            data=new_post.to_json(),
            headers={
                'Content-Type': "application/json",
            },
        )
        assert resp.status_code == 201
        saved_post = Post.from_json(resp.get_data(as_text=True))
        assert saved_post.id is not None

        # Try to get saved post
        resp = client.get(
            url_for("api.posts.fetch_post", post_id=saved_post.id),
        )
        assert resp.status_code < 300
        saved_post = Post.from_json(resp.get_data(as_text=True))
        assert saved_post.title == new_post.title
        assert saved_post.content == new_post.content


def test_update_post(
        flask_app: Flask,
        tester_account: User,
        authenticate_client,
        ):
    with (
        flask_app.app_context(),
        authenticate_client(tester_account) as client,
    ):
        # Create a new post
        new_post = Post(
            title="Test A New Post",
            content="Test a new post",
        )
        resp = client.post(
            url_for("api.posts.create_post"),
            data=new_post.to_json(),
            headers={'Content-Type': "application/json"},
        )
        assert resp.status_code == 201
        saved_post = Post.from_json(resp.get_data(as_text=True))
        assert saved_post.id is not None

        # Update the created post
        saved_post.title = "Updated title of the new post"
        saved_post.content = "Updated content of the new post"

        resp = client.put(
            url_for("api.posts.update_post", post_id=saved_post.id),
            data=saved_post.to_json(),
            headers={'Content-Type': "application/json"},
        )
        assert resp.status_code == 204

        # Get the updated post
        resp = client.get(
            url_for("api.posts.fetch_post", post_id=saved_post.id),
        )
        assert resp.status_code < 300
        updated_post = Post.from_json(resp.get_data(as_text=True))
        assert updated_post.title == saved_post.title
        assert updated_post.content == saved_post.content


def test_delete_post(
        flask_app: Flask,
        tester_account: User,
        authenticate_client,
        ):
    with (
        flask_app.app_context(),
        authenticate_client(tester_account) as client,
    ):
        # Create a new post
        new_post = Post(
            title="Test A New Post",
            content="Test a new post",
        )
        resp = client.post(
            url_for("api.posts.create_post"),
            data=new_post.to_json(),
            headers={'Content-Type': "application/json"},
        )
        assert resp.status_code == 201
        saved_post = Post.from_json(resp.get_data(as_text=True))
        assert saved_post.id is not None

        # Delete the created post
        resp = client.delete(
            url_for("api.posts.delete_post", post_id=saved_post.id),
            headers={'Content-Type': "application/json"},
        )
        assert resp.status_code == 204

        # Get the deleted post
        resp = client.get(
            url_for("api.posts.fetch_post", post_id=saved_post.id),
        )
        assert resp.status_code < 300
        deleted_post = Post.from_json(resp.get_data(as_text=True))
        assert deleted_post.deleted is not None
        assert deleted_post.deleted > saved_post.created
        assert deleted_post.updated > saved_post.created


def test_fetch_not_found_post(
        flask_app: Flask,
        client: FlaskClient,
        ):
    with flask_app.app_context():
        resp = client.get(
            url_for("api.posts.fetch_post", post_id="youwillneverfindit"),
        )
        assert resp.status_code == 404
