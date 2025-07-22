import { Timer } from './Timer'
import { useGame } from '../logic/useGame'

const Attempts = () => {
  const { wordPool } = useGame()
  const attempts = wordPool.length
  return (
    <div>
      {/* Glassmorphism container */}
      <div className="rounded-2xl border border-white/20 bg-yellow-400/70 px-3 py-2 shadow-xl backdrop-blur-md">
        {/* Inner glow effect */}
        <div className="rounded-2xl bg-gradient-to-r from-white/5 to-transparent"></div>

        {/* Timer content */}
        <div className="relative z-10 text-center">
          <p className="text-sm font-bold tracking-wider text-white drop-shadow-lg">
            Attempts : {attempts}
          </p>
        </div>
      </div>
    </div>
  )
}

export function GameDashboard() {
  return (
    <div className="container mx-auto flex items-center justify-around gap-4 rounded-2xl border border-white/20 bg-white/10 px-3 py-2 shadow-xl backdrop-blur-md">
      <Timer />
      <Attempts />
    </div>
  )
}
