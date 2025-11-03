# Plan: Python Ollama Client Library

## Overview
Create a Python library that can be imported into other modules to connect to the Ollama server, send messages, and receive responses. The library will be located in a separate directory outside of the docker-compose setup.

## Project Structure

```
ollama-client/                    # New directory (separate from ollama-server)
├── ollama_client/                # Main package directory
│   ├── __init__.py              # Package initialization, exports main classes
│   ├── client.py                # Main OllamaClient class
│   └── exceptions.py            # Custom exceptions for error handling
├── examples/                    # Example usage scripts
│   ├── simple_chat.py          # Basic chat example
│   ├── generate_example.py     # Simple generation example
│   └── streaming_example.py    # Streaming response example
├── tests/                       # Unit tests (optional but recommended)
│   ├── __init__.py
│   └── test_client.py
├── README.md                    # Documentation
├── pyproject.toml              # Package configuration (modern Python packaging)
└── requirements.txt             # Python dependencies (optional, for reference)
```

## Library Features

### Core Functionality
1. **Connection Management**
   - Configurable base URL (default: `http://localhost:11434`)
   - Connection health checks
   - Timeout configuration

2. **Chat API** (`/api/chat`)
   - Send multi-turn conversations
   - Maintain conversation context
   - Support for system messages, user messages, assistant messages
   - Streaming and non-streaming modes

3. **Generate API** (`/api/generate`)
   - Simple prompt-to-response generation
   - Single-shot completions
   - Streaming and non-streaming modes

4. **Error Handling**
   - Custom exceptions for different error types
   - Network error handling
   - HTTP error handling (4xx, 5xx)
   - Connection timeout handling

5. **Additional Utilities**
   - List available models
   - Check server status
   - Pull models (optional utility)

## Implementation Details

### Dependencies
- `requests` - HTTP client for API calls
- `typing` - Type hints (Python 3.5+)

### Core Classes

#### `OllamaClient` (in `client.py`)
Main class for interacting with Ollama server.

**Methods:**
- `__init__(base_url: str = "http://localhost:11434", timeout: int = 30)`
- `chat(model: str, messages: List[Dict], stream: bool = False, **kwargs) -> Union[Dict, Iterator[Dict]]`
- `generate(model: str, prompt: str, stream: bool = False, **kwargs) -> Union[Dict, Iterator[Dict]]`
- `list_models() -> List[Dict]`
- `check_health() -> bool`

**Chat Message Format:**
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I'm doing well, thank you!"},
    {"role": "user", "content": "What's the weather like?"}
]
```

#### Custom Exceptions (in `exceptions.py`)
- `OllamaError` - Base exception
- `OllamaConnectionError` - Network/connection issues
- `OllamaAPIError` - API errors (4xx, 5xx)
- `OllamaTimeoutError` - Request timeout
- `OllamaModelNotFoundError` - Model doesn't exist

### API Endpoints

1. **Chat Endpoint**: `POST /api/chat`
   - Request body: `{"model": str, "messages": List[Dict], "stream": bool, ...}`
   - Response: `{"model": str, "message": Dict, "done": bool, ...}`

2. **Generate Endpoint**: `POST /api/generate`
   - Request body: `{"model": str, "prompt": str, "stream": bool, ...}`
   - Response: `{"model": str, "response": str, "done": bool, ...}`

3. **List Models**: `GET /api/tags`
   - Response: `{"models": List[Dict]}`

4. **Health Check**: `GET /api/tags` (lightweight endpoint)

## Usage Examples

### Basic Chat (Non-streaming)
```python
from ollama_client import OllamaClient

client = OllamaClient(base_url="http://localhost:11434")

messages = [
    {"role": "user", "content": "Explain quantum computing in simple terms"}
]

response = client.chat(model="llama3.2:3b", messages=messages)
print(response["message"]["content"])
```

### Streaming Chat
```python
from ollama_client import OllamaClient

client = OllamaClient(base_url="http://localhost:11434")

messages = [{"role": "user", "content": "Tell me a story"}]

for chunk in client.chat(model="llama3.2:3b", messages=messages, stream=True):
    if "message" in chunk and "content" in chunk["message"]:
        print(chunk["message"]["content"], end="", flush=True)
```

### Simple Generation
```python
from ollama_client import OllamaClient

client = OllamaClient()

response = client.generate(
    model="llama3.2:3b",
    prompt="Write a haiku about programming"
)
print(response["response"])
```

### Multi-turn Conversation
```python
from ollama_client import OllamaClient

client = OllamaClient()

messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "How do I reverse a list in Python?"}
]

# First turn
response = client.chat(model="llama3.2:3b", messages=messages)
assistant_response = response["message"]["content"]

# Add assistant response to history
messages.append({"role": "assistant", "content": assistant_response})

# Second turn
messages.append({"role": "user", "content": "Can you show me an example?"})
response = client.chat(model="llama3.2:3b", messages=messages)
print(response["message"]["content"])
```

## Error Handling Strategy

1. **Network Errors**: Catch `requests.exceptions.ConnectionError`, `requests.exceptions.Timeout`
2. **HTTP Errors**: Check `response.status_code`, raise appropriate custom exceptions
3. **Invalid Responses**: Validate JSON structure, required fields
4. **Model Not Found**: Check API error messages for model-related errors

## Configuration Options

The client should support common Ollama API parameters:
- `temperature` - Controls randomness (0.0 to 1.0)
- `top_p` - Nucleus sampling parameter
- `top_k` - Top-k sampling
- `max_tokens` / `num_predict` - Maximum tokens to generate
- `context` - Custom context (for advanced use)
- `format` - Response format (JSON mode, etc.)

## Installation as Package

The library should be installable using `uv` directly. From within the directory:
```bash
cd /path/to/ollama-client
uv sync
```

This will install the package in editable mode automatically when using `pyproject.toml`.

The package should use `pyproject.toml` for configuration:
```toml
[project]
name = "ollama-client"
version = "0.1.0"
description = "Python client library for Ollama server"
requires-python = ">=3.7"
dependencies = [
    "requests>=2.31.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Testing Strategy

1. **Unit Tests**: Mock HTTP requests using `unittest.mock` or `responses` library
2. **Integration Tests**: Require running Ollama server (can be skipped in CI)
3. **Test Cases**:
   - Successful chat requests
   - Successful generate requests
   - Streaming responses
   - Error handling (connection errors, HTTP errors)
   - Invalid model names
   - Timeout scenarios

## Documentation

The `README.md` should include:
- Installation instructions
- Quick start guide
- API reference
- Usage examples (all patterns)
- Error handling guide
- Configuration options
- Troubleshooting section

## Implementation Priority

1. **Phase 1: Core Functionality**
   - Basic `OllamaClient` class
   - `chat()` method (non-streaming)
   - `generate()` method (non-streaming)
   - Basic error handling

2. **Phase 2: Enhanced Features**
   - Streaming support
   - Additional utility methods (`list_models`, `check_health`)
   - Comprehensive error handling

3. **Phase 3: Polish**
   - Package setup (`pyproject.toml`)
   - Documentation
   - Examples
   - Tests

## Directory Location

The library should be created in a directory **outside** of the `ollama-server` directory, for example:
- `/home/ohad/data/Projects/ollama-client/` (sibling to ollama-server)
- Or any other directory the user prefers

## Advantages of This Approach

1. **Separation of Concerns**: Client library is independent of server setup
2. **Reusability**: Can be imported into any Python project
3. **Maintainability**: Clear structure, easy to extend
4. **Flexibility**: Supports both chat and generate APIs
5. **Robustness**: Proper error handling and type hints
6. **Usability**: Simple API, clear examples

## Next Steps

1. Create the directory structure
2. Implement core `OllamaClient` class
3. Add error handling and exceptions
4. Implement streaming support
5. Add utility methods
6. Create examples and documentation
7. Set up package installation
8. Add tests (optional but recommended)

