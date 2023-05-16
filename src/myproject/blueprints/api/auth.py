from dataclasses import dataclass
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user
from marshmallow_dataclass import class_schema
from passlib.hash import argon2
from sqlalchemy import or_, select
from sqlalchemy.orm import load_only

from myproject.core.errors import AuthorizationError
from myproject.repository.db import Session
from myproject.repository.model import User

bp = Blueprint("auth", __name__)


@dataclass
class UserCred():
    username: str
    password: str


UserCredSchema = class_schema(UserCred)


@dataclass
class ResponseUser():
    id: str
    username: str
    email: str


ResponseUserSchema = class_schema(ResponseUser)


@bp.route("/login", methods=["POST"])
def login():
    cred = UserCredSchema().load(request.get_json())
    stmt = select(User) \
        .options(
            load_only(
                User.id, User.username, User.password, User.email,
                User.banned_until,
            ),
        ) \
        .where(or_(
            User.username == cred.username,
            User.email == cred.username,
        ))
    result = Session.scalars(stmt).first()
    if result is None:
        raise AuthorizationError("username or password is invalid")
    if result.banned_until is not None and \
       datetime.utcnow() < result.banned_until:
        raise AuthorizationError("the account is banned")
    if not argon2.verify(cred.password, result.password):
        raise AuthorizationError("username or password is invalid")
    stmt = select(User) \
        .options(
            load_only(
                User.id, User.username, User.email,
            ),
        ) \
        .where(User.id == result.id)
    result = Session.scalars(stmt).first()
    login_user(result)
    return jsonify(ResponseUserSchema().dump(result)), 201


@bp.route("/whoami", methods=["GET"])
@login_required
def whoami():
    return jsonify(ResponseUserSchema().dump(current_user))
