#!/usr/bin/env python3
"""
Initialize and run the Langchain Tool Agent with Model Farm (Azure OpenAI compatible)
Uses AzureChatOpenAI with proper tool binding support
"""

import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from agent import create_agent


def create_llmfarm_agent():
    """Create and return an agent with Model Farm LLM"""
    try:
        from langchain_openai import AzureChatOpenAI

        print(f"\nInitializing Model Farm (Azure OpenAI)...")
        print(f"  Endpoint: https://aoai-farm.bosch-temp.com")
        print(f"  Deployment: gpt-5-nano-2025-08-07")
        print(f"  Temperature: {Config.LLM_TEMPERATURE}")

        llm = AzureChatOpenAI(
    azure_endpoint="https://aoai-farm.bosch-temp.com/api",
    api_key=os.getenv("MODEL_FARM_API_KEY"),
    api_version="2025-04-01-preview",
    deployment_name="gpt-5-nano-2025-08-07",
    temperature=1   # ✅ FORCE THIS
)

        print("  ✓ Model Farm LLM initialized")

        agent = create_agent(llm=llm)
        print("✓ Agent created with LLM + Tools\n")

        return agent

    except ImportError:
        print("✗ langchain-openai not installed")
        print("  Install with: pip install langchain-openai")
        return None
    except Exception as e:
        print(f"✗ Failed to initialize agent: {e}")
        import traceback
        traceback.print_exc()
        return None


def interactive_mode(agent):
    """Run agent in interactive mode with full conversation display"""
    print("\n" + "="*60)
    print("INTERACTIVE MODE WITH MODEL FARM + TOOLS")
    print("="*60)
    print("Enter your requests below (type 'quit' to exit)")
    print("Type 'help' to see available tools\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() == 'quit':
                print("Goodbye!")
                break

            if user_input.lower() == 'help':
                agent.print_tools_info()
                continue

            if not user_input:
                continue

            result = agent.run(user_input)

            if result['success']:
                print(f"\nAI: {result['output']}\n")
            else:
                print(f"\n✗ Error: {result['error']}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Langchain Tool Agent with Model Farm (LLM + Tools)"
    )
    args = parser.parse_args()

    print("="*60)
    print("LANGCHAIN TOOL AGENT WITH MODEL FARM")
    print("="*60)
    print(f"Configuration:")
    print(f"  Model: gpt-5-nano-2025-08-07")
    print(f"  Endpoint: https://aoai-farm.bosch-temp.com")
    print(f"  Database: {Config.DATABASE_PATH}")
    print("="*60 + "\n")

    # Check API key
    if not os.getenv("MODEL_FARM_API_KEY"):
        print("✗ MODEL_FARM_API_KEY not set!")
        print("Set it using:")
        print('  $env:MODEL_FARM_API_KEY="your_api_key_here"')
        return

    # Create agent
    print("\n" + "="*60)
    print("INITIALIZING AGENT")
    print("="*60)

    agent = create_llmfarm_agent()
    if agent is None:
        print("Failed to create agent. Exiting.")
        return

    # Show tools
    agent.print_tools_info()

    # Start interactive mode
    interactive_mode(agent)


if __name__ == "__main__":
    main()