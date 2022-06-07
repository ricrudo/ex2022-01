from random import choice
from collections import namedtuple

from kivy.uix.label import Label

from ried.chord.chord_generator import Chord
from ried.note.note_generator import Note

from audio import midi

statement = 'Selecciones "Verdadero" si el ACORDE presentado en el audio coincide con la descripción que se encuentra debajo, de lo contrario seleccione "Falso".'

class Quest_Gen:

    def __init__(self, n_answers=4, counter=1):
        self.counter = counter
        self.chords = ['mayor', 'menor']
        self.n_answers = n_answers
        self.answers = self.make_questionary()

    def make_questionary(self):
        response = {}
        times = 1
        while times * len(self.chords) < self.n_answers:
            times += 1
        chords = self.chords * times
        for _ in range(self.n_answers):
            q = chords.pop(choice(range(len(chords))))
            answer = choice([True, False])
            if answer:
                response[f'question_{self.counter}'] = {'audio':q, 'visual': q}
            else:
                response[f'question_{self.counter}'] = {'audio':q, 'visual': choice(self.chords)}
            self.counter += 1
        return response


def Run_questionary(question):
    audio = make_audio(question['audio'])
    label = make_label(question['visual'])
    return label, audio

Bar = namedtuple('Bar', ['content'])

def make_audio(question):
    posibleNotes = [f'{root}{alter}4' for root in 'ABCDEFG' for alter in ['', '#', 'b']]
    
    root = Note(choice(posibleNotes))
    if question == 'menor':
        third = root + '3m'
    elif question == 'mayor':
        third = root + '3M'
    fifth = root + '5p'
    for x in [root, third, fifth]:
        x.set_duration(4)
    chord = Chord(content=[root, third, fifth])
    chord.duration = 4
    beat = Bar([chord])
    bar = Bar([beat])
    instr = Bar([bar])
    audio = midi.create_midiFile(content=[bar])
    return audio

def make_label(question):
    l = Label(text=f'Acorde {question}')
    l.size_hint = None, None
    l.size=(1024, 200)
    l.font_size = '36dp'
    l.text_size = l.size
    l.valign = 'middle'
    l.halign = 'center'
    l.color = 0,0,0,1
    return l

