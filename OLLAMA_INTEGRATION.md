# Ollama Agent Integration Guide

## Overview

The Langchain Tool Agent is now fully integrated with **Ollama** instead of OpenAI. This means:

✓ **No API keys required**
✓ **No API costs**
✓ **Local inference** on your compute node
✓ **Privacy-preserving** (data stays local)
✓ **Fast** (especially with GPU)

## Quick Start

### 1. Environment Setup (Already in BSUB Job)

Your job file already includes:

```bash
export OLLAMA_HOST="http://127.0.0.1:11777"
export MODEL_NAME="mistral:latest"
export OLLAMA_HOME="/fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor"
```

### 2. Install Dependencies

```bash
cd /fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor/langchain_tools

# Core dependencies (always needed)
pip install -r requirements.txt

# For Ollama LLM support (recommended)
pip install langchain-ollama
```

### 3. Verify Ollama is Running

```bash
# Check status
python run_agent.py --mode check

# Output should show:
# ✓ Ollama is running at http://127.0.0.1:11777
# ✓ Model 'mistral:latest' is available
```

### 4. Run the Agent

```bash
# Interactive mode
python run_agent.py --mode interactive

# Tools-only mode (no LLM required)
python run_agent.py --mode tools-only

# Check setup
python run_agent.py --mode check
```

## Usage Examples

### Example 1: Using the Agent Interactively

```bash
python run_agent.py --mode interactive
```

Then type your requests:

```
You: Create a table called 'users' with columns id, name, and email
Agent: [Creates the table and confirms]

You: Insert a record with name='John' and email='john@example.com'
Agent: [Inserts record and confirms]

You: Calculate the average of numbers 10, 20, 30, 40
Agent: [Calculates and returns 25]
```

### Example 2: Tool-Only Mode (No LLM)

```python
from agent import create_agent

# Create agent without LLM
agent = create_agent(llm=None)

# Use tools directly
result = agent.execute_task(
    "calculate",
    operation="add",
    a=5,
    b=3
)
print(result['result'])  # Output: 8
```

### Example 3: With Ollama LLM

```python
from langchain_ollama import OllamaLLM
from agent import create_agent
from config import Config

# Create LLM
llm = OllamaLLM(
    model=Config.LLM_MODEL,
    base_url=Config.OLLAMA_HOST,
    temperature=Config.LLM_TEMPERATURE
)

# Create agent
agent = create_agent(llm=llm)

# Run complex task
result = agent.run("""
    Please:
    1. Create a products table
    2. Insert 3 sample products
    3. Calculate the average price
""")

print(result['output'])
```

### Example 4: Programmatic Configuration

```python
from config import Config
from agent import create_agent

# Override configuration
Config.initialize(
    LLM_MODEL="orca-mini:latest",  # Use different model
    OLLAMA_HOST="http://127.0.0.1:11777",
    LLM_TEMPERATURE=0.5
)

# Use the agent
agent = create_agent(llm=None)
agent.print_tools_info()
```

## Available Tools

### File Operations
```python
agent.execute_task("read_file", file_path="/path/to/file.txt")
agent.execute_task("write_file", file_path="/path/to/file.txt", content="Hello")
agent.execute_task("list_files", directory="/path/to/dir")
agent.execute_task("copy_file", source="/path/from", destination="/path/to")
agent.execute_task("delete_file", file_path="/path/to/file.txt")
```

### Database Operations
```python
agent.execute_task("create_table", table_name="users", schema={
    "id": "INTEGER PRIMARY KEY",
    "name": "TEXT",
    "email": "TEXT"
})

agent.execute_task("insert_record", table_name="users", record={
    "name": "John",
    "email": "john@example.com"
})

agent.execute_task("query", query="SELECT * FROM users WHERE name='John'")
```

### Mathematical Operations
```python
agent.execute_task("calculate", operation="add", a=5, b=3)  # 8
agent.execute_task("calculate", operation="multiply", a=4, b=5)  # 20
agent.execute_task("calculate", operation="average", numbers=[1,2,3,4,5])  # 3
```

## Configuration Options

### Environment Variables

```bash
# Ollama settings
export OLLAMA_HOST="http://127.0.0.1:11777"
export MODEL_NAME="mistral:latest"

# Model parameters
export LLM_TEMPERATURE="0.7"  # 0=deterministic, 1=creative
export LLM_MAX_TOKENS="2000"

# Agent settings
export AGENT_VERBOSE="true"
export DB_PATH="./agent.db"
```

### Python Configuration

```python
from config import Config

Config.LLM_MODEL = "neural-chat:latest"
Config.LLM_TEMPERATURE = 0.5
Config.DATABASE_PATH = "./custom.db"
Config.AGENT_VERBOSE = True
```

## Troubleshooting

### Issue: "Cannot connect to Ollama"

```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
export OLLAMA_HOST="http://127.0.0.1:11777"
ollama serve &

# Wait for it to start
sleep 10

# Test connection
curl http://127.0.0.1:11777/api/version
```

### Issue: "Model not found"

```bash
# Check available models
ollama list

# Download the model
ollama pull mistral:latest

# Or use a different model
ollama pull neural-chat:latest
ollama pull orca-mini:latest
```

### Issue: "LangChain Ollama not installed"

```bash
pip install langchain-ollama

# Or install all dependencies
pip install -r requirements.txt
pip install langchain-ollama
```

### Issue: Out of Memory

```bash
# Use a smaller model
ollama pull orca-mini:latest

# Or reduce number of parallel requests
export OLLAMA_NUM_PARALLEL=1
```

## Integration with BSUB

The agent is integrated in your job submission:

```bash
#!/bin/bash -l
#BSUB -J agent-job
#BSUB -q batch_a100
#BSUB -W 48:00
#BSUB -gpu "num=1"

# Set up Ollama paths
export OLLAMA_HOST="http://127.0.0.1:11777"
export MODEL_NAME="mistral:latest"
export OLLAMA_HOME="/fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor"

# Start Ollama
ollama serve > $OLLAMA_HOME/logs/ollama.log 2>&1 &
sleep 10

# Run your agent code
cd /fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor/langchain_tools
python run_agent.py --mode interactive
```

## Available Models

### Recommended for Speed
- **mistral:latest** (4.4GB) - Best balance, default
- **neural-chat:latest** (3.8GB) - Good for chat
- **orca-mini:latest** (1.3GB) - Very fast

### For Better Quality
- **llama2:latest** (3.8GB) - Llama2 base
- **neural-chat:70b** (35GB) - Larger, better quality
- **mistral:8x7b** (46GB) - Mixture of experts

## Performance Notes

| Model | Size | Speed | Quality | GPU Mem |
|-------|------|-------|---------|---------|
| orca-mini | 1.3GB | ★★★★★ | ★★ | 2GB |
| mistral | 4.4GB | ★★★★ | ★★★★ | 8GB |
| neural-chat | 3.8GB | ★★★★ | ★★★ | 8GB |
| llama2:70b | 38GB | ★★ | ★★★★★ | 40GB |

## API Reference

See the inline documentation for detailed API:

- [File Operations](file_operations.py)
- [Database Operations](database_operations.py)
- [Math Operations](math_operations.py)
- [Agent Class](agent.py)

## Support

For issues or questions:

1. Check [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for setup help
2. Review [ADVANCED_USAGE.md](ADVANCED_USAGE.md) for complex scenarios
3. Run `python run_agent.py --mode check` to diagnose issues
