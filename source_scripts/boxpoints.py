# quick tutorial fodder:

# box points, docs aren't clear about the order


def draw_box_points(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)
    # get the countours
    _, cnts, _ = cv2.findContours(thresh,
                                  cv2.RETR_LIST,
                                  cv2.CHAIN_APPROX_SIMPLE)
    # sort the contours
    cnt = sorted(cnts, key=cv2.contourArea)
    print('len', len(cnts))
    if len(cnt) == 0:
        print('Failed to find skew angle')
        return thresh
    # get the min rotated bounding rect of the largest one
    rect = cv2.minAreaRect(cnt[-1])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    # box points is a list of lists of x/y coords in order:
    # bottom-right, bottom-left, top-left, top-right
    cv2.circle(image, tuple(one), 30, (0, 0, 255), -1)
    cv2.circle(image, tuple(two), 30, (0, 255, 0), -1)
    cv2.circle(image, tuple(three), 30, (255, 0, 0), -1)
    cv2.circle(image, tuple(four), 30, (255, 255, 255), -1)
