import { Router } from 'express';
import sneakersController from '../controllers/sneakersController.js';

const router = Router();

router.get('/', sneakersController.getAll);

export default router;
