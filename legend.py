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

import inkscape_move_files as imf

INKSCAPE_DIR = r'C:\Program Files\Inkscape\bin'
LEGEND_DSTDIR = r'C:\Users\kroma\Documents\Differential\Boxes\testPrint'
LEGEND_SRCDIR = r'default_templates\truffles'


def legend_box(flavors, num):
    assert(num in [1,2])
    relative2abs = {}
    if len(flavors) == 3: # bars
        shutil.copy(os.path.join(LEGEND_SRCDIR, f'Back_BarTruffle_Base_{num}.svg'),
                    os.path.join(LEGEND_DSTDIR, f'back_{num}.svg'))
        shutil.copy(os.path.join(LEGEND_SRCDIR, 'unit_bars.svg'),
                    os.path.join(LEGEND_DSTDIR, f'base_{num}.svg'))
        relative2abs[f'base_{num}.svg'] = r'file:///' + os.path.join(LEGEND_DSTDIR, f'base_{num}.svg')
        for nflavor, flavor in enumerate(flavors):
            shutil.copy(os.path.join(LEGEND_SRCDIR, f'ingredient_{flavor}.svg'),
                        os.path.join(LEGEND_DSTDIR, f'ingredient_{num}_{nflavor}.svg'))
            relative2abs[f'ingredient_{num}_{nflavor}.svg'] = r'file:///' + os.path.join(LEGEND_DSTDIR, f'ingredient_{num}_{nflavor}.svg')
            shutil.copy(os.path.join(LEGEND_SRCDIR, f'truffle_{flavor}.svg'),
                        os.path.join(LEGEND_DSTDIR, f'truffle_{num}_{nflavor}.svg')) 
            relative2abs[f'truffle_{num}_{nflavor}.svg'] = r'file:///' + os.path.join(LEGEND_DSTDIR, f'truffle_{num}_{nflavor}.svg')
    elif len(flavors) == 4: #all truffles
        shutil.copy(os.path.join(LEGEND_SRCDIR, f'Back_onlyTruffles_{num}.svg'),
                    os.path.join(LEGEND_DSTDIR, f'back_{num}.svg'))
        shutil.copy(os.path.join(LEGEND_SRCDIR, 'unit_onlyTruffles.svg'),
                    os.path.join(LEGEND_DSTDIR, f'base_{num}.svg'))
        relative2abs[f'base_{num}.svg'] = r'file:///' + os.path.join(LEGEND_DSTDIR, f'base_{num}.svg')
        for nflavor, flavor in enumerate(flavors):
            shutil.copy(os.path.join(LEGEND_SRCDIR, f'ingredient_{flavor}.svg'),
                        os.path.join(LEGEND_DSTDIR, f'ingredient_{num}_{nflavor}.svg'))
            relative2abs[f'ingredient_{num}_{nflavor}.svg'] = r'file:///' + os.path.join(LEGEND_DSTDIR, f'ingredient_{num}_{nflavor}.svg')
            shutil.copy(os.path.join(LEGEND_SRCDIR, f'truffle_{flavor}.svg'),
                        os.path.join(LEGEND_DSTDIR, f'truffle_{num}_{nflavor}.svg'))    
            relative2abs[f'truffle_{num}_{nflavor}.svg'] = r'file:///' + os.path.join(LEGEND_DSTDIR, f'truffle_{num}_{nflavor}.svg')
    else:
        raise NotImplementedError('how many truffles do you want?!')
    imf.replace_defaults(os.path.join(LEGEND_DSTDIR, f'back_{num}.svg'),
                     os.path.join(LEGEND_DSTDIR, f'back_{num}.svg'),
                     replacedict = relative2abs)    
    return

def bulk_legend(combos):    
    for count, ncomb in enumerate(range(0, len(combos), 2)):
        legend_box(combos[ncomb],1)
        legend_box(combos[ncomb+1],2)
        imf.export(os.path.join(LEGEND_DSTDIR, 'Back_Print.svg'),
                os.path.join(LEGEND_DSTDIR, f'back_print_{count}.pdf'))
    print('Done.')
    
if __name__ == '__main__':
    import time
    # combos are a list of flavors
    # Each entry in combos in a list, either 3 or 4 long
    # If 3, assumes minibars
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
    shutil.copy(os.path.join(LEGEND_SRCDIR, f'Back_Print.svg'),
               os.path.join(LEGEND_DSTDIR, f'Back_Print.svg'))
    bulk_legend(combos)
