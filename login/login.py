from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.graphics import Color

import os, json
from string import ascii_letters

import audioperceptiva, teoria

import requests

stringKv = '''
#:import os os
<Login>
    canvas.before:
        Rectangle:
            size:self.size
            pos:self.pos
            source: "assets/bk.jpg"
    Label:
        canvas.before:
            Color:
                rgba: 0,0,0,0.3
            Rectangle:
                size: self.size
                pos: self.pos
        color: 0.8, 0.8, 0.8, 1
        size_hint: None, None
        size: 900, 100
        pos: 62, 600
        font_size: '35dp'
        text_size: self.size
        halign: 'center'
        valign: 'middle'
        bold: True
        text: 'Bienvenido al examen de admisión al Programa de Música de la Universidad del Atlántico'
    Label:
        size: 200, 50
        pos: 100, 450
        canvas.before:
            Color:
                rgba: 0,0,0,0.3
            Rectangle:
                size: 1024, self.size[1] + 4
                pos: 0, self.pos[1] - 2
        size_hint: None, None
        font_size: '24dp'
        color: 0.8, 0.8, 0.8, 1
        text: 'Nombre completo'
    TextInput:
        id: name
        size_hint: None, None
        size: 900-320, 50 
        pos: 320, 450
        font_size: '24dp'
    Widget:
        color: 1,0,0,0
        id: shadowName
        canvas.before:
            Color:
                rgba: self.color
            Line:
                rectangle: name.pos[0] - 2, name.pos[1] -2, name.size[0] + 4, name.size[1] + 4
                width: 1.5
    Label:
        size_hint: None, None
        size: 200, 50 
        pos: 100, 350
        canvas.before:
            Color:
                rgba: 0,0,0,0.3
            Rectangle:
                size: 1024, self.size[1] + 4
                pos: 0, self.pos[1] - 2
        font_size: '24dp'
        text: 'No. Identificación'
    TextInput:
        id: identifica
        size_hint: None, None
        size: 300, 50 
        pos: 320, 350
        font_size: '24dp'
    Widget:
        color: 1,0,0,0
        id: shadowID
        canvas.before:
            Color:
                rgba: self.color
            Line:
                rectangle: identifica.pos[0] - 2, identifica.pos[1] -2, identifica.size[0] + 4, identifica.size[1] + 4
                width: 1.5
    ButtonBlack:
        pos: (1024/2)-100, 200
        text: 'Comenzar'
        on_release: root.start(self, name, identifica)
    Image:
        size_hint: None, None
        size: 130, 130 
        pos: 1024-150, 10
        source: 'assets/logoRied.png'
    Label:
        size_hint: None, None
        size: 130, 50 
        pos: 1024-150, 130
        font_size: '24dp'
        text: 'Powered by'

'''


Builder.load_string(stringKv)


class Login(Screen):

    def pressButton(self, btn):
        btn.background_color = 0.1,0,0.1,0.7

    def start(self, btn, name, identi):
        btn.background_color= 0,0,0,1
        nombre = self.formatName(name.text)
        cedula = identi.text
        if not nombre:
            self.ids.shadowName.color = 1,0,0,1
        else:
            self.ids.shadowName.color = 1,0,0,0
        if not cedula:
            self.ids.shadowID.color = 1,0,0,1
        else:
            self.ids.shadowID.color = 1,0,0,0
        if nombre and cedula:
            self.check_user(nombre, cedula)

    def formatName(self, name):
        posibles = ascii_letters + ' '
        nameFinal = ''
        for letter in name:
            if letter in posibles:
                nameFinal += letter
            else:
                nameFinal += '_'
        return nameFinal

    def check_user(self, nombre, cedula):
        cedula = ''.join([x for x in cedula if x.isdigit()])
        if os.path.exists(os.sep.join(['login', 'users', cedula+'.dlt'])):
            self.load_exam(cedula)
            self.sm.totalQstn = self.count_questions()
            self.sm.indexQstn = self.seek_header()
        else:
            self.create_exam(cedula, nombre)
            self.sm.totalQstn = self.counter - 1
            self.sm.indexQstn = 1
        questScreen = self.sm.get_screen('Question')
        questScreen.set_header(data=self.sm.data, counter=self.sm.indexQstn, total=self.sm.totalQstn)
        if self.sm.indexQstn != 1:
            questScreen.ids.pre.disabled = False
        if not 'left_time' in self.sm.data or self.sm.data['left_time'] > 0:
            questScreen.timer.left_time = self.sm.data['left_time']
            questScreen.timer.startTimer()
            self.sm.current = 'Question'
        else:
            self.sm.show_prompSend(time=True) 

    def load_exam(self, cedula):
        path = os.sep.join(['login', 'users', f'{cedula}.dlt'])
        with open(path, 'r') as f:
            self.sm.data = json.load(f)

    def count_questions(self):
        counter = 0
        for section in self.sm.data:
            if section in  ['audioperceptiva', 'teoria']:
                for category in self.sm.data[section].keys():
                    counter += len(self.sm.data[section][category])
        return counter

    def seek_header(self):
        if 'Head' in list(self.sm.data.keys()):
            question = self.sm.data['Head'].split('_')[-1]
            return int(question)
        return 1

    def create_exam(self, cedula, nombre):
        self.sm.data = {'nombre': nombre.strip(), 'cedula': cedula,'audioperceptiva': {}, 'teoria':{}}
        questStructure = self.call_API()
        self.counter = 1
        for key, value in questStructure['audioperceptiva'].items():
            self._audioperceptiva(category=key, n_answers=value)
        for key, value in questStructure['teoria'].items():
            self._teoria(category=key, n_answers=value)
        self.sm.data['left_time'] = questStructure['time']  * 60 * 1000
        self.sm.save_data()

    def call_API(self):
        response = requests.get('https://riedmusicapp.com/examination/examen_ua/cuestionario/Promusica')
        return json.loads(response.text)

    def _audioperceptiva(self, category, n_answers=None):
        if category == 'bar':
            q = audioperceptiva.compas.Quest_Gen(counter=self.counter, n_answers=n_answers)
            self.sm.data['audioperceptiva']['bar'] = q.answers
        elif category == 'intervals':
            q = audioperceptiva.intervals.Quest_Gen(counter=self.counter, n_answers=n_answers)
            self.sm.data['audioperceptiva']['intervals'] = q.answers
        elif category == 'chords':
            q = audioperceptiva.chords.Quest_Gen(counter=self.counter, n_answers=n_answers)
            self.sm.data['audioperceptiva']['chords'] = q.answers
        elif category == 'rhythms':
            q = audioperceptiva.rhythms.Quest_Gen(counter=self.counter, n_answers=n_answers)
            self.sm.data['audioperceptiva']['rhythms'] = q.answers
        elif category == 'melody':
            q = audioperceptiva.melody.Quest_Gen(counter=self.counter, n_answers=n_answers)
            self.sm.data['audioperceptiva']['melody'] = q.answers
        else:
            raise ValueError(f'{category} not found in teoria section')
        self.counter = q.counter

    def _teoria(self, category, n_answers=None):
        if category == 'chords':
            q = teoria.chords.Quest_Gen(counter=self.counter, n_answers=n_answers)
            self.sm.data['teoria']['chords'] = q.answers
        elif category == 'intervals':
            q = teoria.intervals.Quest_Gen(counter=self.counter, n_answers=n_answers)
            self.sm.data['teoria']['intervals'] = q.answers
        elif category == 'bar':
            q = teoria.compas.Quest_Gen(counter=self.counter, n_answers=n_answers)
            self.sm.data['teoria']['bar'] = q.answers
        elif category == 'keys':
            q = teoria.keys.Quest_Gen(counter=self.counter, n_answers=n_answers)
            self.sm.data['teoria']['keys'] = q.answers
        elif category == 'scales':
            q = teoria.scales.Quest_Gen(counter=self.counter, n_answers=n_answers)
            self.sm.data['teoria']['scales'] = q.answers
        else:
            raise ValueError(f'{category} not found in teoria section')
        self.counter = q.counter



