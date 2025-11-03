"""Ollama Python Client Library."""

from .client import OllamaClient
from .exceptions import (
    OllamaError,
    OllamaConnectionError,
    OllamaAPIError,
    OllamaTimeoutError,
    OllamaModelNotFoundError,
)

__version__ = "0.1.0"

__all__ = [
    "OllamaClient",
    "OllamaError",
    "OllamaConnectionError",
    "OllamaAPIError",
    "OllamaTimeoutError",
    "OllamaModelNotFoundError",
]

