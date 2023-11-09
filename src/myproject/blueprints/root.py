from dataclasses import field
from typing import Optional

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, Flask, jsonify
from marshmallow_dataclass import dataclass
from redis import Redis

from myproject.containers import App

bp = Blueprint("root", __name__)


@bp.route("/", methods=["GET"])
def landing():
    return "<h1>Hello, World!</h1>"


@dataclass
class ServiceStatus:
    status: str = field(default=None)
    error: Optional[str] = field(default=None)


@bp.route("/healthcheck", methods=["GET"])
@inject
def health_check(
        r: Redis = Provide[App.core.redis_client],
        ):
    redis_status = ServiceStatus()
    try:
        r.ping()
        redis_status.status = "Successful"
    except Exception:
        redis_status.status = "Unavailable"
        redis_status.error = "Cannot connect to Redis"

    postgres_status = ServiceStatus()

    return jsonify({
        'redis_status': ServiceStatus.Schema().dump(redis_status),
    })


def register_blueprints(app: Flask):
    app.register_blueprint(bp)
