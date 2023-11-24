from abc import ABC, abstractmethod
from typing import Sequence

from myproject.domain.datatypes import NewUser, Post, User, UserCredential


class ICreatePost(ABC):
    @abstractmethod
    def execute(self, post: Post):
        raise NotImplementedError("TODO")


class IGetPost(ABC):
    @abstractmethod
    def execute(self, post_id: str):
        raise NotImplementedError("TODO")


class IGetPosts(ABC):
    @abstractmethod
    def execute(self) -> Sequence[Post]:
        raise NotImplementedError("TODO")


class IUpdatePost(ABC):
    @abstractmethod
    def execute(self, post: Post):
        raise NotImplementedError("TODO")


class IDeletePost(ABC):
    @abstractmethod
    def execute(self, post_id: str):
        raise NotImplementedError("TODO")


class ILogin(ABC):
    @abstractmethod
    def execute(self, user_cred: UserCredential) -> User:
        raise NotImplementedError("TODO")


class ICreateUser(ABC):
    @abstractmethod
    def execute(self, user: NewUser):
        raise NotImplementedError("TODO")


class IGetUser(ABC):
    @abstractmethod
    def execute(self, user_id: str) -> User:
        raise NotImplementedError("TODO")


class IHealthCheck(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError("TODO")
