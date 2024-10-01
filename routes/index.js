import { Router } from 'express';

import brandRouter from './brandRouter.js';
import sneakersRouter from './sneakersRouter.js';

const router = Router();

router.use('/sneakers', sneakersRouter);
router.use('/brand', brandRouter);

export default router;
