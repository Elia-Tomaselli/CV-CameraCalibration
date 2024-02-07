import os
import subprocess
import cv2 as cv


def get_nth_frame(video_path, n):
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Couldn't open video file")
        return None

    cap.set(cv.CAP_PROP_POS_FRAMES, n - 1)  # Set the frame position (zero-based index)

    ret, frame = cap.read()
    if not ret:
        print(f"Error: Couldn't read frame {n}")
        return None

    cap.release()
    return frame


camera_number = 12
video_path = os.path.join("videos", f"out{camera_number}.mp4")

output_directory = os.path.join("output", "court_images", "raw")
output_image_path = os.path.join(output_directory, f"out{camera_number}.jpg")

image = get_nth_frame(video_path, 1)

os.makedirs(output_directory, exist_ok=True)
cv.imwrite(output_image_path, image)