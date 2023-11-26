Reference: https://realpython.com/python-async-features/

![Getting Started With Async Features in Python](https://files.realpython.com/media/Understanding-Asynchronous-Programming-in-Python_Watermarked.4b590c7c03ea.jpg)

# Getting Started With Async Features in Python

by [Doug Farrell](#author)

Table of Contents

- [Getting Started With Async Features in Python](#getting-started-with-async-features-in-python)
  - [Understanding Asynchronous Programming](#understanding-asynchronous-programming)
    - [Building a Synchronous Web Server](#building-a-synchronous-web-server)
    - [Thinking Differently About Programming](#thinking-differently-about-programming)
  - [Programming Parents: Not as Easy as It Looks](#programming-parents-not-as-easy-as-it-looks)
    - [Thought Experiment #1: The Synchronous Parent](#thought-experiment-1-the-synchronous-parent)
    - [Thought Experiment #2: The Polling Parent](#thought-experiment-2-the-polling-parent)
    - [Thought Experiment #3: The Threading Parent](#thought-experiment-3-the-threading-parent)
  - [Using Python Async Features in Practice](#using-python-async-features-in-practice)
    - [Synchronous Programming](#synchronous-programming)
    - [Simple Cooperative Concurrency](#simple-cooperative-concurrency)
    - [Cooperative Concurrency With Blocking Calls](#cooperative-concurrency-with-blocking-calls)
    - [Cooperative Concurrency With Non-Blocking Calls](#cooperative-concurrency-with-non-blocking-calls)
    - [Synchronous (Blocking) HTTP Calls](#synchronous-blocking-http-calls)
    - [Asynchronous (Non-Blocking) HTTP Calls](#asynchronous-non-blocking-http-calls)
  - [Conclusion](#conclusion)
- [Author](#author)
  - [About Doug Farrell](#about-doug-farrell)

Have you heard of asynchronous programming in Python? Are you curious to know more about Python async features and how you can use them in your work? Perhaps you’ve even tried to write [threaded programs](https://realpython.com/intro-to-python-threading/) and run into some issues. If you’re looking to understand how to use Python async features, then you’ve come to the right place.

**In this article, you’ll learn:**

- What a **synchronous program** is
- What an **asynchronous program** is
- Why you might want to write an asynchronous program
- How to use Python async features

All of the example code in this article have been tested with Python 3.7.2. You can grab a copy to follow along by clicking the link below:

**Download Code:** [Click here to download the code you’ll use](https://realpython.com/bonus/async-features/) to learn about async features in Python in this tutorial.

## Understanding Asynchronous Programming[](#understanding-asynchronous-programming "Permanent link")

A **synchronous program** is executed one step at a time. Even with conditional branching, loops and function calls, you can still think about the code in terms of taking one execution step at a time. When each step is complete, the program moves on to the next one.

Here are two examples of programs that work this way:

- **Batch processing programs** are often created as synchronous programs. You get some input, process it, and create some output. Steps follow one after the other until the program reaches the desired output. The program only needs to pay attention to the steps and their order.
- **Command-line programs** are small, quick processes that run in a terminal. These scripts are used to create something, transform one thing into something else, generate a report, or perhaps list out some data. This can be expressed as a series of program steps that are executed sequentially until the program is done.

An **asynchronous program** behaves differently. It still takes one execution step at a time. The difference is that the system may not wait for an execution step to be completed before moving on to the next one.

This means that the program will move on to future execution steps even though a previous step hasn’t yet finished and is still running elsewhere. This also means that the program knows what to do when a previous step does finish running.

Why would you want to write a program in this manner? The rest of this article will help you answer that question and give you the tools you need to elegantly solve interesting asynchronous problems.

### Building a Synchronous Web Server[](#building-a-synchronous-web-server "Permanent link")

A web server’s basic unit of work is, more or less, the same as batch processing. The server will get some input, process it, and create the output. Written as a synchronous program, this would create a working web server.

It would also be an _absolutely terrible_ web server.

Why? In this case, one unit of work (input, process, output) is not the only purpose. The real purpose is to handle hundreds or even thousands of units of work as quickly as possible. This can happen over long periods of time, and several work units may even arrive all at once.

Can a synchronous web server be made better? Sure, you could optimize the execution steps so that all the work coming in is handled as quickly as possible. Unfortunately, there are limitations to this approach. The result could be a web server that doesn’t respond fast enough, can’t handle enough work, or even one that times out when work gets stacked up.

**Note:** There are other limitations you might see if you tried to optimize the above approach. These include network speed, file IO speed, database query speed, and the speed of other connected services, to name a few. What these all have in common is that they are all IO functions. All of these items are orders of magnitude slower than the CPU’s processing speed.

In a synchronous program, if an execution step starts a database query, then the CPU is essentially idle until the database query is returned. For batch-oriented programs, this isn’t a priority most of the time. Processing the results of that IO operation is the goal. Often, this can take longer than the IO operation itself. Any optimization efforts would be focused on the processing work, not the IO.

Asynchronous programming techniques allow your programs to take advantage of relatively slow IO processes by freeing the CPU to do other work.

### Thinking Differently About Programming[](#thinking-differently-about-programming "Permanent link")

When you start trying to understand asynchronous programming, you might see a lot of discussion about the importance of blocking, or writing [non-blocking code](https://medium.com/vaidikkapoor/understanding-non-blocking-i-o-with-python-part-1-ec31a2e2db9b). (Personally, I struggled to get a good grasp of these concepts from the people I asked and the documentation I read.)

What is non-blocking code? What’s blocking code, for that matter? Would the answers to these questions help you write a better web server? If so, how could you do it? Let’s find out!

Writing asynchronous programs requires that you think differently about programming. While this new way of thinking can be hard to wrap your head around, it’s also an interesting exercise. That’s because the real world is almost entirely asynchronous, and so is how you interact with it.

Imagine this: you’re a parent trying to do several things at once. You have to balance the checkbook, do the laundry, and keep an eye on the kids. Somehow, you’re able to do all of these things at the same time without even thinking about it! Let’s break it down:

- Balancing the checkbook is a **synchronous** task. One step follows another until it’s done. You’re doing all the work yourself.
- However, you can break away from the checkbook to do laundry. You unload the dryer, move clothes from the washer to the dryer, and start another load in the washer.
- Working with the washer and dryer is a synchronous task, but the bulk of the work happens _after_ the washer and dryer are started. Once you’ve got them going, you can walk away and get back to the checkbook task. At this point, the washer and dryer tasks have become **asynchronous**. The washer and dryer will run independently until the buzzer goes off (notifying you that the task needs attention).
- Watching your kids is another asynchronous task. Once they are set up and playing, they can do so independently for the most part. This changes when someone needs attention, like when someone gets hungry or hurt. When one of your kids yells in alarm, you react. The kids are a long-running task with high priority. Watching them supersedes any other tasks you might be doing, like the checkbook or laundry.

These examples can help to illustrate the concepts of blocking and non-blocking code. Let’s think about this in programming terms. In this example, you’re like the CPU. While you’re moving the laundry around, you (the CPU) are busy and blocked from doing other work, like balancing the checkbook. But that’s okay because the task is relatively quick.

On the other hand, starting the washer and dryer does not block you from performing other tasks. It’s an asynchronous function because you don’t have to wait for it to finish. Once it’s started, you can go back to something else. This is called a context switch: the context of what you’re doing has changed, and the machine’s buzzer will notify you sometime in the future when the laundry task is complete.

As a human, this is how you work all the time. You naturally juggle multiple things at once, often without thinking about it. As a developer, the trick is how to translate this kind of behavior into code that does the same kind of thing.

## Programming Parents: Not as Easy as It Looks![](#programming-parents-not-as-easy-as-it-looks "Permanent link")

If you recognize yourself (or your parents) in the example above, then that’s great! You’ve got a leg up in understanding asynchronous programming. Again, you’re able to switch contexts between competing tasks fairly easily, picking up some tasks and resuming others. Now you’re going to try and program this behavior into virtual parents!

### Thought Experiment #1: The Synchronous Parent[](#thought-experiment-1-the-synchronous-parent "Permanent link")

How would you create a parent program to do the above tasks in a completely synchronous manner? Since watching the kids is a high-priority task, perhaps your program would do just that. The parent watches over the kids while waiting for something to happen that might need their attention. However, nothing else (like the checkbook or laundry) would get done in this scenario.

Now, you can re-prioritize the tasks any way you want, but only one of them would happen at any given time. This is the result of a synchronous, step-by-step approach. Like the synchronous web server described above, this would work, but it might not be the best way to live. The parent wouldn’t be able to complete any other tasks until the kids fell asleep. All other tasks would happen afterward, well into the night. (A couple of weeks of this and many real parents might jump out the window!)

### Thought Experiment #2: The Polling Parent[](#thought-experiment-2-the-polling-parent "Permanent link")

If you used [polling](<https://en.wikipedia.org/wiki/Polling_(computer_science)>), then you could change things up so that multiple tasks are completed. In this approach, the parent would periodically break away from the current task and check to see if any other tasks need attention.

Let’s make the polling interval something like fifteen minutes. Now, every fifteen minutes your parent checks to see if the washer, dryer or kids need any attention. If not, then the parent can go back to work on the checkbook. However, if any of those tasks _do_ need attention, then the parent will take care of it before going back to the checkbook. This cycle continues on until the next timeout out of the polling loop.

This approach works as well since multiple tasks are getting attention. However, there are a couple of problems:

1.  **The parent may spend a lot of time checking on things that don’t need attention:** The washer and dryer haven’t yet finished, and the kids don’t need any attention unless something unexpected happens.
2.  **The parent may miss completed tasks that do need attention:** For instance, if the washer finished its cycle at the beginning of the polling interval, then it wouldn’t get any attention for up to fifteen minutes! What’s more, watching the kids is supposedly the highest priority task. They couldn’t tolerate fifteen minutes with no attention when something might be going drastically wrong.

You could address these issues by shortening the polling interval, but now your parent (the CPU) would be spending more time context switching between tasks. This is when you start to hit a point of diminishing returns. (Once again, a couple of weeks living like this and, well… See the previous comment about windows and jumping.)

### Thought Experiment #3: The Threading Parent[](#thought-experiment-3-the-threading-parent "Permanent link")

“If I could only clone myself…” If you’re a parent, then you’ve probably had similar thoughts! Since you’re programming virtual parents, you can essentially do this by using threading. This is a mechanism that allows multiple sections of one program to run at the same time. Each section of code that runs independently is known as a thread, and all threads share the same memory space.

If you think of each task as a part of one program, then you can separate them and run them as threads. In other words, you can “clone” the parent, creating one instance for each task: watching the kids, monitoring the washer, monitoring the dryer, and balancing the checkbook. All of these “clones” are running independently.

This sounds like a pretty nice solution, but there are some issues here as well. One is that you’ll have to explicitly tell each parent instance what to do in your program. This can lead to some problems since all instances share everything in the program space.

For example, say that Parent A is monitoring the dryer. Parent A sees that the clothes are dry, so they take control of the dryer and begin unloading the clothes. At the same time, Parent B sees that the washer is done, so they take control of the washer and begin removing clothes. However, Parent B also needs to take control of the dryer so they can put the wet clothes inside. This can’t happen, because Parent A currently has control of the dryer.

After a short while, Parent A has finished unloading clothes. Now they want to take control of the washer and start moving clothes into the empty dryer. This can’t happen, either, because Parent B currently has control of the washer!

These two parents are now [deadlocked](https://realpython.com/intro-to-python-threading/#deadlock). Both have control of their own resource _and_ want control of the other resource. They’ll wait forever for the other parent instance to release control. As the programmer, you’d have to write code to work this situation out.

**Note:** Threaded programs allow you to create multiple, parallel paths of execution that all share the same memory space. This is both an advantage and a disadvantage. Any memory shared between threads is subject to one or more threads trying to use the same shared memory at the same time. This can lead to data corruption, data read in an invalid state, and data that’s just messy in general.

In threaded programming, the context switch happens under system control, not the programmer. The system controls when to switch contexts and when to give threads access to shared data, thereby changing the context of how the memory is being used. All of these kinds of problems are manageable in threaded code, but it’s difficult to get right, and hard to debug when it’s wrong.

Here’s another issue that might arise from threading. Suppose that a child gets hurt and needs to be taken to urgent care. Parent C has been assigned the task of watching over the kids, so they take the child right away. At the urgent care, Parent C needs to write a fairly large check to cover the cost of seeing the doctor.

Meanwhile, Parent D is at home working on the checkbook. They’re unaware of this large check being written, so they’re very surprised when the family checking account is suddenly overdrawn!

Remember, these two parent instances are working within the same program. The family checking account is a shared resource, so you’d have to work out a way for the child-watching parent to inform the checkbook-balancing parent. Otherwise, you’d need to provide some kind of locking mechanism so that the checkbook resource can only be used by one parent at a time, with updates.

## Using Python Async Features in Practice[](#using-python-async-features-in-practice "Permanent link")

Now you’re going to take some of the approaches outlined in the thought experiments above and turn them into functioning Python programs.

All of the examples in this article have been tested with Python 3.7.2. The `requirements.txt` file indicates which modules you’ll need to install to run all the examples. If you haven’t yet downloaded the file, you can do so now:

**Download Code:** [Click here to download the code you’ll use](https://realpython.com/bonus/async-features/) to learn about async features in Python in this tutorial.

You also might want to set up a [Python virtual environment](https://realpython.com/python-virtual-environments-a-primer/) to run the code so you don’t interfere with your system Python.

### Synchronous Programming[](#synchronous-programming "Permanent link")

This first example shows a somewhat contrived way of having a task retrieve work from a queue and process that work. A queue in Python is a nice [FIFO](<https://en.wikipedia.org/wiki/FIFO_(computing_and_electronics)>) (first in first out) data structure. It provides methods to put things in a queue and take them out again in the order they were inserted.

In this case, the work is to get a number from the queue and have a loop count up to that number. It prints to the console when the loop begins, and again to output the total. This program demonstrates one way for multiple synchronous tasks to process the work in a queue.

The program named `example_1.py` in the repository is listed in full below:

```python
import queue


def task(name, work_queue):
    if work_queue.empty():
        print(f"Task {name} nothing to do")
    else:
        while not work_queue.empty():
            count = work_queue.get()
            total = 0
            print(f"Task {name} running")
            for x in range(count):
                total += 1
            print(f"Task {name} total: {total}")


def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = queue.Queue()

    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        work_queue.put(work)

    # Create some synchronous tasks
    tasks = [(task, "One", work_queue), (task, "Two", work_queue)]

    # Run the tasks
    for t, n, q in tasks:
        t(n, q)


if __name__ == "__main__":
    main()
```

Let’s take a look at what each line does:

- **Line 1** imports the `queue` module. This is where the program stores work to be done by the tasks.
- **Lines 3 to 13** define `task()`. This function pulls work out of `work_queue` and processes the work until there isn’t any more to do.
- **Line 15** defines `main()` to run the program tasks.
- **Line 20** creates the `work_queue`. All tasks use this shared resource to retrieve work.
- **Lines 23 to 24** put work in `work_queue`. In this case, it’s just a random count of values for the tasks to process.
- **Line 27** creates a [list](https://realpython.com/python-lists-tuples/) of task tuples, with the parameter values those tasks will be passed.
- **Lines 30 to 31** iterate over the list of task tuples, calling each one and passing the previously defined parameter values.
- **Line 34** calls `main()` to run the program.

The task in this program is just a function accepting a string and a queue as parameters. When executed, it looks for anything in the queue to process. If there is work to do, then it pulls values off the queue, starts a [`for` loop](https://realpython.com/courses/python-for-loop/) to count up to that value, and outputs the total at the end. It continues getting work off the queue until there is nothing left and it exits.

When this program is run, it produces the output you see below:

```
Task One running
Task One total: 15
Task One running
Task One total: 10
Task One running
Task One total: 5
Task One running
Task One total: 2
Task Two nothing to do
```

This shows that `Task One` does all the work. The [`while` loop](https://realpython.com/courses/mastering-while-loops/) that `Task One` hits within `task()` consumes all the work on the queue and processes it. When that loop exits, `Task Two` gets a chance to run. However, it finds that the queue is empty, so `Task Two` prints a statement that says it has nothing to do and then exits. There’s nothing in the code to allow both `Task One` and `Task Two` to switch contexts and work together.

### Simple Cooperative Concurrency[](#simple-cooperative-concurrency "Permanent link")

The next version of the program allows the two tasks to work together. Adding a `yield` statement means the loop will yield control at the specified point while still maintaining its context. This way, the yielding task can be restarted later.

The `yield` statement turns `task()` into a [generator](https://realpython.com/introduction-to-python-generators/). A generator function is called just like any other function in Python, but when the `yield` statement is executed, control is returned to the caller of the function. This is essentially a context switch, as control moves from the generator function to the caller.

The interesting part is that control can be given _back_ to the generator function by calling `next()` on the generator. This is a context switch back to the generator function, which picks up execution with all function [variables](https://realpython.com/python-variables/) that were defined before the `yield` still intact.

The `while` loop in [`main()`](https://realpython.com/python-main-function/) takes advantage of this when it calls `next(t)`. This statement restarts the task at the point where it previously yielded. All of this means that you’re in control when the context switch happens: when the `yield` statement is executed in `task()`.

This is a form of cooperative multitasking. The program is yielding control of its current context so that something else can run. In this case, it allows the `while` loop in `main()` to run two instances of `task()` as a generator function. Each instance consumes work from the same queue. This is sort of clever, but it’s also a lot of work to get the same results as the first program. The program `example_2.py` demonstrates this simple [concurrency](https://realpython.com/python-concurrency/) and is listed below:

```python
import queue


def task(name, queue):
    while not queue.empty():
        count = queue.get()
        total = 0
        print(f"Task {name} running")
        for x in range(count):
            total += 1
            yield
        print(f"Task {name} total: {total}")


def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = queue.Queue()

    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        work_queue.put(work)

    # Create some tasks
    tasks = [task("One", work_queue), task("Two", work_queue)]

    # Run the tasks
    done = False
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
```

Here’s what’s happening in the code above:

- **Lines 3 to 11** define `task()` as before, but the addition of `yield` on Line 10 turns the function into a generator. This where the context switch is made and control is handed back to the `while` loop in `main()`.
- **Line 25** creates the task list, but in a slightly different manner than you saw in the previous example code. In this case, each task is called with its parameters as its entered in the `tasks` list variable. This is necessary to get the `task()` generator function running the first time.
- **Lines 31 to 36** are the modifications to the `while` loop in `main()` that allow `task()` to run cooperatively. This is where control returns to each instance of `task()` when it yields, allowing the loop to continue and run another task.
- **Line 32** gives control back to `task()`, and continues its execution after the point where `yield` was called.
- **Line 36** sets the `done` variable. The `while` loop ends when all tasks have been completed and removed from `tasks`.

This is the output produced when you run this program:

```
Task One running
Task Two running
Task Two total: 10
Task Two running
Task One total: 15
Task One running
Task Two total: 5
Task One total: 2
```

You can see that both `Task One` and `Task Two` are running and consuming work from the queue. This is what’s intended, as both tasks are processing work, and each is responsible for two items in the queue. This is interesting, but again, it takes quite a bit of work to achieve these results.

The trick here is using the `yield` statement, which turns `task()` into a generator and performs a context switch. The program uses this context switch to give control to the `while` loop in `main()`, allowing two instances of a task to run cooperatively.

Notice how `Task Two` outputs its total first. This might lead you to think that the tasks are running asynchronously. However, this is still a synchronous program. It’s structured so the two tasks can trade contexts back and forth. The reason why `Task Two` outputs its total first is that it’s only counting to 10, while `Task One` is counting to 15. `Task Two` simply arrives at its total first, so it gets to print its output to the console before `Task One`.

**Note:** All of the example code that follows from this point use a module called [codetiming](https://pypi.org/project/codetiming/) to time and output how long sections of code took to execute. There is a great article [here](https://realpython.com/python-timer/) on RealPython that goes into depth about the codetiming module and how to use it.

This module is part of the Python Package Index and is built by [Geir Arne Hjelle](https://realpython.com/team/gahjelle/), who is part of the _Real Python_ team. Geir Arne has been a great help to me reviewing and suggesting things for this article. If you are writing code that needs to include timing functionality, Geir Arne’s codetiming module is well worth looking at.

To make the codetiming module available for the examples that follow you’ll need to install it. This can be done with `pip` with this command: `pip install codetiming`, or with this command: `pip install -r requirements.txt`. The `requirements.txt` file is part of the example code repository.

### Cooperative Concurrency With Blocking Calls[](#cooperative-concurrency-with-blocking-calls "Permanent link")

The next version of the program is the same as the last, except for the addition of a [`time.sleep(delay)`](https://realpython.com/python-sleep/) in the body of your task loop. This adds a delay based on the value retrieved from the work queue to every iteration of the task loop. The delay simulates the effect of a blocking call occurring in your task.

A blocking call is code that stops the CPU from doing anything else for some period of time. In the thought experiments above, if a parent wasn’t able to break away from balancing the checkbook until it was complete, that would be a blocking call.

`time.sleep(delay)` does the same thing in this example, because the CPU can’t do anything else but wait for the delay to expire.

```python
import time
import queue
from codetiming import Timer


def task(name, queue):
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    while not queue.empty():
        delay = queue.get()
        print(f"Task {name} running")
        timer.start()
        time.sleep(delay)
        timer.stop()
        yield


def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = queue.Queue()

    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        work_queue.put(work)

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
```

Here’s what’s different in the code above:

- **Line 1** imports the [`time` module](https://realpython.com/python-time-module/) to give the program access to `time.sleep()`.
- **Line 3** imports the the `Timer` code from the `codetiming` module.
- **Line 6** creates the `Timer` instance used to measure the time taken for each iteration of the task loop.
- **Line 10** starts the `timer` instance
- **Line 11** changes `task()` to include a `time.sleep(delay)` to mimic an IO delay. This replaces the `for` loop that did the counting in `example_1.py`.
- **Line 12** stops the `timer` instance and outputs the elapsed time since `timer.start()` was called.
- **Line 30** creates a `Timer` [context manager](https://realpython.com/python-with-statement/) that will output the elapsed time the entire while loop took to execute.

When you run this program, you’ll see the following output:

```
Task One running
Task One elapsed time: 15.0
Task Two running
Task Two elapsed time: 10.0
Task One running
Task One elapsed time: 5.0
Task Two running
Task Two elapsed time: 2.0

Total elapsed time: 32.0
```

As before, both `Task One` and `Task Two` are running, consuming work from the queue and processing it. However, even with the addition of the delay, you can see that cooperative concurrency hasn’t gotten you anything. The delay stops the processing of the entire program, and the CPU just waits for the IO delay to be over.

This is exactly what’s meant by blocking code in Python async documentation. You’ll notice that the time it takes to run the entire program is just the cumulative time of all the delays. Running tasks this way is not a win.

### Cooperative Concurrency With Non-Blocking Calls[](#cooperative-concurrency-with-non-blocking-calls "Permanent link")

The next version of the program has been modified quite a bit. It makes use of Python async features using [asyncio/await](https://realpython.com/async-io-python/) provided in Python 3.

The `time` and `queue` modules have been replaced with the `asyncio` package. This gives your program access to asynchronous friendly (non-blocking) sleep and queue functionality. The change to `task()` defines it as asynchronous with the addition of the `async` prefix on line 4. This indicates to Python that the function will be asynchronous.

The other big change is removing the `time.sleep(delay)` and `yield` statements, and replacing them with `await asyncio.sleep(delay)`. This creates a non-blocking delay that will perform a context switch back to the caller `main()`.

The `while` loop inside `main()` no longer exists. Instead of `task_array`, there’s a call to `await asyncio.gather(...)`. This tells `asyncio` two things:

1.  Create two tasks based on `task()` and start running them.
2.  Wait for both of these to be completed before moving forward.

The last line of the program `asyncio.run(main())` runs `main()`. This creates what’s known as an [event loop](https://realpython.com/lessons/asyncio-event-loop/)). It’s this loop that will run `main()`, which in turn will run the two instances of `task()`.

The event loop is at the heart of the Python async system. It runs all the code, including `main()`. When task code is executing, the CPU is busy doing work. When the [`await` keyword](https://realpython.com/python-keywords/#the-await-keyword) is reached, a context switch occurs, and control passes back to the event loop. The event loop looks at all the tasks waiting for an event (in this case, an `asyncio.sleep(delay)` timeout) and passes control to a task with an event that’s ready.

`await asyncio.sleep(delay)` is non-blocking in regards to the CPU. Instead of waiting for the delay to timeout, the CPU registers a sleep event on the event loop task queue and performs a context switch by passing control to the event loop. The event loop continuously looks for completed events and passes control back to the task waiting for that event. In this way, the CPU can stay busy if work is available, while the event loop monitors the events that will happen in the future.

**Note:** An asynchronous program runs in a single thread of execution. The context switch from one section of code to another that would affect data is completely in your control. This means you can atomize and complete all shared memory data access before making a context switch. This simplifies the shared memory problem inherent in threaded code.

The `example_4.py` code is listed below:

```python
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
```

Here’s what’s different between this program and `example_3.py`:

- **Line 1** imports `asyncio` to gain access to Python async functionality. This replaces the `time` import.
- **Line 2** imports the the `Timer` code from the `codetiming` module.
- **Line 4** shows the addition of the `async` keyword in front of the `task()` definition. This informs the program that `task` can run asynchronously.
- **Line 5** creates the `Timer` instance used to measure the time taken for each iteration of the task loop.
- **Line 9** starts the `timer` instance
- **Line 10** replaces `time.sleep(delay)` with the non-blocking `asyncio.sleep(delay)`, which also yields control (or switches contexts) back to the main event loop.
- **Line 11** stops the `timer` instance and outputs the elapsed time since `timer.start()` was called.
- **Line 18** creates the non-blocking asynchronous `work_queue`.
- **Lines 21 to 22** put work into `work_queue` in an asynchronous manner using the `await` keyword.
- **Line 25** creates a `Timer` context manager that will output the elapsed time the entire while loop took to execute.
- **Lines 26 to 29** create the two tasks and gather them together, so the program will wait for both tasks to complete.
- **Line 32** starts the program running asynchronously. It also starts the internal event loop.

When you look at the output of this program, notice how both `Task One` and `Task Two` start at the same time, then wait at the mock IO call:

```
Task One running
Task Two running
Task Two total elapsed time: 10.0
Task Two running
Task One total elapsed time: 15.0
Task One running
Task Two total elapsed time: 5.0
Task One total elapsed time: 2.0

Total elapsed time: 17.0
```

This indicates that `await asyncio.sleep(delay)` is non-blocking, and that other work is being done.

At the end of the program, you’ll notice the total elapsed time is essentially half the time it took for `example_3.py` to run. That’s the advantage of a program that uses Python async features! Each task was able to run `await asyncio.sleep(delay)` at the same time. The total execution time of the program is now less than the sum of its parts. You’ve broken away from the synchronous model!

### Synchronous (Blocking) HTTP Calls[](#synchronous-blocking-http-calls "Permanent link")

The next version of the program is kind of a step forward as well as a step back. The program is doing some actual work with real IO by making HTTP requests to a list of URLs and getting the page contents. However, it’s doing so in a blocking (synchronous) manner.

The program has been modified to import [the wonderful `requests` module](https://realpython.com/python-requests/) to make the actual HTTP requests. Also, the queue now contains a list of URLs, rather than numbers. In addition, `task()` no longer increments a counter. Instead, `requests` gets the contents of a URL retrieved from the queue, and prints how long it took to do so.

The `example_5.py` code is listed below:

```python
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
```

Here’s what’s happening in this program:

- **Line 2** imports `requests`, which provides a convenient way to make HTTP calls.
- **Line 3** imports the the `Timer` code from the `codetiming` module.
- **Line 6** creates the `Timer` instance used to measure the time taken for each iteration of the task loop.
- **Line 11** starts the `timer` instance
- **Line 12** introduces a delay, similar to `example_3.py`. However, this time it calls `session.get(url)`, which returns the contents of the URL retrieved from `work_queue`.
- **Line 13** stops the `timer` instance and outputs the elapsed time since `timer.start()` was called.
- **Lines 23 to 32** put the list of URLs into `work_queue`.
- **Line 39** creates a `Timer` context manager that will output the elapsed time the entire while loop took to execute.

When you run this program, you’ll see the following output:

```
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
```

Just like in earlier versions of the program, `yield` turns `task()` into a generator. It also performs a context switch that lets the other task instance run.

Each task gets a URL from the work queue, retrieves the contents of the page, and reports how long it took to get that content.

As before, `yield` allows both your tasks to run cooperatively. However, since this program is running synchronously, each `session.get()` call blocks the CPU until the page is retrieved. **Note the total time it took to run the entire program at the end.** This will be meaningful for the next example.

### Asynchronous (Non-Blocking) HTTP Calls[](#asynchronous-non-blocking-http-calls "Permanent link")

This version of the program modifies the previous one to use Python async features. It also imports the [`aiohttp`](https://aiohttp.readthedocs.io/en/stable/) module, which is a library to make HTTP requests in an asynchronous fashion using `asyncio`.

The tasks here have been modified to remove the `yield` call since the code to make the HTTP `GET` call is no longer blocking. It also performs a context switch back to the event loop.

The `example_6.py` program is listed below:

```python
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
```

Here’s what’s happening in this program:

- **Line 2** imports the `aiohttp` library, which provides an asynchronous way to make HTTP calls.
- **Line 3** imports the the `Timer` code from the `codetiming` module.
- **Line 5** marks `task()` as an asynchronous function.
- **Line 6** creates the `Timer` instance used to measure the time taken for each iteration of the task loop.
- **Line 7** creates an `aiohttp` session context manager.
- **Line 8** creates an `aiohttp` response context manager. It also makes an HTTP `GET` call to the URL taken from `work_queue`.
- **Line 11** starts the `timer` instance
- **Line 12** uses the session to get the text retrieved from the URL asynchronously.
- **Line 13** stops the `timer` instance and outputs the elapsed time since `timer.start()` was called.
- **Line 39** creates a `Timer` context manager that will output the elapsed time the entire while loop took to execute.

When you run this program, you’ll see the following output:

```
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
```

Take a look at the total elapsed time, as well as the individual times to get the contents of each URL. You’ll see that the duration is about half the cumulative time of all the HTTP `GET` calls. This is because the HTTP `GET` calls are running asynchronously. In other words, you’re effectively taking better advantage of the CPU by allowing it to make multiple requests at once.

Because the CPU is so fast, this example could likely create as many tasks as there are URLs. In this case, the program’s run time would be that of the single slowest URL retrieval.

## Conclusion[](#conclusion "Permanent link")

This article has given you the tools you need to start making asynchronous programming techniques a part of your repertoire. Using Python async features gives you programmatic control of when context switches take place. This means that many of the tougher issues you might see in threaded programming are easier to deal with.

Asynchronous programming is a powerful tool, but it isn’t useful for every kind of program. If you’re writing a program that calculates pi to the millionth decimal place, for instance, then asynchronous code won’t help you. That kind of program is CPU bound, without much IO. However, if you’re trying to implement a server or a program that performs IO (like file or network access), then using Python async features could make a huge difference.

**To sum it up, you’ve learned:**

- What **synchronous programs** are
- How **asynchronous programs** are different, but also powerful and manageable
- Why you might want to write asynchronous programs
- How to use the built-in async features in Python

You can get the code for all of the example programs used in this tutorial:

**Download Code:** [Click here to download the code you’ll use](https://realpython.com/bonus/async-features/) to learn about async features in Python in this tutorial.

Now that you’re equipped with these powerful skills, you can take your programs to the next level!

# Author

## About Doug Farrell[](#about-doug-farrell "Permanent link")

![Image](https://robocrop.realpython.net/?url=https%3A//files.realpython.com/media/author-df.aa73a07afa57.jpg&w=200&h=200&mode=crop&sig=259baf8c71f368867f32293e2692905daaadf859)

Doug Farrell

Doug is a Python developer with more than 25 years of experience. He writes about Python on his personal website and works as a Senior Web Engineer with Shutterfly.

[More about Doug](https://realpython.com/team/dfarrell)
