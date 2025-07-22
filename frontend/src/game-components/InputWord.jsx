import { useGame } from '../logic/useGame'

export function InputWord() {
  const { word, gameStatus } = useGame()

  const isLoading = gameStatus === 'isComparing'

  return (
    <div className="relative">
      <input
        className={`rounded-full bg-white/10 px-4 py-1 font-mono text-zinc-600 shadow-md outline-none ring-1 ring-red-700 backdrop-blur-md duration-300 placeholder:text-center placeholder:text-zinc-600 placeholder:opacity-50 focus:shadow-lg focus:shadow-red-700 focus:ring-2 focus:ring-red-700 ${
          isLoading
            ? 'bg-size-200 animate-gradient-x scale-105 animate-pulse bg-gradient-to-r from-red-500/20 via-orange-500/20 to-red-500/20 shadow-lg shadow-orange-500/50 ring-2 ring-orange-500'
            : ''
        }`}
        autoComplete="off"
        placeholder={isLoading ? '🔍 Comparing...' : 'Guess a word'}
        name="text"
        type="text"
        value={word}
        readOnly
      />

      {/* Loading spinner overlay */}
      {isLoading && (
        <div className="absolute right-3 top-1/2 -translate-y-1/2 transform">
          <div className="h-4 w-4 animate-spin rounded-full border-2 border-orange-500 border-t-transparent"></div>
        </div>
      )}
    </div>
  )
}
