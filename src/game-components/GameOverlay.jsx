import { Button } from '../app-components/Button'
import { useGame } from '../logic/useGame'

export function GameOverlay() {
  const { startGame, gameStatus } = useGame()

  if (gameStatus !== 'newGame') return null

  return (
    <div className="absolute inset-0 z-10 bg-black bg-opacity-50">
      <p className="text-bold text-white">Start New Game</p>
      <Button onClick={startGame}>Start</Button>
    </div>
  )
}
