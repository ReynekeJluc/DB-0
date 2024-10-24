import { DataTypes } from 'sequelize';  // обьект содержащий все поддерживаемые типы данных ORM
import alembic_version from './alembic_version.js';
import brands from './brands.js';
import orders from './orders.js';
import orders_sneakers from './orders_sneakers.js';
import payment from './payment.js';
import providers from './providers.js';
import sneakers from './sneakers.js';

// Нужен для работы с моделями их импорта, экспорта и определением связей (для правильного создания запросов) 

export default function initModels(sequelize) {
	const alembic = alembic_version(sequelize, DataTypes);
	const brandModel = brands(sequelize, DataTypes);
	const orderModel = orders(sequelize, DataTypes);
	const orderSneakerModel = orders_sneakers(sequelize, DataTypes);
	const paymentModel = payment(sequelize, DataTypes);
	const sneakerModel = sneakers(sequelize, DataTypes);
	const providersModel = providers(sequelize, DataTypes);

	// Явная связь
	orderModel.belongsToMany(sneakerModel, {
		as: 'sneaker_id_sneakers',
		through: orderSneakerModel,
		foreignKey: 'order_id',
		otherKey: 'sneaker_id',
	});
	sneakerModel.belongsToMany(orderModel, {
		as: 'order_id_orders',
		through: orderSneakerModel,
		foreignKey: 'sneaker_id',
		otherKey: 'order_id',
	});

	// 1:N Sneakers - Brands
	sneakerModel.belongsTo(brandModel, {
		as: 'brand',
		foreignKey: 'brand_id',
	});
	brandModel.hasMany(sneakerModel, {
		as: 'sneakers',
		foreignKey: 'brand_id',
	});

	// 1:N Order_Sneakers - Orders && Order_Sneakers - Sneakers
	orderSneakerModel.belongsTo(orderModel, {
		as: 'order',
		foreignKey: 'order_id',
	});
	orderModel.hasMany(orderSneakerModel, {
		as: 'orders_sneakers',
		foreignKey: 'order_id',
	});

	orderSneakerModel.belongsTo(sneakerModel, {
		as: 'sneaker',
		foreignKey: 'sneaker_id',
	});
	sneakerModel.hasMany(orderSneakerModel, {
		as: 'orders_sneakers',
		foreignKey: 'sneaker_id',
	});

	// 0:1 Payment - Orders
	paymentModel.belongsTo(orderModel, {
		foreignKey: 'order_id',
		allowNull: true,
	});
	orderModel.hasOne(paymentModel, {
		foreignKey: 'order_id',
	});

	// 1:1 Payment - Providers
	paymentModel.belongsTo(providersModel, {
		as: 'provider',
		foreignKey: 'provider_id',
	});
	providersModel.hasOne(paymentModel, {
		as: 'payments',
		foreignKey: 'provider_id',
	});

	return {
		alembic,
		brands: brandModel,
		orders: orderModel,
		orders_sneakers: orderSneakerModel,
		payment: paymentModel,
		sneakers: sneakerModel,
	};
}
