import { Router } from 'express';

import brandController from '../controllers/brandController.js';

const router = Router();

router.post('/', brandController.create);
router.get('/', brandController.getAll);
// router.get('/find', brandController.find);
router.get('/manyFind', brandController.manyFind);
router.get('/:id', brandController.getById);
router.patch('/:id', brandController.update);
router.delete('/:id', brandController.delete);
router.delete('/', brandController.deleteMany);

export default router;
