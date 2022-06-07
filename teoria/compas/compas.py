import json, os
from random import choice

from kivy.uix.label import Label

from ried.bar.bar_generator import Bar
from ried_kivy.interactive_staff import staff_generator


statement = 'Seleccione "Verdadero" si la SIGNATURA DE COMPÁS presentada en el pentagrama coincide con la notación rítmica dentro del pentagrama, de lo contrario seleccione "Falso".'

class Quest_Gen:
    with open(os.sep.join(['teoria', 'compas', 'content.json'])) as f:
        options = json.load(f)

    def __init__(self, n_answers=15, counter=1):
        self.counter = counter
        self.n_answers = n_answers
        self.answers = self.make_questionary()

    def make_questionary(self):
        response = {}
        measure = self.options['bars'] * 3
        for x in range(self.n_answers):
            bar, total_fig, sub = self.get_bar(measure)
            q = self.get_rhythms(total_fig, sub)
            answer = choice([True, False])
            if answer:
                response[f'question_{self.counter}'] = {'barA':bar,'audio':q, 'barB': bar,'visual': q}
            else:
                bar2, total_fig2, sub2 = self.get_bar(self.options['bars'][:], exception=bar)
                q2 = self.get_rhythms(total_fig2, sub2)
                response[f'question_{self.counter}'] = {'barA':bar, 'audio':q, 'barB': bar2, 'visual': q2}
            self.counter += 1
        return response

    def get_bar(self, measure, exception=None):
        while True:
            bar = measure.pop(choice(range(len(measure))))
            if bar != exception:
                break
        if bar[-1] == '4':
            total_fig = int(bar[0])
            sub = 'binary'
        else:
            total_fig = int(int(bar[0])/3)
            sub = 'ternary'
        return bar, total_fig, sub

    def get_rhythms(self, total_fig, sub):
        content = []
        while len(content) < total_fig:
            q = choice(self.options[sub])
            if q not in content:
                content.append(q)
        return content


def Run_questionary(question):
    label = make_label(question['barA'])
    staff = make_staff(question['barB'], question['visual'])
    return staff, label

def make_label(question):
    sep = [x for x in question if not x.isdigit()][0]
    question = question.split(sep)
    l = Label(text=f'{question[0]}/{question[1]}')
    l.size_hint = None, None
    l.size=(1024, 200)
    l.font_size = '36dp'
    l.text_size = l.size
    l.valign = 'middle'
    l.halign = 'center'
    l.color = 0,0,0,1
    return l
    
def make_staff(measure, question):
    content = ['B4' for j in range(sum([len(x) for x in question]))]
    bar = Bar(measure, content=content, subdivision='distribution', distribution=question)
    interStaff = staff_generator.InteractiveStaff()
    interStaff.init_staff(content=[bar])
    return interStaff
