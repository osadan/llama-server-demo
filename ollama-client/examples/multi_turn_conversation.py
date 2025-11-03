"""Multi-turn conversation example using OllamaClient."""
from ollama_client import OllamaClient

def main():
    # Initialize the client
    client = OllamaClient()
    
    # Start the conversation
    messages = [
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "How do I reverse a list in Python?"}
    ]
    
    # First turn
    print("User: How do I reverse a list in Python?")
    response = client.chat(model="llama3.2:3b", messages=messages)
    assistant_response = response["message"]["content"]
    print(f"\nAssistant: {assistant_response}\n")
    
    # Add assistant response to history
    messages.append({"role": "assistant", "content": assistant_response})
    
    # Second turn
    messages.append({"role": "user", "content": "Can you show me an example?"})
    print("User: Can you show me an example?")
    response = client.chat(model="llama3.2:3b", messages=messages)
    print(f"\nAssistant: {response['message']['content']}")

if __name__ == "__main__":
    main()

