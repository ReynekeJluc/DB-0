import sequelize from '../db.js'; // Импортирую sequelize
import initModels from '../models/init-models.js'; // Импортирую функцию инициализации

import { Op } from 'sequelize'; // набор операторов для создания условий

const models = initModels(sequelize); // Инициализирую модели
const { brands } = models; // Деструктурирую brands из моделей
const { sneakers } = models; // Деструктурирую sneakers из моделей

class BrandController {
	async create(req, res) {
		try {
			const newBrand = await brands.create(req.body);

			res.status(200).json(newBrand);
		} catch (error) {
			res.status(500).json({ error: error.message });
		}
	}

	async getAll(req, res) {
		try {
			const allBrands = await brands.findAll();

			res.status(200).json(allBrands);
		} catch (error) {
			res.status(500).json({ error: error.message });
		}
	}

	async getById(req, res) {
		const { id } = req.params;
		try {
			const brand = await brands.findByPk(id); // поиск по первичному ключу фича sequelize

			if (!brand) {
				return res.status(404).json({ message: 'Brand not found' });
			}

			res.status(200).json(brand);
		} catch (error) {
			res.status(500).json({ error: error.message });
		}
	}

	async update(req, res) {
		try {
			const { id } = req.params;
			const { name, description } = req.body;

			// Проверяю на существование брэнда с таким же названием
			const existingBrand = await brands.findOne({
				where: {
					name: name,
					id: { [Op.ne]: id }, // Op.ne = не равно, чтобы не считать саму обновляемую запись
				},
			});

			if (existingBrand) {
				return res.status(400).json({
					message: 'A brand with that name already exists or incorrect id',
				});
			}

			// обновляю
			const [updatedRows] = await brands.update(
				{
					name: name,
					description: description,
				},
				{
					where: { id },
				}
			);

			if (updatedRows === 0) {
				return res.status(404).json({
					message: "Couldn't find a brand",
				});
			}

			res.json({
				success: true,
			});
		} catch (error) {
			console.error(error.message);
			res.status(400).json({
				error: 'Failed to update the brand',
			});
		}
	}

	async delete(req, res) {
		const { id } = req.params;
		try {
			// также фича sequelize для удаления записи из таблицы, { id } является сокращенной записью для { id: id } когда у них имена одинаковые
			const deletedRecord = await brands.destroy({ where: { id } });

			if (deletedRecord === 0) {
				return res.status(404).json({ message: 'Brand not found' });
			}

			res.status(200).send({ message: 'Brand deleted successfully' });
		} catch (error) {
			// Обработка ошибок внешнего ключа
			if (error.name === 'SequelizeForeignKeyConstraintError') {
				return res.status(400).json({
					message: 'Cannot delete brand, as it is referenced by sneakers.',
				});
			}
			res.status(500).json({ error: error.message });
		}
	}

	async deleteMany(req, res) {
		const { ids } = req.query;

		if (!ids) {
			return res.status(400).json({ message: 'No ids provided' });
		}

		const idsArray = ids.split(',').map(Number);

		try {
			// Сначала находим бренды, которые можно удалить
			const brandsToDelete = await brands.findAll({
				where: {
					id: idsArray,
				},
				include: [
					{
						model: sneakers,
						as: 'sneakers', // Указываем алиас (альтернативное название для связей, для избежания конфликтов именования)
						required: false, // Получаем бренды даже если у них нет связанных кроссовок
					},
				],
			});

			// Фильтруем только те бренды, у которых нет связанных кроссовок
			const deletableBrands = brandsToDelete.filter(
				brand => !brand.sneakers.length // brand.sneakers.length содержит количество связанных кроссовок
			);

			if (deletableBrands.length === 0) {
				return res.status(400).json({
					message: 'No brands can be deleted due to existing references',
				});
			}

			// Удаляем только те бренды, которые можно удалить
			const deletedCount = await brands.destroy({
				where: {
					id: deletableBrands.map(brand => brand.id),
				},
			});

			res.status(200).json({
				message: `${deletedCount} brands deleted successfully`,
			});
		} catch (error) {
			res.status(500).json({ message: error.message });
		}
	}
}

export default new BrandController();
