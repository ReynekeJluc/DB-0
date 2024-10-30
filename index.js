import 'dotenv/config';

import cors from 'cors';
import express from 'express';
import sequelize from './db.js';

import router from './routes/index.js'; // делаем маршрутизатор, который хавает запросы и из них вырывает метод, заголовки, тело сам url и дальше проходит по всем маршрутами

const PORT = process.env.PORT || 5000;

const app = express();
app.use(cors({ origin: '*' })); // доступ с любого домена
app.use(express.json()); // для работы с json
app.use('/api', router); // создаем подмаршрут

// нулевой эндпоинт для проверки работы
app.get('/', (req, res) => {
	res.status(200).json({ message: 'Working!' });
});

// запуск сервера
const start = async () => {
	try {
		await sequelize.authenticate(); // Проверка можно ли подключиться к бд
		await sequelize.sync(); // синхронизация моделей и структур бд

		app.listen(PORT, err => {
			// запускаем, точнее пытаемся запустить сервер на порте PORT
			if (err) {
				return console.log(err);
			} else {
				console.log(`Server has been started on port ${PORT}`);
			}
		});
	} catch (error) {
		console.log(error.message);
	}
};

start();
