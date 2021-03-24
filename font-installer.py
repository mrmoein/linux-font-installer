#!/usr/bin/python
import os, sys
from shutil import copyfile
from pathlib import Path
from bcolors import bcolors

# all fonts type
types = [".ttf", '.TTF', ".otf", ".OTF"]
all_fonts_dir_path = '{}/.local/share/fonts/font-installer-by-moein/'.format(Path.home())

# create fonts directory if not exist
if not os.path.exists(all_fonts_dir_path):
    Path(all_fonts_dir_path).mkdir(parents=True, exist_ok=True)


# print colored text
def print_c(text, style, newLine=False):
    if newLine:
        print(style + text + bcolors.ENDC, end='')
    else:
        print(style + text + bcolors.ENDC)

# find font directory
if len(sys.argv) > 1:
    currnet_path = sys.argv[1]
else:
    currnet_path = '.'


# copy all font to all_fonts_dir_path
for font_type in types:
    for dirpath, dirnames, filenames in os.walk(currnet_path):
        for filename in [f for f in filenames if f.endswith(font_type)]:
            font_path = dirpath + '/' + filename
            if not os.path.exists(all_fonts_dir_path + '/' + filename):
                copyfile(font_path, all_fonts_dir_path + "/" + filename)
                print_c("{}: installed".format(font_path), bcolors.OKGREEN)
            else:
                print_c("{}: already exist".format(font_path), bcolors.WARNING)

print_c("============== Done! ==============", bcolors.HEADER)

# create font cache
os.system('fc-cache -f -v')
