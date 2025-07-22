import logging
import threading
from typing import Dict, Any, Optional, Union
import time

# Gensim imports
import gensim
from gensim.models import KeyedVectors
import gensim.downloader as api

from utils.exceptions import ModelError

class ModelManager:
    """
    Manages loading, caching, and lifecycle of Word2Vec/GloVe models
    """

    def __init__(self):
        """
        Initialize the ModelManager for gensim pre-trained models
        """
        self.logger = logging.getLogger(__name__)
        self.loaded_models: Dict[str, Any] = {}
        self.model_load_times: Dict[str, float] = {}
        self.load_lock = threading.RLock()  # Thread-safe model loading

        # Model configuration - all models are loaded via gensim.downloader
        self.model_config = {
            # GloVe models (via gensim-data)
            'glove-wiki-gigaword-50': {
                'name': 'glove-wiki-gigaword-50',
                'description': 'GloVe 50D vectors trained on Wikipedia+Gigaword',
                'size_mb': 69,  # Approximate download size
                'vocab_size': 400000
            },
            'glove-wiki-gigaword-100': {
                'name': 'glove-wiki-gigaword-100',
                'description': 'GloVe 100D vectors trained on Wikipedia+Gigaword',
                'size_mb': 128,
                'vocab_size': 400000
            },
            'glove-wiki-gigaword-200': {
                'name': 'glove-wiki-gigaword-200',
                'description': 'GloVe 200D vectors trained on Wikipedia+Gigaword',
                'size_mb': 252,
                'vocab_size': 400000
            },
            'glove-wiki-gigaword-300': {
                'name': 'glove-wiki-gigaword-300',
                'description': 'GloVe 300D vectors trained on Wikipedia+Gigaword',
                'size_mb': 376,
                'vocab_size': 400000
            },
            'glove-twitter-25': {
                'name': 'glove-twitter-25',
                'description': 'GloVe 25D vectors trained on Twitter (2B tweets)',
                'size_mb': 104,
                'vocab_size': 1193514
            },
            'glove-twitter-50': {
                'name': 'glove-twitter-50',
                'description': 'GloVe 50D vectors trained on Twitter (2B tweets)',
                'size_mb': 205,
                'vocab_size': 1193514
            },
            'glove-twitter-100': {
                'name': 'glove-twitter-100',
                'description': 'GloVe 100D vectors trained on Twitter (2B tweets)',
                'size_mb': 405,
                'vocab_size': 1193514
            },
            'glove-twitter-200': {
                'name': 'glove-twitter-200',
                'description': 'GloVe 200D vectors trained on Twitter (2B tweets)',
                'size_mb': 805,
                'vocab_size': 1193514
            },

            # Word2Vec models (via gensim-data)
            'word2vec-google-news-300': {
                'name': 'word2vec-google-news-300',
                'description': 'Word2Vec 300D vectors trained on Google News (3B words)',
                'size_mb': 1662,
                'vocab_size': 3000000
            },

            # FastText models (via gensim-data)
            'fasttext-wiki-news-subwords-300': {
                'name': 'fasttext-wiki-news-subwords-300',
                'description': 'FastText 300D vectors with subword info (2M vocab)',
                'size_mb': 958,
                'vocab_size': 999999
            }
        }

        self.logger.info(f"ModelManager initialized with {len(self.model_config)} gensim pre-trained models")

    def get_model(self, model_name: str, force_reload: bool = False) -> Any:
        """
        Get a loaded model, loading it if necessary

        Args:
            model_name: Name of the model to load
            force_reload: Force reload even if model is already loaded

        Returns:
            Loaded Gensim model
        """
        with self.load_lock:
            # Check if model is already loaded
            if model_name in self.loaded_models and not force_reload:
                self.logger.debug(f"Returning cached model: {model_name}")
                return self.loaded_models[model_name]

            # Validate model name
            if model_name not in self.model_config:
                available_models = list(self.model_config.keys())
                raise ModelError(f"Unknown model '{model_name}'. Available models: {available_models}")

            # Load the model
            self.logger.info(f"Loading model: {model_name}")
            start_time = time.time()

            try:
                model = self._load_model(model_name)
                load_time = time.time() - start_time

                # Cache the loaded model
                self.loaded_models[model_name] = model
                self.model_load_times[model_name] = load_time

                self.logger.info(f"Successfully loaded model '{model_name}' in {load_time:.2f} seconds")
                return model

            except Exception as e:
                load_time = time.time() - start_time
                self.logger.error(f"Failed to load model '{model_name}' after {load_time:.2f} seconds: {str(e)}")
                raise ModelError(f"Failed to load model '{model_name}': {str(e)}")

    def _load_model(self, model_name: str) -> Any:
        """
        Load a gensim pre-trained model

        Args:
            model_name: Name of the model to load

        Returns:
            Loaded Gensim model
        """
        config = self.model_config[model_name]
        return self._load_gensim_data_model(config['name'])

    def _load_gensim_data_model(self, model_name: str) -> KeyedVectors:
        """
        Load model from gensim-data repository

        Args:
            model_name: Name of the model in gensim-data

        Returns:
            Loaded KeyedVectors model
        """
        try:
            # Check if model is available
            available_models = api.info()['models'].keys()
            if model_name not in available_models:
                raise ModelError(f"Model '{model_name}' not available in gensim-data")

            # Load the model (this will download if not cached)
            self.logger.info(f"Loading model from gensim-data: {model_name}")
            model = api.load(model_name)

            return model

        except Exception as e:
            if "internet connection" in str(e).lower() or "download" in str(e).lower():
                raise ModelError(f"Failed to download model '{model_name}'. Please check your internet connection.")
            else:
                raise ModelError(f"Error loading gensim-data model '{model_name}': {str(e)}")

    def unload_model(self, model_name: str) -> bool:
        """
        Unload a model from memory to free up resources

        Args:
            model_name: Name of the model to unload

        Returns:
            True if model was unloaded, False if it wasn't loaded
        """
        with self.load_lock:
            if model_name in self.loaded_models:
                del self.loaded_models[model_name]
                if model_name in self.model_load_times:
                    del self.model_load_times[model_name]

                self.logger.info(f"Unloaded model: {model_name}")
                return True
            return False

    def unload_all_models(self):
        """Unload all models from memory"""
        with self.load_lock:
            model_count = len(self.loaded_models)
            self.loaded_models.clear()
            self.model_load_times.clear()
            self.logger.info(f"Unloaded {model_count} models from memory")

    def get_loaded_models_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about currently loaded models

        Returns:
            Dict with info about each loaded model
        """
        info = {}
        for model_name, model in self.loaded_models.items():
            try:
                vocab_size = len(model.key_to_index) if hasattr(model, 'key_to_index') else 0
                vector_size = model.vector_size if hasattr(model, 'vector_size') else 0
                load_time = self.model_load_times.get(model_name, 0)

                info[model_name] = {
                    'vocabulary_size': vocab_size,
                    'vector_size': vector_size,
                    'model_type': type(model).__name__,
                    'load_time_seconds': round(load_time, 2),
                    'description': self.model_config.get(model_name, {}).get('description', 'No description')
                }
            except Exception as e:
                info[model_name] = {
                    'error': f"Could not get info: {str(e)}"
                }

        return info

    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all available gensim pre-trained models

        Returns:
            Dict with info about each available model
        """
        available = {}
        for model_name, config in self.model_config.items():
            model_info = {
                'description': config.get('description', 'No description'),
                'estimated_size_mb': config.get('size_mb', 'Unknown'),
                'estimated_vocab_size': config.get('vocab_size', 'Unknown'),
                'loaded': model_name in self.loaded_models
            }

            if model_name in self.loaded_models:
                model_info['load_time_seconds'] = round(self.model_load_times.get(model_name, 0), 2)
                try:
                    model = self.loaded_models[model_name]
                    model_info['actual_vocabulary_size'] = len(model.key_to_index) if hasattr(model, 'key_to_index') else 0
                    model_info['vector_size'] = model.vector_size if hasattr(model, 'vector_size') else 0
                except:
                    pass

            available[model_name] = model_info

        return available

    def list_available_gensim_models(self) -> Dict[str, Any]:
        """
        Query gensim.downloader for all available models

        Returns:
            Dict with information about available models from gensim-data
        """
        try:
            info = api.info()
            return {
                'models': list(info['models'].keys()),
                'datasets': list(info['datasets'].keys()) if 'datasets' in info else []
            }
        except Exception as e:
            self.logger.error(f"Failed to get gensim model info: {str(e)}")
            return {'error': str(e)}

    def get_memory_usage_mb(self) -> float:
        """
        Estimate memory usage of loaded models (rough approximation)

        Returns:
            Estimated memory usage in MB
        """
        total_size = 0

        for model_name, model in self.loaded_models.items():
            try:
                if hasattr(model, 'key_to_index') and hasattr(model, 'vector_size'):
                    vocab_size = len(model.key_to_index)
                    vector_size = model.vector_size
                    # Rough estimate: 4 bytes per float32 + overhead
                    model_size_mb = (vocab_size * vector_size * 4) / (1024 * 1024)
                    total_size += model_size_mb
            except:
                # If we can't estimate, skip this model
                pass

        return round(total_size, 2)
