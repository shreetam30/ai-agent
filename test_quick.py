#!/usr/bin/env python3
"""Quick test of the agent with LLM + Tools"""

from langchain_ollama import ChatOllama
from config import Config
from agent import create_agent

print("Initializing ChatOllama...")
llm = ChatOllama(
    model=Config.LLM_MODEL,
    base_url=Config.OLLAMA_HOST,
    temperature=Config.LLM_TEMPERATURE,
)

print("Creating agent with LLM + Tools...")
agent = create_agent(llm=llm)

print("\n" + "="*60)
print("TEST: Calculate 5 + 3")
print("="*60)
result = agent.run("Calculate 5 plus 3")
