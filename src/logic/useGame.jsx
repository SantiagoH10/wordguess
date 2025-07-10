import { useState, useEffect } from 'react'
import { createContext, useContext } from 'react'

function useGameLogic() {
  const [gameStatus, setGameStatus] = useState('newGame')
  const [word, setWord] = useState('')

  const startGame = () => {
    console.log("game set to play")
    setGameStatus('play')
    setWord('')
  }

  useEffect(() => {
    const handleKeyPress = event => {
      console.log("key pressed", event.key)
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
  }
}

const GameContext = createContext()

export function GameProvider({ children }) {
  const gameState = useGameLogic()

  return (
    <GameContext.Provider value={gameState}>
      {children}
    </GameContext.Provider>
  )
}

export function useGame() {
  const context = useContext(GameContext)
  if (!context) {
    throw new Error('useGame must be used within a GameProvider')
  }
  return context
}
