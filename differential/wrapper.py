import os
import glob
import shutil
import datetime
import time
from pathlib import Path

import differential.plot_choco as pc
from differential.config import load_config, make_config, write_config
import differential.inkscape_move_files as imf
import default_templates as differential_templates

WRAPPER_SRCDIR = Path(differential_templates.__file__).parent /'bars' 
# default dstdir
current = os.getcwd()
WRAPPER_DSTDIR = os.path.join(os.path.split(current)[0], 'Wrappers')
# the following allows us search for wrappers by easy name, as well as full path. e.g. 'bolivian', 'nibs'
wrapper_folders = sorted(glob.glob(os.path.join(WRAPPER_DSTDIR, '*')))
wrapper_folders = [x for x in wrapper_folders if os.path.isdir(x)]

def insert_print(insert_dict, outdir):
    count = 0
    for insert_name, num_inserts in insert_dict.items():
        insert_name = os.path.abspath(insert_name)
        if not os.path.exists(insert_name):
            raise ValueError('Need full path to insert.')
        neven, nodd = num_inserts // 3, num_inserts % 3
        if neven:
            replaceDict = {}
            for _ in range(3):
                replaceDict["InsertFront_default.svg"] = "file:///" + insert_name
        if nodd:
            raise NotImplementedError('Sorry, too tired. Chantilly day.')
        directory = os.path.split(insert_name)[0]
        imf.replace_paths(directory, insert_name)
        imf.replace_defaults(os.path.join(WRAPPER_SRCDIR, 'InsertBack_print_printingmarks - Copy.svg'),
                            os.path.join(outdir, f'Insert_print_{count}.svg'),
                            replacedict = replaceDict, nreplace=3)
        imf.export(os.path.join(outdir, f'Insert_print_{count}.svg'),
                   os.path.join(outdir, f'Insert_print_{count}.pdf'))
        count += 1
    return


def wrapper_bar_print(wrapper_dict, outdir):
    hold = []
    count = 0
    for wrapper_name, num_wrappers in wrapper_dict.items():
        print(hold)
        if not os.path.exists(wrapper_name): #search
            matches = [x for x in wrapper_folders if wrapper_name in os.path.split(x)[-1].lower()]
            if len(matches) == 0:
                raise ValueError(f'could not find folder for wrapper {wrapper_name}')
            if len(matches) > 1:
                print(f'Warning! Found multiple matches for {wrapper_name}. Going with {matches[0]}.')
            match = matches[0]
            wfile = sorted(glob.glob(os.path.join(match, '*.svg')))
            wfile = [x for x in wfile if 'insert' not in x][0]
        else:
            wfile = wrapper_name

        # do count stuff
        hrefs = ['Blank_Wrapper_0.svg', 'Blank_Wrapper_1.svg', 'Blank_Wrapper_2.svg', 'Blank_Wrapper_3.svg']
        neven, nodd = num_wrappers//4, num_wrappers % 4
        if neven:
            replaceDict = {}
            for nw in range(4):
                replaceDict[hrefs[nw]] = "file:///" + wfile
                #shutil.copy(wfile, os.path.join(WRAPPER_DSTDIR, f'Wrapper_{nw}.svg'))
            imf.replace_defaults(os.path.join(WRAPPER_SRCDIR, 'Wrapper_Print4.svg'),
                            os.path.join(outdir, f'Wrapper_print_{count}.svg'),
                            replacedict = replaceDict)
            imf.export(os.path.join(outdir, f'Wrapper_print_{count}.svg'),
                   os.path.join(outdir, f'Wrapper_print_{count}.pdf'))
            count += 1
        if nodd:
            hold.extend([wfile]*nodd)
        nhold = len(hold) // 4
        for _ in range(nhold):
            replaceDict = {}
            for nw in range(4):
                wfile = hold.pop(0)
                replaceDict[hrefs[nw]] = "file:///" + wfile
                #shutil.copy(wfile, os.path.join(WRAPPER_DSTDIR, f'Wrapper_{nw}.svg'))
            imf.replace_defaults(os.path.join(WRAPPER_SRCDIR, 'Wrapper_Print4.svg'),
                            os.path.join(outdir, f'Wrapper_print_{count}.svg'),
                            replacedict = replaceDict)
            imf.export(os.path.join(outdir, f'Wrapper_print_{count}.svg'),
                   os.path.join(outdir, f'Wrapper_print_{count}.pdf'))
            count += 1
    if len(hold): # still some remaining
        replaceDict = {}
        for nw, wfile in enumerate(hold):
            replaceDict[hrefs[nw]] = "file:///" + wfile
            #shutil.copy(wfile, os.path.join(WRAPPER_DSTDIR, f'Wrapper_{nw}.svg')
        for bn in range(nw, 4):
            replaceDict[hrefs[bn]] = "file:///" + os.path.join(WRAPPER_SRCDIR, 'Blank_Wrapper.svg')
            imf.replace_defaults(os.path.join(WRAPPER_SRCDIR, 'Wrapper_Print4.svg'),
                                os.path.join(outdir, f'Wrapper_print_{count}.svg'),
                                replacedict = replaceDict)
        imf.export(os.path.join(outdir, f'Wrapper_print_{count}.svg'),
               os.path.join(outdir, f'Wrapper_print_{count}.pdf'))
        count += 1
    print(f'Saved wrapper_prints 0 - {count}')


def create_wrapper(config, odir, double=False, insert=True): #name, darkper, tasting_notes, lat, lon, city, country, flavor_data, specf):
    if os.path.exists(odir):
        pass #raise NameError(f'{wrapper_folder} already exists! :-o')
    else:
        os.mkdir(odir)
    
    #spec
    if not len(config['specim']):
        if len(config['specf']):
            pc.plot_spec(config['specf'], save=os.path.join(odir, f'spec.png'))
        config['specim'] = os.path.join(odir, f'spec.png')
    
    #star
    if not len(config['starf']):
        pc.pokey_star(config['flavor_data'].items(), save=os.path.join(odir, f'star.png'))
        config['starf'] = os.path.join(odir, f'star.png')

    #map
    if not len(config['mapf']):
        pc.mapthingy(config['lat'], config['lon'], save=os.path.join(odir, f'map.png'))
        config['mapf'] = os.path.join(os.path.join(odir, f'map.png'))
    
    # do wrapper stuff
    now = datetime.datetime.now()
    map_file = "file:///" + config['mapf'] #.replace(r"\", r'%5C', 20) 
    stellar_file = "file:///" + config['starf'] #.replace(r"\", r'%5C', 20)
    spec_file = "file:///" + config['specim']

    NAME1, NAME2 = config['name1'], config['name2']
    WRAPPER_DEFAULTS = {'NAME 1': NAME1,
                        'NAME 2': NAME2,
                        'ORIGIN: CITY': f'{config["city"]}',
                        ', COUNTRY': f', {config["country"]}',
                        'MM/YY': str(now.month)+"/"+str(now.year)[-2:],
                        'TN1, TN2, TN3': config["tasting_notes"],
                        'DARKPER': config["darkper"],
                        'map_image.png': map_file,
                        'stellar_image.png': stellar_file}
                        
    #save data
    config.update(WRAPPER_DEFAULTS)
    write_config(config, os.path.join(odir, f'config.yaml'))

    # do inkscape stuff    
    if double:
        wrappertemplate = 'DoubleBar_Template.svg'
    else:
        wrappertemplate = 'Dark_Wrapper_Template.svg'
    shutil.copy(os.path.join(WRAPPER_SRCDIR, wrappertemplate),
                os.path.join(odir, 'wrapper.svg'))
    imf.replace_defaults(os.path.join(odir, 'wrapper.svg'),
                     os.path.join(odir, 'wrapper.svg'),
                     replacedict = WRAPPER_DEFAULTS)
    if insert:               
        shutil.copy(os.path.join(WRAPPER_SRCDIR, 'insert_back.svg'),
                    os.path.join(odir, 'insert_back.svg'))
        imf.replace_defaults(os.path.join(odir, 'insert_back.svg'),
                        os.path.join(odir, 'insert_back.svg'),
                        replacedict = {'stellar.png': stellar_file,
                                        'spec.png': spec_file,
                                        'CITY, COUNTRY': config["city"] + ', '+config["country"],
                                        'YY': str(now.year)[-2:],
                                        'DARKPER': config['darkper']})
    print(f'Built wrapper {odir}')
    return


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--print', nargs='+', help='file and number')
    parser.add_argument('-c', '--config', help='path to config file')
    parser.add_argument('-o', '--odir', help='path to output directory')
    parser.add_argument('-d', '--double', help='double bar', action='store_true')
    parser.add_argument('-i', '--insert', help='create insert', action='store_true')
    args = parser.parse_args()

    if not args.odir:
        odir = WRAPPER_DSTDIR
    else:
        odir = os.path.abspath(args.odir)
    if not os.path.exists(odir):
        os.makedirs(odir)

    if args.print:
        template_dict = {k:int(v) for k,v in zip(args.print[::2], args.print[1::2])}
        if args.insert:
            insert_print(template_dict, odir)
        else:
            wrapper_bar_print(template_dict, odir)
        return

    if not args.config:
        config = make_config(odir)
    else:
        config = load_config(args.config)
    create_wrapper(config, odir, double=args.double, insert=args.insert)

if __name__ == '__main__': 
    main()