import midinote
import aligner

def argmin(x):
  return x.index(min(x))

def get_minimum_and_argmin(x):
  argmin = None
  minimum = float('inf')
  for i, X in enumerate(x):
    if X < minimum:
      argmin = i
      minimum = X
  return minimum, argmin

def parse(filename):
  with open(filename) as f:
    lines = f.readlines()
  notes = []
  for line in lines:
    note, start = map(float, line.split())
    notes.append(midinote.MidiNote(note, start, 1))
  return notes

def fix_offset(notes):
  # first note starts at time 0
  # hm, but when we align against some section, it seems like we want to treat offset from first note as zero
  # does that mess up dp?
  # for now, just set the weight for starts to zero
  offset = notes[0].start
  for note in notes:
    note.start = note.start - offset

def set_tempo(notes, tempo):
  # measure time in seconds
  # would beats be more convennient?
  # 3.3s for 30 "beats"
  # 30/(3.3/60) = 545.45 bpm
  # clearly these are sixteenth notes
  # or whatever I did in teh sample
  # to line up first 32 data
  for note in notes:
    note.start /= tempo / 60

def round_starts(notes, time_signature_denominator=4, time_units_per_beat=4):
  # with the defaults, we report times in sixteenth notes, where the quarter note gets the beat
  scale_factor = time_signature_denominator * time_units_per_beat
  for note in notes:
    old = note.start * scale_factor
    note.start = int(round(scale_factor * note.start))
    deviation = old - note.start
    #print old, note.start, deviation

def test_sonatina():
  midinote.MidiNote.start_distance_weight = 1
  midinote.MidiNote.deletion_weight = 10
  a = parse('sonatina-play.csv')
  b = parse('sonatina-score.csv')
  fix_offset(a)
  fix_offset(b)
  n = min(len(a), len(b))
  tempo = (b[n-1].start / a[n-1].start) * 60
  set_tempo(b, tempo)
  assert aligner.get_note_uses(a[3:7], b) == [3, 4, 5, 6]
  assert aligner.get_note_uses(a, b) == range(len(b)) + [None]*(len(a) - len(b))
  del a[4]
  assert aligner.get_note_uses(a, b) == range(4) + range(5, len(b)) + [None]*(len(a) - len(b) + 1)
  a[6], a[7] = a[7], a[6]
  assert aligner.get_note_uses(a, b) == range(4) + range(5, len(b)) + [None]*(len(a) - len(b) + 1)
  a[6].start, a[7].start = a[7].start, a[6].start
  midinote.MidiNote.deletion_weight = .5
  assert aligner.get_note_uses(a, b) == range(4) + [5, 6, None, 7] + range(9, len(b)) + [None]*(len(a) - len(b) + 1) # make sure this seems like the right answer...

def align(filename, tempo):
  # returns with time measured in quarter notes at $tempo, starting from zero
  with open(filename) as f:
    lines = f.readlines()
  notes = []
  for line in lines:
    note, start = line.split()
    notes.append(midinote.MidiNote(int(note), float(start), 1))
  print lines[:5]
  print lines[-5:]
  #notes = [midinote.MidiNote(note, start, 1) for line in lines for (note, start, _) in line.split()] # fix up durations some day?
  fix_offset(notes)
  set_tempo(notes, tempo)
  round_starts(notes) # plumb so as not to use defaults
  return notes

#print notes

def main():
  notes = align('minuet.csv', 80)
  test_sonatina()

if __name__ == '__main__':
  main()
