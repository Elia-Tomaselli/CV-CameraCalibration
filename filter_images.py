# Filtra le immagini in images/chessboards
# rimuovendo le immagini dove non
# compare alcuna scacchiera

import os
from os import path
import cv2 as cv
import numpy as np
from glob import glob

folders = [1, 2, 3, 4, 5, 6, 7, 8, 12, 13]
# Dimensione della scacchiera usata nei diversi video
chessboard_sizes = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 9), (6, 9), (6, 8), (6, 9), (6, 8), (6, 8)]

for index in range(len(folders)):
    folder = folders[index]
    chessboard_size = chessboard_sizes[index]
    images_path = path.join("images", "chessboards", str(folder))
    for file_path in glob(path.join(images_path, "*.png")):
        img = cv.imread(file_path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, chessboard_size, None)
        if not ret:
            os.remove(file_path)
    print("Folder " + str(folder) + " done.")