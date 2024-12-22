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

from matplotlib import font_manager
from matplotlib import rcParams

INKSCAPE_DIR = r'C:\Program Files\Inkscape\bin'

font_paths = font_manager.findSystemFonts(fontpaths=None, fontext="ttf")
GOTHAM_FONTPATH = [x for x in font_paths if 'GothamBook' in x]
if not len(GOTHAM_FONTPATH):
    raise FileNotFoundError('Could not find Gotham Book font.')
GOTHAM_FONTPATH = GOTHAM_FONTPATH[0]
font_manager.fontManager.addfont(GOTHAM_FONTPATH)
rcParams['font.family']='Gotham'

import matplotlib.pyplot as plt
import differential.plot_choco as pc

'''
In addition to changing paths below, ensure 
    FOR LEGEND CARDS: Back_*.svg and 'base_*.svg' have absolute filepaths
    FOR WRAPPERS: Wrapper_Print4.svg
To change absolute filepaths, in inkscape select reference and right click > image properties.
In the URL field, change path. Note, expects: file:///{PATH}
Note: Inkscape kept dying, found creating absolute path, then prepending file:/// worked
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
        
def replace_paths(new_absfolder, filename):
    with open(filename, 'r') as fin:
        base = fin.read()
    seek = 0
    paths = []
    while seek >= 0:
        start = base.find('file:///', seek)
        end = base.find('.png', start)
        if not ((start >=0) and (end >= 0)):
            break
        paths.append( base[start:end]) 
        seek = end
    for old_path in paths:
        if r'%5C' in old_path:
            basename = os.path.splitext(old_path.split(r'%5C')[-1])[0]
        else:
            basename = os.path.splitext(os.path.basename(old_path))[0]
        base = base.replace(old_path, "file:///"+os.path.join(new_absfolder, basename))
    with open(filename, 'w') as fout:
        fout.write(base)          
