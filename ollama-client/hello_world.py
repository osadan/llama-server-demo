"""Simple hello world example to test Ollama server connection."""
from ollama_client import OllamaClient

def main():
    print("Testing connection to Ollama server...")
    
    # Initialize the client
    client = OllamaClient(base_url="http://localhost:11434")
    
    # Check server health
    print("Checking server health...")
    if client.check_health():
        print("✓ Server is healthy and accessible!")
    else:
        print("✗ Server is not accessible. Make sure Ollama is running.")
        return
    
    # List available models
    print("\nChecking available models...")
    try:
        models = client.list_models()
        if models:
            print(f"✓ Found {len(models)} model(s):")
            for model in models:
                print(f"  - {model.get('name', 'unknown')}")
            model_name = models[0].get('name', 'llama3.2:3b')
            print(f"\nUsing model: {model_name}")
        else:
            print("⚠ No models found. Using default 'llama3.2:3b'")
            model_name = "llama3.2:3b"
    except Exception as e:
        print(f"⚠ Could not list models: {e}")
        model_name = "llama3.2:3b"
    
    # Try a simple chat
    print(f"\nSending a simple 'Hello' message to {model_name}...")
    try:
        messages = [
            {"role": "user", "content": "Say hello in one sentence"}
        ]
        
        response = client.chat(model=model_name, messages=messages)
        
        print("\n✓ Response received:")
        print("-" * 50)
        print(response["message"]["content"])
        print("-" * 50)
        print("\n✓ Connection test successful!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("1. Ollama server is running (docker-compose up)")
        print("2. The model 'llama3.2:3b' is available (ollama pull llama3.2:3b)")

if __name__ == "__main__":
    main()

