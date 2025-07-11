import { useEffect, useState } from 'react'
import { useGame } from '../logic/useGame'

export function Timer() {
  const { gameStatus } = useGame()
  const [time, setTime] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      if (gameStatus === 'play') {
        setTime(prev => prev + 1)
      }
    }, 1000)
    return () => clearInterval(interval)
  }, [gameStatus])

  // Format time as MM:SS
  const formatTime = seconds => {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
  }

  return (
    <div className="relative">
      {/* Glassmorphism container */}
      <div className="rounded-2xl border border-white/20 bg-red-700/90 px-3 py-2 shadow-xl backdrop-blur-md">
        {/* Inner glow effect */}
        <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-white/5 to-transparent"></div>

        {/* Timer content */}
        <div className="relative z-10 text-center">
          <p className="text-2xl font-bold tracking-wider text-white drop-shadow-lg">
            {formatTime(time)}
          </p>
        </div>
      </div>
    </div>
  )
}
