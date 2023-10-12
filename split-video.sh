#!/bin/bash

file_name="out10"
input_path="videos/$file_name.mp4"
output_path="videos/$file_name\_section"
width=$((4096/4))
height=1800

for ((i = 0; i < 4; i++)); do
    ffmpeg -i $input_path -filter:v "crop=$width:$height:$(($width * $i)):0" "$output_path$(($i + 1)).mp4" -y
done