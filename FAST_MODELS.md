# Fast Models Guide

## Available Fast Models

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **phi:latest** | 2.6B | ⚡⚡⚡⚡⚡ Fastest | Good | Quick responses, limited context |
| **neural-chat:latest** | 13B | ⚡⚡⚡ Fast | Very Good | Balanced speed/quality |
| **orca-mini:latest** | 3B | ⚡⚡⚡⚡ Very Fast | Good | Fast reasoning |
| mistral:latest | 7B | ⚡⚡ Slow | Excellent | Complex tasks (current) |

## Quick Setup

### 1. Download a Fast Model

```bash
chmod +x setup_fast_models.sh
./setup_fast_models.sh
```

Or manually:

```bash
# Download Phi (fastest)
ollama pull phi:latest

# Or Neural-Chat (balanced)
ollama pull neural-chat:latest

# Or Orca-Mini (fast + decent quality)
ollama pull orca-mini:latest
```

### 2. Use the Fast Model

```bash
# Set environment variable
export MODEL_NAME="phi:latest"

# Run agent with fast model
python run_agent.py --mode interactive
```

### 3. Check Speed Difference

```bash
# With tool-only mode (instant)
time python run_agent.py --mode tools-only

# With fast model (seconds)
export MODEL_NAME="phi:latest"
time python run_agent.py --mode interactive
```

## Performance Comparison

```
Tool-Only Mode:      < 100ms (instant)
Phi:latest:          1-3 seconds
Neural-Chat:latest:  3-5 seconds
Orca-Mini:latest:    2-4 seconds
Mistral:latest:      5-10 seconds (current)
```

## Recommendations

### For Development (Quick Testing)
```bash
export MODEL_NAME="phi:latest"
```

### For Balanced Use
```bash
export MODEL_NAME="neural-chat:latest"
```

### For Complex Reasoning
```bash
export MODEL_NAME="mistral:latest"  # (current)
```

### For Zero-Latency (Tool-Only)
```bash
python run_agent.py --mode tools-only
```

## Usage Examples

### Start Interactive with Phi (Fast)
```bash
export MODEL_NAME="phi:latest"
python run_agent.py --mode interactive
```

### Run Examples with Neural-Chat
```bash
export MODEL_NAME="neural-chat:latest"
python examples.py
```

### Switch Models Mid-Session
```bash
# Terminal 1: Start agent with default
python run_agent.py --mode interactive

# Terminal 2: Change model and test
export MODEL_NAME="phi:latest"
curl http://127.0.0.1:11777/api/generate -d '{"model":"phi:latest","prompt":"Hello"}'
```

## Troubleshooting

### Model taking too long?
```bash
# Try the fastest model
export MODEL_NAME="phi:latest"
timeout 10 python run_agent.py --mode interactive
```

### Want zero latency?
```bash
# Use tool-only mode (no LLM)
python run_agent.py --mode tools-only
```

### Model not found?
```bash
# Check available models
ollama list

# Download the model
ollama pull phi:latest
```

## Pro Tips

1. **For production**, use `--mode tools-only` for instant response times
2. **For development**, use `phi:latest` for fast feedback
3. **For quality**, use `mistral:latest` or `neural-chat:latest`
4. **Parallel requests**: Use `--num-threads 4` with Ollama for better throughput

```bash
export OLLAMA_NUM_THREADS=4
python run_agent.py --mode interactive
```

5. **Batch operations**: Use tool-only mode for multiple sequential operations

```bash
# This is instant
python run_agent.py --mode tools-only << EOF
create_table users
insert_record users name=John email=john@example.com
query SELECT * FROM users
EOF
```
