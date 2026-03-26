"""
Advanced Usage and Troubleshooting Guide for Langchain Tool Agent
"""

# Advanced Usage Examples

## 1. Building Complex Workflows

### Multi-Step Data Processing Pipeline

```python
from langchain_tools import create_agent
import json

# Create agent
agent = create_agent(llm=None)

# Step 1: Create a database for tracking
print("Setting up database...")
agent.execute_task(
    "create_table",
    table_name="sales",
    schema={
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "product": "TEXT NOT NULL",
        "amount": "REAL NOT NULL",
        "quantity": "INTEGER",
        "timestamp": "TEXT"
    }
)

# Step 2: Generate sample data and insert
print("Inserting sales data...")
sales_data = [
    {"product": "Laptop", "amount": 1200.00, "quantity": 5, "timestamp": "2024-01-01"},
    {"product": "Mouse", "amount": 25.00, "quantity": 50, "timestamp": "2024-01-02"},
    {"product": "Keyboard", "amount": 75.00, "quantity": 30, "timestamp": "2024-01-03"},
]

for sale in sales_data:
    agent.execute_task("insert_record", table_name="sales", record=sale)

# Step 3: Query and analyze
print("Analyzing data...")
result = agent.execute_task("query", query="SELECT * FROM sales")
sales = result['result']

# Step 4: Calculate statistics
amounts = [sale['amount'] for sale in sales]
total = agent.execute_task("calculate", operation="sum", numbers=amounts)
average = agent.execute_task("calculate", operation="average", numbers=amounts)

# Step 5: Generate report
report = f"""
SALES ANALYSIS REPORT
====================
Total Sales: ${total['result']:.2f}
Average Sale: ${average['result']:.2f}
Number of Transactions: {len(sales)}

Details:
"""

for sale in sales:
    revenue = sale['amount'] * sale['quantity']
    report += f"\n- {sale['product']}: ${revenue:.2f} ({sale['quantity']} units)"

# Step 6: Save report
agent.execute_task("write_file", file_path="sales_report.txt", content=report)

print("Report generated successfully!")
```

### Real-Time Data Processing

```python
from langchain_tools import create_agent
import json
from datetime import datetime

agent = create_agent(llm=None)

class DataProcessor:
    def __init__(self):
        self.db_path = "streaming_data.db"
        self.setup_database()
    
    def setup_database(self):
        """Initialize database schema"""
        agent.execute_task(
            "create_table",
            table_name="events",
            schema={
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "event_type": "TEXT",
                "timestamp": "TEXT",
                "value": "REAL",
                "processed": "BOOLEAN DEFAULT 0"
            }
        )
    
    def process_event(self, event_type, value):
        """Process incoming event"""
        record = {
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "value": value
        }
        
        agent.execute_task(
            "insert_record",
            table_name="events",
            record=record
        )
    
    def get_statistics(self):
        """Get statistics for current events"""
        result = agent.execute_task(
            "query",
            query="SELECT value FROM events WHERE processed = 0"
        )
        
        values = [event['value'] for event in result['result']]
        
        if values:
            stats = {
                'count': len(values),
                'sum': agent.execute_task("calculate", operation="sum", numbers=values)['result'],
                'average': agent.execute_task("calculate", operation="average", numbers=values)['result'],
                'min': agent.execute_task("calculate", operation="min", numbers=values)['result'],
                'max': agent.execute_task("calculate", operation="max", numbers=values)['result'],
            }
            return stats
        return None
    
    def generate_report(self):
        """Generate current statistics report"""
        stats = self.get_statistics()
        
        if stats:
            report = f"""
EVENT STATISTICS REPORT
======================
Generated: {datetime.now().isoformat()}

Events Processed: {stats['count']}
Total Value: {stats['sum']:.2f}
Average Value: {stats['average']:.2f}
Min Value: {stats['min']:.2f}
Max Value: {stats['max']:.2f}
"""
            
            agent.execute_task(
                "write_file",
                file_path="event_stats.txt",
                content=report
            )
            return report
        return None

# Usage
processor = DataProcessor()

# Simulate events
for i in range(5):
    processor.process_event("sensor_reading", 10 + i * 2.5)

# Generate report
report = processor.generate_report()
print(report)
```

## 2. Custom Tool Creation and Registration

```python
from langchain.tools import tool
from langchain_tools import create_agent, LangchainToolAgent
from typing import List

# Create custom tools
@tool
def custom_text_analysis(text: str) -> dict:
    """Analyze text and return statistics"""
    return {
        "length": len(text),
        "word_count": len(text.split()),
        "char_count": len(text.replace(" ", "")),
        "average_word_length": len(text.replace(" ", "")) / len(text.split())
    }

@tool
def custom_data_transform(data: List[float], operation: str) -> List[float]:
    """Transform data with custom operations"""
    if operation == "double":
        return [x * 2 for x in data]
    elif operation == "square":
        return [x ** 2 for x in data]
    elif operation == "normalize":
        max_val = max(data)
        return [x / max_val for x in data]
    return data

# Create agent and extend with custom tools
class ExtendedAgent(LangchainToolAgent):
    def __init__(self, llm=None, verbose=True):
        super().__init__(llm, verbose)
        self.custom_tools = [custom_text_analysis, custom_data_transform]
    
    def get_all_tools(self):
        """Get both standard and custom tools"""
        return self.tools + self.custom_tools

# Usage
agent = ExtendedAgent(llm=None, verbose=True)

# Use custom tools
result = custom_text_analysis("The quick brown fox jumps over the lazy dog")
print(f"Text Analysis: {result}")

result = custom_data_transform([1, 2, 3, 4, 5], "normalize")
print(f"Normalized Data: {result}")
```

## 3. Error Handling and Retry Logic

```python
from langchain_tools import create_agent
import time
from typing import Dict, Any

class RobustAgent:
    def __init__(self, max_retries=3, retry_delay=1):
        self.agent = create_agent(llm=None)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.error_log = []
    
    def execute_with_retry(self, task_type: str, **kwargs) -> Dict[str, Any]:
        """Execute task with retry logic"""
        for attempt in range(self.max_retries):
            try:
                result = self.agent.execute_task(task_type, **kwargs)
                
                if result['success']:
                    return result
                else:
                    self.error_log.append({
                        'attempt': attempt + 1,
                        'task': task_type,
                        'error': result.get('error')
                    })
                    
                    if attempt < self.max_retries - 1:
                        print(f"Attempt {attempt + 1} failed. Retrying in {self.retry_delay}s...")
                        time.sleep(self.retry_delay)
            
            except Exception as e:
                self.error_log.append({
                    'attempt': attempt + 1,
                    'task': task_type,
                    'exception': str(e)
                })
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        return {
            'success': False,
            'error': f'Failed after {self.max_retries} attempts',
            'log': self.error_log
        }
    
    def get_error_report(self):
        """Get error report"""
        return self.error_log

# Usage
robust_agent = RobustAgent(max_retries=3, retry_delay=1)

# Execute with retry
result = robust_agent.execute_with_retry(
    "write_file",
    file_path="/tmp/test_retry.txt",
    content="Testing retry logic"
)

print(result)
```

## 4. Batch Processing Large Datasets

```python
from langchain_tools import create_agent
import csv
from typing import List, Dict

class BatchProcessor:
    def __init__(self, batch_size=100):
        self.agent = create_agent(llm=None)
        self.batch_size = batch_size
    
    def process_csv_file(self, input_file: str, table_name: str) -> Dict:
        """Process CSV file and load into database"""
        
        # Read CSV
        data = []
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        
        print(f"Read {len(data)} rows from {input_file}")
        
        # Infer schema from first row
        first_row = data[0]
        schema = {}
        for key in first_row.keys():
            # Simple type inference
            try:
                float(first_row[key])
                schema[key] = "REAL"
            except:
                schema[key] = "TEXT"
        
        schema['id'] = "INTEGER PRIMARY KEY AUTOINCREMENT"
        
        # Create table
        self.agent.execute_task(
            "create_table",
            table_name=table_name,
            schema=schema
        )
        
        print(f"Created table '{table_name}' with schema: {schema}")
        
        # Process in batches
        stats = {'total': len(data), 'batches': 0, 'processed': 0}
        
        for i in range(0, len(data), self.batch_size):
            batch = data[i:i+self.batch_size]
            
            result = self.agent.execute_task(
                "insert_records",
                table_name=table_name,
                records=batch
            )
            
            if result['success']:
                stats['processed'] += len(batch)
                stats['batches'] += 1
                print(f"Batch {stats['batches']}: Inserted {len(batch)} records")
        
        return stats

# Usage
processor = BatchProcessor(batch_size=50)

# Create sample CSV
sample_data = """name,age,salary
John Doe,30,50000
Jane Smith,28,55000
Bob Johnson,35,60000
Alice Brown,32,58000
Charlie Wilson,29,52000"""

with open('/tmp/employees.csv', 'w') as f:
    f.write(sample_data)

# Process CSV
stats = processor.process_csv_file('/tmp/employees.csv', 'employees')
print(f"Processing complete: {stats}")
```

---

# Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: Database Locked Error

**Error Message**:
```
sqlite3.OperationalError: database is locked
```

**Causes**:
- Multiple processes accessing the same database
- Transaction not committed properly
- Database file permissions issue

**Solutions**:
```python
# Use different database paths for different processes
from langchain_tools import DatabaseOperations

# Solution 1: Use unique database names
db1 = DatabaseOperations("process1.db")
db2 = DatabaseOperations("process2.db")

# Solution 2: Increase timeout
import sqlite3
sqlite3.connect("agent.db", timeout=30)

# Solution 3: Check file permissions
import os
print(os.access("agent.db", os.R_OK | os.W_OK))
```

### Issue 2: File Not Found Errors

**Error Message**:
```
Error reading file: [Errno 2] No such file or directory: 'data.txt'
```

**Solutions**:
```python
from langchain_tools import FileOperations
from pathlib import Path

# Solution 1: Create parent directories
Path("path/to/directory").mkdir(parents=True, exist_ok=True)

# Solution 2: Verify file exists before reading
import os
if os.path.exists("file.txt"):
    content = FileOperations.read_file("file.txt")

# Solution 3: Use absolute paths
from pathlib import Path
abs_path = str(Path("file.txt").absolute())
```

### Issue 3: Division by Zero

**Error Message**:
```
ValueError: Cannot divide by zero
```

**Solution**:
```python
from langchain_tools import MathCalculations

# Check before dividing
divisor = 0
if divisor != 0:
    result = MathCalculations.divide(10, divisor)
else:
    result = float('inf')  # or handle as needed
```

### Issue 4: JSON Decode Error

**Error Message**:
```
json.JSONDecodeError: Expecting value: line 1 column 1
```

**Solutions**:
```python
from langchain_tools import FileOperations
import json

# Solution 1: Validate JSON before reading
try:
    data = FileOperations.read_json("config.json")
except json.JSONDecodeError:
    print("Invalid JSON file")

# Solution 2: Check file contents
with open("config.json") as f:
    content = f.read()
    print(f"File content: {content}")

# Solution 3: Use error result
result = FileOperations.read_json("config.json")
if "error" in result:
    print(f"Error: {result['error']}")
```

### Issue 5: Import Errors

**Error Message**:
```
ModuleNotFoundError: No module named 'langchain_tools'
```

**Solutions**:
```python
# Solution 1: Add path to sys.path
import sys
sys.path.insert(0, '/fs/scratch/Ban_EHM_VoiceSolution/ollama_ccm2kor/langchain_tools')

from agent import create_agent

# Solution 2: Install as package
# In langchain_tools directory, run:
# pip install -e .

# Solution 3: Verify installation
import langchain_tools
print(langchain_tools.__version__)
```

### Issue 6: Permission Denied

**Error Message**:
```
PermissionError: [Errno 13] Permission denied
```

**Solutions**:
```python
import os
import stat

# Check permissions
file_path = "test.txt"
print(os.access(file_path, os.R_OK))  # Read permission
print(os.access(file_path, os.W_OK))  # Write permission

# Fix permissions
os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)

# Create files in writable directory
import tempfile
temp_dir = tempfile.gettempdir()
test_file = os.path.join(temp_dir, "test.txt")
```

---

## Performance Optimization Tips

### Tip 1: Use Batch Operations
```python
# Slow: Insert one by one
for record in records:
    agent.execute_task("insert_record", table_name="users", record=record)

# Fast: Insert as batch
agent.execute_task("insert_records", table_name="users", records=records)
```

### Tip 2: Use Appropriate Data Types
```python
# Bad: Everything as TEXT
schema = {"id": "TEXT", "age": "TEXT", "price": "TEXT"}

# Good: Use appropriate types
schema = {
    "id": "INTEGER PRIMARY KEY",
    "age": "INTEGER",
    "price": "REAL",
    "name": "TEXT"
}
```

### Tip 3: Index Frequently Queried Columns
```python
from langchain_tools import DatabaseOperations

db = DatabaseOperations("mydata.db")

# Create index for faster queries
db.execute_update("CREATE INDEX idx_user_email ON users(email)")
```

### Tip 4: Use Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_database_query(query: str):
    from langchain_tools import DatabaseOperations
    db = DatabaseOperations("cache.db")
    success, results = db.execute_query(query)
    return results
```

---

## Logging and Debugging

### Enable Detailed Logging
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)

# Get logger
logger = logging.getLogger(__name__)
logger.info("Agent initialized")
```

### Debug Mode
```python
from langchain_tools import create_agent

# Enable verbose logging
agent = create_agent(llm=None, verbose=True)

# Execute task with debugging
result = agent.execute_task(
    "write_file",
    file_path="debug.txt",
    content="Debug content"
)

# Print full result
import json
print(json.dumps(result, indent=2))
```

---

## Performance Benchmarking

```python
import time
from langchain_tools import create_agent

agent = create_agent(llm=None)

# Benchmark database operations
def benchmark_inserts(n_records=1000):
    start = time.time()
    
    records = [
        {"name": f"User{i}", "email": f"user{i}@example.com"}
        for i in range(n_records)
    ]
    
    agent.execute_task(
        "insert_records",
        table_name="benchmark_users",
        records=records
    )
    
    elapsed = time.time() - start
    per_sec = n_records / elapsed
    
    print(f"Inserted {n_records} records in {elapsed:.2f}s ({per_sec:.0f} records/sec)")

benchmark_inserts()
```

---

## Best Practices

1. **Always use error checking**
   ```python
   result = agent.execute_task(...)
   if result['success']:
       # process result
   else:
       # handle error
   ```

2. **Use context managers for files**
   ```python
   with open('file.txt', 'r') as f:
       content = f.read()
   ```

3. **Validate input data**
   ```python
   if not isinstance(record, dict):
       raise ValueError("Record must be a dictionary")
   ```

4. **Use meaningful logging**
   ```python
   logger.info(f"Processing {len(records)} records")
   logger.error(f"Failed to process: {error_message}")
   ```

5. **Clean up resources**
   ```python
   # Close connections explicitly
   db.conn.close() if hasattr(db, 'conn') else None
   ```
