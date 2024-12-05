from itertools import chain, zip_longest
from matplotlib import rcParams
rcParams['font.family']='Gotham'
from math import ceil, pi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import imageio
import cartopy
import cartopy.crs as ccrs


def round_up(value):
    """

    >>> round_up(25)

    30

    """
    return int(ceil(value / 10.0)) * 10


def even_odd_merge(even, odd, filter_none=True):
    """

    >>> list(even_odd_merge([1,3], [2,4]))

    [1, 2, 3, 4]

    """
    if filter_none:
        return filter(None.__ne__, chain.from_iterable(zip_longest(even, odd)))

    return chain.from_iterable(zip_longest(even, odd))
def prepare_angles(N):
    angles = [n / N * 2 * pi for n in range(N)]

    # Repeat the first angle to close the circle

    angles += angles[:1]

    return angles
def prepare_data(data):
    labels = [d[0] for d in data]  # Variable names

    values = [int(d[1]) for d in data]

    # Repeat the first value to close the circle

    values += values[:1]

    N = len(labels)
    angles = prepare_angles(N)

    return labels, values, angles, N
def prepare_stellar_aux_data(angles, ymax, N):
    angle_midpoint = pi / N

    stellar_angles = [angle + angle_midpoint for angle in angles[:-1]]
    stellar_values = [0.05 * ymax] * N

    return stellar_angles, stellar_values
def draw_peripherals(ax, labels, angles, ymax, outer_color, inner_color):
    # X-axis

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='black', size=20,fontweight='bold')

    # Y-axis

    ax.set_yticks(range(10, ymax, 10))
    ax.set_yticklabels(range(10, ymax, 10), color='black', size=7)
    ax.set_ylim(0, ymax)
    ax.set_rlabel_position(0)

    # Both axes

    ax.set_axisbelow(True)

    # Boundary line

    ax.spines["polar"].set_color(outer_color)

    # Grid lines

    ax.xaxis.grid(True, color=inner_color, linestyle="--")
    ax.yaxis.grid(True, color=inner_color, linestyle="--")
def draw_stellar(
    ax,
    labels,
    values,
    angles,
    N,
    shape_color="black", #tab:blue",
    outer_color="slategray",
    inner_color="white",
):
    # Limit the Y-axis according to the data to be plotted

    ymax = round_up(max(values))

    # Get the lists of angles and variable values

    # with the necessary auxiliary values injected

    stellar_angles, stellar_values = prepare_stellar_aux_data(angles, ymax, N)
    all_angles = list(even_odd_merge(angles, stellar_angles))
    all_values = list(even_odd_merge(values, stellar_values))

    # Apply the desired style to the figure elements

    draw_peripherals(ax, labels, angles, ymax, outer_color, inner_color)

    # Draw (and fill) the star-shaped outer line/area

    ax.plot(
        all_angles,
        all_values,
        linewidth=1,
        linestyle="solid",
        solid_joinstyle="round",
        color=shape_color,
    )

    ax.fill(all_angles, all_values, shape_color)

    # Add a small hole in the center of the chart

    ax.plot(0, 0, marker="o", color="white", markersize=3)

    
def pokey_star(data, save=None):
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(111, polar=True)  # Don't forget the projection!

    
    draw_stellar(ax, *prepare_data(data))
    if save is not None:
        plt.savefig(save, dpi=600)
        tmp = imageio.imread(save)
        tmp[:,:,3] = 255-tmp[:,:,0] #modify alpha channel
        imageio.imwrite(save, tmp)
    else:
        plt.draw()
    plt.close('all')
                   


def mapthingy(lat,lon,mark_colo='k', save=None):

    fig = plt.figure(figsize=(11,11))

    ax = fig.add_subplot(1,1,1,projection=ccrs.EckertIV())

    ax.set_global()

    ax.patch.set_facecolor(color='gray')
    #ax.outline_patch.set_edgecolor('gray')

    ax.add_feature(cartopy.feature.OCEAN, color='white')

    ax.plot(lon, lat, mark_colo, marker=7, markersize=29, transform=ccrs.PlateCarree())
    if save is not None:
        plt.savefig(save, dpi=600)
        tmp = imageio.imread(save)
        tmp[:,:,3] = 255-tmp[:,:,0] #modify alpha channel
        imageio.imwrite(save, tmp)
    else:
        plt.show()
    plt.close('all')

    
def wavelength_to_rgb(wavelength, gamma=0.8):
    ''' taken from http://www.noah.org/wiki/Wavelength_to_RGB_in_Python
    This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    Additionally alpha value set to 0.5 outside range
    '''
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 750:
        A = 1.
    else:
        A = 0.5
    if wavelength < 380:
        wavelength = 380.
    if wavelength > 750:
        wavelength = 750.
    if 380 <= wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 440 <= wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif 490 <= wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 <= wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif 580 <= wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif 645 <= wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return (R, G, B, A)

def plot_spec(specf,linecolor='white',save=None,offset=.05):
    if specf.endswith('.npy'):
        wavelengths = np.linspace(400, 750, 1000)
        specdata = np.load(specf, allow_pickle=True)
        if 'spec' in specdata:
            specdata = specdata['spec']
        minlamb = 300
        maxlamb = -100
        spectrum = offset+specdata[1][minlamb:maxlamb][::-1]
        wavelengths = specdata[0][minlamb:maxlamb][::-1]
    else:
        df = pd.read_csv(specf)
        specdata = (df.Wavelength.values, df.Intensity.values)
        minlamb = 0
        maxlamb = len(specdata[0])
        spectrum = offset+specdata[1][minlamb:maxlamb]
        wavelengths = specdata[0][minlamb:maxlamb]
    
    clim = (380, 750)
    norm = plt.Normalize(*clim)
    wl = np.arange(clim[0], clim[1] + 1, 2)
    colorlist = list(zip(norm(wl), [wavelength_to_rgb(w) for w in wl]))
    spectralmap = matplotlib.colors.LinearSegmentedColormap.from_list("spectrum", colorlist)

    fig, axs = plt.subplots(1, 1, figsize=(8*2, 4*2), tight_layout=True)

    axs.plot(wavelengths, spectrum, color=linecolor, linewidth=1)

    y = spectrum
    X, Y = np.meshgrid(wavelengths, y)

    #extent = (400, 800, np.min(y), np.max(y)) 
    extent = (np.min(wavelengths), np.max(wavelengths), np.min(y), np.max(y))

    axs.imshow(X, clim=clim, extent=extent, cmap=spectralmap, aspect='auto')
    #plt.xlabel('Wavelength (nm)',fontsize=44)
    axs.set_yticks([])
    axs.set_xticks([])

    axs.fill_between(wavelengths, spectrum, max(spectrum), color='w')
    axs.plot(specdata[0][minlamb:maxlamb][::-1],np.zeros_like(specdata[1][minlamb:maxlamb]),'k--',lw=10,label='Commercial Chocolate')
    axs.legend(fontsize=44)#,loc=3)
    if save is not None:
        plt.savefig(save,dpi=600)
    else:
        plt.show()
    plt.close('all')
    return
    
if __name__ == '__main__':
    from argparse import ArgumentParser
    from pathlib import Path
    
    parser = ArgumentParser()
    parser.add_argument('-n', '--name', help='name for plots')
    parser.add_argument('-o', '--odir', help='path to output directory')
    parser.add_argument('-m', '--map', action='store_true', help='plot map') 
    parser.add_argument('-s', '--spec', action='store_true', help='plot spectrogram') 
    parser.add_argument('-p', '--pokey', action='store_true', help='plot pokey star') 

    args = parser.parse_args()
    name = args.name if args.name else ''
    if args.odir:
        outpath = Path(args.odir)
    else:
        outpath = Path(__file__).parent.parent
    
    if args.map:
        lat, lon = input('\nLatitude and Longitude, comma separated: ').split(',')
        lat, lon = float(lat), float(lon)
        mapthingy(lat, lon, save=Path.joinpath(outpath, f'{name}_map.png'))
        
    if args.spec:
        specf = input('\nFilepath to spec data: ')
        plot_spec(specf, save=Path.joinpath(outpath, f'{name}_spec.png'))
        
    if args.pokey:
        flavors = ["Floral", "Fruit", "Nut", "Earth", "Chocolate", "Bitter"]
        ranks = input(f'\nRanks for {flavors}, 0-10 comma separated:\n').split(',')
        flavor_data = [(flavors[n], int(r)) for n,r in enumerate(ranks)]
        pokey_star(flavor_data, save=Path.joinpath(outpath, f'{name}_star.png'))

                  
