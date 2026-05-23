"""add medical_records table and doctor availability calendar

Revision ID: 6dede1dbfe4f
Revises: c585fa2113fc
Create Date: 2026-05-23 20:23:31.859856

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '6dede1dbfe4f'
down_revision: Union[str, Sequence[str], None] = 'c585fa2113fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add availability column to doctors
    op.add_column(
        'doctors',
        sa.Column(
            'availability',
            sa.JSON(),
            nullable=False,
            server_default='[]'
        )
    )

    # Remove temporary default
    op.alter_column(
        'doctors',
        'availability',
        server_default=None
    )

    # Remove old column
    op.drop_column('doctors', 'available_slots')

    # Create medical_records table
    op.create_table(
        'medical_records',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'patient_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'doctor_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'diagnosis',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'prescription',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'notes',
            sa.String(),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ['patient_id'],
            ['patients.id']
        ),

        sa.ForeignKeyConstraint(
            ['doctor_id'],
            ['doctors.id']
        ),

        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Drop medical_records table
    op.drop_table('medical_records')

    # Add back old column
    op.add_column(
        'doctors',
        sa.Column(
            'available_slots',
            postgresql.JSON(astext_type=sa.Text()),
            server_default=sa.text("'[]'::json"),
            autoincrement=False,
            nullable=False
        )
    )

    # Remove availability column
    op.drop_column('doctors', 'availability')