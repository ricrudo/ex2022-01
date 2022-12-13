from random import choice

from kivy.uix.label import Label

from ried_kivy.interactive_staff import staff_generator
from ried.scale.scale_range import ScaleRange
from ried.note.note_generator import Note
from ried.bar.bar_generator import Bar

statement = 'Seleccione "Verdadero" si el nombre de la ESCALA MODAL coincide con la partitura que se encuentra debajo, de lo contrario seleccione "Falso".'

class Quest_Gen:

    def __init__(self, n_answers=5, counter=1):
        self.counter = counter
        self.roots = [f'{root}b' for root in 'ABDE']
        self.roots.extend([f'{root}#' for root in 'FC'])
        self.roots.extend([f'{root}' for root in 'ABCDEFG'])
        self.mode = ['jonica', 'dorica', 'frigia', 'lidia', 'mixolidia', 'eolica', 'locria']
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
    staff = make_staff(generateScale(question['visual']))
    return staff, label


def generateScale(question):
    root, mode = question.split(' ')
    modeTranslate = {'jonica': 'ionian', 'dorica': 'dorian', 'frigia': 'phrygian', 'lidia': 'lydian', 'mixolidia': 'mixolydian', 'eolica': 'aeolian', 'locria': 'locrian'}
    mode = modeTranslate[mode]
    rangeScale = ScaleRange(Note(f'{root}4'), Note(f'{root}5'), key=root, mode=mode)
    return [x.full_name for x in rangeScale.range]
    

def make_label(question):
    root, mode = question.split(' ')
    if mode[1] == 'o' and mode[0] != 'l':
        mode = mode[0] + 'ó' + mode[2:]
    mode = mode[:-1] + 'o'
    label = Label(text=f'{root} {mode}')
    label.size_hint = None, None
    label.size=(1024, 200)
    label.font_size = '36dp'
    label.text_size = label.size
    label.valign = 'middle'
    label.halign = 'center'
    label.color = 0,0,0,1
    return label

def make_staff(rangeScale):
    bar = Bar('4-4', content=rangeScale, subdivision='distribution', distribution=[[0.5,0.5], [0.5,0.5], [0.5,0.5], [0.5,0.5]])
    interStaff = staff_generator.InteractiveStaff()
    interStaff.init_staff(content=[bar], beamless=True)
    return interStaff
