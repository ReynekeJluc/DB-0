import { Sequelize } from 'sequelize';

//const { DB_USER, DB_PASS, DB_HOST, DB_NAME } = process.env;

const sequelize = new Sequelize(
	`postgresql://db_a10c_user:A0khoNqbLhlUvzuv7hlR3aZAWp0au3s3@dpg-csksr2u8ii6s7380n160-a.oregon-postgres.render.com/db_a10c?ssl=true`,
	{ dialect: 'postgres' }
);

export default sequelize;

// pool: {
// 	max: 5,        // Максимальное количество соединений
// 	min: 0,        // Минимальное количество соединений
// 	acquire: 30000, // Максимальное время ожидания соединения
// 	idle: 10000    // Время ожидания перед закрытием неиспользуемых соединений
// }
