import os
import cv2
import time
import numpy as np
from PIL import Image
from datetime import timedelta
import collections
from PIL import Image

st = time.time()
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
    for i in np.arange(0, clip_duration, 1 / saving_fps):
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
                frames_dir, f"frame{frame_duration_formatted}.jpg"), frame)
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

def hex_2_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def change_color(frame, hex_code):
    img_dir, _ = os.path.splitext(img)
    img_dir += "_image_changed"
    rgb_code = hex_2_rgb(hex_code)
    img = Image.open(frame)
    img = img.convert("RGB")
 
    data_rgb = img.getdata()
 
    new_image = []
    for item in data_rgb:
        if item[0] == rgb_code:
            new_image.append((255, 0, 0))
        else:
            new_image.append(item)
         
    img.putdata(new_image)
   
    img.save(img_dir + ".jpg")

if __name__ == "__main__":
    video_file = "adventure_time.mkv"
    frames_dir, _ = os.path.splitext(video_file)
    frames_dir += "_frames"
    #frame_extractor(video_file, frames_dir)
    
    files = get_files(frames_dir)
    #files = files[100:130] # for debugging purposes

    all_colors = collections.defaultdict(int)
    for image in files:
        colors = extract_colors(image)
        for col in colors:
            all_colors[col] += colors[col]

    hex_dict = rgb_2_hex(all_colors)
    hex_list = list(hex_dict.items())
    hex_list.sort(key=lambda x: x[1], reverse=True)

    with open('colors.csv', 'w') as f:
        for hex in hex_list:
            f.write("%s,%s\n" % (hex[0], hex[1]))

    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    
    frame = ""
    hex_code = ()
    change_color(frame, hex_code)

