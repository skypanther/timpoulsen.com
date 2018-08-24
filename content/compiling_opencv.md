Title: Build OpenCV and install from source
Date: March 27, 2018
Category: OpenCV
Tags: python, opencv, anaconda

(Originally posted at skypanther.com)

I wanted to set up the latest OpenCV version on my Mac. I found various instructions, but few that applied specifically to my setup — Mac OS X High Sierra running Anaconda. What follows are my steps to compile and install the latest OpenCV version onto my Mac.

## Prerequisites

You’ll need a few things first…if you don’t have these, set them up now.

* Xcode and its command-line tools
* A working Python 3.x environment (hint: use Anaconda)
* Homebrew

Once you have those installed, you’re ready to start. You’ll need to install some pre-requisite packages. Each of the following is a separate command:

    brew install cmake pkg-config
    brew install jpeg libpng libtiff openexr
    brew install eigen tbb

Next, you’ll need the OpenCV source code. Clone OpenCV and OpenCV_contrib:

    cd ~
    git clone https://github.com/opencv/opencv
    git clone https://github.com/opencv/opencv_contrib
    cd ~/opencv
    mkdir build
    cd build

Next you’ll configure `make` with the following command. All of this is one big command, split over multiple lines, and yes it does end with two periods. You can just copy it all and paste in your terminal.

    cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
        -D PYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
        -D PYTHON_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
        -D PYTHON3_EXECUTABLE=$(which python3) \
        -D BUILD_opencv_python2=OFF \
        -D BUILD_opencv_python3=ON \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D INSTALL_C_EXAMPLES=OFF \
        -D BUILD_TESTS=OFF \
        -D BUILD_PERF_TESTS=OFF \
        -D WITH_CUDA=OFF \
        -D WITH_FFMPEG=ON \
        -D ENABLE_PRECOMPILED_HEADERS=OFF \
        -D BUILD_EXAMPLES=OFF ..

That command will take a while...after which you can do the actual build:

    make -j4

That will take even longer; depending on the speed of your system it could take an hour or longer. Once it’s all done, you’re ready to actually install the compiled project:

    sudo make install

That will copy all the files to the right spot on your system. At this point, you’re pretty much done. I found a few guides that suggested that you need to rename (or copy or link) one of the .so files that was copied to your python lib folder.

Rather than digging for the location of that folder, what the first command below does is ask python to find that folder for you and pass it to the `cd` command:

    cd $(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
    cp cv2.cpython-36m-darwin.so cv2.so

Finally, you’re done and ready test your work:

    $ python

    Python 3.6.3 |Anaconda, Inc.| (default, Oct  6 2017, 12:04:38) 
    [GCC 4.2.1 Compatible Clang 4.0.1 (tags/RELEASE_401/final)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import cv2
    >>> cv2.__version__
    '3.4.1-dev'

That’s it, OpenCV is installed!