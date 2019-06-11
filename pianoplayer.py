import mido
import time
import sys

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

def main():
  piano_listener = PianoPlayer()
  piano_player.play_file()

if __name__ == '__main__':
  main()
