import json
import os
from random import choice
from collections import namedtuple

from kivy.uix.label import Label

from ried.note.note_generator import Note
from ried.chord.chord_generator import Chord

from audio import midi


statement = 'Seleccione "Verdadero" si el INTERVALO presentado en el audio coincide con la descripción que se encuentra debajo, de lo contrario seleccione "Falso".'

class Quest_Gen:
    with open(os.sep.join(['audioperceptiva', 'intervals', 'content.json'])) as f:
        options = json.load(f)

    def __init__(self, n_answers=9, counter=1):
        self.counter = counter
        self.pos_inter = self.options['intervals']
        self.n_answers = n_answers 
        self.answers = self.make_questionary()

    def make_questionary(self):
        response = {}
        times = 1
        while times * len(self.pos_inter) < self.n_answers:
            times += 1
        intervals = self.pos_inter * times
        for _ in range(self.n_answers):
            inter = intervals.pop(choice(range(len(intervals))))
            answer = choice([True, False])
            if answer:
                response[f'question_{self.counter}'] = {'audio': inter, 'visual': inter}
            else:
                response[f'question_{self.counter}'] = {'audio': inter, 'visual': choice(self.pos_inter)}
            self.counter += 1
        return response

def Run_questionary(question):
    audio = make_audio(question['audio'])
    label = make_label(question['visual'])
    return label, audio

Bar = namedtuple('Bar', ['content'])
def make_audio(question):
    posibleNotes = [f'{root}{alter}4' for root in 'ABCDEFG' for alter in ['', '#', 'b']]
    
    low = Note(choice(posibleNotes), duration = 4)
    hi = low + question
    hi.set_duration(4)
    chord = Chord(content=[low, hi])
    chord.duration = 4
    beat = Bar([chord])
    bar = Bar([beat])
    audio = midi.create_midiFile(content=[bar])
    return audio

def make_label(question):
    translator = {'m': 'menor', 'M': 'mayor', 'p': 'perfecta', '2': 'Segunda', '3': 'Tercera', '4': 'Cuarta', '5': 'Quinta', '6': 'Sexta'}
    nume = question.replace(question[0], translator[question[0]])[:-1]
    suf = question.replace(question[-1], translator[question[-1]])[1:]
    l = Label(text=f'{nume} {suf}')
    l.size_hint = None, None
    l.size=(1024, 200)
    l.font_size = '36dp'
    l.text_size = l.size
    l.valign = 'middle'
    l.halign = 'center'
    l.color = 0,0,0,1
    return l
