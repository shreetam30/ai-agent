"""
Example usage of the Langchain Tool Agent with Ollama LLM
No OpenAI API key required - uses local Ollama instance
"""

import os
from agent import create_agent
from config import Config


def example_with_ollama_llm():
    """Example using Ollama LLM (recommended - no API key needed)"""
    try:
        from langchain_ollama import OllamaLLM
        
        print("="*60)
        print("OLLAMA AGENT EXAMPLE")
        print("="*60)
        print(f"Connecting to Ollama at: {Config.OLLAMA_HOST}")
        print(f"Using model: {Config.LLM_MODEL}")
        print(f"Temperature: {Config.LLM_TEMPERATURE}")
        print("="*60 + "\n")
        
        # Initialize Ollama LLM (no API key required!)
        llm = OllamaLLM(
            model=Config.LLM_MODEL,
            base_url=Config.OLLAMA_HOST,
            temperature=Config.LLM_TEMPERATURE,
            num_predict=Config.LLM_MAX_TOKENS,
            top_k=40,
            top_p=0.9,
        )
        
        # Test connection
        print("Testing Ollama connection...")
        try:
            test_response = llm.invoke("Hello, are you working?")
            print(f"✓ Ollama is working!\n")
        except Exception as e:
            print(f"✗ Error connecting to Ollama: {e}")
            print(f"  Make sure Ollama is running at {Config.OLLAMA_HOST}")
            print(f"  Start Ollama with: ollama serve\n")
            return
        
        # Create agent with Ollama LLM
        agent = create_agent(llm=llm, verbose=True)
        
        # Show available tools
        agent.print_tools_info()
        
        # Example 1: Complex task with multiple steps
        print("\n\n" + "="*60)
        print("EXAMPLE 1: Complex Task with Multiple Steps")
        print("="*60)
        
        input_text = """
        Please perform the following tasks:
        1. Create a table called 'products' with columns: id (INTEGER PRIMARY KEY), 
           name (TEXT), price (REAL), quantity (INTEGER)
        2. Insert a sample product: name='Laptop', price=1299.99, quantity=5
        3. Calculate the total value of this product (price * quantity)
        4. Write the result to a file called '/tmp/product_report.txt'
        """
        
        result = agent.run(input_text)
        if result['success']:
            print(f"\n✓ Agent Response:\n{result['output']}")
        else:
            print(f"\n✗ Error: {result['error']}")
            
    except ImportError:
        print("Ollama dependencies not installed. Please run:")
        print("pip install langchain-ollama")
        print("\nAlso ensure Ollama is installed and running:")
        print("https://ollama.ai")


def example_without_llm():
    """Example using direct tool execution without LLM"""
    from agent import create_agent
    
    print("\n\n" + "="*60)
    print("EXAMPLE: Direct Tool Execution (No LLM Required)")
    print("="*60 + "\n")
    
    agent = create_agent(llm=None, verbose=True)
    
    # Show available tools
    agent.print_tools_info()
    
    # Example 1: Create database table
    print("\n\nStep 1: Create Products Table")
    print("-" * 60)
    result = agent.execute_task(
        "create_table",
        table_name="products",
        schema={
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "price": "REAL",
            "quantity": "INTEGER"
        }
    )
    print(f"✓ {result['result']}" if result['success'] else f"✗ {result['error']}")
    
    # Example 2: Insert multiple products
    print("\n\nStep 2: Insert Products")
    print("-" * 60)
    products = [
        {"name": "Laptop", "price": 1299.99, "quantity": 5},
        {"name": "Mouse", "price": 29.99, "quantity": 50},
        {"name": "Keyboard", "price": 79.99, "quantity": 30},
        {"name": "Monitor", "price": 399.99, "quantity": 10}
    ]
    
    result = agent.execute_task(
        "insert_record",
        table_name="products",
        record=products[0]
    )
    print(f"✓ Inserted first product" if result['success'] else f"✗ {result['error']}")
    
    # Example 3: Query database
    print("\n\nStep 3: Query Database")
    print("-" * 60)
    result = agent.execute_task(
        "query",
        query="SELECT * FROM products"
    )
    if result['success']:
        print("✓ Products in database:")
        for product in result['result']:
            print(f"  - {product}")
    else:
        print(f"✗ {result['error']}")
    
    # Example 4: Calculate statistics
    print("\n\nStep 4: Calculate Price Statistics")
    print("-" * 60)
    prices = [1299.99, 29.99, 79.99, 399.99]
    
    avg_price = agent.execute_task(
        "calculate",
        operation="average",
        numbers=prices
    )
    print(f"✓ Average price: ${avg_price['result']:.2f}" if avg_price['success'] else f"✗ {avg_price['error']}")
    
    # Example 5: Write results to file
    print("\n\nStep 5: Write Results to File")
    print("-" * 60)
    report_content = f"""
PRODUCT INVENTORY REPORT
========================

Products:
- Laptop: $1299.99 (5 units)
- Mouse: $29.99 (50 units)
- Keyboard: $79.99 (30 units)
- Monitor: $399.99 (10 units)

Statistics:
- Average Price: $452.49
- Total Value: $1809.96

Generated by: Langchain Tool Agent
"""
    
    result = agent.execute_task(
        "write_file",
        file_path="/tmp/product_report.txt",
        content=report_content
    )
    print(f"✓ {result['result']}" if result['success'] else f"✗ {result['error']}")


def example_json_operations():
    """Example of JSON file operations"""
    print("\n\n" + "="*60)
    print("EXAMPLE: JSON File Operations")
    print("="*60 + "\n")
    
    from agent import create_agent
    agent = create_agent(llm=None)
    
    # Write JSON
    print("Step 1: Write JSON Configuration")
    print("-" * 60)
    config = {
        "database": "agent.db",
        "tables": ["users", "products", "orders"],
        "settings": {
            "debug": True,
            "max_connections": 10,
            "timeout": 30
        }
    }
    
    result = agent.execute_task(
        "write_file",
        file_path="/tmp/config.json",
        content=str(config)
    )
    print(f"✓ Configuration written" if result['success'] else f"✗ {result['error']}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("LANGCHAIN TOOL-BASED AGENT EXAMPLES (OLLAMA)")
    print("="*60)
    
    # Run examples
    example_without_llm()
    example_json_operations()
    
    # Try Ollama example (recommended - no API key needed!)
    print("\n\nAttempting to connect to Ollama LLM...")
    try:
        example_with_ollama_llm()
    except Exception as e:
        print(f"\nSkipping Ollama example: {str(e)}")
        print("Make sure Ollama is running: ollama serve")
