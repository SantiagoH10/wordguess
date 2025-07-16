import { useState, useEffect } from 'react'
import { createContext, useContext } from 'react'

function useGameLogic() {
  const [gameStatus, setGameStatus] = useState('newGame')
  const [word, setWord] = useState('')
  const [wordPool, setWordPool] = useState([])
  const [model, setModel] = useState(null)
  const [targetWord, setTargetWord] = useState('')

  const startGame = () => {
    setGameStatus('play')
    setWord('')
    setWordPool([])
    setTargetWord(model.getRandomWord())
  }

  const submitWord = () => {
    const wordObj = {
      id: Date.now() + Math.random(),
      word: word,
      score: Math.floor(Math.random() * 100) + 1,
    }
    setWordPool(prev => [...prev, wordObj])
    setWord('')
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
      const isLetter = new RegExp('^[a-zA-Z]$').test(key)

      if (isLetter) {
        setWord(w => w + key)
        console.log(word)
        return
      }

      if (event.key === 'Enter') {
        submitWord()
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
