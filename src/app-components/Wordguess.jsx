import { useState, useEffect } from 'react'
import { Timer } from '../game-components/Timer'
import { Button } from './Button'
import { useGame } from '../logic/useGame'

export function GameDashboard() {
  const { gameStatus, startGame } = useGame()
  return (
    <div>
      <Timer gameStatus={gameStatus} />
      <Button onClick={startGame}>Start</Button>
    </div>
  )
}

function InputWord() {
  const { gameStatus, word } = useGame()

  return (
    <div>
      <input
        className="rounded-full bg-zinc-200 px-4 py-1 font-mono text-zinc-600 shadow-md outline-none ring-1 ring-zinc-400 duration-300 placeholder:text-zinc-600 placeholder:opacity-50 focus:shadow-lg focus:shadow-rose-400 focus:ring-2 focus:ring-rose-400"
        autoComplete="off"
        placeholder="Guess a word"
        name="text"
        type="text"
        value={word}
        readOnly
      />
    </div>
  )
}

function WordguessGame() {
  return (
    <div>
      <InputWord />
    </div>
  )
}

export function Wordguess() {
  return (
    <>
      <div className="container bg-gray-200">
        <GameDashboard />
        <WordguessGame />
      </div>
    </>
  )
}
