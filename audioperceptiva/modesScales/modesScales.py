from random import choice

from kivy.uix.label import Label

from ried_kivy.interactive_staff import staff_generator
from ried.scale.scale_range import ScaleRange
from ried.note.note_generator import Note
from ried.bar.bar_generator import Bar

from audio import midi

statement = 'Seleccione "Verdadero" si el audio coincide con el tipo de ESCALA MODAL que se encuentra debajo, de lo contrario seleccione "Falso".'

class Quest_Gen:

    def __init__(self, n_answers=5, counter=1):
        self.counter = counter
        self.roots = [f'{root}b' for root in 'ABDE']
        self.roots.extend([f'{root}#' for root in 'FC'])
        self.roots.extend([f'{root}' for root in 'ABCDEFG'])
        self.mode = ['jónica', 'dórica', 'frigia', 'lidia', 'mixolidia', 'eólica', 'locria']
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
    audio = make_audio(generateScale(question['audio']))
    label = make_label(question['visual'])
    return label, audio


def generateScale(question):
    root, mode = question.split(' ')
    modeTranslate = {'jónica': 'ionian', 'dórica': 'dorian', 'frigia': 'phrygian', 'lidia': 'lydian', 'mixolidia': 'mixolydian', 'eólica': 'aeolian', 'locria': 'locrian'}
    mode = modeTranslate[mode]
    rangeScale = ScaleRange(Note(f'{root}4'), Note(f'{root}5'), key=root, mode=mode)
    return [x.full_name for x in rangeScale.range]
    

def make_audio(rangeScale):
    bar = Bar('8-4', content=rangeScale, subdivision='distribution', distribution=[[1],[1],[1],[1],[1],[1],[1],[1]])
    audio = midi.create_midiFile(content=[bar])
    return audio


def make_label(question):
    mode = question.split(' ')[1]
    l = Label(text=f'Escala {mode}')
    l.size_hint = None, None
    l.size=(1024, 200)
    l.font_size = '36dp'
    l.text_size = l.size
    l.valign = 'middle'
    l.halign = 'center'
    l.color = 0,0,0,1
    return l

