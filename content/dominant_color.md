Title: Finding the dominant color
Date: 2018-07-10
Category: OpenCV
Tags: opencv, python
Status: draft

A common way to isolate or find an object in an image is to look for its color. You specify a range of colors, then use OpenCV to identify regions in an image that contain colors within that range. But, even if you know the exact color of your target, lighting, shadows, and your camera's sensor will alter the detected color. So, how do you best determine the color range to use?

In this article, I'll explore some different methods to work with colors. By the end, I'll show you how to <a href="https://www.timpoulsen.com/2018/handling-mouse-events-in-opencv.html">select a region of interest</a> within an image, then get the exact range of colors needed to isolate that object in a live video stream.

Let's say your goal is to isolate the puppy in this image. You'll notice that his fur color varies between an off-white to a golden tan. The foreground is brighter, making his hindquarters darker and less richly colored. The toy he has is only a bit darker red-brown.

<img src="../images/2018/puppy.jpg" width="480" title="Puppy"/>

Your first attempt might be to take an average of the colors to find the midpoint of his range of colors. Then, to make the range you might choose colors a bit darker and lighter than that average. Of course, you wouldn't want to include the grass in the average. Assuming a cropped version of just the puppy, you could use this script to calculate the average color:

    #!python
    #
    #  Find the average color in an image
    #
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


That tan is not too bad, but you probably won't find any pixels in the puppy that match that exact shade. In a range of lighter to darker than that average, only a few of his pixels would be included. It's even likely you'd get a few pixels of his toy. As bad as the average works with the puppy, the average would totally fail on a multi-colored object like the FIRST<sup>&reg;</sup> logo.

<img src="../images/2018/first_logo_average.png" width="480" title="Average color of the NASA log"/>

<p class="imgcaption">FIRST&reg;, the FIRST&reg; logo, FIRST&reg; Robotics Competition (formerly also known as FRC&reg;), FIRST&reg; Tech Challenge (formerly also known as FTC&reg;) are trademarks of For Inspiration and Recognition of Science and Technology (FIRST&reg;).</p>

Let's try a more powerful method. We'll find the most common colors in our image using _k-means clustering_. A <a href="https://en.wikipedia.org/wiki/K-means_clustering" target="_blank">formal definition</a> would go something like "_k-means clustering partitions n observations into k clusters_". In our case, we have a bunch of pixels (our `n`) and we want to pull out some number (the `k`) of colors.

With k-means, you have to specify the number of clusters up-front. There are other techniques that don't have this requirement. In any case, it's not a significant limitation for our needs here.

We'll use the scikit-learn library's <a href="http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html" target="_blank">`sklearn.cluster.kmeans`</a> function to do the heavy lifting. (OpenCV itself offers a `kmeans()` function, but scikit's is a bit more flexible for our needs). The following script is based on a post on <a href="https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/" target="_blank">the PyImageSearch blog</a> (a great resource!):


    #!python
    #
    #  Use k-means clustering to find the most-common colors in an image
    #
    import cv2
    import numpy as np
    from sklearn.cluster import KMeans


    def make_histogram(cluster):
        """
        Count the number of pixels in each cluster
        :param: KMeans cluster
        :return: numpy histogram
        """
        numLabels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
        hist, _ = np.histogram(cluster.labels_, bins=numLabels)
        hist = hist.astype('float32')
        hist /= hist.sum()
        return hist


    def make_bar(height, width, color):
        """
        Create an image of a given color
        :param: height of the image
        :param: width of the image
        :param: BGR pixel values of the color
        :return: tuple of bar, rgb values, and hsv values
        """
        bar = np.zeros((height, width, 3), np.uint8)
        bar[:] = color
        red, green, blue = int(color[2]), int(color[1]), int(color[0])
        hsv_bar = cv2.cvtColor(bar, cv2.COLOR_BGR2HSV)
        hue, sat, val = hsv_bar[0][0]
        return bar, (red, green, blue), (hue, sat, val)


    def sort_hsvs(hsv_list):
        """
        Sort the list of HSV values
        :param hsv_list: List of HSV tuples
        :return: List of indexes, sorted by hue, then saturation, then value
        """
        bars_with_indexes = []
        for index, hsv_val in enumerate(hsv_list):
            bars_with_indexes.append((index, hsv_val[0], hsv_val[1], hsv_val[2]))
        bars_with_indexes.sort(key=lambda elem: (elem[1], elem[2], elem[3]))
        return [item[0] for item in bars_with_indexes]


    img = cv2.imread('puppy_cropped.jpg')
    height, width, _ = np.shape(img)

    # reshape the image to be a simple list of RGB pixels
    image = img.reshape((height * width, 3))

    # we'll pick the 5 most common colors
    num_clusters = 5
    clusters = KMeans(n_clusters=num_clusters)
    clusters.fit(image)

    # count the dominant colors and put them in "buckets"
    histogram = make_histogram(clusters)
    # then sort them, most-common first
    combined = zip(histogram, clusters.cluster_centers_)
    combined = sorted(combined, key=lambda x: x[0], reverse=True)

    # finally, we'll output a graphic showing the colors in order
    bars = []
    hsv_values = []
    for index, rows in enumerate(combined):
        bar, rgb, hsv = make_bar(100, 100, rows[1])
        print(f'Bar {index + 1}')
        print(f'  RGB values: {rgb}')
        print(f'  HSV values: {hsv}')
        hsv_values.append(hsv)
        bars.append(bar)

    # sort the bars[] list so that we can show the colored boxes sorted
    # by their HSV values -- sort by hue, then saturation
    sorted_bar_indexes = sort_hsvs(hsv_values)
    sorted_bars = [bars[idx] for idx in sorted_bar_indexes]

    cv2.imshow('Sorted by HSV values', np.hstack(sorted_bars))
    cv2.imshow(f'{num_clusters} Most Common Colors', np.hstack(bars))
    cv2.waitKey(0)

This script does a few things here. First, it examines the image (our cropped puppy) to find the five most common colors (lines 58 - 60). Next, we use a histogram to count the pixels of those colors, and sort them into a descending order of most to least common. Starting on line 69, the code handles output. We loop through our "buckets" to create images (aka "bars") from those colors. We also save the RGB and HSV values.

Check out your console: the script outputs the RGB and HSV color values for each of the colored boxes. 

    :::shell
    > python dominant_color.py 
    Bar 1
      RGB values: (131, 114, 99)
      HSV values: (14, 62, 131)
    Bar 2
      RGB values: (153, 133, 114)
      HSV values: (15, 65, 153)
    Bar 3
      RGB values: (141, 138, 136)
      HSV values: (12, 9, 141)
    Bar 4
      RGB values: (165, 156, 148)
      HSV values: (14, 26, 165)
    Bar 5
      RGB values: (99, 87, 75)
      HSV values: (15, 62, 99)

Given our cropped puppy image, the script outputs two CV2 windows. The first shows colored boxes in the top 5 colors, listed most to least common left to right. If you move that window out of the way, you'll see a similar one showing those same colors arranged in HSV order.

<img src="../images/2018/puppy_5_colors_with_hsv.png" width="480" title="Top 5 colors of the puppy"/>

It might be surprising when seen as RGB boxes on your screen, but the dominant colors are fairly close in hue, even in saturation. In fact, hue values range between 12 and 15. (Sidenote: OpenCV represents hue ranges from 0-180, not 0-360 as graphics apps typically do.)

The detected HSV values will be what we use for object detection. We'll use OpenCV to detect and isolate elements in an image (or video frame) based on a range of HSV values.



Source materials and further explorations:

* https://adamspannbauer.github.io/2018/03/02/app-icon-dominant-colors/
* https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
* https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
* https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/



<i class="fa fa-robot"></i> - <i class="fa fa-heart red"></i>