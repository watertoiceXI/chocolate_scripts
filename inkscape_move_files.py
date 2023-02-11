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

WRAPPER_SRCDIR = r'default_templates\bars'
WRAPPER_DSTDIR = os.path.join(os.path.split(current)[0], 'Wrappers')
if not os.path.exists(WRAPPER_DSTDIR):
    os.mkdir(WRAPPER_DSTDIR)



def export(srcfile, dstfile):
    cwd = os.getcwd()
    os.chdir(INKSCAPE_DIR)
    out = subprocess.run(['inkscape' , srcfile,'--export-filename', dstfile], capture_output=True)
    print(out)
    os.chdir(cwd)
    
def wrapper_bar():
    wrappers = [['blueberry', 'nibs', 'bolivian', 'vietnamese'],
                ['cherry', 'cherry', 'cherry', 'cherry']]
    wrapper_folders = sorted(glob.glob(os.path.join(WRAPPER_DIR, '*')))
    wrapper_folders = [x for x in wrapper_folders if os.path.isdir(x)]
    for count, wrapper_set in enumerate(wrappers):
        assert(len(wrapper_set) == 4)
        for nw, wrapper in enumerate(wrapper_set):
            matches = [x for x in wrapper_folders if wrapper in os.path.split(x)[-1].lower()]
            if len(matches) == 0:
                raise ValueError(f'could not find folder for wrapper {wrapper}')
            match = matches[0]
            wfile = sorted(glob.glob(os.path.join(match, '*.svg')))
            wfile = [x for x in wfile if 'insert' not in x][0]
            shutil.copy(wfile, os.path.join(WRAPPER_DIR, f'Wrapper_{nw}.svg'))
        export(os.path.join(WRAPPER_DIR, 'Wrapper_Print4.svg'),
               os.path.join(WRAPPER_DIR, f'Wrapper_print4_{count}.pdf'))
        print(f'Saved wrapper_print4_{count}.pdf')
    print('Done.')
                    

def replace_defaults(default_file, export_file, replacedict):
    with open(default_file, 'r') as fin:
        base = fin.read()
    for k,v in replacedict.items():
        #print(k, v)
        base = base.replace(k, v, 2)
    with open(export_file, 'w') as fout:
        fout.write(base)
    #print('Done.')
    
def create_wrapper(name, darkper, tasting_notes, lat, lon, city, country, flavor_data, specf):
    wrapper_folder = os.path.join(WRAPPER_DSTDIR, name)
    if os.path.exists(wrapper_folder):
        pass #raise NameError(f'{wrapper_folder} already exists! :-o')
    else:
        os.mkdir(wrapper_folder)
    
    spec = None
    if specf is not None:
        wavelengths = np.linspace(400, 750, 1000)
        spec = np.load(specf,allow_pickle=True)
        spectrum = np.zeros([2,1000])
        
        #spectrum
        spec_file = os.path.join(wrapper_folder, f'{name}_spec.png')
        fig, axs = plt.subplots(1, 1, figsize=(8*2, 4*2), tight_layout=True)
        minlamb=300
        maxlamb = -100
        pc.plot_spec(0.05+spec[1][minlamb:maxlamb][::-1],spec[0][minlamb:maxlamb][::-1],fig=fig)
        plt.plot(spec[0][minlamb:maxlamb][::-1],np.zeros_like(spec[1][minlamb:maxlamb]),'k--',lw=10,label='Commercial Chocolate')
        plt.legend(fontsize=44,loc=3)
        plt.savefig(spec_file,dpi=600)
    
    #star
    if flavor_data is not None:
        pc.pokey_star(flavor_data)
        plt.draw()
        stellar_file = os.path.join(wrapper_folder, f'{name}_star.png')
        plt.savefig(stellar_file,dpi=600)
        tmp = imageio.imread(stellar_file)
        tmp[:,:,3] = 255-tmp[:,:,0] #modify alpha channel
        imageio.imwrite(stellar_file, tmp)

    #map
    map_file = os.path.join(wrapper_folder, f'{name}_map.png')
    pc.mapthingy(lon, lat)
    plt.savefig(map_file,dpi=600)
    tmp = imageio.imread(map_file)
    tmp[:,:,3] = 255-tmp[:,:,0] #modify alpha channel
    imageio.imwrite(map_file, tmp)
    
    # do wrapper stuff
    now = datetime.datetime.now()
    map_file = r'file:///' + map_file #.replace(r"\", r'%5C', 20) 
    stellar_file = "file:///" + stellar_file #.replace(r"\", r'%5C', 20)

    NAME1, NAME2 = name.split('_')
    WRAPPER_DEFAULTS = {'NAME 1': NAME1,
                        'NAME 2': NAME2,
                        'ORIGIN: CITY': f'ORIGIN: {city}',
                        ', COUNTRY': f', {country}',
                        'MM/YY': str(now.month)+"/"+str(now.year)[-2:],
                        'TN1, TN2, TN3': tasting_notes,
                        'DARKPER': darkper,
                        'map_image.png': map_file,
                        'stellar_image.png': stellar_file}
                        
    #save data
    dat = {'spec':spec,'loc':[lat, lon],'flavors':flavor_data}
    dat.update(WRAPPER_DEFAULTS)
    with open(os.path.join(wrapper_folder, f"{name}_dat.pkl"),"wb") as f:
        pickle.dump(dat,f)
        
    shutil.copy(os.path.join(WRAPPER_SRCDIR, 'Dark_Wrapper_Template.svg'),
                os.path.join(wrapper_folder, 'wrapper.svg'))
    replace_defaults(os.path.join(wrapper_folder, 'wrapper.svg'),
                     os.path.join(wrapper_folder, 'wrapper.svg'),
                     replacedict = WRAPPER_DEFAULTS)
    print(f'Built wrapper {name}')
    return
    
if __name__ == '__main__': 
    name = 'Chaparral_Forest' #expects two part name, separated by _
    darkper = '65' #str
    tasting_notes = 'BLUEBERRY, FUDGE, EARTH'  # single string
    
    # 0-10
    flavor_data = [
        ("Floral", 2),
        ("Fruit", 7),
        ("Nut", 4),
        ("Earth", 6),
        ("Chocolate", 8),
        ("Bitter", 2)]
        
    specf = None
    
    lat, lon = 3.725365326642447, -75.48982214591314 
    city, country = 'Chaparral', 'Colombia'
    
    create_wrapper(name, darkper, tasting_notes, lat, lon, city, country, flavor_data, specf)
