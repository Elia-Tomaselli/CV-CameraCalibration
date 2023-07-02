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

# Prepare object points, like (0, 0, 0), (1, 0, 0), (2, 0, 0), ..., (6, 5, 0)
worldPoints = np.array([[
    [0, 0, 0],
    [6, 0, 0],
    [12, 0, 0],
    [18, 0, 0],

    [0, 9, 0],
    [6, 9, 0],
    [12, 9, 0],
    [18, 9, 0],

    # [0, -1.75, 0],
    # [6, -1.75, 0],
    # [12, -1.75, 0],
    # [18, -1.75, 0],

    # [0, 9 + 1.75, 0],
    # [6, 9 + 1.75, 0],
    # [12, 9 + 1.75, 0],
    # [18, 9 + 1.75, 0]
]], np.float32)

imagePoints = np.array([[
    [268, 1632],
    [1198, 1775],
    [2579, 1790],
    [3513, 1667],

    [860, 943],
    [1519, 928],
    [2278, 936],
    [2938, 964],

    # [126, 1848],
    # [1091, 2097],
    # [2676, 2116],
    # [3650, 1888],

    # [942, 866],
    # [1555, 847],
    # [2244, 855],
    # [2854, 885]
]], np.float32)  # 2D points in image plane

# Arrays to store object points and image points from all the images

# Get the paths of all images in the samples folder as a list
imagePath = path.join(IMAGES_PATH, IMAGES_NAMES[5])

img = cv.imread(imagePath)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

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

width, height = gray.shape[:2]

# Get the optimal new camera matrix and region of interest
optimalCameraMatrix, roi = cv.getOptimalNewCameraMatrix(
    cameraMatrix, distortionCoeffs, (width, height), 1, (width, height))

print("\nOptimal camera matrix: ")
print(optimalCameraMatrix)

# Undistort
undistortedImg = cv.undistort(
    img, cameraMatrix, distortionCoeffs, None, optimalCameraMatrix)

# crop the image
# x, y, w, h = roi
# undistortedImg = undistortedImg[y:y+h, x:x+w]

cv.imwrite('result.png', undistortedImg)

# Reprojection error
meanError = 0
for i in range(len(worldPoints)):
    imagePoints2, _ = cv.projectPoints(
        worldPoints[i], rotationVecs[i], translationVecs[i], cameraMatrix, distortionCoeffs)
    imagePoints2 = imagePoints2.reshape(imagePoints.shape)
    error = cv.norm(imagePoints[i], imagePoints2[i],
                    cv.NORM_L2) / len(imagePoints2)
    meanError += error
print("total error: {}".format(meanError/len(worldPoints)))
