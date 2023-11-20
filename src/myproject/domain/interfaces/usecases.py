from abc import ABC, abstractmethod
from typing import Sequence

from myproject.domain.datatypes import Post, User, UserCredential


class CreatePost(ABC):
    @abstractmethod
    def execute(self, post: Post):
        raise NotImplementedError("TODO")


class GetPost(ABC):
    @abstractmethod
    def execute(self, post_id: str):
        raise NotImplementedError("TODO")


class GetPosts(ABC):
    @abstractmethod
    def execute(self) -> Sequence[Post]:
        raise NotImplementedError("TODO")


class UpdatePost(ABC):
    @abstractmethod
    def execute(self, post: Post):
        raise NotImplementedError("TODO")


class DeletePost(ABC):
    @abstractmethod
    def execute(self, post_id: str):
        raise NotImplementedError("TODO")


class Login(ABC):
    @abstractmethod
    def execute(self, user_cred: UserCredential) -> User:
        raise NotImplementedError("TODO")
