from random import choice

from kivy.uix.label import Label

from ried_kivy.interactive_staff import staff_generator
from ried.scale.scale_generator import Scale

statement = 'Seleccione "Verdadero" si el texto corresponde a una de las tonalidades posibles para la ARMADURA presentada en el pentagrama, de lo contrario seleccione "Falso".'

class Quest_Gen:

    def __init__(self, n_answers=5, counter=1):
        self.counter = counter
        self.roots = [f'{root}b' for root in 'ABDE']
        self.roots.extend([f'{root}#' for root in 'FC'])
        self.roots.extend([f'{root}' for root in 'ABCDEFG'])
        self.mode = ['mayor', 'menor']
        self.n_answers = n_answers
        self.answers = self.make_questionary()

    def make_questionary(self):
        response = {}
        roots = self.roots[:]
        for x in range(self.n_answers):
            r = roots.pop(choice(range(len(roots))))
            m = choice(self.mode)
            q = f'{r} {m}'
            answer = choice([True, False])
            if answer:
                response[f'question_{self.counter}'] = {'audio':q, 'visual': q}
            else:
                response[f'question_{self.counter}'] = {'audio':q, 'visual': f'{choice(self.roots)} {m}'}
            self.counter += 1
        return response


def Run_questionary(question):
    label = make_label(question['audio'])
    staff = make_staff(question['visual'])
    return staff, label


def make_label(question):
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
    mode = 'mayor' in question and 'ionian' or 'menor' in question and 'aeolian'
    
    sc = Scale()
    primera = sc.generate_scale(root=root, mode=mode)
    primera = ''.join(primera)
    if '#' in primera:
        alter = primera.count('#')
    elif 'b' in primera:
        alter = primera.count('b') * -1
    else:
        alter = 0

    interStaff = staff_generator.InteractiveStaff()
    interStaff.width = 200
    interStaff.init_staff(alter=alter)
    return interStaff

