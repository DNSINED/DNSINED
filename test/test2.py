# from PIL import Image
# import os
# def hex_2_rgb(value):
#     value = value.lstrip("#")
#     lv = len(value)
#     return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# def change_color(frame, hex_code):
#     name = hex_code
#     rgb_code = hex_2_rgb(hex_code)
#     img = Image.open(frame)
#     img = img.convert("RGB")

#     data_rgb = list(img.getdata())
#     new_image = []

#     for item in data_rgb:
#         if item == rgb_code:
#             new_image.append((255, 0, 0))
#         else:
#             new_image.append(item)   
#     img.putdata(new_image)
   
#     img.save(name + ".png")

# if __name__ == "__main__":
#     frame = "frame0-05-00.01.png"
#     hex_code = ("#ffc2ff","#9e4b35","#caf9ff","#fff5df","#00bee6","#ffe10a","#ffffff","#73ffdb","#ffff9c")

#     for x in hex_code:
#         change_color(frame, x)







# rgb_list = [((0, 0, 0), 1), ((1, 1, 1), 1), ((2, 2, 2), 1)]
# 
# rgb_list = [((0, 0, 0), 1), ((1, 11, 1), 1), ((2, 2, 2), 1)]
# rgb_list = [((0, 0, 0), 1), ((1, 1, 1), 1), ((2, 2, 2), 1)]

# rgb_list.sort(key=lambda x: x[1], reverse=True)
# aux_list = list(rgb_list)
# count = 0
# duplicates = []
# for codes, occurrence in rgb_list:
#     aux_list.pop(0)
#     for code, occ in aux_list:
#         r = abs(codes[0]-code[0])
#         g = abs(codes[1]-code[1])
#         b = abs(codes[2]-code[2])
#         if r <= tl and g <= tl and b <= tl:
#             occurrence += occ
#             rgb_list[count] = (codes, occurrence)
#             duplicates.append(code)

#     count += 1
# rgb = []
# for codes,occurrence in rgb_list:
#     if codes not in duplicates:
#         rgb.append((codes, occurrence))

# print(rgb)


rgb_list = [((0, 0, 0), 1), ((1, 1, 1), 2), ((2, 2, 2), 3)]
tl = 1
# rgb_list.sort(key=lambda x: x[1], reverse=True)
# duplicates = set()
# for idx, (codes, occurrence) in enumerate(rgb_list):
#     for idx2 in range(idx + 1, len(rgb_list)):
#         code = rgb_list[idx2][0]
#         occ = rgb_list[idx2][1] 
#         r = abs(codes[0]-code[0])
#         g = abs(codes[1]-code[1])
#         b = abs(codes[2]-code[2])
#         if r <= tl and g <= tl and b <= tl:
#             occurrence += occ
#             rgb_list[idx] = (codes, occurrence)
#             duplicates.add(code)

# rgb = []
# for codes, occurrence in rgb_list:
#     if codes not in duplicates:
#         rgb.append((codes, occurrence))

# print(rgb)
def colors_are_similar(col1, col2, tl):
    r = abs(col1[0]-col2[0])
    g = abs(col1[1]-col2[1])
    b = abs(col1[2]-col2[2])
    return r <= tl and g <= tl and b <= tl


colors = [((0, 0, 0), 1), ((1, 1, 1), 2), ((2, 2, 2), 3)]
tl = 1
colors.sort(key=lambda x: x[1], reverse=True)
compressed_colors = []
while colors:
    most_common_color = colors[0][0]
    similar_colors = [x for x in colors if colors_are_similar(
        x[0], most_common_color, tl)]
    sum_of_occurrences = sum(x[1] for x in similar_colors)
    compressed_colors.append((most_common_color, sum_of_occurrences))
    colors = [x for x in colors if x not in similar_colors]

print(compressed_colors)






colors = [((0, 0, 0), 1), ((1, 1, 1), 2), ((2, 2, 2), 3)]