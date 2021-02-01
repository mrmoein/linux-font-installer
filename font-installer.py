#!/usr/bin/python
import os
from shutil import copyfile
from pathlib import Path
from bcolors import bcolors

types = [".ttf", '.TTF', ".otf", ".OTF"]
all_fonts_dirpath = '{}/.local/share/fonts/font-installer-by-moein/'.format(Path.home())


def printC(text, style, newLine=False):
    if newLine:
        print(style + text + bcolors.ENDC, end='')
    else:
        print(style + text + bcolors.ENDC)


for font_type in types:
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames if f.endswith(font_type)]:
            # print(os.path.join(dirpath, filename))
            font_path = dirpath + '/' + filename
            if not os.path.exists(all_fonts_dirpath + '/' + filename):
                copyfile(font_path,  all_fonts_dirpath + "/" + filename)
                printC("{}: installed".format(font_path), bcolors.OKGREEN)
            else:
                printC("{}: already exist".format(font_path), bcolors.WARNING)

printC("============== Done! ==============", bcolors.HEADER)

os.system('fc-cache -f -v')