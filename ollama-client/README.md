# Ollama Python Client

A Python client library for interacting with the Ollama server. This library provides a simple and intuitive interface to send messages and receive responses from Ollama models.

## Features

- ✅ **Chat API** - Multi-turn conversations with context management
- ✅ **Generate API** - Simple prompt-to-response generation
- ✅ **Streaming Support** - Real-time streaming responses
- ✅ **Error Handling** - Comprehensive error handling with custom exceptions
- ✅ **Type Hints** - Full type support for better IDE experience
- ✅ **Easy Installation** - Simple setup with `uv`

## Installation

### Prerequisites

- Python 3.7 or higher
- `uv` package manager
- Running Ollama server (default: `http://localhost:11434`)

### Install the Library

From within the `ollama-client` directory:

```bash
uv sync
```

This will install the package and its dependencies automatically.

## Quick Start

### Basic Chat Example

```python
from ollama_client import OllamaClient

# Initialize the client
client = OllamaClient(base_url="http://localhost:11434")

# Send a chat message
messages = [
    {"role": "user", "content": "Explain quantum computing in simple terms"}
]

response = client.chat(model="llama3.2:3b", messages=messages)
print(response["message"]["content"])
```

### Simple Generation Example

```python
from ollama_client import OllamaClient

client = OllamaClient()

response = client.generate(
    model="llama3.2:3b",
    prompt="Write a haiku about programming"
)

print(response["response"])
```

### Streaming Example

```python
from ollama_client import OllamaClient

client = OllamaClient()

messages = [{"role": "user", "content": "Tell me a story"}]

for chunk in client.chat(model="llama3.2:3b", messages=messages, stream=True):
    if "message" in chunk and "content" in chunk["message"]:
        print(chunk["message"]["content"], end="", flush=True)
```

## API Reference

### OllamaClient

Main client class for interacting with the Ollama server.

#### Constructor

```python
OllamaClient(base_url: str = "http://localhost:11434", timeout: int = 30)
```

**Parameters:**
- `base_url` (str): Base URL of the Ollama server (default: `http://localhost:11434`)
- `timeout` (int): Request timeout in seconds (default: 30)

#### Methods

##### `chat(model, messages, stream=False, **kwargs)`

Send a chat request to the Ollama API.

**Parameters:**
- `model` (str): Model name (e.g., `'llama3.2:3b'`)
- `messages` (List[Dict]): List of message dictionaries with `role` and `content` keys
- `stream` (bool): Whether to stream the response (default: `False`)
- `**kwargs`: Additional parameters:
  - `temperature` (float): Controls randomness (0.0 to 1.0)
  - `top_p` (float): Nucleus sampling parameter
  - `top_k` (int): Top-k sampling
  - `num_predict` (int): Maximum tokens to generate
  - `format` (str): Response format (e.g., `"json"` for JSON mode)

**Returns:**
- If `stream=False`: Complete response dictionary
- If `stream=True`: Iterator of response chunks

**Example:**
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]

response = client.chat(
    model="llama3.2:3b",
    messages=messages,
    temperature=0.7
)
```

##### `generate(model, prompt, stream=False, **kwargs)`

Send a generate request to the Ollama API.

**Parameters:**
- `model` (str): Model name (e.g., `'llama3.2:3b'`)
- `prompt` (str): Input prompt
- `stream` (bool): Whether to stream the response (default: `False`)
- `**kwargs`: Additional parameters (same as `chat`)

**Returns:**
- If `stream=False`: Complete response dictionary
- If `stream=True`: Iterator of response chunks

**Example:**
```python
response = client.generate(
    model="llama3.2:3b",
    prompt="Write a Python function to reverse a string",
    temperature=0.5
)
```

##### `list_models()`

List all available models on the Ollama server.

**Returns:**
- `List[Dict]`: List of model dictionaries

**Example:**
```python
models = client.list_models()
for model in models:
    print(f"{model['name']}: {model.get('size', 0)} bytes")
```

##### `check_health()`

Check if the Ollama server is accessible and healthy.

**Returns:**
- `bool`: `True` if server is healthy, `False` otherwise

**Example:**
```python
if client.check_health():
    print("Server is healthy!")
else:
    print("Server is not accessible")
```

## Usage Examples

### Multi-turn Conversation

```python
from ollama_client import OllamaClient

client = OllamaClient()

# Start conversation
messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "How do I reverse a list in Python?"}
]

# First turn
response = client.chat(model="llama3.2:3b", messages=messages)
assistant_response = response["message"]["content"]
print(f"Assistant: {assistant_response}")

# Add to history
messages.append({"role": "assistant", "content": assistant_response})

# Second turn
messages.append({"role": "user", "content": "Can you show me an example?"})
response = client.chat(model="llama3.2:3b", messages=messages)
print(f"Assistant: {response['message']['content']}")
```

### Streaming Chat with Progress

```python
from ollama_client import OllamaClient

client = OllamaClient()

messages = [{"role": "user", "content": "Explain machine learning"}]

print("Response: ", end="", flush=True)
for chunk in client.chat(model="llama3.2:3b", messages=messages, stream=True):
    if "message" in chunk and "content" in chunk["message"]:
        print(chunk["message"]["content"], end="", flush=True)
    if chunk.get("done", False):
        break
print("\n[Complete]")
```

### Using Configuration Options

```python
from ollama_client import OllamaClient

client = OllamaClient()

response = client.chat(
    model="llama3.2:3b",
    messages=[{"role": "user", "content": "Write a creative story"}],
    temperature=0.9,      # More creative
    top_p=0.9,            # Nucleus sampling
    num_predict=500        # Limit response length
)
```

## Error Handling

The library provides custom exceptions for different error scenarios:

### Exception Types

- `OllamaError`: Base exception for all Ollama-related errors
- `OllamaConnectionError`: Network or connection issues
- `OllamaAPIError`: API errors (4xx, 5xx responses)
- `OllamaTimeoutError`: Request timeout
- `OllamaModelNotFoundError`: Model doesn't exist

### Example Error Handling

```python
from ollama_client import OllamaClient
from ollama_client.exceptions import (
    OllamaConnectionError,
    OllamaAPIError,
    OllamaTimeoutError,
    OllamaModelNotFoundError,
)

client = OllamaClient()

try:
    response = client.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": "Hello"}]
    )
except OllamaConnectionError as e:
    print(f"Connection failed: {e}")
except OllamaTimeoutError as e:
    print(f"Request timed out: {e}")
except OllamaModelNotFoundError as e:
    print(f"Model not found: {e}")
except OllamaAPIError as e:
    print(f"API error ({e.status_code}): {e}")
```

## Configuration Options

The Ollama API supports various configuration parameters that can be passed via `**kwargs`:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `temperature` | float | Controls randomness (0.0-1.0) | Model default |
| `top_p` | float | Nucleus sampling | Model default |
| `top_k` | int | Top-k sampling | Model default |
| `num_predict` | int | Maximum tokens to generate | Model default |
| `format` | str | Response format (e.g., "json") | None |
| `context` | List[int] | Custom context | None |

## Troubleshooting

### Connection Errors

**Problem:** `OllamaConnectionError: Failed to connect to Ollama server`

**Solutions:**
1. Ensure the Ollama server is running: `docker-compose up` (if using Docker)
2. Check the base URL matches your server configuration
3. Verify the server is accessible: `curl http://localhost:11434/api/tags`

### Model Not Found

**Problem:** `OllamaModelNotFoundError`

**Solutions:**
1. Check available models: `client.list_models()`
2. Pull the required model: `ollama pull llama3.2:3b`
3. Verify the model name is correct

### Timeout Errors

**Problem:** `OllamaTimeoutError: Request timed out`

**Solutions:**
1. Increase the timeout: `OllamaClient(timeout=60)`
2. Check server performance and model size
3. Use a smaller/faster model

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'ollama_client'`

**Solutions:**
1. Ensure the package is installed: `uv sync`
2. Check you're in the correct Python environment
3. Verify the package is in your Python path

## Examples

See the `examples/` directory for more detailed usage examples:

- `simple_chat.py` - Basic chat interaction
- `generate_example.py` - Simple text generation
- `streaming_example.py` - Streaming responses
- `multi_turn_conversation.py` - Conversation with context

Run examples:
```bash
cd examples
python simple_chat.py
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or using unittest:

```bash
python -m unittest tests.test_client
```

## License

This library is provided as-is for use with Ollama servers.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## See Also

- [Ollama Documentation](https://docs.ollama.com)
- [Ollama API Reference](https://docs.ollama.com/api)

