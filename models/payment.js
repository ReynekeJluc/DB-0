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
			provider_id: {
				type: DataTypes.INTEGER,
				allowNull: false,
				references: {
					model: 'providers',
					key: 'id',
				},
			},
			date: {
				type: DataTypes.DATE,
				allowNull: true,
				defaultValue: sequelize.fn('now'),
			},
		},
		{
			tableName: 'payment',
			schema: 'public',
			timestamps: false,
		}
	);
}
