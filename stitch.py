from tqdm import tqdm
import argparse
import cv2 as cv
import glob
import numpy as np
import os
import yaml

from stitching.blender import Blender
from stitching.camera_adjuster import CameraAdjuster
from stitching.camera_estimator import CameraEstimator
from stitching.camera_wave_corrector import WaveCorrector
from stitching.cropper import Cropper
from stitching.exposure_error_compensator import ExposureErrorCompensator
from stitching.feature_detector import FeatureDetector
from stitching.feature_matcher import FeatureMatcher
from stitching.images import Images
from stitching.seam_finder import SeamFinder
from stitching.warper import Warper


class Stitcher:
    def stitch(self, frame_number: int, computeHomography: bool = True) -> np.ndarray:
        frame_path_like = os.path.join(
            "frames", "undistorted", f"frame{frame_number}*.png"
        )
        frame_imgs = glob.glob(frame_path_like)
        imgs = Images.of(frame_imgs)

        # For the first frame to stitch, compute the homography matrix and save it
        if computeHomography:
            # Resize the images to medium (and later to low) resolution
            medium_imgs = list(imgs.resize(Images.Resolution.MEDIUM))

            # Find features
            # finder = FeatureDetector(detector="orb", nfeatures=500)
            finder = FeatureDetector(detector="orb", nfeatures=10000)
            features = [finder.detect_features(img) for img in medium_imgs]

            # Match the features of the pairwise images
            matcher = FeatureMatcher()
            matches = matcher.match_features(features)

            # Calibrate cameras which can be used to warp the images
            camera_estimator = CameraEstimator()
            camera_adjuster = CameraAdjuster()
            wave_corrector = WaveCorrector()

            cameras = camera_estimator.estimate(features, matches)
            cameras = camera_adjuster.adjust(features, matches, cameras)
            cameras = wave_corrector.correct(cameras)

            # Save camera calibration parameters
            self.save_cameras(cameras)

            # Warp the images into the final plane
            panorama = self.warping_blending(imgs, cameras)
        else:
            # Get camera calibration parameters
            cameras = self.load_cameras()
            panorama = self.warping_blending(imgs, cameras)

        return panorama

    def save_cameras(self, cameras: list[cv.detail.CameraParams]):
        yaml_data = {}

        for i, camera in enumerate(cameras):
            data = {
                "focal": camera.focal,
                "aspect": camera.aspect,
                "ppx": camera.ppx,
                "ppy": camera.ppy,
                "R": camera.R.tolist(),
                "t": camera.t.tolist(),
            }
            yaml_data[f"camera{i+1}"] = data

        with open("cameras.yaml", "w") as file:
            # To save the data for better human readability
            # use the default_flow_style=None parameter and sort_keys=False
            yaml.dump(yaml_data, file, default_flow_style=None, sort_keys=False)

    def load_cameras(self) -> list[cv.detail.CameraParams]:
        cameras = []

        with open("cameras.yaml", "r") as file:
            yaml_data = yaml.load(file, Loader=yaml.FullLoader)

        for camera_name, camera_values in yaml_data.items():
            camera = cv.detail.CameraParams()

            camera.focal = camera_values["focal"]
            camera.aspect = camera_values["aspect"]
            camera.ppx = camera_values["ppx"]
            camera.ppy = camera_values["ppy"]
            camera.R = np.array(camera_values["R"])
            camera.t = np.array(camera_values["t"])

            cameras.append(camera)

        return cameras

    def warping_blending(self, imgs: Images, cameras: list[str]) -> np.ndarray:
        low_imgs = list(imgs.resize(Images.Resolution.LOW))
        final_imgs = list(imgs.resize(Images.Resolution.FINAL))

        # Select the warper
        warper = Warper(warper_type="paniniA1.5B1")
        # Set the the medium focal length of the cameras as scale
        warper.set_scale(cameras)

        # Warp low resolution images
        low_sizes = []
        for img in low_imgs:
            low_sizes.append(imgs.get_image_size(img))
        camera_aspect = imgs.get_ratio(Images.Resolution.MEDIUM, Images.Resolution.LOW)

        warped_low_imgs = list(warper.warp_images(low_imgs, cameras, camera_aspect))
        warped_low_masks = list(
            warper.create_and_warp_masks(low_sizes, cameras, camera_aspect)
        )
        low_corners, low_sizes = warper.warp_rois(low_sizes, cameras, camera_aspect)

        # Warp final resolution images
        final_sizes = []
        for img in final_imgs:
            final_sizes.append(imgs.get_image_size(img))
        camera_aspect = imgs.get_ratio(
            Images.Resolution.MEDIUM, Images.Resolution.FINAL
        )

        warped_final_imgs = list(warper.warp_images(final_imgs, cameras, camera_aspect))
        warped_final_masks = list(
            warper.create_and_warp_masks(final_sizes, cameras, camera_aspect)
        )
        final_corners, final_sizes = warper.warp_rois(
            final_sizes, cameras, camera_aspect
        )

        # Estimate the largest joint interior rectangle and crop the single images accordingly
        cropper = Cropper()
        mask = cropper.estimate_panorama_mask(
            warped_low_imgs, warped_low_masks, low_corners, low_sizes
        )
        lir = cropper.estimate_largest_interior_rectangle(mask)
        low_corners = cropper.get_zero_center_corners(low_corners)
        rectangles = cropper.get_rectangles(low_corners, low_sizes)
        overlap = cropper.get_overlap(rectangles[1], lir)
        intersection = cropper.get_intersection(rectangles[1], overlap)

        cropper.prepare(warped_low_imgs, warped_low_masks, low_corners, low_sizes)

        cropped_low_masks = list(cropper.crop_images(warped_low_masks))
        cropped_low_imgs = list(cropper.crop_images(warped_low_imgs))
        low_corners, low_sizes = cropper.crop_rois(low_corners, low_sizes)

        lir_aspect = imgs.get_ratio(Images.Resolution.LOW, Images.Resolution.FINAL)
        cropped_final_masks = list(cropper.crop_images(warped_final_masks, lir_aspect))
        cropped_final_imgs = list(cropper.crop_images(warped_final_imgs, lir_aspect))
        final_corners, final_sizes = cropper.crop_rois(
            final_corners, final_sizes, lir_aspect
        )

        # Seam masks to find a transition line between images with the least amount of interference
        seam_finder = SeamFinder()
        seam_masks = seam_finder.find(cropped_low_imgs, low_corners, cropped_low_masks)
        seam_masks = [
            seam_finder.resize(seam_mask, mask)
            for seam_mask, mask in zip(seam_masks, cropped_final_masks)
        ]

        # Exposure error compensation
        compensator = ExposureErrorCompensator()
        compensator.feed(low_corners, cropped_low_imgs, cropped_low_masks)
        compensated_imgs = [
            compensator.apply(idx, corner, img, mask)
            for idx, (img, mask, corner) in enumerate(
                zip(cropped_final_imgs, cropped_final_masks, final_corners)
            )
        ]

        # Blending
        blender = Blender()
        blender.prepare(final_corners, final_sizes)
        for img, mask, corner in zip(compensated_imgs, seam_masks, final_corners):
            blender.feed(img, mask, corner)
        panorama, _ = blender.blend()

        return panorama


def stitch_images(stitcher: Stitcher, n_frames: int) -> None:
    """
    Stitches the images in the frames/undistorted folder and saves the
    stitched images in the frames/stitched folder.

    :param stitcher: Stitcher object.
    :param n_frames: Number of frames to stitch.
    """

    stitched_folder = os.path.join("frames", "stitched")

    if not os.path.exists("frames"):
        os.mkdir("frames")

    if not os.path.exists(stitched_folder):
        os.mkdir(stitched_folder)

    for i in tqdm(range(n_frames)):
        # for i in tqdm(range(n_frames)):
        output_path = os.path.join(stitched_folder, f"frame_{i}.png")

        if i == 0:
            panorama = stitcher.stitch(i, computeHomography=True)
        else:
            panorama = stitcher.stitch(i, computeHomography=False)

        # Save the stitched images in frames/stitched folder
        cv.imwrite(output_path, panorama)


def crop_video(video_path: str) -> None:
    """
    Crops the input video into two videos using ffmpeg.
    The left video is saved as videos/cropped/left.mp4 and the right video
    is saved as videos/cropped/right.mp4.
    WHEN YOU RUN THE PROGRAM ON DIFFERENT CAMERAS, YOU NEED TO CHANGE THE HEIGHT,
    WIDTH AND OFFSET_X PARAMETERS IN THE FUNCTION, OR CHECK IF THEY ARE CORRECT.

    :param video_path: Path to the input video.
    """

    cropped_folder = os.path.join("videos", "cropped")

    if not os.path.exists("videos"):
        os.mkdir("videos")

    if not os.path.exists(cropped_folder):
        os.mkdir(cropped_folder)

    # Camera 10 has height 1800 and width 4096, the four sections are all equally wide 1024
    # height = 1800
    # width = 1024
    # offsetX = 1024

    # Camera 9 and 11 have height 1792 and width 4096, the four sections are wide 896, 1152, 1152, 896 respectively
    height = 1792
    width = 1152
    offset_x = 896

    left_video_path = os.path.join(cropped_folder, "left.mp4")
    right_video_path = os.path.join(cropped_folder, "right.mp4")

    # Right now the two middle sections of the video are saved in the videos/cropped folder
    # It would be better to crop all 4 sections of the video and save them all in the videos/cropped folder
    # This way we can stitch all four sections at the same time
    os.system(
        f'ffmpeg -i {video_path} -filter:v "crop={width}:{height}:{offset_x}:0" {left_video_path}'
    )
    os.system(
        f'ffmpeg -i {video_path} -filter:v "crop={width}:{height}:{offset_x + width}:0" {right_video_path}'
    )


def get_number_of_frames(video_path: str) -> int:
    """
    Returns the number of frames in the input video.

    :param video: Path to the input video.
    :return: Number of frames in the video.
    """

    cap = cv.VideoCapture(video_path)
    length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    return length


def get_image_size(img_path: str) -> tuple[int, int]:
    """
    Returns the size of the input image.

    :param img_path: Path to the input image.
    :return: Size of the image.
    """

    img = cv.imread(img_path)
    height, width, _ = img.shape
    return (width, height)


def extract_frames(n_frames: int) -> None:
    """
    Extracts every frame from the video in the videos/cropped folder and
    saves themin the frames/distorted folder.

    :param videos: List of video paths to extract frames from.
    """

    cropped_folder = os.path.join("videos", "cropped")
    distorted_folder = os.path.join("frames", "distorted")

    if not os.path.exists("frames"):
        os.mkdir("frames")

    if not os.path.exists(distorted_folder):
        os.mkdir(distorted_folder)

    videos = glob.glob(os.path.join(cropped_folder, "*.mp4"))
    with tqdm(total=n_frames * len(videos)) as pbar:
        for video in videos:
            original_video_name = os.path.splitext(os.path.basename(video))[0]
            cap = cv.VideoCapture(video)
            count = 0

            while True:
                success, img = cap.read()

                if not success:
                    break

                frame_file_name = f"frame{count}_{original_video_name}.png"
                output_path = os.path.join(distorted_folder, frame_file_name)
                cv.imwrite(output_path, img)
                count += 1
                pbar.update(1)


def read_csv_map(file_name: str) -> np.ndarray:
    """
    Reads a csv file as a numpy array.

    :param file_name: Path to the csv file.
    """

    with open(file_name, "r") as file:
        data = np.loadtxt(file, delimiter=",")

    return data


def calibrate_images() -> None:
    """
    Takes the images in the frames/distorted folder and undistorts them
    using the calibration parameters found in the calibration folder.
    The undistorted images are saved in the frames/undistorted folder.
    """

    distorted_folder = os.path.join("frames", "distorted")
    undistorted_folder = os.path.join("frames", "undistorted")

    if not os.path.exists("frames"):
        os.mkdir("frames")

    if not os.path.exists(undistorted_folder):
        os.mkdir(undistorted_folder)

    if not os.path.exists(distorted_folder):
        os.mkdir(distorted_folder)
        print(
            "No distorted images found in frames/distorted folder. Please extract frames from the video first."
        )
        return

    img_file_names = [
        os.path.basename(x) for x in glob.glob(os.path.join(distorted_folder, "*.png"))
    ]

    for img_file_name in tqdm(img_file_names):
        img = cv.imread(os.path.join(distorted_folder, img_file_name))

        if "left" in img_file_name:
            mapX = read_csv_map(os.path.join("calibration", "out11_left_map_x.csv"))
            mapY = read_csv_map(os.path.join("calibration", "out11_left_map_y.csv"))
        elif "right" in img_file_name:
            mapX = read_csv_map(os.path.join("calibration", "out11_right_map_x.csv"))
            mapY = read_csv_map(os.path.join("calibration", "out11_right_map_y.csv"))

        mapX = np.float32(mapX)
        mapY = np.float32(mapY)

        undistorted_img = cv.remap(img, mapX, mapY, cv.INTER_LINEAR)
        cv.imwrite(os.path.join(undistorted_folder, img_file_name), undistorted_img)


def build_video_from_frames(output_path: str, fps: int, n_frames: int) -> None:
    """
    Construct a video from a series of image frames.
    The frames are taken from the frames/stitched folder.

    :param output_path: Path to the output video file.
    :param fps: Frames per second for the output video.
    :param n_frames: Number of frames to include in the video.
    """

    size = get_image_size(os.path.join("frames", "stitched", "frame_0.png"))
    out = cv.VideoWriter(output_path, cv.VideoWriter_fourcc(*"DIVX"), fps, size)
    frames_folder = os.path.join("frames", "stitched")

    for i in tqdm(range(n_frames)):
        file_name = os.path.join(frames_folder, f"frame_{i}.png")
        frame = cv.imread(file_name)
        out.write(frame)

    out.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Video stitching",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-i",
        "--input-video",
        action="store",
        help="Specifies the input video",
        required=True,
    )

    parser.add_argument(
        "-o",
        "--output-video",
        action="store",
        help="Specifies the output video",
        required=True,
    )

    parser.add_argument(
        "--skip-crop",
        action="store_true",
        help="Skip the left and right video cropping step",
        required=False,
    )

    parser.add_argument(
        "--skip-extraction",
        action="store_true",
        help="Skip the frame extraction step",
        required=False,
    )

    parser.add_argument(
        "--skip-calibration",
        action="store_true",
        help="Skip the image calibration step",
        required=False,
    )

    args = parser.parse_args()

    n_frames = get_number_of_frames(args.input_video)

    if not args.skip_crop:
        print("----- Cropping Video -----")
        crop_video(args.input_video)

    if not args.skip_extraction:
        print("----- Extracting Frames -----")
        extract_frames(n_frames)

    if not args.skip_calibration:
        print("----- Calibrating Images -----")
        calibrate_images()

    print("----- Stitching Images -----")
    stitcher = Stitcher()
    stitch_images(stitcher, n_frames)

    print("----- Creating Final Video -----")
    fps = 30.0
    build_video_from_frames(args.output_video, fps, n_frames)
