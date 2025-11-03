"""Streaming chat example using OllamaClient."""
from ollama_client import OllamaClient

def main():
    # Initialize the client
    client = OllamaClient(base_url="http://localhost:11434")
    
    # Define the messages
    messages = [{"role": "user", "content": "Tell me a short story about a robot"}]
    
    # Send streaming chat request
    print("Streaming response:\n")
    print("-" * 50)
    
    for chunk in client.chat(model="llama3.2:3b", messages=messages, stream=True):
        if "message" in chunk and "content" in chunk["message"]:
            content = chunk["message"]["content"]
            print(content, end="", flush=True)
    
    print("\n" + "-" * 50)
    print("\nStreaming complete!")

if __name__ == "__main__":
    main()

