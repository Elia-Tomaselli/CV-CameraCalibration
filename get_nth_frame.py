# This script will get the nth frame from a video file.

import argparse
import cv2 as cv
import os


def main(args):
    project_directory = os.path.dirname(os.path.abspath(__file__))

    image = get_nth_frame(args.video_path, args.n)

    if image is not None:
        filename, extension = os.path.splitext(os.path.basename(args.video_path))
        cv.imwrite(os.path.join(project_directory, f"{filename}-{args.n}.jpg"), image)

        # cv.imshow(f"Frame {args.n}", image)
        # cv.waitKey(0)
        # cv.destroyAllWindows()


def get_nth_frame(video_path, n):
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Couldn't open video file")
        return None

    cap.set(cv.CAP_PROP_POS_FRAMES, n)

    ret, frame = cap.read()
    if not ret:
        print(f"Error: Couldn't read frame {n}")
        return None

    cap.release()
    return frame


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the nth frame from a video file")

    parser.add_argument("video_path", type=str, help="The path to the video file")

    parser.add_argument("n", type=int, help="The frame number")

    args = parser.parse_args()

    main(args)
