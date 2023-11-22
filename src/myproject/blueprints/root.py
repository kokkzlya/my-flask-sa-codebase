from dependency_injector.wiring import Provide, inject
from flask import Blueprint, Flask, Response

from myproject.containers import App
from myproject.domain.interfaces.usecases import HealthCheck


bp = Blueprint("root", __name__)


@bp.route("/", methods=["GET"])
def landing():
    return "<h1>Hello, World!</h1>"


@bp.route("/healthcheck", methods=["GET"])
@inject
def health_check(hc: HealthCheck = Provide[App.usecases.healthcheck]):
    status = hc.execute()
    return Response(
        status=200 if status.status == "healthy" else 500,
        content_type="application/json",
        response=status.to_json(),
    )


def register_blueprints(app: Flask):
    app.register_blueprint(bp)
