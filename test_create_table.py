#!/usr/bin/env python3
"""
Test if table creation actually works
"""

from agent import create_agent

# Create agent without LLM (tools-only)
agent = create_agent(llm=None, verbose=True)

print("="*60)
print("TEST: Creating a table")
print("="*60)

# Execute the task directly
result = agent.execute_task(
    "create_table",
    table_name="users",
    schema={
        "id": "INTEGER PRIMARY KEY",
        "name": "TEXT",
        "email": "TEXT"
    }
)

print(f"\nSuccess: {result['success']}")
print(f"Result: {result['result']}")

# Verify by querying
if result['success']:
    print("\n" + "="*60)
    print("TEST: Querying the table")
    print("="*60)
    
    query_result = agent.execute_task(
        "query",
        query="SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
    )
    
    print(f"\nSuccess: {query_result['success']}")
    print(f"Result: {query_result['result']}")
