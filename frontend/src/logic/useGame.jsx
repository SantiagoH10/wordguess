import { createContext, useContext, useEffect, useState } from 'react'
import { getApiUrl, API_CONFIG } from '../config/api.js'

function useGameLogic() {
  const [gameStatus, setGameStatus] = useState('newGame')
  const [word, setWord] = useState('')
  const [wordPool, setWordPool] = useState([])
  const [model, setModel] = useState('glove-wiki-gigaword-100')
  const [targetWord, setTargetWord] = useState('')
  const [error, setError] = useState(null)

  //#region API request functions
  const getRandomWord = async (selectedModel = model) => {
    const url = getApiUrl(API_CONFIG.ENDPOINTS.RANDOM_WORD)

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: selectedModel,
        }),
      })

      console.log('Response status:', response.status)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      if (data.error) {
        throw new Error(data.error)
      }

      return data.word
    } catch (err) {
      console.error('❌ Fetch failed:', err)
      console.error('❌ Error details:', err.message)
      throw new Error(`Failed to get random word: ${err.message}`)
    }
  }

  const compareWords = async (selectedModel = model, word1, word2) => {
    const url = getApiUrl(API_CONFIG.ENDPOINTS.SIMILAR_WORDS)

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: selectedModel,
          word1: word1,
          word2: word2,
        }),
      })
    } catch (e) {
      console.error('Compare words fetch failed:', e)
      throw new Error(`Failed to compare words: ${e.message}`)
    }
  }
  //#endregion

  const startGame = async () => {
    setError(null)
    setGameStatus('loading')

    try {
      const randomWord = await getRandomWord(model)
      setTargetWord(randomWord)
      setGameStatus('play')
      setWord('')
      setWordPool([])
    } catch (err) {
      setError(err.message)
      setGameStatus('newGame')
    }
  }

  const submitWord = async guessWord => {
    if (guessWord === targetWord) {
      setGameStatus('gameOver')
      return
    }

    try {
      const similScore = await compareWords(model, targetWord, guessWord)
      const wordObj = {
        id: Date.now() + Math.random(),
        word: word,
        score: similScore,
      }
      setWordPool(prev => [...prev, wordObj])
      setWord('')
    } catch (e) {
      console.error('Unable to submit word and get score', e.mesage)
    }
  }

  useEffect(() => {
    const handleKeyPress = event => {
      if (gameStatus === 'newGame' && event.key === 'Enter') {
        startGame()
        return
      }

      if (gameStatus !== 'play') return

      if (event.key === 'Backspace' || event.key === 'Delete') {
        setWord(w => w.slice(0, -1))
        return
      }

      const key = event.key.toUpperCase()
      const isLetter = /^[a-zA-Z]$/.test(key)

      if (isLetter) {
        setWord(w => w + key)
        console.log(word)
        return
      }

      if (event.key === 'Enter') {
        submitWord(word)
        console.log(wordPool)
        return
      }
    }

    document.addEventListener('keydown', handleKeyPress)

    return () => {
      document.removeEventListener('keydown', handleKeyPress)
    }
  }, [gameStatus, word])

  return {
    gameStatus,
    startGame,
    word,
    wordPool,
    targetWord,
    model,
    setModel,
    error,
  }
}

const GameContext = createContext()

export function GameProvider({ children }) {
  const gameState = useGameLogic()

  return (
    <GameContext.Provider value={gameState}>{children}</GameContext.Provider>
  )
}

export function useGame() {
  const context = useContext(GameContext)
  if (!context) {
    throw new Error('useGame must be used within a GameProvider')
  }
  return context
}
