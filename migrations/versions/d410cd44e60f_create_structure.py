"""Create structure

Revision ID: d410cd44e60f
Revises: 
Create Date: 2024-11-20 19:13:24.196223

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d410cd44e60f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table (
		'categories',
		sa.Column('id', sa.Integer, autoincrement = True, nullable = False),
		sa.Column('name', sa.String(255), nullable = False),
		sa.Column('path', sa.Text, nullable = False, unique = True),
            
    sa.PrimaryKeyConstraint('id'),
    sa.CheckConstraint('LENGTH(TRIM(name)) > 0', name='check_brand_name_not_empty')
  )


def downgrade() -> None:
    op.drop_table('categories')
