from os import environ

_ = environ.get


class Base():
    SQL_URL = _("SQL_URL",
                "postgresql://myproject:myproject@localhost/myproject")
    SECRET_KEY = _("SECRET_KEY", "changepls")


class Development(Base):
    pass


class Production(Base):
    pass


class Testing(Base):
    pass
