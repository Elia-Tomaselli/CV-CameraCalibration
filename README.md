# Single Camera Multiple Focus Calibration

This folder holds various python scripts that were developed during the 2023/2024 UniTN Computer Vision course project for the SanbàPolis sports hall cameras. One script here helps to get the extrinsic camera parameters from the different cameras. Each script's purpose is described below.

## Usage

### calibration_with_court.py

This script uses the volleyball court corner points to calculate the intrinsic matrix of the camera. It uses as input the distorted points in the *points.yaml* file. The output image is saved in the *images/undistorted_with_court* folder.

#### Arguments

- ``camera-number``: the camera you want to calibrate

```bash
# Example for checking the calibration using the court corner points of camera 3
python calibration_with_court.py 3
```

---

### extrinsics.py

This script uses the volleyball court corner points to calculate the extrinsic matrix of the camera. It uses as input either the undistorted_with_crop or undistorted_without_crop points in the *points.yaml* file. It also uses the intrinsic camera matrices in the *camera_parameters* folder.

#### Arguments

- ``camera-number``: the camera you want to calibrate
- either ``--with-crop`` (``-w``) or ``without-crop`` (``-wo``): choose between obtaining the extrinsic matrix using undistorted images with or without crop
- optionally ``--size`` (``-s``): this changes the size covered in the plot, defaults to 10

```bash
# Example for calibrating camera 2 using cropped undistorted images
python extrinsics.py 4 --without-crop -s 20
```

---

### get_nth_frame.py

This script is mostly for utility, it can be used to extract the nth frame from a video. The output image frame will be saved in the project directory.

#### Arguments

- ``video-path``: the input video path to extract the frame from
- ``n``: the nth frame to save

```bash
# Example for getting the first frame of a video
python get_nth_frame.py videos/out1.mp4 0
```

---

### show_points.py

This script is used to check were the points defined in the *points.yaml* file lie on the image. It uses the images in the *images/court* directory. To close the image preview window press **Esc**.

#### Arguments

- ``camera-number``: the camera you want to examine
- either ``--distorted`` (``-d``), ``--undistorted-with-crop`` (``-uw``) or ``--undistorted-without-crop`` (``-uwo``): choose between which image to inspect.

```bash
# Example for inspecting the points on the distorted image captured by camera 1
python show_points.py 1 --distorted
```

---

### split_video.py

This is a utility script that can be used to split the different sections of the videos captured from the cameras positioned on the ceiling (namely camera number 9, 10 and 11). Check that the variables declared inside, such as the video path and section sizes are correct. Also make sure to have **FFmpeg** installed.

```bash
python split_video.py
```

---

### undistort.py

This scripts uses the images in the *images/court/distorted* folder and the camera intrinsic matrices in the *camera_parameters* folder to undistort the images, and places them appropriately in the *images/court/undistorted_with_crop* or *images/court/undistorted_without_crop*.

#### Arguments

- ``camera-number``: the camera that has taken the image you want to undistort
- either ``--with-crop`` (``-w``) or ``without-crop`` (``-wo``): choose between having an undistorted image with or without crop

```bash
## Undistort the image captured from the camera number 3 with crop
python undistort.py 3 --with-crop
```
