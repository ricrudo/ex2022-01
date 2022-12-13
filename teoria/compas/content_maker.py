import json
import os

posibilidadesBinario = [[1],[-1],
        [.5,.5],[0.5,-.5],[-.5,.5],
        [.25,.25,.25,.25],[.25,.5,.25],[.25,-.5,.25],[.5,.25,.25],[.25,.25,.5],[-.5,.25,.25],[.25,.25,-.5],[.5,-.25,.25]]

posibilidadesTernario = [[.5,.5,.5],[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5],[1,.5],[-1,.5],[1,-.5],
        [.25,.25,.25,.25,.25,.25],[.5,.25,.25,.5],[.25,.25,.5,.5],[.5,.5,.25,.25],[.25,.25,.25,.25,.5],[.5,.25,.25,.25,.25],[.25,.25,.5,.25,.25]]

posible_bars = ['4/4', '3/4', '2/4', '6/8', '9/8']

data = {'binary': posibilidadesBinario, 'ternary': posibilidadesTernario, 'bars': posible_bars}

path_file = os.sep.join([os.getcwd(), 'teoria', 'compas', 'content.json'])
with open(path_file, 'w') as f:
    json.dump(data, f, indent=4)

