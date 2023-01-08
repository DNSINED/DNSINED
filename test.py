import os
import cv2
import time
from pyciede2000 import ciede2000
from colorir import *
import numpy as np
from PIL import Image
from datetime import timedelta
import collections
from PIL import Image
import shutil
import math
import colorsys


SAVING_FRAMES_PER_SECOND = 1


def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def get_saved_frames_durations(cap, saving_fps):
    s = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / \
        cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(300, clip_duration-300, 1 / saving_fps):
        s.append(i)
    return s       


def format_timedelta(td):
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


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


def get_files(directory):
    directory = os.path.abspath(directory)
    files = os.listdir(directory)
    full_paths = []
    for file in files:
        full_paths.append(os.path.join(directory, file))
    return full_paths


def extract_colors(image_file):
    img = Image.open(image_file)
    img = img.convert("RGB")
    img = list(img.getdata())
    colors = collections.defaultdict(int)
    for color in img:
        colors[color] += 1
    return colors


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


def rgb_2_lab(value_rgb):
    value_xyz = rgb_2_xyz(value_rgb)
    var_X = value_xyz[0] / 95.044
    var_Y = value_xyz[1] / 100.000
    var_Z = value_xyz[2] / 108.755
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

    return(CIE_L, CIE_a, CIE_b)


def rgb_2_lab(list_rgb):
    value_xyz = rgb_2_xyz(list_rgb)
    var_X = value_xyz[0] / 95.044
    var_Y = value_xyz[1] / 100.000
    var_Z = value_xyz[2] / 108.755
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

    return(CIE_L, CIE_a, CIE_b)


def Delta_E94_array(L1, a1, b1, L2_list, a2_list, b2_list): 
    L2_array = np.array(L2_list)
    a2_array = np.array(a2_list)
    b2_array = np.array(b2_list)

    C1 = math.sqrt(a1**2 + b1**2)

    C2 = np.sqrt(a2_array**2 + b2_array**2)

    delta_Eab = np.sqrt(((L2_array-L1)**2) + ((a2_array-a1)**2) + ((b2_array-b1)**2))
    delta_L = L1 - L2_array
    delta_Cab = C1 - C2
    delta_Hab = (delta_Eab**2) - (delta_L**2) - (delta_Cab**2)
    delta_Hab = delta_Hab.clip(min=0)
    delta_Hab = np.sqrt(delta_Hab) 

    K1 = 0.045
    K2 = 0.015

    SC = 1 + (K1*C1)
    SH = 1 + (K2*C1)

    delta_E94 = np.sqrt((delta_L**2) + ((delta_Cab/SC)**2) + ((delta_Hab/SH)**2))

    return(delta_E94)


def apply_tolerance_color(rgb_list, tl):
    rgb_list = list(rgb_list)
    rgb_list.sort(key=lambda x: x[1], reverse=True)   
    occ_list = np.empty(len(rgb_list))

    lab_list = []
    L_list = []
    a_list = []
    b_list = []

    for idx, (codes,occ) in enumerate(rgb_list):
        L, a, b = rgb_2_lab(codes)
        L_list.append(L)
        a_list.append(a)
        b_list.append(b)
        value_cielab = (L, a, b)
        lab_list.append((value_cielab, occ))
        occ_list[idx] = occ 
    
    duplicates = np.full(len(lab_list), False)

    for idx, (L, a, b, occurrence) in enumerate(zip(L_list, a_list, b_list, occ_list)):
        if not duplicates[idx]:
            deltas = np.full(len(lab_list[idx + 1:]), 0)
            deltas = Delta_E94_array(L, a, b, L_list[idx + 1:], a_list[idx + 1:], b_list[idx + 1:])

            similar = deltas < tl

            view = duplicates[idx + 1:]
            combined = similar | view
            np.copyto(view, combined)

            view_occ = occ_list[idx + 1:]
            exclude = np.logical_not(similar)
            relevant_occ = np.ma.MaskedArray(view_occ, exclude)
            extra_occ = relevant_occ.sum()
            lab_list[idx] = (codes, occurrence + extra_occ)
    
    rgb = []
    for idx, (codes, occurrence) in enumerate(lab_list):
        if not duplicates[idx]:
            rgb.append((rgb_list[idx][0], occurrence))
    
    return (rgb)


def Delta_E94(col1, col2):

    L1 = col1[0]
    a1 = col1[1]
    b1 = col1[2]

    L2 = col2[0]
    a2 = col2[1]
    b2 = col2[2]
  
    C1 = math.sqrt(a1**2 + b1**2)
    C2 = math.sqrt(a2**2 + b2**2)

    delta_Eab = math.sqrt(((L2-L1)**2) + ((a2-a1)**2) + ((b2-b1)**2))
    delta_L = L1 - L2
    delta_Cab = C1 - C2
    delta_Hab = (delta_Eab**2) - (delta_L**2) - (delta_Cab**2)
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
    SC = 1 + (K1*C1)
    SH = 1 + (K2*C1)

    delta_E94 = math.sqrt(((delta_L/(kL*SL))**2) + ((delta_Cab/(kC*SC))**2) +
        ((delta_Hab/(kH*SH))**2))

    return(delta_E94)


def colors_are_similar(col1, col2, tl):
    diff = Delta_E94(col1, col2)
    return (diff <= tl)


def apply_tolerance_frame(frame, result_frame, code_rgb, tl):
    img = cv2.imread(frame)

    print(len(img))
    print(len(img[0]))
    print(img[0][0])


    # L, a, b = rgb_2_lab(code_rgb[0])
    for h in range(0, len(img)):
        # L1 = img[:len(img[0][0])]
        # deltas = Delta_E94_array(L, a, b, img[:len(img[0])][0], img[:len(img[0])][1], img[:len(img[0])][2])

        for w in range(0, len(img[0])):
            L, a, b = rgb_2_lab(img[h][w])
            # if colors_are_similar(Lab1, Lab2, tl):
            img[h][w][0] = L
            img[h][w][1] = a
            img[h][w][2] = b

    cv2.imwrite(result_frame, img)
    duplicates = np.full(len(img), False) 
    # img = Image.open(frame)
    # img = img.convert("RGB")

    # data_rgb = list(img.getdata())
    # new_image = []
    # Lab2 = rgb_2_lab(code_rgb[0])
    # for code in data_rgb:
    #     Lab1 = rgb_2_lab(code)
    #     if colors_are_similar(Lab1, Lab2, tl):
    #         new_image.append((255, 0, 0))
    #     else:
    #         new_image.append(code)
    # img.putdata(new_image)
    # img.save(result_frame)


def rgb_code(frame, color_list, tl):
    frame_changed= f'{frame.removesuffix(".png")}'
    for idx, (col) in enumerate(color_list):
        apply_tolerance_frame(frame,  f'{frame_changed}-{idx}.png', col, tl)


def frames(parent_dir, frame_list, color_list, tl):
    make_dir(parent_dir)
    for frame in frame_list:
        filename = os.path.basename(frame)
        frame_dir = f'{parent_dir}/{filename.removesuffix(".png")}'
        make_dir(frame_dir)
        new_frame = f'{frame_dir}/{filename}'
        shutil.copy(frame, new_frame)

        rgb_code(new_frame, color_list, tl)


def save_palette_as_image(colors, file, square_size):
    w, h = square_size, square_size
    img = Image.new(mode = "RGB", size = (w,h))
    pixels = img.load()
    x, y = 0, 0
    for col,hue in colors:
        pixels[x,y] = col
        x += 1
        if x == w:
            y += 1
            x = 0
    img = img.resize((100*w,100*h), Image.NEAREST)
    # img.show()
    img.save(file)


def rgb_to_hex(r, g, b):
  hex_code = '%02X%02X%02X' % (r, g, b)
  return(hex_code)


def save_palette_as_text(colors, file):
    with open (file,'w') as f:
        for col,hue in colors:
            hex_code = rgb_to_hex(col[0], col[1], col[2])
            f.write("%s\n" % hex_code)


def get_palette_name(tl_type, tl, min_occ, len):
    palette_name = f'palette-{tl_type}-{tl}-{min_occ}-{len}'
    return(palette_name)


def sort_colors(colors):
    colors.sort(key=lambda a: a[1])
    return(colors)


def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v


def extract_palette(min_occ, list): 
    rgb_palette = []
    for col,occ in list:
        if occ>=min_occ:
            h, s, v = rgb_to_hsv(col[0], col[1], col[2])
            rgb_palette.append((col, h))

    return(rgb_palette)


def create_palette(tolerance_type, tolerance, minimum_occurrences, color_list, dir):
	colors = extract_palette(minimum_occurrences, color_list)
	
	colors = sort_colors(colors)
	
	palette_name = get_palette_name(tolerance_type, tolerance, minimum_occurrences, len(colors))
	
	save_palette_as_text(colors, f'{dir}/{palette_name}.txt')

	square_size = math.ceil(math.sqrt(len(colors)))

	if len(colors) < 1000:
		save_palette_as_image(colors, f'{dir}/{palette_name}.png', square_size)


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


if __name__ == "__main__":
    st = time.time()
    new_frames_dir = os.getcwd() + "\\frames_with_tolerance"
    make_dir(new_frames_dir)
    palette_dir = os.getcwd() + "\\palette"
    make_dir(palette_dir)
    video_file = "adventure_time.mkv"
    frames_dir, _ = os.path.splitext(video_file)
    frames_dir += "_frames"

    tolerance = 2
    tl_type = "rgb"
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

    rgb_list = []

    for col,occ in all_colors:
        if occ >= 10:
            rgb_list.append((col,occ))

    rgb_list.sort(key=lambda x: x[1], reverse=True)

    new_rgb_list = apply_tolerance_color(rgb_list.copy(), tolerance)
    new_rgb_list.sort(key=lambda x: x[1], reverse=True)

    with open('colors.csv', 'w') as f:
        for rgb in rgb_list:
            f.write("%s,%s\n" % (rgb[0], rgb[1]))

    os.chdir(new_frames_dir)
    color_list = new_rgb_list
    # frames(new_frames_dir, files, color_list, tolerance)

    # test
    # test = color_list[:1]
    # frames(new_frames_dir, files, test, tolerance)


    min_occ = 7000
    create_palette(tl_type, tolerance, min_occ, rgb_list, palette_dir)
    
    # optional feature:
    # frame = ""
    # hex_code = ()
    # change_color(frame, hex_code)

    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
