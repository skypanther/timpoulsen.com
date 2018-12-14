Title: Raspberry Pi for IoT
Date: December 14, 2018
Category: Making, Python
Tags: raspberry pi, making, python

I gave a presentation to the Buffalo Python meetup group in December. My talk centered around using the Raspberry Pi as a platform for IoT and embedded development. I want to share my presentation and the resources I mentioned here on my blog.

![Slide preview](../images/2018/2018DecBufPy.jpg)

View/download as a [PDF](../images/2018/2018DecBufPy.pdf), [PowerPoint](../images/2018/2018DecBufPy.pptx), or [Keynote](../images/2018/2018DecBufPy.key).

During my talk, I referred to a bunch of sites and resources. These included:


## Getting started with the Pi

* The [Raspberry Pi home page](https://www.raspberrypi.org/)
* [OS downloads](https://www.raspberrypi.org/downloads/), including Raspbian and more
* [Etcher](https://www.balena.io/etcher/), for copying OS images to an SD card
* The [Official Raspberry Pi Beginner's Guide](https://store.rpipress.cc/products/the-official-raspberry-pi-beginner-s-guide) looks to be a good starter book for younger RPi tinkerers.

## Development tools and docs

* [Visual Studio Code](https://code.headmelted.com/) for the Raspberry Pi
* [Pi Wheels](www.piwheels.org) precompiled python libraries
* [PiCamera](https://picamera.readthedocs.io) docs

## Blogs and tutorial sites

* [Adafruit](https://learn.adafruit.com/) offers many great tutorials on the Raspberry Pi, Arduino, and other electronics topics. Their [GitHub account](https://github.com/adafruit) has tons of free code, too.
* [SparkFun](https://learn.sparkfun.com/) has great electronics tutorials, more towards the microcontroller (Arduino) type level than the Pi.
* [Pololu](https://www.pololu.com/blog)'s blog has some info, but unlike some other vendors, their individual product listings often come with sample code and how-to information.
* The [PyImageSearch blog](https://www.pyimagesearch.com/) is a great resource for OpenCV and computer vision. Adrian, the author, often includes Raspberry Pi specifics for his posts, though most can also be implemented on other platforms. I specifically mentioned his [motion detection / tracking post](www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/) (and its [second part](https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/))
* And while we're on the topic of OpenCV, Satya Mallick's [LearnOpenCV.com](https://www.learnopencv.com/) blog has tons of great computer vision information and he generally posts both Python and C++ code for every example.
* And humbly, my blog right here

## Stores / resellers

* [Adafruit](https://www.adafruit.com/) - Pi, Arduino, and other electronic components
* [SparkFun](https://www.sparkfun.com/) - Generally a bit more Arduino/microcontroller oriented components
* [Pololu](https://www.pololu.com/) - Robotics, electronics, and other components.
* I usually purchase Raspberry Pis from Amazon. Just be sure you're getting the model you want (the 3B+ is the current model) since many vendors are still selling the older boards.

**Note:** Unlike earlier models, the 3B+ has somewhat stringent power demands. You'll need a 5v power brick that has a 2.4 amps or greater output rating. That old cell phone charger you've got probably won't cut it.


## My projects

Disclosure, the code here sucks and is nothing I'd show as part of a job interview. But, it gets the job done.

* My [PiLit Christmas light controller](https://github.com/skypanther/PiLit) project
* And my someday-I'll-actually-finish-it [automated cat feeder](https://github.com/skypanther/catfeeder)
