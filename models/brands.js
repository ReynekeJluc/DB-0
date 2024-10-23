import { DataTypes } from 'sequelize';
import sequelize from '../db.js'; // Импортирую sequelize
import initModels from '../models/init-models.js';

const models = initModels(sequelize); // Инициализирую модели
const { brands } = models; // Деструктурирую brands из моделей

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
					isUnique: async (value, next) => {
						const trimmedValue = value.trim();
						const brand = await brands.findOne({
							where: { name: trimmedValue },
						});
						if (brand) {
							return next('Brand name must be unique');
						}
						next();
					},
				},
				set(value) {
					// Убираем пробелы перед сохранением
					this.setDataValue('name', value.trim());
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
			// Ограничение для проверки пустоты и лишних пробелов в имени
			validate: {
				nameNotEmpty() {
					if (this.name.trim().length === 0) {
						throw new Error('Brand name cannot be empty or just whitespace');
					}
				},
			},
		}
	);
}
