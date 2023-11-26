import asyncio
import aiohttp
from codetiming import Timer


async def task(name, work_queue):
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f"Task {name} getting URL: {url}")
            timer.start()
            async with session.get(url) as response:
                await response.text()
            timer.stop()


async def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = asyncio.Queue()

    # Put some work in the queue
    for url in [
        "http://google.com",
        "http://yahoo.com",
        "http://linkedin.com",
        "http://apple.com",
        "http://microsoft.com",
        "http://facebook.com",
        "http://twitter.com",
    ]:
        await work_queue.put(url)

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

    Task One getting URL: http://google.com
    Task Two getting URL: http://yahoo.com
    Task One total elapsed time: 0.3
    Task One getting URL: http://linkedin.com
    Task One total elapsed time: 0.3
    Task One getting URL: http://apple.com
    Task One total elapsed time: 0.3
    Task One getting URL: http://microsoft.com
    Task Two total elapsed time: 0.9
    Task Two getting URL: http://facebook.com
    Task Two total elapsed time: 0.4
    Task Two getting URL: http://twitter.com
    Task One total elapsed time: 0.5
    Task Two total elapsed time: 0.3

    Total elapsed time: 1.7
    """