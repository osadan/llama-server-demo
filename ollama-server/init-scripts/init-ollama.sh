#!/bin/bash
set -e

MODEL="llama3.2:3b"
OLLAMA_HOST="${OLLAMA_HOST:-0.0.0.0:11434}"
MAX_RETRIES=30
RETRY_DELAY=2

# Function to check if Ollama API is ready
wait_for_ollama() {
    local retries=0
    echo "Waiting for Ollama API to be ready..."
    
    while [ $retries -lt $MAX_RETRIES ]; do
        # Try multiple methods to check if API is ready
        if curl -s -f "http://127.0.0.1:11434/api/tags" > /dev/null 2>&1 || \
           curl -s -f "http://localhost:11434/api/tags" > /dev/null 2>&1 || \
           curl -s -f "http://[::1]:11434/api/tags" > /dev/null 2>&1 || \
           (command -v wget > /dev/null && wget -q -O - "http://127.0.0.1:11434/api/tags" > /dev/null 2>&1) || \
           (command -v ollama > /dev/null && ollama list > /dev/null 2>&1); then
            echo "Ollama API is ready!"
            return 0
        fi
        
        retries=$((retries + 1))
        if [ $((retries % 5)) -eq 0 ]; then
            echo "Attempt $retries/$MAX_RETRIES: Ollama API not ready yet, waiting ${RETRY_DELAY}s..."
        fi
        sleep $RETRY_DELAY
    done
    
    echo "ERROR: Ollama API did not become ready within timeout period"
    return 1
}

# Function to check if model exists
model_exists() {
    if ollama list 2>/dev/null | grep -q "^${MODEL}\s"; then
        return 0
    else
        return 1
    fi
}

# Function to pull model
pull_model() {
    echo "Model ${MODEL} not found. Pulling..."
    if ollama pull "${MODEL}"; then
        echo "Successfully pulled ${MODEL}"
        return 0
    else
        echo "ERROR: Failed to pull ${MODEL}"
        return 1
    fi
}

# Start Ollama server in background
echo "Starting Ollama server..."
/bin/ollama serve &
OLLAMA_PID=$!

# Trap signals to forward them to Ollama process
cleanup() {
    echo "Shutting down..."
    kill $OLLAMA_PID 2>/dev/null || true
    wait $OLLAMA_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGTERM SIGINT

# Wait for Ollama to be ready
if ! wait_for_ollama; then
    kill $OLLAMA_PID 2>/dev/null || true
    exit 1
fi

# Check if model exists and pull if needed
if ! model_exists; then
    if ! pull_model; then
        kill $OLLAMA_PID 2>/dev/null || true
        exit 1
    fi
else
    echo "Model ${MODEL} already exists, skipping pull."
fi

echo "Initialization complete. Ollama server is running with model ${MODEL} available."

# Wait for the Ollama process
wait $OLLAMA_PID

