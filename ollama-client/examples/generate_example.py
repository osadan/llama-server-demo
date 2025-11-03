"""Simple generation example using OllamaClient."""
from ollama_client import OllamaClient

def main():
    # Initialize the client
    client = OllamaClient()
    
    # Send a generation request
    print("Generating response...")
    response = client.generate(
        model="llama3.2:3b",
        prompt="Write a haiku about programming"
    )
    
    # Print the response
    print("\nGenerated text:")
    print(response["response"])

if __name__ == "__main__":
    main()

