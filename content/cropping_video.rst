Handling mouse events in OpenCV
###############################

:date: 2018-05-21
:tags: opencv
:category: OpenCV

For a project I'm working on, I need to select a region of interest in a video frame and extract info about that region. Fortunately, that's a pretty simple task to do in OpenCV. In this article, I'll show you how to detect and react to mouse actions, such as clicking and moving. Then, as an example of what to do with that sort of functionality, we'll see how to crop an image to the dimensions selected.

You'll need Python and OpenCV installed. I'm using Python 3.6 (Anaconda) and OpenCV 3.4 myself. Open your favorite text editor and create a file named **crop_image.py** and enter the following code:

.. code-block:: python
    :linenos: table

    import argparse
    import cv2

    coords = []
    drawing = False

    def main():

    def get_image(source):

    def click_and_crop(event, x, y, flag, image):

    if __name__ == "__main__":
        main()

That gives us the shell of the file we'll fill in throughout the rest of this article. We'll need the argparse and cv2 (OpenCV) libraries, as well as a couple of global variables. We'll have a couple of functions plus ``main()`` and the code to call ``main()`` when we run the script. 

Let's fill in the rest of ``main()``:

.. code-block:: python
    :linenos: table
    :linenostart: 7

    def main():
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", help="Path to the image")
        args = vars(ap.parse_args())
        image_source = args["image"] if args["image"] else 0
        # now get our image from either the file or built-in webcam
        image = get_image(image_source)
        if image is not None:
            # show the captured image in a window
            cv2.namedWindow('CapturedImage', cv2.WINDOW_NORMAL)
            cv2.imshow('CapturedImage', image)
            # specify the callback function to be called when the user
            # clicks/drags in the 'CapturedImage' window
            cv2.setMouseCallback('CapturedImage', click_and_crop, image)
            while True:
                # wait for Esc or q key and then exit
                key = cv2.waitKey(1) & 0xFF
                if key == 27 or key == ord("q"):
                    print('Image cropped at coordinates: {}'.format(coords))
                    cv2.destroyAllWindows()
                    break

That's a good chunk of code. Let's walk through what it's doing. Using argparse, the script will look for and parse command-line arguments. This script will accept a single argument (either ``-i`` or ``--image``) to specify an image file to load. We'll store the value in an ``image_source`` variable on line 12. If no image is specified, we'll store ``0`` in the variable -- that will tell the script to use the default webcam on the system as the image source.

One line 14, we call our ``get_image()`` function (which we've yet to write) to load our image. If we successfully load the image, the statements in the ``if`` block will run. line 17 createa a named ``cv2.imshow`` window and the next line shows the image in that window.

Line 21 is perhaps the key line here. With ``setMouseCallback()`` we specify which window to listen for mouse events on ('CapturedImage'), what function to call each time there's a mouse event (a click, drag, move, etc.), as well as an optional third parameter. The ``cv2.setMouseCallback()`` function lets us pass whatever value we want in that third parameter. In the docs and other examples, you'll typically see it named generically as ``param`` for this reason. We'll use it to pass the image to that function.

Finally, we want the image window to remain open while the rest of the script operates. So, we use a while loop. In each iteration of the loop, we use the ``cv.waitKey()`` function to listen for a key press. If the key pressed is the escape key (value 27) or the letter q (the script would actually receive the ordinal value of the character 'q'), then we destroy all the cv2 windows and break out of the loop, ending the script.

There's the main logic of our script -- get an image, show it, then watch for mouse events and call a function when they happen. We've got a couple of other functions to write. Let's tackle ``get_image()`` first.

.. code-block:: python
    :linenos: table
    :linenostart: 30

    def get_image(source):
        # open the camera, grab a frame, and release the camera
        cam = cv2.VideoCapture(source)
        image_captured, image = cam.read()
        cam.release()
        if (image_captured):
            return image
        return None

This function is pretty straightforward. We'll use ``cv2.VideoCapture()`` to open whatever source it's passed (which will be either a filename or ``0`` for the webcam). It will read a single frame, then return the captured image.

The bigger function is ``click_and_crop()`` which is our event handler. Let's see this one in stages.

.. code-block:: python
    :linenos: table
    :linenostart: 39

    def click_and_crop(event, x, y, flag, image):
        """
        Callback function, called by OpenCV when the user interacts
        with the window using the mouse. This function will be called
        repeatedly as the user interacts.
        """
        # get access to the two global variables we'll need
        global coords, drawing

Here we see the function signature. When called, the function will be passed five arguments. The first is the event, such as the left button being pressed down (``cv2.EVENT_LBUTTONDOWN``). Next comes the x/y coordinates of the event. I could not find documentation on the ``flag`` parameter, other than the docs saying it was an integer. In testing, it appears to identify the event type and modifier keys. For example on my Mac, while moving the mouse, ``flag`` is 0. Holding down the Control key while moving the mouse, it was 8. Holding down Shift and moving was 16. Since this may vary by platform, test before using this parameter.

The last param, ``image``, corresponds to whatever third parameter we passed in the ``cv2.setMouseCallback()`` call. In our case, our call looks like ``cv2.setMouseCallback('CapturedImage', click_and_crop, image)`` where we're passing the captured image in that parameter.

Next, we're going to handle three different mouse events associated with cropping an image. First, the user will click the mouse down at the top-left corner. Then, they'll drag down to the bottom right. And third, they'll release the mouse button. I'll cover these three separately. As you examine this code, remember, this function will be called repeatedly, every time there's a mouse event (such as moving the mouse over the image).

.. code-block:: python
    :linenos: table
    :linenostart: 47

        if event == cv2.EVENT_LBUTTONDOWN:
            # user has clicked the mouse's left button
            drawing = True
            # save those starting coordinates
            coords = [(x, y)]

When the user clicks the button down, we'll set our global ``drawing`` variable to True. We'll use this for tracking state in the next sections. Then, we store the x/y coordinates of the mouse down event in our global ``coords`` list.

.. code-block:: python
    :linenos: table
    :linenostart: 52

        elif event == cv2.EVENT_MOUSEMOVE:
            # user is moving the mouse within the window
            if drawing is True:
                # if we're in drawing mode, we'll draw a green rectangle
                # from the starting x,y coords to our current coords
                clone = image.copy()
                cv2.rectangle(clone, coords[0], (x, y), (0, 255, 0), 2)
                cv2.imshow('CapturedImage', clone)

The user will move their mouse all over the image, even when they're not trying to crop it. We want this section of the code to run only if they've clicked down the mouse button. For that reason, we check the ``drawing`` variable set in the mouse down portion of the function. When that's true, we'll create a clone of our original image. Next, we'll draw a rectangle on the clone with the top-left corner at ``coords[0]`` (where the user clicked the mouse button down) and the current x/y coordinates. We'll draw a green outline (remember, OpenCV specifies the colors in blue-green-red order) with a width of 2. Finally, we show that image in our CapturedImage window.

.. code-block:: python
    :linenos: table
    :linenostart: 60

        elif event == cv2.EVENT_LBUTTONUP:
            # user has released the mouse button, leave drawing mode
            # and crop the photo
            drawing = False
            # save our ending coordinates
            coords.append((x, y))
            if len(coords) == 2:
                # calculate the four corners of our region of interest
                ty, by, tx, bx = coords[0][1], coords[1][1], coords[0][0], coords[1][0]
                # crop the image using array slicing
                roi = image[ty:by, tx:bx]
                height, width = roi.shape[:2]
                if width > 0 and height > 0:
                    # make sure roi has height/width to prevent imshow error
                    # and show the cropped image in a new window
                    cv2.namedWindow("ROI", cv2.WINDOW_NORMAL)
                    cv2.imshow("ROI", roi)

Finally, we handle the case when the user releases the mouse button. This is the bottom-right corner of the cropping rectangle. We set ``drawing`` back to False so we stop processing mouse-move events. We append the new x/y coordinates to our global list. Assuming something didn't go wrong, that list will have two members. 

On line 70, we crop the image. OpenCV images are represented as Numpy arrays of pixel values. We're using array slicing, in perhaps a non-inuitive way. Let's step back to line 68, where we grab the y values from the top-left and bottom-right corners (so ``ty`` and ``by``), and then the x values from the two corners (``tx`` and ``bx``) out of our global ``coords`` list.

We're ready to crop the image. OpenCV images are represented as Numpy arrays of pixel values. Since the image is just an array, we can use array slicing to select a portion of it -- in other words, to crop it. On line 68, we grab the y values from the top-left and bottom-right corners (so ``ty`` and ``by``), and then the x values from the two corners (``tx`` and ``bx``) out of our global ``coords`` list. Then on line 70, we crop by slicing the ``image`` array to those ty/by, tx/bx values and storing the "region of interest" in the ``roi`` variable.

If the user were to select a very small slice, such that either the width or height were treated as zero, the ``imshow()`` function would throw an error. To avoid that, we'll calcualte the height and width of the cropped image by grabbing the first two members of the roi's shape. We do our zero-test and then show the ``roi`` image in a new OpenCV window.

And that's it! If you haven't so far, try it out. 

.. code-block:: bash

    python3 crop_image.py

Click, drag, and release on the "CapturedImage" window and you'll get a new window with the cropped portion of your original. It may show up behind other windows you have open. (That's an annoying OpenCV bug on some platforms.)

The whole shebang
-----------------

Finally, let's close by seeing the entire script. Hopefully you've typed in the code as we went and didn't just copy & paste it. But this here will let you check your work against my original.

.. code-block:: python
    :linenos: table

    import argparse
    import cv2

    coords = []
    drawing = False

    def main():
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", help="Path to the image")
        args = vars(ap.parse_args())
        image_source = args["image"] if args["image"] else 0
        # now get our image from either the file or built-in webcam
        image = get_image(image_source)
        if image is not None:
            # show the captured image in a window
            cv2.namedWindow('CapturedImage', cv2.WINDOW_NORMAL)
            cv2.imshow('CapturedImage', image)
            # specify the callback function to be called when the user
            # clicks/drags in the 'CapturedImage' window
            cv2.setMouseCallback('CapturedImage', click_and_crop, image)
            while True:
                # wait for Esc or q key and then exit
                key = cv2.waitKey(1) & 0xFF
                if key == 27 or key == ord("q"):
                    print('Image cropped at coordinates: {}'.format(coords))
                    cv2.destroyAllWindows()
                    break

    def get_image(source):
        # open the camera, grab a frame, and release the camera
        cam = cv2.VideoCapture(source)
        image_captured, image = cam.read()
        cam.release()
        if (image_captured):
            return image
        return None

    def click_and_crop(event, x, y, flag, image):
        """
        Callback function, called by OpenCV when the user interacts
        with the window using the mouse. This function will be called
        repeatedly as the user interacts.
        """
        # get access to a couple of global variables we'll need
        global coords, drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            # user has clicked the mouse's left button
            drawing = True
            # save those starting coordinates
            coords = [(x, y)]
        elif event == cv2.EVENT_MOUSEMOVE:
            # user is moving the mouse within the window
            if drawing is True:
                # if we're in drawing mode, we'll draw a green rectangle
                # from the starting x,y coords to our current coords
                clone = image.copy()
                cv2.rectangle(clone, coords[0], (x, y), (0, 255, 0), 2)
                cv2.imshow('CapturedImage', clone)
        elif event == cv2.EVENT_LBUTTONUP:
            # user has released the mouse button, leave drawing mode
            # and crop the photo
            drawing = False
            # save our ending coordinates
            coords.append((x, y))
            if len(coords) == 2:
                # calculate the four corners of our region of interest
                ty, by, tx, bx = coords[0][1], coords[1][1], coords[0][0], coords[1][0]
                # crop the image using array slicing
                roi = image[ty:by, tx:bx]
                height, width = roi.shape[:2]
                if width > 0 and height > 0:
                    # make sure roi has height/width to prevent imshow error
                    # and show the cropped image in a new window
                    cv2.namedWindow("ROI", cv2.WINDOW_NORMAL)
                    cv2.imshow("ROI", roi)

    if __name__ == "__main__":
        main()

In this article, you saw how to detect and react to mouse actions, such as clicking and moving. Then, as an example of what to do with that sort of functionality, I showed you how to crop an image to the dimensions selected. In a future article, I will show you how to extract information from that region of interest, such as the predominant color.