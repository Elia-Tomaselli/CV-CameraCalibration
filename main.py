import cv2 as cv
import numpy as np
from os import path


def findCourtCorners():
    pass


def drawCourtCorners():
    pass


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

for i, imageName in enumerate(IMAGES_NAMES):
    IMAGE_PATH = path.join(IMAGES_PATH, imageName)
    img = cv.imread(IMAGE_PATH)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # 219 63 66
    courtColorLow = np.array([100, 80, 90])
    courtColorHigh = np.array([125, 255, 255])
    courtMask = cv.inRange(hsv, courtColorLow, courtColorHigh)
    cv.imwrite(path.join(IMAGES_PATH, "tests", "court", f"court{i + 1}.png"), courtMask)
    # 42 13 62
    # floor = cv.GaussianBlur(hsv, (5, 5), cv.BORDER_DEFAULT)
    floorColorLowHSV1 = (0, 30, 90)
    floorColorHighHSV1 = (40, 255, 255)
    # floorColorLowRGB = (127, 127, 127)
    # floorColorHighRGB = (255, 255, 255)
    floorColorLowHSV2 = (0, 0, 127)
    floorColorHighHSV2 = (179, 255, 255)
    # floorColorLow2 = np.array([160, 30, 90])
    # floorColorHigh2 = np.array([179, 255, 255])
    floorMaskHSV1 = cv.inRange(hsv, floorColorLowHSV1, floorColorHighHSV1)
    floorMaskHSV2 = cv.inRange(hsv, floorColorLowHSV2, floorColorHighHSV2)
    floorMask = cv.bitwise_or(floorMaskHSV1, floorMaskHSV2)

    floorMaskHSV2 = cv.erode(floorMaskHSV2, generateCircularKernel(100), iterations=4)
    floorMaskHSV2 = cv.dilate(floorMaskHSV2, generateCircularKernel(100), iterations=10)
    floorMaskHSV2 = cv.erode(floorMaskHSV2, generateCircularKernel(100), iterations=2)
    # floorMaskRGB = cv.inRange(img, floorColorLowRGB, floorColorHighRGB)
    # floorMaskHSV2 = cv.dilate(floorMaskHSV2, generateCircularKernel(200))
    # floorMaskHSV2 = cv.erode(floorMaskHSV2, generateCircularKernel(100), iterations=2)
    # floorMaskRGB = cv.dilate(floorMaskRGB, (3, 3), iterations=1)
    # floorMask = cv.bitwise_or(floorMaskHSV, floorMaskRGB)
    # res = cv.bitwise_and(img, img, mask=mask)
    cv.imwrite(path.join(IMAGES_PATH, "tests", "floor", f"floor-dilate{i + 1}.png"), floorMask)
    # cv.imwrite(path.join(IMAGES_PATH, "tests", "floor", f"floor-dilate{i + 1}.png"), floorMaskRGB)
    # cv.imwrite(path.join(IMAGES_PATH, "tests", "floor", f"floor{i + 1}.png"), floorMask)

    # Apply Canny edge detection
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # edges = cv.Canny(gray, 3250, 3500, apertureSize=5)
    # cv.imwrite(path.join(IMAGES_PATH, "tests", f"edges{i + 1}.png"), edges)
