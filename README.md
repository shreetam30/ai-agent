# Langchain Tool-Based Agent

A comprehensive Langchain agent integrated with file operations, database operations, and mathematical calculation tools.

## Overview

This package provides a powerful, extensible agent framework built on Langchain that combines:

1. **File Operations**: Read, write, copy, list, and manipulate files
2. **Database Operations**: SQLite database CRUD operations and queries
3. **Mathematical Calculations**: Statistical and mathematical operations

## Features

### File Operations
- `read_file`: Read file contents
- `write_file`: Write content to files
- `append_file`: Append content to existing files
- `list_files`: List files with pattern matching
- `delete_file`: Delete files
- `copy_file`: Copy files with directory creation
- `read_json`: Parse JSON files
- `write_json`: Write data as JSON

### Database Operations
- `create_table`: Create database tables with custom schemas
- `insert_record`: Insert single records
- `insert_records`: Batch insert multiple records
- `query_database`: Execute SELECT queries
- `update_database`: Execute UPDATE/INSERT/DELETE queries
- `get_table_schema`: Get table structure information
- `list_tables`: List all database tables
- `delete_records`: Delete records with conditions
- `drop_table`: Drop entire tables

### Mathematical Operations
- Basic: `add`, `subtract`, `multiply`, `divide`, `power`, `square_root`, `absolute`
- Aggregation: `sum`, `average`, `min`, `max`
- Statistics: `median`, `standard_deviation`, `variance`
- Number Theory: `factorial`, `gcd`, `lcm`
- Utility: `percentage`, `round`

## Installation

### Basic Installation

```bash
cd /fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor/langchain_tools
pip install -r requirements.txt
```

### Installation with OpenAI Support

```bash
pip install langchain-openai
```

## Configuration

### Environment Variables

Create a `.env` file in the agent directory:

```env
# Database configuration
DB_PATH=./agent.db

# File operations
BASE_FILE_PATH=./data
ALLOWED_EXTENSIONS=.txt,.json,.csv,.log,.md

# LLM configuration
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0
LLM_MAX_TOKENS=2000
OPENAI_API_KEY=your_api_key_here

# Agent settings
AGENT_VERBOSE=true
```

### Programmatic Configuration

```python
from langchain_tools.config import Config

Config.initialize(
    DATABASE_PATH="custom.db",
    AGENT_VERBOSE=True,
    LLM_MODEL="gpt-3.5-turbo"
)
```

## Usage

### Basic Usage (No LLM Required)

```python
from langchain_tools import create_agent

# Create agent without LLM
agent = create_agent(llm=None)

# Execute file operation
result = agent.execute_task(
    "write_file",
    file_path="/tmp/example.txt",
    content="Hello, World!"
)

# Execute database operation
result = agent.execute_task(
    "create_table",
    table_name="users",
    schema={
        "id": "INTEGER PRIMARY KEY",
        "name": "TEXT NOT NULL",
        "email": "TEXT"
    }
)

# Execute math operation
result = agent.execute_task(
    "calculate",
    operation="average",
    numbers=[10, 20, 30, 40, 50]
)
```

### Advanced Usage (With LLM)

```python
from langchain_openai import ChatOpenAI
from langchain_tools import create_agent

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create agent with LLM
agent = create_agent(llm=llm, verbose=True)

# Run complex tasks
result = agent.run("""
    Create a database table for products with columns:
    id (INTEGER PRIMARY KEY), name (TEXT), price (REAL)
    Then insert a sample product and calculate the average price.
""")

print(result['output'])
```

## Examples

### Example 1: File Operations

```python
from langchain_tools.file_operations import FileOperations

# Read a file
content = FileOperations.read_file("/path/to/file.txt")

# Write a file
FileOperations.write_file("/path/to/output.txt", "Content here")

# List files with pattern
files = FileOperations.list_files("./data", "*.json")

# JSON operations
data = FileOperations.read_json("config.json")
FileOperations.write_json("output.json", {"key": "value"})
```

### Example 2: Database Operations

```python
from langchain_tools.database_operations import get_db

db = get_db("products.db")

# Create table
success, msg = db.create_table("products", {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "name": "TEXT NOT NULL",
    "price": "REAL",
    "quantity": "INTEGER"
})

# Insert records
record = {
    "name": "Laptop",
    "price": 1299.99,
    "quantity": 5
}
success, msg = db.insert_record("products", record)

# Query data
success, results = db.execute_query("SELECT * FROM products WHERE price > 100")

# List tables
success, tables = db.list_tables()
```

### Example 3: Mathematical Operations

```python
from langchain_tools.math_operations import MathCalculations

# Basic operations
result = MathCalculations.add(5, 3)  # 8
result = MathCalculations.divide(10, 2)  # 5.0

# Aggregations
average = MathCalculations.average([1, 2, 3, 4, 5])  # 3.0
maximum = MathCalculations.max_number([5, 2, 8, 1])  # 8

# Statistics
std_dev = MathCalculations.standard_deviation([1, 2, 3, 4, 5])
variance = MathCalculations.variance([1, 2, 3, 4, 5])

# Number theory
gcd = MathCalculations.gcd(48, 18)  # 6
lcm = MathCalculations.lcm(12, 18)  # 36
```

### Example 4: Complex Workflow

```python
from langchain_tools import create_agent

agent = create_agent(llm=None)

# Step 1: Create table
agent.execute_task(
    "create_table",
    table_name="sales",
    schema={
        "id": "INTEGER PRIMARY KEY",
        "product": "TEXT",
        "amount": "REAL",
        "date": "TEXT"
    }
)

# Step 2: Insert records
records = [
    {"product": "Widget A", "amount": 100.50, "date": "2024-01-01"},
    {"product": "Widget B", "amount": 250.75, "date": "2024-01-02"},
    {"product": "Widget C", "amount": 175.25, "date": "2024-01-03"}
]

for record in records:
    agent.execute_task("insert_record", table_name="sales", record=record)

# Step 3: Calculate statistics
amounts = [100.50, 250.75, 175.25]
avg = agent.execute_task("calculate", operation="average", numbers=amounts)
total = agent.execute_task("calculate", operation="sum", numbers=amounts)

# Step 4: Write report
report = f"""
SALES REPORT
============
Total Sales: ${total['result']:.2f}
Average Sale: ${avg['result']:.2f}
"""

agent.execute_task("write_file", file_path="report.txt", content=report)
```

## Running Examples

```bash
# Run examples with demonstrations
python examples.py

# Run with output
python agent.py
```

## API Reference

### LangchainToolAgent

Main agent class for orchestrating tool execution.

**Methods:**

- `get_tools_info()`: Get grouped information about available tools
- `print_tools_info()`: Print tools to console
- `run(input_text)`: Run agent with LLM (requires LLM initialization)
- `execute_task(task_type, **kwargs)`: Direct task execution without LLM

**Properties:**

- `tools`: List of all available tools
- `agent`: The underlying agent instance
- `executor`: The agent executor

### FileOperations

Static methods for file handling:

- `read_file(file_path)`: Read file contents
- `write_file(file_path, content, append=False)`: Write to file
- `list_files(directory, pattern=None)`: List files
- `delete_file(file_path)`: Delete file
- `copy_file(source, destination)`: Copy file
- `read_json(file_path)`: Parse JSON
- `write_json(file_path, data)`: Write JSON

### DatabaseOperations

Database management class:

- `create_table(table_name, schema)`: Create table
- `insert_record(table_name, record)`: Insert single record
- `insert_records(table_name, records)`: Insert multiple records
- `execute_query(query, params=None)`: Execute SELECT query
- `execute_update(query, params=None)`: Execute UPDATE/INSERT/DELETE
- `get_table_info(table_name)`: Get table schema
- `list_tables()`: List all tables
- `delete_records(table_name, condition=None)`: Delete records
- `drop_table(table_name)`: Drop table

### MathCalculations

Static methods for mathematical operations:

- `add(a, b)`, `subtract(a, b)`, `multiply(a, b)`, `divide(a, b)`
- `power(base, exponent)`, `square_root(value)`, `absolute(value)`
- `sum_numbers(numbers)`, `average(numbers)`, `min_number(numbers)`, `max_number(numbers)`
- `factorial(n)`, `gcd(a, b)`, `lcm(a, b)`, `percentage(part, total)`
- `median(numbers)`, `standard_deviation(numbers)`, `variance(numbers)`
- `round_number(value, decimals=0)`

## Architecture

```
langchain_tools/
├── __init__.py                 # Package initialization
├── agent.py                    # Main agent class
├── file_operations.py          # File handling tools
├── database_operations.py      # Database tools
├── math_operations.py          # Math calculation tools
├── config.py                   # Configuration management
├── examples.py                 # Usage examples
├── requirements.txt            # Dependencies
└── README.md                   # Documentation
```

## Error Handling

All tools include comprehensive error handling:

```python
result = agent.execute_task(...)

if result['success']:
    print(f"Operation successful: {result['result']}")
else:
    print(f"Operation failed: {result['error']}")
```

## Logging

Configure logging to monitor agent operations:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

## Performance Considerations

- **Database**: Uses SQLite for local database operations
- **File Operations**: Supports up to 100MB files by default
- **Math Operations**: Uses 64-bit floating point precision
- **LLM Integration**: Supports streaming for large responses

## Limitations

- Database operations are synchronous
- File operations are limited to local filesystem
- Math operations use standard floating-point arithmetic
- LLM integration requires valid API key

## Contributing

To extend the agent with new tools:

1. Create a new module with tool definitions
2. Add Langchain `@tool` decorators
3. Import tools in `agent.py`
4. Add to `__init__.py` exports
5. Update documentation

## License

This project is provided as-is for development and testing purposes.

## Support

For issues and questions, refer to the Langchain documentation:
- https://python.langchain.com/
- https://python.langchain.com/docs/integrations/

## Version

Current version: 1.0.0
Last updated: 2024
