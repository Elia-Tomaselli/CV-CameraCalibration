import cv2 as cv
from os import path 

def split_video(input_video, output_left, output_right):
    cap = cv.VideoCapture(input_video)
    
    # Get the video's frame width and height
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define codec and create VideoWriter objects for left and right halves
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out_left = cv.VideoWriter(output_left, fourcc, 30.0, (frame_width // 2, frame_height))
    out_right = cv.VideoWriter(output_right, fourcc, 30.0, (frame_width // 2, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Split the frame into left and right halves
        left_half = frame[:, :frame_width // 2, :]
        right_half = frame[:, frame_width // 2:, :]

        # Write the left and right halves to their respective output files
        out_left.write(left_half)
        out_right.write(right_half)

    cap.release()
    out_left.release()
    out_right.release()

if __name__ == "__main__":
    FILE_NAME = "out10"
    input_video = path.join("videos", FILE_NAME + ".mp4")
    output_left = path.join("videos", FILE_NAME + "_left.mp4")
    output_right = path.join("videos", FILE_NAME + "_right.mp4")

    split_video(input_video, output_left, output_right)
    print("Done splitting video")
