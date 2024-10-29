import sequelize from '../db.js'; // Импортирую sequelize
import initModels from '../models/init-models.js'; // Импортирую функцию инициализации

const models = initModels(sequelize); // Инициализирую модели
const { sneakers } = models; // Деструктурирую sneakers из моделей

class SneakersController {
	async getAll(req, res) {
		try {
			const allSneakers = await sneakers.findAll();

			res.status(200).json(allSneakers);
		} catch (error) {
			res.status(500).json({ error: error.message });
		}
	}
}

export default new SneakersController();
