import os

file_names = ["out11safe"]

starting_time = "00:00:30"
duration = "00:00:15"

for video_index in range(len(file_names)):
    file_name = file_names[video_index]
    input_path = f"videos/{file_name}.mp4"
    output_path = f"videos/{file_name}_trimmed.mp4"
    
    command = f"ffmpeg -i {input_path} -ss {starting_time} -t {duration} -c:v copy -c:a copy {output_path}"
    os.system(command)    
