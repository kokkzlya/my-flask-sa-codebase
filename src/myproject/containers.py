from dependency_injector import containers, providers
from redis import ConnectionPool as RedisConnectionPool, Redis


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()

    redis_pool = providers.Singleton(
        RedisConnectionPool.from_url, config.REDIS_URL,
    )
    redis_client = providers.Singleton(
        Redis, connection_pool=redis_pool,
    )


class App(containers.DeclarativeContainer):
    config = providers.Configuration()

    core = providers.Container(Core, config=config)
