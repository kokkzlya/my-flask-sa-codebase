from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from marshmallow_dataclass import class_schema
from sqlalchemy import select

from myproject.core.errors import NotFoundError
from myproject.repository.db import Session
from myproject.repository.model import Post, User

bp = Blueprint("posts", __name__)


@dataclass
class RequestNewPost():
    title: str
    content: str


RequestNewPostSchema = class_schema(RequestNewPost)


@dataclass
class RequestEditPost(RequestNewPost):
    published_at: Optional[datetime]


RequestEditPostSchema = class_schema(RequestEditPost)


@dataclass
class ResponsePostAuthor:
    id: str


@dataclass
class ResponsePost(RequestEditPost):
    id: str
    author: ResponsePostAuthor
    created: datetime
    updated: datetime
    deleted: Optional[datetime]


ResponsePostSchema = class_schema(ResponsePost)


@bp.route("", methods=["GET"])
def fetch_posts():
    stmt = select(Post) \
        .where(Post.deleted.is_(None)) \
        .join(User, User.id == Post.author_id, isouter=True) \
        .order_by(Post.created)
    result = Session.scalars(stmt).all()
    return jsonify([
        ResponsePostSchema().dump(row)
        for row in result
    ])


@bp.route("", methods=["POST"])
@login_required
def create_post():
    p = RequestNewPostSchema().load(request.get_json())
    new_post = Post(
        title=p.title,
        content=p.content,
        author_id=current_user.id,
        created=datetime.utcnow(),
        updated=datetime.utcnow(),
    )
    Session.add(new_post)
    Session.flush()
    return jsonify(ResponsePostSchema().dump(new_post)), 201


@bp.route("/<post_id>", methods=["GET"])
def fetch_post(post_id):
    stmt = select(Post).where(Post.id == post_id)
    result = Session.scalars(stmt).first()
    if result is None:
        raise NotFoundError(f"post with id `{post_id}` is not found")
    print(result.id, result.title)
    return jsonify(ResponsePostSchema().dump(result))


@bp.route("/<post_id>", methods=["PUT"])
def update_post(post_id):
    stmt = select(Post).where(Post.id == post_id)
    result = Session.scalars(stmt).first()
    if result is None:
        raise NotFoundError(f"post with id `{post_id}` is not found")

    p = RequestEditPostSchema().load(request.get_json())
    result.title = p.title
    result.content = p.content
    result.published_at = p.published_at
    return "", 204


@bp.route("/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    stmt = select(Post).where(Post.id == post_id)
    result = Session.scalars(stmt).first()
    if result is None:
        raise NotFoundError(f"post with id `{post_id}` is not found")
    result.deleted = datetime.utcnow()
    return "", 204
