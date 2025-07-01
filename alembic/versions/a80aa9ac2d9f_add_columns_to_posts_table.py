"""add columns to posts table

Revision ID: a80aa9ac2d9f
Revises: a079690fc1b0
Create Date: 2025-07-01 15:23:19.771641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a80aa9ac2d9f'
down_revision: Union[str, Sequence[str], None] = 'a079690fc1b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(), server_default = 'TRUE', nullable = False))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('now()')))


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
