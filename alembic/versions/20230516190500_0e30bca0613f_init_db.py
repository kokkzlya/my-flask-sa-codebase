"""init db

Revision ID: 0e30bca0613f
Revises: 
Create Date: 2023-05-16 19:05:43.448802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e30bca0613f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('banned_until', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('email', name=op.f('uq_user_email')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    op.create_table('post',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('published_at', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.String(length=36), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name=op.f('fk_post_author_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_post'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('user')
    # ### end Alembic commands ###