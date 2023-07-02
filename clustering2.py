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

    blurred = cv.medianBlur(img, 45)

    # Find brightest and darkest pixels, and use them as initial centroids for k-means
    darkest, brightest, darkest_loc, brightest_loc = cv.minMaxLoc(gray)
    centroids = np.array([brightest, darkest])
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    positions = np.dstack(np.meshgrid(
        range(img.shape[0]), range(img.shape[1]))).astype(np.float32)    
    positions[:, :, 0] = (positions[:, :, 0] + 1) * (127 / positions.shape[1])
    positions[:, :, 1] = (positions[:, :, 1] + 1) * (127 / positions.shape[0])

    data = np.hstack((blurred.reshape((-1, 3)), positions.reshape(-1, 2)))
    data = np.float32(data)

    # 2 clusters, 1 for floor and 1 for everything else
    # It is used to filter the floor out of the image so it's easier to find the court lines
    ret, labels, centers = cv.kmeans(
        data, 2, None, criteria, 10, flags=cv.KMEANS_USE_INITIAL_LABELS, centers=centroids)

    centers = np.uint8(centers[:, :3])

    floorFilter = None
    # Find the brightest color
    if (centers[0].sum() > centers[1].sum()):
        floorFilter = ~(labels.astype(np.uint8).flatten() * 255)
    else:
        floorFilter = (labels.astype(np.uint8).flatten() * 255)

    floorFilter = floorFilter.reshape((img.shape[0], img.shape[1]))
    # cv.imwrite(path.join(IMAGES_PATH, "tests", "floorFilter",
    #            f"before{i + 1}.png"), floorFilter)
    floorFilter = cv.erode(floorFilter, generateCircularKernel(200), iterations=12)
    floorFilter = cv.dilate(floorFilter, generateCircularKernel(200), iterations=10)

    floor = cv.bitwise_and(img, img, mask=floorFilter)
    floorHSV = cv.cvtColor(floor, cv.COLOR_BGR2HSV)

    # lab = cv.cvtColor(floor, cv.COLOR_BGR2Lab)
    data = np.hstack((floorHSV.reshape((-1, 3)), positions.reshape(-1, 2)))
    
    spatialRadius = 100
    colorRadius = 20

    filteredImage = cv.pyrMeanShiftFiltering(floorHSV, spatialRadius, colorRadius)
    filteredImage = filteredImage.reshape(floorHSV.shape)
    filteredImageRGB = cv.cvtColor(filteredImage, cv.COLOR_HSV2BGR)

    print(f"Done {i + 1}")
    cv.imwrite(path.join(IMAGES_PATH, "tests", "floor", f"after{i + 1}.png"), filteredImageRGB)


for i, imageName in enumerate(IMAGES_NAMES):
    IMAGE_PATH = path.join(IMAGES_PATH, imageName)

    img = cv.imread(IMAGE_PATH)

    floor = findFloor(img)
