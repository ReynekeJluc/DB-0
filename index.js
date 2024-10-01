import 'dotenv/config';
import initModels from './models/init-models.js';

import cors from 'cors';
import express from 'express';
import sequelize from './db.js';

import router from './routes/index.js';

// вспомогательные действия

const PORT = process.env.PORT || 5000;

const app = express();
app.use(cors({ origin: '*' })); // доступ с любого домена
app.use(express.json()); // для работы с json
app.use('/api', router);

const models = initModels(sequelize);
const { brands, orders, sneakers, payment } = models;

// запросы

app.get('/', (req, res) => {
	res.status(200).json({ message: 'Working!' });
});

// запуск сервера

const start = async () => {
	try {
		await sequelize.authenticate();
		await sequelize.sync();

		app.listen(PORT, err => {
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
