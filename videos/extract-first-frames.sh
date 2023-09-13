#!/bin/bash

for ((i=1; i<=8; i++))
do
    ffmpeg -i out$i.mp4 -vf "select=eq(n\,0)" -vframes 1 ../images/out$i.png
done
