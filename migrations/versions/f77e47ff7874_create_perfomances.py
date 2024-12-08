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
    # Представление на получение данных о платежах с информацией о заказах и связанных провайдерах
    op.execute(
    '''
        CREATE VIEW provider_payment_info AS
        SELECT 
            o.id AS order_id,
            pa.id AS payment_id,
            o.name_customer,
            o.order_date::TEXT,
            pa.date::TEXT,
            o.status,
            p.name
        FROM 
            payment pa
        JOIN 
            orders o ON pa.id = o.id
        JOIN 
            providers p ON pa.provider_id = p.id;
    ''')

    #Триггер для вставки 
    op.execute(
        '''
            CREATE OR REPLACE FUNCTION provider_payment_insert()
            RETURNS TRIGGER AS $$
            BEGIN
                INSERT INTO payment(provider_id, date)
                VALUES (NEW.provider_id, NEW.payment_date)
                RETURNING id INTO NEW.payment_id;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER provider_payment_insert_trigger
            INSTEAD OF INSERT ON provider_payment_info
            FOR EACH ROW    
            EXECUTE FUNCTION provider_payment_insert();
        '''
    )

    # Триггер для обновления
    op.execute(
        '''
            CREATE OR REPLACE FUNCTION provider_payment_update() 
            RETURNS TRIGGER AS $$
            BEGIN
                UPDATE payment
                SET provider_id = NEW.provider_id, date = NEW.payment_date
                WHERE id = NEW.payment_id;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER provider_payment_update_trigger
            INSTEAD OF UPDATE ON provider_payment_info
            FOR EACH ROW
            EXECUTE FUNCTION provider_payment_update();
        '''
    )

    # Триггер для удаления
    op.execute(
        '''
            CREATE OR REPLACE FUNCTION provider_payment_delete() 
            RETURNS TRIGGER AS $$
            BEGIN
                DELETE FROM payment WHERE id = OLD.payment_id;

                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER provider_payment_delete_trigger
            INSTEAD OF DELETE ON provider_payment_info
            FOR EACH ROW
            EXECUTE FUNCTION provider_payment_delete();
        '''
    )


    op.execute(
        '''
            CREATE MATERIALIZED VIEW sneakers_sales_stats AS
            SELECT
                s.id AS sneaker_id,
                s.name AS sneaker_name,
                b.name AS brand_name,
                SUM(os.quantity * os.price) AS total_sales,  -- Общее количество проданных единиц * цена
                COUNT(os.order_id) AS total_orders,  -- Общее количество заказов для этой модели
                RANK() OVER (ORDER BY SUM(os.quantity * os.price) DESC) AS sales_rank  -- Рейтинг по доходу
            FROM
                sneakers s
            JOIN
                orders_sneakers os ON s.id = os.sneaker_id
            JOIN
                orders o ON os.order_id = o.id
            JOIN
                brands b ON s.brand_id = b.id
            GROUP BY
                s.id, s.name, b.name
            ORDER BY
                total_sales DESC;
        '''
    )

    op.execute(
        '''
            CREATE OR REPLACE FUNCTION refresh_sneakers_sales_stats()
            RETURNS TRIGGER AS $$
            BEGIN
                REFRESH MATERIALIZED VIEW sneakers_sales_stats;
                RETURN NULL;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER sneakers_sales_update_trigger
            AFTER INSERT OR UPDATE OR DELETE ON orders_sneakers
            FOR EACH STATEMENT
            EXECUTE FUNCTION refresh_sneakers_sales_stats();

            CREATE TRIGGER sneakers_sales_update_trigger_orders
            AFTER INSERT OR UPDATE OR DELETE ON orders
            FOR EACH STATEMENT
            EXECUTE FUNCTION refresh_sneakers_sales_stats();

            CREATE TRIGGER sneakers_sales_update_trigger_sneakers
            AFTER INSERT OR UPDATE OR DELETE ON sneakers
            FOR EACH STATEMENT
            EXECUTE FUNCTION refresh_sneakers_sales_stats();
        '''
    )


def downgrade() -> None:
    # Удаление триггеров
    op.execute("DROP TRIGGER IF EXISTS provider_payment_delete_trigger ON provider_payment_info;")
    op.execute("DROP TRIGGER IF EXISTS provider_payment_update_trigger ON provider_payment_info;")
    op.execute("DROP TRIGGER IF EXISTS provider_payment_insert_trigger ON provider_payment_info;")

    # Удаление функций для триггеров
    op.execute("DROP FUNCTION IF EXISTS provider_payment_insert();")
    op.execute("DROP FUNCTION IF EXISTS provider_payment_update();")
    op.execute("DROP FUNCTION IF EXISTS provider_payment_delete();")

    # Удаление представления
    op.execute("DROP VIEW IF EXISTS provider_payment_info;")
