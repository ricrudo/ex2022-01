from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import requests
import json

string = '''
<PromptSend>
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size:self.size
            pos:self.pos
            source: "assets/bk.jpg"
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: self.size
            pos: self.pos
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
        text: 'Fin del examen'
    Label:
        canvas.before:
            Color:
                rgba: 0,1,0,0
            Rectangle:
                size: self.size
                pos: self.pos
        id: statement
        size_hint: None, None
        color: 0,0,0,1
        size: 900, 200
        pos: 62, 454
        text_size: self.size
        halign: 'left'
        valign: 'top'
        font_size: '24dp'
    Border:
        pos: 0, 0
    ButtonBlack:
        id: enviar
        text: 'Enviar'
        pos: 1024-230, 20
        on_release: root.send_btn()
    ButtonBlack:
        id: volver
        text: 'Volver'
        pos: -300 if self.disabled == True else 20, 20
        on_release: root.back_btn()
    
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
'''

Builder.load_string(string)

class PromptSend(Screen):

    def back_btn(self):
        self.sm.current = 'Question'

    def send_btn(self):
        url = 'https://riedmusicapp.com/examination/examen_ua'
        response = requests.post(url, json=self.sm.data)
        self.parent.current = 'EndScreen'
