# This script will undistort an image using the camera parameters obtained from the calibration process.
# The program will search for the camera parameters in the camera_parameters directory and the image in the images/court/distorted directory.
# The camera parameters are the ones obtained from the calibration process and saved in a pickle file (they are just renamed for simplicity).
# The undistorted image will be saved in the images/court/undistorted_with_crop or images/court/undistorted_without_crop directory.

import argparse
import cv2 as cv
import os
import pickle
import sys


def main(args):
    camera_number = args.camera_number

    IMAGES_DIRECTORY = os.path.join(os.path.dirname(__file__), "images", "court")
    CAMERA_PARAMETERS_DIRECTORY = os.path.join(os.path.dirname(__file__), "camera_parameters")

    input_image_path = os.path.join(IMAGES_DIRECTORY, "distorted", f"out{camera_number}.jpg")

    if args.with_crop:
        camera_parameters_path = os.path.join(CAMERA_PARAMETERS_DIRECTORY, "with_crop", f"out{camera_number}F.p")
        output_image_path = os.path.join(IMAGES_DIRECTORY, "undistorted_with_crop", f"out{camera_number}.jpg")
    elif args.without_crop:
        camera_parameters_path = os.path.join(CAMERA_PARAMETERS_DIRECTORY, "without_crop", f"out{camera_number}F.p")
        output_image_path = os.path.join(IMAGES_DIRECTORY, "undistorted_without_crop", f"out{camera_number}.jpg")
    else:
        print("Invalid arguments", file=sys.stderr)
        return

    input_image = cv.imread(input_image_path)
    camera_parameters = pickle.load(open(camera_parameters_path, "rb"))

    camera_matrix = camera_parameters["mtx"]
    # new_mtx does not exist in the pickle file if the image was undistorted with crop
    new_camera_matrix = None if args.with_crop else camera_parameters["new_mtx"]
    distortion_coefficients = camera_parameters["dist"]

    if args.with_crop:
        # For cropping we use the camera matrix as the 5th argument
        undistorted_image = cv.undistort(input_image, camera_matrix, distortion_coefficients, None, camera_matrix)
        os.makedirs(os.path.join("images", "court", "undistorted_with_crop"), exist_ok=True)
    else:
        # For no cropping we use the new camera matrix as the 5th argument
        undistorted_image = cv.undistort(input_image, camera_matrix, distortion_coefficients, None, new_camera_matrix)
        os.makedirs(os.path.join("images", "court", "undistorted_without_crop"), exist_ok=True)

    cv.imwrite(output_image_path, undistorted_image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Undistort an image")

    parser.add_argument("camera_number", type=int, help="The camera number")

    undistortion_mode_group = parser.add_mutually_exclusive_group(required=True)
    undistortion_mode_group.add_argument("--with-crop", action="store_true", help="Undistort with crop")
    undistortion_mode_group.add_argument("--without-crop", action="store_true", help="Undistort without crop")

    args = parser.parse_args()

    main(args)
