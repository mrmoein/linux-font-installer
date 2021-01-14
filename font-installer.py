#!/usr/bin/python
import os
from shutil import copyfile
from pathlib import Path

types = [".ttf", '.TTF', ".otf", ".OTF"]
all_fonts_dirpath = '{}/.local/share/fonts/font-installer-by-moein/'.format(Path.home())

for font_type in types:
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames if f.endswith(font_type)]:
            # print(os.path.join(dirpath, filename))
            font_path = dirpath + '/' + filename
            if not os.path.exists(all_fonts_dirpath + '/' + filename):
                copyfile(font_path,  all_fonts_dirpath + "/" + filename)
                print("{}: installed".format(font_path))
            else:
                print("{}: already exist".format(font_path))

print("Done!")

os.system('fc-cache -f -v')