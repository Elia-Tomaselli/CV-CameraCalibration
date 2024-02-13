# Basketball court | Stitching using [openStitching](https://github.com/OpenStitching)

Preview the tutorial [here](https://github.com/lukasalexanderweber/stitching_tutorial/blob/master/docs/Stitching%20Tutorial.md)

## Installation 👷‍♂️

Install the dependencies.

```bash
pip3 install -r requirements.txt
```

Make sure to have also **Ffmpeg** installed in your system ⚠️

## Usage 🕹️

```bash
python3 stitch.py -i input_video.mp4 -o output_video.mp4
```

- First of all, two crops of the `stitch.mp4` video are created using *Ffmpeg*, which correspond to two different optics of the camera. These crops to stitch are saved in the `Video` folder.
- The frames of the two crops are extracted and saved in the `Frames` folder, where corresponding frames are named `frame{i}_left` and `frame{i}_right`.
- The code implementation allows to stitch together corresponding frames, and stitched images are stored in the `Result` folder.
- Once all the frames are successfully stitched, a final video is created.

The homography matrix and camera calibration parameters are computed only for the first frame and then saved in the `cameras.yml` file. These parameters are subsequently reused for successive frames to accelerate the stitching process.

## Final result 🎞️

The final result is stored in the `output_video.avi` file.
