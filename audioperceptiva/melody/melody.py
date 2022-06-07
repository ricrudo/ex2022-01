from random import choice

from ried.bar.bar_generator import Bar
from ried_kivy.interactive_staff import staff_generator

from audio import midi

statement = 'Seleccione "Verdadero" si la MELODIA presentada en el audio coincide con la partitura que se encuentra debajo, de lo contrario seleccione "Falso".'

class Quest_Gen:

    def __init__(self, n_answers=3, counter=1):
        self.counter = counter 
        self.notes = [f'{x}4' for x in 'CDEFG']
        self.n_answers = n_answers
        self.answers = self.make_questionary()

    def make_questionary(self):
        response = {}
        for x in range(self.n_answers):
            q = self.get_notes_melody()
            answer = choice([True, False])
            if answer:
                response[f'question_{self.counter}'] = {'audio':q, 'visual': q}
            else:
                response[f'question_{self.counter}'] = {'audio':q, 'visual': self.get_notes_melody()}
        self.counter += 1
        return response

    def get_notes_melody(self):
        response = []
        while len(response) < 5:
            n = choice(self.notes)
            if n not in response:
                response.append(n)
        return response


def Run_questionary(question):
    audio = make_audio(question['audio'][:])
    label = make_visual(question['visual'][:])
    return label, audio

def make_audio(question):
    bar = Bar('5-4', content=question, subdivision='distribution', distribution=[[1],[1],[1],[1],[1]])
    audio = midi.create_midiFile(content=[bar])
    return audio

def make_visual(question):
    bar = Bar('5-4', content=question, subdivision='distribution', distribution=[[1],[1],[1],[1],[1]])
    interStaff = staff_generator.InteractiveStaff()
    interStaff.init_staff(content=[bar],beamless=True)
    return interStaff
