import sequelize from '../db.js'; // Импортирую sequelize
import initModels from '../models/init-models.js'; // Импортирую функцию инициализации

const models = initModels(sequelize); // Инициализирую модели
const { brands } = models; // Деструктурирую brands из моделей
const { sneakers } = models; // Деструктурирую sneakers из моделей

class BrandController {
	async create(req, res) {
		try {
			const { id, ...brandData } = req.body; // исключаем айди

			//const lowerCaseName = brandData.name.toLowerCase().trim();

			// Проверяем на существование бренда с таким же именем в нижнем регистре
			// const existingBrand = await brands.findOne({
			// 	where: sequelize.where(
			// 		// условие для фильтрации два параметра первое - сравниваемое, второе - с чем сравниваем
			// 		sequelize.fn('LOWER', sequelize.col('name')), // берем из базы в lower (fn - это функция для выполнения SQL фукнций)
			// 		lowerCaseName
			// 	),
			// });

			// if (existingBrand) {
			// 	return res.status(400).json({
			// 		message: 'A brand with that name already exists',
			// 	});
			// }

			const newBrand = await brands.create(brandData);

			res.status(200).json(newBrand);
		} catch (error) {
			res.status(400).json({
				message: error.message,
				// error: error,
			});
		}
	}

	async getAll(req, res) {
		try {
			const allBrands = await brands.findAll(); // использует SELECT * FROM brands, но можно добавить { attributes: ['name', 'description'] } и тогда конкретные будет брать

			res.status(200).json(allBrands);
		} catch (error) {
			res.status(400).json({ error: error.message });
		}
	}

	async getById(req, res) {
		const { id } = req.params;
		try {
			const brand = await brands.findByPk(id); // поиск по первичному ключу фича sequelize (также по умолчанию юзает *, но можно аттрибуты вставить)

			if (!brand) {
				return res.status(404).json({ message: 'Brand not found' });
			}

			res.status(200).json(brand);
		} catch (error) {
			res.status(400).json({ error: error.message });
		}
	}

	async update(req, res) {
		try {
			const { id } = req.params;
			const { name, description } = req.body;

			//const lowerCaseName = name.toLowerCase().trim();

			// Проверяем на существование бренда с таким же именем в нижнем регистре
			// const existingBrand = await brands.findOne({
			// 	where: {
			// 		// оператор обьединения нескольких условий
			// 		[Op.and]: [
			// 			sequelize.where(
			// 				sequelize.fn('LOWER', sequelize.col('name')),
			// 				lowerCaseName
			// 			),
			// 			{ id: { [Op.ne]: id } }, // Исключаем текущую запись из проверки ([Op.ne] - тоже что и <> то есть неравны (not equal))
			// 		],
			// 	},
			// });

			// if (existingBrand) {
			// 	return res.status(400).json({
			// 		message: 'A brand with that name already exists or incorrect id',
			// 	});
			// }

			// обновляю
			const [updatedRows] = await brands.update(
				// почему [updatedRows], потому что update возвращает массив из 2-х элементов, где первый кол-во обновленных и второй собственно обновленные и я сразу деструктурирую забирая то что мне нужно (и то чтобы возвращать массив измененных нужно указать returning: true)
				{
					name: name,
					description: description,
				},
				{
					where: { id },
					// вот сюда returning: true, если надо будет возвращать массив измененных
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
			res.status(400).json({
				message: error.message,
				// error: error,
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

			res
				.status(200)
				.send({ message: 'Brand deleted successfully (or set null)' });
		} catch (error) {
			res.status(400).json({ error: error.message });
		}
	}

	async deleteMany(req, res) {
		const { ids } = req.query;

		if (!ids) {
			return res.status(400).json({ message: 'No ids provided' });
		}

		const idsLength = ids.split(',');

		const idsArray = ids // собственно получаем массив только с валидными значениями id
			.split(',')
			.map(id => parseInt(id, 10)) // 10 это система счисления и мы парсим что можем а что не можем нам выдаст NaN который мы след фильтруем
			.filter(id => !isNaN(id)); // удаляем все не числа из массива

		try {
			// Генерим массив из брэндов, и у тех кого есть связанные кроссовки добавляем связанную инфу, если нету то просто оставляем
			const brandsToDelete = await brands.findAll({
				where: {
					id: idsArray, // под капотом запрос типа SELECT * FROM brands AS brands WHERE brands.id IN (idsArray);
				},
				include: [
					{
						model: sneakers,
						as: 'sneakers', // Указываем алиас (альтернативное название для связей, для избежания конфликтов именования) и на его основе формируется название для вложенного обьекта
						required: false, // Получаем бренды даже если у них нет связанных кроссовок
						// мы как бы создаем вложенный обьект связанных кроссовок для каждого брэнда
					},
				],
			});

			await brands.destroy({
				// он генерирует запрос типа DELETE FROM brands WHERE id IN (idsArray), где idsArray в виде конкретных значений
				where: {
					id: idsArray,
				},
			});

			res.status(200).json({
				message: `${
					brandsToDelete.length
				} brands deleted successfully (or set null) and ${
					idsLength.length - brandsToDelete.length
				} brands not found or not valid value`,
			});
		} catch (error) {
			res.status(400).json({ message: error.message });
		}
	}

	// -------2-LB-------
	async find(req, res) {
		try {
			const filters = req.query; // получаем атрибуты переданные через строку запроса

			const foundBrands = await brands.findAll({
				where: filters, // генерит запрос вида    SELECT * FROM brands WHERE name = 'название какое то' AND description = 'какое то опичсание';
			});

			if (foundBrands.length === 0) {
				return res
					.status(404)
					.json({ message: 'No brands found with attributes' });
			}

			res.status(200).json(foundBrands);
		} catch (error) {
			res.status(400).json({ message: error.message });
		}
	}

	async manyFind(req, res) {
		try {
			const filters = req.query;

			// Получаем параметры лимита и смещения
			const limitBrands = parseInt(filters.limit) || 5; // Количество результатов (по умолчанию 5)
			const offsetBrands = parseInt(filters.offset) || 0; // Смещение (по умолчанию 0)

			console.log(limitBrands + ' ' + offsetBrands);

			// удаляем из фильтров лимит и оффсет чтобы он не искал по ним в базе
			delete filters.limit;
			delete filters.offset;

			// Выполняем запрос с атрибутами, лимитом и смещением
			const results = await brands.findAll({
				// SELECT * FROM brands WHERE name = '...' LIMIT 10 OFFSET 0;

				where: filters,
				limit: limitBrands,
				offset: offsetBrands,
			});

			res.status(200).json(results);
		} catch (error) {
			res.status(400).json({ error: error.message });
		}
	}
}

export default new BrandController();

//! заметки
// Sequelize не открывает и закрывает соединения он создает ПУЛ СОЕДИНЕНИЙ, набор заранее открыттых соединений можно настраивать в конфиге (db.js):
// max (сколько всего можно), min (сколько минимум поддерживать будет), acquire (сколько ждать прежде чем ошибку выдавать в миллисекундах), idle (сколько жить будут соединения в миллисекундах)
// И собственно когда мы кидаем запрос он берет свободный из пула, выполняет и не закрывает его а возвращает обратно в пул
