from flask import Flask
from flask_login import LoginManager
from sqlalchemy import select

from myproject.blueprints import api, root
from myproject.domain.datatypes import AuthedUser, User
from myproject.repository import db
from myproject.repository.model import User as UserModel
from myproject import containers, reverse_proxy_url_scheme

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id) -> User:
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = db.Session.scalars(stmt).first()
    return AuthedUser(User.from_dict({
        col.name: getattr(result, col.name)
        for col in UserModel.__table__.columns
    }))


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    reverse_proxy_url_scheme.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    root.register_blueprints(app)
    api.register_blueprints(app)

    container = containers.App()
    container.config.from_dict(app.config)
    container.init_resources()
    container.wire(modules=[
        "myproject.blueprints.api.auth",
        "myproject.blueprints.api.posts",
        "myproject.blueprints.root",
    ])
    app.container = container
    return app
