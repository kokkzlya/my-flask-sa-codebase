from flask import Blueprint, Flask

bp = Blueprint("root", __name__)


@bp.route("/", methods=["GET"])
def landing():
    return "<h1>Hello, World!</h1>"


def register_blueprints(app: Flask):
    app.register_blueprint(bp)
