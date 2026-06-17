"""add content column

Revision ID: 6fd9e74597d6
Revises: b881fa89a4f0
Create Date: 2026-06-10 16:32:17.689838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fd9e74597d6'
down_revision: Union[str, Sequence[str], None] = 'b881fa89a4f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("post", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("post", "content")
    pass
