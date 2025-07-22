import { useGame } from '../logic/useGame'

const MODELS = ['glove-wiki-gigaword-100', 'word2vec-google-news-300']

export function ModelSelector() {
  const { model } = useGame()
  return (
    <div className="container mx-auto flex justify-center rounded-2xl border border-white/20 bg-white/10 px-3 py-2 shadow-xl backdrop-blur-md">
      <p>Current model : {model}</p>
    </div>
  )
}
