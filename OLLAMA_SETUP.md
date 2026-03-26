# Ollama Setup Guide for Langchain Tool Agent

## Quick Start

### 1. Ensure Ollama is Running

```bash
# Check if Ollama is running
curl -s http://127.0.0.1:11777/api/version
# You should see a response like: {"version":"x.x.x"}

# If not running, start it:
export OLLAMA_HOST="http://127.0.0.1:11777"
export OLLAMA_HOME="/fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor"
ollama serve &
```

### 2. Verify Mistral Model

```bash
# List available models
ollama list

# Should show something like:
# mistral:latest            4.4 GB   2 days ago

# If not present, pull it:
ollama pull mistral:latest
```

### 3. Run the Agent

```bash
cd /fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor/langchain_tools

# Option 1: Direct execution with no LLM (no dependencies needed)
python examples.py

# Option 2: With Ollama LLM (requires langchain-ollama)
pip install langchain-ollama
python -c "from examples import example_with_ollama_llm; example_with_ollama_llm()"
```

## Environment Setup

The BSUB job already exports these variables:

```bash
export OLLAMA_HOST="http://127.0.0.1:11777"
export MODEL_NAME="mistral:latest"
export OLLAMA_HOME="/fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor"
export OLLAMA_MODELS="$OLLAMA_HOME/models"
export OLLAMA_LOGS="$OLLAMA_HOME/logs"
```

You can also set them manually:

```bash
export OLLAMA_HOST="http://127.0.0.1:11777"
export MODEL_NAME="mistral:latest"
```

## Available Ollama Models

The agent is configured for `mistral:latest` but you can use any Ollama model:

### Small & Fast (Good for CPU)
```bash
ollama pull mistral:latest      # 4.4GB - Fast, capable
ollama pull neural-chat:latest  # 3.8GB - Good for chat
ollama pull orca-mini:latest    # 1.3GB - Very fast
```

### Larger & More Capable (Need good GPU)
```bash
ollama pull llama2:latest       # 3.8GB - Llama2 base
ollama pull llama2:70b          # 40GB - Large version
ollama pull neural-chat:70b     # 35GB - Large chat model
```

## Troubleshooting

### Issue: Connection refused

```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama if not running
export OLLAMA_HOST="http://127.0.0.1:11777"
ollama serve > /fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor/logs/ollama.log 2>&1 &

# Wait for it to start (10-20 seconds)
sleep 15

# Test connection
curl -s http://127.0.0.1:11777/api/version
```

### Issue: Model not found

```bash
# List available models
ollama list

# Pull the model
ollama pull mistral:latest

# Verify it was downloaded
ls -la /fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor/models/
```

### Issue: Out of memory

```bash
# Reduce context window in config
export OLLAMA_NUM_PARALLEL=1

# Or use a smaller model
ollama pull orca-mini:latest
```

### Issue: Slow responses

```bash
# Check if GPU is available
nvidia-smi

# If no GPU, Ollama will use CPU (much slower)
# Consider using a smaller model:
ollama pull orca-mini:latest
```

## Testing the Agent

```python
from agent import create_agent
from config import Config

# Test 1: Direct tool execution (no LLM)
print("Test 1: Direct execution")
agent = create_agent(llm=None)
result = agent.execute_task(
    "calculate",
    operation="add",
    a=5,
    b=3
)
print(f"5 + 3 = {result['result']}")

# Test 2: With Ollama LLM
try:
    from langchain_ollama import OllamaLLM
    
    print("\nTest 2: With Ollama")
    llm = OllamaLLM(
        model=Config.LLM_MODEL,
        base_url=Config.OLLAMA_HOST,
        temperature=Config.LLM_TEMPERATURE
    )
    
    agent = create_agent(llm=llm)
    result = agent.run("Calculate 5 + 3")
    print(f"Response: {result['output']}")
except ImportError:
    print("langchain-ollama not installed")
```

## Integration with BSUB Job

The agent is already integrated in the BSUB job:

```bash
# In agent_intent_training.bsub:
export OLLAMA_HOST="http://127.0.0.1:11777"
export MODEL_NAME="mistral:latest"
export OLLAMA_HOME="/fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor"

# The job starts Ollama:
ollama serve > "${OLLAMA_LOGS}/ollama.log" 2>&1 &

# And verifies it's ready:
for i in $(seq 1 60); do
    if curl -sS "${OLLAMA_HOST}/api/version" >/dev/null 2>&1; then
        echo "Ollama is ready"
        break
    fi
    sleep 2
done
```

## Performance Notes

- **Mistral (4.4GB)**: ~20-50 tokens/sec on A100 GPU
- **Orca-Mini (1.3GB)**: ~100+ tokens/sec (faster, slightly lower quality)
- **On CPU**: Much slower - not recommended for production

## Resources

- Ollama Documentation: https://ollama.ai
- Model Library: https://ollama.ai/library
- LangChain + Ollama: https://python.langchain.com/docs/integrations/providers/ollama
