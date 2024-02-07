import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import sys
import yaml


def pretty_print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{val:8.4f}" for val in row))


def plot_camera(extrinsic_matrix, size):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    volleyball_points = np.array(
        [
            [9.0, 4.5, 0.0],
            [3.0, 4.5, 0.0],
            [-3.0, 4.5, 0.0],
            [-9.0, 4.5, 0.0],
            [9.0, -4.5, 0.0],
            [3.0, -4.5, 0.0],
            [-3.0, -4.5, 0.0],
            [-9.0, -4.5, 0.0],
        ],
        dtype=np.float32,
    )

    camera_position = extrinsic_matrix[:3, 3]

    # Plot camera location
    ax.scatter(camera_position[0], camera_position[1], camera_position[2], c="r", marker="o", label="Camera")

    # Plot camera direction
    direction_vector_size = 10
    camera_direction = extrinsic_matrix[:3, :3] @ np.array([0, 0, direction_vector_size]) + camera_position
    ax.plot(
        [camera_position[0], camera_direction[0]],
        [camera_position[1], camera_direction[1]],
        [camera_position[2], camera_direction[2]],
        c="g",
        label="Camera Direction",
    )

    ax.scatter(
        volleyball_points[:, 0], volleyball_points[:, 1], volleyball_points[:, 2], c="b", marker="o", label="Points"
    )

    ax.set_xlim([camera_position[0] - size, camera_position[0] + size])
    ax.set_ylim([camera_position[1] - size, camera_position[1] + size])
    ax.set_zlim([camera_position[2] - size, camera_position[2] + size])

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Camera Position and Points")
    ax.legend()

    plt.show()


cropped = True

# Test undistortion on an image
# print("Testing undistortion on camera", camera.camera_number)
camera_number = int(sys.argv[1])

image_path = os.path.join("output", "court_images", "raw", f"out{camera_number}.jpg")
image = cv.imread(image_path)

pickle_path = os.path.join("camera_parameters", "crop" if cropped else "no_crop", f"out{camera_number}F.p")
pickle_file = pickle.load(open(pickle_path, "rb"))

if not os.path.exists(pickle_path):
    print("Pickle file does not exist")
    sys.exit(1)

camera_matrix = pickle_file["mtx"]
new_camera_matrix = None if cropped else pickle_file["new_mtx"]
distortion_coefficients = np.zeros((1, 5), dtype=np.float32)

# undistorted_image = cv.undistort(image, camera_matrix, distortion_coefficients, None, camera_matrix if cropped else new_camera_matrix)

with open("points.yaml", "r") as file:
    data = yaml.safe_load(file)
    camera_points = data[camera_number]["crop" if cropped else "no_crop"]

    world_points = camera_points["world_points"]
    image_points = camera_points["image_points"]

    world_points = np.array(world_points, dtype=np.float32)
    image_points = np.array(image_points, dtype=np.float32)

if cropped:
    success, rotation_vector, translation_vector = cv.solvePnP(
        world_points, image_points, camera_matrix, distortion_coefficients
    )
else:
    success, rotation_vector, translation_vector = cv.solvePnP(
        world_points, image_points, new_camera_matrix, distortion_coefficients
    )

if not success:
    print("Failed to solve PnP")
    sys.exit(1)

rotation_matrix, _ = cv.Rodrigues(rotation_vector)

extrinsic_matrix = np.hstack((rotation_matrix, translation_vector))
extrinsic_matrix = np.vstack((extrinsic_matrix, [0, 0, 0, 1]))

pretty_print_matrix(extrinsic_matrix)

plot_camera(extrinsic_matrix, 50)
