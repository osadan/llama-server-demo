"""Custom exceptions for the Ollama client library."""


class OllamaError(Exception):
    """Base exception for all Ollama-related errors."""
    pass


class OllamaConnectionError(OllamaError):
    """Raised when there's a network or connection issue."""
    pass


class OllamaAPIError(OllamaError):
    """Raised when the Ollama API returns an error response."""
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code


class OllamaTimeoutError(OllamaError):
    """Raised when a request times out."""
    pass


class OllamaModelNotFoundError(OllamaAPIError):
    """Raised when a requested model doesn't exist."""
    pass

