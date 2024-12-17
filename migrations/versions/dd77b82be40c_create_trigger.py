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
                NEW.name := regexp_replace(TRIM(NEW.name), '\s+', ' ', 'g');
                NEW.description := NULLIF(regexp_replace(TRIM(NEW.description), '\s+', ' ', 'g'), '');
                
                IF LENGTH(NEW.name) = 0 THEN
                    RAISE EXCEPTION 'Название не может состоять из пустой строки или набора пробелов';
                END IF;

                IF NOT REGEXP_LIKE (NEW.name, '[a-zA-Z0-9]') THEN
                    RAISE EXCEPTION 'Название должно состоять из латинских букв и чисел';
                END IF;

                IF NEW.price is NULL THEN
                    RAISE EXCEPTION 'Цена не введена';
                END IF;

                IF NEW.price < 0 THEN
                    RAISE EXCEPTION 'Цена не может быть отрицательной';
                END IF;

                IF NEW.size IS NULL THEN
                    RAISE EXCEPTION 'Размер не введен';
                END IF;

                IF NEW.size < 26 OR NEW.size > 76 THEN
                    RAISE EXCEPTION 'Размер должен быть в диапазоне 26 - 76';
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
                NEW.name := regexp_replace(TRIM(NEW.name), '\s+', ' ', 'g');
                NEW.description := NULLIF(regexp_replace(TRIM(NEW.description), '\s+', ' ', 'g'), '');

                IF LENGTH(NEW.name) = 0 THEN
                    RAISE EXCEPTION 'Название не может состоять из пустой строки или набора пробелов';
                END IF;

                IF NOT REGEXP_LIKE (NEW.name, '[a-zA-Z0-9]') THEN
                    RAISE EXCEPTION 'Название должно состоять из латинских букв и чисел';
                END IF;

                
                IF NEW.price is NULL THEN
                    RAISE EXCEPTION 'Цена не введена';
                END IF;

                IF NEW.price < 0 THEN
                    RAISE EXCEPTION 'Цена не может быть отрицательной';
                END IF;

                IF NEW.size IS NULL THEN
                    RAISE EXCEPTION 'Размер не введен';
                END IF;

                IF NEW.size < 26 OR NEW.size > 76 THEN
                    RAISE EXCEPTION 'Размер должен быть в диапазоне 26 - 76';
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
