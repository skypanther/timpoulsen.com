'''
slider.py - Demonstrating a user of trackbars on OpenCV windows
Author: Tim Poulsen, github.com/skypanther
License: MIT
2018-10-15

Example usage:

python3 slider.py -i path/to/image.jpg
'''

import argparse
import cv2
import imutils
import os


def main():
    min_val = 200
    max_val = 300
    aperture_size = 3

    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', default='',
                    help='Image to use for edge detection')
    args = vars(ap.parse_args())
    file_name = args['image']
    if os.path.isfile(file_name) is False:
        print('Cannot open image, quitting...')
        exit()
    image = cv2.imread(file_name)
    image = imutils.resize(image, height=480)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.namedWindow('Original')
    cv2.createTrackbar('Min', 'Original', 0, 800, no_op)
    cv2.createTrackbar('Max', 'Original', 100, 800, no_op)
    cv2.imshow('Original', image)

    while True:
        min_val = int(cv2.getTrackbarPos('Min', 'Original'))
        max_val = int(cv2.getTrackbarPos('Max', 'Original'))
        print('Min: {}'.format(min_val))
        print('Max: {}'.format(max_val))
        edges = cv2.Canny(gray, min_val, max_val, aperture_size)
        cv2.imshow('Edges', imutils.resize(edges, height=480))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            exit()


def no_op(new_val):
    pass


if __name__ == '__main__':
    main()
