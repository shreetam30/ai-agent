"""
Database Operations Tools for Langchain Agent
Handles SQLite database operations including CRUD and query operations
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from langchain.tools import tool
import logging

logger = logging.getLogger(__name__)


class DatabaseOperations:
    """Database operations utility class for SQLite"""
    
    def __init__(self, db_path: str = "agent.db"):
        self.db_path = db_path
        self.ensure_db_exists()
    
    def ensure_db_exists(self) -> None:
        """Ensure database file exists"""
        try:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            conn.close()
            logger.info(f"Database ensured at {self.db_path}")
        except Exception as e:
            logger.error(f"Error ensuring database exists: {str(e)}")
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> Tuple[bool, Any]:
        """Execute a database query (SELECT)"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            conn.close()
            
            # Convert Row objects to dictionaries
            data = [dict(row) for row in results]
            logger.info(f"Query executed successfully, returned {len(data)} rows")
            return True, data
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            return False, f"Query error: {str(e)}"
    
    def execute_update(self, query: str, params: Optional[Tuple] = None) -> Tuple[bool, str]:
        """Execute a database update/insert/delete"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            affected_rows = cursor.rowcount
            conn.close()
            
            logger.info(f"Update executed successfully, affected {affected_rows} rows")
            return True, f"Success: {affected_rows} rows affected"
        except Exception as e:
            logger.error(f"Error executing update: {str(e)}")
            return False, f"Update error: {str(e)}"
    
    def create_table(self, table_name: str, schema: Dict[str, str]) -> Tuple[bool, str]:
        """Create a table with given schema"""
        try:
            columns = ", ".join([f"{col} {dtype}" for col, dtype in schema.items()])
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()
            
            logger.info(f"Table {table_name} created successfully")
            return True, f"Table {table_name} created successfully"
        except Exception as e:
            logger.error(f"Error creating table: {str(e)}")
            return False, f"Error creating table: {str(e)}"
    
    def insert_record(self, table_name: str, record: Dict[str, Any]) -> Tuple[bool, str]:
        """Insert a record into a table"""
        try:
            columns = ", ".join(record.keys())
            placeholders = ", ".join(["?" for _ in record])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            success, msg = self.execute_update(query, tuple(record.values()))
            if success:
                return True, f"Record inserted into {table_name}"
            return success, msg
        except Exception as e:
            logger.error(f"Error inserting record: {str(e)}")
            return False, f"Insert error: {str(e)}"
    
    def insert_records(self, table_name: str, records: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Insert multiple records into a table"""
        try:
            if not records:
                return False, "No records to insert"
            
            first_record = records[0]
            columns = ", ".join(first_record.keys())
            placeholders = ", ".join(["?" for _ in first_record])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            values_list = [tuple(record.values()) for record in records]
            cursor.executemany(query, values_list)
            
            conn.commit()
            affected_rows = cursor.rowcount
            conn.close()
            
            logger.info(f"Inserted {affected_rows} records into {table_name}")
            return True, f"Success: {affected_rows} records inserted"
        except Exception as e:
            logger.error(f"Error inserting records: {str(e)}")
            return False, f"Insert error: {str(e)}"
    
    def get_table_info(self, table_name: str) -> Tuple[bool, Any]:
        """Get table schema information"""
        try:
            query = f"PRAGMA table_info({table_name})"
            success, results = self.execute_query(query)
            
            if not success:
                return False, results
            
            schema_info = {
                row["name"]: row["type"] for row in results
            }
            logger.info(f"Retrieved schema for {table_name}")
            return True, schema_info
        except Exception as e:
            logger.error(f"Error getting table info: {str(e)}")
            return False, f"Error: {str(e)}"
    
    def list_tables(self) -> Tuple[bool, List[str]]:
        """List all tables in the database"""
        try:
            query = "SELECT name FROM sqlite_master WHERE type='table'"
            success, results = self.execute_query(query)
            
            if not success:
                return False, results
            
            tables = [row["name"] for row in results]
            logger.info(f"Listed {len(tables)} tables")
            return True, tables
        except Exception as e:
            logger.error(f"Error listing tables: {str(e)}")
            return False, f"Error: {str(e)}"
    
    def delete_records(self, table_name: str, condition: Optional[str] = None) -> Tuple[bool, str]:
        """Delete records from a table"""
        try:
            query = f"DELETE FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            
            success, msg = self.execute_update(query)
            return success, msg
        except Exception as e:
            logger.error(f"Error deleting records: {str(e)}")
            return False, f"Delete error: {str(e)}"
    
    def drop_table(self, table_name: str) -> Tuple[bool, str]:
        """Drop a table from the database"""
        try:
            query = f"DROP TABLE IF EXISTS {table_name}"
            success, msg = self.execute_update(query)
            return success, msg
        except Exception as e:
            logger.error(f"Error dropping table: {str(e)}")
            return False, f"Error: {str(e)}"


# Global database instance
_db_instance = None


def get_db(db_path: str = "agent.db") -> DatabaseOperations:
    """Get or create global database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseOperations(db_path)
    return _db_instance


# Langchain tool definitions
@tool
def create_table_tool(table_name: str, schema: Dict[str, str]) -> str:
    """Create a table in the database. Schema is a dict mapping column names to types (e.g., {'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT'})."""
    db = get_db()
    success, msg = db.create_table(table_name, schema)
    return msg


@tool
def insert_record_tool(table_name: str, record: Dict[str, Any]) -> str:
    """Insert a single record into a table."""
    db = get_db()
    success, msg = db.insert_record(table_name, record)
    return msg


@tool
def insert_records_tool(table_name: str, records: List[Dict[str, Any]]) -> str:
    """Insert multiple records into a table."""
    db = get_db()
    success, msg = db.insert_records(table_name, records)
    return msg


@tool
def query_database_tool(query: str) -> str:
    """Execute a SELECT query on the database. Returns results as a list of dictionaries."""
    db = get_db()
    success, results = db.execute_query(query)
    if success:
        return str(results)
    return f"Error: {results}"


@tool
def update_database_tool(query: str) -> str:
    """Execute an UPDATE, INSERT, or DELETE query on the database."""
    db = get_db()
    success, msg = db.execute_update(query)
    return msg


@tool
def get_table_schema_tool(table_name: str) -> str:
    """Get the schema (column names and types) of a table."""
    db = get_db()
    success, schema = db.get_table_info(table_name)
    if success:
        return str(schema)
    return f"Error: {schema}"


@tool
def list_tables_tool() -> str:
    """List all tables in the database."""
    db = get_db()
    success, tables = db.list_tables()
    if success:
        return str(tables)
    return f"Error: {tables}"


@tool
def delete_records_tool(table_name: str, condition: str = "") -> str:
    """Delete records from a table. Condition is optional (e.g., 'id = 5')."""
    db = get_db()
    success, msg = db.delete_records(table_name, condition if condition else None)
    return msg


@tool
def drop_table_tool(table_name: str) -> str:
    """Drop (delete) an entire table from the database."""
    db = get_db()
    success, msg = db.drop_table(table_name)
    return msg
