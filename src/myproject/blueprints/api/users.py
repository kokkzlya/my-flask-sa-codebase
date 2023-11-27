from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json
from dependency_injector.wiring import Provide, inject
from flask import Blueprint, Response, jsonify, request
from sqlalchemy import select
from sqlalchemy.orm import load_only

from myproject.containers import App
from myproject.domain.datatypes import NewUser, User
from myproject.domain.interfaces.usecases import ICreateUser, IGetUser
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
@inject
def create_user(create_user: ICreateUser = Provide[App.usecases.create_user]):
    u = NewUser.from_json(request.get_data(as_text=True))
    create_user.execute(u)
    return Response(
        response=User.from_dict(u.to_dict()).to_json(),
        status=201,
        headers={'Content-Type': "application/json"},
    )


@bp.route("/<user_id>", methods=["GET"])
@inject
def fetch_user(
        user_id: str,
        get_user: IGetUser = Provide[App.usecases.get_user],
        ):
    user = get_user.execute(user_id)
    if user is None:
        raise NotFoundError(f"user with ID: `{user_id}` is not found")
    return Response(
        response=user.to_json(),
        headers={'Content-Type': "application/json"},
    )
