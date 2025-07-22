import { Button } from '../app-components/Button'
import { useGame } from '../logic/useGame'

const GameStartOverlay = ({ startGame }) => {
  return (
    <div className="align-center flex flex-col items-center justify-center gap-4">
      <p className="text-bold rounded-full border-2 border-red-400 bg-white px-4 py-1 text-2xl text-gray-700">
        Start New Game
      </p>
      <Button onClick={startGame}>Start</Button>
    </div>
  )
}

const LoadingOverlay = () => {
  return (
    <div className="z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="flex flex-col items-center space-y-4 rounded-lg bg-white p-8 shadow-2xl">
        {/* Spinning loader */}
        <div className="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"></div>

        {/* Loading text with pulse animation */}
        <p className="animate-pulse text-lg font-semibold text-gray-800">
          Loading...
        </p>

        {/* Optional: Animated dots */}
        <div className="flex space-x-1">
          <div className="h-2 w-2 animate-bounce rounded-full bg-blue-600"></div>
          <div
            className="h-2 w-2 animate-bounce rounded-full bg-blue-600"
            style={{ animationDelay: '0.1s' }}
          ></div>
          <div
            className="h-2 w-2 animate-bounce rounded-full bg-blue-600"
            style={{ animationDelay: '0.2s' }}
          ></div>
        </div>
      </div>
    </div>
  )
}

const GameEndOverlay = ({ startGame, targetWord }) => {
  return (
    <div>
      <p className="text-bold text-white">You won!</p>
      <p className="text-bold text-white">Secret word : {targetWord}</p>

      <Button onClick={startGame}>New Word</Button>
    </div>
  )
}

export function GameOverlay() {
  const { startGame, gameStatus, targetWord } = useGame()

  const statusMapping = {
    loading: <LoadingOverlay />,
    newGame: <GameStartOverlay startGame={startGame} />,
    gameOver: <GameEndOverlay startGame={startGame} targetWord={targetWord} />,
  }

  if (!statusMapping[gameStatus]) {
    return null
  }

  return (
    <div className="align-center absolute inset-0 z-10 flex flex-col items-center justify-center bg-black bg-opacity-70">
      {statusMapping[gameStatus]}
    </div>
  )
}
