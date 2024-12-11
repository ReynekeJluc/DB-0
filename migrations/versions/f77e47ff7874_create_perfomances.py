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
    op.execute(
        '''
            CREATE VIEW sneakers_orders_view AS
            SELECT
                s.id AS sneaker_id,
                s.name AS sneaker_name,
                s.price AS sneaker_price,
                s.size AS sneaker_size,
                s.description AS sneaker_description,
                os.order_id AS order_id,
                os.quantity AS order_quantity,
                os.price AS order_price
            FROM sneakers s
            LEFT JOIN orders_sneakers os ON s.id = os.sneaker_id
        '''
    )


    op.execute(
        '''
            CREATE OR REPLACE FUNCTION insert_into_sneakers_orders_view()
            RETURNS TRIGGER AS $$ 
            BEGIN
                INSERT INTO sneakers (id, name, price, size, description)
                VALUES (NEW.sneaker_id, NEW.sneaker_name, NEW.sneaker_price, NEW.sneaker_size, NEW.sneaker_description);

                INSERT INTO orders_sneakers (sneaker_id, order_id, quantity, price)
                VALUES (NEW.sneaker_id, NEW.order_id, NEW.order_quantity, NEW.order_price);

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER insert_into_sneakers_orders_view_trigger
            INSTEAD OF INSERT ON sneakers_orders_view
            FOR EACH ROW
            EXECUTE FUNCTION insert_into_sneakers_orders_view();
        '''
    )


    op.execute(
        '''
            CREATE OR REPLACE FUNCTION update_sneakers_orders_view()
            RETURNS TRIGGER AS $$ 
            BEGIN
                UPDATE sneakers
                SET name = NEW.sneaker_name, 
                    price = NEW.sneaker_price, 
                    size = NEW.sneaker_size, 
                    description = NEW.sneaker_description
                WHERE id = NEW.sneaker_id;

                UPDATE orders_sneakers
                SET quantity = NEW.order_quantity, 
                    price = NEW.order_price
                WHERE sneaker_id = NEW.sneaker_id;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER update_sneakers_orders_view_trigger
            INSTEAD OF UPDATE ON sneakers_orders_view
            FOR EACH ROW
            EXECUTE FUNCTION update_sneakers_orders_view();
        '''
    )


    op.execute(
        '''
            CREATE OR REPLACE FUNCTION delete_from_sneakers_orders_view()
            RETURNS TRIGGER AS $$ 
            BEGIN
                DELETE FROM sneakers WHERE id = OLD.sneaker_id;
                DELETE FROM orders_sneakers WHERE sneaker_id = OLD.sneaker_id;

                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER delete_from_sneakers_orders_view_trigger
            INSTEAD OF DELETE ON sneakers_orders_view
            FOR EACH ROW
            EXECUTE FUNCTION delete_from_sneakers_orders_view();
        '''
    )








    op.execute(
        '''
            CREATE MATERIALIZED VIEW brand_sneaker_count AS
            SELECT
                b.id AS brand_id,
                b.name AS brand_name,
                COUNT(s.id) AS sneaker_count
            FROM brands b
            JOIN sneakers s ON b.id = s.brand_id
            GROUP BY b.id, b.name;
        '''
    )



def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS insert_into_sneakers_orders_view ON sneakers_orders_view;")
    op.execute("DROP TRIGGER IF EXISTS update_sneakers_orders_view ON sneakers_orders_view;")
    op.execute("DROP TRIGGER IF EXISTS delete_from_sneakers_orders_view ON sneakers_orders_view;")
    op.execute('DROP VIEW IF EXISTS sneakers_orders_view;')

    op.execute("DROP MATERIALIZED VIEW IF EXISTS brand_sneaker_count;")