#!/bin/bash
# ============================================================================
# Complete Setup and Run Script for Langchain Tool Agent with Ollama
# 
# This script sets up all environment variables, installs dependencies,
# verifies Ollama connectivity, and starts the agent.
# ============================================================================

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# SECTION 1: ENVIRONMENT VARIABLES
# ============================================================================

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}SETTING UP ENVIRONMENT VARIABLES${NC}"
echo -e "${BLUE}========================================${NC}"

# Python environment
vEnv="/home/ccm2kor/.conda/envs/myenv"
export CACHE_BASE="/home/ccm2kor/.conda/envs/myenv"

# Ollama paths
export OLLAMA_HOME="/fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor"
export OLLAMA_MODELS="${OLLAMA_HOME}/models"
export OLLAMA_LOGS="${OLLAMA_HOME}/logs"
export PATH="${OLLAMA_HOME}/bin:$PATH"

# Model configuration
export MODEL_NAME="mistral:latest"

# Ollama host configuration
export OLLAMA_HOST="http://127.0.0.1:11777"
export NO_PROXY="127.0.0.1,localhost"
export no_proxy="127.0.0.1,localhost"
export OLLAMA_NUM_PARALLEL=4

# Agent paths
AGENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor/ResponseGen/jarvic-first-pass-filter"

# PyTorch/Triton settings
export PYTORCH_CUDA_ALLOC_CONF="max_split_size_mb:512"
export TORCH_COMPILE_DEBUG_DIR="${CACHE_BASE}/torch_compile_debug"
export TORCHINDUCTOR_CACHE_DIR="${CACHE_BASE}/torch_compile"
export TRITON_CACHE_DIR="${CACHE_BASE}/triton"

# Cache and temp directories
export HOME="${CACHE_BASE}"
export TMPDIR="${CACHE_BASE}/tmp"
export XDG_CACHE_HOME="${CACHE_BASE}"
export TORCH_HOME="${CACHE_BASE}/torch_home"
export TRANSFORMERS_CACHE="${CACHE_BASE}/hf_cache"
export HF_HOME="${CACHE_BASE}/hf_cache"
export CUDA_CACHE_PATH="${CACHE_BASE}/cuda_cache"

# Proxy settings (if needed)
export HTTP_PROXY="http://rb-proxy-sl.bosch.com:8080"
export HTTPS_PROXY="http://rb-proxy-sl.bosch.com:8080"

echo -e "${GREEN}✓ Environment variables configured${NC}"

# ============================================================================
# SECTION 2: CREATE NECESSARY DIRECTORIES
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}CREATING NECESSARY DIRECTORIES${NC}"
echo -e "${BLUE}========================================${NC}"

mkdir -p "${CACHE_BASE}/torch_compile" \
         "${CACHE_BASE}/torch_compile_debug" \
         "${CACHE_BASE}/triton" \
         "${CACHE_BASE}/hf_cache" \
         "${CACHE_BASE}/tmp" \
         "${CACHE_BASE}/torch_home" \
         "${OLLAMA_LOGS}" \
         "${OLLAMA_MODELS}" \
         "${PROJECT_ROOT}/output/logs" \
         "${PROJECT_ROOT}/output_uvi/logs"

echo -e "${GREEN}✓ All directories created${NC}"

# ============================================================================
# SECTION 3: ACTIVATE CONDA ENVIRONMENT
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}ACTIVATING CONDA ENVIRONMENT${NC}"
echo -e "${BLUE}========================================${NC}"

# Source conda initialization
if [ -f "/fs/applications/modules/current/init/bash" ]; then
    . /fs/applications/modules/current/init/bash
fi

# Activate conda environment
if [ -d "${vEnv}" ]; then
    source activate "${vEnv}" 2>/dev/null || conda activate "${vEnv}"
    echo -e "${GREEN}✓ Conda environment activated: ${vEnv}${NC}"
else
    echo -e "${YELLOW}⚠ Conda environment not found: ${vEnv}${NC}"
    echo -e "${YELLOW}Make sure your conda environment is set up${NC}"
fi

# ============================================================================
# SECTION 4: VERIFY GPU AVAILABILITY
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}CHECKING GPU AVAILABILITY${NC}"
echo -e "${BLUE}========================================${NC}"

if command -v nvidia-smi &> /dev/null; then
    echo -e "${GREEN}GPU Information:${NC}"
    nvidia-smi --query-gpu=index,name,memory.total,memory.free --format=csv,noheader
    GPU_AVAILABLE=1
else
    echo -e "${YELLOW}⚠ GPU not available (nvidia-smi not found)${NC}"
    GPU_AVAILABLE=0
fi

# ============================================================================
# SECTION 5: NAVIGATE TO AGENT DIRECTORY
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}NAVIGATING TO AGENT DIRECTORY${NC}"
echo -e "${BLUE}========================================${NC}"

cd "${AGENT_DIR}"
echo -e "${GREEN}✓ Working directory: $(pwd)${NC}"

# ============================================================================
# SECTION 6: INSTALL DEPENDENCIES
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}INSTALLING PYTHON DEPENDENCIES${NC}"
echo -e "${BLUE}========================================${NC}"

if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}Upgrading pip, setuptools, and wheel...${NC}"
    pip install --upgrade pip setuptools wheel --quiet
    
    echo -e "${YELLOW}Installing langchain-core and langchain-ollama...${NC}"
    pip install langchain-core langchain-ollama --quiet
    
    echo -e "${YELLOW}Installing packages from requirements.txt...${NC}"
    pip install -r requirements.txt --only-binary :all: 2>/dev/null || \
    pip install -r requirements.txt
    
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ requirements.txt not found${NC}"
    exit 1
fi

# ============================================================================
# SECTION 7: VERIFY ENVIRONMENT VARIABLES
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}ENVIRONMENT VARIABLES SUMMARY${NC}"
echo -e "${BLUE}========================================${NC}"

echo "HOME: $HOME"
echo "TMPDIR: $TMPDIR"
echo "OLLAMA_HOME: $OLLAMA_HOME"
echo "OLLAMA_HOST: $OLLAMA_HOST"
echo "MODEL_NAME: $MODEL_NAME"
echo "OLLAMA_NUM_PARALLEL: $OLLAMA_NUM_PARALLEL"
echo "Python: $(which python)"
echo "Agent Directory: $AGENT_DIR"
echo "Project Root: $PROJECT_ROOT"

# ============================================================================
# SECTION 8: CHECK OLLAMA CONNECTIVITY
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}CHECKING OLLAMA CONNECTIVITY${NC}"
echo -e "${BLUE}========================================${NC}"

if command -v curl &> /dev/null; then
    if curl -s "${OLLAMA_HOST}/api/version" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Ollama is running at ${OLLAMA_HOST}${NC}"
        OLLAMA_RUNNING=1
    else
        echo -e "${YELLOW}⚠ Ollama is not running at ${OLLAMA_HOST}${NC}"
        echo -e "${YELLOW}You need to start Ollama with: ollama serve &${NC}"
        OLLAMA_RUNNING=0
    fi
else
    echo -e "${YELLOW}⚠ curl not available - cannot verify Ollama${NC}"
    OLLAMA_RUNNING=0
fi

# ============================================================================
# SECTION 9: START OLLAMA (if not running and GPU available)
# ============================================================================

if [ $OLLAMA_RUNNING -eq 0 ] && [ $GPU_AVAILABLE -eq 1 ]; then
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}STARTING OLLAMA SERVER${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    echo -e "${YELLOW}Starting Ollama on $(hostname)...${NC}"
    nohup ollama serve > "${OLLAMA_LOGS}/ollama_agent.log" 2>&1 &
    OLLAMA_PID=$!
    echo -e "${YELLOW}Ollama PID: $OLLAMA_PID${NC}"
    
    # Wait for Ollama to be ready
    echo -e "${YELLOW}Waiting for Ollama to be ready...${NC}"
    READY=0
    for i in $(seq 1 60); do
        if curl -s "${OLLAMA_HOST}/api/version" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Ollama is ready (attempt $i/60)${NC}"
            READY=1
            break
        fi
        echo "  Waiting... (attempt $i/60)"
        sleep 2
    done
    
    if [ $READY -eq 0 ]; then
        echo -e "${RED}✗ Ollama failed to start${NC}"
        echo -e "${RED}Last 50 lines of log:${NC}"
        tail -n 50 "${OLLAMA_LOGS}/ollama_agent.log" 2>/dev/null || true
        exit 1
    fi
fi

# ============================================================================
# SECTION 10: VERIFY MODEL AVAILABILITY
# ============================================================================

if [ $OLLAMA_RUNNING -eq 1 ] || [ $READY -eq 1 ]; then
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}CHECKING MODEL AVAILABILITY${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    echo -e "${YELLOW}Checking for model: ${MODEL_NAME}${NC}"
    
    if ! ollama list 2>/dev/null | grep -q "mistral"; then
        echo -e "${YELLOW}Pulling model ${MODEL_NAME}...${NC}"
        if ollama pull "${MODEL_NAME}"; then
            echo -e "${GREEN}✓ Model pulled successfully${NC}"
        else
            echo -e "${YELLOW}⚠ Failed to pull model${NC}"
        fi
    else
        echo -e "${GREEN}✓ Model ${MODEL_NAME} is available${NC}"
    fi
fi

# ============================================================================
# SECTION 11: RUN VERIFICATION TESTS
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}RUNNING VERIFICATION TESTS${NC}"
echo -e "${BLUE}========================================${NC}"

if [ -f "test_ollama_integration.py" ]; then
    echo -e "${YELLOW}Running integration tests...${NC}"
    python test_ollama_integration.py
    echo -e "${GREEN}✓ Tests completed${NC}"
else
    echo -e "${YELLOW}⚠ test_ollama_integration.py not found${NC}"
fi

# ============================================================================
# SECTION 12: DISPLAY STARTUP OPTIONS
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}SETUP COMPLETE!${NC}"
echo -e "${BLUE}========================================${NC}"

echo -e "\n${GREEN}You can now start the agent using:${NC}\n"

echo -e "${YELLOW}1. Interactive Mode (Recommended):${NC}"
echo "   cd ${AGENT_DIR}"
echo "   python run_agent.py --mode interactive"

echo -e "\n${YELLOW}2. Tool-Only Mode (No Ollama needed):${NC}"
echo "   cd ${AGENT_DIR}"
echo "   python run_agent.py --mode tools-only"

echo -e "\n${YELLOW}3. Check Mode (Diagnose issues):${NC}"
echo "   cd ${AGENT_DIR}"
echo "   python run_agent.py --mode check"

echo -e "\n${YELLOW}4. Run Examples:${NC}"
echo "   cd ${AGENT_DIR}"
echo "   python examples.py"

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}ENVIRONMENT READY FOR AGENT EXECUTION${NC}"
echo -e "${BLUE}========================================${NC}\n"

# ============================================================================
# SECTION 13: OPTIONAL - START AGENT INTERACTIVELY
# ============================================================================

read -p "Would you like to start the agent now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n${BLUE}Starting agent in interactive mode...${NC}\n"
    python run_agent.py --mode interactive
else
    echo -e "\n${GREEN}Setup complete. Run: python run_agent.py --mode interactive${NC}"
fi
