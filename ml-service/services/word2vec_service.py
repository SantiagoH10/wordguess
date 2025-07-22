import random
import logging
import numpy as np
import os
from typing import Dict, List, Any, Union
import gensim
from gensim.models import KeyedVectors
from utils.exceptions import ModelError, ValidationError

class Word2VecService:
    """
    Service class to handle Word2Vec/GloVe model operations using Gensim
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def log_memory_usage(self, operation: str):
        """
        Log current memory usage for debugging

        Args:
            operation: Description of the current operation
        """
        try:
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            self.logger.info(f"{operation}: Memory usage: {memory_mb:.1f} MB")
        except Exception as e:
            self.logger.warning(f"Could not get memory info: {e}")

    def compare_words(self, model: Union[KeyedVectors, Any], word1: str, word2: str, model_name: str) -> Dict[str, Any]:
        """
        Compare similarity between two words using the provided model

        Args:
            model: Loaded Gensim model (KeyedVectors or similar)
            word1: First word to compare
            word2: Second word to compare
            model_name: Name of the model being used

        Returns:
            Dict containing similarity score and metadata
        """
        try:
            self.log_memory_usage(f"Starting word comparison: {word1} vs {word2}")

            # Check if both words exist in the model vocabulary
            if not self._word_exists_in_model(model, word1):
                raise ValidationError(f"Word '{word1}' not found in model vocabulary")

            if not self._word_exists_in_model(model, word2):
                raise ValidationError(f"Word '{word2}' not found in model vocabulary")

            # Calculate similarity
            similarity_score = model.similarity(word1, word2)

            # Convert numpy types to native Python types for JSON serialization
            if isinstance(similarity_score, np.floating):
                similarity_score = float(similarity_score)

            result = {
                'word1': word1,
                'word2': word2,
                'similarity': similarity_score,
                'model': model_name,
                'status': 'success'
            }

            self.log_memory_usage(f"Completed word comparison: {word1} vs {word2}")
            self.logger.debug(f"Similarity calculated: {word1} <-> {word2} = {similarity_score}")
            return result

        except Exception as e:
            self.logger.error(f"Error comparing words '{word1}' and '{word2}': {str(e)}")
            if isinstance(e, (ValidationError, ModelError)):
                raise
            raise ModelError(f"Failed to compare words: {str(e)}")

    def get_random_word(self, model: Union[KeyedVectors, Any], model_name: str, batch_size: int = 10, max_retries: int = 5) -> Dict[str, Any]:
        """
        Get a clean random word from the most common words in the model vocabulary

        Samples only from the first 15,000 words (Tier 1 & 2 - most common words)
        and returns the first one that meets validation criteria:
        - Only alphabetic characters (a-z, A-Z)
        - Length between 3-15 characters

        Args:
            model: Loaded Gensim model
            model_name: Name of the model being used
            batch_size: Number of words to request per batch (default: 10)
            max_retries: Maximum number of batch attempts (default: 5)

        Returns:
            Dict containing clean random word and metadata
        """
        try:
            self.log_memory_usage(f"Starting random word operation for {model_name}")

            # Get vocabulary size efficiently without loading all words
            self.logger.info(f"Getting vocabulary size for {model_name}")
            vocab_size = self._get_vocabulary_size(model)
            self.log_memory_usage(f"Got vocabulary size: {vocab_size}")

            if vocab_size == 0:
                raise ModelError("Model vocabulary is empty")

            # HARDCODED: Limit to most common words (first 15,000 indices for frequency ordering)
            MAX_WORD_INDEX = min(15000, vocab_size)
            self.logger.info(f"Using word index range: 0-{MAX_WORD_INDEX} from total {vocab_size}")

            # Try to find a clean word within retry limit
            for attempt in range(max_retries):
                self.logger.debug(f"Random word attempt {attempt + 1}/{max_retries}")
                self.log_memory_usage(f"Before batch generation (attempt {attempt + 1})")

                # Generate random indices in the common word range
                batch_indices = random.choices(range(MAX_WORD_INDEX), k=batch_size)

                # Get words at those indices
                for i, index in enumerate(batch_indices):
                    try:
                        self.logger.debug(f"Getting word at index {index} ({i+1}/{len(batch_indices)})")
                        word = self._get_word_at_index(model, index)

                        if word and self._is_clean_word(word):
                            self.logger.debug(f"Found potentially clean word: {word}")

                            # CRITICAL: Verify the word actually exists in the model vocabulary
                            if self._word_exists_in_model(model, word):
                                self.log_memory_usage(f"Verified clean word exists: {word}")

                                result = {
                                    'word': word,
                                    'model': model_name,
                                    'batch_attempt': attempt + 1,
                                    'batch_size': batch_size,
                                    'common_words_pool': MAX_WORD_INDEX,
                                    'total_vocab_size': vocab_size,
                                    'word_index': index,
                                    'status': 'success'
                                }

                                self.logger.info(f"Clean, verified word selected: '{word}' at index {index} from model {model_name}")
                                self.log_memory_usage(f"Completing random word operation successfully")
                                return result
                            else:
                                self.logger.warning(f"Word '{word}' at index {index} exists in index but not in vocabulary - skipping")
                        else:
                            if not word:
                                self.logger.debug(f"No word found at index {index}")
                            else:
                                self.logger.debug(f"Word '{word}' at index {index} failed clean word validation")

                    except Exception as e:
                        self.logger.debug(f"Error accessing word at index {index}: {str(e)}")
                        continue

                self.log_memory_usage(f"Completed batch attempt {attempt + 1}")
                self.logger.debug(f"No clean words found in batch attempt {attempt + 1}, retrying...")

            # If no clean word found after all retries, use fallback
            self.logger.warning(f"No clean words found after {max_retries} attempts, using fallback")
            self.log_memory_usage("Using fallback word")
            fallback_word = self._get_fallback_word(model_name, model)

            result = {
                'word': fallback_word,
                'model': model_name,
                'batch_attempt': max_retries,
                'batch_size': batch_size,
                'common_words_pool': MAX_WORD_INDEX,
                'total_vocab_size': vocab_size,
                'status': 'success',
                'fallback_used': True
            }

            self.log_memory_usage("Completing random word operation with fallback")
            return result

        except Exception as e:
            self.logger.error(f"Error getting random word from model: {str(e)}")
            self.log_memory_usage(f"Error in random word operation")

            # Log the full stack trace
            import traceback
            self.logger.error(f"Full stack trace: {traceback.format_exc()}")

            if isinstance(e, (ValidationError, ModelError)):
                raise
            raise ModelError(f"Failed to get random word: {str(e)}")

    def check_word_exists(self, model: Union[KeyedVectors, Any], word: str, model_name: str) -> Dict[str, Any]:
        """
        Check if a word exists in the model vocabulary

        Args:
            model: Loaded Gensim model
            word: Word to check
            model_name: Name of the model being used

        Returns:
            Dict containing existence status and metadata
        """
        try:
            exists = self._word_exists_in_model(model, word)

            result = {
                'word': word,
                'exists': exists,
                'model': model_name,
                'status': 'success'
            }

            # Add additional info if word exists
            if exists:
                try:
                    # Get word frequency rank if available
                    vocab = self._get_vocabulary(model)
                    if hasattr(model, 'get_index') or hasattr(model, 'key_to_index'):
                        word_index = model.get_index(word) if hasattr(model, 'get_index') else model.key_to_index.get(word)
                        result['vocabulary_rank'] = word_index
                except:
                    # If we can't get rank, that's okay - just don't include it
                    pass

            self.logger.debug(f"Word existence check: '{word}' exists = {exists}")
            return result

        except Exception as e:
            self.logger.error(f"Error checking word existence for '{word}': {str(e)}")
            if isinstance(e, (ValidationError, ModelError)):
                raise
            raise ModelError(f"Failed to check word existence: {str(e)}")

    def get_model_info(self, model: Union[KeyedVectors, Any], model_name: str) -> Dict[str, Any]:
        """
        Get information about the model

        Args:
            model: Loaded Gensim model
            model_name: Name of the model being used

        Returns:
            Dict containing model information and metadata
        """
        try:
            # Get basic model information efficiently
            vocab_size = self._get_vocabulary_size(model)

            # Get vector size
            vector_size = None
            if hasattr(model, 'vector_size'):
                vector_size = model.vector_size
            elif hasattr(model, 'vectors') and hasattr(model.vectors, 'shape'):
                vector_size = model.vectors.shape[1]
            elif vocab_size > 0:
                # Fallback: get vector size from first word
                try:
                    first_word = self._get_word_at_index(model, 0)
                    if first_word:
                        vector_size = len(model[first_word])
                except:
                    vector_size = None

            model_type = type(model).__name__

            result = {
                'model': model_name,
                'vocabulary_size': vocab_size,
                'vector_size': vector_size,
                'model_type': model_type,
                'status': 'success'
            }

            # Add additional info if available
            try:
                if hasattr(model, 'corpus_count'):
                    result['corpus_count'] = model.corpus_count
                if hasattr(model, 'corpus_total_words'):
                    result['total_words_trained'] = model.corpus_total_words
            except:
                # If additional info isn't available, that's fine
                pass

            self.logger.debug(f"Model info retrieved for {model_name}: {vocab_size} words, {vector_size}D vectors")
            return result

        except Exception as e:
            self.logger.error(f"Error getting model info: {str(e)}")
            if isinstance(e, (ValidationError, ModelError)):
                raise
            raise ModelError(f"Failed to get model info: {str(e)}")

    def compare_words_batch(self, model: Union[KeyedVectors, Any], comparisons: List[Dict[str, str]], model_name: str) -> Dict[str, Any]:
        """
        Compare multiple word pairs in batch for better performance

        Args:
            model: Loaded Gensim model
            comparisons: List of dicts with 'word1' and 'word2' keys
            model_name: Name of the model being used

        Returns:
            Dict containing list of similarity results and metadata
        """
        try:
            results = []
            successful_comparisons = 0
            failed_comparisons = []

            for i, comp in enumerate(comparisons):
                try:
                    word1, word2 = comp['word1'], comp['word2']

                    # Check if both words exist
                    if not self._word_exists_in_model(model, word1):
                        failed_comparisons.append({
                            'index': i,
                            'word1': word1,
                            'word2': word2,
                            'error': f"Word '{word1}' not found in vocabulary"
                        })
                        continue

                    if not self._word_exists_in_model(model, word2):
                        failed_comparisons.append({
                            'index': i,
                            'word1': word1,
                            'word2': word2,
                            'error': f"Word '{word2}' not found in vocabulary"
                        })
                        continue

                    # Calculate similarity
                    similarity_score = model.similarity(word1, word2)

                    # Convert numpy types to native Python types
                    if isinstance(similarity_score, np.floating):
                        similarity_score = float(similarity_score)

                    results.append({
                        'word1': word1,
                        'word2': word2,
                        'similarity': similarity_score
                    })

                    successful_comparisons += 1

                except Exception as e:
                    failed_comparisons.append({
                        'index': i,
                        'word1': comp.get('word1', 'unknown'),
                        'word2': comp.get('word2', 'unknown'),
                        'error': str(e)
                    })

            result = {
                'results': results,
                'model': model_name,
                'total_comparisons': len(comparisons),
                'successful_comparisons': successful_comparisons,
                'failed_comparisons': len(failed_comparisons),
                'status': 'success'
            }

            # Include failed comparisons if any
            if failed_comparisons:
                result['failures'] = failed_comparisons

            self.logger.info(f"Batch comparison completed: {successful_comparisons}/{len(comparisons)} successful")
            return result

        except Exception as e:
            self.logger.error(f"Error in batch word comparison: {str(e)}")
            if isinstance(e, (ValidationError, ModelError)):
                raise
            raise ModelError(f"Failed to perform batch comparison: {str(e)}")

    def get_most_similar_words(self, model: Union[KeyedVectors, Any], word: str, model_name: str, topn: int = 10) -> Dict[str, Any]:
        """
        Get most similar words to a given word

        Args:
            model: Loaded Gensim model
            word: Word to find similar words for
            model_name: Name of the model being used
            topn: Number of similar words to return

        Returns:
            Dict containing similar words and their similarity scores
        """
        try:
            if not self._word_exists_in_model(model, word):
                raise ValidationError(f"Word '{word}' not found in model vocabulary")

            # Get most similar words
            similar_words = model.most_similar(word, topn=topn)

            # Format results - convert numpy types to Python types
            formatted_similar = []
            for similar_word, similarity_score in similar_words:
                formatted_similar.append({
                    'word': similar_word,
                    'similarity': float(similarity_score) if isinstance(similarity_score, np.floating) else similarity_score
                })

            result = {
                'query_word': word,
                'similar_words': formatted_similar,
                'model': model_name,
                'topn': topn,
                'status': 'success'
            }

            self.logger.debug(f"Found {len(formatted_similar)} similar words for '{word}'")
            return result

        except Exception as e:
            self.logger.error(f"Error finding similar words for '{word}': {str(e)}")
            if isinstance(e, (ValidationError, ModelError)):
                raise
            raise ModelError(f"Failed to find similar words: {str(e)}")

    def _is_clean_word(self, word: str) -> bool:
        """
        Check if a word meets clean word criteria for random word selection

        Criteria:
        - Only alphabetic characters (a-z, A-Z)
        - Length between 3-15 characters

        Args:
            word: Word to validate

        Returns:
            True if word is clean, False otherwise
        """
        if not isinstance(word, str):
            return False

        # Check length
        if len(word) < 3 or len(word) > 15:
            return False

        # Check if only alphabetic characters
        if not word.isalpha():
            return False

        return True

    def _get_fallback_word(self, model_name: str, model: Union[KeyedVectors, Any] = None) -> str:
        """
        Get a fallback word when no clean words are found in random batches

        Args:
            model_name: Name of the model being used
            model: The loaded model (optional, for verification)

        Returns:
            A safe fallback word
        """
        # Curated list of common, clean words that should exist in most models
        fallback_words = [
            'word', 'time', 'person', 'year', 'way', 'day', 'thing', 'man',
            'world', 'life', 'hand', 'part', 'child', 'eye', 'woman', 'place',
            'work', 'week', 'case', 'point', 'government', 'company', 'number',
            'group', 'problem', 'fact', 'water', 'money', 'story', 'example',
            'family', 'system', 'program', 'question', 'school', 'business',
            'area', 'health', 'power', 'book', 'music', 'house', 'food'
        ]

        # If we have the model, try to find a fallback word that actually exists
        if model:
            for word in fallback_words:
                if self._word_exists_in_model(model, word):
                    self.logger.info(f"Using verified fallback word: {word}")
                    return word

            # If none of the fallback words exist, log a warning
            self.logger.warning(f"None of the fallback words exist in model {model_name}")

        # Default fallback (should work in most models)
        return random.choice(fallback_words)

    def _word_exists_in_model(self, model: Union[KeyedVectors, Any], word: str) -> bool:
        """
        Check if a word exists in the model vocabulary
        Handles different Gensim model types
        """
        try:
            # Try different methods depending on the model type
            if hasattr(model, 'has_index_for'):
                return model.has_index_for(word)
            elif hasattr(model, 'key_to_index'):
                return word in model.key_to_index
            elif hasattr(model, '__contains__'):
                return word in model
            else:
                # Fallback: try to access the word vector
                try:
                    _ = model[word]
                    return True
                except KeyError:
                    return False
        except:
            return False

    def _get_vocabulary_size(self, model: Union[KeyedVectors, Any]) -> int:
        """
        Get vocabulary size efficiently without loading all words
        """
        try:
            if hasattr(model, '__len__'):
                return len(model)
            elif hasattr(model, 'key_to_index'):
                return len(model.key_to_index)
            elif hasattr(model, 'index_to_key'):
                return len(model.index_to_key)
            elif hasattr(model, 'vocab'):
                return len(model.vocab)
            else:
                # Fallback - get full vocabulary and count
                vocab = self._get_vocabulary(model)
                return len(vocab) if vocab else 0
        except Exception as e:
            self.logger.error(f"Error getting vocabulary size: {str(e)}")
            return 0

    def _get_word_at_index(self, model: Union[KeyedVectors, Any], index: int) -> str:
        """
        Get word at specific index efficiently
        """
        try:
            word = None

            # Primary method for modern Gensim models
            if hasattr(model, 'index_to_key'):
                if index < len(model.index_to_key):
                    word = model.index_to_key[index]
            # Alternative for older versions
            elif hasattr(model, 'index2word'):
                if index < len(model.index2word):
                    word = model.index2word[index]
            # KeyedVectors approach
            elif hasattr(model, 'key_to_index'):
                # This is less efficient but works
                keys = list(model.key_to_index.keys())
                if index < len(keys):
                    word = keys[index]

            # Validate the word is not None, empty, or just whitespace
            if word and isinstance(word, str) and word.strip():
                return word.strip()
            else:
                self.logger.debug(f"Invalid word at index {index}: {repr(word)}")
                return None

        except (IndexError, AttributeError, Exception) as e:
            self.logger.debug(f"Error getting word at index {index}: {str(e)}")
            return None

    def _get_vocabulary(self, model: Union[KeyedVectors, Any]) -> Union[Dict, List]:
        """
        Get model vocabulary - handles different Gensim model types
        """
        try:
            # Primary method for modern Gensim (most models including Word2Vec)
            if hasattr(model, 'index_to_key'):
                return model.index_to_key
            # Alternative for KeyedVectors
            elif hasattr(model, 'key_to_index'):
                return list(model.key_to_index.keys())
            # Older Gensim versions
            elif hasattr(model, 'index2word'):
                return model.index2word
            # Even older versions or custom models
            elif hasattr(model, 'vocab'):
                return list(model.vocab.keys())
            # Last resort - try to get keys directly
            elif hasattr(model, 'keys'):
                return list(model.keys())
            else:
                raise ModelError("Unable to determine vocabulary access method")
        except Exception as e:
            self.logger.error(f"Error accessing model vocabulary: {str(e)}")
            raise ModelError(f"Unable to access model vocabulary: {str(e)}")
