from typing import Tuple
import logging

from dependency_injector.wiring import Provide, inject
from redis import Redis
from sqlalchemy.sql import text

from myproject.containers import App
from myproject.repository.db import Session

logger = logging.getLogger(__name__)


@inject
def redis_healthcheck(
        r: Redis = Provide[App.core.redis_client],
        ) -> Tuple[bool, str]:
    try:
        r.ping()
        return True, None
    except Exception:
        return False, "Lost Redis connection"


@inject
def postgres_healthcheck() -> Tuple[bool, str]:
    try:
        Session.execute(text("SELECT 1"))
        return True, None
    except Exception as e:
        logger.warn(e)
        return False, "Lost database connection"
