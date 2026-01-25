"""
LocalAI Assistant - Task Scheduler Service
Automation, task scheduling, and execution
Author: Manus AI
"""

import asyncio
import subprocess
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import logging
import uuid

logger = logging.getLogger(__name__)


class TaskStatus(str, Enum):
    """Task status enum"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ScheduleType(str, Enum):
    """Schedule type enum"""
    ONCE = "once"
    INTERVAL = "interval"
    CRON = "cron"


class Task:
    """Represents a scheduled task"""
    
    def __init__(
        self,
        task_id: str,
        name: str,
        command: str,
        schedule_type: ScheduleType,
        schedule_value: str,
        created_at: datetime = None
    ):
        self.task_id = task_id
        self.name = name
        self.command = command
        self.schedule_type = schedule_type
        self.schedule_value = schedule_value
        self.status = TaskStatus.PENDING
        self.created_at = created_at or datetime.now()
        self.last_run = None
        self.next_run = None
        self.result = None
        self.error = None
        self.execution_count = 0


class TaskScheduler:
    """
    Service for scheduling and executing tasks.
    Supports one-time, interval, and cron-based scheduling.
    """
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.running_tasks: Dict[str, asyncio.Task] = {}
    
    async def create_task(
        self,
        name: str,
        command: str,
        schedule_type: str,
        schedule_value: str
    ) -> Dict[str, Any]:
        """
        Create a new scheduled task.
        
        Args:
            name: Task name
            command: Command to execute (Python code or shell command)
            schedule_type: Type of schedule (once, interval, cron)
            schedule_value: Schedule value (depends on type)
            
        Returns:
            Dictionary with task information
        """
        task_id = str(uuid.uuid4())
        
        try:
            schedule_enum = ScheduleType(schedule_type)
        except ValueError:
            return {
                "error": f"Invalid schedule type: {schedule_type}",
                "valid_types": [t.value for t in ScheduleType]
            }
        
        task = Task(
            task_id=task_id,
            name=name,
            command=command,
            schedule_type=schedule_enum,
            schedule_value=schedule_value
        )
        
        self.tasks[task_id] = task
        
        # Calculate next run time
        await self._calculate_next_run(task)
        
        logger.info(f"Created task: {task_id} - {name}")
        
        return {
            "task_id": task_id,
            "name": name,
            "schedule_type": schedule_type,
            "schedule_value": schedule_value,
            "status": task.status.value,
            "created_at": task.created_at.isoformat(),
            "next_run": task.next_run.isoformat() if task.next_run else None
        }
    
    async def execute_task(self, task_id: str) -> Dict[str, Any]:
        """
        Execute a task immediately.
        
        Args:
            task_id: ID of task to execute
            
        Returns:
            Dictionary with execution result
        """
        if task_id not in self.tasks:
            return {"error": f"Task not found: {task_id}"}
        
        task = self.tasks[task_id]
        task.status = TaskStatus.RUNNING
        
        try:
            logger.info(f"Executing task: {task_id}")
            
            # Execute the command
            result = await self._execute_command(task.command)
            
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.last_run = datetime.now()
            task.execution_count += 1
            
            logger.info(f"Task completed: {task_id}")
            
            return {
                "task_id": task_id,
                "status": task.status.value,
                "result": result,
                "execution_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
            task.last_run = datetime.now()
            
            logger.error(f"Task failed: {task_id} - {str(e)}")
            
            return {
                "task_id": task_id,
                "status": task.status.value,
                "error": str(e),
                "execution_time": datetime.now().isoformat()
            }
    
    async def _execute_command(self, command: str) -> str:
        """
        Execute a command (Python or shell).
        
        Args:
            command: Command to execute
            
        Returns:
            Command output
        """
        # Try to execute as Python code first
        try:
            local_vars = {}
            exec(command, {}, local_vars)
            return str(local_vars)
        except:
            pass
        
        # Otherwise, execute as shell command
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise Exception(f"Command failed: {result.stderr}")
            
            return result.stdout
            
        except subprocess.TimeoutExpired:
            raise Exception("Command execution timeout (5 minutes)")
        except Exception as e:
            raise Exception(f"Command execution failed: {str(e)}")
    
    async def list_tasks(self) -> List[Dict[str, Any]]:
        """
        List all scheduled tasks.
        
        Returns:
            List of task information
        """
        tasks_list = []
        
        for task in self.tasks.values():
            tasks_list.append({
                "task_id": task.task_id,
                "name": task.name,
                "schedule_type": task.schedule_type.value,
                "schedule_value": task.schedule_value,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "last_run": task.last_run.isoformat() if task.last_run else None,
                "next_run": task.next_run.isoformat() if task.next_run else None,
                "execution_count": task.execution_count
            })
        
        return tasks_list
    
    async def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific task.
        
        Args:
            task_id: ID of task
            
        Returns:
            Task information or None
        """
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        
        return {
            "task_id": task.task_id,
            "name": task.name,
            "command": task.command,
            "schedule_type": task.schedule_type.value,
            "schedule_value": task.schedule_value,
            "status": task.status.value,
            "created_at": task.created_at.isoformat(),
            "last_run": task.last_run.isoformat() if task.last_run else None,
            "next_run": task.next_run.isoformat() if task.next_run else None,
            "execution_count": task.execution_count,
            "result": task.result,
            "error": task.error
        }
    
    async def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """
        Cancel a scheduled task.
        
        Args:
            task_id: ID of task to cancel
            
        Returns:
            Cancellation result
        """
        if task_id not in self.tasks:
            return {"error": f"Task not found: {task_id}"}
        
        task = self.tasks[task_id]
        
        # Cancel running task if exists
        if task_id in self.running_tasks:
            self.running_tasks[task_id].cancel()
            del self.running_tasks[task_id]
        
        task.status = TaskStatus.CANCELLED
        
        logger.info(f"Task cancelled: {task_id}")
        
        return {
            "task_id": task_id,
            "status": task.status.value,
            "message": "Task cancelled successfully"
        }
    
    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        """
        Delete a scheduled task.
        
        Args:
            task_id: ID of task to delete
            
        Returns:
            Deletion result
        """
        if task_id not in self.tasks:
            return {"error": f"Task not found: {task_id}"}
        
        # Cancel if running
        if task_id in self.running_tasks:
            self.running_tasks[task_id].cancel()
            del self.running_tasks[task_id]
        
        del self.tasks[task_id]
        
        logger.info(f"Task deleted: {task_id}")
        
        return {
            "task_id": task_id,
            "message": "Task deleted successfully"
        }
    
    async def _calculate_next_run(self, task: Task):
        """Calculate next run time for a task"""
        now = datetime.now()
        
        if task.schedule_type == ScheduleType.ONCE:
            # Parse datetime from schedule_value
            try:
                task.next_run = datetime.fromisoformat(task.schedule_value)
            except:
                task.next_run = now + timedelta(seconds=int(task.schedule_value))
        
        elif task.schedule_type == ScheduleType.INTERVAL:
            # Parse interval in seconds
            try:
                seconds = int(task.schedule_value)
                task.next_run = now + timedelta(seconds=seconds)
            except:
                task.next_run = now + timedelta(minutes=1)
        
        elif task.schedule_type == ScheduleType.CRON:
            # Simple cron parsing (limited support)
            # Format: "HH:MM" for daily, "MM" for hourly
            try:
                if ":" in task.schedule_value:
                    hour, minute = map(int, task.schedule_value.split(":"))
                    next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    if next_run <= now:
                        next_run += timedelta(days=1)
                    task.next_run = next_run
                else:
                    minute = int(task.schedule_value)
                    task.next_run = now + timedelta(minutes=minute)
            except:
                task.next_run = now + timedelta(hours=1)


# Global instance
task_scheduler = TaskScheduler()
