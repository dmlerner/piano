import random
import midinote
import util

def get_distance_dp(a, b):
  dp = [[(float('inf'), None)]*(len(b)+1) for j in range(len(a)+1)]
  dp[0][0] = 0, None # perfect match between empty sequences

  PAIR_A_AND_B = 0
  DELETE_A = 1
  DELETE_B = 2

  # consider distances of a[:i] to b[:j]

  for i in range(1, len(a)+1):
    dp[i][0] = dp[i-1][0][0] + a[i-1].deletion_cost(), DELETE_A # using none of b, have to delete a
  for j in range(1, len(b)+1):
    dp[0][j] = dp[0][j-1][0] + b[j-1].deletion_cost(), DELETE_B


  for i in range(1, len(a)+1):
    for j in range(1, len(b)+1):
      pair_a_and_b = dp[i-1][j-1][0] + a[i-1].distance(b[j-1])
      delete_a = dp[i-1][j][0] + a[i-1].deletion_cost()
      delete_b = dp[i][j-1][0] + b[j-1].deletion_cost()

      options = pair_a_and_b, delete_a, delete_b

      dp[i][j] = util.get_minimum_and_argmin(options)

  return dp

def test_get_distance_dp():
  a = midinote.MidiNote(0, 0, 1)
  b = midinote.MidiNote(1, 0, 1)
  A = a, a, a
  B = b, b, a, b, a
  distance_dp = get_distance_dp(A, B)
  correct_dp = [
    [(0, None), (1.125, 2), (2.25, 2), (3.375, 2), (4.5, 2), (5.625, 2)],
    [(1.125, 1), (1, 0), (2.125, 0), (2.25, 0), (3.375, 2), (4.5, 0)],
    [(2.25, 1), (2.125, 0), (2, 0), (2.125, 0), (3.25, 0), (3.375, 0)],
    [(3.375, 1), (3.25, 0), (3.125, 0), (2, 0), (3.125, 0), (3.25, 0)]
  ]
  assert distance_dp == correct_dp

def get_optimal_alignment(a, b):
  optimal = float('inf'), float('inf')
  optimal_bounds = None
  outer_dp = []
  for k in range(len(b)+1):
    dp = get_distance_dp(a, b[k:])
    sub_dp = [dp[len(a)][j] for j in range(len(b)+1-k)]
    outer_dp.append(dp)
    optimal_j = util.argmin(sub_dp)
    if sub_dp[optimal_j] < optimal:
      optimal = sub_dp[optimal_j]
      optimal_bounds = k, optimal_j
  b_bounds = optimal_bounds[0], optimal_bounds[0] + optimal_bounds[1]
  # we return a dp of distances to sections of b of length equal to optimal length
  # and then never use it.
  # we do have the full rectangle in outer_dp if we ever wanted it
  return outer_dp, b_bounds, b[slice(*b_bounds)], optimal[0]

def test_get_optimal_alignment():
  a = midinote.MidiNote(0, 0, 1)
  b = midinote.MidiNote(1, 0, 1)
  A = a, a, a
  B = b, b, a, b, a
  dp, b_bounds, b_slice, optimal = get_optimal_alignment(A, B)
  correct_dp = [ # outermost index is length substring of b (k)
      [[(0, None), (1.125, 2), (2.25, 2), (3.375, 2), (4.5, 2), (5.625, 2)], # then enumerate prefixes of a (i)
      [(1.125, 1), (1, 0), (2.125, 0), (2.25, 0), (3.375, 2), (4.5, 0)], # then enumerate prefixes of b[k:] (j)
      [(2.25, 1), (2.125, 0), (2, 0), (2.125, 0), (3.25, 0), (3.375, 0)],
      [(3.375, 1), (3.25, 0), (3.125, 0), (2, 0), (3.125, 0), (3.25, 0)]], # must pick a score from i == 3 row, ie, use all of a
      # so for this k=0 block, optimal is 2

      [[(0, None), (1.125, 2), (2.25, 2), (3.375, 2), (4.5, 2)],
      [(1.125, 1), (1, 0), (1.125, 0), (2.25, 2), (3.375, 0)],
      [(2.25, 1), (2.125, 0), (1, 0), (2.125, 0), (2.25, 0)],
      [(3.375, 1), (3.25, 0), (2.125, 0), (2, 0), (2.125, 0)]],
      # and we do only exactly as well by using b[1:]

      [[(0, None), (1.125, 2), (2.25, 2), (3.375, 2)],
      [(1.125, 1), (0, 0), (1.125, 2), (2.25, 0)],
      [(2.25, 1), (1.125, 0), (1, 0), (1.125, 0)],
      [(3.375, 1), (2.25, 0), (2.125, 0), (1, 0)]],
      # but using b[2:] produces optimal result

      [[(0, None), (1.125, 2), (2.25, 2)],
      [(1.125, 1), (1, 0), (1.125, 0)],
      [(2.25, 1), (2.125, 0), (1, 0)],
      [(3.375, 1), (3.25, 0), (2.125, 0)]],
      # but going shorter is worse!

      [[(0, None), (1.125, 2)],
      [(1.125, 1), (0, 0)],
      [(2.25, 1), (1.125, 0)],
      [(3.375, 1), (2.25, 0)]],

      [[(0, None)],
      [(1.125, 1)],
      [(2.25, 1)],
      [(3.375, 1)]]
  ]

  assert b_bounds == (2, 5)
  assert b_slice == (a, b, a)
  assert optimal == 1

  c = midinote.MidiNote(4, 0, 1)
  C = c, c, a, c, a
  dp, c_bounds, c_slice, optimal = get_optimal_alignment(A, C)

  assert c_bounds == (2, 3)
  assert optimal == 2.25

def get_note_uses(a, b):
  # sorts a and b
  # because otherwise the return mapping is hard to interpret
  # this way a[i] is paired with b[get_note_uses(a, b)[i]]
  assert type(a) is list
  assert type(b) is list
  a.sort()
  b.sort()
  optimal_alignment = get_optimal_alignment(a, b)
  b_slice = optimal_alignment[2]
  dp = get_distance_dp(a, b_slice)
  pairings = [None]*(len(dp)-1) # a_index: b_index or None for delete
  i = len(dp) - 1
  j = len(dp[0]) - 1

  while i > 0 and j > 0:
    if dp[i][j][1] == 0:
      i -= 1
      j -= 1
      pairings[i] = j
    if dp[i][j][1] == 1:
      i -= 1
      pairings[i] = None
    if dp[i][j][1] == 2:
      j -= 1

  return [pairing + optimal_alignment[1][0] if pairing is not None else None for pairing in pairings]

def test_get_note_uses():
  a = midinote.MidiNote(0, 0, 1)
  b = midinote.MidiNote(4, 0, 1)
  A = [a, a, a]
  B = [b, b, a, b, a]
  pairings = get_note_uses(A, B)
  assert pairings == [None, None, 2]

  I = range(12)
  scale = [midinote.MidiNote(i, i, 1) for i in I]
  played = [midinote.MidiNote(i, i-.05+.1*random.random(), .95+.1*random.random()) for i in I]
  mistaken_note = midinote.MidiNote(100, 4.3, 300)
  played.append(mistaken_note)
  played.insert(0, midinote.MidiNote(100, -54, 300))
  pairings = get_note_uses(played, scale)
  # notice that mistaken note shows up in the time ordered position in correct_pairings as None
  correct_pairings = [None, 0, 1, 2, 3, 4, None, 5, 6, 7, 8, 9, 10, 11]
  assert pairings == correct_pairings

  played_with_indices = list(enumerate(played))
  scale_with_indices = list(enumerate(scale))
  random.shuffle(played_with_indices)
  random.shuffle(scale_with_indices)
  pairings = get_note_uses([p for i, p in played_with_indices] , [s for i, s in scale_with_indices])
  assert get_note_uses(played, scale) == correct_pairings

def test_algorithms():
  midinote.MidiNote.note_distance_weight = 1
  midinote.MidiNote.start_distance_weight = 1
  midinote.MidiNote.duration_distance_weight = 1

  midinote.MidiNote.deletion_weight = 1 + 2**-3

  test_get_distance_dp()
  test_get_optimal_alignment()
  test_get_note_uses()
  print 'all aligner algorithm tests pass'

def main():
  test_algorithms()

if __name__ == '__main__':
  main()
