def _lstsq(a, b):
  # faster than jsp.linalg.lstsq
  a2 = _dot(a.T.conj(), a)
  b2 = _dot(a.T.conj(), b)
  return jsp.linalg.solve(a2, b2, assume_a='pos')
