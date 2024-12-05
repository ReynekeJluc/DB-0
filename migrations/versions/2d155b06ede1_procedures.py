"""Procedures

Revision ID: 2d155b06ede1
Revises: 03c77835a4c3_
Create Date: 2024-12-05 18:09:08.015365

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2d155b06ede1"
down_revision: Union[str, None] = "03c77835a4c3_"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
