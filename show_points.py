# This script is used to show the points on the court image.
# It uses the points.yaml file to get the points and the camera number.
# The points.yaml file contains the world and image points for each camera.
# To check where the points are located on the undistorted images with or without crop, first run the undistort.py script, if you don't have any image in the images/undistorted_with_crop or images/undistorted_without_crop directory.

import argparse
import cv2 as cv
import numpy as np
import os
import sys
import yaml


def main(args):
    camera_number = args.camera_number

    IMAGES_DIRECTORY = os.path.join(os.path.dirname(__file__), "images", "court")

    with open("points.yaml", "r") as file:
        yaml_data = yaml.safe_load(file)

    if args.distorted:
        mode_directory = "distorted"
        camera_points = yaml_data[camera_number]["distorted"]
    elif args.undistorted_with_crop:
        mode_directory = "undistorted_with_crop"
        camera_points = yaml_data[camera_number]["undistorted_with_crop"]
    elif args.undistorted_without_crop:
        mode_directory = "undistorted_without_crop"
        camera_points = yaml_data[camera_number]["undistorted_without_crop"]
    else:
        print("Invalid arguments", file=sys.stderr)
        return

    image_path = os.path.join(IMAGES_DIRECTORY, mode_directory, f"out{camera_number}.jpg")
    image = cv.imread(image_path)

    world_points = np.array(camera_points["world_points"], dtype=np.float32)
    image_points = np.array(camera_points["image_points"], dtype=np.float32)

    # Variables for drawing the points
    RADIUS = 8
    COLOR = (0, 0, 255)
    THICKNESS = 2

    # Draw the points on the image
    for image_point, world_point in zip(image_points, world_points):
        label = f"({world_point[0]}, {world_point[1]})"
        center = (int(image_point[0]), int(image_point[1]))
        cv.circle(image, center, RADIUS, COLOR, -1)
        label_position = (center[0], center[1] - 30)
        cv.putText(image, label, label_position, cv.FONT_HERSHEY_SIMPLEX, 1, COLOR, THICKNESS)

    image = cv.resize(image, (1920, 1080))

    cv.namedWindow("Court Image Points", cv.WINDOW_NORMAL)
    cv.setWindowProperty("Court Image Points", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.imshow("Court Image Points", image)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show the court points on the image")

    parser.add_argument("camera_number", type=int, help="The camera number")

    image_type_parser_group = parser.add_mutually_exclusive_group(required=True)
    image_type_parser_group.add_argument("-d", "--distorted", action="store_true", help="Use the distorted images")
    image_type_parser_group.add_argument(
        "-uw", "--undistorted-with-crop", action="store_true", help="Use the cropped images"
    )
    image_type_parser_group.add_argument(
        "-uwo", "--undistorted-without-crop", action="store_true", help="Use the cropped images"
    )

    args = parser.parse_args()

    main(args)
