import express from 'express'

const router = express.Router()

// General API endpoints
router.get('/', (req, res) => {
  res.json({ message: 'WordGuess API' })
})

router.get('/status', (req, res) => {
  res.json({
    api: 'WordGuess API',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
  })
})

export default router
