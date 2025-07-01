"""add foreign key to posts table

Revision ID: a079690fc1b0
Revises: f51c04184f08
Create Date: 2025-07-01 15:17:02.087458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a079690fc1b0'
down_revision: Union[str, Sequence[str], None] = 'f51c04184f08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key("posts_users_fk",source_table='posts',referent_table='users',
                          local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
