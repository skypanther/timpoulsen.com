'''
slider2.py - Demonstrating a user of trackbars on OpenCV windows
Author: Tim Poulsen, github.com/skypanther
License: MIT
2018-10-15

Example usage:

python3 slider2.py -i path/to/image.jpg
'''

import argparse
import cv2
import imutils
import os

edge_params = {
    'min_val': 200,
    'max_val': 300,
    'aperture_size': 3
}
gray = None


def main():
    global edge_params, gray
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
    cv2.createTrackbar('Min', 'Original', 0, 800, min_change)
    cv2.createTrackbar('Max', 'Original', 100, 800, max_change)
    cv2.imshow('Original', image)
    redraw_edges()

    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            exit()


def min_change(new_val):
    change_params('min_val', new_val)


def max_change(new_val):
    change_params('max_val', new_val)


def change_params(name, value):
    global edge_params
    edge_params[name] = value
    print(edge_params)
    redraw_edges()


def redraw_edges():
    edges = cv2.Canny(gray,
                      edge_params['min_val'],
                      edge_params['max_val'],
                      edge_params['aperture_size'])
    cv2.imshow('Edges', imutils.resize(edges, height=480))


if __name__ == '__main__':
    main()
