
"""add available_slots to doctors

Revision ID: 403fccdc3661
Revises: 275a6c0ff27c
Create Date: 2026-05-21 17:04:06.837369

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '403fccdc3661'
down_revision: Union[str, Sequence[str], None] = '275a6c0ff27c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        'doctors',
        sa.Column(
            'available_slots',
            sa.JSON(),
            nullable=False,
            server_default='[]'
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column('doctors', 'available_slots')