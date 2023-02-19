Title: Acquiring images with OpenCV
Date: April 16, 2018
Category: OpenCV
Tags: opencv, python
Slug: acquiring-images

To manipulate an image, the first thing you must do is open it. OpenCV lets you open images and videos from files and cameras, both locally attached and on the network. Let's check it out.

## Still images

We'll start with the simple case of still images. This is probably best illustrated with some sample code:

    #!python
    import cv2

    # read an image from the current folder
    image = cv2.imread('cat.jpg')

    # or from another folder
    image = cv2.imread('images/cat.jpg')

    # then we'll just show it in an OpenCV window
    cv2.imshow('Photo', image)

In the above example, the `image` variable is a binary object representing the RGB data of your file. Keep in mind that internally, OpenCV represents these "backwards" as BGR images. That will matter if you use a different library, such as matplotlib, in your script which expects RGB image data.

OpenCV supports the most common image file formats, including JPG, PNG, WebP, TIF, and more.

### Errors and exception handling

The `imread` method does not raise a proper exception in the case the file doesn't exist. So, you can't wrap your code in a try/except block to handle errors. Instead, you'll need to check before calling `imread` with Python's usual file-handling functions, for example:

    #!python
    from os import path

    if path.isfile('cat.jpg'):
        image = cv2.imread('cat.jpg')
        ...

However, just because a file exists and can be opened by `imread` does not mean that you can successfully read image data from it. In such cases, the function will return `None` which you should test for:

    #!python
    image = cv2.imread('not_an_image.txt')
    if image is None:
    print('Could not read image data')

Note: OpenCV determines the file type by its contents, not its extension. So, if you renamed cat.jpg to cat.txt, the `imread()` function would still be able to read it as a JPG file.

## Video files and cameras

OpenCV lets you read video data from files and cameras. What's better, you use the same technique no matter the video source. First, you get a reference, or handle to the video source. Then, you read from that source frame by frame.

Strictly speaking, you use the `cv2.VideoCapture.open()` method to get a reference to your video source. However, OpenCV offers a shorter equivalent in the `cv2.VideoCapture()` method.

    VideoCapture(source[, options])

Where _source_ is one of:

- an integer, representing which locally attached webcam to read from. A value of `0` represents your built-in webcam if available.
- a string, representing a path to a local video file
- a string, representing the URL to a streaming network camera, such as an IP camera

Typically, you don't need to provide any options for the method. These flags would be used to specify the format of the data stream and other specifics. As with still images, OpenCV can typically figure out the video parameters automatically by examining the input data.

Here is a very typical loop used to read frames from a video source. In this simple example, we just show each frame in an OpenCV window. Within each loop, the script checks for a key-press and if the letter "q" was typed, we break out of the loop, which in this example would release the video source and end the program:

    #!python
    camera = cv2.VideoCapture(0)
    while True:
        # loop continuously reading frame-by-frame
        success, frame = camera.read()
        if success:
            # a frame was successfully read
            # we'll just show it in a window
            cv2.imshow("Live Video", frame)

            # if the 'q' key is pressed, stop the loop
            if cv2.waitKey(1) & 0xFF == ord("q"):
                camera.release()
                break
        else:
            # frame wasn't read, handle that problem, for example
            camera.release()
            break

### Errors and exceptions

As with reading still images, OpenCV does not offer proper exception handling when reading from a video source. If you specify a source that doesn't exist, you'll get an error like the following

    out device of bound (0-0): 1 opencv: camera failed to properly initialize!

(To create the preceding error, I used `camera = cv2.VideoCapture(1)` and since my laptop has just one camera, camera `1` doesn't exist.)

It's important to release the video source properly when you're done by calling the `release()` method. Failing to do so can leave your camera unusable. Below is an example of the error you get attempting to use the built-in camera on a Mac that was not released properly before.

    OpenCV: error in [AVCaptureDeviceInput initWithDevice:error:]
    OpenCV: Cannot Use FaceTime HD Camera (Built-in)
    OpenCV: camera failed to properly initialize!

If you end up in this state, you may have to restart your computer to recover. On the Mac, you can use the following command rather than restarting:

    sudo killall VDCAssistant

## Summary

There you have it, the ins-and-outs of aquiring image data to use with OpenCV.
