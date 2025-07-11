import { useState } from 'react'
import { MySociabble } from './app-components/MySociabble'
import { Wordguess } from './app-components/Wordguess'
import { GameProvider } from './logic/useGame'

function App() {
  return (
    <div className="min-h-screen bg-blue-100">
      <MySociabble />
      <GameProvider>
        <Wordguess />
      </GameProvider>
    </div>
  )
}

export default App
