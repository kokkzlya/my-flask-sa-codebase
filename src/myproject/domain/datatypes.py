from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json
from flask_login import UserMixin
import dataclasses_json

dataclasses_json.cfg.global_config.encoders[datetime] = datetime.isoformat
dataclasses_json.cfg.global_config.decoders[datetime] = datetime.fromisoformat


@dataclass_json
@dataclass
class User:
    id: Optional[str] = field(default=None)
    name: str = field(default=None)
    email: str = field(default=None)
    username: str = field(default=None)
    created: Optional[datetime] = field(default=None)
    updated: Optional[datetime] = field(default=None)
    deleted: Optional[datetime] = field(default=None)


class AuthedUser(UserMixin):
    def __init__(self, user):
        self._user = user

    @property
    def id(self):
        return self.user.id

    @property
    def user(self):
        return self._user


@dataclass_json
@dataclass
class NewUser(User):
    password: str = field(default=None)


@dataclass_json
@dataclass
class UserCredential:
    user_id: str
    password: str


@dataclass_json
@dataclass
class Post:
    id: Optional[str] = field(default=None)
    title: str = field(default=None)
    content: str = field(default=None)
    author: Optional[User] = field(default=None)
    created: Optional[datetime] = field(default=None)
    updated: Optional[datetime] = field(default=None)
    deleted: Optional[datetime] = field(default=None)
