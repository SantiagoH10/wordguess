import { Timer } from './Timer'

export function GameDashboard() {
  return (
    <div className="container mx-auto flex justify-center rounded-2xl border border-white/20 bg-white/10 px-3 py-2 shadow-xl backdrop-blur-md">
      <Timer />
    </div>
  )
}
