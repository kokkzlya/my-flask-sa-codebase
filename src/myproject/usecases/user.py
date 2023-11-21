from datetime import datetime

from passlib.hash import argon2
from sqlalchemy import or_, select
from sqlalchemy.orm import load_only, scoped_session

from myproject.domain.datatypes import User, UserCredential
from myproject.domain.interfaces.usecases import Login
from myproject.errors import AuthorizationError
from myproject.repository.model import User as UserModel


class Login(Login):
    def __init__(self, session: scoped_session):
        self.session = session

    def execute(self, user_cred: UserCredential) -> User:
        with self.session.begin():
            stmt = select(UserModel) \
                .options(
                    load_only(
                        UserModel.id, UserModel.username, UserModel.password,
                        UserModel.email, UserModel.banned_until,
                    ),
                ) \
                .where(or_(
                    UserModel.username == user_cred.user_id,
                    UserModel.email == user_cred.user_id,
                ))
            result = self.session.scalars(stmt).first()
            if result is None:
                raise AuthorizationError("username or password is invalid")

            if result.banned_until is not None \
               and datetime.utcnow() < result.banned_until:
                raise AuthorizationError("the account is banned")

            if not argon2.verify(user_cred.password, result.password):
                raise AuthorizationError("username or password is invalid")

            stmt = select(UserModel) \
                .options(
                    load_only(
                        UserModel.id, UserModel.username, UserModel.email,
                    ),
                ) \
                .where(UserModel.id == result.id)
            u = self.session.scalars(stmt).first()
            return User.from_dict({
                col.name: getattr(u, col.name)
                for col in u.__table__.columns
            })
