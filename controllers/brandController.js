import sequelize from '../db.js'; // Импортирую sequelize
import initModels from '../models/init-models.js'; // Импортирую функцию инициализации

import { Op } from 'sequelize';

const models = initModels(sequelize); // Инициализирую модели
const { brands } = models; // Деструктурирую brands из моделей

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
			const { brand, desc } = req.body;

			// Проверяю на существование брэнда с таким же названием
			const existingBrand = await brands.findOne({
				where: {
					brand: brand,
					id: { [Op.ne]: id },
				},
			});

			if (existingBrand) {
				return res.status(400).json({
					message: 'A brand with that name already exists',
				});
			}

			// обновляю
			const [updatedRows] = await brands.update(
				{
					brand: brand,
					desc: desc,
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
			const deletedCount = await brands.destroy({
				where: {
					id: idsArray,
				},
			});

			res
				.status(200)
				.json({ message: `${deletedCount} brands deleted successfully.` });
		} catch (error) {
			res.status(500).json({ message: error.message });
		}
	}
}

export default new BrandController();
