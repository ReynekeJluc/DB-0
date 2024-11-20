"""Insert data

Revision ID: 01a545279d17
Revises: d410cd44e60f
Create Date: 2024-11-20 19:13:37.206111

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "01a545279d17"
down_revision: Union[str, None] = "d410cd44e60f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    meta = sa.MetaData()  
    categories = sa.Table('categories', meta, autoload_with = op.get_bind())

    op.bulk_insert(
        categories, 
        [
            {"id": 1, "name": "Обувь", "path": "1"},
            {"id": 2, "name": "Мужская", "path": "1/2"},
            {"id": 3, "name": "Туфли", "path": "1/2/3"},
            {"id": 4, "name": "Дерби", "path": "1/2/3/4"},
            {"id": 5, "name": "Оксфорды", "path": "1/2/3/5"},
            {"id": 6, "name": "Лоферы", "path": "1/2/3/6"},
            {"id": 7, "name": "Монки", "path": "1/2/3/7"},
            {"id": 8, "name": "Сандалии", "path": "1/2/8"},
            {"id": 9, "name": "Кроссовки", "path": "1/2/9"},
            {"id": 10, "name": "Ботинки", "path": "1/2/10"},
            {"id": 11, "name": "Детская", "path": "1/11"},
            {"id": 12, "name": "Мальчики", "path": "1/11/12"},
            {"id": 13, "name": "Девочки", "path": "1/11/13"},
            {"id": 14, "name": "Женская", "path": "1/14"},
            {"id": 15, "name": "Сапоги", "path": "1/14/15"},
            {"id": 16, "name": "Лето", "path": "1/14/15/16"},
            {"id": 17, "name": "Зима", "path": "1/14/15/17"},
            {"id": 18, "name": "Туфли", "path": "1/14/18"},
            {"id": 19, "name": "Каблук", "path": "1/14/18/19"},
            {"id": 20, "name": "Танкетка", "path": "1/14/18/20"},
            {"id": 21, "name": "Кроссовки", "path": "1/14/21"},
        ]
    )
    op.execute("SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories));")

def downgrade() -> None:
    op.execute("TRUNCATE categories RESTART IDENTITY")
