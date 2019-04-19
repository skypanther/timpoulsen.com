Title: Multiprocessing in Python
Date: April 15, 2019
Category: Python
Tags: python
Status: draft

Modern CPUs typically feature multiple cores, which in some sense is like having multiple computers at your disposal. By default, your Python code will run on one core. But when performance is critical, you can use multiple cores to run operations simultaneously. In this article, I'll walk through how we used multiprocessing in our FIRST Robotics code to run our scripts across all four cores of our Jetson TX2 board.

Python supports both multithreading and multiprocessing. Judging by the number of StackOverflow articles, there's a ton of confusion surrounding these terms. There are many <a href="https://realpython.com/python-concurrency/" target="_blank">great articles</a> explaining the differences and nuances of multithreading and multiprocessing. Here's my take:

* Multithreading - run portions of your code **asynchronously** so that your script doesn't have to wait for **I/O bound operations**; but all your code runs on the same CPU core, and **shares the same memory and variable space.**
* Multiprocessing - run portions of your code **simultaneously** across multiple cores so that you script doesn't have to wait for **CPU bound operations**; because your code runs across multiple cores, each process has its own **separate memory and variable space.**

Use multithreading if your script needs to access data across the network, read a lot of data from disk, or do other I/O bound operations. Multithreading isn't really running code simultaneously. It's just not stopping everything while waiting for the I/O operation to finish. 

Use multiprocessing if your script does a lot of computation, such as processing image frames from a webcam stream. Multiprocessing can actually run code simultaneously. Though, sharing information between processes is more difficult.

## Multiprocess-bot

While we used both on our 2019 FRC bot, I'm going to focus on multiprocessing. Here are the tasks we programmed our Jetson to do:

* One process captured frames from an IP camera, did target identification and field orientation calculations, then wrote the results to NetworkTables so that the data was available to the robot and driver computers.
* Another process captured frames from a pair of web cams, read field &amp; robot data from the NetworkTables, and used it to create custom overlays atop the video feeds. Then we streamed those processed feeds across the network to the driver computer.
* And we had a third process that acted as a communication hub between those processes and managed them.










Question 4 basically says don't bother using multithreading
https://www.codementor.io/sheena/essential-python-interview-questions-du107ozr6






first paragraph

Syntax highlighting with & without line numbers

    :::python
    print("The triple-colon syntax will *not* show line numbers.")

To display line numbers, use a path-less shebang instead of colons:

    #!python
    print("The path-less shebang syntax *will* show line numbers.")

    #!javascript
    sample code block

Include font-awesome symbols like this
<i class="fa fa-heart red"></i>