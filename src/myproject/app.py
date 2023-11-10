from flask import Flask
from flask_login import LoginManager
from sqlalchemy import select

from myproject.blueprints import api, root
from myproject.repository import db
from myproject.repository.model import User
from myproject import containers

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    stmt = select(User).where(User.id == user_id)
    result = db.Session.scalars(stmt).first()
    return result


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    root.register_blueprints(app)
    api.register_blueprints(app)

    container = containers.App()
    container.config.from_dict(app.config)
    container.init_resources()
    container.wire(modules=[
        "myproject.healthchecks",
    ])
    app.container = container
    return app
