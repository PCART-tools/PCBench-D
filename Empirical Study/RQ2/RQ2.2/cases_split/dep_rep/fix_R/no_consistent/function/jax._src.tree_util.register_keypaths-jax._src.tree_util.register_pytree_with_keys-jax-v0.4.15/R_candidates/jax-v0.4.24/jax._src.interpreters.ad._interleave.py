def _interleave(xs, ys):
  assert len(xs) == len(ys)
  return [e for pair in zip(xs, ys) for l in pair for e in l]
