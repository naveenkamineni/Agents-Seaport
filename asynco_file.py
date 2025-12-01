import asyncio
import aiofiles

# Async file write
async def write_file():
    print("Writing to file...")
    async with aiofiles.open("demo.txt", "w") as f:
        await f.write("Hello, this is async file write!\n")
    print("File write completed.")

# Async file read
async def read_file():
    print("Reading file...")
    async with aiofiles.open("demo.txt", "r") as f:
        content = await f.read()   # WAITING while file loads
    print("File read completed.")
    return content

async def main():
    # Run both at the same time
    write_task = asyncio.create_task(write_file())
    read_task = asyncio.create_task(read_file())

    results = await asyncio.gather(write_task, read_task)

    print("\nFinal Output:")
    print(results[1])  # content from read_file()

asyncio.run(main())
