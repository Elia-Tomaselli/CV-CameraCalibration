import os
import shutil

# This python script clears the frames and videos directory

distorted_folder = os.path.join("frames", "distorted")
undistorted_folder = os.path.join("frames", "undistorted")
stitched_folder = os.path.join("frames", "stitched")

# cropped_folder = os.path.join("videos", "cropped")

folders = [
    distorted_folder,
    undistorted_folder,
    stitched_folder,
    # cropped_folder
]

for folder in folders:
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)

        try:
            if os.path.isfile(file_path) and file_name.endswith(".png"):
                os.unlink(file_path)

        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
