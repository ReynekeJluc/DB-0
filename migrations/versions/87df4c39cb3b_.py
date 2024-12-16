"""empty message

Revision ID: 87df4c39cb3b
Revises: 
Create Date: 2024-10-01 18:10:06.616807

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import CITEXT

order_status_enum = sa.Enum('Pending', 'Shipped', 'Delivered', 'Canceled', name='orderstatusenum')

# revision identifiers, used by Alembic.
revision: str = "87df4c39cb3b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.execute("CREATE EXTENSION IF NOT EXISTS citext")   # добавление расширения

    op.create_table(
        "brands",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", CITEXT(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("LENGTH(TRIM(name)) > 0", name="check_brand_name_not_empty"),
        sa.UniqueConstraint("name", name="uq_brand_name"),
    )

    # Триггер — это специальный объект базы данных, который автоматически выполняет определенный набор действий в ответ на определенные события (хранятся в сист каталогах базы (pg_trigger))
    # op.execute("""
    #     CREATE OR REPLACE FUNCTION check_unique_brand_name()   -- создание новой функции или перезапись такой же
    #     RETURNS TRIGGER AS $$                                  -- возвращение триггерного значения (она не будет что-то менять, но говорит что продолжит с вводимым значением) $$ - начало и конец текста функции
    #     BEGIN
    #         IF EXISTS (                                        -- собственно делаем проверку совпадения имени без учета регистра
    #             SELECT 1                          -- В контексте триггеров NEW представляет собой новую строку, которую пытаются вставить или обновить
    #             FROM brands                        -- мы просто хотим узнать есть ли хотябы 1 запись попадающая под наше условие
    #             WHERE LOWER(name) = LOWER(NEW.name) AND id != NEW.id
    #         ) THEN
    #             RAISE EXCEPTION 'Brand name "%s" already exists', NEW.name;     -- вызываем эксепшен   %s - спец символ вставки переменной
    #         END IF;
    #         RETURN NEW;                                        -- возвращаем нашу строку для продолжения работы
    #     END;
    #     $$ LANGUAGE plpgsql;           -- процедурный язык PostgreSQL (нужный для написания триггеров, есть условия, отправка эксепшенов, циклы и тд.)
    # """)

    # # Создание триггера
    # op.execute("""
    #     CREATE TRIGGER unique_brand_name_trigger  --собственно создаем триггер срабатывающий перед вставкой или обновлением и выполняющая функцию выше
    #     BEFORE INSERT OR UPDATE ON brands
    #     EXECUTE PROCEDURE check_unique_brand_name();
    # """)

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name_customer", sa.String(length=255), nullable=False),
        sa.Column("pickup_code", sa.JSON, nullable=False),
        sa.Column("status", order_status_enum),
        sa.Column(
            "order_date",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("LENGTH(TRIM(name_customer)) > 0", name="check_customer_name_not_empty")
    )
    op.create_table(
        "providers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("address", sa.Text(), nullable=False),
        sa.Column("phone", sa.String(length=10), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        # sa.CheckConstraint("phone ~ '^[0-9]{10}$'", name="check_phone_format"),
        # sa.CheckConstraint("email ~ '^[^@]+@[^@]+\\.[^@]+$'", name="check_email_format"),
        # sa.CheckConstraint("LENGTH(TRIM(name)) > 0", name="check_providers_name_not_empty"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_providers_name"),
    )
    op.create_table(
        "payment",
        sa.Column("id", sa.Integer(), autoincrement=True),
        sa.Column("provider_id", sa.Integer, nullable=False),
        sa.Column(
            "date",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["orders.id"],
            ondelete="CASCADE",
            onupdate='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ["provider_id"],
            ["providers.id"],
            ondelete="CASCADE",
            onupdate='CASCADE'
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sneakers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", CITEXT(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("size", sa.Numeric(precision=3, scale=1), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("brand_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["brand_id"],
            ["brands.id"],
            ondelete="SET NULL",
            onupdate='CASCADE'
        ),
        sa.PrimaryKeyConstraint("id"),
        # sa.UniqueConstraint("name", name="uq_sneakers_name"),
        # sa.CheckConstraint('price >= 0', name='check_price_positive_1'),
        # sa.CheckConstraint('size >= 0', name='check_size_positive'),
        # sa.CheckConstraint("LENGTH(TRIM(name)) > 0", name='check_name_length'),
        # sa.CheckConstraint("LENGTH(TRIM(description)) > 0", name='check_description_length')
    )
    op.create_table(
        "orders_sneakers",
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("sneaker_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
            ondelete="CASCADE",
            onupdate='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ["sneaker_id"],
            ["sneakers.id"],
            ondelete="CASCADE",
            onupdate='CASCADE'
        ),
        sa.PrimaryKeyConstraint("order_id", "sneaker_id"),
        sa.CheckConstraint('quantity >= 0', name='check_quantity_positive'),
        sa.CheckConstraint('price >= 0', name='check_price_positive_2'),
    )



    # ### end Alembic commands ###

# sa.UniqueConstraint("email", name="uq_provider_email"),
# sa.UniqueConstraint("phone", name="uq_provider_phone")


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    # Удаление триггера
    # op.execute("DROP TRIGGER IF EXISTS unique_brand_name_trigger ON brands;")
    
    # Удаление функции
    op.execute("DROP FUNCTION IF EXISTS check_unique_brand_name();")

    op.drop_table("payment")
    op.drop_table("providers")
    op.drop_table("orders_sneakers")
    op.drop_table("orders")
    op.drop_table("sneakers")
    op.drop_table("brands")

    op.execute("DROP TYPE IF EXISTS orderstatusenum CASCADE")
    op.execute("DROP EXTENSION IF EXISTS citext")
    # ### end Alembic commands ###
