import { DataTypes } from 'sequelize';

export default function (sequelize) {
	return sequelize.define(
		'sneakers',
		{
			id: {
				autoIncrement: true,
				type: DataTypes.INTEGER,
				allowNull: false,
				primaryKey: true,
			},
			name: {
				type: DataTypes.STRING(255),
				allowNull: false,
			},
			price: {
				type: DataTypes.DECIMAL(10, 2),
				allowNull: false,
				validate: {
					min: 0,
				},
			},
			size: {
				type: DataTypes.DECIMAL(3, 1),
				allowNull: false,
				validate: {
					min: 16,
				},
			},
			description: {
				type: DataTypes.TEXT,
				allowNull: true,
			},
			brand_id: {
				type: DataTypes.INTEGER,
				allowNull: false,
				references: {
					model: 'brands',
					key: 'id',
				},
				onDelete: 'SET NULL'
			},
		},
		{
			tableName: 'sneakers',
			schema: 'public',
			timestamps: false,
		}
	);
}
