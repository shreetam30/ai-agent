#!/usr/bin/env python3
"""Test the updated agent with LLM + Tools"""

from langchain_ollama import ChatOllama
from config import Config
from agent import create_agent

# Initialize ChatOllama
print("Initializing ChatOllama...")
llm = ChatOllama(
    model=Config.LLM_MODEL,
    base_url=Config.OLLAMA_HOST,
    temperature=Config.LLM_TEMPERATURE,
)

# Create agent
print("Creating agent with LLM + Tools...")
agent = create_agent(llm=llm)

# Test 1: Create a file
print("\n" + "="*60)
print("TEST 1: Create a file")
print("="*60)
result = agent.run("Create a file called hello.txt with the content 'Hello from Ollama!'")

# Test 2: Math calculation
print("\n" + "="*60)
print("TEST 2: Math calculation")
print("="*60)
result = agent.run("Calculate the sum of 10 and 20")

# Test 3: Create a database table
print("\n" + "="*60)
print("TEST 3: Create a database table")
print("="*60)
result = agent.run("Create a table called products with columns: id INTEGER PRIMARY KEY, name TEXT, price REAL")
    
    def test_list_files(self):
        """Test listing files"""
        FileOperations.write_file(self.test_file, "test")
        os.makedirs(os.path.join(self.test_dir, "subdir"), exist_ok=True)
        
        files = FileOperations.list_files(self.test_dir)
        self.assertGreater(len(files), 0)
    
    def test_copy_file(self):
        """Test copying files"""
        content = "Original content"
        FileOperations.write_file(self.test_file, content)
        
        dest = os.path.join(self.test_dir, "copy.txt")
        FileOperations.copy_file(self.test_file, dest)
        
        result = FileOperations.read_file(dest)
        self.assertEqual(result, content)
    
    def test_delete_file(self):
        """Test deleting files"""
        FileOperations.write_file(self.test_file, "test")
        self.assertTrue(os.path.exists(self.test_file))
        
        FileOperations.delete_file(self.test_file)
        self.assertFalse(os.path.exists(self.test_file))
    
    def test_json_operations(self):
        """Test JSON read/write"""
        data = {"name": "test", "value": 123, "nested": {"key": "value"}}
        FileOperations.write_json(self.test_json, data)
        
        result = FileOperations.read_json(self.test_json)
        self.assertEqual(result, data)


class TestDatabaseOperations(unittest.TestCase):
    """Test database operation tools"""
    
    def setUp(self):
        """Set up test database"""
        self.test_db = os.path.join(tempfile.gettempdir(), "test_agent.db")
        self.db = DatabaseOperations(self.test_db)
    
    def tearDown(self):
        """Clean up test database"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_create_table(self):
        """Test creating tables"""
        success, msg = self.db.create_table("users", {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "email": "TEXT"
        })
        self.assertTrue(success)
        
        success, tables = self.db.list_tables()
        self.assertIn("users", tables)
    
    def test_insert_record(self):
        """Test inserting records"""
        self.db.create_table("users", {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "email": "TEXT"
        })
        
        success, msg = self.db.insert_record("users", {
            "name": "John Doe",
            "email": "john@example.com"
        })
        self.assertTrue(success)
    
    def test_insert_records(self):
        """Test batch insert"""
        self.db.create_table("users", {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "email": "TEXT"
        })
        
        records = [
            {"name": "John", "email": "john@example.com"},
            {"name": "Jane", "email": "jane@example.com"},
            {"name": "Bob", "email": "bob@example.com"}
        ]
        
        success, msg = self.db.insert_records("users", records)
        self.assertTrue(success)
        self.assertIn("3", msg)
    
    def test_query_database(self):
        """Test querying data"""
        self.db.create_table("users", {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "email": "TEXT"
        })
        
        self.db.insert_record("users", {
            "name": "John",
            "email": "john@example.com"
        })
        
        success, results = self.db.execute_query("SELECT * FROM users")
        self.assertTrue(success)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "John")
    
    def test_get_table_schema(self):
        """Test getting table schema"""
        self.db.create_table("products", {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT NOT NULL",
            "price": "REAL"
        })
        
        success, schema = self.db.get_table_info("products")
        self.assertTrue(success)
        self.assertIn("id", schema)
        self.assertIn("name", schema)
        self.assertIn("price", schema)
    
    def test_delete_records(self):
        """Test deleting records"""
        self.db.create_table("users", {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT"
        })
        
        self.db.insert_record("users", {"name": "John"})
        success, results = self.db.execute_query("SELECT COUNT(*) as count FROM users")
        self.assertEqual(results[0]["count"], 1)
        
        self.db.delete_records("users", "name = 'John'")
        success, results = self.db.execute_query("SELECT COUNT(*) as count FROM users")
        self.assertEqual(results[0]["count"], 0)
    
    def test_drop_table(self):
        """Test dropping tables"""
        self.db.create_table("temp", {"id": "INTEGER PRIMARY KEY"})
        
        success, msg = self.db.drop_table("temp")
        self.assertTrue(success)
        
        success, tables = self.db.list_tables()
        self.assertNotIn("temp", tables)


class TestMathOperations(unittest.TestCase):
    """Test mathematical operation tools"""
    
    def test_basic_operations(self):
        """Test basic arithmetic"""
        self.assertEqual(MathCalculations.add(5, 3), 8)
        self.assertEqual(MathCalculations.subtract(10, 3), 7)
        self.assertEqual(MathCalculations.multiply(4, 5), 20)
        self.assertEqual(MathCalculations.divide(10, 2), 5.0)
    
    def test_power_and_root(self):
        """Test power and square root"""
        self.assertEqual(MathCalculations.power(2, 3), 8)
        self.assertEqual(MathCalculations.square_root(16), 4.0)
    
    def test_absolute(self):
        """Test absolute value"""
        self.assertEqual(MathCalculations.absolute(-5), 5)
        self.assertEqual(MathCalculations.absolute(5), 5)
    
    def test_aggregations(self):
        """Test aggregation functions"""
        numbers = [1, 2, 3, 4, 5]
        
        self.assertEqual(MathCalculations.sum_numbers(numbers), 15)
        self.assertEqual(MathCalculations.average(numbers), 3.0)
        self.assertEqual(MathCalculations.min_number(numbers), 1)
        self.assertEqual(MathCalculations.max_number(numbers), 5)
    
    def test_factorial(self):
        """Test factorial"""
        self.assertEqual(MathCalculations.factorial(0), 1)
        self.assertEqual(MathCalculations.factorial(5), 120)
    
    def test_gcd_lcm(self):
        """Test GCD and LCM"""
        self.assertEqual(MathCalculations.gcd(12, 8), 4)
        self.assertEqual(MathCalculations.lcm(12, 8), 24)
    
    def test_percentage(self):
        """Test percentage calculation"""
        result = MathCalculations.percentage(25, 100)
        self.assertEqual(result, 25.0)
    
    def test_median(self):
        """Test median"""
        self.assertEqual(MathCalculations.median([1, 2, 3, 4, 5]), 3)
        self.assertEqual(MathCalculations.median([1, 2, 3, 4]), 2.5)
    
    def test_standard_deviation(self):
        """Test standard deviation"""
        numbers = [1, 2, 3, 4, 5]
        std_dev = MathCalculations.standard_deviation(numbers)
        self.assertGreater(std_dev, 0)
    
    def test_variance(self):
        """Test variance"""
        numbers = [1, 2, 3, 4, 5]
        variance = MathCalculations.variance(numbers)
        self.assertGreater(variance, 0)
    
    def test_round(self):
        """Test rounding"""
        self.assertEqual(MathCalculations.round_number(3.14159, 2), 3.14)
        self.assertEqual(MathCalculations.round_number(3.5), 4.0)


class TestLangchainAgent(unittest.TestCase):
    """Test the main Langchain Agent"""
    
    def setUp(self):
        """Set up agent"""
        self.agent = create_agent(llm=None, verbose=False)
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.tools)
        self.assertGreater(len(self.agent.tools), 0)
    
    def test_get_tools_info(self):
        """Test getting tools information"""
        tools_info = self.agent.get_tools_info()
        
        self.assertIn("file_operations", tools_info)
        self.assertIn("database_operations", tools_info)
        self.assertIn("math_operations", tools_info)
        
        self.assertGreater(len(tools_info["file_operations"]), 0)
        self.assertGreater(len(tools_info["database_operations"]), 0)
        self.assertGreater(len(tools_info["math_operations"]), 0)
    
    def test_execute_file_task(self):
        """Test executing file task"""
        test_file = os.path.join(self.test_dir, "test.txt")
        
        result = self.agent.execute_task(
            "write_file",
            file_path=test_file,
            content="Test content"
        )
        
        self.assertTrue(result['success'])
        self.assertTrue(os.path.exists(test_file))
    
    def test_execute_database_task(self):
        """Test executing database task"""
        test_db = os.path.join(self.test_dir, "test.db")
        
        result = self.agent.execute_task(
            "create_table",
            table_name="test_table",
            schema={"id": "INTEGER PRIMARY KEY", "value": "TEXT"}
        )
        
        self.assertTrue(result['success'])
    
    def test_execute_math_task(self):
        """Test executing math task"""
        result = self.agent.execute_task(
            "calculate",
            operation="average",
            numbers=[10, 20, 30, 40, 50]
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['result'], 30)


class TestConfiguration(unittest.TestCase):
    """Test configuration"""
    
    def test_config_get(self):
        """Test getting configuration"""
        config = Config.get_config()
        self.assertIsInstance(config, dict)
        self.assertIn("DATABASE_PATH", config)
        self.assertIn("LLM_MODEL", config)
    
    def test_config_initialize(self):
        """Test initializing configuration"""
        original_value = Config.LLM_MODEL
        
        Config.initialize(LLM_MODEL="test-model")
        self.assertEqual(Config.LLM_MODEL, "test-model")
        
        Config.initialize(LLM_MODEL=original_value)


if __name__ == "__main__":
    unittest.main()
