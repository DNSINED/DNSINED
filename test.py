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
    input_name = image
    output_width = 900                   
    img = Image.open(input_name)
    wpercent = (output_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((output_width,hsize), Image.Resampling.LANCZOS)                 
    extract_colors(input_name, 400)


def extract_colors(input_image, resize):         
    output_width = resize
    img = Image.open(input_image)
    if img.size[0] >= resize:
        wpercent = (output_width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((output_width,hsize), Image.Resampling.LANCZOS)
        resize_name = 'resize_'+ input_image
        img.save(resize_name)
    else:
        resize_name = input_image
    img_url = resize_name
    colors_x = extract_from_path(img_url)
    return colors_x


def extract_from_image(img):
    pixels = _load(img)
    colors = _count_colors(pixels)

    return colors
   


def extract_from_path(path):
    img = Image.open(path)
    return extract_from_image(img)


def _load(img):
    img = img.convert("RGB")
    return list(img.getdata())


def _count_colors(pixels):
    counter = collections.defaultdict(int)
    for color in pixels:
        counter[color] += 1
    return counter


def rgb_2_hex(input):
    hex_dict ={}
    for rgb, count in input.items():
        hex = '#%02x%02x%02x' % rgb
        hex_dict[hex] = count
    return hex_dict


if __name__ == "__main__":
    video_file = "zoo.mp4"

    frame_extractor(video_file)
    path, _ = os.path.splitext(video_file)
    path += "_frames"
    files = os.listdir(path)
    os.chdir(path)
    resize = 900
    all_colors = {}
    for image in files:
       colors = extract_colors(image, resize)
    for x in list(colors.keys()):
       if x in all_colors.keys():
          all_colors[x] = all_colors[x] + colors[x]
          del colors[x]
    all_colors.update(colors)
    colors.clear()

    hex_dict = rgb_2_hex(all_colors)
    with open('colors.csv', 'w') as f:
       for key in hex_dict.keys():
           f.write("%s,%s\n"%(key,hex_dict[key]))
