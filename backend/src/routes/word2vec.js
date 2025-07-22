import express from 'express'
import axios from 'axios'
import { validateWord, validateModel } from '../utils/validation.js'

const router = express.Router()

// Flask service configuration
const FLASK_SERVICE_URL =
  process.env.FLASK_SERVICE_URL || 'http://localhost:5000'
const REQUEST_TIMEOUT = parseInt(process.env.FLASK_REQUEST_TIMEOUT) || 30000

// Helper function to call Flask service
async function callFlaskService(
  endpoint,
  method = 'POST',
  data = null,
  params = null,
) {
  try {
    const config = {
      method,
      url: `${FLASK_SERVICE_URL}/api${endpoint}`,
      timeout: REQUEST_TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    }

    if (data) config.data = data
    if (params) config.params = params

    const response = await axios(config)
    return response.data
  } catch (error) {
    // Handle Flask service errors
    if (error.response) {
      // Flask returned an error response
      const flaskError = error.response.data
      const errorMessage = flaskError.message || 'Flask service error'
      const serviceError = new Error(errorMessage)
      serviceError.statusCode = error.response.status
      serviceError.details = flaskError
      throw serviceError
    } else if (error.code === 'ECONNREFUSED') {
      throw new Error('ML service is unavailable. Please try again later.')
    } else if (error.code === 'ETIMEDOUT') {
      throw new Error('ML service request timed out. Please try again.')
    } else {
      throw new Error(`ML service error: ${error.message}`)
    }
  }
}

// Compare two words
router.post('/compare', async (req, res, next) => {
  try {
    const { word1, word2, model = 'glove-wiki-gigaword-100' } = req.body

    const validatedWord1 = validateWord(word1)
    const validatedWord2 = validateWord(word2)
    const validatedModel = validateModel(model)

    const result = await callFlaskService('/compare', 'POST', {
      word1: validatedWord1,
      word2: validatedWord2,
      model: validatedModel,
    })

    res.json(result)
  } catch (error) {
    next(error)
  }
})

// Get random word
router.post('/random', async (req, res, next) => {
  try {
    const { model = 'glove-wiki-gigaword-100' } = req.body

    const validatedModel = validateModel(model)

    const result = await callFlaskService('/random', 'POST', {
      model: validatedModel,
    })

    res.json(result)
  } catch (error) {
    next(error)
  }
})

// Check if word exists
router.post('/exists', async (req, res, next) => {
  try {
    const { word, model = 'glove-wiki-gigaword-100' } = req.body

    const validatedWord = validateWord(word)
    const validatedModel = validateModel(model)

    const result = await callFlaskService('/exists', 'POST', {
      word: validatedWord,
      model: validatedModel,
    })

    res.json(result)
  } catch (error) {
    next(error)
  }
})

// Get model info
router.get('/info', async (req, res, next) => {
  try {
    const { model = 'glove-wiki-gigaword-100' } = req.query

    const validatedModel = validateModel(model)

    const result = await callFlaskService('/info', 'GET', null, {
      model: validatedModel,
    })

    res.json(result)
  } catch (error) {
    next(error)
  }
})

export default router
