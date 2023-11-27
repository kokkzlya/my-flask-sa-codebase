from typing import Callable, Tuple
import logging

from redis import Redis
from sqlalchemy.orm import scoped_session
from sqlalchemy.sql import text

from myproject.domain.datatypes import (
    HealthcheckError, HealthcheckStatus, ServiceStatus,
)
from myproject.domain.interfaces.usecases import IHealthCheck

logger = logging.getLogger(__name__)


def redis_healthcheck(r: Redis) -> Tuple[bool, str]:
    try:
        r.ping()
        return True, None
    except Exception:
        return False, "Lost Redis connection"


def postgres_healthcheck(session: scoped_session) -> Tuple[bool, str]:
    try:
        session.execute(text("SELECT 1"))
        return True, None
    except Exception as e:
        logger.warn(e)
        return False, "Lost database connection"


class HealthCheck(IHealthCheck):
    def __init__(self, redis_client: Redis, session: scoped_session):
        self.redis_client = redis_client
        self.session = session

    def execute(self) -> HealthcheckStatus:
        healthcheckers: Tuple[str, Callable] = [
            ("redis", lambda: redis_healthcheck(self.redis_client), ),
            ("postgresql", lambda: postgres_healthcheck(self.session), ),
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
        return status
