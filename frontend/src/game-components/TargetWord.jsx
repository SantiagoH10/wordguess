import { useState } from 'react'
import { useGame } from '../logic/useGame'

export function TargetWord() {
  const { targetWord } = useGame()
  const [displayWord, setDisplayWord] = useState(false)

  return (
    <div className="flex items-center gap-3">
      <div className="rounded-full bg-white/10 px-4 py-1 font-mono text-zinc-600 shadow-md outline-none ring-1 ring-red-700 backdrop-blur-md duration-300 placeholder:text-center placeholder:text-zinc-600 placeholder:opacity-50 focus:shadow-lg focus:shadow-red-700 focus:ring-2 focus:ring-red-700">
        <p>
          Word to guess :{' '}
          {displayWord ? targetWord : '•'.repeat(targetWord.length)}
        </p>
      </div>

      <div className="flex items-center gap-2">
        <span className="text-sm font-medium text-zinc-700">Display word</span>

        {/* Toggle Switch */}
        <button
          onClick={() => setDisplayWord(!displayWord)}
          className={`relative inline-flex h-6 w-11 items-center rounded-full border-2 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-red-700 focus:ring-offset-2 ${
            displayWord
              ? 'border-red-700 bg-red-700'
              : 'border-gray-300 bg-gray-200'
          }`}
        >
          <span
            className={`inline-block h-4 w-4 transform rounded-full bg-white shadow-sm transition-transform duration-200 ${
              displayWord ? 'translate-x-6' : 'translate-x-1'
            }`}
          />
        </button>
      </div>
    </div>
  )
}
