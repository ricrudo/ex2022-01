from kivy.uix.button import Button
from kivy.lang import Builder

string = '''
<ButtonBlack>
    font_size: '24dp'
    size_hint: None, None
    size: 200, 50
    color: 1,1,1,1
    background_color: (0,0,0,1) if self.disabled == False else (1,1,1,0)
    disabled_color: 0,0,0,0  

<ButtonHold>
    selected: False
    background_normal: ''
    color: 0,0.5,0.5,1
    font_size: '24dp'
    size_hint: None, None
    size: 200, 50
    bold: True
    background_color: 1,1,1,0.2
    canvas:
        Color:
            rgba:0,0.5,0.5,1
        Line:
            width: 1.3
            rectangle: self.pos[0], self.pos[1], 200, 50

<ButtonPlaySound>
    background_normal: ''
    size_hint: None, None
    size: 200, 50
    background_color: (0,0,0,0.4) if self.disabled == True else (0,0,0,1)
    background_disabled_normal: ''
    canvas.after:
        Color:
            rgba: (1,1,1,0.5) if self.disabled == True else (1,1,1,1)
        Triangle:
            points: self.pos[0] + 83, self.pos[1] + 8, self.pos[0] + 83, self.pos[1] + 42, self.pos[0] + 116, self.pos[1] + 25

<Border@Widget>
    size_hint: None, None
    size: 1024, 90
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size:self.size
            pos:self.pos
            source: "assets/borde.png"
'''

Builder.load_string(string)

class ButtonBlack(Button):

    def on_press(self):
        self.background_color = 0.1,0,0.1,0.7
    
    def on_release(self):
        self.background_color = 0,0,0,1


class ButtonHold(Button):

    def on_press(self):
        self.background_color = 0.1,0,0.1,0.1
    
    def on_release(self):
        self.background_color = 0,0.5,0.5,1
        self.color = 1,1,1,1
        self.selected = True

    def liberate(self):
        self.background_color = 1,1,1,0.2
        self.color = 0,0.5,0.5,1
        self.selected = False

class ButtonPlaySound(Button):

    def on_release(self):
        self.disabled = True
    pass
