import logging

from flask import Flask
from greenlet import getcurrent
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

logger = logging.getLogger(__name__)

naming_convention = {
    'ix': "ix_%(column_0_label)s",
    'uq': "uq_%(table_name)s_%(column_0_name)s",
    'ck': "ck_%(table_name)s_%(constraint_name)s",
    'fk': "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    'pk': "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=naming_convention)
Base = declarative_base(metadata=metadata)
session_factory = sessionmaker(autocommit=False, autoflush=True, bind=None)
Session = scoped_session(session_factory, scopefunc=getcurrent)


def init_app(app: Flask):
    engine = create_engine(app.config["SQL_URL"])
    Session.configure(bind=engine)

    # app.before_request(_before_request)
    # app.after_request(_after_request)

    # https://github.com/pallets-eco/flask-sqlalchemy/blob/main/src/flask_sqlalchemy/extension.py#L406
    app.teardown_appcontext(_teardown_session)


# def _before_request():
#     g.force_commit = False


# def _after_request(resp):
#     try:
#         if getattr(g, "force_commit", False) or resp.status_code < 400:
#             Session.commit()
#         else:
#             Session.rollback()
#     finally:
#         Session.close()
#         return resp


def _teardown_session(resp_or_exc):
    try:
        Session.remove()
    except Exception:
        pass
    return resp_or_exc
