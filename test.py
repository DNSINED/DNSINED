import os
import cv2
import numpy as np
from PIL import Image
from datetime import timedelta
import collections
from PIL import Image


SAVING_FRAMES_PER_SECOND = 2


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
    global colors_x, pixels_x           
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
    colors_x, pixels_x = extract_from_path(img_url)
    

def extract_from_image(img): #,limit):
    pixels = _load(img)
    pixel_count = len(pixels)
    pixels = _filter_fully_transparent(pixels)
    pixels = _strip_alpha(pixels)
    colors = _count_colors(pixels)

    return colors, pixel_count
   

def extract_from_path(path):
    img = Image.open(path)
    return extract_from_image(img)


def _load(img):
    img = img.convert("RGBA")
    return list(img.getdata())


def _filter_fully_transparent(pixels):
    return [p for p in pixels if p[3] > 0]


def _strip_alpha(pixels):
    return [(p[0], p[1], p[2]) for p in pixels]


def _count_colors(pixels):
    counter = collections.defaultdict(int)
    for color in pixels:
        counter[color] += 1
    return counter


def dict_hex(rgb_dict):
    global hex_dict
    hex_dict ={}
    for rgb, count in rgb_dict.items():
       hex = '#%02x%02x%02x' % rgb
       hex_dict[hex] = count
    return hex_dict


if __name__ == "__main__":
    video_file = "rick&morty.jpg"
    frame_extractor(video_file)
    path, _ = os.path.splitext(video_file)
    path += "_frames"
    files = os.listdir(path)
    os.chdir(path)
    resize = 900
    for image in files:
        extract_colors(image, resize)

    dict_hex(colors_x)
    with open('colors.csv', 'w') as f:
        for key in hex_dict.keys():
             f.write("%s,%s\n"%(key,hex_dict[key]))
