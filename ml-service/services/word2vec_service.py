import random
import logging
import numpy as np
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

            self.logger.debug(f"Similarity calculated: {word1} <-> {word2} = {similarity_score}")
            return result

        except Exception as e:
            self.logger.error(f"Error comparing words '{word1}' and '{word2}': {str(e)}")
            if isinstance(e, (ValidationError, ModelError)):
                raise
            raise ModelError(f"Failed to compare words: {str(e)}")

    def get_random_word(self, model: Union[KeyedVectors, Any], model_name: str) -> Dict[str, Any]:
        """
        Get a random word from the model vocabulary

        Args:
            model: Loaded Gensim model
            model_name: Name of the model being used

        Returns:
            Dict containing random word and metadata
        """
        try:
            # Get vocabulary - different models might store this differently
            vocab = self._get_vocabulary(model)

            if not vocab:
                raise ModelError("Model vocabulary is empty")

            # Select random word
            random_word = random.choice(list(vocab))

            result = {
                'word': random_word,
                'model': model_name,
                'status': 'success'
            }

            self.logger.debug(f"Random word selected: '{random_word}' from model {model_name}")
            return result

        except Exception as e:
            self.logger.error(f"Error getting random word from model: {str(e)}")
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
            # Get basic model information
            vocab_size = len(self._get_vocabulary(model))
            vector_size = model.vector_size if hasattr(model, 'vector_size') else len(model[list(model.key_to_index.keys())[0]])
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

    def _get_vocabulary(self, model: Union[KeyedVectors, Any]) -> Union[Dict, List]:
        """
        Get model vocabulary - handles different Gensim model types
        """
        if hasattr(model, 'key_to_index'):
            return model.key_to_index
        elif hasattr(model, 'index_to_key'):
            return model.index_to_key
        elif hasattr(model, 'index2word'):
            return model.index2word
        elif hasattr(model, 'vocab'):
            return model.vocab
        else:
            # Fallback - try to get keys from the model
            try:
                return list(model.keys()) if hasattr(model, 'keys') else []
            except:
                raise ModelError("Unable to access model vocabulary")
