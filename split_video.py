import os

file_names = ["out9safe", "out10safe", "out11safe"]

# The four sections of the videos out9safe.mp4 and out11safe.mp4
#do not have the same width 
# the 1st and the 4th sections are a little bit smaller
# compared to the 2nd and the 3rd
video_widths = [[896, 1152, 1152, 896], [1024, 1024, 1024, 1024], [896, 1152, 1152, 896]]
video_heights = [1792, 1800, 1792]

for video_index in range(len(file_names)):
    file_name = file_names[video_index]
    input_path = os.path.join("videos", f"{file_name}.mp4")
    section_widths = video_widths[video_index]
    height = video_heights[video_index]

    for section_index in range(len(section_widths)):
        offset_x = sum(section_widths[0:section_index])
        output_path = os.path.join("videos", f"{file_name}_section{section_index + 1}.mp4")
        width = section_widths[section_index]
        
        command = f"ffmpeg -i {input_path} -filter:v crop={width}:{height}:{offset_x}:0 {output_path} -y"
        os.system(command)
