import { useGame } from '../logic/useGame'

export function InputWord() {
  const { word, gameStatus } = useGame()

  const isLoading = gameStatus === 'isComparing'

  return (
    <div className="relative">
      <input
        className={`rounded-full bg-white/10 px-4 py-1 font-mono text-zinc-600 shadow-md outline-none ring-1 ring-red-700 backdrop-blur-md duration-300 placeholder:text-center placeholder:text-zinc-600 placeholder:opacity-50 focus:shadow-lg focus:shadow-red-700 focus:ring-2 focus:ring-red-700 ${
          isLoading
            ? 'animate-pulse bg-gradient-to-r from-red-500/20 via-orange-500/20 to-red-500/20 ring-2 ring-orange-500 shadow-lg shadow-orange-500/50 scale-105 bg-size-200 animate-gradient-x'
            : ''
        }`}
        autoComplete="off"
        placeholder={isLoading ? "🔍 Comparing..." : "Guess a word"}
        name="text"
        type="text"
        value={word}
        readOnly
      />

      {/* Loading spinner overlay */}
      {isLoading && (
        <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
          <div className="animate-spin rounded-full h-4 w-4 border-2 border-orange-500 border-t-transparent"></div>
        </div>
      )}

      
    </div>
  )
}
