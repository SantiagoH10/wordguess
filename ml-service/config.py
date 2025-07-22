"""
Configuration settings for Word2Vec ML Service
"""

import os
from typing import List, Dict, Any

class Config:
    """
    Base configuration class
    """
    # Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'word2vec-ml-service-secret-key-change-in-production')
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True

    # Server Settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 'yes']
    THREADED = True

    # CORS Settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:8000').split(',')
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization', 'X-Requested-With']
    CORS_METHODS = ['GET', 'POST', 'OPTIONS']

    # Model Settings
    DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL', 'word2vec-google-news-300')
    PRELOAD_DEFAULT_MODEL = os.environ.get('PRELOAD_DEFAULT_MODEL', 'True').lower() in ['true', '1', 'yes']
    MODEL_CACHE_SIZE_LIMIT = int(os.environ.get('MODEL_CACHE_SIZE_LIMIT', 5))  # Max models in memory
    MODEL_LOAD_TIMEOUT = int(os.environ.get('MODEL_LOAD_TIMEOUT', 300))  # 5 minutes

    # Validation Settings
    MIN_WORD_LENGTH = int(os.environ.get('MIN_WORD_LENGTH', 1))
    MAX_WORD_LENGTH = int(os.environ.get('MAX_WORD_LENGTH', 100))
    MAX_BATCH_SIZE = int(os.environ.get('MAX_BATCH_SIZE', 1000))
    MAX_SIMILARITY_RESULTS = int(os.environ.get('MAX_SIMILARITY_RESULTS', 100))
    DEFAULT_SIMILARITY_RESULTS = int(os.environ.get('DEFAULT_SIMILARITY_RESULTS', 10))

    # Performance Settings
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 60))  # seconds
    MAX_CONCURRENT_REQUESTS = int(os.environ.get('MAX_CONCURRENT_REQUESTS', 100))
    ENABLE_REQUEST_LOGGING = os.environ.get('ENABLE_REQUEST_LOGGING', 'True').lower() in ['true', '1', 'yes']

    # Logging Settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
    LOG_FORMAT = os.environ.get('LOG_FORMAT', '%(asctime)s %(levelname)s %(name)s: %(message)s')
    ENABLE_ACCESS_LOGS = os.environ.get('ENABLE_ACCESS_LOGS', 'True').lower() in ['true', '1', 'yes']
    LOG_FILE = os.environ.get('LOG_FILE', None)  # None = stdout only

    # Health Check Settings
    HEALTH_CHECK_MODELS = os.environ.get('HEALTH_CHECK_MODELS', 'True').lower() in ['true', '1', 'yes']
    HEALTH_CHECK_MEMORY = os.environ.get('HEALTH_CHECK_MEMORY', 'True').lower() in ['true', '1', 'yes']

    # Rate Limiting Settings (if needed in future)
    ENABLE_RATE_LIMITING = os.environ.get('ENABLE_RATE_LIMITING', 'False').lower() in ['true', '1', 'yes']
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', 60))

    # Memory Management Settings
    MAX_MEMORY_USAGE_MB = int(os.environ.get('MAX_MEMORY_USAGE_MB', 8192))  # 8GB default
    MEMORY_CHECK_INTERVAL = int(os.environ.get('MEMORY_CHECK_INTERVAL', 300))  # 5 minutes
    AUTO_UNLOAD_UNUSED_MODELS = os.environ.get('AUTO_UNLOAD_UNUSED_MODELS', 'False').lower() in ['true', '1', 'yes']
    UNUSED_MODEL_TIMEOUT = int(os.environ.get('UNUSED_MODEL_TIMEOUT', 3600))  # 1 hour

    # Available Models Configuration
    AVAILABLE_MODELS = {
        'glove-wiki-gigaword-50': {
            'name': 'glove-wiki-gigaword-50',
            'description': 'GloVe 50D vectors trained on Wikipedia+Gigaword',
            'size_mb': 69,
            'vocab_size': 400000,
            'vector_size': 50
        },
        'glove-wiki-gigaword-100': {
            'name': 'glove-wiki-gigaword-100',
            'description': 'GloVe 100D vectors trained on Wikipedia+Gigaword',
            'size_mb': 128,
            'vocab_size': 400000,
            'vector_size': 100
        },
        'glove-wiki-gigaword-200': {
            'name': 'glove-wiki-gigaword-200',
            'description': 'GloVe 200D vectors trained on Wikipedia+Gigaword',
            'size_mb': 252,
            'vocab_size': 400000,
            'vector_size': 200
        },
        'glove-wiki-gigaword-300': {
            'name': 'glove-wiki-gigaword-300',
            'description': 'GloVe 300D vectors trained on Wikipedia+Gigaword',
            'size_mb': 376,
            'vocab_size': 400000,
            'vector_size': 300
        },
        'glove-twitter-25': {
            'name': 'glove-twitter-25',
            'description': 'GloVe 25D vectors trained on Twitter (2B tweets)',
            'size_mb': 104,
            'vocab_size': 1193514,
            'vector_size': 25
        },
        'glove-twitter-50': {
            'name': 'glove-twitter-50',
            'description': 'GloVe 50D vectors trained on Twitter (2B tweets)',
            'size_mb': 205,
            'vocab_size': 1193514,
            'vector_size': 50
        },
        'glove-twitter-100': {
            'name': 'glove-twitter-100',
            'description': 'GloVe 100D vectors trained on Twitter (2B tweets)',
            'size_mb': 405,
            'vocab_size': 1193514,
            'vector_size': 100
        },
        'glove-twitter-200': {
            'name': 'glove-twitter-200',
            'description': 'GloVe 200D vectors trained on Twitter (2B tweets)',
            'size_mb': 805,
            'vocab_size': 1193514,
            'vector_size': 200
        },
        'word2vec-google-news-300': {
            'name': 'word2vec-google-news-300',
            'description': 'Word2Vec 300D vectors trained on Google News (3B words)',
            'size_mb': 1662,
            'vocab_size': 3000000,
            'vector_size': 300
        },
        'fasttext-wiki-news-subwords-300': {
            'name': 'fasttext-wiki-news-subwords-300',
            'description': 'FastText 300D vectors with subword info (2M vocab)',
            'size_mb': 958,
            'vocab_size': 999999,
            'vector_size': 300
        }
    }

    @classmethod
    def get_model_names(cls) -> List[str]:
        """Get list of available model names"""
        return list(cls.AVAILABLE_MODELS.keys())

    @classmethod
    def get_model_info(cls, model_name: str) -> Dict[str, Any]:
        """Get information for a specific model"""
        return cls.AVAILABLE_MODELS.get(model_name, {})

    @classmethod
    def is_valid_model(cls, model_name: str) -> bool:
        """Check if a model name is valid"""
        return model_name in cls.AVAILABLE_MODELS

    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """Get a summary of current configuration"""
        return {
            'server': {
                'host': cls.HOST,
                'port': cls.PORT,
                'debug': cls.DEBUG
            },
            'models': {
                'default_model': cls.DEFAULT_MODEL,
                'preload_default': cls.PRELOAD_DEFAULT_MODEL,
                'cache_size_limit': cls.MODEL_CACHE_SIZE_LIMIT,
                'available_count': len(cls.AVAILABLE_MODELS)
            },
            'validation': {
                'min_word_length': cls.MIN_WORD_LENGTH,
                'max_word_length': cls.MAX_WORD_LENGTH,
                'max_batch_size': cls.MAX_BATCH_SIZE
            },
            'performance': {
                'request_timeout': cls.REQUEST_TIMEOUT,
                'max_concurrent_requests': cls.MAX_CONCURRENT_REQUESTS,
                'max_memory_mb': cls.MAX_MEMORY_USAGE_MB
            }
        }


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    ENABLE_ACCESS_LOGS = True
    ENABLE_REQUEST_LOGGING = True
    PRELOAD_DEFAULT_MODEL = False  # Faster startup in dev
    MODEL_CACHE_SIZE_LIMIT = 2  # Limit memory usage in dev


class ProductionConfig(Config):
    """
    Production configuration
    """
    DEBUG = False
    LOG_LEVEL = 'INFO'
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production
    PRELOAD_DEFAULT_MODEL = True  # Faster first requests
    MODEL_CACHE_SIZE_LIMIT = 5

    # Enhanced security in production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')

    # Performance optimizations
    MAX_CONCURRENT_REQUESTS = 200
    ENABLE_RATE_LIMITING = True

    # Memory management
    AUTO_UNLOAD_UNUSED_MODELS = True

    @classmethod
    def validate_production_config(cls):
        """Validate that production configuration is properly set"""
        issues = []

        if not cls.SECRET_KEY or cls.SECRET_KEY == Config.SECRET_KEY:
            issues.append("SECRET_KEY must be set to a secure value in production")

        if not cls.CORS_ORIGINS or cls.CORS_ORIGINS == ['']:
            issues.append("CORS_ORIGINS must be properly configured in production")

        if cls.DEBUG:
            issues.append("DEBUG should be False in production")

        return issues


class TestingConfig(Config):
    """
    Testing configuration
    """
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    PRELOAD_DEFAULT_MODEL = False  # Faster test startup
    MODEL_CACHE_SIZE_LIMIT = 1  # Minimal memory usage
    MIN_WORD_LENGTH = 1  # Relaxed validation for tests
    MAX_BATCH_SIZE = 10  # Small batches for tests
    REQUEST_TIMEOUT = 30  # Shorter timeout for tests


class ConfigManager:
    """
    Configuration manager to handle different environments
    """

    CONFIG_MAPPING = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
        'dev': DevelopmentConfig,
        'prod': ProductionConfig,
        'test': TestingConfig
    }

    @classmethod
    def get_config(cls, env_name: str = None) -> Config:
        """
        Get configuration class based on environment

        Args:
            env_name: Environment name (development, production, testing)

        Returns:
            Configuration class
        """
        if env_name is None:
            env_name = os.environ.get('FLASK_ENV', 'development').lower()

        config_class = cls.CONFIG_MAPPING.get(env_name, DevelopmentConfig)

        # Validate production config if needed
        if config_class == ProductionConfig:
            issues = ProductionConfig.validate_production_config()
            if issues:
                print("WARNING: Production configuration issues detected:")
                for issue in issues:
                    print(f"  - {issue}")

        return config_class

    @classmethod
    def print_config_info(cls, config: Config):
        """Print configuration information"""
        print(f"=== Word2Vec ML Service Configuration ===")
        print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
        print(f"Debug Mode: {config.DEBUG}")
        print(f"Server: {config.HOST}:{config.PORT}")
        print(f"Default Model: {config.DEFAULT_MODEL}")
        print(f"Preload Default Model: {config.PRELOAD_DEFAULT_MODEL}")
        print(f"Max Models in Cache: {config.MODEL_CACHE_SIZE_LIMIT}")
        print(f"CORS Origins: {', '.join(config.CORS_ORIGINS)}")
        print(f"Log Level: {config.LOG_LEVEL}")
        print(f"Available Models: {len(config.AVAILABLE_MODELS)}")
        if config.ENABLE_RATE_LIMITING:
            print(f"Rate Limiting: {config.RATE_LIMIT_PER_MINUTE} requests/minute")
        print("=" * 45)


# Convenience function to get current config
def get_config() -> Config:
    """Get the current configuration"""
    return ConfigManager.get_config()


# Environment-specific settings that can be imported
def load_config_from_env():
    """
    Load additional configuration from environment variables
    This can be used to override specific settings at runtime
    """
    env_overrides = {}

    # Check for any custom model configurations
    for key, value in os.environ.items():
        if key.startswith('WORD2VEC_'):
            config_key = key[9:]  # Remove 'WORD2VEC_' prefix
            env_overrides[config_key] = value

    return env_overrides


# Default configuration export
config = get_config()
