import asyncio
from codetiming import Timer


async def task(name, work_queue):
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    while not work_queue.empty():
        delay = await work_queue.get()
        print(f"Task {name} running")
        timer.start()
        await asyncio.sleep(delay)
        timer.stop()


async def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = asyncio.Queue()

    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        await work_queue.put(work)

    # Run the tasks
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        await asyncio.gather(
            asyncio.create_task(task("One", work_queue)),
            asyncio.create_task(task("Two", work_queue)),
        )


if __name__ == "__main__":
    asyncio.run(main())

    """
    Output:

    Task One running
    Task Two running
    Task Two total elapsed time: 10.0
    Task Two running
    Task One total elapsed time: 15.0
    Task One running
    Task Two total elapsed time: 5.0
    Task One total elapsed time: 2.0

    Total elapsed time: 17.0
    """