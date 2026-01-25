"""
LocalAI Assistant - Tasks Router
API endpoints for task scheduling and execution
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from ..services.task_scheduler import task_scheduler

router = APIRouter(prefix="/tasks", tags=["Task Scheduling"])


class TaskCreate(BaseModel):
    """Model for creating a task"""
    name: str
    command: str
    schedule_type: str  # once, interval, cron
    schedule_value: str


@router.post("/create")
async def create_task(task: TaskCreate):
    """
    Create a new scheduled task.
    
    - **name**: Task name
    - **command**: Command to execute
    - **schedule_type**: Type of schedule (once, interval, cron)
    - **schedule_value**: Schedule value
    """
    result = await task_scheduler.create_task(
        task.name,
        task.command,
        task.schedule_type,
        task.schedule_value
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.post("/execute/{task_id}")
async def execute_task(task_id: str):
    """
    Execute a task immediately.
    
    - **task_id**: ID of task to execute
    """
    result = await task_scheduler.execute_task(task_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@router.get("/list")
async def list_tasks():
    """List all scheduled tasks"""
    tasks = await task_scheduler.list_tasks()
    return {"tasks": tasks, "count": len(tasks)}


@router.get("/{task_id}")
async def get_task(task_id: str):
    """
    Get information about a specific task.
    
    - **task_id**: ID of task
    """
    task = await task_scheduler.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.post("/{task_id}/cancel")
async def cancel_task(task_id: str):
    """
    Cancel a scheduled task.
    
    - **task_id**: ID of task to cancel
    """
    result = await task_scheduler.cancel_task(task_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """
    Delete a scheduled task.
    
    - **task_id**: ID of task to delete
    """
    result = await task_scheduler.delete_task(task_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result
