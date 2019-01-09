Title: Using OpenCV in an iOS app
Date: January 8, 2019
Category: opencv, swift, ios
Tags: OpenCV, iOS
Status: draft


Using OpenCV in your iOS app

## Integration steps

1. Download and unzip the OpenCV pack:
    1. Go to https://opencv.org/releases.html
    2. Find 3.4.4 (or other suitable version) and click the **iOS pack** link
    3. Unzip the file to a convenient temporary location
2. If necessary, create your Xcode project
3. Drag the **opencv2.framework** bundle (special folder) into the Xcode project tree to add it to your project.
    * Make sure **Copy items if needed** is checked
    * Make sure **Create folder references** is checked
    * Make sure **Add to targets: _your\_project_** is checked
4. Create the wrapper and bridging header in your project:
    1. Choose File > New > File
    2. Create a **Cocoa Touch Class** file, naming it *OpenCVWrapper* (or another name if you prefer)
    3. It should subclass **NSOBject**
    4. It should be an **Objective-**C file
    5. When prompted, click the **Create Bridging Header** button
5. Open the YourApp-Bridging-Header.h file and add this line:

        #import "OpenCVWrapper.h"

6. Change the name of the OpenCVWrapper.m file to **OpenCVWrapper.mm** (to set it as a C++ rather than C file)
7. Make sure the imports at the top are in this order:

        #import <opencv2/opencv.hpp>
        #import "OpenCVWrapper.h"

8. Create a prefix header.
    1. Choose File > New > File
    2. Scroll to near the bottom and choose **PCH File**
    3. Make sure your app is checked in the Targets list
    4. Click Create
9. Before the closing `#endif` statement, add:

        #ifdef __cplusplus
        #include <opencv2/opencv.hpp>
        #endif

10. You're done! Well, you can build the app now and OpenCV is integrated. Of course you've done nothing to implement OpenCV's functions yet. (Ignore all the semantic build warning from OpenCV's code.)

## Implementing an OpenCV function

The basic steps you'll follow to implement an OpenCV function and use it in your app are:

1. Add the function signature to the OpenCVWrapper.h file
2. Add the function's implementation code in the OpenCVWrapper.mm file
3. Call that function in your Swift file

For example:

1. Open the OpenCVWrapper.h header file
2. Between the `@interface OpenCVWrapper : NSObject` and `@end` lines, add: 

        + (NSString *)openCVVersionString;
<br/>(Note: Per Objective-C syntax, the `+` indicates a class method; use `-` to indicate an instance method.)
3. In the OpenCVWrapper.mm file, after the `@implementation OpenCVWrapper` line, add:

        + (NSString *)openCVVersionString {
            return [NSString stringWithFormat:@"OpenCV Version %s",  CV_VERSION];
        }
4. In your main ViewController.swift file, update **viewDidLoad**

        override func viewDidLoad() {
            super.viewDidLoad()
            print("\(cv2.openVersionString())")
        }
5. Build to a simulator and watch the Xcode debug console and you should see `OpenCV Version 3.4.4` there.


first paragraph

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