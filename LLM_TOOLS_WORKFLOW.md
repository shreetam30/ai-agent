# LLM + Tools Workflow Guide

## Overview

An **LLM with Tools** is a system where:
1. **LLM** (Language Model) - Understands user requests in natural language
2. **Tools** - Executable functions the LLM can call
3. **Agent** - Controller that manages the interaction between LLM and Tools

## The Basic Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                       USER REQUEST                          │
│              "Calculate 5 + 3 and save to file"             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  LANGCHAIN AGENT                            │
│  (Orchestrates interaction between LLM and Tools)           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM (phi/mistral)                        │
│  Input: User request + Available tools                      │
│  Process: "What tool should I use?"                         │
│  Output: Tool call specification                            │
│                                                              │
│  Thinking: "User wants to add 5+3 and save to file"        │
│  Decision: "I need add_tool and write_file_tool"            │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
   ┌──────────────┐              ┌──────────────────┐
   │  add_tool    │              │  write_file_tool │
   │  a=5, b=3    │              │  path=/tmp/out   │
   │  Returns: 8  │              │  content=8       │
   └──────┬───────┘              └────────┬─────────┘
          │                               │
          ▼                               ▼
      Result: 8                   File written: /tmp/out
          │                               │
        ┌─┴───────────────────────────────┤
        │                                 │
        ▼                                 ▼
┌─────────────────────────────────────────────────────────────┐
│              LLM PROCESSES TOOL RESULTS                     │
│  Input: Tool results (8 and file written)                  │
│  Process: "What to tell the user?"                         │
│  Output: Natural language response                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   USER RESPONSE                             │
│        "I've added 5 + 3 = 8 and saved to file"            │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. **Tools** (Your 36 Functions)

```python
# Each tool is a function the LLM can call
add_tool = Tool(
    name="add",
    func=lambda a, b: a + b,
    description="Add two numbers"
)

write_file_tool = Tool(
    name="write_file",
    func=write_file,
    description="Write content to a file"
)
```

**The LLM knows:**
- Tool name: `add`
- What it does: "Add two numbers"
- What parameters it needs: `a`, `b`
- What it returns: the sum

### 2. **LLM** (Brain)

```python
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="phi:latest")

# The LLM is given:
# - User request
# - Available tools (names, descriptions, parameters)
# - Tool results (if calling multiple tools)

# It responds with:
# "I should use the 'add' tool with a=5, b=3"
```

### 3. **Agent** (Orchestrator)

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(llm, tools)

# The agent:
# 1. Sends user request to LLM
# 2. LLM decides which tool to use
# 3. Agent executes the tool
# 4. Agent sends result back to LLM
# 5. LLM decides if done or needs more tools
# 6. Loop until task complete
```

## The Execution Loop (React Agent)

**ReAct = Reasoning + Acting**

```python
# Step 1: User gives request
user_input = "Calculate 5 + 3 and save to file"

# Step 2: Agent sends to LLM with tools available
# LLM receives:
# - Request: "Calculate 5 + 3 and save to file"
# - Available tools:
#   * add(a, b) - Add two numbers
#   * write_file(path, content) - Write to file
#   * ... (34 more tools)

# Step 3: LLM "thinks" and decides
# "I need to:
#  1. Use add(5, 3) to get result
#  2. Use write_file to save result"

# Step 4: Agent executes tool #1
result_1 = add(5, 3)  # Returns: 8

# Step 5: Agent sends result to LLM
# LLM receives: "add(5, 3) returned 8"

# Step 6: LLM decides next action
# "Now I'll write_file with content='8'"

# Step 7: Agent executes tool #2
result_2 = write_file(path="/tmp/result", content="8")

# Step 8: LLM sees both tasks done
# Generates response: "Done! Calculated 5 + 3 = 8 and saved to file"

# Step 9: Return to user
```

## Code Example: Complete Workflow

```python
from langchain_ollama import OllamaLLM
from langgraph.prebuilt import create_react_agent
from agent import create_agent

# Step 1: Create LLM
llm = OllamaLLM(model="phi:latest")

# Step 2: Create agent with tools
agent = create_agent(llm=llm)

# Step 3: User makes request
user_request = "Calculate the average of [10, 20, 30, 40, 50] and save to file /tmp/avg.txt"

# Step 4: Agent processes request
result = agent.run(user_request)

# What happens internally:
#
# 1. Agent.run() sends request to LLM with 36 tools available
#
# 2. LLM decides: "I need average() and write_file() tools"
#
# 3. Agent calls average([10, 20, 30, 40, 50])
#    Returns: 30
#
# 4. Agent tells LLM: "average() returned 30"
#
# 5. LLM decides: "Now save 30 to file"
#
# 6. Agent calls write_file("/tmp/avg.txt", "30")
#    Returns: "File written"
#
# 7. LLM sees task complete, generates response:
#    "I calculated the average of [10, 20, 30, 40, 50] which is 30,
#     and saved it to /tmp/avg.txt"
#
# 8. Return to user

print(result["output"])
# Output: "I calculated the average of [10, 20, 30, 40, 50] which is 30,
#          and saved it to /tmp/avg.txt"
```

## Tool Binding Explanation

**What does "bind_tools" mean?**

```python
# Without binding (what we have now):
llm = OllamaLLM(model="phi:latest")
# LLM only knows how to generate text
# It doesn't know about your tools

# With binding (what langgraph needs):
agent = create_react_agent(llm, tools)
# Agent internally "binds" tools to LLM
# Now LLM can:
# 1. See tool definitions
# 2. Decide which tool to call
# 3. Format tool calls correctly
# 4. Receive tool results
# 5. Generate final response

# Why OllamaLLM can't bind tools:
# - OllamaLLM is a basic LLM wrapper
# - It doesn't support tool calling protocol
# - Langgraph expects more advanced LLM features
```

## Our Fallback Solution

Since OllamaLLM doesn't support full tool binding, we:

1. **Create LLM directly** (OllamaLLM works fine)
2. **Skip langgraph** (doesn't work with OllamaLLM)
3. **Use tool-only mode** (instant, no LLM reasoning)
4. **OR direct LLM invocation** (simple text generation)

```python
# What we do instead:
llm = OllamaLLM(model="phi:latest")

# Option A: Tool-only (no LLM)
agent = create_agent(llm=None)
agent.execute_task("add", a=5, b=3)  # Returns: 8

# Option B: Direct LLM (simple text, no tool calling)
response = llm.invoke("What is 5 + 3?")  # Returns: "5 + 3 equals 8"

# Option C: Manual tool orchestration (you manage which tool to call)
user_input = "Calculate 5 + 3"
if "calculate" in user_input.lower():
    result = agent.execute_task("calculate", operation="add", a=5, b=3)
```

## Why Tool-Only Works Great

```
┌──────────────────┐
│  Tool-Only Mode  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────┐
│  You call tool directly       │
│  agent.execute_task(...)      │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  Execute function            │
│  Return result immediately   │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  Result to user              │
│  No LLM latency!             │
└──────────────────────────────┘

Benefits:
✓ Super fast (< 100ms)
✓ No LLM needed
✓ Predictable results
✓ Perfect for automation
✓ Great for BSUB jobs
```

## Full LLM + Tools (GPT-4/Claude)

With advanced models, the workflow is:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent

# Advanced LLM that DOES support tool binding
llm = ChatOpenAI(model="gpt-4")

# Create agent that DOES work
agent = create_react_agent(llm, tools)

# Now LLM can:
# 1. See all 36 tools
# 2. Decide which to use
# 3. Call multiple tools
# 4. Process results
# 5. Generate natural response

result = agent.invoke({"input": "Your request"})
# LLM does the smart orchestration!
```

## Summary

| Aspect | Description |
|--------|-------------|
| **User Request** | Natural language input |
| **LLM Role** | Understand + decide which tools to use |
| **Tools Role** | Execute specific functions |
| **Agent Role** | Orchestrate (LLM ↔ Tools) |
| **Output** | Natural language response |

**Our Setup:**
- ✓ LLM available (OllamaLLM/phi)
- ✓ 36 tools ready
- ✗ Advanced tool binding (OllamaLLM limitation)
- ✓ Tool-only mode (fast alternative)
- ✓ Direct LLM (simple text generation)

**Recommendation:**
Use **tool-only mode** for production pipelines - it's faster, more reliable, and perfect for your DIIA BSUB job! 🚀
