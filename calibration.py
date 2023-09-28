import numpy as np
import cv2 as cv
import glob
from pprint import pprint
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

# The image used for the calibration, change it if you change the points used for calibration
IMAGE_NAME = IMAGES_NAMES[5]

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