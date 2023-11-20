from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json
from flask import Blueprint, Response, jsonify, request
from passlib.hash import argon2
from sqlalchemy import or_, select
from sqlalchemy.orm import load_only

from myproject.domain.datatypes import User
from myproject.errors import NotFoundError
from myproject.repository.db import Session
from myproject.repository.model import User as UserModel

bp = Blueprint("users", __name__)


@dataclass_json
@dataclass
class RequestNewUser:
    name: str
    email: str
    username: str
    password: str


@dataclass_json
@dataclass
class ResponseUser:
    id: str
    name: str
    email: str
    username: str
    created: datetime
    updated: datetime
    deleted: Optional[datetime]


@bp.route("", methods=["GET"])
def fetch_users():
    stmt = select(UserModel) \
        .options(load_only(
            UserModel.id, UserModel.name, UserModel.email, UserModel.username,
            UserModel.password, UserModel.banned_until, UserModel.created,
            UserModel.updated,
        )) \
        .where(UserModel.deleted.is_(None)) \
        .order_by(UserModel.deleted.is_(None))
    result = Session.scalars(stmt)
    return jsonify([
        User.from_dict(row)
        for row in result
    ])


@bp.route("", methods=["POST"])
def create_user():
    u = User.from_json(request.get_data(as_text=True))
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
    return Response(
        response=User.from_dict(new_user).to_json(),
        status=201,
        headers={'Content-Type': "application/json"},
    )


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
    return Response(
        response=User.from_dict({
            col.name: getattr(result, col.name)
            for col in UserModel.__table__.columns
        }),
        headers={'Content-Type': "application/json"},
    )
