# from PIL import Image
# import os
# img = "flower.jpg" 
# img_dir, _ = os.path.splitext(img)
# img_dir += "_image_changed" 
# img = Image.open("flower.jpg")
# img = img.convert("RGB")
 
# d = img.getdata()
 
# new_image = []
# for item in d:
   
#     # change all white (also shades of whites)
#     # pixels to yellow
#     if item[0] in list(range(200, 256)):
#         new_image.append((255, 224, 100))
#     else:
#         new_image.append(item)
# img.putdata(new_image)        
# # update image data

# img.save(img_dir + ".jpg")


 
# # save new image

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
ffmpeg_extract_subclip("video1.mp4", start_time, end_time, targetname="test.mp4")