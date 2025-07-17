import { GameDashboard } from '../game-components/GameDashboard'
import { GameOverlay } from '../game-components/GameOverlay'
import { InputWord } from '../game-components/InputWord'
import { TargetWord } from '../game-components/TargetWord'
import { WordPool } from '../game-components/WordPool'
import { useGame } from '../logic/useGame'

function WordguessGame() {
  return (
    <div className="container mx-auto flex flex-col items-center justify-center gap-2 rounded-2xl border border-white/20 bg-white/10 px-3 py-2 shadow-xl backdrop-blur-md">
      <TargetWord />
      <InputWord />
      <WordPool />
    </div>
  )
}

export function Wordguess() {
  return (
    <div className="container relative mx-auto flex flex-col gap-2 bg-white p-2">
      <GameDashboard />
      <WordguessGame />
      <GameOverlay />
    </div>
  )
}
