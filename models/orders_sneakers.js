import { DataTypes } from 'sequelize';

export default function (sequelize) {
	return sequelize.define(
		'orders_sneakers',
		{
			order_id: {
				type: DataTypes.INTEGER,
				allowNull: false,
				references: {
					model: 'orders',
					key: 'id',
				},
				primaryKey: true,
			},
			sneaker_id: {
				type: DataTypes.INTEGER,
				allowNull: false,
				references: {
					model: 'sneakers',
					key: 'id',
				},
				primaryKey: true,
			},
			quantity: {
				type: DataTypes.INTEGER,
				allowNull: false,
				validate: {
					min: 0,
				},
			},
			price: {
				type: DataTypes.DECIMAL(10, 2),
				allowNull: false,
				validate: {
					min: 0,
				},
			},
		},
		{
			tableName: 'orders_sneakers',
			schema: 'public',
			timestamps: false,
		}
	);
}
