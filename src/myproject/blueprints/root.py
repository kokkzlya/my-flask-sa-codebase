from dataclasses import field
from typing import Callable, Optional, Tuple

from flask import Blueprint, Flask, Response
from marshmallow_dataclass import dataclass

from myproject.healthchecks import (
    postgres_healthcheck, redis_healthcheck,
)

bp = Blueprint("root", __name__)


@bp.route("/", methods=["GET"])
def landing():
    return "<h1>Hello, World!</h1>"


@dataclass
class HealthcheckError:
    error: str


@dataclass
class HealthcheckStatus:
    status: str = field(default=None)
    errors: Optional[list[HealthcheckError]] = field(default=None)
    services: list["ServiceStatus"] = field(default_factory=list)


@dataclass
class ServiceStatus:
    name: str = field(default=None)
    status: str = field(default=None)
    error: Optional[str] = field(default=None)


@bp.route("/healthcheck", methods=["GET"])
def health_check():
    healthcheckers: Tuple[str, Callable] = [
        ("redis", redis_healthcheck, ),
        ("postgresql", postgres_healthcheck, ),
    ]
    status = HealthcheckStatus()
    errs = []
    for healthchecker in healthcheckers:
        service_name, func = healthchecker
        ok, err = func()
        status.services.append(ServiceStatus(
            name=service_name,
            status="healthy" if ok else "unhealthy",
            error=err,
        ))
        if not ok:
            errs.append(HealthcheckError(error=err))

    status.status = "healthy" if len(errs) == 0 else "unhealthy"
    status.errors = errs if len(errs) > 0 else None
    return Response(
        status=200 if status.status == "healthy" else 500,
        content_type="application/json",
        response=HealthcheckStatus.Schema().dumps(status),
    )


def register_blueprints(app: Flask):
    app.register_blueprint(bp)
