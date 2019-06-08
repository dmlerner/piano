


























import matplotlib
import matplotlib.pyplot
import numpy
import time

class Visualizer:
    def __init__(self, n_lines=1, measures_per_line=1, time_signature=(4,4)):
        # time signature is a tuple, eg (3,4) for 3 beats per measure, quarter notes gets beat
        self.n_lines = n_lines
        self.measures_per_line = measures_per_line
        self.time_signature = time_signature

        matplotlib.pyplot.ion()
        self.figure = matplotlib.pyplot.figure()
        self.axis = self.figure.add_subplot(111)
        self.axis.set_xlim(0, 1)
        self.axis.set_ylim(0, 1)
        self.line, = self.axis.plot([], [])
        self.figure.show()
        #matplotlib.pyplot.show()

    def update(self):
        self.line.set_data(numpy.random.random((10,1)), numpy.random.random((10, 1)))
        print type(self.line)
        x = []
        #self.figure.canvas.draw()

v = Visualizer()
for i in range(4):
    v.update()
    matplotlib.pyplot.pause(.4)

raw_input()
