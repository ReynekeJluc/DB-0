"""Insert data

Revision ID: a5e8fd960f4c
Revises: f66257da5311
Create Date: 2024-11-12 16:30:43.439784

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a5e8fd960f4c"
down_revision: Union[str, None] = "f66257da5311"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    meta = sa.MetaData()  
    categories = sa.Table('categories', meta, autoload_with = op.get_bind())

    # Вставка данных
    op.bulk_insert(
        categories, 
        [
            {"id": 1, "name": "Обувь", "parent_id": None},
            {"id": 2, "name": "Мужская", "parent_id": 1},
            {"id": 3, "name": "Туфли", "parent_id": 2},
            {"id": 4, "name": "Дерби", "parent_id": 3},
            {"id": 5, "name": "Оксфорды", "parent_id": 3},
            {"id": 6, "name": "Лоферы", "parent_id": 3},
            {"id": 7, "name": "Монки", "parent_id": 3},
            {"id": 8, "name": "Сандалии", "parent_id": 2},
            {"id": 9, "name": "Кроссовки", "parent_id": 2},
            {"id": 10, "name": "Ботинки", "parent_id": 2},
            {"id": 11, "name": "Детская", "parent_id": 1},
            {"id": 12, "name": "Мальчики", "parent_id": 11},
            {"id": 13, "name": "Девочки", "parent_id": 11},
            {"id": 14, "name": "Женская", "parent_id": 1},
            {"id": 15, "name": "Сапоги", "parent_id": 14},
            {"id": 16, "name": "Лето", "parent_id": 15},
            {"id": 17, "name": "Зима", "parent_id": 15},
            {"id": 18, "name": "Туфли", "parent_id": 14},
            {"id": 19, "name": "Каблук", "parent_id": 18},
            {"id": 20, "name": "Танкетка", "parent_id": 18},
            {"id": 21, "name": "Кроссовки", "parent_id": 14},
        ]
    )
    op.execute("SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories));")


def downgrade() -> None:
    meta = sa.MetaData()  
    categories = sa.Table('categories', meta, autoload_with = op.get_bind())
		
    op.execute(categories.delete().where(categories.c.name == 'Обувь'))
