import cv2 as cv
from os import path

VIDEO_DIR = "videos"

video_paths = [
    path.join(VIDEO_DIR, "out14.mp4"),
    path.join(VIDEO_DIR, "out20.mp4"),
    path.join(VIDEO_DIR, "out42.mp4")
]

video = cv.VideoCapture(video_paths[0])

camera_calibration_matrix = [
    [3110,   0,    2048],
    [0,      3110, 900],
    [0,      0,    1],
]

# Verifica file video valido
if not video.isOpened():
    print("Errore nel caricamento del file")
    exit()

while True:
    # Lettura frame dal video
    ret, frame = video.read()

    # Verifica fine video
    if not ret:
        break

    cv.imshow("Frame", frame)

    if cv.waitKey(25) == ord('q'):
        break

video.release()
cv.destroyAllWindows()
