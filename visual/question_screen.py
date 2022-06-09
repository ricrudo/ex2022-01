from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.animation import Animation

from visual import kv_elements, popup_noAnswer
import audioperceptiva, teoria

import json
import os
from functools import partial

string = '''
<QuestionScreen>
    RelativeLayout:
        id: relative
        size_hint: None, None
        size: 1024, 768
        pos: (self.parent.width/2)-512, (self.parent.height/2)-384
    
        canvas.before:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                size:self.size
                pos:0,0
                source: "assets/bk.jpg"
            Color:
                rgba: 1,1,1,1
                #rgba: 1,1,1,0.6
            Rectangle:
                size: self.size
                pos: 0,0
        Border:
            height: 80
            pos: 0, 768-80
        Label:
            canvas.before:
                Color:
                    rgba: 0,0,0,0.3
                Rectangle:
                    size: 1024, 50
                    pos: 0, 768 - 65
            bold: True
            id: header
            size_hint: None, None
            size: 900, 80
            pos: 40,768-80
            color: 1,1,1,1
            font_size: '24dp'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            id: timer
            canvas.before:
                Color:
                    rgba: 1,1,1,1
                Rectangle:
                    pos: self.pos
                    size: self.size
            size_hint: None, None
            color: 0,0,0,1
            text: '00:00'
            font_size: '24dp'
            size: 100,60
            pos: 914, 768-70

        Label:
            canvas.before:
                Color:
                    rgba: 0,1,0,0
                Rectangle:
                    size: self.size
                    pos: self.pos
            id: statement
            text: 'El siguiente audio corresponde con la notación musical presentada en el ejemplo que continua despues de la explicación anteriormente mencionada y que pocos entiendes y que puede ser confusa pero que no se como'
            size_hint: None, None
            color: 0,0,0,1
            size: 900, 200
            pos: 62, 454
            text_size: self.size
            halign: 'left'
            valign: 'top'
            font_size: '24dp'
        ButtonPlaySound:
            id: btnPlay
            size: 200, 50
            pos: (1024/2)-(self.size[0]/2), 424
            on_release: root.release_button(self, 'play_sound')
        ButtonHold:
            id: verdad
            text: 'Verdadero'
            pos: 1024/2-self.width - 10, 158 - 34
            on_release: root.release_button(self, 'true')
        ButtonHold:
            id: falso
            text: 'Falso'
            pos: 1024/2 + 10, 158 - 34
            on_release: root.release_button(self, 'false')
        Border:
            pos: 0, 0
        ButtonBlack:
            id: sig
            text: 'Siguiente'
            pos: 1024-230, 20
            on_release: root.release_button(self, 'next')
        ButtonBlack:
            id: pre
            disabled: True
            text: 'Anterior'
            pos: -300 if self.disabled == True else 20, 20
            on_release: root.release_button(self, 'previous')
        
        Widget:
            size_hint: None, None
            id: cortina
            pos: -1024, 90
            size: 1024, 768-90-80
            canvas.after:
                Color:
                    rgba: 1,1,1,1
                Rectangle:
                    pos: self.pos
                    size: self.size
    BlackOut:
        size: (self.parent.width-1024)/2, self.parent.height
        pos:0,0
    BlackOut:
        size: (self.parent.width-1024)/2, self.parent.height
        pos:self.parent.width - self.width,0


'''

Builder.load_string(string)

class QuestionScreen(Screen):

    translator = {'audioperceptiva': 'audioperceptiva',\
            'bar': 'Compases',\
            'intervals': 'Intervalos',\
            'chords': 'Acordes',\
            'rhythms': 'Ritmos',\
            'melody': 'Melodías',\
            'teoria': 'teórica',\
            'keys': 'Armaduras',\
            'scales': 'Escalas'
            }

    def release_button(self, btn, text):
        if text in ['true', 'false']:
            self.sm.currentAnswer = text
            if text == 'true': 
                other = self.ids.falso
            else: 
                other = self.ids.verdad
            other.liberate()
        elif text in ['next', 'previous']:
            response = self.check_answer()
            if response:
                if text == 'next':
                    if self.sm.indexQstn < self.sm.totalQstn:
                        self.sm.indexQstn += 1
                    else:
                        self.register_answer()
                        self.sm.show_prompSend()
                        return
                    if self.sm.indexQstn > 1:
                        self.ids.pre.disabled = False
                else:
                    if self.sm.indexQstn > 1:
                        self.sm.indexQstn -= 1
                    if self.sm.indexQstn == 1:
                        btn.disabled = True
                self.register_answer()
                if hasattr(self, 'staff'):
                    self.ids.relative.remove_widget(self.staff)
                    del self.staff
                if hasattr(self, 'label'):
                    self.ids.relative.remove_widget(self.label)
                    del self.label
                self.set_header()
        elif text in ['play_sound']:
            if hasattr(self, 'audio'):
                self.play_sound()

    def set_header(self, **kwargs):
        if not self.sm:
            counter = kwargs['counter']
            total = kwargs['total']
            data = kwargs['data']
        else:
            counter = self.sm.indexQstn
            total = self.sm.totalQstn
            data = self.sm.data
        quest = f'question_{counter}'
        for section in data.keys():
            if section in ['audioperceptiva', 'teoria']:
                for category in data[section].keys():
                    for question in data[section][category].keys():
                        if question == quest:
                            self.ids.header.text = f'Sección {self.translator[section]} - {self.translator[category]} - {counter}/{total}'
                            self.build_question([section, category, question], data)
                            self.updateButton([section, category, question], data)
                            return 

    def build_question(self, head, data):
        self.head = head
        section, category, question = head
        question = data[section][category][question]
        audio = None
        if section == 'audioperceptiva':
            if category == 'bar':
                maker, audio = audioperceptiva.compas.Run_questionary(question)
                self.ids.statement.text = audioperceptiva.compas.statement
            elif category == 'intervals':
                maker, audio = audioperceptiva.intervals.Run_questionary(question)
                self.ids.statement.text = audioperceptiva.intervals.statement
            elif category == 'chords':
                maker, audio = audioperceptiva.chords.Run_questionary(question)
                self.ids.statement.text = audioperceptiva.chords.statement
            elif category == 'rhythms':
                maker, audio = audioperceptiva.rhythms.Run_questionary(question)
                self.ids.statement.text = audioperceptiva.rhythms.statement
            elif category == 'melody':
                maker, audio = audioperceptiva.melody.Run_questionary(question)
                self.ids.statement.text = audioperceptiva.melody.statement
        elif section == 'teoria':
            if category == 'bar':
                maker, label = teoria.compas.Run_questionary(question)
                self.ids.statement.text = teoria.compas.statement
            elif category == 'intervals':
                maker, label = teoria.intervals.Run_questionary(question)
                self.ids.statement.text = teoria.intervals.statement
            elif category == 'chords':
                maker, label = teoria.chords.Run_questionary(question)
                self.ids.statement.text = teoria.chords.statement
            elif category == 'keys':
                maker, label = teoria.keys.Run_questionary(question)
                self.ids.statement.text = teoria.keys.statement
            elif category == 'scales':
                maker, label = teoria.scales.Run_questionary(question)
                self.ids.statement.text = teoria.scales.statement

        self.staff = maker
        self.ids.relative.add_widget(maker)
        if isinstance(maker, Label):
            maker.pos = 0, 214
        else:
            maker.pos = (1024/2)-(maker.width/2), 180
        ani = Animation(x=1024)
        cortina = self.ids.cortina
        self.ids.relative.remove_widget(cortina)
        self.ids.relative.add_widget(cortina)
        self.ids.cortina.pos[0] = -1024
        ani.start(self.ids.cortina)
        if section == 'audioperceptiva':
            if audio:
                self.audio = audio
            elif not audio and hasattr(self, 'audio'):
                del self.audio
            self.ids.btnPlay.pos[0] = (1024/2)-(self.ids.btnPlay.size[0]/2)
        elif section == 'teoria':
            self.label = label
            self.ids.relative.add_widget(self.label)
            self.label.pos = (1024/2)-(self.label.width/2), 330
            self.ids.btnPlay.pos[0] = -1024


    def reset_animation(self, *args):
        self.ids.cortina.x = -1024

    def updateButton(self, head, data):
        section, category, question = head
        question = data[section][category][question]
        if 'answer' in question:
            if question['answer'] == 'true':
                self.ids.verdad.on_release()
                self.ids.falso.liberate()
            elif question['answer'] == 'false':
                self.ids.falso.on_release()
                self.ids.verdad.liberate()
        else:
            self.ids.falso.liberate()
            self.ids.verdad.liberate()

    def play_sound(self):
        filename = self.audio[0]
        self.sound = SoundLoader.load(filename)
        self.sound.play()
        Clock.schedule_once(self.stop_sound, self.audio[1])
        self.ids.pre.disabled = True
        self.ids.sig.disabled = True

    def stop_sound(self, *args):
        self.sound.stop()
        del self.sound
        self.ids.btnPlay.disabled = False
        if self.sm.indexQstn > 1:
            self.ids.pre.disabled = False
        self.ids.sig.disabled = False
    
    def check_answer(self):
        if any([self.ids[x].selected for x in ['verdad', 'falso']]):
            return True
        if not hasattr(self.sm, 'currentAnswer'): 
            if not hasattr(self, 'alertas'):
                self.noAnswer = popup_noAnswer.NoAnswer()
                self.alertas = {1:'NA', 2:'NA', 3:'NA'}
            if any(x == self.sm.indexQstn for x in list(self.alertas.values())):
                return True
            if any(x == 'NA' for x in list(self.alertas.values())):
                for x in self.alertas:
                    if self.alertas[x] == 'NA':
                        self.alertas[x] = self.sm.indexQstn * 1
                        self.noAnswer.open()
                        return False

        return True

    def register_answer(self):
        if hasattr(self.sm, 'currentAnswer'):
            section, category, question = self.head
            expected = self.sm.data[section][category][question]['audio'] == self.sm.data[section][category][question]['visual']
            if not expected:
                if self.sm.currentAnswer == 'false':
                    points = 1
                else:
                    points = 0
            else:
                if self.sm.currentAnswer == 'true':
                    points = 1
                else:
                    points = 0
            self.sm.data[section][category][question]['answer'] = self.sm.currentAnswer
            self.sm.data[section][category][question]['points'] = points
            del self.sm.currentAnswer
        self.sm.data['Head'] = f'question_{self.sm.indexQstn}'
        self.sm.data['left_time'] = self.timer.left_time
        self.sm.save_time()

