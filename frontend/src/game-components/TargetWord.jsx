import { useGame } from '../logic/useGame'

export function TargetWord() {
  const { targetWord } = useGame()
  return (
    <div className="rounded-full bg-white/10 px-4 py-1 font-mono text-zinc-600 shadow-md outline-none ring-1 ring-red-700 backdrop-blur-md duration-300 placeholder:text-center placeholder:text-zinc-600 placeholder:opacity-50 focus:shadow-lg focus:shadow-red-700 focus:ring-2 focus:ring-red-700">
      <p>Word to guess : {targetWord}</p>
    </div>
  )
}
