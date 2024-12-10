"""Create trigger

Revision ID: dd77b82be40c
Revises: 03c77835a4c3_
Create Date: 2024-12-10 21:06:20.670251

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dd77b82be40c"
down_revision: Union[str, None] = "03c77835a4c3_"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute(
        '''
            CREATE OR REPLACE FUNCTION validate_sneakers_insert() 
            RETURNS TRIGGER AS $$
            BEGIN
                -- Очистка пробелов в поле name и description
                NEW.name := TRIM(NEW.name);
                NEW.description := NULLIF(TRIM(NEW.description), '');

                -- Капитализация поля name
                NEW.name := INITCAP(NEW.name);

                -- Проверка и замена пустых строк в description на NULL
                IF NEW.description = '' THEN
                    NEW.description := NULL;
                END IF;

                -- Проверка отрицательных значений для price и size
                IF NEW.price < 0 THEN
                    RAISE EXCEPTION 'Цена не может быть отрицательной';
                END IF;

                IF NEW.size < 0 THEN
                    RAISE EXCEPTION 'Размер не может быть отрицательным';
                END IF;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER trg_validate_sneakers_insert
            BEFORE INSERT ON sneakers
            FOR EACH ROW
            EXECUTE FUNCTION validate_sneakers_insert();
        '''
    )

    op.execute(
        '''
            CREATE OR REPLACE FUNCTION validate_sneakers_update() 
            RETURNS TRIGGER AS $$
            BEGIN
                -- Очистка пробелов в поле name и description
                NEW.name := TRIM(NEW.name);
                NEW.description := NULLIF(TRIM(NEW.description), '');

                -- Капитализация поля name
                NEW.name := INITCAP(NEW.name);

                -- Проверка и замена пустых строк в description на NULL
                IF NEW.description = '' THEN
                    NEW.description := NULL;
                END IF;

                -- Проверка отрицательных значений для price и size
                IF NEW.price < 0 THEN
                    RAISE EXCEPTION 'Цена не может быть отрицательной';
                END IF;

                IF NEW.size < 0 THEN
                    RAISE EXCEPTION 'Размер не может быть отрицательным';
                END IF;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER trg_validate_sneakers_update
            BEFORE UPDATE ON sneakers
            FOR EACH ROW
            EXECUTE FUNCTION validate_sneakers_update();
        '''
    )


def downgrade() -> None:
    op.execute(
        '''
            DROP TRIGGER IF EXISTS trg_validate_sneakers_insert ON sneakers;
            DROP FUNCTION IF EXISTS validate_sneakers_insert;
            DROP TRIGGER IF EXISTS trg_validate_sneakers_update ON sneakers;
            DROP FUNCTION IF EXISTS validate_sneakers_update;
        '''
    )