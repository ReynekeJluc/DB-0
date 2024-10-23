import { DataTypes } from 'sequelize';

// Используем sequelize-auto для авто подгрузки моделей из бд / sequelize-auto -o "/models" -d <db-name> -h <host> -u <user> -p <port> -x <password> -e postgres

export default function (sequelize) {
	return sequelize.define(
		'brands',
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
				validate: {
					notEmpty: true,
				},
			},
			description: {
				type: DataTypes.TEXT,
				allowNull: true,
			},
		},
		{
			tableName: 'brands',
			schema: 'public',
			timestamps: false,
			indexes: [
				{
					name: 'brands_pkey',
					unique: true,
					fields: [{ name: 'id' }],
				},
				{
					name: 'uq_brand_name',
					unique: true,
					fields: [{ name: 'name' }],
				},
			],
		}
	);
}
