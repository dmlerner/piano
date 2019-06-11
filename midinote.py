
class MidiNote:

  note_distance_weight = 1
  start_distance_weight = 1
  duration_distance_weight = 1

  deletion_weight = 1 + 2**-3

  def __init__(self, note, start, duration):
    self.note = int(note)
    self.start = start
    self.duration = duration


  def distance(self, other):
    return self.note_distance(other) * self.note_distance_weight +\
        self.start_distance(other) * self.start_distance_weight +\
        self.duration_distance(other) * self.duration_distance_weight

  def note_distance(self, other):
    return abs(self.note - other.note)

  def start_distance(self, other):
    return abs(self.start - other.start)

  def duration_distance(self, other):
    return abs(self.duration - other.duration)

  def deletion_cost(self):
    return self.duration * self.deletion_weight

  def __repr__(self):
    return 'Note(' + ', '.join(map(str, [self.note, self.start, self.duration])) + ')'

  def __lt__(self, other):
    return self.start < other.start

  def __iter__(self):
    yield self.note
    yield self.start
    yield self.duration

def main():
  a = MidiNote(20, 0, 1)
  b = MidiNote(21, 1, 3)
  print a.distance(b)
  print a.deletion_cost()
  print a < b
  print a

if __name__ == '__main__':
  main()
