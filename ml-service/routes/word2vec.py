from flask import Blueprint, request, jsonify, current_app
import logging

# Import custom modules (we'll create these)
from utils.validation import validate_word, validate_model
from services.word2vec_service import Word2VecService
from utils.exceptions import ValidationError, ModelError

# Create Blueprint
word2vec_bp = Blueprint('word2vec', __name__)

# Initialize service
word2vec_service = Word2VecService()

# Setup logger
logger = logging.getLogger(__name__)

@word2vec_bp.route('/compare', methods=['POST'])
def compare_words():
    """
    Compare similarity between two words

    Expected JSON body:
    {
        "word1": "king",
        "word2": "queen",
        "model": "glove-wiki-gigaword-100" (optional)
    }

    Returns:
    {
        "word1": "king",
        "word2": "queen",
        "model": "glove-wiki-gigaword-100",
        "similarity": 0.7234,
        "status": "success"
    }
    """
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            raise ValidationError("Request body must contain JSON data")

        # Extract parameters
        word1 = data.get('word1')
        word2 = data.get('word2')
        model = data.get('model', 'glove-wiki-gigaword-100')

        # Validate inputs
        validated_word1 = validate_word(word1)
        validated_word2 = validate_word(word2)
        validated_model = validate_model(model)

        logger.info(f"Comparing words: '{validated_word1}' vs '{validated_word2}' using model: {validated_model}")

        # Get model from model manager
        gensim_model = current_app.model_manager.get_model(validated_model)

        # Perform comparison using service
        result = word2vec_service.compare_words(
            gensim_model,
            validated_word1,
            validated_word2,
            validated_model
        )

        logger.info(f"Word comparison successful. Similarity: {result['similarity']}")
        return jsonify(result)

    except ValidationError as e:
        logger.warning(f"Validation error in compare_words: {str(e)}")
        raise
    except ModelError as e:
        logger.error(f"Model error in compare_words: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in compare_words: {str(e)}", exc_info=True)
        raise


@word2vec_bp.route('/random', methods=['POST'])
def get_random_word():
    """
    Get a random word from the model vocabulary

    Expected JSON body:
    {
        "model": "glove-wiki-gigaword-100" (optional)
    }

    Returns:
    {
        "word": "elephant",
        "model": "glove-wiki-gigaword-100",
        "status": "success"
    }
    """
    try:
        # Get JSON data (body might be empty for default model)
        data = request.get_json() or {}

        # Extract model parameter
        model = data.get('model', 'glove-wiki-gigaword-100')

        # Validate model
        validated_model = validate_model(model)

        logger.info(f"Getting random word from model: {validated_model}")

        # Get model from model manager
        gensim_model = current_app.model_manager.get_model(validated_model)

        # Get random word using service
        result = word2vec_service.get_random_word(gensim_model, validated_model)

        logger.info(f"Random word generated: '{result['word']}'")
        return jsonify(result)

    except ValidationError as e:
        logger.warning(f"Validation error in get_random_word: {str(e)}")
        raise
    except ModelError as e:
        logger.error(f"Model error in get_random_word: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_random_word: {str(e)}", exc_info=True)
        raise


@word2vec_bp.route('/exists', methods=['POST'])
def check_word_exists():
    """
    Check if a word exists in the model vocabulary

    Expected JSON body:
    {
        "word": "elephant",
        "model": "glove-wiki-gigaword-100" (optional)
    }

    Returns:
    {
        "word": "elephant",
        "exists": true,
        "model": "glove-wiki-gigaword-100",
        "status": "success"
    }
    """
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            raise ValidationError("Request body must contain JSON data")

        # Extract parameters
        word = data.get('word')
        model = data.get('model', 'glove-wiki-gigaword-100')

        # Validate inputs
        validated_word = validate_word(word)
        validated_model = validate_model(model)

        logger.info(f"Checking if word '{validated_word}' exists in model: {validated_model}")

        # Get model from model manager
        gensim_model = current_app.model_manager.get_model(validated_model)

        # Check existence using service
        result = word2vec_service.check_word_exists(
            gensim_model,
            validated_word,
            validated_model
        )

        logger.info(f"Word existence check: '{validated_word}' exists = {result['exists']}")
        return jsonify(result)

    except ValidationError as e:
        logger.warning(f"Validation error in check_word_exists: {str(e)}")
        raise
    except ModelError as e:
        logger.error(f"Model error in check_word_exists: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in check_word_exists: {str(e)}", exc_info=True)
        raise


@word2vec_bp.route('/info', methods=['GET'])
def get_model_info():
    """
    Get information about a model

    Query parameters:
    ?model=glove-wiki-gigaword-100 (optional)

    Returns:
    {
        "model": "glove-wiki-gigaword-100",
        "vocabulary_size": 400000,
        "vector_size": 100,
        "model_type": "KeyedVectors",
        "status": "success"
    }
    """
    try:
        # Get model from query parameters
        model = request.args.get('model', 'glove-wiki-gigaword-100')

        # Validate model
        validated_model = validate_model(model)

        logger.info(f"Getting info for model: {validated_model}")

        # Get model from model manager
        gensim_model = current_app.model_manager.get_model(validated_model)

        # Get model info using service
        result = word2vec_service.get_model_info(gensim_model, validated_model)

        logger.info(f"Model info retrieved for: {validated_model}")
        return jsonify(result)

    except ValidationError as e:
        logger.warning(f"Validation error in get_model_info: {str(e)}")
        raise
    except ModelError as e:
        logger.error(f"Model error in get_model_info: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_model_info: {str(e)}", exc_info=True)
        raise


# Optional: Batch operations endpoint for better performance
@word2vec_bp.route('/compare-batch', methods=['POST'])
def compare_words_batch():
    """
    Compare multiple word pairs in a single request for better performance

    Expected JSON body:
    {
        "comparisons": [
            {"word1": "king", "word2": "queen"},
            {"word1": "man", "word2": "woman"},
            {"word1": "cat", "word2": "dog"}
        ],
        "model": "glove-wiki-gigaword-100" (optional)
    }

    Returns:
    {
        "results": [
            {"word1": "king", "word2": "queen", "similarity": 0.7234},
            {"word1": "man", "word2": "woman", "similarity": 0.6543},
            {"word1": "cat", "word2": "dog", "similarity": 0.4321}
        ],
        "model": "glove-wiki-gigaword-100",
        "status": "success"
    }
    """
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            raise ValidationError("Request body must contain JSON data")

        comparisons = data.get('comparisons', [])
        model = data.get('model', 'glove-wiki-gigaword-100')

        if not comparisons or not isinstance(comparisons, list):
            raise ValidationError("'comparisons' must be a non-empty list")

        # Validate model
        validated_model = validate_model(model)

        # Validate each comparison pair
        validated_comparisons = []
        for comp in comparisons:
            if not isinstance(comp, dict) or 'word1' not in comp or 'word2' not in comp:
                raise ValidationError("Each comparison must have 'word1' and 'word2' fields")

            validated_comparisons.append({
                'word1': validate_word(comp['word1']),
                'word2': validate_word(comp['word2'])
            })

        logger.info(f"Processing batch comparison of {len(validated_comparisons)} word pairs using model: {validated_model}")

        # Get model from model manager
        gensim_model = current_app.model_manager.get_model(validated_model)

        # Perform batch comparison using service
        result = word2vec_service.compare_words_batch(
            gensim_model,
            validated_comparisons,
            validated_model
        )

        logger.info(f"Batch word comparison completed successfully")
        return jsonify(result)

    except ValidationError as e:
        logger.warning(f"Validation error in compare_words_batch: {str(e)}")
        raise
    except ModelError as e:
        logger.error(f"Model error in compare_words_batch: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in compare_words_batch: {str(e)}", exc_info=True)
        raise


# Health check for this specific blueprint
@word2vec_bp.route('/health', methods=['GET'])
def word2vec_health():
    """Health check specific to word2vec endpoints"""
    try:
        # Try to access the model manager
        loaded_models = list(current_app.model_manager.loaded_models.keys())

        return jsonify({
            'status': 'healthy',
            'blueprint': 'word2vec',
            'loaded_models': loaded_models,
            'available_endpoints': [
                '/api/compare',
                '/api/random',
                '/api/exists',
                '/api/info',
                '/api/compare-batch'
            ]
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500
