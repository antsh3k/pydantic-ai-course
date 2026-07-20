"""
Example 2: asyncio.create_task - Creating and Running Several Tasks

Demonstrates asyncio.create_task() with multiple tasks outside of a notebook context.
Use asyncio.run() since there is no existing event loop.
Run with: uv run python session_0_example_2.py
"""

import asyncio
import time


# Asynchronous (non-blocking) version - same as in session_0.ipynb
async def fetch_data_async(task_id: int, delay: float) -> str:
    """Simulates a long-running I/O operation using asyncio.sleep"""
    print(f"Task {task_id}: Starting (will take {delay}s)")
    await asyncio.sleep(delay)  # Yields control to other tasks
    print(f"Task {task_id}: Completed")
    return f"Result from task {task_id}"


async def main():
    print("=== asyncio.create_task Example ===")
    start = time.time()

    # Create all tasks - they start running as soon as created
    task1 = asyncio.create_task(fetch_data_async(1, 1.0))
    task2 = asyncio.create_task(fetch_data_async(2, 1.0))
    task3 = asyncio.create_task(fetch_data_async(3, 1.0))

    # Await each task to get results (they run concurrently, so total ~1s not 3s)
    result1 = await task1
    result2 = await task2
    result3 = await task3

    end = time.time()
    print(f"Completed in {end - start:.2f} seconds")
    print(f"Results: {result1}, {result2}, {result3}")


if __name__ == "__main__":
    asyncio.run(main())
