"""
Custom exceptions for the Word2Vec ML service
"""

class Word2VecServiceError(Exception):
    """
    Base exception class for all Word2Vec service errors
    """

    def __init__(self, message: str, error_code: str = None, details: dict = None):
        """
        Initialize the exception

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code for API responses
            details: Additional details about the error
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__.lower().replace('error', '')
        self.details = details or {}

    def to_dict(self) -> dict:
        """
        Convert exception to dictionary for JSON responses

        Returns:
            Dict representation of the exception
        """
        result = {
            'error_type': self.__class__.__name__,
            'error_code': self.error_code,
            'message': self.message
        }

        if self.details:
            result['details'] = self.details

        return result


class ValidationError(Word2VecServiceError):
    """
    Exception raised for input validation errors

    This includes:
    - Invalid word format (empty, too long, contains invalid characters)
    - Invalid model names
    - Missing required parameters
    - Invalid parameter types or values
    """

    def __init__(self, message: str, field: str = None, value: str = None, **kwargs):
        """
        Initialize validation error

        Args:
            message: Error message
            field: Name of the field that failed validation
            value: Value that failed validation
        """
        super().__init__(message, error_code='validation_error', **kwargs)

        if field:
            self.details['field'] = field
        if value is not None:
            self.details['invalid_value'] = str(value)


class ModelError(Word2VecServiceError):
    """
    Exception raised for model-related errors

    This includes:
    - Model loading failures
    - Model not found/unavailable
    - Model compatibility issues
    - Gensim operation failures
    - Network errors during model download
    """

    def __init__(self, message: str, model_name: str = None, operation: str = None, **kwargs):
        """
        Initialize model error

        Args:
            message: Error message
            model_name: Name of the model that caused the error
            operation: Operation that was being performed when error occurred
        """
        super().__init__(message, error_code='model_error', **kwargs)

        if model_name:
            self.details['model_name'] = model_name
        if operation:
            self.details['operation'] = operation


class WordNotFoundError(ValidationError):
    """
    Exception raised when a word is not found in the model vocabulary
    """

    def __init__(self, word: str, model_name: str = None, suggestions: list = None):
        """
        Initialize word not found error

        Args:
            word: The word that was not found
            model_name: Name of the model where word was not found
            suggestions: List of suggested alternative words
        """
        message = f"Word '{word}' not found in vocabulary"
        if model_name:
            message += f" of model '{model_name}'"

        super().__init__(
            message,
            field='word',
            value=word,
            error_code='word_not_found'
        )

        if model_name:
            self.details['model_name'] = model_name
        if suggestions:
            self.details['suggestions'] = suggestions


class ModelNotFoundError(ModelError):
    """
    Exception raised when a requested model is not available
    """

    def __init__(self, model_name: str, available_models: list = None):
        """
        Initialize model not found error

        Args:
            model_name: Name of the model that was not found
            available_models: List of available model names
        """
        message = f"Model '{model_name}' is not available"

        super().__init__(
            message,
            model_name=model_name,
            error_code='model_not_found'
        )

        if available_models:
            self.details['available_models'] = available_models


class ModelLoadingError(ModelError):
    """
    Exception raised when a model fails to load
    """

    def __init__(self, model_name: str, reason: str = None, load_time: float = None):
        """
        Initialize model loading error

        Args:
            model_name: Name of the model that failed to load
            reason: Specific reason for the failure
            load_time: Time spent trying to load the model
        """
        message = f"Failed to load model '{model_name}'"
        if reason:
            message += f": {reason}"

        super().__init__(
            message,
            model_name=model_name,
            operation='load',
            error_code='model_loading_error'
        )

        if load_time:
            self.details['load_time_seconds'] = load_time


class NetworkError(ModelError):
    """
    Exception raised for network-related errors during model operations
    """

    def __init__(self, message: str, model_name: str = None, url: str = None):
        """
        Initialize network error

        Args:
            message: Error message
            model_name: Model being downloaded when error occurred
            url: URL that failed to load
        """
        super().__init__(
            message,
            model_name=model_name,
            operation='download',
            error_code='network_error'
        )

        if url:
            self.details['failed_url'] = url


class ServiceUnavailableError(Word2VecServiceError):
    """
    Exception raised when the service is temporarily unavailable
    """

    def __init__(self, message: str = "Service is temporarily unavailable", retry_after: int = None):
        """
        Initialize service unavailable error

        Args:
            message: Error message
            retry_after: Suggested retry time in seconds
        """
        super().__init__(message, error_code='service_unavailable')

        if retry_after:
            self.details['retry_after_seconds'] = retry_after


class ConfigurationError(Word2VecServiceError):
    """
    Exception raised for configuration-related errors
    """

    def __init__(self, message: str, config_key: str = None, config_value: str = None):
        """
        Initialize configuration error

        Args:
            message: Error message
            config_key: Configuration key that caused the error
            config_value: Invalid configuration value
        """
        super().__init__(message, error_code='configuration_error')

        if config_key:
            self.details['config_key'] = config_key
        if config_value is not None:
            self.details['config_value'] = str(config_value)


class RateLimitError(Word2VecServiceError):
    """
    Exception raised when rate limits are exceeded
    """

    def __init__(self, message: str = "Rate limit exceeded", limit: int = None, reset_time: int = None):
        """
        Initialize rate limit error

        Args:
            message: Error message
            limit: Request limit that was exceeded
            reset_time: When the rate limit resets (Unix timestamp)
        """
        super().__init__(message, error_code='rate_limit_exceeded')

        if limit:
            self.details['limit'] = limit
        if reset_time:
            self.details['reset_time'] = reset_time


class MemoryError(Word2VecServiceError):
    """
    Exception raised when memory limits are exceeded
    """

    def __init__(self, message: str = "Insufficient memory", operation: str = None, required_mb: float = None):
        """
        Initialize memory error

        Args:
            message: Error message
            operation: Operation that caused memory issue
            required_mb: Amount of memory required in MB
        """
        super().__init__(message, error_code='memory_error')

        if operation:
            self.details['operation'] = operation
        if required_mb:
            self.details['required_memory_mb'] = required_mb


class BatchProcessingError(Word2VecServiceError):
    """
    Exception raised for batch processing errors
    """

    def __init__(self, message: str, total_items: int = None, failed_items: int = None, partial_results: list = None):
        """
        Initialize batch processing error

        Args:
            message: Error message
            total_items: Total number of items in batch
            failed_items: Number of items that failed
            partial_results: Any partial results that were computed
        """
        super().__init__(message, error_code='batch_processing_error')

        if total_items is not None:
            self.details['total_items'] = total_items
        if failed_items is not None:
            self.details['failed_items'] = failed_items
        if partial_results:
            self.details['partial_results'] = partial_results


# Convenience functions for common error scenarios

def raise_word_not_found(word: str, model_name: str = None, suggestions: list = None):
    """
    Convenience function to raise WordNotFoundError
    """
    raise WordNotFoundError(word, model_name, suggestions)


def raise_model_not_found(model_name: str, available_models: list = None):
    """
    Convenience function to raise ModelNotFoundError
    """
    raise ModelNotFoundError(model_name, available_models)


def raise_validation_error(message: str, field: str = None, value: str = None):
    """
    Convenience function to raise ValidationError
    """
    raise ValidationError(message, field, value)


def raise_model_error(message: str, model_name: str = None, operation: str = None):
    """
    Convenience function to raise ModelError
    """
    raise ModelError(message, model_name, operation)


# Exception mapping for HTTP status codes
EXCEPTION_HTTP_STATUS_MAP = {
    ValidationError: 400,
    WordNotFoundError: 400,
    ModelNotFoundError: 404,
    ModelLoadingError: 500,
    ModelError: 500,
    NetworkError: 502,
    ServiceUnavailableError: 503,
    ConfigurationError: 500,
    RateLimitError: 429,
    MemoryError: 507,  # Insufficient Storage
    BatchProcessingError: 500,
    Word2VecServiceError: 500  # Default for base exception
}


def get_http_status_for_exception(exception: Exception) -> int:
    """
    Get the appropriate HTTP status code for an exception

    Args:
        exception: The exception instance

    Returns:
        HTTP status code
    """
    exception_type = type(exception)
    return EXCEPTION_HTTP_STATUS_MAP.get(exception_type, 500)
