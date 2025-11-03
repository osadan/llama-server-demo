# Plan: Auto-pull llama3.2:3b Model for Ollama Docker Compose

## Overview
Add functionality to automatically pull and make available the `llama3.2:3b` model when the Ollama container starts, without manual intervention.

## Implementation Approach

### Option 1: Entrypoint Wrapper Script (Recommended)
Create a wrapper script that:
1. Starts the original Ollama service in the background
2. Waits for the Ollama API to be ready (health check on port 11434)
3. Checks if the model `llama3.2:3b` already exists
4. If not present, automatically pulls it using `ollama pull llama3.2:3b`
5. Then execs the original Ollama entrypoint

**Files to create:**
- `scripts/init-ollama.sh` - Shell script that handles model pulling
- Update `docker-compose.yml` to:
  - Mount the init script as a volume
  - Override entrypoint to use the wrapper script
  - Make script executable

**Advantages:**
- Single container solution
- Automatic on every start
- Checks if model exists before pulling (faster restarts)
- Minimal changes to existing setup

### Option 2: Init Container Pattern
Create a separate init container that:
1. Waits for Ollama service to be healthy
2. Pulls the model using `ollama pull`
3. Exits after model is pulled

**Files to create:**
- `scripts/init-container.sh` - Script for init container
- Update `docker-compose.yml` to add an init service

**Advantages:**
- Keeps main Ollama service unchanged
- Clear separation of concerns

**Disadvantages:**
- More complex docker-compose setup
- Requires additional container

## Selected Approach
**Option 1: Entrypoint Wrapper Script**

This is simpler, more maintainable, and keeps everything in one container while providing automatic model initialization.

## Implementation Details

### File Structure
```
ollama-server/
├── docker-compose.yml (to be updated)
└── scripts/
    └── init-ollama.sh (new - entrypoint wrapper script)
```

### init-ollama.sh Script Features
1. Start Ollama in background using original entrypoint
2. Poll Ollama API endpoint (`http://localhost:11434/api/tags`) with retry logic
3. Check if model exists using `ollama list | grep -q "llama3.2:3b"`
4. Pull model if missing: `ollama pull llama3.2:3b`
5. Forward process signals for proper shutdown

### docker-compose.yml Changes
- Add volume mount for init script: `./scripts/init-ollama.sh:/init-ollama.sh:ro`
- Override entrypoint: `entrypoint: ["/init-ollama.sh"]`
- Ensure script is executable via build or chmod in script itself

### Error Handling
- Maximum retry attempts for API health check (e.g., 30 attempts with 2s delay = 60s timeout)
- Log messages for debugging
- Exit with error if model pull fails
- Graceful handling of existing model (skip pull if already present)

## Implementation Steps

1. Create `scripts/init-ollama.sh` script with:
   - Background Ollama startup
   - Health check polling loop
   - Model existence check
   - Conditional model pull
   - Proper signal forwarding

2. Update `docker-compose.yml`:
   - Add volume mount for init script
   - Override entrypoint to use wrapper script
   - Ensure proper file permissions

3. Test the setup:
   - Verify model is pulled on first start
   - Verify model is not re-pulled on subsequent starts (faster startup)
   - Verify Ollama API is accessible after model pull completes

