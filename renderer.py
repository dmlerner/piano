import music21
import threading
import os
import time

class Renderer:

    def __init__(self, stream=None, writer='lily.svg', viewer='eom', path='./piano'):
        self.stream = stream or music21.stream.Stream()
        self.writer = writer
        self.viewer = viewer
        self.path = path

        music21.environment.set('vectorPath', '/usr/bin/' + viewer)

    def write(self):
        print 'writing...'
        self.stream.write(self.writer, fp=self.path)

    def loop_write(self, frames=float('inf'), delay=0):
        frame = 0
        while frame < frames:
            print 'frame= ', frame
            frame += 1
            self.write()
            #time.sleep(delay)

    def view(self):
        print 'calling os.system'
        view_command = self.viewer + ' ' + self.path + '.svg'
        #threading.Thread(target=os.system, args=(view_command)).start()
        os.system(view_command)
        print 'called os.system'

    def animate(self, frames=float('inf'), delay=0):
        threading.Thread(target=self.loop_write, args=(frames, delay)).start()
#        time.sleep(1)
        print '*'*20 + 'preview' + '*'*20
        self.view()
        print '*'*20 + 'end of animate' + '*'*20

def main():
    r = Renderer()
    def toggle_color(s, note):
        for i in range(10):
            print i, '.'*30
            print
            time.sleep(1)
            #note.color = ['#00ff00', '#ff00ff'][i%2]
            note.style.color = ['red', 'green'][i%2]
    f = music21.note.Note('F5')
    r.stream.append(f)
    f.pitch.name = 'a'
    f.style.color = 'blue'
#    r.write()
#    r.view()
    #toggle_color(r.stream, f)
    threading.Thread(target=toggle_color, args=(r.stream, f)).start()
    r.animate()
    print '*'*20 +  'post animate' +  '*'*20

main()
