#!/bin/bash

video_numbers=(1 2 3 4 5 6 7 8 12 13)
sample_rate=10

for video_number in "${video_numbers[@]}"; do
    output_folder="../images/chessboards/${video_number}"
    file_name="out${video_number}F.mp4"
    ffmpeg -i $file_name -vf "select=not(mod(n\,$sample_rate))" -vsync vfr $output_folder/%d.png
done
