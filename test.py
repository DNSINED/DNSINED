import os
import cv2
import numpy as np
from PIL import Image
from datetime import timedelta
import collections
from PIL import Image


SAVING_FRAMES_PER_SECOND = 10


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
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def frame_extractor(video_file):
    filename, _ = os.path.splitext(video_file)
    filename += "_frames"
    if not os.path.isdir(filename):
        os.mkdir(filename) 
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_durations = get_saved_frames_durations(cap, saving_frames_per_second)
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
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            cv2.imwrite(os.path.join(filename,f"frame{frame_duration_formatted}.jpg"), frame)        
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass    
        count += 1


def color_extractor(image):         
    colors_x = extract_from_image(image)
    return colors_x


def extract_from_image(img):
    img = Image.open(path)
    img = img.convert("RGB")
    counter = collections.defaultdict(int)
    for color in img:
        counter[color] += 1
    return counter    


def rgb_2_hex(input):
    hex_dict ={}
    for rgb, count in input.items():
        hex = '#%02x%02x%02x' % rgb
        hex_dict[hex] = count
    return hex_dict


if __name__ == "__main__":
    video_file = "adventure_time.mkv"

    frame_extractor(video_file)
    path, _ = os.path.splitext(video_file)
    path += "_frames"
    files = os.listdir(path)
    os.chdir(path)
    resize = 900
    all_colors = collections.defaultdict(int)
    for image in files:
       colors = color_extractor(image)
       for col in colors:
        all_colors[col] += colors[col]

    hex_dict = rgb_2_hex(all_colors)
    with open('colors.csv', 'w') as f:
       for key in hex_dict.keys():
           f.write("%s,%s\n"%(key,hex_dict[key]))
