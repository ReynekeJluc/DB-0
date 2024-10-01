import { DataTypes } from 'sequelize';

export default function (sequelize) {
	return sequelize.define(
		'orders_sneakers',
		{
			order_id: {
				type: DataTypes.INTEGER,
				allowNull: false,
				primaryKey: true,
				references: {
					model: 'orders',
					key: 'id',
				},
			},
			sneaker_id: {
				type: DataTypes.INTEGER,
				allowNull: false,
				primaryKey: true,
				references: {
					model: 'sneakers',
					key: 'id',
				},
			},
			quantity: {
				type: DataTypes.INTEGER,
				allowNull: false,
			},
			price: {
				type: DataTypes.DECIMAL,
				allowNull: false,
			},
		},
		{
			tableName: 'orders_sneakers',
			schema: 'public',
			timestamps: false,
			indexes: [
				{
					name: 'orders_sneakers_pkey',
					unique: true,
					fields: [{ name: 'order_id' }, { name: 'sneaker_id' }],
				},
			],
		}
	);
}
