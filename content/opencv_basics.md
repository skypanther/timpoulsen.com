Title: OpenCV Basics
Date: April 15, 2018
Category: OpenCV
Tags: opencv, python

OpenCV is a library of computer vision functions available for C++, Java, Python, and more on Windows, Linux, OS X, Android, and iOS. The OpenCV project began way back in 1999 and has been continually expanded and improved since then.

This article and the others on this site focus on OpenCV-Python. As the OpenCV site puts it, "_OpenCV-Python is a library of Python bindings_" for OpenCV. What they mean by that is the core functionality of OpenCV is performed by compiled C++ code (so its fast) yet is programmed from Python (which means it's easier to use).

## What can you do with OpenCV?

Here's a short list of what's possible with OpenCV:

* Read an image from a file, a USB web cam, an IP cam, and more
* Convert an image to another color space: RGB, HSV, LAB, YCrCb, grayscale, etc.
* Blur or sharpen an image
* Add noise to or remove noise from (denoise) an image
* Resize, rotate, warp, and adjust perspective of an image
* Extract portions of an image
* Find the edges of objects in the image
* Get the outlines (contours) of objects in the image and find the dimensions, area, and more about those contours

Of course, you can do all the above operations on a video source too, with both files and video streams.

## Installing OpenCV

For Python environments, installing OpenCV is pretty simple. You'll need to choose between installing just OpenCV or the contributed modules as well. The "contrib" modules are extra functions provided by the community. Popular and well-written contrib modules sometimes get pulled into the core OpenCV distribution. However, not all of them are error free or fully optimized. 

To install the core OpenCV Python version:

	pip install opencv-python

To install the version containing the contrib modules:

	pip install opencv-contrib-python

(The above commands will work just fine if you're using the Anaconda Python distribution, which I recommend you use.)

Mac users can also install OpenCV using <a href="http://brew.sh/" target="_blank">Homebrew</a> and Linux users can sometimes use their package manager (e.g. apt-get). You can even <a href="/compiling-opencv.html" target="_blank">compile OpenCV from its source code version</a>. You would do this to get the newest version or to get a version tailored to your specific computer.

## Learning to use OpenCV

The <a href="https://docs.opencv.org/" target="_blank">OpenCV docs</a> are not particularly beginner-friendly. Fortunately, there are many great resources for learning OpenCV. A few sites I recommend you check out are:

* The official <a href="https://docs.opencv.org/3.4.1/d6/d00/tutorial_py_root.html" target="_blank">OpenCV Python tutorials</a>
* <a href="https://www.pyimagesearch.com" target="_blank">www.pyimagesearch.com </a>
* <a href="http://www.learnopencv.com" target="_blank">www.learnopencv.com</a>

And of course, check back here too. In future articles on this site, I will cover how you can use OpenCV to perform some interesting and fun operations on images and video.