import os
import cv2
import time
import numpy as np
from PIL import Image
from datetime import timedelta
import collections
from PIL import Image

# def extract_colors(image_file):
#     img = Image.open(image_file)
#     img = img.convert("RGB")
#     img = list(img.getdata())
#     colors = collections.defaultdict(int)
#     for color in img:
#         colors[color] += 1
#     return colors

# def apply_tolerance(rgb_list, tl):
#     rgb_list = list(rgb_list)
#     rgb_list.sort(key=lambda x: x[1], reverse=True)
#     duplicates = set()
#     for idx, (codes, occurrence) in enumerate(rgb_list):
#         for idx2 in range(idx + 1, len(rgb_list)):
#             code = rgb_list[idx2][0]
#             occ = rgb_list[idx2][1]
#             r = abs(codes[0]-code[0])
#             g = abs(codes[1]-code[1])
#             b = abs(codes[2]-code[2])
#             if r <= tl and g <= tl and b <= tl:
#                 occurrence += occ
#                 rgb_list[idx] = (codes, occurrence)
#                 duplicates.add(code)

#     rgb = []
#     for codes, occurrence in rgb_list:
#         if codes not in duplicates:
#             rgb.append((codes, occurrence))

#     return(rgb)  

def get_files(directory):
    files = os.listdir(directory)
    full_paths = []
    for file in files:
        full_paths.append(os.path.join(directory, file))
    return full_paths

def colors_are_similar(col1, col2, tl):
    r = abs(col1[0]-col2[0])
    g = abs(col1[1]-col2[1])
    b = abs(col1[2]-col2[2])
    return r <= tl and g <= tl and b <= tl

def apply_tolerance_frame(frame, tl):
    # rgb_code = hex_2_rgb(hex_code)
    img = Image.open(frame)
    img = img.convert("RGB")

    data_rgb = list(img.getdata())
    new_image = [] 

    for idx,(codes) in enumerate(data_rgb):
        for idx2 in range(idx + 1, len(data_rgb)):
            code = data_rgb[idx2]
            r = abs(codes[0]-code[0])
            g = abs(codes[1]-code[1])
            b = abs(codes[2]-code[2])
            if r <= tl and g <= tl and b <= tl:
                new_image.append(code)
            else:
                new_image.append(codes)
                
    img.putdata(new_image)    
    img.save("new_img.png")

if __name__ == "__main__":
    frame = "frame0-05-00.01.png"
  
    tl = 10 
    apply_tolerance_frame(frame, tl)