import os
import cv2
import time
import numpy as np
from PIL import Image
from datetime import timedelta
import collections
from PIL import Image
import shutil
import math


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
    for i in np.arange(300, clip_duration-300, 1 / saving_fps):
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
    directory = os.path.abspath(directory)
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
            if colors_are_similar(codes, code, tl):
                occurrence += occ
                rgb_list[idx] = (codes, occurrence)
                duplicates.add(code)

    rgb = []
    for codes, occurrence in rgb_list:
        if codes not in duplicates:
            rgb.append((codes, occurrence))

    return (rgb)


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


def rgb_2_xyz(value_rgb):
    R = value_rgb[0]
    G = value_rgb[1]
    B = value_rgb[2]
    var_R = ( R / 255 )
    var_G = ( G / 255 )
    var_B = ( B / 255 )

    if ( var_R > 0.04045 ):
        var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
    else:
        var_R = var_R / 12.92
    if ( var_G > 0.04045 ):
        var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
    else:                  
        var_G = var_G / 12.92
    if ( var_B > 0.04045 ):
        var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
    else:                   
        var_B = var_B / 12.92

    var_R = var_R * 100
    var_G = var_G * 100
    var_B = var_B * 100

    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.950
    
    value_xyz = [X, Y, Z]
    return(value_xyz)


def rgb_2_cielab(value_rgb):
    value_xyz = rgb_2_xyz(value_rgb)
    var_X = value_xyz[0]
    var_Y = value_xyz[1]
    var_Z = value_xyz[2]
    if ( var_X > 0.008856 ):
        var_X = var_X ** ( 1/3 )
    else:                   
        var_X = ( 7.787 * var_X ) + ( 16 / 116 )
    if ( var_Y > 0.008856 ):
        var_Y = var_Y ** ( 1/3 )
    else:                   
        var_Y = ( 7.787 * var_Y ) + ( 16 / 116 )
    if ( var_Z > 0.008856 ):
        var_Z = var_Z ** ( 1/3 )
    else:                    
        var_Z = ( 7.787 * var_Z ) + ( 16 / 116 )

    CIE_L = ( 116 * var_Y ) - 16
    CIE_a = 500 * ( var_X - var_Y )
    CIE_b = 200 * ( var_Y - var_Z )

    value_cielab = [CIE_L, CIE_a, CIE_b]
    return(value_cielab)


def Delta_E94(col1, col2):
    L1 = col1[0]
    a1 = col1[1]
    b1 = col1[2]

    L2 = col2[0]
    a2 = col2[1]
    b2 = col2[2]
  
    C1 = math.sqrt(a1**2 + b1**2)
    C2 = math.sqrt(a2**2 + b2**2)

    delta_Eab = math.sqrt((L2-L1)**2 + (a2-a1)**2 + (b2-b1)**2)
    delta_L = L1 - L2
    delta_Cab = C1 - C2
    delta_Hab = delta_Eab**2 - delta_L**2 - delta_Cab**2
    if delta_Hab > 0:
        delta_Hab = math.sqrt(delta_Hab)
    else:
        delta_Hab = 0

    kL = 1
    kC = 1
    kH = 1
    K1 = 0.045
    K2 = 0.015

    SL = 1
    SC = 1 + K1*C1
    SH = 1 + K2*C1

    delta_E94 = math.sqrt((delta_L/(kL*SL))**2 + (delta_Cab/(kC*SC))**2 +
        (delta_Hab/kH*SH)**2)

    return(delta_E94)


def colors_are_similar(col1, col2, tl):
    col1 = rgb_2_cielab(col1)
    col2 = rgb_2_cielab(col2)
    diff = Delta_E94(col1, col2)
    return diff <= tl


def apply_tolerance_frame(frame, result_frame, code_rgb, tl):
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
    img.save(result_frame)


def rgb_code(frame, color_list, tl):
    frame_changed= f'{frame.removesuffix(".png")}'
    for idx, (col) in enumerate(color_list):
        apply_tolerance_frame(frame,  f'{frame_changed}-{idx}.png', col, tl)


def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def frames(parent_dir, frame_list, color_list, tl):
    make_dir(parent_dir)
    for frame in frame_list:
        # copy the frame to the new dir
        filename = os.path.basename(frame)
        frame_dir = f'{parent_dir}/{filename.removesuffix(".png")}'
        make_dir(frame_dir)
        new_frame = f'{frame_dir}/{filename}'
        shutil.copy(frame, new_frame)

        rgb_code(new_frame, color_list, tl)


if __name__ == "__main__":
    st = time.time()
    new_frames_dir = os.getcwd() + "\\frames_with_tolerance"
    make_dir(new_frames_dir)
    video_file = "adventure_time.mkv"
    frames_dir, _ = os.path.splitext(video_file)
    frames_dir += "_frames"
    tolerance = 45
    # frame_extractor(video_file, frames_dir)

    files = get_files(frames_dir)
    files = files[0:1]  # for debugging purposes

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

    os.chdir(new_frames_dir)
    color_list = all_colors[:10]
    frames(new_frames_dir, files, color_list, tolerance)

    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
