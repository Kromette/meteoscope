"""add location coordinates unique constraint

Revision ID: b145bca668b3
Revises: 8fb0b1fa2c43
Create Date: 2026-09-17 14:03:07.963530

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b145bca668b3'
down_revision: str | Sequence[str] | None = '8fb0b1fa2c43'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_locations_coordinates",
        "locations",
        ["latitude", "longitude"]
        )


def downgrade() -> None:
    op.drop_constraint(
        "uq_locations_coordinates",
        "locations",
        type_="unique"
        )
