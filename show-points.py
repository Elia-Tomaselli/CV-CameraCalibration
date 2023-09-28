import numpy as np
import cv2 as cv
from os import path

IMAGES_PATH = path.join(path.dirname(__file__), 'images')

IMAGES_NAMES = [
    'out1.png',
    'out2.png',
    'out3.png',
    'out4.png',
    'out5.png',
    'out6.png',
    'out7.png',
    'out8.png',
]

# The image used for the calibration
IMAGE_NAME = IMAGES_NAMES[1]

IMAGE_PATH = path.join(IMAGES_PATH, IMAGE_NAME)

img = cv.imread(IMAGE_PATH)

volleyballWorldPoints = [
    [-9.0, -4.5, 0.0],
    [-3.0, -4.5, 0.0],
    [3.0, -4.5, 0.0],
    [9.0, -4.5, 0.0],

    [-9.0, 4.5, 0.0],
    [-3.0, 4.5, 0.0],
    [3.0, 4.5, 0.0],
    [9.0, 4.5, 0.0],

    [-9.0, -6.25, 0.0],
    [-3.0, -6.25, 0.0],
    [3.0, -6.25, 0.0],
    [9.0, -6.25, 0.0],

    [-9.0, 6.25, 0.0],
    [-3.0, 6.25, 0.0],
    [3.0, 6.25, 0.0],
    [9.0, 6.25, 0.0],

    [-6.0, -4.5, 0.0],
    [0.0, -4.5, 0.0],
    [6.0, -4.5, 0.0],
]

volleyballImagePoints = [
    [745, 1347],
    [1431, 1380],
    [2242, 1392],
    [2945, 1380],

    [1096, 1042],
    [1584, 1044],
    [2108, 1052],
    [2602, 1065],

    [645, 1442],
    [1382, 1493],
    [2286, 1506],
    [3039, 1477],

    [1144, 1003],
    [1603, 1005],
    [2091, 1012],
    [2551, 1025],

    [1088, 1367],
    [1833, 1390],
    [2594, 1390],
]

basketballWorldPoints = [
    [-14.0, -7.5, 0.0],
    [14.0, -7.5, 0.0],
    [-14.0, 7.5, 0.0],
    [14.0, 7.5, 0.0],
]

basketballImagePoints = [
    [150, 1458],
    [3551, 1507],
    [859, 982],
    [2848, 1013],
]

worldPoints = np.array([volleyballWorldPoints + basketballWorldPoints], dtype=np.float32)
imagePoints = np.array([volleyballImagePoints + basketballImagePoints], dtype=np.float32)

RADIUS = 8
COLOR = (0, 0, 255)
THICKNESS = 2
for center, label in zip(imagePoints[0], worldPoints[0]):
    label = f"({label[0]}, {label[1]})"
    center = (int(center[0]), int(center[1]))
    cv.circle(img, center, RADIUS, COLOR, -1)
    label_position = (center[0], center[1] - 30)
    cv.putText(img, label, label_position,
               cv.FONT_HERSHEY_SIMPLEX, 1, COLOR, THICKNESS)

img = cv.resize(img, (1920, 1080))
cv.namedWindow('Court Image', cv.WINDOW_NORMAL)
cv.setWindowProperty('Court Image', cv.WND_PROP_FULLSCREEN,
                     cv.WINDOW_FULLSCREEN)
cv.imshow('Court Image', img)
cv.imwrite("court-points.png", img)
cv.waitKey(0)
cv.destroyAllWindows()
