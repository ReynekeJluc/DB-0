from sqlalchemy import MetaData, Table, Column, Integer, String, Text, TIMESTAMP, func, Numeric, ForeignKey, Enum, JSON

metaData = MetaData();

class OrderStatus(Enum):
	PENDING = "Pending"
	SHIPPED = "Shipped"
	DELIVERED = "Delivered"
	CANCELED = "Canceled"

# primary_key=True 1) создание обьекта столбца 2) регистрация первичного ключа (регистрирует и обновляет внутренние структуры чтобы отметить столбец как отвечающий за уникальность) 3) генерируют схему sql 4) устанавливает ограничения (предотвращение null, обеспечение уникальности, создание индекса для улучшения производительности) 5) установка атрибутов на уровне orm (напримр генерация исключений при попытке создать с таким же id) 

brands = Table(
	"brands",
	metaData,
	Column("id", Integer, primary_key=True),
	Column("name", String(255), nullable=False),
	Column("description", Text, nullable=True),
)

sneakers = Table(
	"sneakers",
	metaData,
	Column("id", Integer, primary_key=True),
	Column("name", String(255), nullable=False),
	Column("price", Numeric(10, 2), nullable=False),
	Column("size", Numeric(3, 1), nullable=False),
	Column("description", Text, nullable=True),
	Column("brand_id", Integer, ForeignKey("brands.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
)

orders = Table(
	"orders",
	metaData,
	Column("id", Integer, primary_key=True),
	Column("name_customer", String(255), nullable=False),
	Column("pickup_code", JSON, nullable=False),
	Column("status", Enum(OrderStatus)),                                               # используем как кэш, а так высчитывать можно напрямую из данных таблицы
	Column("order_date", TIMESTAMP, server_default=func.now()),                        #текущие дата и время данного компьютера
)

order_sneakers = Table(
	"orders_sneakers",
	metaData,
	Column("order_id", Integer, ForeignKey("orders.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),           #обеспечивает уникальность каждой комбинации
	Column("sneaker_id", Integer, ForeignKey("sneakers.id", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
	Column("quantity", Integer, nullable=False, default=1),
	Column("price", Numeric(10, 2), nullable=False),
)

providers = Table(
	"providers",
	metaData,
	Column("id", Integer, primary_key=True),
	Column("name", String(255), nullable=False),
	Column("address", Text, nullable=False),
	Column("phone", String(10), nullable=False),
	Column("email", String(255), nullable=False),
)

payment = Table(
	"payment",
	metaData,
	Column("id", Integer, primary_key=True, ForeignKey("orders.id", ondelete='CASCADE', onupdate='CASCADE')),
	Column("date", TIMESTAMP, server_default=func.now()),
	Column("provider_id", Integer, ForeignKey("providers.id", ondelete='CASCADE', onupdate='CASCADE'),nullable=False),
)
