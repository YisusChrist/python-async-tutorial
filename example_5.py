import queue
import requests
from codetiming import Timer


def task(name, work_queue):
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    with requests.Session() as session:
        while not work_queue.empty():
            url = work_queue.get()
            print(f"Task {name} getting URL: {url}")
            timer.start()
            session.get(url)
            timer.stop()
            yield


def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = queue.Queue()

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
        work_queue.put(url)

    tasks = [task("One", work_queue), task("Two", work_queue)]

    # Run the tasks
    done = False
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        while not done:
            for t in tasks:
                try:
                    next(t)
                except StopIteration:
                    tasks.remove(t)
                if len(tasks) == 0:
                    done = True


if __name__ == "__main__":
    main()

    """
    Output:
    
    Task One getting URL: http://google.com
    Task One total elapsed time: 0.3
    Task Two getting URL: http://yahoo.com
    Task Two total elapsed time: 0.8
    Task One getting URL: http://linkedin.com
    Task One total elapsed time: 0.4
    Task Two getting URL: http://apple.com
    Task Two total elapsed time: 0.3
    Task One getting URL: http://microsoft.com
    Task One total elapsed time: 0.5
    Task Two getting URL: http://facebook.com
    Task Two total elapsed time: 0.5
    Task One getting URL: http://twitter.com
    Task One total elapsed time: 0.4

    Total elapsed time: 3.2
    """