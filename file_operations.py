"""
File Operations Tools for Langchain Agent
Handles reading, writing, and manipulating files
"""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from langchain.tools import tool
import logging

logger = logging.getLogger(__name__)


class FileOperations:
    """File operations utility class"""
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """Read content from a file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"Error: File '{file_path}' does not exist"
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"Successfully read file: {file_path}")
            return content
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return f"Error reading file: {str(e)}"
    
    @staticmethod
    def write_file(file_path: str, content: str, append: bool = False) -> str:
        """Write or append content to a file"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            mode = 'a' if append else 'w'
            with open(path, mode, encoding='utf-8') as f:
                f.write(content)
            
            action = "appended to" if append else "written to"
            logger.info(f"Successfully {action} file: {file_path}")
            return f"Content successfully {action} {file_path}"
        except Exception as e:
            logger.error(f"Error writing to file {file_path}: {str(e)}")
            return f"Error writing to file: {str(e)}"
    
    @staticmethod
    def list_files(directory: str, pattern: Optional[str] = None) -> List[str]:
        """List files in a directory with optional pattern matching"""
        try:
            path = Path(directory)
            if not path.exists():
                return [f"Error: Directory '{directory}' does not exist"]
            
            if pattern:
                files = list(path.glob(pattern))
            else:
                files = list(path.iterdir())
            
            file_list = [str(f.relative_to(path)) for f in files if f.is_file()]
            logger.info(f"Listed {len(file_list)} files in {directory}")
            return sorted(file_list)
        except Exception as e:
            logger.error(f"Error listing files in {directory}: {str(e)}")
            return [f"Error: {str(e)}"]
    
    @staticmethod
    def delete_file(file_path: str) -> str:
        """Delete a file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"Error: File '{file_path}' does not exist"
            
            path.unlink()
            logger.info(f"Successfully deleted file: {file_path}")
            return f"File {file_path} deleted successfully"
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {str(e)}")
            return f"Error deleting file: {str(e)}"
    
    @staticmethod
    def copy_file(source: str, destination: str) -> str:
        """Copy a file from source to destination"""
        try:
            src_path = Path(source)
            dst_path = Path(destination)
            
            if not src_path.exists():
                return f"Error: Source file '{source}' does not exist"
            
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            with open(src_path, 'rb') as src:
                with open(dst_path, 'wb') as dst:
                    dst.write(src.read())
            
            logger.info(f"Successfully copied {source} to {destination}")
            return f"File copied from {source} to {destination}"
        except Exception as e:
            logger.error(f"Error copying file: {str(e)}")
            return f"Error copying file: {str(e)}"
    
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """Read a JSON file"""
        try:
            content = FileOperations.read_file(file_path)
            if content.startswith("Error"):
                return {"error": content}
            
            data = json.loads(content)
            logger.info(f"Successfully read JSON from {file_path}")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {file_path}: {str(e)}")
            return {"error": f"JSON decode error: {str(e)}"}
        except Exception as e:
            logger.error(f"Error reading JSON file: {str(e)}")
            return {"error": str(e)}
    
    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any]) -> str:
        """Write data as JSON to a file"""
        try:
            json_content = json.dumps(data, indent=2)
            result = FileOperations.write_file(file_path, json_content)
            logger.info(f"Successfully wrote JSON to {file_path}")
            return result
        except Exception as e:
            logger.error(f"Error writing JSON to {file_path}: {str(e)}")
            return f"Error writing JSON: {str(e)}"


# Langchain tool definitions
@tool
def read_file_tool(file_path: str) -> str:
    """Read the contents of a file. Use this to read text files."""
    return FileOperations.read_file(file_path)


@tool
def write_file_tool(file_path: str, content: str) -> str:
    """Write content to a file. Creates the file if it doesn't exist."""
    return FileOperations.write_file(file_path, content)


@tool
def append_file_tool(file_path: str, content: str) -> str:
    """Append content to the end of a file."""
    return FileOperations.write_file(file_path, content, append=True)


@tool
def list_files_tool(directory: str, pattern: str = "*") -> List[str]:
    """List files in a directory. Pattern uses glob syntax (e.g., '*.txt', '*.json')."""
    return FileOperations.list_files(directory, pattern if pattern != "*" else None)


@tool
def delete_file_tool(file_path: str) -> str:
    """Delete a file from the filesystem."""
    return FileOperations.delete_file(file_path)


@tool
def copy_file_tool(source: str, destination: str) -> str:
    """Copy a file from source to destination."""
    return FileOperations.copy_file(source, destination)


@tool
def read_json_tool(file_path: str) -> Dict[str, Any]:
    """Read and parse a JSON file."""
    return FileOperations.read_json(file_path)


@tool
def write_json_tool(file_path: str, data: Dict[str, Any]) -> str:
    """Write a dictionary as JSON to a file."""
    return FileOperations.write_json(file_path, data)
