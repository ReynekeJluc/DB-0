import { DataTypes } from 'sequelize';

export default function (sequelize) {
	return sequelize.define(
		'orders',
		{
			id: {
				autoIncrement: true,
				type: DataTypes.INTEGER,
				allowNull: false,
				primaryKey: true,
			},
			order_date: {
				type: DataTypes.DATE,
				allowNull: true,
				defaultValue: sequelize.fn('now'),
			},
		},
		{
			tableName: 'orders',
			schema: 'public',
			timestamps: false,
			indexes: [
				{
					name: 'orders_pkey',
					unique: true,
					fields: [{ name: 'id' }],
				},
			],
		}
	);
}
