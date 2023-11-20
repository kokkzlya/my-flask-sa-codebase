from dependency_injector.wiring import Provide, inject
from flask import Blueprint, Response, request
from flask_login import current_user, login_required

from myproject.containers import App
from myproject.domain.datatypes import Post
from myproject.domain.interfaces.usecases import (
    CreatePost, DeletePost, GetPost, UpdatePost,
)
from myproject.errors import NotFoundError

bp = Blueprint("posts", __name__)


# @bp.route("", methods=["GET"])
# def fetch_posts():
#     stmt = select(Post) \
#         .where(Post.deleted.is_(None)) \
#         .join(User, User.id == Post.author_id, isouter=True) \
#         .order_by(Post.created)
#     result = Session.scalars(stmt).all()
#     return jsonify([
#         ResponsePostSchema().dump(row)
#         for row in result
#     ])


@bp.route("", methods=["POST"])
@login_required
@inject
def create_post(create_post: CreatePost = Provide[App.usecases.create_post]):
    p: Post = Post.from_json(request.get_data(as_text=True))
    p.author = current_user.user
    create_post.execute(p)
    return Response(
        response=p.to_json(),
        status=201,
        headers={'Content-Type': "application/json"},
    )


@bp.route("/<post_id>", methods=["GET"])
@inject
def fetch_post(
        post_id,
        get_post: GetPost = Provide[App.usecases.get_post],
        ):
    result = get_post.execute(post_id)
    if result is None:
        raise NotFoundError(f"post with id `{post_id}` is not found")
    return Response(
        response=result.to_json(),
        headers={'Content-Type': "application/json"},
    )


@bp.route("/<post_id>", methods=["PUT"])
@inject
def update_post(
        post_id: str,
        get_post: GetPost = Provide[App.usecases.get_post],
        update_post: UpdatePost = Provide[App.usecases.update_post],
        ):
    result = get_post.execute(post_id)
    if result is None:
        raise NotFoundError(f"post with id `{post_id}` is not found")
    post: Post = Post.from_json(request.get_data(as_text=True))
    update_post.execute(post)
    return "", 204


@bp.route("/<post_id>", methods=["DELETE"])
@inject
def delete_post(
        post_id: str,
        get_post: GetPost = Provide[App.usecases.get_post],
        delete_post: DeletePost = Provide[App.usecases.delete_post],
        ):
    result = get_post.execute(post_id)
    if result is None:
        raise NotFoundError(f"post with id `{post_id}` is not found")
    delete_post.execute(post_id)
    return "", 204
