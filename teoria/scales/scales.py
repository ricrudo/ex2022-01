from random import choice

from kivy.uix.label import Label

from ried_kivy.interactive_staff import staff_generator
from ried.scale.scale_range import ScaleRange
from ried.note.note_generator import Note
from ried.bar.bar_generator import Bar

statement = 'Seleccione "Verdadero" si el texto con el nombre de la ESCALA coincide con escala presentada en el pentagrama, de lo contrario seleccione "Falso".'

class Quest_Gen:

    def __init__(self, n_answers=5, counter=1):
        self.counter = counter
        self.roots = [f'{root}b' for root in 'ABDE']
        self.roots.extend([f'{root}#' for root in 'FC'])
        self.roots.extend([f'{root}' for root in 'ABCDEFG'])
        self.mode = ['mayor', 'menor armonica', 'menor natural', 'menor melodica']
        self.options = [f'{r} {m}' for r in self.roots for m in self.mode]
        self.n_answers = n_answers
        self.answers = self.make_questionary()

    def make_questionary(self):
        response = {}
        options = self.options[:]
        for x in range(self.n_answers):
            q = options.pop(choice(range(len(options))))
            answer = choice([True, False])
            if answer:
                response[f'question_{self.counter}'] = {'audio':q, 'visual': q}
            else:
                response[f'question_{self.counter}'] = {'audio':q, 'visual': f'{q.split(" ")[0]} {choice(self.mode)}'}
            self.counter += 1
        return response


def Run_questionary(question):
    label = make_label(question['audio'])
    staff = make_staff(question['visual'])
    return staff, label


def make_label(question):
    question = question.replace('melodica', 'melódica')
    question = question.replace('armonica', 'armónica')
    l = Label(text=question)
    l.size_hint = None, None
    l.size=(1024, 200)
    l.font_size = '36dp'
    l.text_size = l.size
    l.valign = 'middle'
    l.halign = 'center'
    l.color = 0,0,0,1
    return l



def make_staff(question):
    root = question.split(' ')[0]
    mode = 'mayor' in question and 'ionian' or 'natural' in question and 'aeolian' or 'melodica' and 'melodic minor' or 'armonica' and 'harmonic minor'
    rangeScale = ScaleRange(Note(f'{root}4'), Note(f'{root}5'), key=root, mode=mode)
    if 'armonica' in question or 'melodica' in question: 
        rangeScale.range[-2] = rangeScale.range[-1] - '2m'
        if 'armonica' in question:
            rangeScale.range[-3] = rangeScale.range[-4] + '2m'
    content = [x.full_name for x in rangeScale.range]
    bar = Bar('4-4', content=content, subdivision='distribution', distribution=[[0.5,0.5], [0.5,0.5], [0.5,0.5], [0.5,0.5]])
    interStaff = staff_generator.InteractiveStaff()
    interStaff.init_staff(content=[bar], beamless=True)
    return interStaff
