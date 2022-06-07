from kivy.clock import Clock
from functools import partial

class Timer:

    def __init__(self, parent=None, time=1):
        self.questScreen = parent
        
        self.left_time = time * 60 * 1000
        self.state = False
        self.trig = Clock.create_trigger(partial(self.counter), 1)

    def startTimer(self):
        self.state = True
        self.trig()

    def counter(self, *clock):
        if self.state:
            self.left_time -= 1000
            minuntes = '{:0>2}'.format(self.left_time//60000)
            seconds = '{:0>2}'.format(int(self.left_time/1000)%60)
            text = f'{minuntes}:{seconds}'
            self.questScreen.ids.timer.text = text
            if self.left_time <= 0:
                self.state = False
                self.questScreen.sm.show_prompSend(time=True)
            else:
                self.trig()
            

    def stopTimer(self):
        self.state = False


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.label import Label

    class myApp(App):
        
        def build(self):
            t = Timer()
            t.startTimer()
            return Label()

    myApp().run()

