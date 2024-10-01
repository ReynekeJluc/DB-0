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
				type: DataTypes.DECIMAL,
				allowNull: false,
			},
			size: {
				type: DataTypes.DECIMAL,
				allowNull: false,
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
			},
		},
		{
			tableName: 'sneakers',
			schema: 'public',
			timestamps: false,
			indexes: [
				{
					name: 'sneakers_pkey',
					unique: true,
					fields: [{ name: 'id' }],
				},
			],
		}
	);
}
