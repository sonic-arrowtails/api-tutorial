"""add content column to posts table

Revision ID: a8d4ec11c2f8
Revises: 580c9e9923d3
Create Date: 2025-06-30 23:02:49.450293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8d4ec11c2f8'
down_revision: Union[str, Sequence[str], None] = '580c9e9923d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable = False))


def downgrade() -> None:
    op.drop_column("posts", "content")
