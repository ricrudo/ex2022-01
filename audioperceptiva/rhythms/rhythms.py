import json
import os
from random import choice

from ried.bar.bar_generator import Bar
from ried_kivy.interactive_staff import staff_generator

from audio import midi

statement = 'Seleccione "Verdadero" si el RITMO presentado en el audio coincide con la partitura que se encuentra debajo, de lo contrario seleccione "Falso".'

class Quest_Gen:
    with open(os.sep.join(['audioperceptiva', 'rhythms', 'content.json'])) as f:
        options = json.load(f)

    def __init__(self, n_answers=5, beats=4, subdivision='binary', counter=1):
        self.counter = counter
        self.subdivision = subdivision
        self.n_answers = n_answers
        self.beats = beats
        self.answers = self.make_questionary()

    def make_questionary(self):
        response = {}
        for x in range(self.n_answers):
            q = self._select_rhythms()
            answer = choice([True, False])
            if answer:
                response[f'question_{self.counter}'] = {'audio':q, 'visual': q}
            else:
                response[f'question_{self.counter}'] = {'audio':q, 'visual': self._select_rhythms()}
            self.counter += 1
        return response

    def _select_rhythms(self):
        response = []
        while len(response) < self.beats:
            beat = choice(self.options['posibleRhythms'])
            if beat not in response:
                if not response and beat[0] < 0:# and isinstance(q.content[0], Silence):
                    continue

                response.append(beat)
        return response


def Run_questionary(question):
    audio = make_audio(question['audio'])
    staff = make_visual(question['visual'])
    return staff, audio

def make_audio(question):
    content = ['B4' for j in range(sum([len(x) for x in question]))]
    bar = Bar('4-4', content=content, subdivision='distribution', distribution=question)
    audio = midi.create_midiFile(content=[bar], program=[115])
    return audio


def make_visual(question):
    content = ['B4' for j in range(sum([len(x) for x in question]))]
    bar = Bar('4-4', content=content, subdivision='distribution', distribution=question)
    interStaff = staff_generator.InteractiveStaff()
    interStaff.init_staff(content=[bar])
    return interStaff
