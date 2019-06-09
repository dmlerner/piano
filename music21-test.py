from music21 import *
import time
import threading
import sys
import os

def toggle_color(note):
    for i in range(1000):
        print i, '.'*30
        print
        #time.sleep(2)
        #note.color = ['#00ff00', '#ff00ff'][i%2]
        note.style.color = ['red', 'green'][i%2]
        s.write('lily.svg', fp='./test')

image_viewer = 'eom'
environment.set('vectorPath', '/usr/bin/' + image_viewer)
s = stream.Stream()
f = note.Note('F5')
s.append(f)
f.pitch.name = 'a'
f.style.color = 'blue'
path = s.write('lily.svg', fp='./test')
print path
threading.Thread(target=toggle_color, args=(f,)).start()
os.system(image_viewer + ' ' + path)
#toggle_color(f)


#toggle_color(f)
#threading.Thread(target=f.show, args=('lily.svg',)).start()
