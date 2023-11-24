from datetime import datetime
from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.orm import scoped_session

from myproject.domain.datatypes import Post
from myproject.domain.interfaces.usecases import (
    ICreatePost, IDeletePost, IGetPost, IGetPosts, IUpdatePost,
)
from myproject.repository.model import Post as PostModel


class CreatePost(ICreatePost):
    def __init__(self, session: scoped_session):
        self.session = session

    def execute(self, post: Post):
        post.created = post.updated = datetime.utcnow()
        new_post = PostModel(
            title=post.title,
            content=post.content,
            author_id=post.author.id,
            created=post.created,
            updated=post.updated,
        )
        self.session.add(new_post)
        self.session.flush()
        post.id = new_post.id


class DeletePost(IDeletePost):
    def __init__(self, session: scoped_session):
        self.session = session

    def execute(self, post_id: str):
        stmt = update(PostModel).where(PostModel.id == post_id) \
            .values(
                updated=datetime.utcnow(),
                deleted=datetime.utcnow(),
            )
        self.session.execute(stmt)


class GetPost(IGetPost):
    def __init__(self, session: scoped_session):
        self.session = session

    def execute(self, post_id: str) -> Post:
        stmt = select(PostModel).where(PostModel.id == post_id)
        result = self.session.scalars(stmt).first()
        if result is None:
            return None
        return Post.from_dict({
            col.name: getattr(result, col.name)
            for col in PostModel.__table__.columns
        })


class GetPosts(IGetPosts):
    def execute(self) -> Sequence[Post]:
        pass


class UpdatePost(IUpdatePost):
    def __init__(self, session: scoped_session):
        self.session = session

    def execute(self, post: Post):
        stmt = update(PostModel).where(PostModel.id == post.id) \
            .values(
                title=post.title,
                content=post.content,
                updated=datetime.utcnow(),
            )
        self.session.execute(stmt)
