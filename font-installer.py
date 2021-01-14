#!/usr/bin/python
import glob, os
from shutil import copyfile
from pathlib import Path
import time

types = ["*.ttf", '*.TTF', "*.otf", "*.OTF"]
fonts_dir = '{}/.local/share/fonts/font-installer-by-moein/'.format(Path.home())

if not os.path.exists(fonts_dir):
    os.mkdir(fonts_dir)
    print('font-installer-by-moein directory is created')

os.chdir(os.getcwd())
for type in types:
    for file in glob.glob(type):
        if not os.path.exists(fonts_dir + file):
            copyfile(file, fonts_dir + file)
            print("{}: installed".format(file))
        else:
            print("{}: already exist".format(file))
print("Done")
time.sleep(2)

os.system('fc-cache -f -v')