import { Sequelize } from 'sequelize';

const { DB_USER, DB_PASS, DB_HOST, DB_NAME } = process.env;

const sequelize = new Sequelize(
	`postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}.oregon-postgres.render.com/${DB_NAME}?ssl=true`,
	{ dialect: 'postgres' }
);

export default sequelize;
