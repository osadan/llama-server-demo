<!-- 1b6125d8-9b78-4629-816c-790e5e3dc315 1dde3302-64a1-4602-84be-a73b2434a988 -->
# Docker Compose Setup for Ollama Server

Create a `docker-compose.yml` file that runs Ollama server with external access.

## Implementation Details

**File to create:**

- `docker-compose.yml` - Docker Compose configuration file

**Configuration:**

- Use official `ollama/ollama:latest` Docker image
- Expose port `11434:11434` to allow external access
- Create named volume `ollama_data` mapped to `/root/.ollama` for persistent model storage
- Set environment variable `OLLAMA_HOST=0.0.0.0:11434` to bind to all network interfaces
- Set restart policy to `unless-stopped` for automatic recovery
- No GPU configuration (no device mappings or runtime specifications)

**Service Details:**

- Service name: `ollama`
- Container name: `ollama`
- Port mapping: Host port 11434 → Container port 11434
- Volume: Named volume for data persistence

This setup allows the Ollama server to be accessed from outside the container on port 11434, with models stored persistently in a Docker volume.

### To-dos

- [x] Create docker-compose.yml file with Ollama service configuration, port mapping, volume, and environment variables