import gensim.downloader as api
import json
import argparse
import sys
import random

# Global cache for models
_model_cache = {}

def load_model(model_type):
    """Load model with caching"""
    if model_type not in _model_cache:
        print(f"Loading {model_type} model... (this may take a moment)", file=sys.stderr)
        try:
            _model_cache[model_type] = api.load(model_type)
            print(f"Model {model_type} loaded successfully!", file=sys.stderr)
        except Exception as e:
            print(f"Error loading model {model_type}: {e}", file=sys.stderr)
            sys.exit(1)

    return _model_cache[model_type]

def get_random_word(model, exclude_common=True):
    """Get a random word from the vocabulary"""
    try:
        vocab = list(model.key_to_index.keys())

        if exclude_common:
            # Filter out very common words and punctuation
            common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
            vocab = [word for word in vocab if word.lower() not in common_words and word.isalpha()]

        if not vocab:
            return None

        return random.choice(vocab)
    except Exception as e:
        return None

def get_similar_words(model, word, top_n=10):
    """Get similar words"""
    try:
        if word not in model.key_to_index:
            return []

        similar = model.most_similar(word, topn=top_n)
        return [{"word": w, "similarity": float(s)} for w, s in similar]
    except Exception as e:
        return []

def compare_words(model, word1, word2):
    """Compare similarity between two words"""
    try:
        if word1 not in model.key_to_index:
            return {"error": f"Word '{word1}' not found in vocabulary"}

        if word2 not in model.key_to_index:
            return {"error": f"Word '{word2}' not found in vocabulary"}

        similarity = model.similarity(word1, word2)
        return {
            "word1": word1,
            "word2": word2,
            "similarity": float(similarity),
            "interpretation": get_similarity_interpretation(similarity)
        }
    except Exception as e:
        return {"error": str(e)}

def get_similarity_interpretation(similarity):
    """Provide human-readable interpretation of similarity score"""
    if similarity >= 0.7:
        return "Very similar"
    elif similarity >= 0.5:
        return "Similar"
    elif similarity >= 0.3:
        return "Somewhat similar"
    elif similarity >= 0.1:
        return "Slightly similar"
    else:
        return "Not similar"

def word_exists(model, word):
    """Check if word exists in vocabulary"""
    return word in model.key_to_index

def get_vocab_info(model):
    """Get vocabulary information"""
    try:
        vocab_size = len(model.key_to_index)
        vector_size = model.vector_size
        return {
            "vocab_size": vocab_size,
            "vector_size": vector_size,
            "model_type": type(model).__name__
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description='Word2Vec CLI Tool')
    parser.add_argument('--model', default='glove-wiki-gigaword-100',
                       choices=['glove-wiki-gigaword-100', 'glove-wiki-gigaword-300',
                               'word2vec-google-news-300', 'glove-twitter-100',
                               'glove-twitter-50', 'glove-twitter-25'],
                       help='Model to use')

    parser.add_argument('--operation', required=True,
                       choices=['similar', 'compare', 'random', 'exists', 'info'],
                       help='Operation to perform')

    parser.add_argument('--word', help='Word for similarity search or existence check')
    parser.add_argument('--word1', help='First word for comparison')
    parser.add_argument('--word2', help='Second word for comparison')
    parser.add_argument('--top_n', type=int, default=10, help='Number of similar words to return')

    args = parser.parse_args()

    # Load model (cached)
    model = load_model(args.model)

    # Perform operation
    if args.operation == 'similar':
        if not args.word:
            result = {"error": "Word is required for similarity search"}
        else:
            similar_words = get_similar_words(model, args.word.lower(), args.top_n)
            result = {
                "operation": "similar",
                "word": args.word,
                "model": args.model,
                "similar_words": similar_words,
                "found": len(similar_words) > 0
            }

    elif args.operation == 'compare':
        if not args.word1 or not args.word2:
            result = {"error": "Both word1 and word2 are required for comparison"}
        else:
            comparison = compare_words(model, args.word1.lower(), args.word2.lower())
            result = {
                "operation": "compare",
                "model": args.model,
                **comparison
            }

    elif args.operation == 'random':
        random_word = get_random_word(model)
        if random_word:
            result = {
                "operation": "random",
                "model": args.model,
                "word": random_word
            }
        else:
            result = {"error": "Could not generate random word"}

    elif args.operation == 'exists':
        if not args.word:
            result = {"error": "Word is required for existence check"}
        else:
            exists = word_exists(model, args.word.lower())
            result = {
                "operation": "exists",
                "word": args.word,
                "model": args.model,
                "exists": exists
            }

    elif args.operation == 'info':
        vocab_info = get_vocab_info(model)
        result = {
            "operation": "info",
            "model": args.model,
            **vocab_info
        }

    else:
        result = {"error": "Unknown operation"}

    # Return JSON
    print(json.dumps(result))

if __name__ == "__main__":
    main()
