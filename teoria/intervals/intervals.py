from random import choice

from kivy.uix.label import Label

from ried.bar.bar_generator import Bar
from ried_kivy.interactive_staff import staff_generator
from ried.note.note_generator import Note

statement = 'Seleccione "Verdadero" si el texto es la descripción correcta del INTERVALO presentado en el pentagrama, de lo contrario seleccione "Falso".'

class Quest_Gen:

    def __init__(self, n_answers=15, counter=1):
        self.counter = counter
        self.intervals = ['2m', '2M', '3m', '3M', '4p', '5p', '6m', '6M', '7m', '7M']
        self.n_answers = n_answers
        self.answers = self.make_questionary()


    def make_questionary(self):
        response = {}
        quest = []
        for _ in range(self.n_answers):
            q = choice(self.intervals)
            if quest.count(q) < 2:
                answer = choice([True, False])
                low = get_low()
                if answer:
                    response[f'question_{self.counter}'] = {'audio':f'{low} {q}', 'visual': f'{low} {q}'}
                else:
                    response[f'question_{self.counter}'] = {'audio':f'{low} {q}', 'visual': f'{low} {choice(self.intervals)}'}
            self.counter += 1
        return response

def get_low():
    posibleNotes = [f'{root}4' for root in 'ACDEFG']
    posibleNotes.extend([f'{root}b4' for root in 'BEA'])
    posibleNotes.extend([f'{root}#4' for root in 'FCG'])
    return choice(posibleNotes)

def Run_questionary(question):
    label = make_label(question['audio'])
    staff = make_staff(question['visual'])
    return staff, label

def make_label(question):
    translator = {'m': 'menor', 'M': 'mayor', 'p': 'perfecta', '2': 'Segunda', '3': 'Tercera', '4': 'Cuarta', '5': 'Quinta', '6': 'Sexta', '7': 'Séptima'}
    question = question.split(' ')[1]
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

def make_staff(question):
    low, interval = question.split(' ')
    low = Note(low)
    hi = low + interval
    bottom = low.full_name
    top = hi.full_name
    bar = Bar('1-4', content=[[bottom, top]], subdivision='distribution', distribution=[[1]])
    interStaff = staff_generator.InteractiveStaff()
    interStaff.width = 200
    interStaff.init_staff(content=[bar], beamless=True)
    return interStaff

