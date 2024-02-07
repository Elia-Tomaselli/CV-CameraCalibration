import numpy as np
import cv2 as cv
import os
import yaml
import sys

cropped = True
camera_number = int(sys.argv[1])

images_directory = os.path.join("output", "court_images", "undistorted", "crop" if cropped else "no_crop")
image_path = os.path.join(images_directory, f"out{camera_number}.jpg")

image = cv.imread(image_path)

with open("points.yaml", "r") as file:
    data = yaml.safe_load(file)
    camera_points = data[camera_number]["crop" if cropped else "no_crop"]
    world_points = np.array(camera_points["world_points"], dtype=np.float32)
    image_points = np.array(camera_points["image_points"], dtype=np.float32)

RADIUS = 8
COLOR = (0, 0, 255)
THICKNESS = 2

for center, label in zip(image_points, world_points):
    label = f"({label[0]}, {label[1]})"
    center = (int(center[0]), int(center[1]))
    cv.circle(image, center, RADIUS, COLOR, -1)
    label_position = (center[0], center[1] - 30)
    cv.putText(image, label, label_position, cv.FONT_HERSHEY_SIMPLEX, 1, COLOR, THICKNESS)

image = cv.resize(image, (1920, 1080))

cv.namedWindow("Court Image", cv.WINDOW_NORMAL)
cv.setWindowProperty("Court Image", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
cv.imshow("Court Image", image)
cv.imwrite("court-points.png", image)
cv.waitKey(0)
cv.destroyAllWindows()
