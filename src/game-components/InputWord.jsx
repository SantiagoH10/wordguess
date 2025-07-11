import { useGame } from '../logic/useGame'

export function InputWord() {
  const { word } = useGame()
  return (
    <div>
      <input
        className="
        rounded-full bg-white/10 backdrop-blur-md px-4 py-1 font-mono text-zinc-600 shadow-md outline-none ring-1 ring-red-700 duration-300 placeholder:text-zinc-600 placeholder:text-center placeholder:opacity-50 focus:shadow-lg focus:shadow-red-700 focus:ring-2 focus:ring-red-700"
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
