from flask import Flask
from flask_login import LoginManager
from sqlalchemy import select

from myproject.blueprints import api, root
from myproject.repository import db
from myproject.repository.model import User

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

    root.register_blueprints(app)
    api.register_blueprints(app)

    login_manager.init_app(app)

    return app
