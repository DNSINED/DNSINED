import os
import cv2
import numpy as np
import extcolors
from colormap import rgb2hex
from PIL import Image
from datetime import timedelta
import pdb


SAVING_FRAMES_PER_SECOND = 2

global COLOR
global OCCURENCE_RATE
COLOR = []
OCCURENCE_RATE = []

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
    img_url = input_name
    colors_x = extcolors.extract_from_path(img_url)
    colors_x
    
    df_color = rgb_to_hex(colors_x)
    df_color
    extract_colors(input_name, 400, 5 , 20)

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
    colors_x = extcolors.extract_from_path(img_url)
    df_color = rgb_to_hex(colors_x)


def rgb_to_hex(input):
    global COLOR
    global OCCURENCE_RATE

    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
                            
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                        int(i.split(", ")[1]),
                        int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
                        
    COLOR.extend(df_color_up)
    OCCURENCE_RATE.extend(df_percent)



if __name__ == "__main__":
    video_file = "zoo.mp4"

    frame_extractor(video_file)
    path, _ = os.path.splitext(video_file)
    path += "_frames"
    files = os.listdir(path)
    os.chdir(path)
    resize = 900
    tolerance = 0
    limit = 10
    for image in files:

        extract_colors(image, resize)
        COLOR = list(set(COLOR))
        OCCURENCE_RATE = list(set(OCCURENCE_RATE))

    print(COLOR)
    print(OCCURENCE_RATE)
