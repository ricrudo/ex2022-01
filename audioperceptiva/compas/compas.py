import json
import os
from random import choice

from ried.bar.bar_generator import Bar
from ried_kivy.interactive_staff import staff_generator

from audio import midi

statement = 'El siguiente audio presenta un metrónomo con 3 sonidos a distintas alturas. El sonido más agudo indica la primera fracción del compás, el sonido medio indica el comienzo de los demás pulsos del compás y el sonido más grave el resto de fracciones de cada pulso. Seleccione "Verdadero" si el audio conincide con el compás presentado en el pentagrama, de lo contrario seleccione "Falso".'

class Quest_Gen:

    def __init__(self, n_answers=9, counter=1):
        self.counter = counter
        self.bars = ['2/4', '3/4', '4/4', '6/8', '9/8']
        self.n_answers = n_answers
        self.answers = self.make_questionary()

    def make_questionary(self):
        response = {}
        times = 1
        while times * len(self.bars) < self.n_answers:
            times += 1
        bars = self.bars * times
        for _ in range(self.n_answers):
            q = bars.pop(choice(range(len(bars))))
            answer = choice([True, False])
            if answer:
                response[f'question_{self.counter}'] = {'audio':q, 'visual': q}
            else:
                response[f'question_{self.counter}'] = {'audio':q, 'visual': choice(self.bars)}
            self.counter += 1
        return response


def Run_questionary(question):
    audio = make_audio(question['audio'])
    staff = make_visual(question['visual'])
    return staff, audio

def make_audio(question):
    sep = [x for x in question if not x.isdigit()][0]
    num, dem = question.split(sep)
    num = int(num)
    den = int(dem)
    if den == 8:
        num = int(num/3)
    content = []
    distribution = []
    for pulso in range(num):
        if pulso == 0:
            content.append('C5')
        else:
            content.append('G4')
        if den == 4:
            content.append('D4')
            distribution.append([0.5,0.5])
        elif den == 8:
            content.extend(['D4', 'D4'])
            distribution.append([0.5,0.5,0.5])
    bar = Bar(question, content=content, subdivision='distribution', distribution=distribution)
    audio = midi.create_midiFile(content=[bar], program=[115])
    return audio

def make_visual(question):
    interStaff = staff_generator.InteractiveStaff()
    interStaff.width = 200
    interStaff.init_staff(measure=question)
    return interStaff


