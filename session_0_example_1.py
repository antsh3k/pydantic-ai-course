import asyncio
import time


# Sequential (blocking) version
def fetch_data_sequential(task_id: int, delay: float) -> str:
    """Simulates a long-running I/O operation using time.sleep"""
    print(f"Task {task_id}: Starting (will take {delay}s)")
    time.sleep(delay)  # Blocks the entire program
    print(f"Task {task_id}: Completed")
    return f"Result from task {task_id}"


# Asynchronous (non-blocking) version
async def fetch_data_async(task_id: int, delay: float) -> str:
    """Simulates a long-running I/O operation using asyncio.sleep"""
    print(f"Task {task_id}: Starting (will take {delay}s)")
    await asyncio.sleep(delay)  # Yields control to other tasks
    print(f"Task {task_id}: Completed")
    return f"Result from task {task_id}"


async def main():
    # Sequential execution - tasks run one after another
    print("=== Sequential Execution ===")
    start = time.time()
    _ = [
        fetch_data_sequential(1, 1.0),
        fetch_data_sequential(2, 1.0),
        fetch_data_sequential(3, 1.0),
    ]
    end = time.time()
    print(f"Sequential took: {end - start:.2f} seconds\n")

    # Asynchronous execution - tasks run concurrently
    print("=== Asynchronous Execution ===")
    start = time.time()
    _ = await asyncio.gather(
        fetch_data_async(1, 1.0),
        fetch_data_async(2, 1.0),
        fetch_data_async(3, 1.0),
    )
    end = time.time()
    print(f"Asynchronous took: {end - start:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
