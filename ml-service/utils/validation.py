"""
Validation utilities for Word2Vec ML service
"""

import re
import logging
from typing import List, Optional, Union

from utils.exceptions import ValidationError, ModelNotFoundError, raise_validation_error

# Setup logger
logger = logging.getLogger(__name__)

# Constants for validation
MIN_WORD_LENGTH = 1
MAX_WORD_LENGTH = 100
MAX_BATCH_SIZE = 1000

# Valid model names - should match ModelManager configuration
VALID_MODELS = {
    'glove-wiki-gigaword-50',
    'glove-wiki-gigaword-100',
    'glove-wiki-gigaword-200',
    'glove-wiki-gigaword-300',
    'glove-twitter-25',
    'glove-twitter-50',
    'glove-twitter-100',
    'glove-twitter-200',
    'word2vec-google-news-300',
    'fasttext-wiki-news-subwords-300'
}

# Default model
DEFAULT_MODEL = 'glove-wiki-gigaword-100'

# Word validation patterns
WORD_PATTERN = re.compile(r'^[a-zA-Z0-9\-_\'\.]+$')  # Letters, numbers, hyphens, underscores, apostrophes, dots
WORD_BLACKLIST = {
    '',
    ' ',
    '\t',
    '\n',
    '\r'
}


def validate_word(word: Union[str, None], field_name: str = 'word') -> str:
    """
    Validate a word input

    Args:
        word: The word to validate
        field_name: Name of the field being validated (for error messages)

    Returns:
        The validated and cleaned word

    Raises:
        ValidationError: If the word is invalid
    """
    # Check if word is provided
    if word is None:
        raise_validation_error(f"'{field_name}' is required", field_name, None)

    # Convert to string and strip whitespace
    if not isinstance(word, str):
        try:
            word = str(word)
        except:
            raise_validation_error(f"'{field_name}' must be a string", field_name, word)

    original_word = word
    word = word.strip()

    # Check for empty or whitespace-only strings
    if not word or word in WORD_BLACKLIST:
        raise_validation_error(f"'{field_name}' cannot be empty or whitespace", field_name, original_word)

    # Check length
    if len(word) < MIN_WORD_LENGTH:
        raise_validation_error(
            f"'{field_name}' must be at least {MIN_WORD_LENGTH} character(s) long",
            field_name,
            word
        )

    if len(word) > MAX_WORD_LENGTH:
        raise_validation_error(
            f"'{field_name}' cannot be longer than {MAX_WORD_LENGTH} characters",
            field_name,
            word
        )

    # Check for valid characters
    if not WORD_PATTERN.match(word):
        raise_validation_error(
            f"'{field_name}' contains invalid characters. Only letters, numbers, hyphens, underscores, apostrophes, and dots are allowed",
            field_name,
            word
        )

    # Additional checks for common issues
    if word.startswith('-') or word.endswith('-'):
        raise_validation_error(f"'{field_name}' cannot start or end with a hyphen", field_name, word)

    if word.startswith('_') or word.endswith('_'):
        raise_validation_error(f"'{field_name}' cannot start or end with an underscore", field_name, word)

    # Check for consecutive special characters
    if '--' in word or '__' in word or '..' in word:
        raise_validation_error(f"'{field_name}' cannot contain consecutive special characters", field_name, word)

    logger.debug(f"Successfully validated {field_name}: '{word}'")
    return word


def validate_model(model: Union[str, None]) -> str:
    """
    Validate a model name

    Args:
        model: The model name to validate

    Returns:
        The validated model name

    Raises:
        ValidationError: If the model name is invalid
        ModelNotFoundError: If the model is not available
    """
    # Use default if no model provided
    if model is None or (isinstance(model, str) and not model.strip()):
        logger.debug(f"No model specified, using default: {DEFAULT_MODEL}")
        return DEFAULT_MODEL

    # Convert to string and clean
    if not isinstance(model, str):
        try:
            model = str(model)
        except:
            raise_validation_error("Model name must be a string", 'model', model)

    model = model.strip()

    # Check if model is in our valid models list
    if model not in VALID_MODELS:
        available_models = sorted(list(VALID_MODELS))
        raise ModelNotFoundError(model, available_models)

    logger.debug(f"Successfully validated model: '{model}'")
    return model


def validate_word_pair(word1: Union[str, None], word2: Union[str, None]) -> tuple[str, str]:
    """
    Validate a pair of words for comparison

    Args:
        word1: First word
        word2: Second word

    Returns:
        Tuple of (validated_word1, validated_word2)

    Raises:
        ValidationError: If either word is invalid
    """
    validated_word1 = validate_word(word1, 'word1')
    validated_word2 = validate_word(word2, 'word2')

    # Check if words are identical
    if validated_word1.lower() == validated_word2.lower():
        logger.warning(f"Comparing identical words: '{validated_word1}' vs '{validated_word2}'")

    return validated_word1, validated_word2


def validate_batch_comparisons(comparisons: Union[List, None]) -> List[dict]:
    """
    Validate a batch of word comparisons

    Args:
        comparisons: List of comparison dictionaries

    Returns:
        List of validated comparison dictionaries

    Raises:
        ValidationError: If the batch is invalid
    """
    if comparisons is None:
        raise_validation_error("'comparisons' field is required", 'comparisons', None)

    if not isinstance(comparisons, list):
        raise_validation_error("'comparisons' must be a list", 'comparisons', type(comparisons).__name__)

    if len(comparisons) == 0:
        raise_validation_error("'comparisons' cannot be empty", 'comparisons', comparisons)

    if len(comparisons) > MAX_BATCH_SIZE:
        raise_validation_error(
            f"Batch size cannot exceed {MAX_BATCH_SIZE} comparisons",
            'comparisons',
            len(comparisons)
        )

    validated_comparisons = []

    for i, comparison in enumerate(comparisons):
        if not isinstance(comparison, dict):
            raise_validation_error(
                f"Comparison at index {i} must be a dictionary",
                f'comparisons[{i}]',
                type(comparison).__name__
            )

        if 'word1' not in comparison:
            raise_validation_error(
                f"Comparison at index {i} is missing 'word1' field",
                f'comparisons[{i}].word1',
                None
            )

        if 'word2' not in comparison:
            raise_validation_error(
                f"Comparison at index {i} is missing 'word2' field",
                f'comparisons[{i}].word2',
                None
            )

        try:
            word1, word2 = validate_word_pair(comparison['word1'], comparison['word2'])
            validated_comparisons.append({
                'word1': word1,
                'word2': word2
            })
        except ValidationError as e:
            # Re-raise with batch context
            raise_validation_error(
                f"Error in comparison at index {i}: {e.message}",
                f'comparisons[{i}]',
                comparison
            )

    logger.debug(f"Successfully validated batch of {len(validated_comparisons)} comparisons")
    return validated_comparisons


def validate_topn(topn: Union[int, str, None], default: int = 10, max_value: int = 100) -> int:
    """
    Validate topn parameter for similarity queries

    Args:
        topn: Number of top results to return
        default: Default value if None provided
        max_value: Maximum allowed value

    Returns:
        Validated topn value

    Raises:
        ValidationError: If topn is invalid
    """
    if topn is None:
        return default

    # Try to convert to int
    try:
        if isinstance(topn, str):
            topn = int(topn)
        elif not isinstance(topn, int):
            topn = int(topn)
    except (ValueError, TypeError):
        raise_validation_error("'topn' must be an integer", 'topn', topn)

    if topn < 1:
        raise_validation_error("'topn' must be at least 1", 'topn', topn)

    if topn > max_value:
        raise_validation_error(f"'topn' cannot exceed {max_value}", 'topn', topn)

    return topn


def validate_request_json(request_data: Union[dict, None], required_fields: List[str] = None) -> dict:
    """
    Validate JSON request data

    Args:
        request_data: The request data to validate
        required_fields: List of required field names

    Returns:
        Validated request data

    Raises:
        ValidationError: If the request data is invalid
    """
    if request_data is None:
        raise_validation_error("Request body must contain JSON data", 'request_body', None)

    if not isinstance(request_data, dict):
        raise_validation_error("Request body must be a JSON object", 'request_body', type(request_data).__name__)

    if required_fields:
        for field in required_fields:
            if field not in request_data:
                raise_validation_error(f"Required field '{field}' is missing", field, None)

    return request_data


def sanitize_word(word: str) -> str:
    """
    Sanitize a word by applying common transformations

    Args:
        word: Word to sanitize

    Returns:
        Sanitized word
    """
    if not isinstance(word, str):
        return word

    # Convert to lowercase for consistent processing
    sanitized = word.lower().strip()

    # Remove common prefixes/suffixes that might cause issues
    # (This could be expanded based on your specific needs)

    return sanitized


def get_validation_summary() -> dict:
    """
    Get a summary of validation rules and constraints

    Returns:
        Dictionary with validation rules
    """
    return {
        'word_validation': {
            'min_length': MIN_WORD_LENGTH,
            'max_length': MAX_WORD_LENGTH,
            'allowed_characters': 'letters, numbers, hyphens, underscores, apostrophes, dots',
            'forbidden_patterns': ['consecutive special characters', 'leading/trailing hyphens or underscores']
        },
        'model_validation': {
            'available_models': sorted(list(VALID_MODELS)),
            'default_model': DEFAULT_MODEL
        },
        'batch_validation': {
            'max_batch_size': MAX_BATCH_SIZE
        },
        'similarity_validation': {
            'max_topn': 100,
            'default_topn': 10
        }
    }


def is_valid_word(word: str, silent: bool = True) -> bool:
    """
    Check if a word is valid without raising exceptions

    Args:
        word: Word to check
        silent: If True, don't log warnings

    Returns:
        True if word is valid, False otherwise
    """
    try:
        validate_word(word)
        return True
    except ValidationError as e:
        if not silent:
            logger.warning(f"Word validation failed: {e.message}")
        return False


def is_valid_model(model: str, silent: bool = True) -> bool:
    """
    Check if a model name is valid without raising exceptions

    Args:
        model: Model name to check
        silent: If True, don't log warnings

    Returns:
        True if model is valid, False otherwise
    """
    try:
        validate_model(model)
        return True
    except (ValidationError, ModelNotFoundError) as e:
        if not silent:
            logger.warning(f"Model validation failed: {e.message}")
        return False
