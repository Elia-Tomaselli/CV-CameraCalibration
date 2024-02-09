# Script to calibrate the cameras using the court points

import numpy as np
import cv2 as cv
from pprint import pprint
from os import path

# The camera used for the calibration, change it if you change the camera used for calibration
CAMERA_NUMBER = 6

IMAGES_PATH = path.join(path.dirname(__file__), 'images')

IMAGES_NAMES = {
    1: 'out1.png',
    2: 'out2.png',
    3: 'out3.png',
    4: 'out4.png',
    5: 'out5.png',
    6: 'out6.png',
    7: 'out7.png',
    8: 'out8.png',
}

IMAGE_NAME = IMAGES_NAMES[CAMERA_NUMBER]

IMAGE_PATH = path.join(IMAGES_PATH, IMAGE_NAME)

img = cv.imread(IMAGE_PATH)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# World points and image points for image "out2.png"
# volleyballWorldPoints = [
#     [-9.0, -4.5, 0.0],
#     [-3.0, -4.5, 0.0],
#     [3.0, -4.5, 0.0],
#     [9.0, -4.5, 0.0],

#     [-9.0, 4.5, 0.0],
#     [-3.0, 4.5, 0.0],
#     [3.0, 4.5, 0.0],
#     [9.0, 4.5, 0.0],

#     [-9.0, -6.25, 0.0],
#     [-3.0, -6.25, 0.0],
#     [3.0, -6.25, 0.0],
#     [9.0, -6.25, 0.0],

#     [-9.0, 6.25, 0.0],
#     [-3.0, 6.25, 0.0],
#     [3.0, 6.25, 0.0],
#     [9.0, 6.25, 0.0],

#     [-6.0, -4.5, 0.0],
#     [0.0, -4.5, 0.0],
#     [6.0, -4.5, 0.0],
# ]
# volleyballImagePoints = [
#     [745, 1347],
#     [1431, 1380],
#     [2242, 1392],
#     [2945, 1380],

#     [1096, 1042],
#     [1584, 1044],
#     [2108, 1052],
#     [2602, 1065],

#     [645, 1442],
#     [1382, 1493],
#     [2286, 1506],
#     [3039, 1477],

#     [1144, 1003],
#     [1603, 1005],
#     [2091, 1012],
#     [2551, 1025],

#     [1088, 1367],
#     [1833, 1390],
#     [2594, 1390],
# ]

# basketballWorldPoints = [
#     [-14.0, -7.5, 0.0],
#     [14.0, -7.5, 0.0],
#     [-14.0, 7.5, 0.0],
#     [14.0, 7.5, 0.0],
# ]
# basketballImagePoints = [
#     [150, 1458],
#     [3551, 1507],
#     [859, 982],
#     [2848, 1013],
# ]

# World points and image points for image "out6.png"
volleyballWorldPoints = [
    [-9.0, -4.5, 0],
    [-3.0, -4.5, 0],
    [3.0, -4.5, 0],
    [9.0, -4.5, 0],

    [-9.0, 4.5, 0],
    [-3.0, 4.5, 0],
    [3.0, 4.5, 0],
    [9.0, 4.5, 0],
]

volleyballImagePoints = [
    [268, 1632],
    [1198, 1775],
    [2579, 1790],
    [3513, 1667],

    [860, 943],
    [1519, 928],
    [2278, 936],
    [2938, 964],
]

basketballWorldPoints = []
basketballImagePoints = []

worldPoints = np.array(
    [volleyballWorldPoints + basketballWorldPoints], dtype=np.float32)
imagePoints = np.array([volleyballImagePoints + basketballImagePoints], dtype=np.float32)

# Calibrate the camera
calibrationSuccess, cameraMatrix, distortionCoeffs, rotationVecs, translationVecs = cv.calibrateCamera(
    worldPoints, imagePoints, gray.shape[::-1], None, None)

# Print the calibration results
print("Calibration was successful: " + str(calibrationSuccess))
print("Camera matrix:")
print(cameraMatrix)
print("\nDistortion coefficients:")
print(distortionCoeffs)
print("\nRotation vectors:")
pprint(rotationVecs)
print("\nTranslation vectors:")
print(translationVecs)

width, height=gray.shape[:2]

# Get the optimal new camera matrix and region of interest
optimalCameraMatrix, roi=cv.getOptimalNewCameraMatrix(
    cameraMatrix, distortionCoeffs, (width, height), 1, (width, height))

print("\nOptimal camera matrix: ")
print(optimalCameraMatrix)

# Undistort
undistortedImg=cv.undistort(
    img, cameraMatrix, distortionCoeffs, None, optimalCameraMatrix)

# crop the image
# x, y, w, h = roi
# undistortedImg = undistortedImg[y:y+h, x:x+w]

cv.imwrite('result.png', undistortedImg)

# Reprojection error
meanError=0
for i in range(len(worldPoints)):
    imagePoints2, _=cv.projectPoints(
        worldPoints[i], rotationVecs[i], translationVecs[i], cameraMatrix, distortionCoeffs)
    imagePoints2=imagePoints2.reshape(imagePoints.shape)
    error=cv.norm(imagePoints[i], imagePoints2[i],
                    cv.NORM_L2) / len(imagePoints2)
    meanError += error

print("total error: {}".format(meanError / len(worldPoints)))
