import express from 'express';
import PythonRunner from '../utils/pythonRunner.js';
import { validateWord, validateModel } from '../utils/validation.js';

const router = express.Router();

// Helper function to run Python script
async function runWord2VecScript(args) {
  const scriptPath = process.env.PYTHON_SCRIPT_PATH || '../ml-service/scripts/word2vec_cli.py';
  return await PythonRunner.runScript(scriptPath, args);
}

// Get similar words
router.post('/similar', async (req, res, next) => {
  try {
    const { word, model = 'glove-wiki-gigaword-100', top_n = 10 } = req.body;

    const validatedWord = validateWord(word);
    const validatedModel = validateModel(model);

    const result = await runWord2VecScript([
      '--operation', 'similar',
      '--model', validatedModel,
      '--word', validatedWord,
      '--top_n', top_n.toString()
    ]);

    res.json(result);
  } catch (error) {
    next(error);
  }
});

// Compare two words
router.post('/compare', async (req, res, next) => {
  try {
    const { word1, word2, model = 'glove-wiki-gigaword-100' } = req.body;

    const validatedWord1 = validateWord(word1);
    const validatedWord2 = validateWord(word2);
    const validatedModel = validateModel(model);

    const result = await runWord2VecScript([
      '--operation', 'compare',
      '--model', validatedModel,
      '--word1', validatedWord1,
      '--word2', validatedWord2
    ]);

    res.json(result);
  } catch (error) {
    next(error);
  }
});

// Get random word
router.post('/random', async (req, res, next) => {
  try {
    const { model = 'glove-wiki-gigaword-100' } = req.body;

    const validatedModel = validateModel(model);

    const result = await runWord2VecScript([
      '--operation', 'random',
      '--model', validatedModel
    ]);

    res.json(result);
  } catch (error) {
    next(error);
  }
});

// Check if word exists
router.post('/exists', async (req, res, next) => {
  try {
    const { word, model = 'glove-wiki-gigaword-100' } = req.body;

    const validatedWord = validateWord(word);
    const validatedModel = validateModel(model);

    const result = await runWord2VecScript([
      '--operation', 'exists',
      '--model', validatedModel,
      '--word', validatedWord
    ]);

    res.json(result);
  } catch (error) {
    next(error);
  }
});

// Get model info
router.get('/info', async (req, res, next) => {
  try {
    const { model = 'glove-wiki-gigaword-100' } = req.query;

    const validatedModel = validateModel(model);

    const result = await runWord2VecScript([
      '--operation', 'info',
      '--model', validatedModel
    ]);

    res.json(result);
  } catch (error) {
    next(error);
  }
});

export default router;
