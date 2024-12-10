"""Create perfomances

Revision ID: f77e47ff7874
Revises: 03c77835a4c3_
Create Date: 2024-12-08 15:42:24.823225

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f77e47ff7874"
down_revision: Union[str, None] = "03c77835a4c3_"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создание представления для брендов и кроссовок
    op.execute(
        '''
            CREATE VIEW brand_sneaker_info AS
            SELECT 
                b.id AS brand_id,
                b.name AS brand_name,
                b.description AS brand_description,
                s.id AS sneaker_id,
                s.name AS sneaker_name,
                s.size AS sneaker_size,
                s.price AS sneaker_price,
                s.description AS sneaker_description
            FROM 
                brands b
            JOIN 
                sneakers s ON b.id = s.brand_id
            ORDER BY 
                b.name, s.name;
        '''
    )


    op.execute(
        '''
            CREATE OR REPLACE FUNCTION insert_into_brands_and_sneakers()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Вставляем данные в таблицу brands
                INSERT INTO brands (name, description)
                VALUES (NEW.brand_name, NEW.brand_description)
                RETURNING id INTO NEW.brand_id;
                
                -- Вставляем данные в таблицу sneakers
                INSERT INTO sneakers (name, size, price, description, brand_id)
                VALUES (NEW.sneaker_name, NEW.sneaker_size, NEW.sneaker_price, NEW.sneaker_description, NEW.brand_id)
                RETURNING id INTO NEW.sneaker_id;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER insert_into_brands_and_sneakers_trigger
            INSTEAD OF INSERT ON brand_sneaker_info
            FOR EACH ROW
            EXECUTE FUNCTION insert_into_brands_and_sneakers();
        '''
    )  

    op.execute(
        '''
            CREATE OR REPLACE FUNCTION update_brands_and_sneakers()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Обновляем данные в таблице brands
                UPDATE brands
                SET name = NEW.brand_name, description = NEW.brand_description
                WHERE id = NEW.brand_id;
                
                -- Обновляем данные в таблице sneakers
                UPDATE sneakers
                SET name = NEW.sneaker_name, size = NEW.sneaker_size, price = NEW.sneaker_price, description = NEW.sneaker_description
                WHERE id = NEW.sneaker_id;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER update_brands_and_sneakers_trigger
            INSTEAD OF UPDATE ON brand_sneaker_info
            FOR EACH ROW
            EXECUTE FUNCTION update_brands_and_sneakers();
        '''
    )

    op.execute(
        '''
            CREATE OR REPLACE FUNCTION delete_from_brands_and_sneakers()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Удаляем данные из таблицы sneakers
                DELETE FROM sneakers WHERE id = OLD.sneaker_id;
                
                -- Удаляем данные из таблицы brands
                DELETE FROM brands WHERE id = OLD.brand_id;

                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER delete_from_brands_and_sneakers_trigger
            INSTEAD OF DELETE ON brand_sneaker_info
            FOR EACH ROW
            EXECUTE FUNCTION delete_from_brands_and_sneakers();
        '''
    )


def downgrade() -> None:
    # Удаляем триггер для вставки данных в таблицы brands и sneakers
    op.execute(
        '''
            DROP TRIGGER IF EXISTS insert_into_brands_and_sneakers_trigger ON brand_sneaker_info;
            DROP FUNCTION IF EXISTS insert_into_brands_and_sneakers;
        '''
    )

    # Удаляем триггер для обновления данных в таблицах brands и sneakers
    op.execute(
        '''
            DROP TRIGGER IF EXISTS update_brands_and_sneakers_trigger ON brand_sneaker_info;
            DROP FUNCTION IF EXISTS update_brands_and_sneakers;
        '''
    )

    # Удаляем триггер для удаления данных из таблиц brands и sneakers
    op.execute(
        '''
            DROP TRIGGER IF EXISTS delete_from_brands_and_sneakers_trigger ON brand_sneaker_info;
            DROP FUNCTION IF EXISTS delete_from_brands_and_sneakers;
        '''
    )

    # Удаляем представление brand_sneaker_info
    op.execute(
        '''
            DROP VIEW IF EXISTS brand_sneaker_info;
        '''
    )
