Title: Acquiring images with OpenCV
Date: April 16, 2018
Category: OpenCV
Tags: opencv, python
Slug: acquiring-images
Summary: Acquiring images from files and video cameras with OpenCV
Status: draft

Of course, to manipulate an image, the first thing you must do is open it. OpenCV lets you open images from files and cameras. Likewise, you can open video files and streaming sources. Let's check it out.

Let's start super simple:

    #!python
    import cv2
    # read an image from the current folder
    image = cv2.imread("cat.jpg")
    
    # or from another folder
    image = cv2.imread("images/cat.jpg")



It's important to close the video source properly when you're done. Failing to do so can leave your camera unusable until you restart (or find and kill the right process). Below is an example of the error you get attempting to use a camera that was not released properly before.

    OpenCV: error in [AVCaptureDeviceInput initWithDevice:error:]
    2018-04-21 22:18:53.431 python3[55780:1624005] OpenCV: Cannot Use FaceTime HD Camera (Built-in)
    OpenCV: camera failed to properly initialize!
