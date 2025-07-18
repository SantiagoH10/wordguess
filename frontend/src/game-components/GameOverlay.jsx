import { Button } from '../app-components/Button'
import { useGame } from '../logic/useGame'

const GameStartOverlay = () => {
  return (
    <div>
      <p className="text-bold text-white">Start New Game</p>
      <Button onClick={startGame}>Start</Button>
    </div>
  )
}

const LoadingOverlay = () => {
  return (
    <div>
      <p className="text-bold text-white">Start New Game</p>
    </div>
  )
}

const GameEndOverlay = () => {
  return (
    <div>
      <p className="text-bold text-white">Start New Game</p>
      <Button onClick={startGame}>New Word</Button>
    </div>
  )
}

export function GameOverlay() {
  const { startGame, gameStatus } = useGame()

  const statusMapping = {
    loading: <LoadingOverlay />,
    newGame: <GameStartOverlay />,
    gameOver: <GameEndOverlay />,
  }

  return (
    <div className="absolute inset-0 z-10 bg-black bg-opacity-50">
      {statusMapping[gameStatus] ? statusMapping[gameStatus] : null}
    </div>
  )
}
