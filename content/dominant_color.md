Title: Finding the dominant color
Date: 2018-07-10
Category: OpenCV
Tags: opencv, python
Status: draft

A common way to isolate or find an object in an image is to look for its color. You specify a range of colors, then use OpenCV to identify regions in an image that contain colors within that range. But, even if you know the exact color of your target, lighting, shadows, and your camera's sensor will alter the detected color. So, how do you best determine the color range to use?

In this article, I'll explore some different methods to work with colors. By the end, I'll show you how to <a href="https://www.timpoulsen.com/2018/handling-mouse-events-in-opencv.html">select a region of interest</a> within an image, then get the exact range of colors needed to isolate that object in a live video stream.

Let's say your goal is to isolate the puppy in this image. You'll notice that his fur color varies between an off-white to a golden tan. The toy he has is only a bit darker red-brown. 

<img src="../images/2018/puppy.jpg" width="480" title="Puppy"/>

Your first attempt might be to take an average of the colors to find the midpoint of his range of colors. Of course, you wouldn't want to include the grass in the average. Assuming a cropped version of just the puppy, you could use this script to calculate the average color:

    #!python
    import cv2
    import numpy as np

    img = cv2.imread('puppy_cropped.jpg')
    height, width, _ = np.shape(img)

    # calculate the average color of each row of our image
    avg_color_per_row = np.average(img, axis=0)

    # calculate the averages of our rows
    avg_colors = np.average(avg_color_per_row, axis=0)

    # avg_color is a tuple in BGR order of the average colors
    # but as float values
    print(f'avg_colors: {avg_colors}')

    # so, convert that array to integers
    int_averages = np.array(avg_colors, dtype=np.uint8)
    print(f'int_averages: {int_averages}')

    # create a new image of the same height/width as the original
    average_image = np.zeros((height, width, 3), np.uint8)
    # and fill its pixels with our average color
    average_image[:] = int_averages

    # finally, show it side-by-side with the original
    cv2.imshow("Avg Color", np.hstack([img, average_image]))
    cv2.waitKey(0)

Which would give you this:

<img src="../images/2018/average_color.png" width="480" title="Average color of the puppy"/>


That tan is not too bad, but you probably won't find any pixels in the puppy that match that shade. Worse yet, finding the average color would totally fail on a multi-colored object, like the NASA logo.

<img src="../images/2018/meatball_average.png" width="480" title="Average color of the NASA log"/>

Instead, let's try a more powerful method. We'll find the most common colors in our image using _K-means clustering_.


<i class="fa fa-robot"></i> - <i class="fa fa-heart red"></i>