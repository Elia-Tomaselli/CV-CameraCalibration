<p align="center">
  <h2 align="center">Single Camera Multiple Focus Calibration</h2>
  <p align="center">Elia Tomaselli - Alessandro Rizzetto</p>
</p>

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Usage](#usage)
  - [SMART-VIDEO-camera-calibration.ipynb](#smart-video-camera-calibrationipynb)
  - [stitch.py](#stitchpy)
    - [Arguments](#arguments)
  - [calibration\_with\_court.py](#calibration_with_courtpy)
    - [Arguments](#arguments-1)
  - [extrinsics.py](#extrinsicspy)
    - [Arguments](#arguments-2)
  - [get\_nth\_frame.py](#get_nth_framepy)
    - [Arguments](#arguments-3)
  - [show\_points.py](#show_pointspy)
    - [Arguments](#arguments-4)
  - [split\_video.py](#split_videopy)
  - [undistort.py](#undistortpy)
    - [Arguments](#arguments-5)

# Introduction

This folder holds various python scripts that were developed during the 2023/2024 UniTN Computer Vision course project for the SanbàPolis sports hall cameras.

These scripts aid in obtaining both the intrinsic and extrinsic camera parameters from various cameras. Each script is accompanied by a description of its purpose.

# Usage

First of all install the required packages

```bash
pip3 install -r requirements.txt
```

Make sure to have also **FFmpeg** installed in your system.

## SMART-VIDEO-camera-calibration.ipynb

This Python notebook enables the extraction of extrinsic parameters and calibration of multiple cameras simultaneously. It uses as input the video files in the _video_ folder. The output images are saved in the _output_ folder and the camera parameters in the _pickle_ folder.

To run the notebook, open it in Jupyter Notebook and run all the cells you need.

---

## stitch.py

This script is used to stitch together the videos with different sections captured by the cameras installed on the ceiling. The script follows these steps:

1. Two crops of the input video are created using **FFmpeg**
2. The frames of the two crops are extracted and saved in the `frames/distorted` folder
3. The frames are undistorted using the calibration maps in the `calibration` folder, and the undistorted images are placed in the `frames/undistorted` folder
4. The different sections are stitched together and placed in the `frames/stitched` folder
5. All the stitched frames are merged into an output video

### Arguments

- `--input-video` (`-i`): the video to stitch the sections of
- `--output-video` (`-o`): the output video that is generated
- `--skip-crop`: if you wish to skip step 1.
- `--skip-extraction`: if you wish to skip step 2.
- `--skip-calibration`: if you wish to skip step 3.

```bash
python3 stitch.py -i input_video.mp4 -o output_video.mp4
```

---

## calibration_with_court.py

This script uses the volleyball court corner points to calculate the intrinsic matrix of the camera. It uses as input the distorted points in the _points.yaml_ file. The output image is saved in the _images/undistorted_with_court_ folder.

### Arguments

- `camera-number`: the camera you want to calibrate

```bash
# Example for checking the calibration using the court corner points of camera 3
python calibration_with_court.py 3
```

---

## extrinsics.py

This script uses the volleyball court corner points to calculate the extrinsic matrix of the camera. It uses as input either the undistorted*with_crop or undistorted_without_crop points in the \_points.yaml* file. It also uses the intrinsic camera matrices in the _camera_parameters_ folder.

### Arguments

- `camera-number`: the camera you want to calibrate
- either `--with-crop` (`-w`) or `without-crop` (`-wo`): choose between obtaining the extrinsic matrix using undistorted images with or without crop
- optionally `--size` (`-s`): this changes the size covered in the plot, defaults to 10

```bash
# Example for calibrating camera 2 using cropped undistorted images
python extrinsics.py 4 --without-crop -s 20
```

---

## get_nth_frame.py

This script is mostly for utility, it can be used to extract the nth frame from a video. The output image frame will be saved in the project directory.

### Arguments

- `video-path`: the input video path to extract the frame from
- `n`: the nth frame to save

```bash
# Example for getting the first frame of a video
python get_nth_frame.py videos/out1.mp4 0
```

---

## show_points.py

This script is used to check were the points defined in the _points.yaml_ file lie on the image. It uses the images in the _images/court_ directory. To close the image preview window press **Esc**.

### Arguments

- `camera-number`: the camera you want to examine
- either `--distorted` (`-d`), `--undistorted-with-crop` (`-uw`) or `--undistorted-without-crop` (`-uwo`): choose between which image to inspect.

```bash
# Example for inspecting the points on the distorted image captured by camera 1
python show_points.py 1 --distorted
```

---

## split_video.py

This is a utility script that can be used to split the different sections of the videos captured from the cameras positioned on the ceiling (namely camera number 9, 10 and 11). Check that the variables declared inside, such as the video path and section sizes are correct. Also make sure to have **FFmpeg** installed.

```bash
python split_video.py
```

---

## undistort.py

This scripts uses the images in the _images/court/distorted_ folder and the camera intrinsic matrices in the _camera_parameters_ folder to undistort the images, and places them appropriately in the _images/court/undistorted_with_crop_ or _images/court/undistorted_without_crop_.

### Arguments

- `camera-number`: the camera that has taken the image you want to undistort
- either `--with-crop` (`-w`) or `without-crop` (`-wo`): choose between having an undistorted image with or without crop

```bash
## Undistort the image captured from the camera number 3 with crop
python undistort.py 3 --with-crop
```
