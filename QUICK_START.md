# Quick Start Guide - Langchain Tool Agent

## Installation

```bash
# Navigate to the agent directory
cd /fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor/langchain_tools

# Install dependencies
pip install -r requirements.txt
```

## Running Examples

```bash
# Run comprehensive examples (no LLM required)
python examples.py

# Run the agent with demonstrations
python agent.py
```

## Basic Usage

### 1. Simple File Operations

```python
from langchain_tools import FileOperations

# Read a file
content = FileOperations.read_file("data.txt")

# Write a file
FileOperations.write_file("output.txt", "Hello, World!")

# List files
files = FileOperations.list_files("./data", "*.json")
```

### 2. Database Operations

```python
from langchain_tools import DatabaseOperations

db = DatabaseOperations("mydata.db")

# Create table
db.create_table("users", {
    "id": "INTEGER PRIMARY KEY",
    "name": "TEXT",
    "email": "TEXT"
})

# Insert data
db.insert_record("users", {
    "name": "Alice",
    "email": "alice@example.com"
})

# Query data
success, results = db.execute_query("SELECT * FROM users")
print(results)
```

### 3. Mathematical Operations

```python
from langchain_tools import MathCalculations

# Basic operations
result = MathCalculations.add(10, 5)  # 15
result = MathCalculations.multiply(4, 7)  # 28

# Aggregations
avg = MathCalculations.average([1, 2, 3, 4, 5])  # 3.0
median = MathCalculations.median([1, 2, 3, 4, 5])  # 3

# Statistics
std_dev = MathCalculations.standard_deviation([1, 2, 3, 4, 5])
```

### 4. Using the Agent

```python
from langchain_tools import create_agent

# Create agent
agent = create_agent(llm=None)

# File operations
result = agent.execute_task(
    "write_file",
    file_path="report.txt",
    content="Sales Report"
)

# Database operations
result = agent.execute_task(
    "create_table",
    table_name="products",
    schema={
        "id": "INTEGER PRIMARY KEY",
        "name": "TEXT",
        "price": "REAL"
    }
)

# Math operations
result = agent.execute_task(
    "calculate",
    operation="average",
    numbers=[100, 200, 300]
)

# Check results
if result['success']:
    print(f"Success: {result['result']}")
else:
    print(f"Error: {result['error']}")
```

## Common Tasks

### Task 1: Create and Query a Database

```python
from langchain_tools import create_agent

agent = create_agent(llm=None)

# 1. Create products table
agent.execute_task(
    "create_table",
    table_name="products",
    schema={
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "price": "REAL",
        "quantity": "INTEGER"
    }
)

# 2. Insert products
products = [
    {"name": "Laptop", "price": 999.99, "quantity": 10},
    {"name": "Mouse", "price": 29.99, "quantity": 50},
    {"name": "Keyboard", "price": 79.99, "quantity": 30}
]

for product in products:
    agent.execute_task("insert_record", table_name="products", record=product)

# 3. Query all products
result = agent.execute_task("query", query="SELECT * FROM products")
print(result['result'])

# 4. Calculate average price
prices = [999.99, 29.99, 79.99]
avg = agent.execute_task("calculate", operation="average", numbers=prices)
print(f"Average Price: ${avg['result']:.2f}")
```

### Task 2: Generate and Save Reports

```python
from langchain_tools import create_agent
from datetime import datetime

agent = create_agent(llm=None)

# Generate report
report = f"""
INVENTORY REPORT
================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Products:
1. Laptop - $999.99 (10 units)
2. Mouse - $29.99 (50 units)
3. Keyboard - $79.99 (30 units)

Total Inventory Value: $11,529.70
"""

# Save to file
agent.execute_task(
    "write_file",
    file_path="inventory_report.txt",
    content=report
)

# Save as JSON
import json
data = {
    "report_type": "inventory",
    "date": datetime.now().isoformat(),
    "total_products": 3,
    "total_value": 11529.70
}

agent.execute_task(
    "write_file",
    file_path="inventory_report.json",
    content=json.dumps(data, indent=2)
)
```

### Task 3: Data Analysis

```python
from langchain_tools import MathCalculations

# Sample data
sales_data = [1500, 1800, 1600, 2100, 1900, 2200, 1700]

# Calculate statistics
total = MathCalculations.sum_numbers(sales_data)
average = MathCalculations.average(sales_data)
median = MathCalculations.median(sales_data)
min_val = MathCalculations.min_number(sales_data)
max_val = MathCalculations.max_number(sales_data)
std_dev = MathCalculations.standard_deviation(sales_data)

print(f"Total: ${total}")
print(f"Average: ${average:.2f}")
print(f"Median: ${median:.2f}")
print(f"Min: ${min_val}")
print(f"Max: ${max_val}")
print(f"Std Dev: ${std_dev:.2f}")
```

## Testing

```bash
# Run all tests
python -m unittest test_agent.py

# Run specific test class
python -m unittest test_agent.TestFileOperations

# Run with verbose output
python -m unittest test_agent.py -v
```

## Configuration

Create a `.env` file for custom settings:

```env
DB_PATH=./my_data.db
BASE_FILE_PATH=./my_data
LLM_MODEL=gpt-4
AGENT_VERBOSE=true
```

Then load in your code:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Using with LLM (OpenAI)

```bash
# Install OpenAI
pip install langchain-openai
```

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tools import create_agent

load_dotenv()

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Create agent with LLM
agent = create_agent(llm=llm, verbose=True)

# Run complex task
result = agent.run("""
    Create a sales database table with columns for
    date, product, quantity, and price. Then insert
    some sample data and calculate the total revenue.
""")

print(result['output'])
```

## Available Tools Summary

### File Operations (8 tools)
- `read_file` - Read file contents
- `write_file` - Write to file
- `append_file` - Append to file
- `list_files` - List files with pattern
- `delete_file` - Delete file
- `copy_file` - Copy file
- `read_json` - Read JSON file
- `write_json` - Write JSON file

### Database Operations (9 tools)
- `create_table` - Create table
- `insert_record` - Insert single record
- `insert_records` - Insert multiple records
- `query_database` - Query data
- `update_database` - Update/delete data
- `get_table_schema` - Get table structure
- `list_tables` - List all tables
- `delete_records` - Delete records
- `drop_table` - Drop table

### Math Operations (19 tools)
- Basic: `add`, `subtract`, `multiply`, `divide`, `power`, `square_root`, `absolute`
- Aggregation: `sum`, `average`, `min`, `max`
- Statistics: `median`, `standard_deviation`, `variance`
- Number Theory: `factorial`, `gcd`, `lcm`
- Utility: `percentage`, `round`

## Troubleshooting

### Import Errors

```python
# Make sure you're in the correct directory
import sys
sys.path.insert(0, '/fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor/langchain_tools')

from agent import create_agent
```

### Database Locked Error

```python
# Use a different database path or ensure no other processes are using it
from langchain_tools import DatabaseOperations
db = DatabaseOperations("unique_db_name.db")
```

### File Permission Error

```python
# Check write permissions in your directory
import os
print(os.access("./data", os.W_OK))  # Should print True
```

## Next Steps

1. **Read Full Documentation**: See [README.md](README.md)
2. **Explore Examples**: Run `python examples.py`
3. **Run Tests**: Execute `python test_agent.py`
4. **Integrate with LLM**: Setup OpenAI API key and use with GPT models
5. **Extend Tools**: Add custom tools to the agent

## Support

For more information:
- Full documentation: [README.md](README.md)
- Examples: [examples.py](examples.py)
- API Reference: See docstrings in individual modules
- Testing: [test_agent.py](test_agent.py)
