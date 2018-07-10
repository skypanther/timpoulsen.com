import cv2
import numpy as np

img = cv2.imread('meatball.png')
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
