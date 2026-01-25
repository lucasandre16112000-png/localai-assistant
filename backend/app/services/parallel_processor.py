"""
LocalAI Assistant - Parallel Processor Service
Parallel processing, map/reduce, and batch operations
Author: Manus AI
"""

import asyncio
from typing import List, Dict, Any, Callable, Optional, TypeVar, Coroutine
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')
R = TypeVar('R')


class ParallelProcessor:
    """
    Service for parallel processing of tasks.
    Supports map, reduce, batch processing, and concurrent execution.
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.thread_executor = ThreadPoolExecutor(max_workers=max_workers)
        self.process_executor = ProcessPoolExecutor(max_workers=max_workers)
    
    async def map_async(
        self,
        func: Callable[[T], Coroutine[Any, Any, R]],
        items: List[T],
        batch_size: Optional[int] = None
    ) -> List[R]:
        """
        Apply an async function to each item in parallel.
        
        Args:
            func: Async function to apply
            items: List of items to process
            batch_size: Optional batch size for processing
            
        Returns:
            List of results in same order as input
        """
        if batch_size:
            results = []
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                batch_results = await asyncio.gather(*[func(item) for item in batch])
                results.extend(batch_results)
            return results
        else:
            return await asyncio.gather(*[func(item) for item in items])
    
    async def map_sync(
        self,
        func: Callable[[T], R],
        items: List[T],
        use_threads: bool = True,
        batch_size: Optional[int] = None
    ) -> List[R]:
        """
        Apply a sync function to each item in parallel.
        
        Args:
            func: Sync function to apply
            items: List of items to process
            use_threads: Use threads (True) or processes (False)
            batch_size: Optional batch size for processing
            
        Returns:
            List of results in same order as input
        """
        executor = self.thread_executor if use_threads else self.process_executor
        loop = asyncio.get_event_loop()
        
        if batch_size:
            results = []
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                batch_results = await asyncio.gather(*[
                    loop.run_in_executor(executor, func, item)
                    for item in batch
                ])
                results.extend(batch_results)
            return results
        else:
            return await asyncio.gather(*[
                loop.run_in_executor(executor, func, item)
                for item in items
            ])
    
    async def reduce_async(
        self,
        func: Callable[[Any, T], Coroutine[Any, Any, Any]],
        items: List[T],
        initial: Any = None
    ) -> Any:
        """
        Reduce items using an async function.
        
        Args:
            func: Async reduce function (accumulator, item) -> new_accumulator
            items: List of items to reduce
            initial: Initial accumulator value
            
        Returns:
            Reduced value
        """
        accumulator = initial
        for item in items:
            accumulator = await func(accumulator, item)
        return accumulator
    
    async def reduce_sync(
        self,
        func: Callable[[Any, T], Any],
        items: List[T],
        initial: Any = None,
        use_threads: bool = True
    ) -> Any:
        """
        Reduce items using a sync function.
        
        Args:
            func: Sync reduce function (accumulator, item) -> new_accumulator
            items: List of items to reduce
            initial: Initial accumulator value
            use_threads: Use threads (True) or processes (False)
            
        Returns:
            Reduced value
        """
        executor = self.thread_executor if use_threads else self.process_executor
        loop = asyncio.get_event_loop()
        
        accumulator = initial
        for item in items:
            accumulator = await loop.run_in_executor(
                executor,
                func,
                accumulator,
                item
            )
        return accumulator
    
    async def batch_process(
        self,
        items: List[T],
        batch_size: int,
        processor: Callable[[List[T]], Coroutine[Any, Any, List[R]]]
    ) -> List[R]:
        """
        Process items in batches.
        
        Args:
            items: List of items to process
            batch_size: Size of each batch
            processor: Async function to process each batch
            
        Returns:
            List of results
        """
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = await processor(batch)
            results.extend(batch_results)
            logger.info(f"Processed batch {i // batch_size + 1}: {len(batch)} items")
        
        return results
    
    async def execute_concurrent(
        self,
        tasks: List[Coroutine[Any, Any, Any]],
        max_concurrent: Optional[int] = None
    ) -> List[Any]:
        """
        Execute multiple coroutines concurrently with optional limit.
        
        Args:
            tasks: List of coroutines to execute
            max_concurrent: Maximum concurrent tasks (None = unlimited)
            
        Returns:
            List of results
        """
        if max_concurrent is None:
            return await asyncio.gather(*tasks)
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def bounded_task(task):
            async with semaphore:
                return await task
        
        return await asyncio.gather(*[bounded_task(task) for task in tasks])
    
    async def filter_async(
        self,
        predicate: Callable[[T], Coroutine[Any, Any, bool]],
        items: List[T]
    ) -> List[T]:
        """
        Filter items using an async predicate.
        
        Args:
            predicate: Async function that returns True/False
            items: List of items to filter
            
        Returns:
            Filtered list
        """
        results = await asyncio.gather(*[predicate(item) for item in items])
        return [item for item, result in zip(items, results) if result]
    
    async def filter_sync(
        self,
        predicate: Callable[[T], bool],
        items: List[T],
        use_threads: bool = True
    ) -> List[T]:
        """
        Filter items using a sync predicate.
        
        Args:
            predicate: Function that returns True/False
            items: List of items to filter
            use_threads: Use threads (True) or processes (False)
            
        Returns:
            Filtered list
        """
        executor = self.thread_executor if use_threads else self.process_executor
        loop = asyncio.get_event_loop()
        
        results = await asyncio.gather(*[
            loop.run_in_executor(executor, predicate, item)
            for item in items
        ])
        
        return [item for item, result in zip(items, results) if result]
    
    async def process_with_progress(
        self,
        func: Callable[[T], Coroutine[Any, Any, R]],
        items: List[T],
        progress_callback: Optional[Callable[[int, int], Coroutine[Any, Any, None]]] = None
    ) -> List[R]:
        """
        Process items with progress tracking.
        
        Args:
            func: Async function to apply
            items: List of items to process
            progress_callback: Async callback(current, total) for progress updates
            
        Returns:
            List of results
        """
        results = []
        total = len(items)
        
        for i, item in enumerate(items):
            result = await func(item)
            results.append(result)
            
            if progress_callback:
                await progress_callback(i + 1, total)
            
            logger.info(f"Progress: {i + 1}/{total}")
        
        return results
    
    def shutdown(self):
        """Shutdown executors"""
        self.thread_executor.shutdown(wait=True)
        self.process_executor.shutdown(wait=True)
        logger.info("Parallel processor shut down")


# Global instance
parallel_processor = ParallelProcessor()
