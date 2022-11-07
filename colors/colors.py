# from lib2to3.pgen2.pgen import generate_grammar 
import os
# import sys
import cv2
import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import matplotlib.image as mpimg
# from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import extcolors
from colormap import rgb2hex
from PIL import Image
from datetime import timedelta
# import glob


SAVING_FRAMES_PER_SECOND = 2
# Are you using a global variable to store results?
# This is horrible. Don't ever use global variables like this.
# Functions get parameters and return results. That's it.
# Global variables have their place from time to time. But rarely.
# And never for something as common as storing results.
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

# But why does this function need to know that the frames are being saved?
# It's none of its business how the frames are used or how the durations are used.
# It gets a clip and creates a list of durations.
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
    colors_x = extcolors.extract_from_path(img_url, tolerance = 12, limit = 12)
    colors_x
    
    df_color = rgb_to_hex(colors_x)
    df_color
    extract_colors(input_name, 400, 5 , 20)

def extract_colors(input_image, resize, tolerance,limit):                
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
    colors_x = extcolors.extract_from_path(img_url, tolerance = tolerance, limit = limit)
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
    OCCURENCE_RATE.extend(df_percent) #needs more attention!!!



if __name__ == "__main__":
    video_file = "zoo.mp4"
    # How does main_frame know where to store the frames?
    # Oh, there's an implicit convention that it generates them in a folder.
    # So both __main__ and main_frame need to know to do path, _ = os.path.splitext(video_file)
    # in order to get the path where the frames are.
    # So here's the story so far:

    # Hi, I'm main_frame. I get a video file and I generate frames. I decide where the frames are put.
    # I don't tell anyone where I put the frames. And I'm not directly told how many frames to generate
    # or how many frames per second to generate or anything like that. Screw you, read my code
    # if you want to find out.
    frame_extractor(video_file)

    # Hi, I'm __main__. I also know where the frames are put.
    # Not because main_frame told me, but because I know the same thing as main_frame.
    # So we both have to know the same thing and if one of us changes his mind, the author needs to
    # remember to update the other one.
    # Also, I assume that all the files in the folder will be images. Nobody told me this,
    # I just assume it.
    path, _ = os.path.splitext(video_file)
    path += "_frames"
    files = os.listdir(path)
    os.chdir(path) # magic!

    for image in files:
        # Hi. I'm main_color. I get the name of the frame and I don't return anything.
        # If you want to find out what my result is, you have to read every line of my code.
        extract_colors(image)
        COLOR = list(set(COLOR))

    print(COLOR) #for test

    # Here's a better story:

    # Hi, I generate frames from a video.
    # I am told what video it is, how many frames to generate and where to put the frames.
    # I return absolute paths to the files I just generated, so that the one calling me knows
    # exactly what files were generated. And I'm the only one who decides what the files are called.
    # frames = generate_frames(video, fps, dir_frames)
       
    # Hi, I extract colors from a set of images. I just need to know the paths to the images and I'll
    # tell you what the colors are in those images. Neat!
    # colors = extract_colors_from_images(frames)

    # print(colors) 