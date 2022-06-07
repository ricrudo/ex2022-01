import requests

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

string = '''
#:import os os
<EndScreen>
    canvas.before:
        Rectangle:
            size:self.size
            pos:self.pos
            source: "assets/bk.jpg"
    Widget:
        size_hint: 1, 1
        canvas.before:
            Color:
                rgba: 0,0,0,0.3
            Rectangle:
                size: self.size
                pos: self.pos
    Basiclabel:
        height: 100
        y: 600
        bold: True
        text: 'Gracias por tomar este examen'
        font_size: '44dp'
    Basiclabel:
        height: 200
        y: 420
        bold: True
        text: 'Este examen fue diseñado por www.riedmusic.com la primera empresa en latinoamerica en el diseño de apps para la formación musical.'
    Basiclabel:
        id: labelUseful
        height: 100
        y: 350
        bold: True
        text: 'Si lo deseas, puedes suscribirte a nuestra lista de correos para estas informado de nuestros lanzamientos y promociones.'
    TextInput:
        id: email
        size_hint: None, None
        size: 400, 50 
        pos: 312, 290
        font_size: '20dp'
        halign: 'center'
    Widget:
        size_hint: None, None
        size: 10, 10
        pos: -10, -10
        color: 1,0,0,0
        id: shadowEmail
        canvas.before:
            Color:
                rgba: self.color
            Line:
                rectangle: email.pos[0] - 2, email.pos[1] -2, email.size[0] + 4, email.size[1] + 4
                width: 1.5
    ButtonBlack:
        pos: 412, 230
        text: 'suscribirme'
        on_release: root.suscribe(email.text, self)
    Basiclabel:
        height: 100
        y: 100
        bold: True
        text: 'Encuentranos en'
    Image:
        size_hint: None, None
        pos: 537, 50 
        width: 200
        source: 'assets/playstorelogo.png'
        
    Image:
        size_hint: None, None
        pos: 287, 50 
        width: 200
        source: 'assets/appstorelogo.png'

<Basiclabel@Label>
    color: 0.8, 0.8, 0.8, 1
    size_hint: None, None
    width: 824
    x: 100
    font_size: '24dp'
    text_size: self.size
    halign: 'center'
    valign: 'middle'
    font_size: '24dp'
'''

Builder.load_string(string)

class EndScreen(Screen):

    def suscribe(self, email, btn):
        if email:
            url = 'https://riedmusicapp.com/examination/examen_ua/suscribe'
            response = requests.post(url, json={'email':email})
            print(response.text)
            self.remove_widget(self.ids.email)
            self.remove_widget(btn)
            self.remove_widget(self.ids.shadowEmail)
            self.ids.labelUseful.text = 'Gracias! Pronto nos contactaremos contigo.'
            self.ids.labelUseful.pos[1] -= 100
        else:
            self.ids.shadowEmail.color = (1,0,0,1)


