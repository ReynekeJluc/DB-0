import { Sequelize } from 'sequelize';

const { DB_USER, DB_PASS, DB_HOST, DB_NAME } = process.env;

const sequelize = new Sequelize(
	`postgresql://db_vnss_user:odvSKqEe0uNAN5zppSPUMwASfpbeauy5@dpg-cruiooogph6c73aj72hg-a.oregon-postgres.render.com/db_vnss?ssl=true`,
	{ dialect: 'postgres' }
);

export default sequelize;
