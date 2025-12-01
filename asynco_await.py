import asyncio

# Long running function (e.g., downloading a big file)
async def long_task():
    print("Long task started...")
    await asyncio.sleep(5)   # Simulate long work
    print("Long task finished.")
    return "Long task result"

# Short fast function
async def short_task(name):
    print(f"{name} started...")
    await asyncio.sleep(1)   # Fast work
    print(f"{name} finished.")
    return f"{name} result"

# Main function running tasks concurrently
async def main():
    # Create tasks (start running immediately)
    
    task1 = asyncio.create_task(short_task("Task A"))
    task2 = asyncio.create_task(long_task())
    task3 = asyncio.create_task(short_task("Task B"))

    # Wait for all tasks to finish
    results = await asyncio.gather(task1, task2, task3)

    print("\nFinal Results:")
    for r in results:
        print(r)

asyncio.run(main())
