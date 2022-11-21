import os
import cv2
import time
import numpy as np
from PIL import Image
from datetime import timedelta
import collections
from PIL import Image


SAVING_FRAMES_PER_SECOND = 1


def format_timedelta(td):
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")

def get_saved_frames_durations(cap, saving_fps):
    s = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / \
        cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(300 , clip_duration-300, 1 / saving_fps):
        s.append(i)
    return s

def frame_extractor(video_file, frames_dir):
    if not os.path.isdir(frames_dir):
        os.mkdir(frames_dir)
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_durations = get_saved_frames_durations(
        cap, saving_frames_per_second)
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            break
        frame_duration = count / fps
        try:
            closest_duration = saving_frames_durations[0]
        except IndexError:
            break
        if frame_duration >= closest_duration:
            frame_duration_formatted = format_timedelta(
                timedelta(seconds=frame_duration))
            cv2.imwrite(os.path.join(
                frames_dir, f"frame{frame_duration_formatted}.png"), frame)
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        count += 1

def extract_colors(image_file):
    img = Image.open(image_file)
    img = img.convert("RGB")
    img = list(img.getdata())
    colors = collections.defaultdict(int)
    for color in img:
        colors[color] += 1
    return colors

def rgb_2_hex(input):
    hex_dict = {}
    for rgb, count in input.items():
        hex = '#%02x%02x%02x' % rgb
        hex_dict[hex] = count
    return hex_dict

def get_files(directory):
    files = os.listdir(directory)
    full_paths = []
    for file in files:
        full_paths.append(os.path.join(directory, file))
    return full_paths


def apply_tolerance(rgb_list, tl):
    rgb_list = list(rgb_list)
    rgb_list.sort(key=lambda x: x[1], reverse=True)
    duplicates = set()
    for idx, (codes, occurrence) in enumerate(rgb_list):
        for idx2 in range(idx + 1, len(rgb_list)):
            code = rgb_list[idx2][0]
            occ = rgb_list[idx2][1]
            r = abs(codes[0]-code[0])
            g = abs(codes[1]-code[1])
            b = abs(codes[2]-code[2])
            if r <= tl and g <= tl and b <= tl:
                occurrence += occ
                rgb_list[idx] = (codes, occurrence)
                duplicates.add(code)

    rgb = []
    for codes, occurrence in rgb_list:
        if codes not in duplicates:
            rgb.append((codes, occurrence))

    return(rgb)

def hex_2_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def change_color(frame, hex_code):
    name = hex_code
    rgb_code = hex_2_rgb(hex_code)
    img = Image.open(frame)
    img = img.convert("RGB")

    data_rgb = list(img.getdata())
    new_image = []

    for item in data_rgb:
        if item == rgb_code:
            new_image.append((255, 0, 0))
        else:
            new_image.append(item)   
    img.putdata(new_image)
   
    img.save(name + ".png")

def colors_are_similar(col1, col2, tl):
    r = abs(col1[0]-col2[0])
    g = abs(col1[1]-col2[1])
    b = abs(col1[2]-col2[2])
    return r <= tl and g <= tl and b <= tl

def apply_tolerance_frame(frame, code_rgb, tl):
    img = Image.open(frame)
    img = img.convert("RGB")

    data_rgb = list(img.getdata())
    new_image = []    
    for code in data_rgb:
        if colors_are_similar(code, code_rgb[0], tl):
            new_image.append((255, 0, 0))
        else:
            new_image.append(code) 
    img.putdata(new_image)    
    img.save("new_img.png")

def rgb_code(frame, color_list, tl):
    for col in color_list:
        apply_tolerance_frame(frame, col, tl)

def frames(frame_list, color_list, tl):
    for pic in frame_list:
        rgb_code(pic, color_list, tl)

if __name__ == "__main__":
    st = time.time()
    video_file = "adventure_time.mkv"
    frames_dir, _ = os.path.splitext(video_file)
    frames_dir += "_frames"
    tolerance = 10
    # frame_extractor(video_file, frames_dir)
    
    files = get_files(frames_dir)
    files = files[0:1] # for debugging purposes

    all_colors = collections.defaultdict(int)
    for image in files:
        colors = extract_colors(image)
        for col in colors:
            all_colors[col] += colors[col]

    all_colors = list(all_colors.items())
    all_colors.sort(key=lambda x: x[1], reverse=True)     
 
    # rgb_list = apply_tolerance(all_colors, tolerance)
    # rgb_list.sort(key=lambda x: x[1], reverse=True)
    # with open('colors.csv', 'w') as f:
    #     for rgb in rgb_list:
    #         f.write("%s,%s\n" % (rgb[0], rgb[1]))

    # frame = ""
    # hex_code = ()
    # change_color(frame, hex_code)

    color_list = all_colors[:10] 
    frames(files, color_list, tolerance)

    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
