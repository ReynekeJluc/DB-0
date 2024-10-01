import { DataTypes } from 'sequelize';

export default function (sequelize) {
	return sequelize.define(
		'alembic_version',
		{
			version_num: {
				type: DataTypes.STRING(32),
				allowNull: false,
				primaryKey: true,
			},
		},
		{
			tableName: 'alembic_version',
			schema: 'public',
			timestamps: false,
			indexes: [
				{
					name: 'alembic_version_pkc',
					unique: true,
					fields: [{ name: 'version_num' }],
				},
			],
		}
	);
}
