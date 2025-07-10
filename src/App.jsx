import { useState } from 'react'
import { MySociabble } from './app-components/MySociabble'
import { Wordguess } from './app-components/Wordguess'
import { GameProvider } from './logic/useGame'

function App() {
  return (
    <>
      <MySociabble />
      <GameProvider>
      <Wordguess />
      </GameProvider>
    </>
  )
}

export default App
