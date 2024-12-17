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
    # Триггер — это специальный объект базы данных, который автоматически выполняет определенный набор действий в ответ на определенные события (хранятся в сист каталогах базы (pg_trigger))
    # plpgsql процедурный язык PostgreSQL (нужный для написания триггеров, есть условия, отправка эксепшенов, циклы и тд.)
    op.execute(
        '''
            CREATE VIEW receipt_view AS 
            SELECT 
                o.id AS o_id,
                o.name_customer AS c_name, 
                o.order_date AS o_date, 
                p.date AS p_date, 
                SUM(os.quantity * os.price) AS total_price,
                STRING_AGG(s.name || ' (' ||  os.quantity || ')', ', ') AS sneakers_list,          -- Список товаров с количеством (обьединяет все строки из одной группы в одну строку)
                o.status AS o_status,
                pa.name AS p_name, 
                o.pickup_code AS p_code 
            FROM orders o
            JOIN orders_sneakers os ON os.order_id = o.id
            JOIN sneakers s ON s.id = os.sneaker_id
            JOIN brands b ON b.id = s.brand_id 
            JOIN payment p ON p.id = o.id 
            JOIN providers pa ON pa.id = p.provider_id 
            GROUP BY o.id, o.name_customer, o.order_date, p.date, o.status, pa.name, o.pickup_code::TEXT;    -- postgresql не может группировать json без явного преобразования
        '''
    )


    # op.execute(
    #     '''
    #         CREATE OR REPLACE FUNCTION insert_into_sneakers_orders_view()
    #         RETURNS TRIGGER AS $$
    #         BEGIN
    #             INSERT INTO sneakers (id, name, price, size, description)
    #             VALUES (NEW.sneaker_id, NEW.sneaker_name, NEW.sneaker_price, NEW.sneaker_size, NEW.sneaker_description);

    #             INSERT INTO orders_sneakers (sneaker_id, order_id, quantity, price)
    #             VALUES (NEW.sneaker_id, NEW.order_id, NEW.order_quantity, NEW.order_price);

    #             RETURN NEW;
    #         END;
    #         $$ LANGUAGE plpgsql;

    #         CREATE TRIGGER insert_into_sneakers_orders_view_trigger
    #         INSTEAD OF INSERT ON sneakers_orders_view
    #         FOR EACH ROW
    #         EXECUTE FUNCTION insert_into_sneakers_orders_view();
    #     '''
    # )


    # op.execute(
    #     '''
    #         CREATE OR REPLACE FUNCTION update_view()
    #         RETURNS TRIGGER AS $$ 
    #         BEGIN
    #             UPDATE sneakers
    #             SET name = NEW.sneaker_name, 
    #                 price = NEW.sneaker_price, 
    #                 size = NEW.sneaker_size, 
    #                 description = NEW.sneaker_description
    #             WHERE id = NEW.sneaker_id;

    #             UPDATE orders_sneakers
    #             SET quantity = NEW.order_quantity, 
    #                 price = NEW.order_price
    #             WHERE sneaker_id = NEW.sneaker_id;

    #             RETURN NEW;
    #         END;
    #         $$ LANGUAGE plpgsql;

    #         CREATE TRIGGER update_view_trigger
    #         INSTEAD OF UPDATE ON receipt_view
    #         FOR EACH ROW
    #         EXECUTE FUNCTION update_view();
    #     '''
    # )


    # op.execute(
    #     '''
    #         CREATE OR REPLACE FUNCTION delete_from_sneakers_orders_view()
    #         RETURNS TRIGGER AS $$ 
    #         BEGIN
    #             DELETE FROM sneakers WHERE id = OLD.sneaker_id;
    #             DELETE FROM orders_sneakers WHERE sneaker_id = OLD.sneaker_id;

    #             RETURN OLD;
    #         END;
    #         $$ LANGUAGE plpgsql;

    #         CREATE TRIGGER delete_from_sneakers_orders_view_trigger
    #         INSTEAD OF DELETE ON sneakers_orders_view
    #         FOR EACH ROW
    #         EXECUTE FUNCTION delete_from_sneakers_orders_view();
    #     '''
    # )



    #! брать или за год, или за последние 12 месяцев, нарастающий джоход, проверка на продаваемость, изменить оконную функцию
    op.execute(
        '''
            CREATE MATERIALIZED VIEW marketability_view AS
            WITH months AS (                                           -- создаем последовательность для показа месяцев
                SELECT generate_series(1, 12) AS month
            ),
            brands_data AS (
                SELECT
                    DATE_PART('month', o.order_date)::INTEGER AS month,    -- извлекаем месяц как число
                    b.name AS brand_name,
                    SUM(os.quantity) AS sneakers_sold,                  -- кол-во проданных пар
                    SUM(os.quantity * os.price) AS revenue              -- доход
                FROM sneakers s
                JOIN orders_sneakers os ON os.sneaker_id = s.id
                JOIN orders o ON o.id = os.order_id
                JOIN brands b ON b.id = s.brand_id
                JOIN payment p ON p.id = o.id
                WHERE EXTRACT(YEAR FROM o.order_date) = EXTRACT(YEAR FROM CURRENT_DATE) AND 
                      o.status <> 'Canceled' AND
                      p.id = o.id
                GROUP BY month, b.name
            ),
            -- brands_rank AS (                                          -- задаем каждому брэнду ранг (для получения самого популярного за месяц)
            --     SELECT
            --         month,
            --         brand_name,
            --         sneakers_sold,
            --         RANK() OVER (PARTITION BY month ORDER BY sneakers_sold DESC) AS rank
            --         -- делим данные на группы по месяцам (каждый месяц отдельно)
            --         -- далее сортируем по убыванию проданных пар и присваиваем ранг
            --         -- ранги полезнее, потому что можно получить не только лидера, но и топ-3 скажем (а так можно лимитом брать первый после сорта)
            --     FROM brands_data
            -- ),
            cumulative_data AS (
                 SELECT 
                    m.month,
                    SUM(COALESCE(SUM(bd.revenue), 0)) OVER (ORDER BY m.month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue
                    -- суммируем доход по брендам для каждого месяца
                    -- UNBOUNDED PRECEDING - окно с первой строки
                    -- CURRENT ROW - до текущего месяца
                FROM months m
                LEFT JOIN brands_data bd ON bd.month = m.month   -- месяцы без данных, чтобы включались
                GROUP BY m.month
            ),
            month_data AS (
                SELECT
                    m.month,
                    COALESCE(SUM(bd.sneakers_sold), 0) AS total_sneakers_sold,   -- заменяет NULL на 0, если данных за месяц нет
                    COALESCE(SUM(bd.revenue), 0) AS total_revenue,
                    cd.cumulative_revenue AS cumulative_revenue
                FROM months m
                LEFT JOIN brands_data bd ON bd.month = m.month                   -- LEFT JOIN чтобы входили и месяцы в которых, продаж не было
                LEFT JOIN cumulative_data cd ON cd.month = m.month
                GROUP BY m.month, cd.cumulative_revenue
            )
            SELECT
                month,
                total_sneakers_sold,
                total_revenue,
                cumulative_revenue
            FROM month_data
            ORDER BY month;
        '''
    )




def downgrade() -> None:
    # op.execute("DROP TRIGGER IF EXISTS insert_into_sneakers_orders_view ON receipt_view;")
    # op.execute("DROP TRIGGER IF EXISTS update_view ON receipt_view;")
    # op.execute("DROP TRIGGER IF EXISTS delete_from_sneakers_orders_view ON receipt_view;")
    op.execute("DROP VIEW IF EXISTS receipt_view;")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS marketability_view;")
