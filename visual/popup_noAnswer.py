from kivy.uix.modalview import ModalView
from kivy.lang import Builder

string = '''
<NoAnswer>
    id: noAnswer
    auto_dismiss: False
    size_hint: None, None
    size: 600, 450
    pos_hint: {'center_x':0.5, 'center_y':0.5}
    RelativeLayout:
        canvas.before:
            Rectangle:
                size:self.size
                pos: 0,0
                source: "assets/bk.jpg"
        Widget:
            size_hint: None, None
            pos: 0, 150
            size: 600, 200
            canvas:
                Color:
                    rgba: 0,0,0,0.3
                Rectangle:
                    size: self.size
                    pos: self.pos
        Label:
            font_size: '24dp'
            size_hint: 1, None
            height: 90
            text: 'ATENCIÓN'
            pos: 0, 360
        Label:
            font_size: '24dp'
            size_hint: None, None
            size: 460, 200
            pos: 70, 150
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            text: 'No ha seleccionado ninguna respuesta a esta pregunta. Puede hacerlo ahora, o puede ir a la siguiente pregunta y volver más tarde con el botón "Anterior".'
        ButtonBlack: 
            text: 'ACEPTAR'
            pos_hint: {}
            pos: 200, 50
            on_release: noAnswer.dismiss()
'''

Builder.load_string(string)

class NoAnswer(ModalView):
    pass

if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.relativelayout import RelativeLayout
    from kivy.clock import Clock

    class myApp(App):

        def build(self):
            rl = RelativeLayout()
            Clock.schedule_once(self.launch, 2)
            return rl

        def launch(self, clock):
            view = NoAnswer()
            view.open()

    myApp().run()


