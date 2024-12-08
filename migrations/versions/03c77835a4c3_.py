"""empty message

Revision ID: 03c77835a4c3_
Revises: 87df4c39cb3b
Create Date: 2024-10-01 18:14:07.806461

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

order_status_enum = ENUM('Pending', 'Shipped', 'Delivered', 'Canceled',name='orderstatusenum')

# revision identifiers, used by Alembic.
revision: str = "03c77835a4c3_"
down_revision: Union[str, None] = "87df4c39cb3b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    meta = sa.MetaData()               # обьект содержащий в себе коллекцию всех таблиц бд, которые определены или загружаются в ходе выполнения 
    
    brands = sa.Table('brands', meta, autoload_with=op.get_bind())  # meta используется для связи таблицы с существующей бд, а в конце автоматическая подгрузка из бд структуры
    sneakers = sa.Table('sneakers', meta, autoload_with=op.get_bind())  # get_bind() используется для возврата текущего соединения с бд
    orders = sa.Table('orders', meta, autoload_with=op.get_bind())
    orders_sneakers = sa.Table('orders_sneakers', meta, autoload_with=op.get_bind())
    providers = sa.Table('providers', meta, autoload_with=op.get_bind())
    payment = sa.Table('payment', meta, autoload_with=op.get_bind())
    
    op.execute('TRUNCATE TABLE orders_sneakers, providers, payment, orders, sneakers, brands RESTART IDENTITY CASCADE')

    op.bulk_insert(               # op это обьект alembic для взаимодействий с бд в контексте миграций и это массовая вставка
        brands,
        [
            {'id': 1, 'name': "Reebok", 'description': "Иконический бренд с богатой историей."},
            {'id': 2, 'name': "Adidas", 'description': "Качественная обувь для профессиональных спортсменов."},
            {'id': 3, 'name': "Puma", 'description': "Стиль и инновации в каждой модели."},
            {'id': 4, 'name': "Fila", 'description': "Доступные цены без потери качества."},
            {'id': 5, 'name': "Converse", 'description': "Лидер в мире кроссовок и активной одежды."},
            {'id': 6, 'name': "Nike", 'description': "Экологичные материалы для ответственного потребления.!"},
            {'id': 7, 'name': "Demix", 'description': "Популярный среди молодежи и модников."},
            {'id': 8, 'name': "Asics", 'description': "Специальные коллекции для уникального стиля."},
            {'id': 9, 'name': "Kappa", 'description': "Комфорт и производительность в каждой паре."},
            {'id': 10, 'name': "Gucci", 'description': "Бренд, который вдохновляет на движение."},
        ]
    )
    op.execute("SELECT setval('brands_id_seq', (SELECT MAX(id) FROM brands));")  # Обновление последовательности brands

    op.bulk_insert(
        sneakers,
        [
            {'id': 2, 'size': 31, 'name': "Air Max", 'description': "Удобная обувь с хорошей амортизацией.", 'price': 120.00, 'brand_id': 3},
            {'id': 1, 'size': 30, 'name': "Club C Grounds", 'description': "Легкие и стильные кроссовки для бега.", 'price': 75.00, 'brand_id': 1},
            {'id': 3, 'size': 32, 'name': "UltraBoost", 'description': "Элегантный дизайн для повседневной носки.", 'price': 180.00, 'brand_id': 5},
            {'id': 4, 'size': 33, 'name': "Suede Classic", 'description': "Дышащая сетка, идеальная для лета.", 'price': 65.00, 'brand_id': 2},
            {'id': 5, 'size': 34, 'name': "574 Core", 'description': "Прочные материалы для долгого использования.", 'price': 80.00, 'brand_id': 4},
            {'id': 6, 'size': 35, 'name': "Gel-Lyte III", 'description': "Кроссовки с ярким логотипом на боках.", 'price': 100.00, 'brand_id': 8},
            {'id': 7, 'size': 36, 'name': "PLAY COMME DES GARCONS", 'description': "Отличное сцепление для активного отдыха.", 'price': 150.00, 'brand_id': 6},
            {'id': 8, 'size': 37, 'name': "Old Skool", 'description': "Спортивная обувь с уникальным цветовым решением.", 'price': 60.00, 'brand_id': 7},
            {'id': 9, 'size': 38, 'name': "Disruptor 2", 'description': "Мягкая подошва для комфорта и поддержки.", 'price': 85.00, 'brand_id': 10},
            {'id': 10, 'size': 39, 'name': "HOVR Phantom", 'description': "Идеальный выбор для тренировки и прогулок.", 'price': 110.00, 'brand_id': 9},
        ]
    )
    op.execute("SELECT setval('sneakers_id_seq', (SELECT MAX(id) FROM sneakers));")  # Обновление последовательности sneakers

    op.bulk_insert(
        orders,
        [
            {'id': 1, 'order_date': "2024-09-25 10:00:00", 'status': "Shipped", 'name_customer': "John",  'pickup_code': {}},
            {'id': 2, 'order_date': "2024-09-25 10:01:00", 'status': "Shipped", 'name_customer': "Maria", 'pickup_code': {}},
            {'id': 3, 'order_date': "2024-09-25 10:02:00", 'status': "Delivered", 'name_customer': "David", 'pickup_code': {}},
            {'id': 4, 'order_date': "2024-09-25 10:03:00", 'status': "Pending", 'name_customer': "Joseph", 'pickup_code': {}},
            {'id': 5, 'order_date': "2024-09-25 10:04:00", 'status': "Delivered", 'name_customer': "Robert", 'pickup_code': {}},
            {'id': 6, 'order_date': "2024-09-25 10:05:00", 'status': "Pending", 'name_customer': "Lola", 'pickup_code': {}},
            {'id': 7, 'order_date': "2024-09-25 10:06:00", 'status': "Delivered", 'name_customer': "Olga", 'pickup_code': {}}
        ]
    )
    op.execute("SELECT setval('orders_id_seq', (SELECT MAX(id) FROM orders));")  # Обновление последовательности orders

    op.bulk_insert(
        orders_sneakers,
        [
            {'order_id': 1, 'sneaker_id': 1, 'quantity': 1, 'price': 1000},
            {'order_id': 1, 'sneaker_id': 2, 'quantity': 3, 'price': 1200},
            {'order_id': 2, 'sneaker_id': 3, 'quantity': 100, 'price': 1300},
            {'order_id': 2, 'sneaker_id': 4, 'quantity': 2, 'price': 1400},
            {'order_id': 3, 'sneaker_id': 5, 'quantity': 1, 'price': 1500},
            {'order_id': 4, 'sneaker_id': 6, 'quantity': 1, 'price': 1600},
            {'order_id': 5, 'sneaker_id': 7, 'quantity': 1, 'price': 1700},
        ]
    )

    op.bulk_insert(
            providers,
            [
                {'id': 1, 'name': "Tinkoff", 'address': "Tink street 19", 'phone': "9384761991", 'email': "tink@mail.ru"},
                {'id': 2, 'name': "Alfa", 'address': "Alfa street 4", 'phone': "9892303018", 'email': "alfa@mail.ru"},
                {'id': 3, 'name': "Tochka", 'address': "Tochka street 15", 'phone': "9851932733", 'email': "tochka@mail.ru"},
                {'id': 4, 'name': "Sberbank", 'address': "Sber street 1", 'phone': "9000819862", 'email': "sber@mail.ru"},
                {'id': 5, 'name': "VTB", 'address': "VTB street 115", 'phone': "9854739322", 'email': "vtb@mail.ru"},
                {'id': 6, 'name': "Halva", 'address': "Halva street 115", 'phone': "9847089287", 'email': "halva@mail.ru"},
                {'id': 7, 'name': "Continental", 'address': "Continental street 41", 'phone': "9301982307", 'email': "continental@mail.ru"},
            ]
        )

    op.execute("SELECT setval('providers_id_seq', (SELECT MAX(id) FROM providers));")  # Обновление последовательности providers
    
    op.bulk_insert(
        payment,
        [
            {'id': 1, 'provider_id': 1, 'date': "2024-10-01 10:00:00"},
            {'id': 2, 'provider_id': 7, 'date': "2024-10-01 10:01:00"},
            {'id': 3, 'provider_id': 3, 'date': "2024-10-01 10:02:00"},
            {'id': 4, 'provider_id': 5, 'date': "2024-10-01 10:03:00"},
            {'id': 5, 'provider_id': 6, 'date': "2024-10-01 10:04:00"},
            {'id': 6, 'provider_id': 4, 'date': "2024-10-01 10:05:00"},
            {'id': 7, 'provider_id': 2, 'date': "2024-10-01 10:06:00"},
        ]
    )


    op.execute("SELECT setval('payment_id_seq', (SELECT MAX(id) FROM payment));")  # Обновление последовательности payment


def downgrade() -> None:
    op.execute("TRUNCATE providers RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE payment RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE orders_sneakers RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE orders RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE sneakers RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE brands RESTART IDENTITY CASCADE")

    op.execute("DROP TYPE IF EXISTS orderstatusenum CASCADE")