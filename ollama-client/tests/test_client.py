"""Unit tests for OllamaClient."""
import unittest
from unittest.mock import Mock, patch, MagicMock
from ollama_client import OllamaClient
from ollama_client.exceptions import (
    OllamaConnectionError,
    OllamaAPIError,
    OllamaTimeoutError,
    OllamaModelNotFoundError,
)


class TestOllamaClient(unittest.TestCase):
    """Test cases for OllamaClient."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = OllamaClient(base_url="http://localhost:11434", timeout=10)
    
    @patch('ollama_client.client.requests.Session.post')
    def test_chat_success(self, mock_post):
        """Test successful chat request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "model": "llama3.2:3b",
            "message": {"role": "assistant", "content": "Hello! How can I help you?"},
            "done": True
        }
        mock_post.return_value = mock_response
        
        messages = [{"role": "user", "content": "Hello"}]
        response = self.client.chat("llama3.2:3b", messages)
        
        self.assertEqual(response["message"]["content"], "Hello! How can I help you?")
        mock_post.assert_called_once()
    
    @patch('ollama_client.client.requests.Session.post')
    def test_generate_success(self, mock_post):
        """Test successful generate request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "model": "llama3.2:3b",
            "response": "This is a test response",
            "done": True
        }
        mock_post.return_value = mock_response
        
        response = self.client.generate("llama3.2:3b", "Test prompt")
        
        self.assertEqual(response["response"], "This is a test response")
    
    @patch('ollama_client.client.requests.Session.post')
    def test_connection_error(self, mock_post):
        """Test connection error handling."""
        mock_post.side_effect = ConnectionError("Connection failed")
        
        messages = [{"role": "user", "content": "Hello"}]
        
        with self.assertRaises(OllamaConnectionError):
            self.client.chat("llama3.2:3b", messages)
    
    @patch('ollama_client.client.requests.Session.post')
    def test_timeout_error(self, mock_post):
        """Test timeout error handling."""
        from requests.exceptions import Timeout
        mock_post.side_effect = Timeout("Request timed out")
        
        messages = [{"role": "user", "content": "Hello"}]
        
        with self.assertRaises(OllamaTimeoutError):
            self.client.chat("llama3.2:3b", messages)
    
    @patch('ollama_client.client.requests.Session.post')
    def test_api_error(self, mock_post):
        """Test API error handling."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal server error"}
        mock_response.headers = {"content-type": "application/json"}
        mock_post.return_value = mock_response
        
        messages = [{"role": "user", "content": "Hello"}]
        
        with self.assertRaises(OllamaAPIError) as context:
            self.client.chat("llama3.2:3b", messages)
        
        self.assertEqual(context.exception.status_code, 500)
    
    @patch('ollama_client.client.requests.Session.get')
    def test_list_models(self, mock_get):
        """Test list models functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [
                {"name": "llama3.2:3b", "size": 2000000000},
                {"name": "phi3:mini", "size": 2300000000}
            ]
        }
        mock_get.return_value = mock_response
        
        models = self.client.list_models()
        
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0]["name"], "llama3.2:3b")
    
    @patch('ollama_client.client.requests.Session.get')
    def test_check_health(self, mock_get):
        """Test health check functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"models": []}
        mock_get.return_value = mock_response
        
        self.assertTrue(self.client.check_health())


if __name__ == "__main__":
    unittest.main()

