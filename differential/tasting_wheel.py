import os
import cv2
import glob
import numpy as np
import pdb
from matplotlib import rcParams
rcParams['font.family']='Gotham'
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)#The OffsetBox is a simple container artist.

def search_list(val, level, masterlist):
    # val: str, to search for
    # level: index, either 0, 1, or 2
    # masterlist: either masterix or mastername
    return [n for n,x in enumerate(masterlist) if x.split('_')[level] == val]

def format_logo(logopath):
    logo = cv2.imread(logopath)
    im = cv2.resize(logo, (logo.shape[1]//5, logo.shape[0]//5), interpolation=cv2.INTER_NEAREST)
    alpha =  np.zeros((im.shape[0],im.shape[1], 1)).astype(np.uint8)
    alpha[im[:,:,:1] == 0] = 255
    im = np.concatenate([im,alpha], axis=-1).astype(np.uint8)
    return im

def plot_tasting_wheel(flavors, logopath=None, savepath=None):
    '''
    flavors: dict, assumes three levels of flavors e.g. {fruit: {red fruit: [cherry], tropical fruit: [papaya, banana]}}
    logopath: str or None, filepath to logo png. If None, will not plot logo
    savepath: str or None, filepath to save out image. If None will not save out
    '''
    # unravel flavor dict
    masterlist = []
    for ntop, name in enumerate(list(flavors)):
        for nmid, mid_category in enumerate(list(flavors[name])):
            for nbot, bottom in enumerate(flavors[name][mid_category]):
                masterlist.append( (f'{ntop}_{nmid}_{nbot}', f'{name}_{mid_category}_{bottom}') )
    masterix, mastername = zip(*masterlist)
    masterix, mastername = np.array(masterix), np.array(mastername)
    
    #set colors
    cmap = ['crimson', 'peru', 'olivedrab', 'orange', 'brown']#  plt.colormaps["tab20c"]

    # get angles and labels for pie plot
    ntop = len(np.unique([x.split('_')[0] for x in masterix]))
    nbot = len(masterix)
    botangle = 2*np.pi / nbot 
    top_colors = [mcolors.to_rgb(c) for c in cmap] # np.arange(ntop)*4 / (ntop*4) )

    topangles = []
    midangles, midcolors, midlabels = [], [], []
    botangles, botcolors, botlabels = [], [], []
    for n in range(ntop):
        mid_matches = search_list( str(n), 0, masterix )
        mid_ixs = [x.split('_')[1] for x in masterix[mid_matches]]
        unique_mid, uix = np.unique(mid_ixs, return_index=True)
        
        thismid = []
        for ux, nmid in enumerate(unique_mid):
            bot_matches = search_list( nmid, 1, masterix[mid_matches])
            botangles.extend([botangle]*len(bot_matches))
            botcolors.extend([top_colors[n]]*len(bot_matches))
            botlabels.extend([x.split('_')[2] for x in mastername[np.array(mid_matches)][bot_matches]])

            thismid.append(botangle*len(bot_matches))
            midcolors.append(top_colors[n])
            midlabels.append(mastername[mid_matches][uix[ux]].split('_')[1])
        midangles.extend(thismid)
        topangles.append( np.sum(thismid) )

    # plot
    size = .5
    fig, ax = plt.subplots(figsize=(10,10))
    textprops = {'fontsize':11, 'va':'center', 'ha':'center'}
    wedgeprops=dict(width=size, alpha=.8, edgecolor=(.2,.2,.2,.2))

    ax.pie(topangles, radius=size, colors=top_colors, labels=list(flavors),
          labeldistance=size+.15, rotatelabels=True, textprops=textprops,
          wedgeprops=wedgeprops)

    ax.pie(midangles, radius=2*size, colors=midcolors, labels=midlabels,
           textprops=textprops,wedgeprops=wedgeprops,
           labeldistance=size+.25, rotatelabels=True)

    ax.pie(botangles, radius=3*size, colors=botcolors, labels=botlabels,
           textprops=textprops,wedgeprops=wedgeprops, 
           labeldistance=1.7*size, rotatelabels=True)

    if logopath is not None:
        ax.pie(topangles, radius=size*.3, colors=top_colors, wedgeprops={ 'alpha':1})
        im = format_logo(logopath)
        #The child artists are meant to be drawn at a relative position to its #parent.
        imagebox = OffsetImage(im, zoom=.06)#Annotation box for solar pv logo
        #Container for the imagebox referring to a specific position *xy*.
        ab = AnnotationBbox(imagebox, (-.01,.01), frameon = False)
        ax.add_artist(ab)

    if savepath is None:
        savepath = 'testingwheel_test.png'
    if os.path.exists(savepath):
        print()
        print(f'File {savepath} already exists. Press c to overwrite tasting wheel, q to quit.')
        pdb.set_trace()                  
        print(f'Saving to {savepath}')
        plt.savefig(savepath, dpi=200)
    return


if __name__ == '__main__':
    logopath = r'C:/Users/kroma/Documents/Differential/LOGOS/LOGOS/D-C/D-C Logo.png'
    savepath = 'dcAromaWheeltest.png'
    
    fruit = {'Dried': ['Raisin', 'Fig', 'Tamarind'],
        'Tropical' : ['Pineapple', 'Coconut', 'Banana', 'Papaya'], 
        'Red': ['Cherry', 'Raspberry', 'Grape', 'Wine'],
        'Citrus': ['Orange', 'Lemon', 'Lime'],
        'Cooked': ['Strawberry Jam', 'Blueberry Jam', 'Apple Pie']}
    
    earthy = {'Flame': ['Roasted', 'Cedar', 'Smoke', 'Toast'],
              'Earth':['Vegetal', 'Grass', 'Mushroom', 'Earth', 'Coffee', 'Must', 'Peat'],
              'Spice': ['Vanilla', 'Nutmeg', 'Clove', 'Anise', 'Pepper']}
    
    chocolate = {'Chocolate': ['Fudge', 'Bitter', 'Classic Dark']}

    sweet = {'Floral': ['Rose', 'Jasmine', 'Honeysuckle', 'Tea'],
             'Caramel':['Molasses', 'Maple', 'Brown Sugar', 'Butterscotch']}

    nutty = {'Nut': ['Almond', 'Peanut', 'Cashew', 'Walnut', 'Nut Butter']}

    flavors = {'Fruit': fruit, 'Nut': nutty, 'Earth':earthy, 'Sweet': sweet, 'Chocolate':chocolate}
    
    plot_tasting_wheel(flavors, logopath=logopath, savepath=savepath)