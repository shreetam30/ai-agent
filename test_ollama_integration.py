#!/usr/bin/env python3
"""
Test script for Ollama Agent integration
Verifies all components are working correctly
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import langchain
        print("  ✓ langchain")
        
        import langchain_community
        print("  ✓ langchain_community")
        
        import numpy
        print("  ✓ numpy")
        
        import pandas
        print("  ✓ pandas")
        
        print("  ✓ All core imports successful\n")
        return True
    except ImportError as e:
        print(f"  ✗ Import error: {e}\n")
        return False


def test_config():
    """Test configuration loading"""
    print("Testing configuration...")
    try:
        from config import Config
        
        print(f"  LLM Provider: {Config.LLM_PROVIDER}")
        print(f"  Model: {Config.LLM_MODEL}")
        print(f"  Ollama Host: {Config.OLLAMA_HOST}")
        print(f"  Temperature: {Config.LLM_TEMPERATURE}")
        print(f"  Database: {Config.DATABASE_PATH}")
        print("  ✓ Configuration loaded\n")
        return True
    except Exception as e:
        print(f"  ✗ Config error: {e}\n")
        return False


def test_ollama_connection():
    """Test Ollama connectivity"""
    print("Testing Ollama connection...")
    try:
        import requests
        from config import Config
        
        response = requests.get(
            f"{Config.OLLAMA_HOST}/api/version",
            timeout=5
        )
        if response.status_code == 200:
            print(f"  ✓ Connected to Ollama at {Config.OLLAMA_HOST}")
            print(f"  ✓ Response: {response.json()}\n")
            return True
        else:
            print(f"  ✗ Ollama returned status {response.status_code}\n")
            return False
    except Exception as e:
        print(f"  ✗ Cannot connect to Ollama: {e}")
        print(f"     Make sure Ollama is running: ollama serve &\n")
        return False


def test_model_available():
    """Test if configured model is available"""
    print("Testing model availability...")
    try:
        import requests
        from config import Config
        
        response = requests.get(
            f"{Config.OLLAMA_HOST}/api/tags",
            timeout=5
        )
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [m['name'] for m in models]
            
            if model_names:
                print(f"  Available models:")
                for name in model_names:
                    marker = "✓" if name == Config.LLM_MODEL else " "
                    print(f"    {marker} {name}")
                
                if Config.LLM_MODEL in model_names:
                    print(f"\n  ✓ Model '{Config.LLM_MODEL}' is available\n")
                    return True
                else:
                    print(f"\n  ✗ Model '{Config.LLM_MODEL}' not found")
                    print(f"     Download with: ollama pull {Config.LLM_MODEL}\n")
                    return False
            else:
                print(f"  ✗ No models found in Ollama")
                print(f"     Download with: ollama pull mistral:latest\n")
                return False
        else:
            print(f"  ✗ Cannot query models\n")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}\n")
        return False


def test_agent_creation():
    """Test agent creation without LLM"""
    print("Testing agent creation...")
    try:
        from agent import create_agent
        
        agent = create_agent(llm=None)
        print("  ✓ Agent created (tools-only mode)")
        
        tools_info = agent.get_tools_info()
        total_tools = sum(len(v) for v in tools_info.values())
        print(f"  ✓ Loaded {total_tools} tools")
        print(f"    - File operations: {len(tools_info['file_operations'])}")
        print(f"    - Database operations: {len(tools_info['database_operations'])}")
        print(f"    - Math operations: {len(tools_info['math_operations'])}\n")
        return True
    except Exception as e:
        print(f"  ✗ Agent creation error: {e}\n")
        return False


def test_tools():
    """Test basic tool execution"""
    print("Testing tools...")
    try:
        from agent import create_agent
        
        agent = create_agent(llm=None)
        
        # Test math tool
        result = agent.execute_task("calculate", operation="add", a=5, b=3)
        if result['success'] and result['result'] == 8:
            print("  ✓ Math tool (add): 5 + 3 = 8")
        else:
            print(f"  ✗ Math tool failed: {result}")
            return False
        
        # Test file operations
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test.txt")
            content = "Hello, Agent!"
            
            # Write
            result = agent.execute_task(
                "write_file",
                file_path=test_file,
                content=content
            )
            if not result['success']:
                print(f"  ✗ Write file failed: {result}")
                return False
            print("  ✓ File operations (write): File written")
            
            # Read
            result = agent.execute_task("read_file", file_path=test_file)
            if result['success'] and result['result'] == content:
                print("  ✓ File operations (read): File read correctly")
            else:
                print(f"  ✗ Read file failed: {result}")
                return False
        
        print()
        return True
    except Exception as e:
        print(f"  ✗ Tool error: {e}\n")
        return False


def test_ollama_llm():
    """Test Ollama LLM integration"""
    print("Testing Ollama LLM...")
    try:
        from langchain_ollama import OllamaLLM
        from config import Config
        
        llm = OllamaLLM(
            model=Config.LLM_MODEL,
            base_url=Config.OLLAMA_HOST,
            temperature=Config.LLM_TEMPERATURE
        )
        
        print("  ✓ OllamaLLM initialized")
        
        # Test simple response
        response = llm.invoke("Say 'Hello' and nothing else")
        print(f"  ✓ LLM response: {response[:50]}...")
        
        # Test with agent
        from agent import create_agent
        agent = create_agent(llm=llm)
        print("  ✓ Agent created with Ollama LLM\n")
        return True
        
    except ImportError:
        print("  ⚠ langchain-ollama not installed")
        print("    Install with: pip install langchain-ollama")
        print("    (Optional - tools-only mode still works)\n")
        return True  # Not a failure
    except Exception as e:
        print(f"  ✗ LLM error: {e}\n")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("OLLAMA AGENT TEST SUITE")
    print("="*60 + "\n")
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Ollama Connection", test_ollama_connection()))
    results.append(("Model Availability", test_model_available()))
    results.append(("Agent Creation", test_agent_creation()))
    results.append(("Tool Execution", test_tools()))
    results.append(("Ollama LLM", test_ollama_llm()))
    
    # Print summary
    print("="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("="*60)
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All systems operational!\n")
        return 0
    else:
        print("✗ Some tests failed. See above for details.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
