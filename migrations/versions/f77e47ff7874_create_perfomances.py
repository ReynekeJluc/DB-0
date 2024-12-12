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
                s.name AS s_name,
                b.name AS b_name,
                o.name_customer AS c_name,
                o.order_date AS o_date,
                p.date AS p_date,
                os.quantity * os.price AS o_price,
                pa.name AS p_name,
                o.pickup_code AS p_code
            FROM sneakers s
            JOIN brands b ON b.id = s.brand_id
            JOIN orders_sneakers os ON os.sneaker_id = s.id
            JOIN orders o ON o.id = os.order_id
            JOIN payment p ON p.id = o.id
            JOIN providers pa ON pa.id = p.provider_id
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








    op.execute(
        '''
            CREATE MATERIALIZED VIEW marketability_view AS
            WITH months AS (
                SELECT generate_series(1, 12) AS month
            ),
            brand_stats AS (
                SELECT
                    EXTRACT(MONTH FROM o.order_date)::int AS month,
                    b.name AS brand_name,
                    SUM(os.quantity) AS sneakers_sold,
                    SUM(os.quantity * s.price) AS revenue
                FROM sneakers s
                JOIN orders_sneakers os ON os.sneaker_id = s.id
                JOIN orders o ON o.id = os.order_id
                JOIN brands b ON b.id = s.brand_id
                GROUP BY EXTRACT(MONTH FROM o.order_date), b.name
            ),
            ranked_brands AS (
                SELECT
                    month,
                    brand_name,
                    sneakers_sold,
                    RANK() OVER (PARTITION BY month ORDER BY sneakers_sold DESC) AS rank
                FROM brand_stats
            ),
            monthly_stats AS (
                SELECT
                    m.month,
                    COALESCE(SUM(bs.sneakers_sold), 0) AS total_sneakers_sold,
                    COALESCE(SUM(bs.revenue), 0) AS total_revenue,
                    (SELECT brand_name FROM ranked_brands rb WHERE rb.month = m.month AND rb.rank = 1) AS most_popular_brand
                FROM months m
                LEFT JOIN brand_stats bs ON bs.month = m.month
                GROUP BY m.month
            )
            SELECT
                month,
                total_sneakers_sold,
                total_revenue,
                COALESCE(most_popular_brand, 'No Data') AS most_popular_brand
            FROM monthly_stats
            ORDER BY month;
        '''
    )




def downgrade() -> None:
    # op.execute("DROP TRIGGER IF EXISTS insert_into_sneakers_orders_view ON receipt_view;")
    # op.execute("DROP TRIGGER IF EXISTS update_view ON receipt_view;")
    # op.execute("DROP TRIGGER IF EXISTS delete_from_sneakers_orders_view ON receipt_view;")
    op.execute("DROP VIEW IF EXISTS receipt_view;")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS marketability_view;")


    # CREATE MATERIALIZED VIEW marketability_view AS
            # SELECT
            #     DATE_TRUNC('month', o.order_date) AS month,
            #     SUM(os.quantity) AS total_sneakers_sold,  -- Общее количество проданных кроссовок
            #     SUM(os.quantity * s.price) AS total_revenue,  -- Общая выручка
            #     (
            #         SELECT b.name 
            #         FROM brands b 
            #         JOIN sneakers s2 ON b.id = s2.brand_id
            #         JOIN orders_sneakers os2 ON os2.sneaker_id = s2.id
            #         JOIN orders o2 ON o2.id = os2.order_id
            #         WHERE DATE_TRUNC('month', o2.order_date) = DATE_TRUNC('month', o.order_date)  -- Сравниваем с текущим месяцем
            #         GROUP BY b.name 
            #         ORDER BY SUM(os2.quantity) DESC
            #         LIMIT 1
            #     ) AS most_popular_brand  -- Наиболее продаваемый бренд
            # FROM sneakers s
            # JOIN orders_sneakers os ON os.sneaker_id = s.id
            # JOIN orders o ON o.id = os.order_id
            # GROUP BY month
            # ORDER BY month;