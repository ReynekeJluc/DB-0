from sqlalchemy import MetaData, Table, Column, Integer, String, Text, TIMESTAMP, func, Numeric, ForeignKey, Enum, JSON, CheckConstraint, UniqueConstraint

metaData = MetaData();

class OrderStatus(Enum):
	PENDING = "Pending"
	SHIPPED = "Shipped"
	DELIVERED = "Delivered"
	CANCELED = "Canceled"

brands = Table(
	"brands",
	metaData,
	Column("id", Integer, primary_key=True),
	Column("name", String(255), nullable=False),
	Column("description", Text),
	CheckConstraint("LENGTH(TRIM(name)) > 0", name="check_brand_name_not_empty"),              # не пусты и не имеют лишние пробельные символы
	UniqueConstraint("name", name="uq_brand_name")                                             # брэнды уникальны
)

sneakers = Table(
	"sneakers",
	metaData,
	Column("id", Integer, primary_key=True),
	Column("name", String(255), nullable=False),
	Column("price", Numeric(10, 2), nullable=False),
	Column("size", Numeric(3, 1), nullable=False),
	Column("description", Text),
	Column("brand_id", Integer, ForeignKey("brands.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
	CheckConstraint('price >= 0', name='check_price_positive_1'),                # Ограничение на цену
    	CheckConstraint('size >= 16', name='check_size_positive'),                    # Ограничение на размер
)

orders = Table(
	"orders",
	metaData,
	Column("id", Integer, primary_key=True),
	Column("name_customer", String(255), nullable=False),
	Column("pickup_code", JSON),                                                       # используем как кэш, а так высчитывать можно напрямую из данных таблицы
	Column("status", Enum(OrderStatus.PENDING, OrderStatus.SHIPPED, OrderStatus.DELIVERED, OrderStatus.CANCELED), nullable=False),                                              
	Column("order_date", TIMESTAMP, server_default=func.now()),                        # текущие дата и время сервера
	CheckConstraint("LENGTH(TRIM(name_customer)) > 0", name="check_customer_name_not_empty")
)

order_sneakers = Table(
	"orders_sneakers",
	metaData,
	Column("order_id", Integer, ForeignKey("orders.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),           # обеспечивает уникальность каждой комбинации
	Column("sneaker_id", Integer, ForeignKey("sneakers.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
	Column("quantity", Integer, nullable=False, default=1),
	Column("price", Numeric(10, 2), nullable=False),
	CheckConstraint('quantity >= 1', name='check_quantity_positive'),     # Ограничение на количество
	CheckConstraint('price >= 0', name='check_price_positive_2'),         # Ограничение на цену
)

providers = Table(
	"providers",
	metaData,
	Column("id", Integer, primary_key=True),
	Column("name", String(255), nullable=False),
	Column("address", Text, nullable=False),
	Column("phone", String(10), nullable=False),
	Column("email", String(255), nullable=False),
	CheckConstraint("phone ~ '^[0-9]{10}$'", name="check_phone_format"),               # Проверка на 10-значный номер    ~ проверка соответствия   ^: начало строки.   [0-9]{10}: 10 цифр.   $: конец строки.
    	CheckConstraint("email ~ '^[^@]+@[^@]+\\.[^@]+$'", name="check_email_format"),     # Проверка формата электронной почты   Этот шаблон будет соответствовать любой строке, содержащей один или несколько символов, не являющихся символом @, за которым следует символ @, за которым следует один или несколько символов, не являющихся символом @, за которым следует точка, за которой следует один или несколько символов, не являющихся символом @.
)       # Использование ^ и $ делает выражение более строгим, гарантируя, что строка полностью соответствует шаблону
        # Одинарный обратный слэш (\) имеет специальное значение в строках и используется для экранирования других символов. Чтобы указать на один обратный слэш (\), нужно использовать двойной обратный слэш (\\).
        # Таким образом, для регулярного выражения в строке Python, чтобы указать точку как символ, нужно использовать \\.
payment = Table(
	"payment",
	metaData,
	Column("id", Integer, ForeignKey("orders.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
	Column("date", TIMESTAMP, server_default=func.now()),
	Column("provider_id", Integer, ForeignKey("providers.id", ondelete='CASCADE', onupdate='CASCADE'),nullable=False),
)




#UniqueConstraint("email", name="uq_provider_email"),
#UniqueConstraint("phone", name="uq_provider_phone"),
