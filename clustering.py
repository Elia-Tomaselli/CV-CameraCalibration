import numpy as np
import cv2 as cv
from os import path
from pprint import pprint

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


def generateCircularKernel(diameter: int):
    radius = (diameter - 1) // 2
    center = (radius, radius)
    kernel = np.zeros((diameter, diameter), dtype=np.uint8)
    for y in range(diameter):
        for x in range(diameter):
            deltaX = x - center[0]
            deltaY = y - center[1]
            distance = deltaX ** 2 + deltaY ** 2
            if (distance <= radius):
                kernel[y, x] = 1
    return kernel


def findFloor(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # To reduce noise
    img = cv.medianBlur(img, 3)
    
    spatialRadius = 15
    colorRadius = 15

    filteredImage = cv.pyrMeanShiftFiltering(hsv, spatialRadius, colorRadius)
    # filteredImage = cv.cvtColor(filteredImage, cv.COLOR_HSV2BGR)

    # find floor
    floorColorLowHSV = (0, 30, 90)
    floorColorHighHSV = (40, 255, 255)
    floorMask = cv.inRange(filteredImage, floorColorLowHSV, floorColorHighHSV)

    cv.dilate(floorMask, generateCircularKernel(300))
    cv.erode(floorMask, generateCircularKernel(1000))

    floorMaskRGB = cv.cvtColor(floorMask, cv.COLOR_GRAY2BGR)

    print(f"Done {i + 1}")
    cv.imwrite(path.join(IMAGES_PATH, "tests", "floor", f"after{i + 1}.png"), floorMaskRGB)


for i, imageName in enumerate(IMAGES_NAMES):
    IMAGE_PATH = path.join(IMAGES_PATH, imageName)
    img = cv.imread(IMAGE_PATH)
    floor = findFloor(img)
