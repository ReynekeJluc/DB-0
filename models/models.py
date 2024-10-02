from sqlalchemy import MetaData, Table, Column, Integer, String, Text, TIMESTAMP, func, Numeric, ForeignKey

metaData = MetaData();

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
	Column("brand_id", Integer, ForeignKey("brands.id"), nullable=False),
)

orders = Table(
	"orders",
	metaData,
	Column("id", Integer, primary_key=True),
	Column("name_customer", String(255), nullable=False),
	Column("pickup_code", String(30), nullable=False),
	Column("order_date", TIMESTAMP, server_default=func.now()),                        #текущие дата и время данного компьютера
)

order_sneakers = Table(
	"orders_sneakers",
	metaData,
	Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),           #обеспечивает уникальность каждой комбинации
	Column("sneaker_id", Integer, ForeignKey("sneakers.id"), primary_key=True),
	Column("quantity", Integer, nullable=False, default=1),
	Column("price", Numeric(10, 2), nullable=False),
)

payment = Table(
	"payment",
	metaData,
	Column("id", Integer, primary_key=True),
	Column("status", String(50), nullable=False),
	Column("provider", String(255), nullable=False),
	Column("date", TIMESTAMP, server_default=func.now()),
	Column("order_id", Integer, ForeignKey("orders.id"), nullable=False ),
)
