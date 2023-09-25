import numpy as np
import cv2 as cv

# Define chessboard dimensions
CHESSBOARD_WIDTH = 5
CHESSBOARD_HEIGHT = 7

# Termination criteria for corner detection
termination_criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points, like (0, 0, 0), (1, 0, 0), (2, 0, 0), ..., (6, 5, 0)
object_points = np.zeros((CHESSBOARD_WIDTH * CHESSBOARD_HEIGHT, 3), np.float32)
object_points[:, :2] = np.mgrid[0:CHESSBOARD_WIDTH, 0:CHESSBOARD_HEIGHT].T.reshape(-1, 2)

# Arrays to store object points and image points from the video frames
world_points = []  # 3D point in real-world space
image_points = []  # 2D points in image plane

# Open the video file
video_capture = cv.VideoCapture('video/out1F.mp4')  # Replace 'your_video.mp4' with the path to your video file

frame_count = int(video_capture.get(cv.CAP_PROP_FRAME_COUNT))
print(f"Total frames in the video: {frame_count}")

desired_start_frame = 500
video_capture.set(cv.CAP_PROP_POS_FRAMES, desired_start_frame) # Set the starting frame of the video capture

frame_count = 0
max_saved_frames = 30
output_folder = 'saved_frames'

while frame_count < max_saved_frames:
    # Read a frame from the video
    ret, frame = video_capture.read()
    if not ret:
        break  # Break the loop if we've reached the end of the video

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Find the chessboard corners
    found_corners, corners = cv.findChessboardCorners(gray, (CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT), None)
    print(found_corners)
    
    if found_corners:
        frame_count += 1

        # Refine corner positions
        refined_corners = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), termination_criteria)
        
        # Save the frame with detected corners
        frame_filename = f"{output_folder}/frame_{frame_count}.jpg"
        cv.imwrite(frame_filename, frame)

        # Add object points and image points
        world_points.append(object_points)
        image_points.append(refined_corners)

        # Draw and display the corners (optional)
        cv.drawChessboardCorners(frame, (CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT), refined_corners, found_corners)
        cv.imshow('Frame', frame)
        cv.waitKey(100)  # Adjust the delay as needed

video_capture.release()
cv.destroyAllWindows()

# Calibrate the camera using the saved frames
if len(image_points) >= max_saved_frames:
    calibration_success, camera_matrix, distortion_coeffs, _, _ = cv.calibrateCamera(
        world_points, image_points, gray.shape[::-1], None, None)

    # Print the calibration results
    if calibration_success:
        print("Camera matrix:")
        print(camera_matrix)
        print("\nDistortion coefficients:")
        print(distortion_coeffs)
    else:
        print("Calibration failed.")
else:
    print(f"Not enough frames with chessboard found. Found {len(image_points)} frames, required {max_saved_frames}.")

# test undistortion on an image
img = cv.imread('samples/test_undist.jpg')
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(camera_matrix, distortion_coeffs, (w,h), 1, (w,h))
new_image = cv.undistort(img, camera_matrix, distortion_coeffs, None, newcameramtx)
cv.imwrite('samples/undistorted.jpg', new_image)