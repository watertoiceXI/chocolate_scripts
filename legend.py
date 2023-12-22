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
from enum import Enum
import sys

import inkscape_move_files as imf

current = os.getcwd()
LEGEND_DSTDIR = os.path.join(os.path.split(current)[0], r'something_actually_relevant') #output folder
LEGEND_SRCDIR = r'default_templates\truffles'

if not os.path.exists(LEGEND_DSTDIR):
    os.mkdir(LEGEND_DSTDIR)

def legend_box(flavors, num):
    #assert(num in [1,2])
    relative2abs = {}
    relative2abs[f'base_1.svg'] = r'file:///' + os.path.join(LEGEND_DSTDIR, f'base_{num}.svg')
    if len(flavors) == 3: # bars
        shutil.copy(os.path.join(LEGEND_SRCDIR, f'Back_BarTruffle_Base_1.svg'),
                    os.path.join(LEGEND_DSTDIR, f'back_{num}.svg'))
        shutil.copy(os.path.join(LEGEND_SRCDIR, 'unit_bars.svg'),
                    os.path.join(LEGEND_DSTDIR, f'base_{num}.svg'))
    elif len(flavors) == 4: #all truffles
        shutil.copy(os.path.join(LEGEND_SRCDIR, f'Back_onlyTruffles_1.svg'),
                    os.path.join(LEGEND_DSTDIR, f'back_{num}.svg'))
        shutil.copy(os.path.join(LEGEND_SRCDIR, 'unit_onlyTruffles.svg'),
                    os.path.join(LEGEND_DSTDIR, f'base_{num}.svg'))
    elif len(flavors) == 5:
        shutil.copy(os.path.join(LEGEND_SRCDIR, f'Back_SkinnyBox.svg'),
                    os.path.join(LEGEND_DSTDIR, f'back_{num}.svg'))
        shutil.copy(os.path.join(LEGEND_SRCDIR, f'Front_SkinnyBox.svg'),
                    os.path.join(LEGEND_DSTDIR, f'front_{num}.svg'))
    else:
        raise NotImplementedError('how many truffles do you want?!')            
    for nflavor, flavor in enumerate(flavors):
        shutil.copy(os.path.join(LEGEND_SRCDIR, f'ingredient_{flavor}.svg'),
                    os.path.join(LEGEND_DSTDIR, f'ingredient_{num}_{nflavor}.svg'))
        relative2abs[f'ingredient_0_{nflavor}.svg'] = r'file:///' + os.path.join(LEGEND_DSTDIR, f'ingredient_{num}_{nflavor}.svg')
        shutil.copy(os.path.join(LEGEND_SRCDIR, f'truffle_{flavor}.svg'),
                    os.path.join(LEGEND_DSTDIR, f'truffle_{num}_{nflavor}.svg')) 
        relative2abs[f'truffle_0_{nflavor}.svg'] = r'file:///' + os.path.join(LEGEND_DSTDIR, f'truffle_{num}_{nflavor}.svg')
    imf.replace_defaults(os.path.join(LEGEND_DSTDIR, f'back_{num}.svg'),
                     os.path.join(LEGEND_DSTDIR, f'back_{num}.svg'),
                     replacedict = relative2abs) 
    if os.path.exists(os.path.join(LEGEND_DSTDIR, f'front_{num}.svg')):
        imf.replace_defaults(os.path.join(LEGEND_DSTDIR, f'front_{num}.svg'),
                     os.path.join(LEGEND_DSTDIR, f'front_{num}.svg'),
                         replacedict = relative2abs)    
    return

def bulk_legend(combos, size):
    if size == 0: #3x4 in legends, printed on 4x6 in cards
        nperprint = 2
        shutil.copy(os.path.join(LEGEND_SRCDIR, f'Back_Print.svg'),
                   os.path.join(LEGEND_DSTDIR, f'Back_Print.svg'))
        blankpath = os.path.join(LEGEND_SRCDIR, f'Blank_3x4.svg')
    elif size == 1: # 1.5x6 in skinny legends, printed on 8.5x11in
        shutil.copy(os.path.join(LEGEND_SRCDIR, f'SkinnyBox_BackPrint.svg'),
                   os.path.join(LEGEND_DSTDIR, f'Back_Print.svg'))
        shutil.copy(os.path.join(LEGEND_SRCDIR, f'SkinnyBox_FrontPrint.svg'),
                   os.path.join(LEGEND_DSTDIR, f'Front_Print.svg'))
        blankpath = os.path.join(LEGEND_SRCDIR, f'Blank_Skinny.svg')
        nperprint = 7
    else:
        raise NotImplementedError('Pick a valid legend card size or implement')
    for count, ncomb in enumerate(range(0, len(combos), nperprint)):
        for combix in range(0, nperprint):
            if len(combos) <= ncomb+combix: 
                shutil.copy(blankpath, os.path.join(LEGEND_DSTDIR, f'back_{combix+1}.svg'))
                shutil.copy(blankpath, os.path.join(LEGEND_DSTDIR, f'front_{combix+1}.svg'))
            else:
                legend_box(combos[ncomb+combix],combix+1)
            
        imf.export(os.path.join(LEGEND_DSTDIR, 'Back_Print.svg'),
                os.path.join(LEGEND_DSTDIR, f'back_print_{count}.pdf'))
        imf.export(os.path.join(LEGEND_DSTDIR, 'Front_Print.svg'),
                os.path.join(LEGEND_DSTDIR, f'front_print_{count}.pdf'))
    print('Done.')
   

class Size(Enum):
    Standard = 0 # 3x4 inches
    Skinny = 1 #1.5 x 6in

    
if __name__ == '__main__':
    # combos are a list of flavors
    # Each entry in combos in a list, either 3 or 4 or 5 long
    # If 3, assumes minibars
    """
    combos = [['orange_caramel','hazelnut_crunch','chai_tea','red_wine'],
            ['cherry', 'hazelnut_crunch', 'hazelnut_praline','espresso'],
            ['red_wine', 'orange_caramel','hazelnut_crunch','chai_tea'],
            ['hazelnut_crunch','hazelnut_praline','red_wine', 'espresso'],
            ['red_wine', 'hazelnut_crunch', 'espresso', 'orange_caramel'],
            ['orange_caramel', 'chai_tea', 'cherry', 'red_wine'],
            ['espresso', 'hazelnut_praline', 'orange_caramel'], #, 'red_wine'],
            ['red_wine', 'hazelnut_crunch','orange_caramel'], #,'chai_tea'],
            ['hazelnut_crunch','orange_caramel','cherry'], #,'chai_tea']] #,
            ['orange_caramel', 'hazelnut_crunch','red_wine']] #,'chai_tea'],
            #['orange_caramel','red_wine', 'chai_tea', 'cherry'],
            #['orange_caramel', 'hazelnut_crunch', 'red_wine', 'espresso']]
    """
    combos = [['smore', 'raspberry', 'strawberry', 'scotch_honey', "red_wine"], #brian
              ['maple_bourbon', 'smore', 'oreo', 'blueberry','strawberry'], #brian
              ['strawberry', 'raspberry', 'smore', 'scotch_honey', 'oreo'],
              ['strawberry', 'raspberry', 'smore', 'scotch_honey', 'oreo'],
              ['strawberry', 'raspberry', 'smore', 'scotch_honey', 'oreo'],
              ['strawberry', 'raspberry', 'smore', 'scotch_honey', 'oreo'],
              ['strawberry', 'raspberry', 'smore', 'scotch_honey', 'oreo']]
              
              
              #['maple_bourbon', 'raspberry', 'oreo', 'blueberry', "smore"], #shaun
              #['blueberry', 'strawberry', 'smore', 'oreo', 'raspberry'], # adam
              # ['raspberry', 'smore', 'red_wine', 'scotch_honey', "maple_bourbon"], #mike
              # ['raspberry', 'raspberry', 'raspberry', 'raspberry', "raspberry"], #bryan
               #['blueberry', 'blueberry', 'blueberry', 'blueberry', "blueberry"], #bryan
               #['smore', 'raspberry', 'strawberry', 'scotch_honey', "maple_bourbon"], #, #jay
               #['strawberry', 'blueberry', 'smore', 'oreo', 'maple_bourbon']] #jim


    #size = Size.Standard.value 
    size = Size.Skinny.value
    bulk_legend(combos, size=size)
