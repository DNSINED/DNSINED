import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import extcolors
from colormap import rgb2hex
from PIL import Image
from datetime import timedelta

#test
#test2
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


def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def main(video_file):
    filename, _ = os.path.splitext(video_file)
    filename += "-frames"
    # make a folder by the name of the video file
    if not os.path.isdir(filename):
        os.mkdir(filename) 
    cap = cv2.VideoCapture(video_file)o
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)p
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
            cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame) 
            input_name = "colorat.jpg"
output_width = 900                   
img = Image.open(input_name)
wpercent = (output_width/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((output_width,hsize), Image.Resampling.LANCZOS)

resize_name = 'resize_' + input_name  
img.save(resize_name)                 
img_url = resize_name
colors_x = extcolors.extract_from_path(img_url, tolerance = 12, limit = 12)
colors_x

def exact_color(input_image, resize, tolerance, zoom):
    bg = 'bg.png'
    fig, ax = plt.subplots(figsize=(192,108),dpi=10)
    fig.set_facecolor('white')
    plt.savefig(bg)
    plt.close(fig)
    
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
        colors_x = extcolors.extract_from_path(img_url, tolerance = tolerance, limit = 13)
        df_color = color_to_df(colors_x)
    
        list_color = list(df_color['c_code'])
        list_precent = [int(i) for i in list(df_color['occurence'])]
        text_c = [c + ' ' + str(round(p*100/sum(list_precent),1)) +'%' for c, p in zip(list_color, list_precent)]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(160,120), dpi = 10)
    
        wedges, text = ax1.pie(list_precent,
                                labels= text_c,
                                labeldistance= 1.05,
                                colors = list_color,
                                textprops={'fontsize': 150, 'color':'black'})
        plt.setp(wedges, width=0.3)

        img = mpimg.imread(resize_name)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (0, 0))
        ax1.add_artist(ab)
    
        x_posi, y_posi, y_posi2 = 160, -170, -170
        for c in list_color:
            if list_color.index(c) <= 5:
                y_posi += 180
                rect = patches.Rectangle((x_posi, y_posi), 360, 160, facecolor = c)
                ax2.add_patch(rect)
                ax2.text(x = x_posi+400, y = y_posi+100, s = c, fontdict={'fontsize': 190})
            else:
                y_posi2 += 180
                rect = patches.Rectangle((x_posi + 1000, y_posi2), 360, 160, facecolor = c)
                ax2.add_artist(rect)
                ax2.text(x = x_posi+1400, y = y_posi2+100, s = c, fontdict={'fontsize': 190})

        fig.set_facecolor('white')
        ax2.axis('off')
        bg = plt.imread('bg.png')
        plt.imshow(bg)       
        plt.tight_layout()
        return plt.show()


    def color_to_df(input):
        colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
        df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
        df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
        
        df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                            int(i.split(", ")[1]),
                            int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
        
        df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
        return df

    df_color = color_to_df(colors_x)
    df_color
    exact_color('colorat.jpg', 400, 5, 4.5)
                try:
                    saving_frames_durations.pop(0)
                except IndexError:
                    pass
               count += 1




    input_name = "colorat.jpg"
    output_width = 900                   
    img = Image.open(input_name)
    wpercent = (output_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((output_width,hsize), Image.Resampling.LANCZOS)

    resize_name = 'resize_' + input_name  
    img.save(resize_name)                 
    img_url = resize_name
    colors_x = extcolors.extract_from_path(img_url, tolerance = 12, limit = 12)
    colors_x

    def exact_color(input_image, resize, tolerance, zoom):
        bg = 'bg.png'
        fig, ax = plt.subplots(figsize=(192,108),dpi=10)
        fig.set_facecolor('white')
        plt.savefig(bg)
        plt.close(fig)
        
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
        colors_x = extcolors.extract_from_path(img_url, tolerance = tolerance, limit = 13)
        df_color = color_to_df(colors_x)
        
        list_color = list(df_color['c_code'])
        list_precent = [int(i) for i in list(df_color['occurence'])]
        text_c = [c + ' ' + str(round(p*100/sum(list_precent),1)) +'%' for c, p in zip(list_color, list_precent)]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(160,120), dpi = 10)
        
        wedges, text = ax1.pie(list_precent,
                            labels= text_c,
                            labeldistance= 1.05,
                            colors = list_color,
                            textprops={'fontsize': 150, 'color':'black'})
        plt.setp(wedges, width=0.3)

        img = mpimg.imread(resize_name)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (0, 0))
        ax1.add_artist(ab)
        
        x_posi, y_posi, y_posi2 = 160, -170, -170
        for c in list_color:
            if list_color.index(c) <= 5:
                y_posi += 180
                rect = patches.Rectangle((x_posi, y_posi), 360, 160, facecolor = c)
                ax2.add_patch(rect)
                ax2.text(x = x_posi+400, y = y_posi+100, s = c, fontdict={'fontsize': 190})
            else:
                y_posi2 += 180
                rect = patches.Rectangle((x_posi + 1000, y_posi2), 360, 160, facecolor = c)
                ax2.add_artist(rect)
                ax2.text(x = x_posi+1400, y = y_posi2+100, s = c, fontdict={'fontsize': 190})

        fig.set_facecolor('white')
        ax2.axis('off')
        bg = plt.imread('bg.png')
        plt.imshow(bg)       
        plt.tight_layout()
        return plt.show()


    def color_to_df(input):
        colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
        df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
        df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
        
        df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                            int(i.split(", ")[1]),
                            int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
        
        df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
        return df

    df_color = color_to_df(colors_x)
    df_color
    exact_color('colorat.jpg', 400, 5, 4.5)



if __name__ == "__main__":
    import sys
    video_file = "zoo.mp4"
    main(video_file)