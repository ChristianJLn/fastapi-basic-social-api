"""add foreign key to post table

Revision ID: 4510584de8f0
Revises: 1094d6468174
Create Date: 2026-06-10 17:25:55.375968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4510584de8f0'
down_revision: Union[str, Sequence[str], None] = '1094d6468174'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("post",
                  sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("post_user_fk",
                          source_table="post",
                          referent_table="user",
                          local_cols=["owner_id"],
                          remote_cols=["id"],
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_user_fk", table_name="post")
    op.drop_column("post", "owner_id")
    pass
