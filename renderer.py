import music21
import threading
import os
import time
import re
import pdb

extension = '.svg'

class Renderer:

    def __init__(self, stream=None, writer='lily.ly', viewer='svg_refreshview.py', path='sheetmusic'):
        self.stream = stream or music21.stream.Stream()
        self.writer = writer
        self.viewer = viewer
        self.path = path + str(time.time())

    def write(self):
        self.stream.write(self.writer, fp=self.path)
        with open(self.path) as f:
            ly_lines = f.readlines()
        #pdb.set_trace()
        print ''.join(ly_lines)
        print '.'*20
        self.remove_lily_header(ly_lines)
        print ''.join(ly_lines)
        print '.'*20
        self.fix_colors(ly_lines)
        print ''.join(ly_lines)
        print
        with open(self.path + '.ly', 'w') as f:
            f.write(''.join(ly_lines))
        os.system('lilypond -dbackend=svg ' + self.path + '.ly')

    def remove_lily_header(self, ly_lines):
        for i, line in enumerate(ly_lines):
            if 'header' in line:
                break
        del ly_lines[:i+1]

    def fix_colors(self, ly_lines):
        for i, line in enumerate(ly_lines):
            if '\color' in line:
                parsed = head, r, g, b, tail = re.search(r'(.*)\color "(.*) (.*) (.*)" (.*)', line).groups()
                ly_lines[i] = '%s \override NoteHead #\'color = #(rgb-color %s %s %s) %s' % (head[:-2], r, g, b, tail)

    def loop_write(self, frames=float('inf'), delay=0):
        frame = 0
        while frame < frames:
            print 'frame ', frame
            frame += 1
            self.write()
            time.sleep(delay)

    def view(self):
        view_command = 'python ' + self.viewer + ' ' + self.path + extension
        print 'view_command: ', view_command
        os.system(view_command)

    def animate(self, frames=float('inf'), delay=0):
        return
        threading.Thread(target=self.loop_write, args=(frames, delay)).start()
        while not os.path.isfile(self.path + extension):
            print 'path not found ' + self.path + extension
            time.sleep(.1)
        self.view()

def main():
    r = Renderer()
    #use_rgb = True
    use_rgb = True
    def toggle_color(note):
        for i in range(100):
            time.sleep(.2)
            #raw_input('enter to toggle color')
            note.style.color = [['green1', 'green2'], ['.5 0 0', '0 .5 0']][use_rgb][i%2]
    note = music21.note.Note('F5')
    note.style.color = ['blue', '0 0 .5'][use_rgb]
    r.stream.append(note)
    r.write()
    1/0
    threading.Thread(target=toggle_color, args=(note,)).start()
    r.animate()

main()
