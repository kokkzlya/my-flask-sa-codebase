from dependency_injector import containers, providers
from redis import ConnectionPool as RedisConnectionPool, Redis

from myproject.repository.db import Session
from myproject.usecases.post import (
    CreatePost, DeletePost, GetPost, UpdatePost,
)
from myproject.usecases.user import Login


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()

    redis_pool = providers.Singleton(
        RedisConnectionPool.from_url, config.REDIS_URL,
    )
    redis_client = providers.Singleton(
        Redis, connection_pool=redis_pool,
    )
    session = providers.Object(Session)


class UseCases(containers.DeclarativeContainer):
    config = providers.Configuration()
    core = providers.DependenciesContainer()

    login = providers.Factory(Login, session=core.session)

    create_post = providers.Factory(CreatePost, session=core.session)
    update_post = providers.Factory(UpdatePost, session=core.session)
    delete_post = providers.Factory(DeletePost, session=core.session)
    get_post = providers.Factory(GetPost, session=core.session)


class App(containers.DeclarativeContainer):
    config = providers.Configuration()

    core = providers.Container(Core, config=config)

    usecases = providers.Container(UseCases, config=config, core=core)
