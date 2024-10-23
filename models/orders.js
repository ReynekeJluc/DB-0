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
			name_customer: {
				type: DataTypes.STRING(255),
				allowNull: false,
				validate: {
					notEmpty: true,
				},
			},
			pickup_code: {
				type: DataTypes.JSON,
				allowNull: false,
			},
			status: {
				type: DataTypes.ENUM('Pending', 'Shipped', 'Delivered', 'Canceled'),
				allowNull: true,
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
			validate: {
				nameNotEmpty() {
					if (this.name_customer.trim().length === 0) {
						throw new Error('Customer name cannot be empty or just whitespace');
					}
				},
			},
		}
	);
}
