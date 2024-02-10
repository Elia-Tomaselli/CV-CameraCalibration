# Script to calibrate the cameras using the court points
# It will use the points from the points.yaml file and the images
# from the images/distorted directory to calibrate the cameras.

import argparse
import cv2 as cv
import numpy as np
import os
import yaml


def main(args):
    camera_number = args.camera_number

    IMAGES_DIRECTORY = os.path.join(os.path.dirname(__file__), "images", "court", "distorted")
    OUTPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "images", "court", "undistorted_with_court")
    image_name = f"out{camera_number}.jpg"
    image_path = os.path.join(IMAGES_DIRECTORY, image_name)

    image = cv.imread(image_path)
    height, width = image.shape[:2]

    if image is None:
        print("Image not found")
        return

    with open("points.yaml", "r") as file:
        data = yaml.safe_load(file)
        camera_points = data[camera_number]["distorted"]

        world_points = camera_points["world_points"]
        image_points = camera_points["image_points"]

        world_points = np.array([world_points], dtype=np.float32)
        image_points = np.array([image_points], dtype=np.float32)

    success, camera_matrix, distortion_coefficients, rotation_vector, translation_vector = cv.calibrateCamera(
        world_points, image_points, (width, height), None, None
    )

    # Print the calibration results
    print("Calibration was successful: " + str(success))
    print("Camera matrix:")
    print(camera_matrix)
    print("\nDistortion coefficients:")
    print(distortion_coefficients)
    print("\nRotation vectors:")
    print(rotation_vector)
    print("\nTranslation vectors:")
    print(translation_vector)

    # Get the optimal new camera matrix and region of interest
    new_camera_matrix, region_of_interest = cv.getOptimalNewCameraMatrix(
        camera_matrix, distortion_coefficients, (width, height), 1, (width, height)
    )

    print("\nOptimal camera matrix: ")
    print(new_camera_matrix)

    undistorted_image = cv.undistort(image, camera_matrix, distortion_coefficients, None, new_camera_matrix)

    # crop the image
    # x, y, w, h = region_of_interest
    # undistorted_image = undistorted_image[y:y+h, x:x+w]

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    cv.imwrite(os.path.join(OUTPUT_DIRECTORY, image_name), undistorted_image)

    # Calculate reprojection error
    mean_error = 0

    for i in range(len(world_points)):
        reprojected_image_points, _ = cv.projectPoints(
            world_points[i], rotation_vector[i], translation_vector[i], camera_matrix, distortion_coefficients
        )
        reprojected_image_points = reprojected_image_points.reshape(image_points.shape)
        error = cv.norm(image_points[i], reprojected_image_points[i], cv.NORM_L2) / len(reprojected_image_points)
        mean_error += error

    print("Total error: {}".format(mean_error / len(world_points)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calibrate the cameras using the court points")

    parser.add_argument("camera_number", type=int, help="The camera number")

    args = parser.parse_args()

    main(args)
