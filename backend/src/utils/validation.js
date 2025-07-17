export const validateWord = word => {
  if (!word || typeof word !== 'string') {
    throw new Error('Invalid word: must be a non-empty string')
  }

  if (word.length > 50) {
    throw new Error('Word too long: maximum 50 characters')
  }

  // Remove special characters and keep only letters
  const cleaned = word
    .trim()
    .toLowerCase()
    .replace(/[^a-z]/g, '')

  if (!cleaned) {
    throw new Error('Invalid word: must contain at least one letter')
  }

  return cleaned
}

export const validateModel = model => {
  const validModels = [
    'glove-wiki-gigaword-100',
    'glove-wiki-gigaword-300',
    'word2vec-google-news-300',
    'glove-twitter-100',
    'glove-twitter-50',
    'glove-twitter-25',
  ]

  if (!validModels.includes(model)) {
    throw new Error(`Invalid model: must be one of ${validModels.join(', ')}`)
  }

  return model
}

export const validateTopN = topN => {
  const num = parseInt(topN)

  if (isNaN(num) || num < 1 || num > 100) {
    throw new Error('Invalid top_n: must be a number between 1 and 100')
  }

  return num
}
