from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from flask import Blueprint, jsonify, request
from marshmallow_dataclass import class_schema
from passlib.hash import argon2
from sqlalchemy import or_, select
from sqlalchemy.orm import load_only

from myproject.core.errors import NotFoundError
from myproject.repository.db import Session
from myproject.repository.model import User

bp = Blueprint("users", __name__)


@dataclass
class RequestNewUser:
    name: str
    email: str
    username: str
    password: str


RequestNewUserSchema = class_schema(RequestNewUser)


@dataclass
class ResponseUser:
    id: str
    name: str
    email: str
    username: str
    created: datetime
    updated: datetime
    deleted: Optional[datetime]


ResponseUserSchema = class_schema(ResponseUser)


@bp.route("", methods=["GET"])
def fetch_users():
    stmt = select(User) \
        .options(load_only(
            User.id, User.name, User.email, User.username, User.password,
            User.banned_until, User.created, User.updated,
        )) \
        .where(User.deleted.is_(None)) \
        .order_by(User.deleted.is_(None))
    result = Session.scalars(stmt)
    return jsonify([
        ResponseUserSchema().dump(row)
        for row in result
    ])


@bp.route("", methods=["POST"])
def create_user():
    u = RequestNewUserSchema().load(request.get_json())
    new_user = User(
        name=u.name,
        email=u.email,
        username=u.username,
        password=argon2.hash(u.password),
        created=datetime.utcnow(),
        updated=datetime.utcnow(),
    )
    Session.add(new_user)
    Session.flush()
    return jsonify(ResponseUserSchema().dump(new_user)), 201


@bp.route("/<user_id>", methods=["GET"])
def fetch_user(user_id):
    stmt = select(User) \
        .options(
            load_only(
                User.id, User.name, User.email, User.username,
                User.banned_until, User.created, User.updated,
            ),
        ) \
        .where(or_(
            User.id == user_id,
            User.deleted.is_(None),
        ))
    result = Session.scalars(stmt).first()
    if result is None:
        raise NotFoundError(f"user with ID: `{user_id}` is not found")
    return jsonify(ResponseUserSchema().dump(result))
