import numpy as np
import cv2 as cv
import glob
from pprint import pprint

# Define chessboard dimensions
CHESSBOARD_WIDTH = 6
CHESSBOARD_HEIGHT = 7

# Termination criteria for corner detection
termination_criteria = (cv.TERM_CRITERIA_EPS +
                        cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points, like (0, 0, 0), (1, 0, 0), (2, 0, 0), ..., (6, 5, 0)
object_points = np.zeros((CHESSBOARD_WIDTH * CHESSBOARD_HEIGHT, 3), np.float32)
object_points[:, :2] = np.mgrid[0:CHESSBOARD_WIDTH,
                                0:CHESSBOARD_HEIGHT].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images
world_points = []  # 3D point in real-world space
image_points = []  # 2D points in image plane

# Get the paths of all images in the samples folder as a list
image_paths = glob.glob('samples/*.jpg')

for image_path in image_paths:
    img = cv.imread(image_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chessboard corners
    found_corners, corners = cv.findChessboardCorners(
        gray, (CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT), None)
    
    # If corners are found, add object points and image points (after refining them)
    if found_corners:
        # pprint(corners.tolist())
        world_points.append(object_points)
        refined_corners = cv.cornerSubPix(
            gray, corners, (11, 11), (-1, -1), termination_criteria)
        # print(np.array_equal(corners, refined_corners))
        image_points.append(refined_corners)

        # Draw and display the corners
        cv.drawChessboardCorners(
            img, (CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT), refined_corners, found_corners)
        cv.imshow('img', img)
        cv.waitKey(200)

cv.destroyAllWindows()

for i in range(len(image_points)):
    print("Image #" + str(i+1) + ":\n")
    print("Image points:\n")
    pprint(image_points[i].tolist())
    print("\nWorld points:\n")
    pprint(world_points[i].tolist())
    print("\n")

# Calibrate the camera
calibration_success, camera_matrix, distortion_coeffs, rotation_vecs, translation_vecs = cv.calibrateCamera(
    world_points, image_points, gray.shape[::-1], None, None)

# Print the calibration results
print("Camera matrix:")
print(camera_matrix)
print("\nDistortion coefficients:")
print(distortion_coeffs)
print("\nRotation vectors:")
print(rotation_vecs)
print("\nTranslation vectors:")
print(translation_vecs)

test_img = cv.imread("samples/left12.jpg")
height, width = test_img.shape[:2]

# Get the optimal new camera matrix and region of interest
optimal_camera_matrix, roi = cv.getOptimalNewCameraMatrix(
    camera_matrix, distortion_coeffs, (width, height), 1, (width, height))

# Undistort
undistorted_img = cv.undistort(
    test_img, camera_matrix, distortion_coeffs, None, optimal_camera_matrix)

# crop the image
x, y, w, h = roi
undistorted_img = undistorted_img[y:y+h, x:x+w]
cv.imwrite('result.png', undistorted_img)
