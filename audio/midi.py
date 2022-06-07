from midiutil import MIDIFile
from ried.note.note_generator import Note, Silence
from ried.chord.chord_generator import Chord
import os

def create_midiFile(content, tempo=84, program=None, channel=None, volume=[100], filename='question'):
    if not channel:
        channel = [0]
    while len(channel) < len(content):
        channel.append(len(channel))
    if program:
        while len(program) < len(content):
            program.append(0)
    if not volume:
        volume = [100]
    while len(volume) < len(content):
        volume.append(100)


    archivo = MIDIFile(numTracks=len(content))
    for tr in range(len(content)):
        time = 0
        archivo.addTempo(track=tr, time=0, tempo=tempo)
        if program:
           archivo.addProgramChange(tr, channel=channel[tr], time=time, program=program[tr])
        for beat in content[tr].content:
            for fig in beat.content:
                if isinstance(fig, (Note, Silence)):
                    add_note(archivo, fig, tr, channel, volume[tr], time)
                elif isinstance(fig, Chord):
                    for note in fig.content:
                        add_note(archivo, note, tr, channel, volume[tr], time)
                time += fig.duration
    time = add_coda(archivo, time)
    filename = os.sep.join(['audio', filename + '.mid'])
    with open(filename, "wb") as f:
        archivo.writeFile(f)
    time = 60/84*(time-3) 
    return filename, time

def add_note(archivo, fig, tr, channel, volume, time):
    if isinstance(fig, Note):
        archivo.addNote(track=tr, channel=channel[tr], pitch=fig.midi_number, time=time, duration=fig.duration, volume=volume)
    elif isinstance(fig, Silence):
        archivo.addNote(track=tr, channel=channel[tr], pitch=0, time=time, duration=fig.duration, volume=0)
  
def add_coda(archivo, time):
    for x in range(4):    
        archivo.addNote(track=0, channel=0, pitch=0, time=time, duration=1, volume=0)
        time += 1
    return time


if __name__ == '__main__':
    
    from ried.bar.bar_generator import Bar
    content = []
    redo = []
    distribution = []
    for pulso in range(4):
        if pulso == 0:
            content.append('C5')
        else:
            content.append('G4')
        content.append('D4')
        redo.extend(['E2','E2'])
        distribution.append([0.5,0.5])
    #bar = Bar('4-4', content=[['B4', 'D5'],'E5', 'D4', 'B4', 'A4', 'G4', 'A4'], subdivision='distribution', distribution=[[0.5, 0.5],[1], [-1],[0.25,-0.25, 0.25, 0.25]])
    bar = Bar('4-4', content=content, subdivision='distribution', distribution=distribution)
    #bar1 = Bar('4-4', content=redo, subdivision='distribution', distribution=distribution)
    create_midiFile(content=[bar], program=[115, 0], channel=[0,9], volume=[100,0])



