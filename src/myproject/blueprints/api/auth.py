from dataclasses import dataclass

from dataclasses_json import dataclass_json
from dependency_injector.wiring import Provide, inject
from flask import Blueprint, Response, request
from flask_login import current_user, login_required, login_user

from myproject.containers import App
from myproject.domain.datatypes import AuthedUser, UserCredential
from myproject.domain.interfaces.usecases import ILogin

bp = Blueprint("auth", __name__)


@dataclass_json
@dataclass
class ResponseUser():
    id: str
    username: str
    email: str


@bp.route("/login", methods=["POST"])
@inject
def login(login: ILogin = Provide[App.usecases.login]):
    user_cred = UserCredential.from_json(request.get_data(as_text=True))
    user = login.execute(user_cred)
    login_user(AuthedUser(user))
    return Response(
        response=user.to_json(),
        status=201,
        headers={'Content-Type': "application/json"},
    )


@bp.route("/whoami", methods=["GET"])
@login_required
def whoami():
    return Response(
        response=current_user.user.to_json(),
        status=200,
        headers={'Content-Type': "application/json"},
    )
