import { DataTypes, Op, where, fn, col } from 'sequelize';
import sequelize from '../db.js'; // Импортирую sequelize
import initModels from '../models/init-models.js';

const models = initModels(sequelize); // Инициализирую модели
const { brands } = models; // Деструктурирую brands из моделей

/*
function capitalize(str) {
	return str.charAt(0).toUpperCase() + str.slice(1);
}
*/

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
			      isUnique: async function(value, next) {
			        const trimmedValue = value.trim().toLowerCase(); // Преобразуем значение к нижнему регистру
			
			        const brand = await Brand.findOne({
			          where: {
			            [Op.and]: [
			              fn('LOWER', col('name')), // Преобразуем имя в нижний регистр
			              { [Op.eq]: trimmedValue },  // Сравниваем с преобразованным значением
			              { id: { [Op.ne]: this.id } } // Исключаем текущую запись
			            ]
			          }
			        });
			
			        if (brand && brand.id != this.id) {
			          throw new Error('Brand name must be unique'); // Если бренд найден, выбрасываем ошибку
			        }

			        next();
			      }
			    },
			    set(value) {
			      // Убираем пробелы перед сохранением
			      this.setDataValue('name', value.trim());
			    },
			},
			description: {
				type: DataTypes.TEXT,
				allowNull: true,
				set(value) {
					// Убираем пробелы перед сохранением
					this.setDataValue('description', value.trim());
				},
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
