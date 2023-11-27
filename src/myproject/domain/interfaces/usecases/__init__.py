from .healthcheck import IHealthCheck
from .post import (
    ICreatePost, IDeletePost, IGetPost, IGetPosts, IUpdatePost,
)
from .user import (
    ICreateUser, IDeleteUser, IGetUser, IGetUsers, ILogin, IUpdateUser,
    IUpdateUserPassword,
)

__all__ = [
    "ICreatePost",
    "IDeletePost",
    "IGetPost",
    "IGetPosts",
    "IUpdatePost",
    "ICreateUser",
    "IDeleteUser",
    "IGetUser",
    "IGetUsers",
    "ILogin",
    "IUpdateUser",
    "IUpdateUserPassword",
    "IHealthCheck",
]
