#!/bin/bash
# ============================================================================
# Setup Fast Models for Ollama
# 
# Downloads lightweight, fast models for quick LLM inference
# ============================================================================

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Setup Ollama environment
export OLLAMA_HOME="${OLLAMA_HOME:-/fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor}"
export PATH="${OLLAMA_HOME}/bin:$PATH"
export OLLAMA_HOST="${OLLAMA_HOST:-http://127.0.0.1:11777}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}OLLAMA FAST MODELS SETUP${NC}"
echo -e "${BLUE}========================================${NC}"
echo "OLLAMA_HOME: ${OLLAMA_HOME}"
echo "PATH includes: ${OLLAMA_HOME}/bin"
echo ""

# Check if Ollama is running
if ! curl -s "${OLLAMA_HOST}/api/version" > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Ollama is not running${NC}"
    echo -e "${YELLOW}Start Ollama with: ollama serve &${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Ollama is running${NC}\n"

# Define fast models
declare -a FAST_MODELS=(
    "phi:latest|Phi (2.6B) - Super fast, good quality"
    "neural-chat:latest|Neural-Chat (13B) - Fast and capable"
    "orca-mini:latest|Orca-Mini (3B) - Very fast, decent quality"
)

echo -e "${BLUE}Available Fast Models:${NC}\n"

for i in "${!FAST_MODELS[@]}"; do
    IFS='|' read -r model desc <<< "${FAST_MODELS[$i]}"
    echo "$((i+1)). $desc"
    echo "   Model: $model"
    echo ""
done

echo -e "${YELLOW}Current model: ${MODEL_NAME:-mistral:latest}${NC}\n"

read -p "Select model number (1-3) or press Enter to skip: " choice

case $choice in
    1)
        MODEL="phi:latest"
        ;;
    2)
        MODEL="neural-chat:latest"
        ;;
    3)
        MODEL="orca-mini:latest"
        ;;
    *)
        echo -e "${YELLOW}Skipping model download${NC}"
        exit 0
        ;;
esac

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}Downloading ${MODEL}...${NC}"
echo -e "${BLUE}========================================${NC}\n"

if ollama pull "${MODEL}"; then
    echo -e "\n${GREEN}✓ Model ${MODEL} downloaded successfully${NC}"
    echo -e "\n${YELLOW}To use this model, set:${NC}"
    echo "   export MODEL_NAME=\"${MODEL}\""
    echo -e "\n${YELLOW}Then run:${NC}"
    echo "   python run_agent.py --mode interactive"
else
    echo -e "\n${YELLOW}⚠ Failed to download ${MODEL}${NC}"
    exit 1
fi

# Show all available models
echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}Available Models:${NC}"
echo -e "${BLUE}========================================${NC}\n"

ollama list

echo -e "\n${GREEN}Setup complete!${NC}"
