import json
import os

inter = ['2M', '3m', '3M', '4P', '6M']
roots = [f'{root}{alter}4' for root in 'CDEFGAB' for alter in ['b','','#']]

data = {'roots': roots, 'intervals':inter}


path_file = os.sep.join([os.getcwd(), 'audioperceptiva', 'intervals', 'content.json'])
with open(path_file, 'w') as f:
    json.dump(data, f, indent=4)

