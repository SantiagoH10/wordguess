import { useGame } from '../logic/useGame'

const MODELS = ['glove-wiki-gigaword-100', 'word2vec-google-news-300']

export function ModelSelector() {
  const { model, changeModel } = useGame()
  return (
    <div className="container mx-auto flex flex-col justify-center items-center rounded-2xl border border-white/20 bg-white/10 px-3 py-2 shadow-xl backdrop-blur-md">
      <p className='text-lg font-thin'>Models</p>
      <div className='flex gap-2'>
      {MODELS.map(m => {
        const isCurrentModel = m === model
        return(
          <button
            className={`text-xs px-2 py-1 rounded-full transition-all ${
              isCurrentModel
                ? 'bg-ccblue text-white hover:bg-blue-600 cursor-pointer'
                : 'bg-white text-ccblue border-ccblue border-2 cursor-default'
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
