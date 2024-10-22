import { Router } from 'express';

import brandRouter from './brandRouter.js';

const router = Router();

router.use('/brand', brandRouter);

export default router;
