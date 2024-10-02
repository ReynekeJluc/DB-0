import { Sequelize } from 'sequelize';

const sequelize = new Sequelize("postgresql://postgres.rzylrywyevfvduerkzdp:Andrenov2003@aws-0-eu-central-1.pooler.supabase.com:6543/postgres", { dialect: 'postgres' });

export default sequelize;
