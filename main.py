from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.config import Config

Config.set('graphics', 'resizable', False)
#Config.set('graphics', 'height', '768')
#Config.set('graphics', 'width', '1024')
Config.set('graphics', 'fullscreen', 'auto')
Config.set('kivy', 'exit_on_escape', 0)

from ried_kivy.interactive_staff import staff_generator
from login.login import Login
from visual import QuestionScreen, Timer, PromptSend, EndScreen, kv_elements
from audioperceptiva import rhythms

import os
import json

class SM(ScreenManager):

    def load_modules(self):
        self.indexQstn = 1
        self.totalQstn = 2
        login = Login(name='Login')
        login.sm = self
        self.add_widget(login)
        question = QuestionScreen(name='Question')
        question.sm = self
        question.timer = Timer(parent=question, time=1)
        self.add_widget(question)
        promptSend = PromptSend(name='PromptSend')
        promptSend.sm = self
        self.add_widget(promptSend)
        end = EndScreen(name='EndScreen')
        end.sm = self
        self.add_widget(end)
        self.transition = FadeTransition()
        self.current = 'Login'
        return self

    def show_prompSend(self, time=False):
        promptScreen = self.get_screen('PromptSend')
        if time:
            promptScreen.ids.statement.text = 'Su tiempo se ha agotado.\n\nPor favor oprima el botón "Enviar" para concluir con el examen.'
            promptScreen.ids.volver.disabled = True
            self.save_time()
        else:
            promptScreen.ids.statement.text = 'Ha llegado a la última pregunta del examen.\n\nAhora puede pulsar el botón "Enviar" para terminar definitivamente el examen o, si considera que cuenta con tiempo suficiente, oprima "Volver" para revisar las preguntas que desee.'
        if self.current != 'PromptSend':
            self.current = 'PromptSend'

    def save_time(self):
        self.data['left_time'] = 0
        self.save_data()

    def save_data(self):
        if not os.path.exists(os.sep.join(['login', 'users'])):
            os.mkdir(os.sep.join(['login', 'users']))
        filename = os.sep.join(['login', 'users', self.data['cedula']+'.dlt'])
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)


class ExamenAdmisionApp(App):

    def build(self):
        self.sm = SM()
        return self.sm.load_modules()

    def on_stop(self):
        if hasattr(self.sm, 'data'):
            self.sm.data['left_time'] = self.sm.get_screen('Question').timer.left_time
            self.sm.save_data()

ExamenAdmisionApp().run()

