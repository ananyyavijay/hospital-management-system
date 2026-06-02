"""create medical_records table

Revision ID: 0db7625ca731
Revises: 6dede1dbfe4f
Create Date: 2026-05-23 20:36:17.000039

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0db7625ca731'
down_revision: Union[str, Sequence[str], None] = '6dede1dbfe4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # op.create_table(
    #     'medical_records',

    #     sa.Column(
    #         'id',
    #         sa.Integer(),
    #         nullable=False
    #     ),

    #     sa.Column(
    #         'patient_id',
    #         sa.Integer(),
    #         nullable=False
    #     ),

    #     sa.Column(
    #         'doctor_id',
    #         sa.Integer(),
    #         nullable=False
    #     ),

    #     sa.Column(
    #         'diagnosis',
    #         sa.String(),
    #         nullable=False
    #     ),

    #     sa.Column(
    #         'prescription',
    #         sa.String(),
    #         nullable=False
    #     ),

    #     sa.Column(
    #         'notes',
    #         sa.String(),
    #         nullable=True
    #     ),

    #     sa.ForeignKeyConstraint(
    #         ['patient_id'],
    #         ['patients.id']
    #     ),

    #     sa.ForeignKeyConstraint(
    #         ['doctor_id'],
    #         ['doctors.id']
    #     ),

    #     sa.PrimaryKeyConstraint('id')
    # )
    pass


def downgrade() -> None:
    """Downgrade schema."""

    # op.execute("DROP TABLE IF EXISTS medical_records")
    pass