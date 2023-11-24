from abc import ABC, abstractmethod
from typing import Sequence

from myproject.domain.datatypes import NewUser, User, UserCredential


class ILogin(ABC):
    @abstractmethod
    def execute(self, user_cred: UserCredential) -> User:
        raise NotImplementedError("TODO")


class ICreateUser(ABC):
    @abstractmethod
    def execute(self, user: NewUser):
        raise NotImplementedError("TODO")


class IDeleteUser(ABC):
    @abstractmethod
    def execute(self, user_id: str):
        raise NotImplementedError("TODO")


class IGetUser(ABC):
    @abstractmethod
    def execute(self, user_id: str) -> User:
        raise NotImplementedError("TODO")


class IGetUsers(ABC):
    @abstractmethod
    def execute(self) -> Sequence[User]:
        raise NotImplementedError("TODO")


class IUpdateUser(ABC):
    @abstractmethod
    def execute(self, user: User):
        raise NotImplementedError("TODO")


class IUpdateUserPassword(ABC):
    @abstractmethod
    def execute(self, user_cred: UserCredential):
        raise NotImplementedError("TODO")
