"""add content column to posts table

Revision ID: 5369612ffab9
Revises: 7bc82eccf064
Create Date: 2025-10-31 22:00:20.119396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5369612ffab9'
down_revision: Union[str, Sequence[str], None] = '7bc82eccf064'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False, server_default=''))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
