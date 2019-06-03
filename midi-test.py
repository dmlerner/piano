import mido
import time

class PianoListener:
  def __init__(self):
    self.start_time = time.time()
    self.port = PianoListener.get_port()

  @staticmethod
  def get_port(port_name=u'USB func for MIDI:USB func for MIDI MIDI 1 36:0'):
    port_names = mido.get_output_names()
    print port_names
    assert port_name in port_names # edit distance pull from options? lol
    port = mido.open_input(port_name)
    return port

  def __iter__(self):
    for message in self.port:
      yield message

  def listen(self):
    for message in self:
      self.handle_message(message)

  def handle_message(self, message):
    if message.type == 'note_on':
      note = Note(message.note, self.now())
      print note

  def now(self):
    return time.time() - self.start_time

class Note:
  def __init__(self, note, start):
    self.note = note
    self.start = start
    self.rythmic_accuracy_factory = 1

  def distance(self, other):
    return abs(self.note - other.note) + abs(self.start - other.start) * self.rythmic_accuracy_factory

  def __str__(self):
    return ' '.join(map(str, (self.note, self.start)))

class PianoPlayer:

  @staticmethod
  def convert_csv_to_notes(filename='sonatina-score.csv'):
    lines = [line.split() for line in open(filename).readlines()]
    notes = [Note(note, start) for note, start in lines]
    return notes

  @staticmethod
  def play_file(filename='sonatina-score.csv'):
    PianoPlayer.play_notes(PianoPlayer.convert_csv_to_notes(filename))

  @staticmethod
  def play_notes(notes):
    # might need to be in a separate thread
    piano = u'USB func for MIDI:USB func for MIDI MIDI 1 32:0' # the literal kdp-110 piano
    piano_port = mido.open_output(piano)
    notes.sort(lambda note: note.start)
    for note in notes:
      piano_port.send(mido.Message(note=note.note))



piano_listener = PianoListener()
piano_listener.listen()
