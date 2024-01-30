Title: Multiprocessing in Python
Date: April 15, 2019
Category: Python
Tags: python

Modern CPUs typically feature multiple cores, which in some sense is like having multiple computers at your disposal. By default, your Python code will run on one core. But when performance is critical, you can use multiple cores to run operations simultaneously. In this article, I'll walk through how we used multiprocessing in our FIRST Robotics code to run our scripts across all four cores of our Jetson TX2 board.

Python supports both multithreading and multiprocessing. Judging by the number of StackOverflow posts on the topic, there's a ton of confusion surrounding these terms. There are many <a href="https://realpython.com/python-concurrency/" target="_blank">articles</a> explaining the differences and nuances of multithreading and multiprocessing. Here's my take:

- Multithreading &mdash; run portions of your code **asynchronously** so that your script doesn't have to wait for **I/O bound operations**; but all your code runs on the same CPU core, and **shares the same memory and variable space.**
- Multiprocessing &mdash; run portions of your code **simultaneously** across multiple cores so that you script doesn't have to wait for **CPU bound operations**; because your code runs across multiple cores, each process has its own **separate memory and variable space.**

Use multithreading if your script needs to access data across the network, read a lot of data from disk, or do other I/O bound operations. Multithreading isn't really running code simultaneously. It's just not stopping everything while waiting for the I/O operation to finish.

Use multiprocessing if your script does a lot of computation, such as processing image frames from a webcam stream. You might employ multithreading to do the camera I/O. But multiprocessing would let you do the processing simultaneously with other code your script might perform. Sharing information between processes is more difficult since processes don't share memory or variables.

## Multiprocess-bot

While we used both on our 2019 FRC bot, I'm going to focus on multiprocessing. Here are the tasks we programmed our Jetson to do:

- One process captured frames from an IP camera, did target identification and field orientation calculations, then wrote the results to NetworkTables so that the data was available to the robot and driver computers.
- Another process captured frames from a pair of web cams, received data via a queue, and used that data to create custom overlays atop the video feeds. Then it streamed those processed feeds across the network to the driver computer.
- And we had a third process that instantiated and managed those processes.

## Starting multi-process scripts

Let's start by seeing how we can start our multiple processes. (You might not want to actually run code like this till I cover how to stop the processes a bit later in this article.) In <a href="https://github.com/Raider-Robotics-Team-1518/Jetson/blob/master/parallelized/main.py" target="_blank">the main.py file</a>, we import the two custom classes of our bot program, and then call their `start()` methods:

    #!python
    # import our bot-specific classes
    from camstreamer import Camstreamer
    from targeting import Targeting

    if __name__ == "__main__":
        camstreamer_process = Camstreamer(...)
        target_process = Targeting(...)

        camstreamer_process.start()
        target_process.start()

That part looks pretty standard. The magic that enables multiprocessing is actually put in those custom classes. Let's take a look at the (simplified) code of the <a href="https://github.com/Raider-Robotics-Team-1518/Jetson/blob/master/parallelized/targeting.py" target="_blank">targeting.py script</a>:

    #!python
    from multiprocessing import Process

    class Targeting(Process):
        def __init__(self, ...):
            super(Targeting, self).__init__()
            # other initialization stuff here

        def run(self):
            # do the work of your class in this method

Some key points here: we import Process and then inherit from it when defining our class. This gives our class the capabilities to run as a distinct process. Then, as the first statement in our class's init method, we call the superclass's init method. For probably no good reason, I'm using the older Python 2.x syntax in that line. With Python 3.x, you can simplify that to `super().__init__()` (or use the older syntax). For more information on super(), check <a href="https://www.pythonforbeginners.com/super/working-python-super-function" target="_blank">here</a> and <a href="https://stackoverflow.com/questions/576169/understanding-python-super-with-init-methods" target="_blank">here</a>.

As you saw above, we'll call our class's `start()` method to actually start the process. But you don't provide a start method in your subclass. Instead, you have to create a method named `run()`. The inherited start() method will call your run() method. It seems a little weird, but that's how it works.

## Pipes and Queues

As I mentioned above, process don't share memory or variables. To communicate between processes, we need to use <a href="https://docs.python.org/3/library/multiprocessing.html#pipes-and-queues" target="_blank">pipes or queues</a>. Pipes are fast, one-way communication channels between a sender/receiver pair &mdash; put a message in at one end and it's immediately available at the other. Multiprocessing queues are two-way channels between multiple senders and receivers. They work like other FIFO queues you might be familiar with &mdash; the sender places a message onto the queue, the receiver pulls off the first-available message on the queue.

We used queues to share field / positional data between the processes. The targeting script would calculate its values and put them into the queue. The camera streamer class would pull values off the queue and use them in constructing the overlays. Let's see how that was accomplished.

In <a href="https://github.com/Raider-Robotics-Team-1518/Jetson/blob/master/parallelized/main.py" target="_blank">the main.py file</a>, we create the queue instance and pass it to each of the processes that will use it. In this way, each process has a reference to the queue in its memory space. (Only thread/process-safe constructs, like Pipes and Queues can be shared between processes like this.)

    #!python
    from multiprocessing import Queue

    if __name__ == "__main__":
        targeting_queue = Queue()
        camstreamer_process = Camstreamer(targeting_queue=targeting_queue ...)
        target_process = Targeting(targeting_queue=targeting_queue ...)

To write data to the queue, the <a href="https://github.com/Raider-Robotics-Team-1518/Jetson/blob/master/parallelized/targeting.py" target="_blank">targeting.py script</a> just needed to call `put()` on the queue reference passed to the class, like this:

    #!python
    self.targeting_queue.put(field_data)

Our bot's <a href="https://github.com/Raider-Robotics-Team-1518/Jetson/blob/master/parallelized/camstreamer.py" target="_blank">camera streamer class</a> read data from the queue. In that script, we used the `get_nowait()` method to read values from the queue. We could have used the `get()` method. However that function is blocking, meaning your script would pause till data was available on the queue. The `get_nowait()` method doesn't pause for data to be available, so it is faster. But it will throw an exception if there's nothing on the queue to read. To handle that, we just wrapped it in a try/except block, like this:

    #!python
    try:
        field_data = self.targeting_queue.get_nowait()
        # use the field data to draw the overlays
        # ...
    except Empty:
        # exception thrown if there's nothing in the queue to read
        pass

We probably could have used a pipe for this communication, since it was a one-way stream. But, a queue has the advantage of holding multiple values. So, if the sender script gets ahead, messages will still be available to be processed when the reader is available. Pipes pass just a single value. If a new one is written before the previous value is read it will "push" the first value out of the pipe.

### Stopping background processes

Once a script is launched as a separate process, it will run till stopped (or you kill it at the operating system level). During the competition, we were fine with the scripts running till we shut down our Jetson board. But, that's not typically how you'd manage your multiprocessing scripts.

Classes that inherit from Process have a `terminate()` method. When called, it will abruptly halt the process. If you need to close connections or otherwise gracefully stop your script, you'll want to signal it that it's about to be terminated. Once the process finishes its cleanup, then you call terminate().

In our bot program, we implemented this signalling using Pipes. In main.py, we listened for the Escape or "q" key to be pressed. When that happened, we sent a message across each child process's pipe that a shutdown was imminent. The child scripts would then stop their actions and clean up. After a brief delay, main.py would terminate the processes.

Looking again at main.py:

    #!python
    from multiprocessing import Queue, Pipe

    stop_pipes = []

    if __name__ == "__main__":
        cs_reader, cs_writer = Pipe(duplex=False)
        trgt_reader, trgt_writer = Pipe(duplex=False)
        stop_pipes.append(cs_writer)
        stop_pipes.append(trgt_writer)
        targeting_queue = Queue()
        camstreamer_process = Camstreamer(targeting_queue=targeting_queue, stop_pipe=cs_reader)
        target_process = Targeting(targeting_queue=targeting_queue, stop_pipe=trgt_reader, ...)
        ...

        while True:
            # wait for Esc or q key and then exit
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord("q"):
                cv2.destroyAllWindows()
                for pipe in stop_pipes:
                    pipe.put("stop")
                time.sleep(2)
                camstreamer_process.terminate()
                target_process.terminate()
                exit()

When instantiating a pipe, you get back a tuple whose values represent the read and write ends of the pipe. As shown in the snippet above, we created those pipe instances and passed the read ends to our child processes. In main.py's while loop, we use the write ends of the pipes (which were stored in a list) to put the string "stop" onto the pipe when the user signaled to quit.

In our child processes, all the computation was done inside an endless `while True:` loop. At the start of each iteration, we'd poll to see if data was available on the pipe. If so, and if it were the string "stop" we'd break out of the loop.

    #!python
    def run(self):
        ...
        while True:
            if self.stop_pipe.poll():
                # try reading from the stop pipe; if it's not empty
                # this block will work, and we'll exit the while
                # loop and terminate the script
                stop = self.stop_pipe.recv()
                if stop == "stop":
                    break

Pipes are great for this sort of one-way communication. The main.py control script sent out stop messages, and the child messages listened for those messages.
