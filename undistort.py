import cv2 as cv
import numpy as np
import os
import pickle
import sys

cropped = True

# Test undistortion on an image
# print("Testing undistortion on camera", camera.camera_number)
camera_number = int(sys.argv[1])

image_path = os.path.join("output", "court_images", "raw", f"out{camera_number}.jpg")
pickle_path = os.path.join("camera_parameters", "crop" if cropped else "no_crop", f"out{camera_number}F.p")

output_directory = os.path.join("output", "court_images")
output_image_path = os.path.join(
    output_directory,
    "undistorted",
    "crop" if cropped else "no_crop",
    f"out{camera_number}.jpg",
)

image = cv.imread(image_path)
pickle_file = pickle.load(open(pickle_path, "rb"))

camera_matrix = pickle_file["mtx"]
new_camera_matrix = None if cropped else pickle_file["new_mtx"]
distortion_coefficients = pickle_file["dist"]

undistorted_image = cv.undistort(image, camera_matrix, distortion_coefficients, None, camera_matrix if cropped else new_camera_matrix)

os.makedirs(os.path.join("output", "court_images", "undistorted"), exist_ok=True)
cv.imwrite(output_image_path, undistorted_image)

