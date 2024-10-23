import { DataTypes } from 'sequelize';

export default function (sequelize) {
	return sequelize.define(
		'providers',
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
			address: {
				type: DataTypes.TEXT,
				allowNull: false,
			},
			phone: {
				type: DataTypes.STRING(10),
				allowNull: false,
				validate: {
					is: /^[0-9]{10}$/,
				},
			},
			email: {
				type: DataTypes.STRING(255),
				allowNull: false,
				validate: {
					isEmail: true,
				},
			},
		},
		{
			tableName: 'providers',
			schema: 'public',
			timestamps: false,
		}
	);
}
