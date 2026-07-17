"""
FileSystem Tool - Read, create, edit, and delete local files.
"""

import os
from pathlib import Path
from typing import Optional, List

# Base directory for file operations (restrict to workspace for safety)
BASE_DIR = Path("/workspace")

def read_file(filepath: str) -> Optional[str]:
    """
    Read contents of a file.
    
    Args:
        filepath: Path to the file (relative or absolute)
    
    Returns:
        File contents as string, or error message if failed
    """
    try:
        path = _resolve_path(filepath)
        if not path.exists():
            return f"Error: File not found: {filepath}"
        if not path.is_file():
            return f"Error: Not a file: {filepath}"
        
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(filepath: str, content: str) -> dict:
    """
    Write content to a file (creates or overwrites).
    
    Args:
        filepath: Path to the file
        content: Content to write
    
    Returns:
        dict with success status and message
    """
    try:
        path = _resolve_path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return {"success": True, "message": f"Written to {filepath}"}
    except Exception as e:
        return {"success": False, "message": f"Error writing file: {str(e)}"}

def append_file(filepath: str, content: str) -> dict:
    """
    Append content to a file.
    
    Args:
        filepath: Path to the file
        content: Content to append
    
    Returns:
        dict with success status and message
    """
    try:
        path = _resolve_path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        
        return {"success": True, "message": f"Appended to {filepath}"}
    except Exception as e:
        return {"success": False, "message": f"Error appending to file: {str(e)}"}

def delete_file(filepath: str) -> dict:
    """
    Delete a file.
    
    Args:
        filepath: Path to the file
    
    Returns:
        dict with success status and message
    """
    try:
        path = _resolve_path(filepath)
        if path.exists() and path.is_file():
            path.unlink()
            return {"success": True, "message": f"Deleted {filepath}"}
        return {"success": False, "message": f"File not found: {filepath}"}
    except Exception as e:
        return {"success": False, "message": f"Error deleting file: {str(e)}"}

def list_directory(dirpath: str = ".") -> List[str]:
    """
    List contents of a directory.
    
    Args:
        dirpath: Path to the directory
    
    Returns:
        List of filenames/directories
    """
    try:
        path = _resolve_path(dirpath)
        if not path.exists():
            return [f"Error: Directory not found: {dirpath}"]
        if not path.is_dir():
            return [f"Error: Not a directory: {dirpath}"]
        
        items = []
        for item in sorted(path.iterdir()):
            prefix = "[D] " if item.is_dir() else "[F] "
            items.append(f"{prefix}{item.name}")
        return items
    except Exception as e:
        return [f"Error listing directory: {str(e)}"]

def file_exists(filepath: str) -> bool:
    """Check if a file exists."""
    try:
        path = _resolve_path(filepath)
        return path.exists() and path.is_file()
    except:
        return False

def _resolve_path(filepath: str) -> Path:
    """
    Resolve a filepath relative to BASE_DIR for safety.
    
    Prevents access outside the workspace directory.
    """
    path = Path(filepath)
    
    # If absolute path, ensure it's within BASE_DIR
    if path.is_absolute():
        try:
            return path.relative_to(BASE_DIR)
        except ValueError:
            # Path is outside BASE_DIR - restrict it
            return BASE_DIR / path.name
    
    # Relative path - resolve from BASE_DIR
    return BASE_DIR / filepath

if __name__ == "__main__":
    # Test FileSystem tool
    print("Testing FileSystem Tool...\n")
    
    # Test write
    result = write_file("test.txt", "Hello, World!")
    print(f"Write test: {result}")
    
    # Test read
    content = read_file("test.txt")
    print(f"Read test: {content}")
    
    # Test append
    result = append_file("test.txt", "\nAppended line.")
    print(f"Append test: {result}")
    
    # Read again
    content = read_file("test.txt")
    print(f"After append: {content}")
    
    # List directory
    files = list_directory(".")
    print(f"\nFiles in workspace:\n{chr(10).join(files[:10])}")
    
    # Cleanup
    delete_file("test.txt")
    print("\nTest file deleted.")