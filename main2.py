import cv2 as cv
import numpy as np
from os import path
from pprint import pprint

arr = np.dstack(np.meshgrid(range(2000), range(3000))).astype(np.float32)

print(arr)
print()

arr[:, :, 0] = (arr[:, :, 0] + 1) * (255 / arr.shape[1])
arr[:, :, 1] = (arr[:, :, 1] + 1) * (255 / arr.shape[0])

print(arr)
print(arr[-1][-1])
