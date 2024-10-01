import { DataTypes } from 'sequelize';

export default function (sequelize) {
	return sequelize.define(
		'payment',
		{
			id: {
				autoIncrement: true,
				type: DataTypes.INTEGER,
				allowNull: false,
				primaryKey: true,
			},
			status: {
				type: DataTypes.STRING(50),
				allowNull: false,
			},
			provider: {
				type: DataTypes.STRING(255),
				allowNull: false,
			},
			date: {
				type: DataTypes.DATE,
				allowNull: true,
				defaultValue: sequelize.fn('now'),
			},
			order_id: {
				type: DataTypes.INTEGER,
				allowNull: false,
				references: {
					model: 'orders',
					key: 'id',
				},
			},
		},
		{
			tableName: 'payment',
			schema: 'public',
			timestamps: false,
			indexes: [
				{
					name: 'payment_pkey',
					unique: true,
					fields: [{ name: 'id' }],
				},
			],
		}
	);
}
