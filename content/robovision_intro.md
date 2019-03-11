Title: Introducing Robovision
Date: March 10, 2019
Category: OpenCV
Tags: python, opencv, robotics

The FIRST robotics competition (FRC) challenges high school students to design and build a robot capable of performing multiple challenging tasks. These annual challenges typically involve computer vision components, such as identifying and using reflective markers to locate targets. High school computer science curriculum rarely covers software engineering topics, let alone advanced topics like computer vision.

To help FRC teams, I have written the robovision python library. This library includes functions useful for the types of vision tasks typically involved in an FRC competition. The goal of this library is to reduce and hide some of the complexity involved with target identification, measuring, field orienteering, etc.

Robovision is open source, licenced under the permissive MIT license, and free for all FRC teams to use. You can install it from <a href="https://pypi.org/project/robovision/" target="_blank">PyPI</a> or directly from the <a href="https://github.com/skypanther/robovision" target="_blank">GitHub repo</a>.

Some of the functions included in robovision are:

* Multi-threaded image acquisition from a web cam, IP cam (i.e. Axis cam), Raspberry Pi camera, or Jetson onboard gstreamer camera
* Lens distortion removal based on the camera calibrations created with the provided autocalibrate.py script
* Retroreflective target identification, contour finding, and geometry finding functions
* Image resizing, equalization, brightness and contrast adjustments, and more
* A preprocessor class, which enables you to set up a pipeline of functions that will be applied in series to an image.
* Overlay arrows, text, borders, or crosshairs on images
* Rolling (moving) average calculations

Robovision complements the <a href="https://robotpy.readthedocs.io/en/stable/" target="_blank">RobotPy library</a>. It does not duplicate functionality, nor is it meant to replace that excellent project. Team 1518 uses both robovision and the cscore and networktables components of RobotPy.

## Installation

Requirements:

* Python 3.5+ (2.x is not supported)
* OpenCV 3.4+ (4.x will probably work, but is untested)
* Numpy

Robovision is meant to run on a coprocessor (e.g. a Jetson or Raspberry Pi) and hasn't been tested on the RoboRio itself. While it probably works on a Windows computer, it was developed and is tested only on Mac OS and Linux systems.

Installation details are covered in the wiki's <a href="https://github.com/skypanther/robovision/wiki/Installation-and-System-Setup" target="_blank">Installation and System Setup</a> page.

## Example

Here's a sample of how you might use robovision to calculate the distance in inches to a 12" piece of retro-reflective tape held horizontally and face-on to an IP camera:

    #!python
    import cv2
    import robovision as rv

    source = "http://10.15.18.100/mjpg/video.mjpg"
    fl = 100  # Calculated apparent focal length of your camera
    cv2.namedWindow('CapturedImage', cv2.WINDOW_NORMAL)

    # connect to our streaming video source and start the capture thread
    vs = rv.get_video_stream(source)
    vs.start()
    # instantiate a robovision Target object which does all the work of finding
    # and isolating the retro-reflective tape
    target = rv.Target()
    target.set_color_range(lower=(60, 100, 100), upper=(100, 255, 255))
    while True:
        frame = vs.read_frame()
        # get a list of contours around objects within the color range set
        # above; these will be the retro-reflective tape assuming you're using
        # the standard AndyMark green LED light source
        contours = target.get_contours(frame)
        if len(contours) > 1:
            # draw a red border around each of the contours that were found
            cv2.drawContours(frame, contours, 0, (0, 0, 255), 3)
            # assuming you're holding the tape horizontally, you need only
            # the width (in pixels) of the detected object
            _, _, w, _ = target.get_rectangle(for_contour=contours[0])
            # Distance from formula: D’ = (W x F) / P
            d = 12 * fl / w
            print("Assuming a 12-inch retroreflective tape, it is {} inches away".format(d))
        cv2.imshow('CapturedImage', frame)
        # wait for Esc or q key and then exit
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord("q"):
            cv2.destroyAllWindows()
            vs.stop()
            break


### Examples and documentation

I include a selection of example scripts in the <a href="https://github.com/skypanther/robovision/tree/master/extras" target="_blank">extras folder</a> in the GitHub repo. While not really production ready, these show how to perform selected vision tasks that might be helpful for an FRC challenge. There's also a couple of scripts to help you do lens calibration (used to remove lens distortions, also called field flattening).

Be sure to check out the <a href="https://github.com/skypanther/robovision/wiki" target="_blank">project's wiki</a> for documentation on the library's classes and functions. You'll need the numpy and OpenCV python packages to use robovision. Some of the example scripts use additional libraries. 

FRC Team 1518, Raider Robotics used robovision successfully in its 2019 Deep Space Challenge bot. So, another good source of examples (as well as some "incomplete thoughts") is the <a href="https://github.com/Raider-Robotics-Team-1518/Jetson" target="_blank">team's GitHub repository</a>.

### Future

Looking ahead, the library needs even more simplification and abstraction to make it easy for FRC teams to use. Additional documentation and examples are also needed. I have not extensively tested or optimized the library for the Raspberry Pi (we're using a Jetson TX2, which has plenty of horsepower for our vision tasks). I very much welcome pull requests and contributions to the project.

\#omgrobots!
