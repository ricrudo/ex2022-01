import json
import os

posibilidadesBinario = [[1],[-1],
        [.5,.5],[0.5,-.5],[-.5,.5],
        [.25,.25,.25,.25],[.25,.5,.25],[.25,-.5,.25],[.5,.25,.25],[.25,.25,.5],[-.5,.25,.25],[.25,.25,-.5],[.75,.25]]

posibilidadesTernario = [[1.5],[-1.5],[.5,.5,.5],[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5],[1,.5],[-1,.5],[1,-.5],
        [.25,.25,.25,.25,.25,.25],[.5,.25,.25,.5],[.25,.25,.5,.5],[.5,.5,.25,.25],[.25,.25,.25,.25,.5],[.5,.25,.25,.25,.25],[.25,.25,.5,.25,.25]]

posible_bars = ['4/4', '3/4', '2/4', '6/8', '8/9']

posible_clefs = ['sol', 'fa', 'percu']

data = {'posibleRhythms': posibilidadesBinario, 'clef': posible_clefs[2], 'bars': [posible_bars[0]]}

path_file = os.sep.join([os.getcwd(), 'audioperceptiva', 'rhythms', 'content.json'])
with open(path_file, 'w') as f:
    json.dump(data, f, indent=4)
