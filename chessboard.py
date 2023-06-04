import numpy as np
import cv2 as cv
import glob

# Define chessboard dimensions
CHESSBOARD_WIDTH = 6
CHESSBOARD_HEIGHT = 7

# Termination criteria for corner detection
termination_criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points, like (0, 0, 0), (1, 0, 0), (2, 0, 0), ..., (6, 5, 0)
object_points = np.zeros((CHESSBOARD_WIDTH * CHESSBOARD_HEIGHT, 3), np.float32)
object_points[:, :2] = np.mgrid[0:CHESSBOARD_WIDTH, 0:CHESSBOARD_HEIGHT].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images
world_points = []  # 3D point in real-world space
image_points = []  # 2D points in image plane

# Get the paths of all images in the samples folder as a list
image_paths = glob.glob('samples/*.jpg')

for image_path in image_paths:
    img = cv.imread(image_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chessboard corners
    found_corners, corners = cv.findChessboardCorners(gray, (CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT), None)

    # If corners are found, add object points and image points (after refining them)
    if found_corners:
        world_points.append(object_points)
        refined_corners = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), termination_criteria)
        image_points.append(refined_corners)

        # Draw and display the corners
        cv.drawChessboardCorners(img, (CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT), refined_corners, found_corners)
        cv.imshow('img', img)
        cv.waitKey(3000)

cv.destroyAllWindows()
