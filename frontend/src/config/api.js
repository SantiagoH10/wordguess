export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || '',
  ENDPOINTS: {
    RANDOM_WORD: '/api/word2vec/random',
    COMPARE_WORDS: '/api/word2vec/compare',
    SIMILAR_WORDS: '/api/word2vec/similar',
    WORD_EXISTS: '/api/word2vec/exists',
  },
}

export const getApiUrl = endpoint => `${API_CONFIG.BASE_URL}${endpoint}`
