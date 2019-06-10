import music21
import threading
import os
import time

extension = '.svg'

class Renderer:

    def __init__(self, stream=None, writer='lily'+extension, viewer='svg_refreshview.py', path='./piano'):
        self.stream = stream or music21.stream.Stream()
        self.writer = writer
        self.viewer = viewer
        self.path = path #+ str(time.time())

        '''
        music21.environment.set('vectorPath', '/usr/bin/' + viewer)
        music21.environment.set('musicxmlPath', '/usr/bin/' + viewer)
        music21.environment.set('graphicsPath', '/usr/bin/' + viewer)
        '''


    def write(self):
        self.stream.write(self.writer, fp=self.path)

    def loop_write(self, frames=float('inf'), delay=0):
        frame = 0
        while frame < frames:
            frame += 1
            self.write()
            time.sleep(delay)

    def view(self):
        view_command = 'python ' + self.viewer + ' ' + self.path + extension
        print 'view_command: ', view_command
        os.system(view_command)

    def animate(self, frames=float('inf'), delay=0):
        threading.Thread(target=self.loop_write, args=(frames, delay)).start()
        while not os.path.isfile(self.path + extension):
            print 'path not found ' + self.path + extension
            time.sleep(.1)
        self.view()

def main():
    r = Renderer()
    use_rgb = False
    def toggle_color(note):
        for i in range(100):
            time.sleep(.2)
            #raw_input('enter to toggle color')
            note.style.color = [['red', 'green'], ['#ff0000', '#00ff00']][use_rgb][i%2]
    note = music21.note.Note('F5')
    r.stream.append(note)
    note.style.color = ['blue', '#0000ff'][use_rgb]
    threading.Thread(target=toggle_color, args=(note,)).start()
    r.animate()

main()
