import { Router } from 'express';

import brandRouter from './brandRouter.js';
import sneakersRouter from './sneakersRouter.js';

const router = Router();

router.use('/brand', brandRouter);
router.use('/sneakers', sneakersRouter);

export default router;
