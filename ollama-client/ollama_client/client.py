"""Main OllamaClient class for interacting with Ollama server."""
import json
from typing import Dict, List, Union, Iterator, Optional
import requests
from requests.exceptions import ConnectionError, Timeout as RequestsTimeout

from .exceptions import (
    OllamaConnectionError,
    OllamaAPIError,
    OllamaTimeoutError,
    OllamaModelNotFoundError,
)


class OllamaClient:
    """Client for interacting with Ollama server API."""
    
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 30):
        """
        Initialize the Ollama client.
        
        Args:
            base_url: Base URL of the Ollama server (default: http://localhost:11434)
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        stream: bool = False
    ) -> Union[requests.Response, Iterator[Dict]]:
        """
        Make an HTTP request to the Ollama API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request payload
            stream: Whether to stream the response
            
        Returns:
            Response object or iterator of response chunks
            
        Raises:
            OllamaConnectionError: If connection fails
            OllamaTimeoutError: If request times out
            OllamaAPIError: If API returns an error
        """
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    stream=stream
                )
            else:  # POST
                response = self.session.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=self.timeout,
                    stream=stream
                )
            
            # Check for HTTP errors
            if response.status_code != 200:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = error_data.get('error', f'HTTP {response.status_code} error')
                
                # Check if it's a model not found error
                if response.status_code == 404 or 'model' in error_msg.lower():
                    raise OllamaModelNotFoundError(error_msg, status_code=response.status_code)
                
                raise OllamaAPIError(error_msg, status_code=response.status_code)
            
            if stream:
                return self._stream_response(response)
            
            return response.json()
            
        except ConnectionError as e:
            raise OllamaConnectionError(f"Failed to connect to Ollama server at {self.base_url}: {str(e)}")
        except RequestsTimeout as e:
            raise OllamaTimeoutError(f"Request to Ollama server timed out after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise OllamaConnectionError(f"Request failed: {str(e)}")
    
    def _stream_response(self, response: requests.Response) -> Iterator[Dict]:
        """Parse streaming JSON response."""
        for line in response.iter_lines():
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    
    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        stream: bool = False,
        **kwargs
    ) -> Union[Dict, Iterator[Dict]]:
        """
        Send a chat request to the Ollama API.
        
        Args:
            model: Model name (e.g., 'llama3.2:3b')
            messages: List of message dictionaries with 'role' and 'content' keys
            stream: Whether to stream the response
            **kwargs: Additional parameters (temperature, top_p, top_k, etc.)
            
        Returns:
            Complete response dictionary or iterator of response chunks
            
        Example:
            >>> client = OllamaClient()
            >>> messages = [{"role": "user", "content": "Hello!"}]
            >>> response = client.chat("llama3.2:3b", messages)
            >>> print(response["message"]["content"])
        """
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        
        return self._make_request("POST", "/api/chat", data=payload, stream=stream)
    
    def generate(
        self,
        model: str,
        prompt: str,
        stream: bool = False,
        **kwargs
    ) -> Union[Dict, Iterator[Dict]]:
        """
        Send a generate request to the Ollama API.
        
        Args:
            model: Model name (e.g., 'llama3.2:3b')
            prompt: Input prompt
            stream: Whether to stream the response
            **kwargs: Additional parameters (temperature, top_p, top_k, etc.)
            
        Returns:
            Complete response dictionary or iterator of response chunks
            
        Example:
            >>> client = OllamaClient()
            >>> response = client.generate("llama3.2:3b", "Tell me a joke")
            >>> print(response["response"])
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            **kwargs
        }
        
        return self._make_request("POST", "/api/generate", data=payload, stream=stream)
    
    def list_models(self) -> List[Dict]:
        """
        List all available models on the Ollama server.
        
        Returns:
            List of model dictionaries
            
        Example:
            >>> client = OllamaClient()
            >>> models = client.list_models()
            >>> for model in models:
            ...     print(model["name"])
        """
        response = self._make_request("GET", "/api/tags")
        return response.get("models", [])
    
    def check_health(self) -> bool:
        """
        Check if the Ollama server is accessible and healthy.
        
        Returns:
            True if server is healthy, False otherwise
        """
        try:
            self._make_request("GET", "/api/tags")
            return True
        except (OllamaConnectionError, OllamaAPIError, OllamaTimeoutError):
            return False

