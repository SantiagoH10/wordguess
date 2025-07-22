import { useGame } from '../logic/useGame'

const MODELS = ['glove-wiki-gigaword-100', 'word2vec-google-news-300']

export function ModelSelector() {
  const { model, changeModel } = useGame()
  return (
    <div className="container mx-auto flex flex-col items-center justify-center rounded-2xl border border-white/20 bg-white/10 px-3 py-2 shadow-xl backdrop-blur-md">
      <p className="text-lg font-thin">Models</p>
      <div className="flex gap-2">
        {MODELS.map(m => {
          const isCurrentModel = m === model
          return (
            <button
              className={`rounded-full px-2 py-1 text-xs transition-all ${
                isCurrentModel
                  ? 'cursor-pointer bg-ccblue text-white hover:bg-blue-600'
                  : 'cursor-default border-2 border-ccblue bg-white text-ccblue'
              }`}
              key={m}
              onClick={isCurrentModel ? undefined : () => changeModel(m)}
              disabled={isCurrentModel}
            >
              {m}
            </button>
          )
        })}
      </div>
    </div>
  )
}
