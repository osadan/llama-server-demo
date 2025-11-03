"""Simple chat example using OllamaClient."""
from ollama_client import OllamaClient

def main():
    # Initialize the client
    client = OllamaClient(base_url="http://localhost:11434")
    
    # Define the messages
    messages = [
        {"role": "user", "content": "Explain quantum computing in simple terms"}
    ]
    
    # Send the chat request
    print("Sending chat request...")
    response = client.chat(model="llama3.2:3b", messages=messages)
    
    # Print the response
    print("\nResponse:")
    print(response["message"]["content"])

if __name__ == "__main__":
    main()

