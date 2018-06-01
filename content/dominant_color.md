Title: Finding the dominant color
Date: 2018-05-23
Category: OpenCV
Tags: opencv, python
Status: draft

In the previous article, I explored how to select a region of interest within an image. In this article, how we can determine information about that region, such as its predominant color.

* refactor the last code and provide as a download
    * as needed, refactor make functions generic
    * remove the cropping code
    * add shell of needed functions for this article

Basic - open image, select region, calculate average & predominant colors, rgb & hsv values for those, aspect ratio, height/width
Nice to show all of that in a single window (roi original, square of avg, square of pred. colors, data)

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