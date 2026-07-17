"""
Terminal Tool - Execute shell commands safely.
"""

import subprocess
import shlex
from typing import Optional, Tuple

# Allowed commands whitelist for safety
ALLOWED_COMMANDS = {
    # File operations
    "ls", "cat", "head", "tail", "wc", "find", "grep", "tree",
    # Navigation
    "pwd", "cd",
    # System info
    "uname", "whoami", "hostname", "date", "echo",
    # Python
    "python", "python3", "pip", "pip3",
    # Git
    "git",
    # Development
    "npm", "node", "cargo", "rustc", "go",
    # Containers
    "docker", "docker-compose",
    # Network (read-only)
    "curl", "wget",
    # Compression
    "tar", "zip", "unzip", "gzip",
    # Process management
    "ps", "top", "htop", "kill",
    # Disk usage
    "du", "df",
}

# Dangerous commands that are explicitly blocked
BLOCKED_COMMANDS = {
    "rm", "shred", "dd", "mkfs", "fdisk", "chmod", "chown",
    "sudo", "su", "passwd", "useradd", "userdel",
    "wget", "curl",  # Could be used to download malicious content
    "nc", "netcat", "telnet", "ssh",  # Network tools
    "eval", "exec",
}

def execute_command(command: str, timeout: int = 30) -> dict:
    """
    Execute a shell command with safety checks.
    
    Args:
        command: The command to execute
        timeout: Maximum execution time in seconds
    
    Returns:
        dict with stdout, stderr, returncode, and success status
    """
    # Safety check
    safety_check = validate_command(command)
    if not safety_check["allowed"]:
        return {
            "success": False,
            "stdout": "",
            "stderr": safety_check["reason"],
            "returncode": -1,
            "blocked": True
        }
    
    try:
        # Parse command safely
        args = shlex.split(command)
        
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd="/workspace"
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "blocked": False
        }
    
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds",
            "returncode": -1,
            "blocked": False
        }
    except FileNotFoundError as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Command not found: {str(e)}",
            "returncode": -1,
            "blocked": False
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Error executing command: {str(e)}",
            "returncode": -1,
            "blocked": False
        }

def validate_command(command: str) -> dict:
    """
    Validate if a command is safe to execute.
    
    Args:
        command: The command to validate
    
    Returns:
        dict with 'allowed' boolean and 'reason' if blocked
    """
    # Parse the command
    try:
        args = shlex.split(command)
    except ValueError as e:
        return {"allowed": False, "reason": f"Invalid command syntax: {e}"}
    
    if not args:
        return {"allowed": False, "reason": "Empty command"}
    
    base_command = args[0].split("/")[-1]  # Get command name without path
    
    # Check against blocked list first
    if base_command in BLOCKED_COMMANDS:
        return {"allowed": False, "reason": f"Command '{base_command}' is blocked for safety"}
    
    # Check for dangerous patterns
    dangerous_patterns = [">", "|", ";", "&", "$", "`", "(", ")"]
    for pattern in dangerous_patterns:
        if pattern in command and pattern not in ["|"]:  # Allow pipes
            return {"allowed": False, "reason": f"Command contains potentially dangerous character: {pattern}"}
    
    # Check against allowed list (if list is not empty)
    if ALLOWED_COMMANDS and base_command not in ALLOWED_COMMANDS:
        # For commands not in allowed list, warn but don't block
        # In production, you might want stricter enforcement
        pass
    
    return {"allowed": True, "reason": ""}

def run(command: str):
    """
    Main entry point for terminal execution.
    
    Args:
        command: Shell command to run
    
    Returns:
        Formatted output string
    """
    result = execute_command(command)
    
    output = []
    if result.get("blocked"):
        output.append(f"[BLOCKED] {result['stderr']}")
    else:
        if result["stdout"]:
            output.append(result["stdout"])
        if result["stderr"]:
            output.append(f"[stderr] {result['stderr']}")
        if not result["success"]:
            output.append(f"[Exit code: {result['returncode']}]")
    
    return "\n".join(output) if output else "[No output]"

if __name__ == "__main__":
    # Test Terminal tool
    print("Testing Terminal Tool...\n")
    
    # Safe commands
    tests = [
        "pwd",
        "ls -la",
        "echo 'Hello, World!'",
        "python3 --version",
        "git status",
    ]
    
    for cmd in tests:
        print(f"\n$ {cmd}")
        print(run(cmd))
        print("-" * 40)
    
    # Blocked command test
    print("\n$ rm -rf /")
    print(run("rm -rf /"))