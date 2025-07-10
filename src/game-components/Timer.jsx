import { useEffect, useState } from 'react'

export function Timer({ gameStatus }) {
  const [time, setTime] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      if (gameStatus === 'play') {
        setTime(prev => prev + 1)
      }
    }, 1000)
    return () => clearInterval(interval)
  }, [gameStatus])

  return (
    <>
      <div>
        <p>{time}</p>
      </div>
    </>
  )
}
