"""
Working example, demonstrating how Python can be used for converting a folder of JPG files to a folder of PNG files.

Use it with command line arguments, such as "python jpg_to_png images png", where:
- "images" is the name of the source folder that contains the JPG images
- "png" is the name of the output folder that is going to contain the PNG images
"""

import os
import sys
from PIL import Image

source_folder = sys.argv[1]
output_folder = sys.argv[2]

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

files = [file for file in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, file))]
for file in files:
    filename, file_extension = os.path.splitext(file)
    if file_extension == ".jpg":
        source_file = f"{os.path.join(source_folder, file)}"
        output_file = f"{os.path.join(output_folder, filename)}.png"
        Image.open(source_file).save(output_file, "png")
