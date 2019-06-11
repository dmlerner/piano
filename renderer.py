import music21
import threading
import os
import time
import re
import pdb

class Renderer:

    def __init__(self, stream=None, writer='lily.ly', viewer='svg_refreshview.py', path='sheetmusic'):
        self.stream = stream or music21.stream.Stream()
        self.writer = writer
        self.viewer = viewer
        self.path = path #+ str(time.time())

    def write(self):
        self.stream.write(self.writer, fp=self.path)
        with open(self.path) as f:
            ly_lines = f.readlines()
        self.remove_lily_header(ly_lines)
        self.fix_colors(ly_lines)
        ly_lines.insert(0, r'\version "2.18.2"')
        with open(self.path + '.ly', 'w') as f:
            f.write(''.join(ly_lines))
        write_lily_command = 'lilypond -dbackend=svg ' + self.path + '.ly'
        threading.Thread(target=os.system, args=(write_lily_command,)).start()

    def remove_lily_header(self, ly_lines):
        for i, line in enumerate(ly_lines):
            if 'header' in line:
                break
        del ly_lines[:i+1]

    def fix_colors(self, ly_lines):
        for i, line in enumerate(ly_lines):
            if '\color' in line:
                head, r, g, b, tail = re.search(r'(.*)\color "(.*) (.*) (.*)" (.*)', line).groups()
                ly_lines[i] = '%s \override NoteHead #\'color = #(rgb-color %s %s %s) %s' % (head[:-2], r, g, b, tail)

    def loop_write(self, frames=float('inf'), delay=0):
        frame = 0
        while frame < frames:
            frame += 1
            self.write()
            time.sleep(delay)

    def view(self):
        view_command = 'python ' + self.viewer + ' ' + self.path + '.svg'
        os.system(view_command)

    def animate(self, frames=float('inf'), delay=0):
        threading.Thread(target=self.loop_write, args=(frames, delay)).start()
        while not os.path.isfile(self.path + '.svg'):
            time.sleep(.1)
        self.view()

def main():
    def toggle_color(note):
        for i in range(100):
            time.sleep(.2)
            note.style.color = ['.5 0 0', '0 .5 0'][i%2]
    note = music21.note.Note('F5')
    note.style.color = '0 0 .5'
    r = Renderer()
    r.stream.append(note)
    r.write()
    threading.Thread(target=toggle_color, args=(note,)).start()
    r.animate()

if __name__ == '__main__':
    main()
