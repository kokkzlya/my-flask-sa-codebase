from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class TimestampMixin(object):
    created: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: uuid4().hex)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    banned_until: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deleted: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class Post(Base, TimestampMixin):
    __tablename__ = "post"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: uuid4().hex)
    title: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    content: Mapped[str] = mapped_column(Text, nullable=True)
    published_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    author_id = mapped_column(ForeignKey("user.id"), nullable=True)
    deleted: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    author: Mapped[User] = relationship("User")
