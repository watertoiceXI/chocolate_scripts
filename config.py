import yaml
import os

def load_config(cfgf):
    with open(cfgf, 'r') as fin:
        cfg = yaml.safe_load(fin)
    if 'flavor_data' in cfg:
        flavors = ["Floral", "Fruit", "Nut", "Earth", "Chocolate", "Bitter"]
        tmp = {flavor: cfg['flavor_data'][flavor] for flavor in flavors}
        cfg['flavor_data'] = tmp
    return cfg

def make_config(exportdir):
    name1 = input(r'Name 1 (first line on wrapper): ')
    name2 = input(r'Name 2 (second line on wrapper): ')
    if len(name1) == 0:
        raise ValueError('Need a name.')
    #name1 = name1.replace(' ', '_')
    #name2 = name2.replace(' ', '_')
    print('At any time to skip a question, press Enter.')
    darkper = input(r'% dark: ')
    
    lat, lon = input('\nLatitude and Longitude, comma separated: ').split(',')
    lat, lon = float(lat), float(lon)
    city, country = input('City and country, comma separated: ').strip().split(',')
    mapf = input('Filepath to map image: ')

    specf = input('\nFilepath to spec data: ')
    specim = input('Filepath to spectrum image: ')

    starf = input('\nFilepath to star image: ')
    tasting_notes = input('Tasting Notes: (comma separated): ')

    flavors = ["Floral", "Fruit", "Nut", "Earth", "Chocolate", "Bitter"]
    flavor_data = {}
    print('Rank flavors 0-10')
    for n,flavor in enumerate(flavors):
        if n > 0: 
            print(f"{flavor_data}")
        flavor_data[flavor] = int( input(f'{flavor}: '))

    settings = {'name1': name1,
                'name2': name2,
                'city': city,
                'country': country,
                'lat': lat,
                'lon': lon,
                'specf': specf,
                'darkper': darkper,
                'tasting_notes': tasting_notes,
                'flavor_data': flavor_data,
                'starf': starf,
                'mapf': mapf,
                'specim': specim
                }
    
    if not os.path.exists(exportdir):
        os.makedirs(exportdir)
    print(f'Saving config file to {exportdir}')
    write_config(settings, os.path.join(exportdir, 'config.yaml'))
    print(settings)
    return settings

def write_config(config, outf):
    with open(outf, 'w') as fout:
        yaml.dump(config, fout, default_flow_style=False)
    
if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-o', '--odir', help='output directory')
    args = parser.parse_args()

    if not args.odir:
        odir = os.path.split(os.getcwd())[0]
    else:
        odir = args.odir
    make_config(odir)
    