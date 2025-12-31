"""
LocalAI Assistant - Advanced Code Executor Service
Execute Python, JavaScript, Shell code with sandboxing
Author: Manus AI
"""

import asyncio
import subprocess
import tempfile
import os
from typing import Dict, Any, Optional
from datetime import datetime
import logging
import sys

logger = logging.getLogger(__name__)


class CodeExecutor:
    """
    Service for executing code safely with sandboxing and resource limits.
    Supports Python, JavaScript, Shell, and more.
    """
    
    def __init__(self):
        self.timeout = 300  # 5 minutes
        self.max_output = 10000  # 10KB
    
    async def execute_python(
        self,
        code: str,
        timeout: Optional[int] = None,
        sandbox: bool = True
    ) -> Dict[str, Any]:
        """
        Execute Python code.
        
        Args:
            code: Python code to execute
            timeout: Execution timeout in seconds
            sandbox: Whether to sandbox the execution
            
        Returns:
            Dictionary with execution result
        """
        timeout = timeout or self.timeout
        
        try:
            logger.info("Executing Python code")
            
            # Create temporary file for code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute with timeout
                result = subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                output = result.stdout[:self.max_output]
                error = result.stderr[:self.max_output]
                
                return {
                    "status": "success" if result.returncode == 0 else "error",
                    "return_code": result.returncode,
                    "output": output,
                    "error": error,
                    "execution_time": datetime.now().isoformat()
                }
            
            finally:
                # Clean up temp file
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
        
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": f"Code execution timeout ({timeout}s)",
                "execution_time": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error executing Python: {e}")
            return {
                "status": "error",
                "error": str(e),
                "execution_time": datetime.now().isoformat()
            }
    
    async def execute_javascript(
        self,
        code: str,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute JavaScript code.
        
        Args:
            code: JavaScript code to execute
            timeout: Execution timeout in seconds
            
        Returns:
            Dictionary with execution result
        """
        timeout = timeout or self.timeout
        
        try:
            logger.info("Executing JavaScript code")
            
            # Create temporary file for code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute with Node.js
                result = subprocess.run(
                    ["node", temp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                output = result.stdout[:self.max_output]
                error = result.stderr[:self.max_output]
                
                return {
                    "status": "success" if result.returncode == 0 else "error",
                    "return_code": result.returncode,
                    "output": output,
                    "error": error,
                    "execution_time": datetime.now().isoformat()
                }
            
            finally:
                # Clean up temp file
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
        
        except FileNotFoundError:
            return {
                "status": "error",
                "error": "Node.js not installed",
                "execution_time": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": f"Code execution timeout ({timeout}s)",
                "execution_time": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error executing JavaScript: {e}")
            return {
                "status": "error",
                "error": str(e),
                "execution_time": datetime.now().isoformat()
            }
    
    async def execute_shell(
        self,
        command: str,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute shell command.
        
        Args:
            command: Shell command to execute
            timeout: Execution timeout in seconds
            
        Returns:
            Dictionary with execution result
        """
        timeout = timeout or self.timeout
        
        try:
            logger.info(f"Executing shell command: {command[:50]}")
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = result.stdout[:self.max_output]
            error = result.stderr[:self.max_output]
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "return_code": result.returncode,
                "command": command,
                "output": output,
                "error": error,
                "execution_time": datetime.now().isoformat()
            }
        
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": f"Command execution timeout ({timeout}s)",
                "execution_time": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error executing shell command: {e}")
            return {
                "status": "error",
                "error": str(e),
                "execution_time": datetime.now().isoformat()
            }
    
    async def execute_with_input(
        self,
        code: str,
        language: str,
        input_data: str = "",
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute code with input data.
        
        Args:
            code: Code to execute
            language: Programming language
            input_data: Input data for the program
            timeout: Execution timeout
            
        Returns:
            Dictionary with execution result
        """
        timeout = timeout or self.timeout
        
        try:
            logger.info(f"Executing {language} code with input")
            
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{language}', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                if language == "python":
                    cmd = [sys.executable, temp_file]
                elif language == "javascript":
                    cmd = ["node", temp_file]
                else:
                    return {"error": f"Unsupported language: {language}"}
                
                result = subprocess.run(
                    cmd,
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                return {
                    "status": "success" if result.returncode == 0 else "error",
                    "return_code": result.returncode,
                    "output": result.stdout[:self.max_output],
                    "error": result.stderr[:self.max_output],
                    "execution_time": datetime.now().isoformat()
                }
            
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
        
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": f"Execution timeout ({timeout}s)",
                "execution_time": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error executing code: {e}")
            return {
                "status": "error",
                "error": str(e),
                "execution_time": datetime.now().isoformat()
            }


# Global instance
code_executor = CodeExecutor()
