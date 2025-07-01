"""add user table

Revision ID: f51c04184f08
Revises: a8d4ec11c2f8
Create Date: 2025-07-01 15:05:06.389169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f51c04184f08'
down_revision: Union[str, Sequence[str], None] = 'a8d4ec11c2f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable = False), #  primary_key = True,
                    sa.Column('email',sa.String(255), nullable = False), # unique = True
                    sa.Column('password',sa.String(), nullable = False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
