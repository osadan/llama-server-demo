# Ollama Server Project

This project provides a complete setup for running and interacting with an Ollama server. It consists of two main components: a Docker-based Ollama server deployment and a Python client library for programmatic access. The server is configured to automatically initialize and pull the llama3.2:3b model, making it easy to get started with local LLM inference. The Python client library offers a simple, intuitive interface for sending chat messages, generating text, and streaming responses with comprehensive error handling.

## Project Structure

The repository is organized into two primary directories: `ollama-server` and `ollama-client`. The `ollama-server` directory contains Docker Compose configuration files and initialization scripts that handle server startup and model preparation. The `ollama-client` directory includes the Python client library, example scripts demonstrating various use cases, and comprehensive test suites. This separation allows for independent development and deployment of the server infrastructure and client applications.

## Getting Started

To begin using this project, navigate to the `ollama-server` directory and start the Docker container using `docker-compose up`. The initialization script will automatically wait for the Ollama API to be ready and pull the llama3.2:3b model if it's not already available. Once the server is running on `http://localhost:11434`, you can use the Python client library from the `ollama-client` directory to interact with the server. Install the client library using `uv sync` within the `ollama-client` directory, then import `OllamaClient` to start sending requests.

## Features

The server setup includes automatic model management, health checks, and persistent storage for downloaded models. The Python client library supports both synchronous and streaming responses, multi-turn conversations with context management, and comprehensive error handling with custom exceptions. Example scripts are provided for common use cases including simple chat interactions, text generation, streaming responses, and multi-turn conversations. The project is designed to be production-ready with proper error handling, type hints, and extensive documentation.

