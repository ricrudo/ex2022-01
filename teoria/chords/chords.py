from random import choice

from kivy.uix.label import Label

from ried.bar.bar_generator import Bar
from ried_kivy.interactive_staff import staff_generator
from ried.note.note_generator import Note

statement = 'Seleccione "Verdadero" si el texto es la descripción correcta del ACORDE presentado en el pentagrama, de lo contrario seleccione "Falso".'

class Quest_Gen:

    def __init__(self, n_answers=5, counter=1):
        self.counter = counter
        self.chords = ['mayor', 'menor', 'aumentado', 'disminuido']
        self.n_answers = n_answers
        self.answers = self.make_questionary()

    def make_questionary(self):
        response = {}
        chords = []
        while len(chords) < self.n_answers:
            chords.extend(self.chords)
        for _ in range(self.n_answers):
            q = chords.pop(choice(range(len(chords))))
            answer = choice([True, False])
            root = get_root()
            if answer:
                response[f'question_{self.counter}'] = {'audio':f'{root} {q}', 'visual': f'{root} {q}'}
            else:
                response[f'question_{self.counter}'] = {'audio':f'{root} {q}', 'visual': f'{root} {self.get_chord(old=q)}'}
            self.counter += 1
        return response

    def get_chord(self, old=None):
        while True:
            chord = choice(self.chords)
            if chord != old:
                return chord

def get_root():
    posibleNotes = [f'{root}4' for root in 'ACDEFG' ]
    posibleNotes.extend([f'{root}b4' for root in 'BEA'])
    posibleNotes.extend([f'{root}#4' for root in 'FCG'])
    return choice(posibleNotes)


def Run_questionary(question):
    label = make_label(question['audio'])
    staff = make_staff(question['visual'])
    return staff, label

def make_label(question):
    question = question.split(' ')[1]
    l = Label(text=f'Acorde {question}')
    l.size_hint = None, None
    l.size=(1024, 200)
    l.font_size = '36dp'
    l.text_size = l.size
    l.valign = 'middle'
    l.halign = 'center'
    l.color = 0,0,0,1
    return l

def make_staff(question):
    root, question = question.split(' ') 
    root = Note(root)
    if question in ['menor', 'disminuido']:
        third = root + '3m'
    elif question in ['mayor', 'aumentado']:
        third = root + '3M'
    if question == 'disminuido':
        fifth = root + '5d'
    elif question == 'aumentado':
        fifth = root + '5a'
    else:
        fifth = root + '5p'

    bottom = root.full_name
    middle = third.full_name
    top = fifth.full_name
    bar = Bar('1-4', content=[[bottom, middle, top]], subdivision='distribution', distribution=[[1]])
    interStaff = staff_generator.InteractiveStaff()
    interStaff.width = 200
    interStaff.init_staff(content=[bar], beamless=True)
    return interStaff

