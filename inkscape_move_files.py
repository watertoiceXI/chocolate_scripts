'''
12/26/2022 @kroman
'''
import os
import glob
import shutil
import subprocess
import time
import datetime
import numpy as np
import cv2
import pickle
import imageio

INKSCAPE_DIR = r'C:\Program Files\Inkscape\bin'
current = os.getcwd()
if 'krom' in current:
    GOTHAM_FONTPATH = r'C:\Users\kroma\Downloads\Gotham-Font\GothamMedium.ttf'
else:
    GOTHAM_FONTPATH = r'C:\Users\water\Downloads\Gotham-Font\Gotham-Font\GothamBook.ttf'
from matplotlib import font_manager
font_manager.findSystemFonts(fontpaths=None, fontext="ttf")
from matplotlib import rcParams
font_manager.fontManager.addfont(GOTHAM_FONTPATH)
rcParams['font.family']='Gotham'
import matplotlib.pyplot as plt

import plot_choco as pc

'''
In addition to changing paths below, ensure 
    FOR LEGEND CARDS: Back_*.svg and 'base_*.svg' have absolute filepaths
    FOR WRAPPERS: Wrapper_Print4.svg
To change absolute filepaths, in inkscape select reference and right click > image properties.
In the URL field, change path. Note, expects: file:///{PATH}
Note: Inkscape kept dying, found creating absolute path, then prepending file:\\\ worked
rather than starting by typing "file:///" @kroman
'''

def export(srcfile, dstfile):
    cwd = os.getcwd()
    os.chdir(INKSCAPE_DIR)
    out = subprocess.run(['inkscape' , srcfile,'--export-filename', dstfile], capture_output=True)
    print(out)
    os.chdir(cwd)
    
def replace_defaults(default_file, export_file, replacedict, nreplace=2):
    with open(default_file, 'r') as fin:
        base = fin.read()
    for k,v in replacedict.items():
        #print(k, v)
        base = base.replace(k, v, nreplace)
    with open(export_file, 'w') as fout:
        fout.write(base)
    #print('Done.')
        

