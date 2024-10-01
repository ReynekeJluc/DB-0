import { DataTypes } from 'sequelize';
import alembic_version from './alembic_version.js';
import brands from './brands.js';
import orders from './orders.js';
import orders_sneakers from './orders_sneakers.js';
import payment from './payment.js';
import sneakers from './sneakers.js';

export default function initModels(sequelize) {
	const alembic = alembic_version(sequelize, DataTypes);
	const brandModel = brands(sequelize, DataTypes);
	const orderModel = orders(sequelize, DataTypes);
	const orderSneakerModel = orders_sneakers(sequelize, DataTypes);
	const paymentModel = payment(sequelize, DataTypes);
	const sneakerModel = sneakers(sequelize, DataTypes);

	// Определение связей между моделями
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
	sneakerModel.belongsTo(brandModel, { as: 'brand', foreignKey: 'brand_id' });
	brandModel.hasMany(sneakerModel, { as: 'sneakers', foreignKey: 'brand_id' });
	orderSneakerModel.belongsTo(orderModel, {
		as: 'order',
		foreignKey: 'order_id',
	});
	orderModel.hasMany(orderSneakerModel, {
		as: 'orders_sneakers',
		foreignKey: 'order_id',
	});
	paymentModel.belongsTo(orderModel, { as: 'order', foreignKey: 'order_id' });
	orderModel.hasMany(paymentModel, { as: 'payments', foreignKey: 'order_id' });
	orderSneakerModel.belongsTo(sneakerModel, {
		as: 'sneaker',
		foreignKey: 'sneaker_id',
	});
	sneakerModel.hasMany(orderSneakerModel, {
		as: 'orders_sneakers',
		foreignKey: 'sneaker_id',
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
